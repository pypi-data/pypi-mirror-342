import logging
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path

from click import progressbar
from evernote.edam.type.ttypes import Note, Notebook

from evernote_backup.cli_app_util import DatabaseEmptyError, get_progress_output
from evernote_backup.evernote_types import Task
from evernote_backup.log_util import log_format_note, log_format_notebook
from evernote_backup.note_exporter_util import SafePath
from evernote_backup.note_formatter import NoteFormatter
from evernote_backup.note_storage import SqliteStorage

logger = logging.getLogger(__name__)

ENEX_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
"""
ENEX_TAIL = "</en-export>\n"


class NoteExporter:
    def __init__(
        self,
        storage: SqliteStorage,
        target_dir: Path,
        single_notes: bool,
        export_trash: bool,
        no_export_date: bool,
        add_guid: bool,
        add_metadata: bool,
        overwrite: bool,
        filter_notebooks: tuple[str],
        filter_tags: tuple[str],
    ) -> None:
        self.storage = storage
        self.safe_paths = SafePath(target_dir, overwrite)

        self.single_notes = single_notes
        self.export_trash = export_trash
        self.no_export_date = no_export_date
        self.add_guid = add_guid
        self.add_metadata = add_metadata
        self.filter_notebooks = filter_notebooks
        self.filter_tags = filter_tags

    def export_notebooks(self) -> None:
        count_notes = self.storage.notes.get_notes_count()
        count_trash = self.storage.notes.get_notes_count(is_active=False)

        if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
            logger.debug(f"Notes: {count_notes}")
            logger.debug(f"Trashed notes: {count_trash}")
            if self.single_notes:
                logger.debug("Export mode: single notes")
            else:
                logger.debug("Export mode: notebooks")

        if count_notes == 0 and count_trash == 0:
            raise DatabaseEmptyError

        if count_notes > 0:
            logger.info("Exporting notebooks...")

            self._export_active()

        if count_trash > 0 and self.export_trash:
            logger.info("Exporting trash...")

            self._export_trash()

    def _export_active(self) -> None:
        notebooks = list(self.storage.notebooks.iter_notebooks())

        if self.filter_notebooks:
            notebooks = [n for n in notebooks if n.name in self.filter_notebooks]

            missed_notebooks = set(self.filter_notebooks) - {n.name for n in notebooks}

            for n in missed_notebooks:
                logger.warning(f"Notebook '{n}' not found in database.")

        with progressbar(
            notebooks,
            show_pos=True,
            file=get_progress_output(),
        ) as notebooks_bar:
            for nb in notebooks_bar:
                if logger.getEffectiveLevel() == logging.DEBUG:  # pragma: no cover
                    nb_info = log_format_notebook(nb)
                    logger.debug(f"Exporting notebook {nb_info}")

                if self.storage.notebooks.get_notebook_notes_count(nb.guid) == 0:
                    logger.debug("Notebook is empty, skip")
                    continue

                self._export_notes(nb)

    def _filter_tags(self, note: Note) -> bool:
        if not note.tagNames:
            return False

        return bool(set(note.tagNames) & set(self.filter_tags))

    def _export_notes(self, notebook: Notebook) -> None:
        parent_dir = [notebook.stack] if notebook.stack else []

        notes_source = self.storage.notes.iter_notes(notebook.guid)

        if self.filter_tags:
            notes_source = filter(self._filter_tags, notes_source)

        if self.single_notes:
            parent_dir.append(notebook.name)
            self._output_single_notes(parent_dir, notebook.name, notes_source)
        else:
            self._output_notebook(parent_dir, notebook.name, notes_source)

    def _export_trash(self) -> None:
        notes_source = self.storage.notes.iter_notes_trash()

        if self.filter_tags:
            notes_source = filter(self._filter_tags, notes_source)

        if self.single_notes:
            self._output_single_notes(
                ["Trash"],
                "Trash",
                notes_source,
            )
        else:
            self._output_notebook(
                [],
                "Trash",
                notes_source,
            )

    def _output_single_notes(
        self,
        parent_dir: list[str],
        notebook_name: str,
        notes_source: Iterable[Note],
    ) -> None:
        for note in notes_source:
            note_path = self.safe_paths.get_file(*parent_dir, f"{note.title}.enex")

            self._write_export_file(note_path, notebook_name, [note])

    def _output_notebook(
        self,
        parent_dir: list[str],
        notebook_name: str,
        notes_source: Iterable[Note],
    ) -> None:
        notebook_path = self.safe_paths.get_file(*parent_dir, f"{notebook_name}.enex")

        self._write_export_file(notebook_path, notebook_name, notes_source)

    def _get_note_tasks(self, note_guid: str) -> list[Task]:
        tasks = sorted(
            self.storage.tasks.iter_tasks(note_guid),
            key=lambda t: str(t.sortWeight),
        )

        for task in tasks:
            task.reminders = list(self.storage.reminders.iter_reminders(task.taskId))

        return tasks

    def _write_export_file(
        self,
        file_path: Path,
        notebook_name: str,
        note_source: Iterable[Note],
    ) -> None:
        with file_path.open("w", encoding="utf-8") as f:
            logger.debug(f"Writing file {file_path}")

            f.write(ENEX_HEAD)

            if self.no_export_date:
                f.write('<en-export application="Evernote" version="10.134.4">\n')
            else:
                now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                f.write(
                    f'<en-export export-date="{now}"'
                    f' application="Evernote" version="10.134.4">\n'
                )

            note_formatter = NoteFormatter(
                add_guid=self.add_guid,
                add_metadata=self.add_metadata,
            )

            for note in note_source:  # noqa: WPS440
                n_info = log_format_note(note)
                logger.debug(f"Exporting note {n_info}")

                note_tasks = self._get_note_tasks(note.guid)

                f.write(
                    note_formatter.format_note(
                        note,
                        notebook_name,
                        note_tasks,
                    )
                )

            f.write(ENEX_TAIL)
