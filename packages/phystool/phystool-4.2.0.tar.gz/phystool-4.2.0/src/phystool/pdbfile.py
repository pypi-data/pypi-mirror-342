import json
import re

from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path
from typing import Self
from zipfile import ZipFile

from phystool.pytex import PyTex
from phystool.latex import (
    PdfLatex,
    LatexLogParser,
    ErrorMessage,
    Latex3Message,
    WarningMessage
)
from phystool.helper import (
    bat,
    greptex,
    as_valid_filename,
)
from phystool.config import config
from phystool.tags import Tags


logger = getLogger(__name__)


class PDBFile(ABC):
    PDB_TYPE: str

    @classmethod
    def validate_type(list_of_types: str) -> list[str]:
        if not list_of_types:
            return []

        out = []
        for file_type in list_of_types.split(','):
            if file_type not in VALID_TYPES:
                raise ValueError
            out.append(file_type)

        return out

    @classmethod
    def open_unkown(cls, filename: Path) -> Self | None:
        for ft_class in FILE_TYPE_MAP.values():
            try:
                return ft_class(filename, {})
            except ValueError:
                pass
        return None

    @classmethod
    def open(cls, uuid: str) -> Self:
        tex_file = (config.DB_DIR / uuid).with_suffix(".tex")
        if not tex_file.is_file():
            raise ValueError

        try:
            with tex_file.with_suffix(".json").open() as jsin:
                pdb_data = json.load(jsin)
                ft_class = FILE_TYPE_MAP[pdb_data['file_type']]
                return ft_class(tex_file, pdb_data)
        except (FileNotFoundError, json.JSONDecodeError):
            if pdb_file := cls.open_unkown(tex_file):
                return pdb_file
            raise ValueError(f"Parsing failed for: '{tex_file}'")
        except KeyError:
            raise ValueError(f"Unknown file_type for '{tex_file}'")
        raise ValueError(f"Unkown problem with file '{tex_file}'")

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file  # full path
        self.uuid = self.tex_file.stem
        self.tags: Tags
        self.title: str

    def __str__(self) -> str:
        return f"{self.PDB_TYPE.upper()[0:3]}: {self.title} [{self.tags}]"

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PDBFile)
            and self.uuid == other.uuid
        )

    def __lt__(self, other: Self) -> bool:
        return self.tex_file.stat().st_mtime < other.tex_file.stat().st_mtime

    @abstractmethod
    def _parse_texfile(self) -> None:
        """Abstract method that implements the class specific parsing"""

    def parse_texfile(self) -> bool:
        """Parse a texfile to analyse its content and create metadata"""
        try:
            self._parse_texfile()
            return True
        except ValueError:
            return False

    def save(self) -> None:
        with self.tex_file.with_suffix(".json").open('w') as jsout:
            json.dump(self.to_dict(), jsout, indent=4, ensure_ascii=False)

    def pytex(self) -> bool:
        pytex = PyTex(self.tex_file)
        if pytex.run():
            return True
        elif msg := pytex.get_messages():
            logger.error(msg)
        return False

    def cat(self) -> None:
        bat(self.tex_file, str(self))

    @abstractmethod
    def to_dict(self) -> dict[str, str | dict | list[str]]:
        """Return a dict that is JSON compatible"""

    def to_dmenu(self) -> str:
        return "{:<10} {:<60} {:<20}  {}".format(
            self.PDB_TYPE.upper(),
            self.title,
            self.uuid,
            self.tags
        )

    @abstractmethod
    def tex_export(self) -> None:
        """Print a string that can be inserted in LexTeX file"""

    def zip(self) -> None:
        fname = as_valid_filename(f"{self.title}.zip")
        with ZipFile(Path.cwd() / fname, 'w') as zf:
            self.compile()
            files = [self.tex_file]
            if self.PDB_TYPE != Figure.PDB_TYPE:
                files += [config.DB_DIR/figure for figure in self.figures]
            for f in set(files):
                zf.write(
                    f.with_suffix(".tex"),
                    arcname=f.with_suffix(".tex").name
                )
                if f.with_suffix(".pdf").exists():
                    zf.write(
                        f.with_suffix(".pdf"),
                        arcname=f.with_suffix(".pdf").name
                    )

    def create_tmp_tex_file(self) -> Path:
        tmp_tex_file = Path(f"/tmp/physauto-{self.uuid}.tex")
        with tmp_tex_file.open('w') as out:
            out.write(config.LATEX.template(self.uuid))

        return tmp_tex_file

    def should_compile(self) -> bool:
        dest_file = self.tex_file.with_suffix(".pdf")
        # shouldn't attempt to check figures (in case if it's missing)
        return (
            not dest_file.is_file()
            or dest_file.stat().st_mtime < self.tex_file.stat().st_mtime
        )

    def compile(self) -> bool:
        if not self.should_compile():
            logger.debug(f"No compilation required for {self.uuid}")
            return False

        logger.info(f"Compile '{self}")
        self.pytex()
        tmp_tex_file = self.create_tmp_tex_file()
        pdflatex = PdfLatex(tmp_tex_file)
        try:
            pdflatex.compile(env=config.LATEX.env(False))
            pdflatex.move_pdf(self.tex_file.with_suffix(".pdf"))

            llp = LatexLogParser(tmp_tex_file, [WarningMessage])
            llp.process()
            llp.display()
            pdflatex.clean(['.out', '.log', '.aux'])
            return True
        except PdfLatex.CompilationError:
            llp = LatexLogParser(tmp_tex_file, [Latex3Message, ErrorMessage])
            llp.process()
            llp.display()
            return False
        except PdfLatex.MoveError:
            return False


