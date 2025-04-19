from configparser import ConfigParser
from phystool.config import config


class DeltaConfigParser(ConfigParser):
    _default = {
        "no-gitconfig": None,
        "side-by-side": None,
        "width": "200",
        "tabs": "4",
        "navigate": False,
        "hyperlinks": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.read(config.get_static_path() / "delta.conf")

    def get_themes(self) -> list[str]:
        return [
            theme[7:-1]
            for theme in self
            if theme.startswith("delta")
        ]

    def select(self, name: str) -> None:
        self.load(name)
        option = self._inline_options()
        config.save_config('git', 'theme', option)
        config.DELTA_THEME = option

    def load(self, name: str) -> None:
        self._options = {
            key: val
            for key, val in (
                {
                    key.strip(): self._format_val(val.strip())
                    for key, val in self[f'delta "{name}"'].items()
                } | self._default
            ).items()
            if val is not False
        }

    def _format_val(self, val: str) -> str | int | float | bool | None:
        if not val or val == "false":
            return False
        if val == "true":
            return None
        try:
            return int(val)
        except ValueError:
            pass
        try:
            return float(val)
        except ValueError:
            pass

        if val == '':
            return ''

        return f"'{val}'"

    def _inline_options(self) -> str:
        return " ".join(
            [
                f"--{key} {val}" if val
                else f"--{key}"
                for key, val in self._options.items()
            ]
        )
