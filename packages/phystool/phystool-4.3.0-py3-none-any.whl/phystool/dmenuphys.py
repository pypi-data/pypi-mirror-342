import subprocess

from logging import getLogger
from pathlib import Path

from phystool.config import config
from phystool.metadata import Metadata
from phystool.pdbfile import (
    PDBFile,
    Exercise,
    VALID_TYPES
)

logger = getLogger(__name__)


class DmenuPhys:
    DMENU_OPT = 0
    DMENU_VIM = 1
    DMENU_PDF = 2
    DMENU_NEW = 3
    DMENU_COPY_EXERCISE = 4
    DMENU_COPY_SHORTSOL = 5
    DMENU_COPY_LONGSOL = 6
    DMENU_CONSOLIDATE = 7
    DMENU_GIT = 8
    PNG_PATH = "unused/"
    PNG_NOT_FOUND = PNG_PATH + '_file_not_found.png'

    DMENU_OPTIONS = {
        'vim': DMENU_VIM,
        'pdf': DMENU_PDF,
        'new': DMENU_NEW,
        'git': DMENU_GIT,
        'consolidate': DMENU_CONSOLIDATE,
        # 'clip exercise': DMENU_COPY_EXERCISE,
        # 'clip longsol': DMENU_COPY_LONGSOL,
        # 'clip shortsol': DMENU_COPY_SHORTSOL,
    }

    def _popen(
        self,
        command: list[str],
        path: Path,
        check_path: bool = True
    ) -> None:
        if check_path and not path.is_file():
            logger.error(f"{path} does not exists")
            return

        command.append(str(path))
        try:
            subprocess.Popen(
                command,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(e)

    def _vim(self, path: Path, check_path: bool = True) -> None:
        self._popen(
            ["rxvt-unicode", "-e", "vim"],
            path=path,
            check_path=check_path
        )

    def _pdf(self, path: Path) -> None:
        self._popen(["zathura"], path=path)

    def _phystool(self, command: list[str]) -> None:
        if not command:
            return

        command = [
            "rxvt-unicode",
            "-e",
            "phystool"
        ] + command
        try:
            subprocess.Popen(command)
        except subprocess.CalledProcessError as e:
            logger.error(e)

    def _consolidate(self) -> None:
        self._phystool(["--consolidate"])

    def _git(self) -> None:
        self._phystool(["--git"])

    def _xclip(self, uuid: str, fname: str) -> None:
        raise NotImplementedError
        pdb_file = PDBFile.open(uuid)
        pdb_file.compile()

        png_file = (self.PNG_PATH / fname).with_suffix('.png')
        if not png_file.is_file():
            logger.error(f"{png_file} not found")
            png_file = self.PNG_NOT_FOUND

        self._popen(
            [
                "xclip",
                "-selection", "clipboard",
                "-t", "image/png",
                "-i"
            ],
            path=png_file
        )

    def _dmenu_in(self, how: int) -> str | None:
        if how == self.DMENU_OPT:
            dmenu_list = self.DMENU_OPTIONS.keys()
        elif how == self.DMENU_NEW:
            self._vim(config.new_pdb_filename(), check_path=False)
            return None
        elif how == self.DMENU_CONSOLIDATE:
            self._consolidate()
            return None
        elif how == self.DMENU_GIT:
            self._git()
            return None
        else:
            if how in [
                self.DMENU_COPY_EXERCISE,
                self.DMENU_COPY_SHORTSOL,
                self.DMENU_COPY_LONGSOL,
            ]:
                file_types = [
                    Exercise.PDB_TYPE
                ]
            else:
                file_types = VALID_TYPES

            metadata = Metadata()
            self._uuid_map = metadata.dmenu_dict(file_types)
            dmenu_list = self._uuid_map.keys()

        try:
            cmd = subprocess.Popen(
                "dmenu -i -l 20",
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            logger.error(e)
            return None

        stdout, _ = cmd.communicate("\n".join(dmenu_list).encode("utf-8"))
        return stdout.decode('utf-8').strip('\n')

    def _dmenu_out(self, how: int, selected: str) -> None:
        if how == self.DMENU_OPT:
            opt = self.DMENU_OPTIONS[selected]
            self(opt)
            return

        uuid = self._uuid_map[selected]
        if how == self.DMENU_PDF:
            self._pdf((config.DB_DIR / uuid).with_suffix('.pdf'))
        elif how == self.DMENU_VIM:
            self._vim((config.DB_DIR / uuid).with_suffix('.tex'))
        else:
            if how == self.DMENU_COPY_SHORTSOL:
                fname = uuid + "-shortsol"
            elif how == self.DMENU_COPY_LONGSOL:
                fname = uuid + "-longsol"
            elif how == self.DMENU_COPY_EXERCISE:
                fname = uuid + "-exercise"
            else:
                return
            self._xclip(uuid, fname)

    def __call__(self, how: int = 0) -> None:
        if selected := self._dmenu_in(how):
            self._dmenu_out(how, selected)
