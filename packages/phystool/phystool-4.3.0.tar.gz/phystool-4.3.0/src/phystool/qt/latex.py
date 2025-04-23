from logging import getLogger
from pathlib import Path
from collections.abc import Callable

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPlainTextEdit

from phystool.config import config
from phystool.pdbfile import PDBFile, Figure
from phystool.latex import (
    PdfLatex,
    LatexLogParser,
    ErrorMessage,
    Latex3Message
)
from phystool.qt.process import QManagedProcess


logger = getLogger(__name__)


class QPdfLatex(QManagedProcess):
    def __init__(
        self,
        pdb_file: PDBFile,
        post_compilation_hook: Callable[[PDBFile, str], None]
    ):
        super().__init__()
        self._pdb_file = pdb_file
        self._tmp_tex_file: Path
        self._status = self.Status.PENDING
        self._post_compilation_hook = post_compilation_hook

    def __str__(self) -> str:
        return f"{self.__class__.__name__} <{self._pdb_file.uuid}>"

    def get_unique_id(self) -> str:
        return self._pdb_file.uuid

    def get_ready(self) -> None:
        self._status = self.Status.RUNNING
        if not self._pdb_file.should_compile():
            self._status = self.Status.SUCCESS
            return

        logger.info(f"Compile {self._pdb_file}")
        self._tmp_tex_file = self._pdb_file.create_tmp_tex_file()
        cmd = PdfLatex.compilation_command(self._tmp_tex_file)
        self.setProgram(cmd[0])
        self.setArguments(cmd[1:])
        self.setProcessEnvironment(config.LATEX.env(True))
        self.finished.connect(self._handle_exit)

    @Slot(int)
    def _handle_exit(self, exit_code: int) -> None:
        if exit_code:
            self._status = self.Status.ERROR
            llp = LatexLogParser(
                self._tmp_tex_file,
                [ErrorMessage, Latex3Message]
            )
            llp.process()
            msg = llp.get_as_text()
            logger.warning(msg)
            self._post_compilation_hook(self._pdb_file, msg)
            return

        try:
            pdflatex = PdfLatex(self._tmp_tex_file)
            if self._pdb_file.PDB_TYPE != Figure.PDB_TYPE:
                pdflatex.move_pdf(self._pdb_file.tex_file.with_suffix(".pdf"))
            pdflatex.clean(['.out', '.log', '.aux'])
            self._status = self.Status.SUCCESS
            self._post_compilation_hook(self._pdb_file, "")
        except PdfLatex.MoveError as e:
            logger.warning(e)
            self._status = self.Status.ERROR
            self._post_compilation_hook(self._pdb_file, str(e))


class CompilationErrorWidget(QPlainTextEdit):
    def __init__(self):
        super().__init__(
            lineWrapMode=QPlainTextEdit.LineWrapMode.NoWrap,
            ReadOnly=True
        )
        self.setMaximumBlockCount(5)
        self.setMaximumHeight(100)

    def __call__(self, txt: str) -> None:
        if txt:
            self.setPlainText(txt)
            self.parent().show()
        else:
            self.parent().hide()
