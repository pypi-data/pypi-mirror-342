from logging import getLogger

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
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from phystool.tags import Tags
from phystool.pdbfile import VALID_TYPES


logger = getLogger(__name__)


class FilterWidget(QWidget):
    sig_filter_updated = Signal(dict)

    def __init__(self):
        super().__init__()
        settings = QSettings()

        self._query = ""
        self._uuid_bit = ""
        self._excluded_tags = settings.value(
            "FilterWidget/excluded_tags",
            defaultValue=Tags({})
        )
        self._selected_tags = settings.value(
            "FilterWidget/selected_tags",
            defaultValue=Tags({})
        )
        self._file_types = settings.value(
            "FilterWidget/filetypes",
            defaultValue=set()
        )

        self._filters_layout = QHBoxLayout()
        self._file_types_layout = QHBoxLayout()

        for file_type in VALID_TYPES:
            button = QCheckBox(file_type.capitalize(), self)
            button.file_type = file_type
            button.setChecked(file_type in self._file_types)
            button.toggled.connect(self._filter_file_type)
            self._file_types_layout.addWidget(button)

        self._search_widget = QLineEdit()
        self._search_widget.setPlaceholderText(
            "Rechercher dans les fichiers '*.tex'"
        )
        self._search_widget.returnPressed.connect(self._filter_query)

        layout = QVBoxLayout(self)
        layout.addWidget(self._search_widget)
        layout.addLayout(self._file_types_layout)
        layout.addLayout(self._filters_layout)

        self.update_filters()

    @Slot()
    def update_filters(self) -> None:
        while child := self._filters_layout.takeAt(0):
            while subchild := child.takeAt(0):
                if tmp := subchild.widget():
                    tmp.deleteLater()
            if tmp := child.widget():
                tmp.deleteLater()

        for category, tags in Tags.TAGS:
            layout = QVBoxLayout()
            label = QLabel(category.capitalize())
            label.setAlignment(
                Qt.AlignmentFlag.AlignTop
                | Qt.AlignmentFlag.AlignLeft
            )
            label.setFrameStyle(
                QFrame.Shape.Panel
                | QFrame.Shadow.Sunken
            )

            layout.addWidget(label)
            for tag_name in tags:
                button = QCheckBox(tag_name)
                button.setTristate(True)
                button.tags = Tags({category: [tag_name]})
                button.checkStateChanged.connect(self._filter_tags)
                if tag_name in self._selected_tags[category]:
                    button.setCheckState(Qt.CheckState.Checked)
                elif tag_name in self._excluded_tags[category]:
                    button.setCheckState(Qt.CheckState.PartiallyChecked)
                else:
                    button.setCheckState(Qt.CheckState.Unchecked)
                layout.addWidget(button)

            layout.addStretch()
            self._filters_layout.addLayout(layout)

    @Slot()
    def create_new_tag(self) -> None:
        dialog = QDialog()
        dialog.setWindowTitle("Create new tag for category")

        form = QFormLayout()
        category = QComboBox()
        category.addItems(
            [
                cat.capitalize()
                for cat in Tags.TAGS.data.keys()
            ]
        )
        category.setEditable(True)
        category.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        tag = QLineEdit()
        form.addRow("Category", category)
        form.addRow("Tag", tag)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)

        layout = QVBoxLayout(dialog)
        layout.addLayout(form)
        layout.addWidget(btn_box)

        if dialog.exec():
            Tags.create_new_tag(
                category.currentText().lower(),
                tag.text()
            )
            self.update_filters()

    def get_filter_data(self) -> dict[str, str | set[str] | Tags]:
        return {
            'query': self._query,
            'uuid_bit':  self._uuid_bit,
            'file_types':  self._file_types,
            'selected_tags': self._selected_tags,
            'excluded_tags': self._excluded_tags
        }

    @Slot(Qt.CheckState)
    def _filter_tags(self, state: Qt.CheckState) -> None:
        tags = self.sender().tags
        if state == Qt.CheckState.PartiallyChecked:
            self._excluded_tags += tags
        elif state == Qt.CheckState.Checked:
            self._selected_tags += tags
            self._excluded_tags -= tags
        elif state == Qt.CheckState.Unchecked:
            self._selected_tags -= tags
        self.sig_filter_updated.emit(self.get_filter_data())

    @Slot()
    def _filter_file_type(self) -> None:
        button = self.sender()
        if button.isChecked():
            self._file_types.add(button.file_type)
        else:
            self._file_types.remove(button.file_type)
        self.sig_filter_updated.emit(self.get_filter_data())

    @Slot()
    def _filter_query(self) -> None:
        self._query = self.sender().text()
        self.sig_filter_updated.emit(self.get_filter_data())

    def __del__(self):
        settings = QSettings()
        settings.setValue("FilterWidget/filetypes", self._file_types)
        settings.setValue("FilterWidget/selected_tags", self._selected_tags)
        settings.setValue("FilterWidget/excluded_tags", self._excluded_tags)
