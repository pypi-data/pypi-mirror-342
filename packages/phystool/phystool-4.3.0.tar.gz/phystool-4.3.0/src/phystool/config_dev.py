from configparser import ConfigParser
from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QProcessEnvironment


class MyConfig:
    def __init__(self, dev_mode: bool):
        config_dir = self._load_config_file(dev_mode)

        self._data = ConfigParser()
        self._data.read(self._config_file)
        self.DB_DIR = self._locate_db(dev_mode)
        if not self.DB_DIR.exists():
            raise FileNotFoundError(
                f"Database not found, looking for '{self.DB_DIR}'"
            )

        self.METADATA_DIR = _ensure_exists(self.DB_DIR / "metadata")
        self.LOGFILE_PATH = config_dir / 'phystool.log'
        self.METADATA_PATH = self.METADATA_DIR / '0_metadata.pkl'
        self.TAGS_PATH = self.METADATA_DIR / '1_tags.json'
        self.EVALUATION_PATH = self.METADATA_DIR / '2_evaluations.json'
        self.LATEX = LaTeXConf(
            config_dir=config_dir,
            db_dir=self.DB_DIR,
            conf=self._data['latex']
        )
        self.EDITOR_CMD: tuple[str, list[str]] = (self._data['physnoob']['editor'], [])
        if self.EDITOR_CMD[0] == "vim":
            self.EDITOR_CMD = ("rxvt-unicode", ["-e", "vim"])

        self.DELTA_THEME = self._data['git']['theme']

    def _load_config_file(self, dev_mode: bool) -> Path:
        config_dir = (
            Path(__file__).parents[2] / "dev"
            if dev_mode
            else Path.home() / ".phystool"
        )

        self._config_file = config_dir / "phystool.conf"
        if not self._config_file.exists():
            from shutil import (
                copyfile,
                copytree,
                ignore_patterns
            )
            static = self.get_static_path()
            copyfile(
                static / "phystool.conf",
                self._config_file
            )
            copytree(
                (
                    config_dir / "physdb_dev"
                    if dev_mode
                    else static / "physdb_dev"
                ),
                Path.home() / "physdb",
                ignore=ignore_patterns(".git*")
            )  # FIXME: exclude those files within pyproject.yaml
        return config_dir

    def _locate_db(self, dev_mode: bool) -> Path:
        db_dir = self._data['phystool']['db']
        if dev_mode:
            return Path(__file__).parents[2] / "dev" / db_dir
        else:
            return Path(db_dir).expanduser()

    def get_static_path(self) -> Path:
        return Path(__file__).parent / "static"

    def new_pdb_filename(self) -> Path:
        return (self.DB_DIR / str(uuid4())).with_suffix(".tex")

    def save_config(self, section: str, key: str, val: str) -> None:
        try:
            self._data[section][key] = val
        except KeyError:
            self._data.add_section(section)
            self._data[section][key] = val
        with self._config_file.open('w') as out:
            self._data.write(out)


class LaTeXConf:
    def __init__(self, config_dir: Path, db_dir: Path, conf: dict[str, str]):
        self._env: dict[bool, QProcessEnvironment | dict] = {}
        self._template = (
            f"\\documentclass{{{{{conf['auto']}}}}}\n"
            f"\\PdbSetDBPath{{{{{db_dir}/}}}}\n"
            "\\begin{{document}}\n"
            "    \\PdbPrint{{{tex_file}}}\n"
            "\\end{{document}}"
        )
        self.source = _ensure_exists(db_dir / "phystex")
        self.tikz_pattern = fr"^\\documentclass.*{{{conf['tikz']}}}"
        self.aux = _ensure_exists(config_dir / "texaux")

    def env(self, qrocess: bool) -> dict[str, str] | QProcessEnvironment:
        if not self._env:
            tmp = QProcessEnvironment.systemEnvironment()
            tmp.insert("TEXINPUTS", f":{self.source}:")
            self._env = {
                True: tmp,
                False: {
                    key: tmp.value(key)
                    for key in tmp.keys()
                }
            }
        return self._env[qrocess]

    def template(self, tex_file: Path) -> str:
        return self._template.format(tex_file=tex_file)


def _ensure_exists(path: Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path
