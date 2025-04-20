import logging
import lzma
import pickle
import sqlite3
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import NamedTuple, Optional, Union

from evernote.edam.type.ttypes import LinkedNotebook, Note, Notebook

from evernote_backup.config import CURRENT_DB_VERSION
from evernote_backup.evernote_types import Reminder, Task
from evernote_backup.log_util import log_format_note, log_format_notebook

logger = logging.getLogger(__name__)


class NoteForSync(NamedTuple):
    guid: str
    title: str
    linked_notebook_guid: Optional[str]


DB_SCHEMA = """CREATE TABLE IF NOT EXISTS notebooks(
                        guid TEXT PRIMARY KEY,
                        name TEXT,
                        stack TEXT
                    );
                    CREATE TABLE IF NOT EXISTS notebooks_linked(
                        guid TEXT PRIMARY KEY,
                        notebook_guid TEXT,
                        usn INT DEFAULT 0
                    );
                    CREATE TABLE IF NOT EXISTS notes(
                        guid TEXT PRIMARY KEY,
                        title TEXT,
                        notebook_guid TEXT,
                        is_active BOOLEAN,
                        raw_note BLOB
                    );
                    CREATE TABLE IF NOT EXISTS tasks(
                        guid TEXT PRIMARY KEY,
                        note_guid TEXT,
                        raw_task BLOB
                    );
                    CREATE TABLE IF NOT EXISTS reminders(
                        guid TEXT PRIMARY KEY,
                        task_guid TEXT,
                        raw_reminder BLOB
                    );
                    CREATE TABLE IF NOT EXISTS config(
                        name TEXT PRIMARY KEY,
                        value TEXT
                    );
                    CREATE INDEX IF NOT EXISTS idx_notes
                     ON notes(notebook_guid, is_active);
                    CREATE INDEX IF NOT EXISTS idx_notes_title
                     ON notes(title COLLATE NOCASE);
                    CREATE INDEX IF NOT EXISTS idx_notebooks_linked
                     ON notebooks_linked(guid, notebook_guid);
                    CREATE INDEX IF NOT EXISTS idx_notes_raw_null
                     ON notes(guid) WHERE raw_note IS NULL;
                    CREATE INDEX IF NOT EXISTS idx_tasks
                     ON tasks(note_guid);
                    CREATE INDEX IF NOT EXISTS idx_reminders
                     ON reminders(task_guid);
"""


class DatabaseResyncRequiredError(Exception):
    """Raise when database update requires resync"""


def initialize_db(database_path: Path) -> None:
    if database_path.exists():
        raise FileExistsError

    db = sqlite3.connect(database_path)

    with db as con:
        con.executescript(DB_SCHEMA)

    db.close()