class CheckForTikzMixin:
    TIKZ_PATTERN = re.compile(r"\\PdbTikz[^{]*{([^}]*?)}")

    def _find_figures(self, tex_content: str) -> list[str]:
        return sorted(
            {
                match.group(1)
                for match in self.TIKZ_PATTERN.finditer(tex_content)
            }
        )


class Exercise(PDBFile, CheckForTikzMixin):
    PDB_TYPE = "exercise"
    EXO_PATTERN = re.compile(r"^\\begin{exercise}")
    TITLE_PATTERN = re.compile(r"title=([^,]*?)[\]|,]")

    def __init__(self, pdb_file: Path, pdb_data: dict):
        super().__init__(pdb_file)
        if not pdb_data:
            self._parse_texfile()
            self.tags = Tags({})
            self.evaluations = set()
        else:
            self.title = pdb_data['title']
            self.tags = Tags(pdb_data["tags"])
            self.figures = pdb_data["figures"]
            self.evaluations = set(pdb_data["evaluations"])

    def _parse_texfile(self) -> None:
        with self.tex_file.open() as f:
            tex_content = f.read()
            if not self.EXO_PATTERN.search(tex_content):
                raise ValueError

            if match := self.TITLE_PATTERN.search(tex_content):
                self.title = match.group(1)
            else:
                self.title = self.uuid
            self.figures = self._find_figures(tex_content)

    def to_dict(self) -> dict[str, str | dict | list[str]]:
        return {
            "file_type": self.PDB_TYPE,
            "title": self.title,
            "tags": self.tags.data,
            "figures": self.figures,
            "evaluations": sorted(self.evaluations)
        }

    def tex_export(self) -> None:
        print(f"\\PdbExercise{{{self.uuid}}} % {self.title}")


class Theory(PDBFile, CheckForTikzMixin):
    PDB_TYPE = "theory"
    THE_PATTERN = re.compile(r"^\\begin{theory}")
    TITLE_PATTERN = re.compile(r"title=([^,]*?)[\]|,]")

    def __init__(self, pdb_file: Path, pdb_data: dict):
        super().__init__(pdb_file)
        if not pdb_data:
            self._parse_texfile()
            self.tags = Tags({})
        else:
            self.title = pdb_data['title']
            self.tags = Tags(pdb_data["tags"])
            self.figures = pdb_data["figures"]

    def _parse_texfile(self) -> None:
        with self.tex_file.open() as f:
            tex_content = f.read()
            if not self.THE_PATTERN.search(tex_content):
                raise ValueError

            if match := self.TITLE_PATTERN.search(tex_content):
                self.title = match.group(1)
            else:
                self.title = self.uuid
            self.figures = self._find_figures(tex_content)

    def to_dict(self) -> dict[str, str | dict | list[str]]:
        return {
            "file_type": self.PDB_TYPE,
            "title": self.title,
            "tags": self.tags.data,
            "figures": self.figures
        }

    def tex_export(self) -> None:
        print(f"\\PdbTheory[]{{{self.uuid}}} % {self.title}")


