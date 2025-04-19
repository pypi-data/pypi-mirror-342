from ansi2html import Ansi2HTMLConverter

from PySide6.QtCore import (
    QSettings,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from phystool.physgit import (
    PhysGit,
    InvalidGitRepositoryError,
    setup_git_repository
)
from phystool.qt.config import DeltaConfigParser
from phystool.qt.helper import QBusyDialog


class GitListFilesWidget(QTableWidget):
    sig_diff = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._physgit = PhysGit()

        labels = ["Statut", ""]
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels(labels)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setRowCount(len(self._physgit))
        self.currentCellChanged.connect(self._display_diff)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self._uuid_row_map: dict[int, str] = {}
        for row, (uuid, git_file) in enumerate(self._physgit):
            self._uuid_row_map[row] = uuid
            check_box = QCheckBox(git_file.status.name, self)
            self.setCellWidget(row, 0, check_box)
            self.setItem(row, 1, QTableWidgetItem(git_file.title))

    @Slot()
    def _display_diff(self) -> None:
        row = self.currentRow()
        if row < 0:
            return
        self.sig_diff.emit(
            self._physgit.get_diff(self._uuid_row_map[row])
        )

    @Slot()
    def select_all(self) -> None:
        for row in range(self.rowCount()):
            self.cellWidget(row, 0).setChecked(True)

    @Slot()
    def unselect_all(self) -> None:
        for row in range(self.rowCount()):
            self.cellWidget(row, 0).setChecked(False)

    def commit(self) -> str:
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).isChecked():
                self._physgit.stage(self._uuid_row_map[row])
        return self._physgit.commit(for_terminal=False)


class GitDiffWidget(QTextEdit):
    def __init__(self):
        super().__init__(
            lineWrapMode=QTextEdit.LineWrapMode.NoWrap,
            readOnly=True
        )
        self._conv = Ansi2HTMLConverter()

    @Slot(str)
    def display(self, ansi: str) -> None:
        self.setHtml(
            self._conv.convert(ansi)
        )

    def get_ideal_width(self) -> int:
        return int(self.document().idealWidth())


class GitDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self._git_list_files_widget = GitListFilesWidget()
        self.setWindowTitle("Git")
        self.setSizeGripEnabled(True)
        self.setMinimumHeight(500)

        diff_widget = GitDiffWidget()
        self._git_list_files_widget.sig_diff.connect(diff_widget.display)
        self._git_list_files_widget.setCurrentCell(0, 0)

        LEFT_WIDTH = 300
        RIGHT_WIDTH = diff_widget.get_ideal_width()

        select_all = QPushButton("Tout sélectionner")
        select_all.pressed.connect(self._git_list_files_widget.select_all)
        unselect_all = QPushButton("Rien sélectionner")
        unselect_all.pressed.connect(self._git_list_files_widget.unselect_all)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        btn_box.addButton(select_all, QDialogButtonBox.ButtonRole.ResetRole)
        btn_box.addButton(unselect_all, QDialogButtonBox.ButtonRole.ResetRole)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(self._git_list_files_widget)
        splitter.addWidget(diff_widget)
        splitter.setMinimumWidth(LEFT_WIDTH + RIGHT_WIDTH + 30)
        splitter.setSizes([LEFT_WIDTH, RIGHT_WIDTH])

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)
        layout.addWidget(btn_box)

    @Slot()
    def accept(self) -> None:
        busy_dialog = QBusyDialog(
            label="Pushing to remote",
            parent=self.parent(),
        )
        busy_dialog.run(
            self._git_list_files_widget.commit
        )
        super().accept()


class GitConfigureDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Git configure")
        self.setMinimumWidth(400)

        self._theme = QComboBox()
        self._message = QLineEdit(readOnly=True)
        self._remote_url = QLineEdit()

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.configure)
        btn_box.rejected.connect(self.reject)

        form = QFormLayout(self)
        form.addRow("Git diff theme", self._theme)
        form.addRow("Remotre url", self._remote_url)
        form.addWidget(self._message)
        form.addWidget(btn_box)

        self._delta = DeltaConfigParser()
        self._theme.addItems(self._delta.get_themes())
        settings = QSettings()
        if theme := settings.value("GitDiff/Theme"):
            self._theme.setCurrentIndex(self._delta.get_themes().index(theme))

        try:
            physgit = PhysGit()
            self._remote_url.setReadOnly(True)
            self._remote_url.setText(physgit.get_remote_url())
            self._message.setPlaceholderText(
                "Remote already configured, can't be changed"
            )
            self._first_initialization = False
        except InvalidGitRepositoryError:
            self._remote_url.setPlaceholderText(
                "e.g. git@bitbucket.org:username/repository_name.git"
            )
            self._message.setPlaceholderText("Remote's answer")
            self._first_initialization = True

    @Slot()
    def configure(self) -> None:
        if theme := self._theme.currentText():
            self._delta.select(theme)
            settings = QSettings()
            settings.setValue("GitDiff/Theme", theme)

        if self._first_initialization:
            try:
                setup_git_repository(self._remote_url.text())
                super().accept()
            except InvalidGitRepositoryError as e:
                self._message.setText(e.args[0])
        else:
            super().accept()
