from pathlib import Path
import sys

SOURCE = Path(__file__).parents[2] / "src"
sys.path.insert(0, str(SOURCE))

with (SOURCE / "phystool" / "__about__.py").open() as about:
    key, val = about.readline().split("=")
    if key.strip() == "__version__":
        release = val.strip()
        version = ".".join(release.split(".")[:2])
    else:
        raise ValueError(f"Version not found in {about}")


project = 'phystool'
author = 'Jérome Dufour'

extensions = [
    'sphinxarg.ext',
    'autodoc2',
    'myst_parser',
]

html_theme = "sphinx_rtd_theme"
language = "fr"

autodoc2_hidden_objects = ["dunder", "private", "inherited"]
autodoc2_index_template = None
autodoc2_render_plugin = "myst"
autodoc2_packages = [
    {
        "path": "../../src/phystool/",
        "auto_mode": True,
        "exclude_dirs": ["tests"]
    },
]

myst_heading_anchors = 2
myst_enable_extensions = [
    "substitution",
    "fieldlist",
]
myst_substitutions = {
    "phystool": "**phystool**",
    "physnoob": "**physnoob**",
    "phystex": "`phystex`",
    "git": "``git``",
    "python": "`python`",
    "latex": "{math}`\\LaTeX`",
    "tikz": "{math}`\\text{Ti}k{Z}`",
    "pdbfile": "``PDBfile``",
    "exercise": "``Exercise``",
    "theory": "``Theory``",
    "qcm": "``QCM``",
    "tp": "``TP``",
    "figure": "``Figure``",
    "tags": "``Tags``",
    "tex": "``.tex``",
    "json": "``.json``",
    "pdf": "``.pdf``",
    "pty": "``.pty``",
    "uuid": "``uuid``",
}