class TP(PDBFile, CheckForTikzMixin):
    PDB_TYPE = "tp"
    TP_STUDENT_PATTERN = re.compile(r"^\\begin{tpstudent}")
    TITLE_PATTERN = re.compile(r"title=([^,]*?)[\]|,]")

    def __init__(self, pdb_file: Path, pdb_data: dict):
        super().__init__(pdb_file)
        if not pdb_data:
            self._parse_texfile()
            self.tags = Tags({})
        else:
            self.title = pdb_data['title']
            self.tags = Tags(pdb_data["tags"])
            self.figures = pdb_data["figures"]

    def _parse_texfile(self) -> None:
        with self.tex_file.open() as f:
            tex_content = f.read()
            if not self.TP_STUDENT_PATTERN.search(tex_content):
                raise ValueError

            if match := self.TITLE_PATTERN.search(tex_content):
                self.title = match.group(1)
            else:
                self.title = self.uuid
            self.figures = self._find_figures(tex_content)

    def to_dict(self) -> dict[str, str | dict | list[str]]:
        return {
            "file_type": self.PDB_TYPE,
            "title": self.title,
            "tags": self.tags.data,
            "figures": self.figures,
        }

    def tex_export(self) -> None:
        print(f"\\PdbTP{{{self.uuid}}} % {self.title}")


class QCM(PDBFile, CheckForTikzMixin):
    PDB_TYPE = "qcm"
    QCM_PATTERN = re.compile(r"^\\QCM[^{]*{(.*)")

    def __init__(self, pdb_file: Path, pdb_data: dict):
        super().__init__(pdb_file)
        if not pdb_data:
            self._parse_texfile()
            self.tags = Tags({})
        else:
            self.title = pdb_data['title']
            self.tags = Tags(pdb_data["tags"])
            self.figures = pdb_data["figures"]

    def _parse_texfile(self) -> None:
        with self.tex_file.open() as f:
            first_line = f.readline().rstrip()
            second_line = f.readline().rstrip()
            match = self.QCM_PATTERN.search(first_line + second_line)
            if not match:
                raise ValueError

            n_brace = 0
            self.title = ""
            for k, letter in enumerate(match.group(1)):
                if k > 40:
                    self.title += "..."
                    break
                if letter == '{':
                    n_brace += 1
                elif letter == '}':
                    n_brace -= 1
                    if n_brace < 0:
                        break
                self.title += letter

            self.figures = self._find_figures(f.read())

    def to_dict(self) -> dict[str, str | dict | list[str]]:
        return {
            "file_type": self.PDB_TYPE,
            "title": self.title,
            "tags": self.tags.data,
            "figures": self.figures
        }

    def tex_export(self) -> None:
        print(f"\\PdbQCM{{{self.uuid}}} % {self.title}")


class Figure(PDBFile):
    PDB_TYPE = "figure"
    FIG_PATTERN = re.compile(config.LATEX.tikz_pattern)

    def __init__(self, pdb_file: Path, pdb_data: dict):
        super().__init__(pdb_file)
        if not pdb_data:
            self._parse_texfile()
        else:
            self.title = pdb_data['title']
            self.tags = Tags(pdb_data["tags"])
            self.used_by = pdb_data["used_by"]

    def _parse_texfile(self) -> None:
        with self.tex_file.open() as f:
            first_line = f.readline().rstrip()
            if not self.FIG_PATTERN.search(first_line):
                raise ValueError

        self.used_by = sorted(greptex(self.uuid, config.DB_DIR, True))
        self.tags = Tags({})
        if not self.used_by:
            self.title = "__Untitled__"
            return

        all_titles = []
        n_qcm = 0
        for uuid in self.used_by:
            try:
                with (config.DB_DIR / uuid).with_suffix(".json").open() as jsin:
                    pdb_data = json.load(jsin)
                    self.tags += Tags(pdb_data['tags'])
                    if pdb_data['file_type'] == QCM.PDB_TYPE:
                        n_qcm += 1
                    else:
                        all_titles.append(pdb_data['title'])
            except FileNotFoundError:
                # can happen during db first creation
                pass

        all_titles = sorted(all_titles)
        if n_qcm:
            all_titles.append(f"QCM ({n_qcm})")

        self.title = ", ".join(all_titles)
        if len(self.title) > 40:
            self.title = self.title[:40] + "..."

    def to_dict(self) -> dict[str, str | dict | list[str]]:
        return {
            "file_type": self.PDB_TYPE,
            "title": self.title,
            "tags": self.tags.data,
            "used_by": self.used_by
        }

    def tex_export(self) -> None:
        print(f"\\PdbTikz[]{{{self.uuid}}}")

    def create_tmp_tex_file(self) -> Path:
        return self.tex_file


FILE_TYPE_MAP = {
    ft.PDB_TYPE: ft
    for ft in [Exercise, Theory, QCM, Figure, TP]
}
VALID_TYPES = list(FILE_TYPE_MAP.keys())