class SqliteStorage:
    def __init__(self, database: Union[Path, sqlite3.Connection]) -> None:
        if isinstance(database, sqlite3.Connection):
            self.db = database
        else:
            if not database.exists():
                raise FileNotFoundError("Database file does not exist.")

            self.db = sqlite3.connect(database)
            self.db.row_factory = sqlite3.Row

    @property
    def config(self) -> "ConfigStorage":
        return ConfigStorage(self.db)

    @property
    def notes(self) -> "NoteStorage":
        return NoteStorage(self.db)

    @property
    def notebooks(self) -> "NoteBookStorage":
        return NoteBookStorage(self.db)

    @property
    def tasks(self) -> "TasksStorage":
        return TasksStorage(self.db)

    @property
    def reminders(self) -> "RemindersStorage":
        return RemindersStorage(self.db)

    def integrity_check(self) -> str:
        with self.db as con:
            cur = con.execute("PRAGMA integrity_check;")

            try:
                results = cur.fetchall()
            except sqlite3.Error as e:
                return str(e)

            return "\n".join(row[0] for row in results)

    def check_version(self) -> None:
        try:
            db_version = int(self.config.get_config_value("DB_VERSION"))
        except KeyError:
            db_version = 0

        if db_version != CURRENT_DB_VERSION:
            logger.info(
                f"Upgrading database version from {db_version} to {CURRENT_DB_VERSION}..."
            )
            self.upgrade_db(db_version)

    def upgrade_db(self, db_version: int) -> None:
        need_resync = False

        if db_version == 0:
            need_resync = True
            with self.db as con1:
                con1.execute("DROP TABLE notebooks;")
                con1.execute("DROP TABLE notes;")

                con1.executescript(DB_SCHEMA)

        if db_version < 3:
            with self.db as con2:
                con2.execute(
                    "CREATE INDEX IF NOT EXISTS idx_notes_title"
                    " ON notes(title COLLATE NOCASE);"
                )

        if db_version < 4:
            with self.db as con3:
                con3.execute(
                    "CREATE TABLE IF NOT EXISTS notebooks_linked("
                    " guid TEXT PRIMARY KEY,"
                    " notebook_guid TEXT,"
                    " usn INT DEFAULT 0"
                    " );"
                )
                con3.execute(
                    "CREATE INDEX IF NOT EXISTS idx_notebooks_linked"
                    " ON notebooks_linked(guid, notebook_guid);"
                )

        if db_version < 5:
            with self.db as con4:
                con4.execute(
                    "CREATE INDEX IF NOT EXISTS idx_notes_raw_null"
                    " ON notes(guid) WHERE raw_note IS NULL;"
                )

        if db_version < 6:
            self.config.set_config_value("last_connection_tasks", "0")

            with self.db as con5:
                con5.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS tasks(
                        guid TEXT PRIMARY KEY,
                        note_guid TEXT,
                        raw_task BLOB
                    );
                    CREATE TABLE IF NOT EXISTS reminders(
                        guid TEXT PRIMARY KEY,
                        task_guid TEXT,
                        raw_reminder BLOB
                    );
                    CREATE INDEX IF NOT EXISTS idx_tasks
                     ON tasks(note_guid);
                    CREATE INDEX IF NOT EXISTS idx_reminders
                     ON reminders(task_guid);
                    """
                )

        self.config.set_config_value("DB_VERSION", str(CURRENT_DB_VERSION))

        if need_resync:
            self.config.set_config_value("USN", "0")
            raise DatabaseResyncRequiredError


class NoteBookStorage(SqliteStorage):  # noqa: WPS214
    def add_notebooks(self, notebooks: Iterable[Notebook]) -> None:
        if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
            for nb in notebooks:
                nb_info = log_format_notebook(nb)
                logger.debug(f"Adding/updating notebook {nb_info}")

        with self.db as con:
            con.executemany(
                "replace into notebooks(guid, name, stack) values (?, ?, ?)",
                ((nb.guid, nb.name, nb.stack) for nb in notebooks),  # noqa: WPS441
            )

    def iter_notebooks(self) -> Iterator[Notebook]:
        with self.db as con:
            cur = con.execute(
                "select guid, name, stack from notebooks",
            )

            yield from (
                Notebook(
                    guid=row["guid"],
                    name=row["name"],
                    stack=row["stack"],
                )
                for row in cur
            )

    def get_notebook_notes_count(self, notebook_guid: str) -> int:
        with self.db as con:
            cur = con.execute(
                "select COUNT(guid) from notes"
                " where notebook_guid=? and is_active=1 and raw_note is not NULL",
                (notebook_guid,),
            )

            return int(cur.fetchone()[0])

    def expunge_notebooks(self, guids: Iterable[str]) -> None:
        with self.db as con:
            con.executemany("delete from notebooks where guid=?", ((g,) for g in guids))

    def add_linked_notebook(
        self, l_notebook: LinkedNotebook, notebook: Notebook
    ) -> None:
        if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
            logger.debug(
                f"Adding/updating linked notebook '{l_notebook.shareName}'"
                f" [{l_notebook.guid}] -> [{notebook.guid}]"
            )

        with self.db as con:
            con.execute(
                "replace into notebooks_linked(guid, notebook_guid) values (?, ?)",
                (l_notebook.guid, notebook.guid),
            )

    def get_notebook_by_linked_guid(self, l_notebook_guid: str) -> Notebook:
        with self.db as con:
            cur = con.execute(
                "select notebooks.guid, notebooks.name, notebooks.stack"
                " from notebooks_linked"
                " join notebooks"
                " on notebooks.guid=notebooks_linked.notebook_guid"
                " where notebooks_linked.guid=?",
                (l_notebook_guid,),
            )

            row = cur.fetchone()

            if row is None:
                raise ValueError(
                    f"No local notebooks found for linked notebook {l_notebook_guid}"
                )

            return Notebook(
                guid=row["guid"],
                name=row["name"],
                stack=row["stack"],
            )

    def get_linked_notebook_usn(self, l_notebook_guid: str) -> int:
        with self.db as con:
            cur = con.execute(
                "select usn from notebooks_linked where guid=?",
                (l_notebook_guid,),
            )

            res = cur.fetchone()

            if res is None:
                return 0

            return int(res[0])

    def set_linked_notebook_usn(self, l_notebook_guid: str, usn: int) -> None:
        with self.db as con:
            con.execute(
                "update notebooks_linked set usn=? where guid=?",
                (usn, l_notebook_guid),
            )

    def expunge_linked_notebooks(self, guids: Iterable[str]) -> None:
        with self.db as con:
            con.executemany(
                "delete from notebooks_linked where guid=?", ((g,) for g in guids)
            )


class NoteStorage(SqliteStorage):  # noqa: WPS214
    def add_notes_for_sync(self, notes: Iterable[Note]) -> None:
        if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
            for note in notes:
                n_info = log_format_note(note)
                logger.debug(f"Scheduling note for sync {n_info}")

        with self.db as con:
            con.executemany(
                "replace into notes(guid, title, notebook_guid) values (?, ?, ?)",
                ((n.guid, n.title, n.notebookGuid) for n in notes),
            )

    def add_note(self, note: Note) -> None:
        if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
            n_info = log_format_note(note)
            logger.debug(f"Adding/updating note {n_info}")

        note_deflated = lzma.compress(pickle.dumps(note))

        with self.db as con:
            con.execute(
                "replace into notes(guid, title, notebook_guid, is_active, raw_note)"
                " values (?, ?, ?, ?, ?)",
                (
                    note.guid,
                    note.title,
                    note.notebookGuid,
                    note.active,
                    note_deflated,
                ),
            )

        logger.debug(f"Added note [{note.guid}]")

    def iter_notes(self, notebook_guid: str) -> Iterator[Note]:
        for note_guid in self._get_notes_by_notebook(notebook_guid):
            with self.db as con:
                cur = con.execute(
                    "select title, guid, raw_note"
                    " from notes"
                    " where guid=? and raw_note is not NULL",
                    (note_guid,),
                )

                row = cur.fetchone()

                raw_note = self._get_raw_note(
                    row["title"],
                    row["guid"],
                    row["raw_note"],
                )

                if raw_note:
                    yield raw_note

    def iter_notes_trash(self) -> Iterator[Note]:
        with self.db as con:
            cur = con.execute(
                "select title, guid, raw_note"
                " from notes"
                " where is_active=0 and raw_note is not NULL"
                " order by title COLLATE NOCASE",
            )

            for row in cur:
                raw_note = self._get_raw_note(
                    row["title"],
                    row["guid"],
                    row["raw_note"],
                )

                if raw_note:
                    yield raw_note

    def check_notes(self, mark_corrupt: bool) -> Iterator[Optional[Note]]:
        with self.db as con:
            cur = con.execute(
                "select title, guid, raw_note from notes where raw_note is not NULL",
            )

            for row in cur:
                raw_note = self._get_raw_note(
                    row["title"],
                    row["guid"],
                    row["raw_note"],
                )

                if raw_note:
                    yield raw_note
                else:
                    if mark_corrupt:
                        logger.info(
                            f"Marking '{row['title']}' [{row['guid']}] note for re-download"
                        )
                        self._mark_note_for_redownload(row["guid"])
                    yield None

    def get_notes_for_sync(self) -> tuple[NoteForSync, ...]:
        with self.db as con:
            cur = con.execute(
                "select notes.guid, title, notebooks_linked.guid as l_notebook"
                " from notes"
                " left join notebooks_linked"
                " using (notebook_guid)"
                " where raw_note is NULL"
            )

            notes = (
                NoteForSync(
                    guid=row["guid"],
                    title=row["title"],
                    linked_notebook_guid=row["l_notebook"],
                )
                for row in cur.fetchall()
            )

            return tuple(notes)

    def expunge_notes(self, guids: Iterable[str]) -> None:
        with self.db as con:
            con.executemany("delete from notes where guid=?", ((g,) for g in guids))

    def expunge_notes_by_notebook(self, notebook_guid: str) -> None:
        with self.db as con:
            con.execute("delete from notes where notebook_guid=?", (notebook_guid,))

    def get_notes_count(self, is_active: bool = True) -> int:
        with self.db as con:
            cur = con.execute(
                "select COUNT(guid)"
                " from notes"
                " where is_active=? and raw_note is not NULL",
                (is_active,),
            )

            return int(cur.fetchone()[0])

    def _get_notes_by_notebook(self, notebook_guid: str) -> list[str]:
        """Due to wrong idx_notes index, SQLite creates a temporary table on
            from notes where notebook_guid=? and is_active=1
            order by title COLLATE NOCASE
        which may cause a memory leak. This method sorts notes alphabetically
        to prevent SQLite from creating a sort table."""

        with self.db as con:
            cur = con.execute(
                "select guid, title"
                " from notes"
                " where notebook_guid=? and is_active=1 and raw_note is not NULL",
                (notebook_guid,),
            )

            sorted_notes = sorted(cur, key=lambda x: x["title"])

            return [r["guid"] for r in sorted_notes]

    def _get_raw_note(
        self,
        note_title: str,
        note_guid: str,
        raw_note: bytes,
    ) -> Optional[Note]:
        try:
            return pickle.loads(lzma.decompress(raw_note))
        except Exception:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.exception(f"Note '{note_title}' [{note_guid}] is corrupt")

            logger.warning(f"Note '{note_title}' [{note_guid}] is corrupt")

        return None

    def _mark_note_for_redownload(self, note_guid: str) -> None:
        with self.db as con:
            con.execute(
                "update notes set raw_note=NULL, is_active=NULL where guid=?",
                (note_guid,),
            )


class TasksStorage(SqliteStorage):  # noqa: WPS214
    def add_tasks(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            self.add_task(task)

    def add_task(self, task: Task) -> None:
        logger.debug(f"Adding/updating task [{task.taskId}] note_id [{task.parentId}]")

        task_deflated = lzma.compress(task.to_json().encode("utf-8"))

        with self.db as con:
            con.execute(
                "replace into tasks(guid, note_guid, raw_task) values (?, ?, ?)",
                (task.taskId, task.parentId, task_deflated),
            )

    def iter_tasks(self, note_guid: str) -> Iterator[Task]:
        with self.db as con:
            cur = con.execute(
                "select guid, raw_task from tasks where note_guid=?",
                (note_guid,),
            )

            for row in cur:
                raw_task = self._get_raw_task(row["guid"], row["raw_task"])

                if raw_task:
                    yield raw_task

    def expunge_tasks(self, guids: Iterable[str]) -> None:
        with self.db as con:
            con.executemany("delete from tasks where guid=?", ((g,) for g in guids))

    def _get_raw_task(self, task_guid: str, raw_task: bytes) -> Optional[Task]:
        try:
            return Task.from_json(lzma.decompress(raw_task).decode("utf-8"))
        except Exception:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.exception(f"Task [{task_guid}] is corrupt")

            logger.warning(f"Task [{task_guid}] is corrupt")

        return None


class RemindersStorage(SqliteStorage):  # noqa: WPS214
    def add_reminders(self, reminders: Iterable[Reminder]) -> None:
        for reminder in reminders:
            self.add_reminder(reminder)

    def add_reminder(self, reminder: Reminder) -> None:
        logger.debug(
            f"Adding/updating reminder [{reminder.reminderId}] task_id [{reminder.sourceId}]"
        )

        reminder_deflated = lzma.compress(reminder.to_json().encode("utf-8"))

        with self.db as con:
            con.execute(
                "replace into reminders(guid, task_guid, raw_reminder)"
                " values (?, ?, ?)",
                (reminder.reminderId, reminder.sourceId, reminder_deflated),
            )

    def iter_reminders(self, task_guid: str) -> Iterator[Reminder]:
        with self.db as con:
            cur = con.execute(
                "select guid, raw_reminder from reminders where task_guid=?",
                (task_guid,),
            )

            for row in cur:
                raw_reminder = self._get_raw_reminder(row["guid"], row["raw_reminder"])

                if raw_reminder:
                    yield raw_reminder

    def expunge_reminders(self, guids: Iterable[str]) -> None:
        with self.db as con:
            con.executemany("delete from reminders where guid=?", ((g,) for g in guids))

    def _get_raw_reminder(self, guid: str, raw_reminder: bytes) -> Optional[Reminder]:
        try:
            return Reminder.from_json(lzma.decompress(raw_reminder).decode("utf-8"))
        except Exception:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.exception(f"Reminder [{guid}] is corrupt")

            logger.warning(f"Reminder [{guid}] is corrupt")

        return None


class ConfigStorage(SqliteStorage):
    def set_config_value(self, name: str, config_value: str) -> None:
        with self.db as con:
            con.execute(
                "replace into config(name, value) values (?, ?)",
                (name, config_value),
            )

    def get_config_value(self, name: str) -> str:
        with self.db as con:
            cur = con.execute("select value from config where name=?", (name,))
            res = cur.fetchone()

            if not res:
                raise KeyError(f"Config ID {name} not found in database!")

            return str(res[0])
