from logging import getLogger
from pathlib import Path
from shutil import copyfile
from time import sleep
from rapidfuzz.process import extract
from rapidfuzz.fuzz import QRatio

from PySide6.QtCore import (
    Qt,
    QObject,
    Slot,
    Signal,
    QFileSystemWatcher,
)
from PySide6.QtGui import (
    QAction,
    QGuiApplication,
    QColor,
    QColorConstants,
    QContextMenuEvent
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHeaderView,
    QMenu,
    QMessageBox,
    QProgressDialog,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from phystool.config import config
from phystool.metadata import Metadata
from phystool.pdbfile import PDBFile
from phystool.tags import Tags
from phystool.qt.helper import MultipleSelectionWidget
from phystool.qt.latex import (
    QPdfLatex,
    CompilationErrorWidget
)
from phystool.qt.process import (
    ProcessManager,
    OpenFileProcess
)


logger = getLogger(__name__)


class _CategoryTagsWidget(MultipleSelectionWidget):
    def __init__(
        self,
        category: str,
        left_labels: list[str],
        right_labels: list[str]
    ):
        super().__init__(left_labels, right_labels)
        self.category = category


class _TagSelectionWidget(QDialog):
    def __init__(self, current_tags: Tags):
        super().__init__()
        self.setWindowTitle("Édition")

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Save
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        available_tags = Tags.TAGS - current_tags
        self._widgets = [
            _CategoryTagsWidget(
                category,
                available_tags[category],
                current_tags[category]
            )
            for category, tags in Tags.TAGS
        ]

        layout = QVBoxLayout(self)
        for widget in self._widgets:
            layout.addWidget(widget)
        layout.addWidget(btn_box)

    def get_new_tags(self) -> Tags:
        return Tags(
            {
                widget.category: widget.get_right_values()
                for widget in self._widgets
            }
        )


class _TagAction(QAction):
    def __init__(
        self,
        category: str,
        tag: str,
        adding: bool,
        trigger,
        parent: QObject
    ):
        super().__init__(tag, parent)
        self._category = category
        self._tag = tag
        self._adding = adding
        self.triggered.connect(trigger)

    def update_tags(self, pdb_files: list[PDBFile]) -> None:
        tags = Tags({self._category: [self._tag]})
        for pdb_file in pdb_files:
            if self._adding:
                pdb_file.tags += tags
            else:
                pdb_file.tags -= tags


class PdbFileListWidget(QTableWidget):
    sig_update_display = Signal(PDBFile)
    sig_consolidate = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._process_manager = ProcessManager()
        self._metadata = Metadata()
        self._pdb_file_list: list[PDBFile] = []
        self._filter_data: dict[str, str | set[str] | Tags] = {}
        self._row_title_map: dict[int, str] = {}
        self._watched: PDBFile
        self._watcher = QFileSystemWatcher()
        self._watcher.fileChanged.connect(self._auto_compilation)
        self._clipboard = QGuiApplication.clipboard()

        labels = ["Type", "Titre", "Tags"]
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels(labels)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.itemDoubleClicked.connect(self.open_tex_file)
        self.currentItemChanged.connect(self._display_pdb_file)

        header = self.horizontalHeader()
        header.setDefaultSectionSize(40)
        header.setMinimumSectionSize(40)
        header.resizeSection(1, 250)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.compilation_error_widget = CompilationErrorWidget()

    def contextMenuEvent(self, event: QContextMenuEvent):
        context = QMenu(self)
        for adding, submenu in [
            (True, QMenu("Ajouter un tag", context)),
            (False, QMenu("Supprimer un tag", context))
        ]:
            context.addMenu(submenu)
            for category, tags in Tags.TAGS:
                category_menu = QMenu(category, context)
                submenu.addMenu(category_menu)
                for tag in tags:
                    category_menu.addAction(
                        _TagAction(
                            category=category,
                            tag=tag,
                            adding=adding,
                            trigger=self.edit_batch,
                            parent=category_menu
                        )
                    )

        context.exec(event.globalPos())

    @Slot(dict)
    def list_update(self, filter_data: dict) -> None:
        self._filter_data = filter_data
        self._list_update()

    def _list_update(self) -> None:
        self._pdb_file_list = self._metadata.filter(**self._filter_data)
        self.clearContents()
        self.setRowCount(len(self._pdb_file_list))
        self._row_title_map = {}
        for row, pdb_file in enumerate(self._pdb_file_list):
            self.setItem(row, 0, QTableWidgetItem(pdb_file.PDB_TYPE.upper()[:3]))
            self.setItem(row, 1, QTableWidgetItem(pdb_file.title))
            self.setItem(row, 2, QTableWidgetItem(str(pdb_file.tags)))
            self._row_title_map[row] = pdb_file.title.lower()

    @Slot()
    def _display_pdb_file(self) -> None:
        row = self.currentRow()
        if row < 0:
            return
        self._watched = self._pdb_file_list[row]
        self._watch_and_compile()
        self.sig_update_display.emit(self._watched)

    @Slot(str)
    def _auto_compilation(self, path: str) -> None:
        """
        The small delay is required because when a file is saved, the OS copies
        the file before replacing the previous version. This means that for a
        brief period of time, python can't find the file. That's also why it
        disappears from the watch list and should only be re-added when it's
        safe.
        """
        fname = Path(path)
        i = 0
        while (not fname.exists() and i < 10):
            i += 1
            sleep(0.1)

        if i == 10:
            logger.error("Watching file failed")
            return
        self._watch_and_compile()

    def _watch_and_compile(self) -> None:
        if files := self._watcher.files():
            self._watcher.removePaths(files)
        self._watcher.addPath(str(self._watched.tex_file))
        if self._watched.should_compile():
            pdf_latex = QPdfLatex(
                self._watched,
                self._post_compilation_hook
            )
            self._process_manager.add(pdf_latex)

    def _post_compilation_hook(self, pdb_file: PDBFile, msg: str) -> None:
        if self._watched == pdb_file:
            self.sig_update_display.emit(self._watched)
            self.compilation_error_widget(msg)

    def _get_selected_rows(self) -> list[int]:
        return sorted({item.row() for item in self.selectedItems()})

    def _update_metadata(
        self,
        rows: list[int],
        pdb_files: list[PDBFile]
    ) -> None:
        for row, pdb_file in zip(rows, pdb_files):
            pdb_file.save()
            self.setItem(row, 2, QTableWidgetItem(str(pdb_file.tags)))
        self._metadata.save()

    @Slot()
    def edit_pdb_file(self) -> None:
        row = self.currentRow()
        if row < 0:
            return

        pdb_file = self._pdb_file_list[row]
        dialog = _TagSelectionWidget(pdb_file.tags)
        if dialog.exec():
            new_tags = dialog.get_new_tags()
            if pdb_file.tags != new_tags:
                pdb_file.tags = new_tags
                self._update_metadata([row], [pdb_file])

    @Slot()
    def edit_batch(self) -> None:
        rows = self._get_selected_rows()
        pdb_files = [self._pdb_file_list[row] for row in rows]
        self.sender().update_tags(pdb_files)
        self._update_metadata(rows, pdb_files)

    @Slot()
    def open_tex_file(self) -> None:
        if filenames := [
            str(self._pdb_file_list[row].tex_file)
            for row in self._get_selected_rows()
        ]:
            OpenFileProcess(filenames)

    @Slot()
    def consolidate(self) -> None:
        logger.info("Consolidate data")
        dialog = QProgressDialog("Consolidate data", "Cancel", 0, 1, self)
        dialog.setAutoClose(False)
        dialog.setAutoReset(False)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(0)
        dialog.setValue(1)

        _message = ""
        _n = 0
        for i, n, message in self._metadata.consolidate_progress():
            if dialog.wasCanceled():
                return
            if _n != n:
                _n = n
                dialog.setMaximum(n)
            if _message != message:
                _message = message
                dialog.setLabelText(message)
            dialog.setValue(i)

        self.sig_consolidate.emit()
        self._list_update()

    @Slot()
    def delete_pdb_file(self) -> None:
        if pdb_files := [
            self._pdb_file_list[row]
            for row in self._get_selected_rows()
        ]:
            title = "Supression de fichiers"
            button = QMessageBox.question(
                self,
                title,
                "\n".join([str(pdb_file) for pdb_file in pdb_files])
            )
            if button == QMessageBox.StandardButton.Yes:
                for pdb_file in pdb_files:
                    self._metadata.remove(pdb_file)
                self._metadata.save()
                self._list_update()
                QMessageBox.information(
                    self,
                    title,
                    "Les fichiers sélectionnés ont bien été supprimés"
                )

            elif button == QMessageBox.StandardButton.No:
                QMessageBox.information(
                    self,
                    title,
                    "Les fichiers sélectionnés n'ont pas été supprimés"
                )
            else:
                raise ValueError(button)

    @Slot()
    def import_pdb_file(self) -> None:
        title = "Importation d'un nouveau fichier"
        fname, _ = QFileDialog.getOpenFileName(
            self,
            title,
            str(Path.home()),
            "Tex Files (*.tex)"
        )
        if not fname:
            return

        tex_file = Path(fname)
        if (
            not tex_file.is_file()
            or tex_file.suffix != ".tex"
        ):
            QMessageBox.warning(
                self,
                title,
                "Erreur durant l'import du fichier.",
            )
            return

        if pdb_file := PDBFile.open_unkown(tex_file):
            pdb_file.tex_file = config.new_pdb_filename()
            pdb_file.uuid = pdb_file.tex_file.stem
            button = QMessageBox.question(
                self,
                title,
                f"Importer le fichier intitulé '{pdb_file.title}'?"
            )
            if button == QMessageBox.StandardButton.Yes:
                copyfile(fname, pdb_file.tex_file)
                self._metadata.update(pdb_file)
                self._metadata.save()
                self._list_update()
            else:
                QMessageBox.information(
                    self,
                    title,
                    f"L'importation de {pdb_file.title} a été annulée.",
                    buttons=QMessageBox.StandardButton.Ok
                )
        else:
            QMessageBox.warning(
                self,
                title,
                "Le fichier sélectionné n'a pas le bon format.",
            )

    @Slot()
    def new_pdb_file(self) -> None:
        OpenFileProcess([str(config.new_pdb_filename())])

    @Slot(str)
    def search_in_title(self, text: str) -> None:
        if text:
            best_rows = {
                row: score
                for _, score, row in extract(
                    text.lower(),
                    self._row_title_map,
                    limit=10,
                    processor=None,
                    scorer=QRatio
                )
            }
            min_score = 100.0
            max_score = 0.0
            for score in best_rows.values():
                if score < min_score:
                    min_score = score
                if score > max_score:
                    max_score = score

        if not text or (max_score - min_score < 1):
            for row in range(self.rowCount()):
                if item := self.item(row, 1):
                    item.setBackground(QColorConstants.White)
                    self.showRow(row)
            return

        for row in range(self.rowCount()):
            if score := best_rows.get(row, 0):
                if item := self.item(row, 1):
                    item.setBackground(
                        QColor.fromHsvF(
                            0.28,
                            (score-min_score)/(max_score-min_score),
                            0.9
                        )
                    )
                    if self.isRowHidden(row):
                        self.showRow(row)
            else:
                if not self.isRowHidden(row):
                    if item := self.item(row, 1):
                        item.setBackground(QColorConstants.White)
                        self.hideRow(row)

    @Slot()
    def copy_to_clipboard(self) -> None:
        if uuids := [
            self._pdb_file_list[row].uuid
            for row in self._get_selected_rows()
        ]:
            self._clipboard.setText("\n".join(uuids))
