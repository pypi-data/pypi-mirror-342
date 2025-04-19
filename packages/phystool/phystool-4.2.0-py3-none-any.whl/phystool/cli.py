
from logging import getLogger

logger = getLogger(__name__)


def _default(args):
    if args.dmenu:
        from phystool.dmenuphys import DmenuPhys
        dmenu = DmenuPhys()
        dmenu()
    if args.gui:
        from phystool.qt import PhysQt
        qt = PhysQt()
        qt.exec()
    elif args.list_tags:
        from phystool.tags import Tags
        Tags.TAGS.list_tags()
    elif args.tex_export_pdb_files:
        from phystool.pdbfile import PDBFile
        for uuid in args.tex_export_pdb_files:
            pdb_file = PDBFile.open(uuid)
            pdb_file.tex_export()
    elif args.new_pdb_filename:
        from phystool.config import config
        print(config.new_pdb_filename())
    elif args.consolidate:
        from phystool.metadata import Metadata
        metadata = Metadata()
        metadata.consolidate()
    elif args.about:
        from phystool.metadata import Metadata
        from phystool.__about__ import __version__
        about = Metadata().stats()
        about['version'] = __version__
        print(about)
    elif args.git:
        from phystool.physgit import run_git_in_terminal
        run_git_in_terminal()


def _search(args):
    from phystool.metadata import Metadata
    from phystool.tags import Tags
    metadata = Metadata()
    for pdb_file in metadata.filter(
        query=args.query,
        uuid_bit=args.uuid,
        file_types=args.type,
        selected_tags=args.tags,
        excluded_tags=Tags({})
    ):
        print(f"{pdb_file.uuid}:{pdb_file.title:<43}")


def _pdbfile(args):
    pdb_file = args.uuid
    if args.pytex:
        pdb_file.pytex()
        return
    elif args.cat:
        pdb_file.cat()
        return
    elif args.zip:
        pdb_file.zip()
        return

    from phystool.metadata import Metadata
    metadata = Metadata()
    if args.reset:
        from phystool.pdbfile import PDBFile
        pdb_file.tex_file.with_suffix(".json").unlink(missing_ok=True)
        pdb_file = PDBFile.open(pdb_file.uuid)
        pdb_file.save()
        metadata.update(pdb_file)
        metadata.save()
    elif args.remove:
        from phystool.helper import terminal_yes_no
        pdb_file.cat()
        if terminal_yes_no("Remove files?"):
            metadata.remove(pdb_file)
            metadata.save()
    elif args.parse:
        if pdb_file.parse_texfile():
            metadata.update(pdb_file)
            metadata.save()


def _tags(args):
    pdb_file = args.uuid
    old_tags_data = pdb_file.tags.data.copy()
    pdb_file.tags += args.add
    pdb_file.tags -= args.remove
    if (old_tags_data != pdb_file.tags.data):
        pdb_file.save()
        from phystool.metadata import Metadata
        metadata = Metadata()
        metadata.update(pdb_file)
        metadata.save()

    if args.list:
        pdb_file.tags.list_tags()


def _pdflatex(args):
    from phystool.latex import (
        PdfLatex,
        LatexLogParser,
        LogFileMessage,
        texfile_to_symlink,
    )
    from phystool.pdbfile import PDBFile
    from pathlib import Path
    if args.raw_log:
        LogFileMessage.toggle_verbose_mode()

    try:
        pdb_file = PDBFile.open(args.filename)
        pdb_file.compile()
    except ValueError:
        fname = Path(args.filename)
        if not fname.exists():
            logger.error(f"'{fname}' not found")
            return
        if (fname.suffix == ".log" or args.logtex):
            if not fname.with_suffix(".log").exists():
                fname = texfile_to_symlink(fname).with_suffix(".log")
            latex_log_parser = LatexLogParser(fname)
            latex_log_parser.process()
            latex_log_parser.display()
        else:
            pdflatex = PdfLatex(texfile_to_symlink(fname))
            if args.output:
                pdflatex.full_compile(args.output, args.can_recompile)
            if args.clean:
                pdflatex.clean([".aux", ".log", ".out", ".toc"])


def _evaluation(args):
    from phystool.metadata import Metadata
    metadata = Metadata()
    if args.klass_list_current:
        metadata.klass_list()
    elif args.create_for_klass:
        metadata.evaluation_create_for_klass(args.create_for_klass)
    elif args.list_current:
        metadata.evaluation_list()
    elif args.search:
        metadata.evaluation_search(args.search)
    elif args.edit:
        metadata.evaluation_edit(args.edit)
    elif args.update:
        metadata.evaluation_update(args.update)


def get_parser():
    from argparse import (
        ArgumentParser,
        ArgumentDefaultsHelpFormatter,
    )
    from phystool.pdbfile import PDBFile, VALID_TYPES
    from phystool.tags import Tags
    from phystool.latex import PdfLatex

    parser = ArgumentParser(
        prog="phystool",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=_default)
    parser.add_argument(
        "--gui", help="Run graphical user interface",
        action='store_true'
    )
    parser.add_argument(
        "--dmenu", help="Open file via dmenu",
        action='store_true',
    )
    parser.add_argument(
        "--list-tags", help="List all possible tags",
        action='store_true',
    )
    parser.add_argument(
        "--consolidate", help="Consolidate database",
        action='store_true'
    )
    parser.add_argument(
        "--new-pdb-filename", help="Returns new PDBFile filename",
        action='store_true',
    )
    parser.add_argument(
        "--tex-export-pdb-files", help="Print tex string multiple PdbFiles",
        nargs='*', default=None,
    )
    parser.add_argument(
        "--git", help="Commit database modifications to git",
        action='store_true',
    )
    parser.add_argument(
        "--about", help="Print information about phystool and the database",
        action='store_true',
    )

    sub_parser = parser.add_subparsers()
    ###########################
    # search
    ###########################
    search_parser = sub_parser.add_parser(
        "search", help="Search in database",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    search_parser.set_defaults(func=_search)
    search_parser.add_argument(
        "--tags", help="Filter by tags",
        default=Tags({}), type=Tags.validate
    )
    search_parser.add_argument(
        "--type", help="Filter by types",
        default=VALID_TYPES, type=PDBFile.validate_type
    )
    search_parser.add_argument(
        "--uuid", help="Filter by uuid containing",
        default=""
    )
    search_parser.add_argument(
        "--query", help="Filter the search by content matching the query",
        default=""
    )

    ###########################
    # PDBFile
    ###########################
    pdbfile_parser = sub_parser.add_parser(
        "pdbfile", help="Act on pdbfile",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    pdbfile_parser.set_defaults(func=_pdbfile)
    pdbfile_parser.add_argument(
        "uuid", help="Select the PDBFile by its uuid",
        type=PDBFile.open,
    )
    pdbfile_parser.add_argument(
        "--pytex", help="Execute Python code",
        action='store_true'
    )
    pdbfile_parser.add_argument(
        "--cat", help="Display in terminal",
        action='store_true'
    )
    pdbfile_parser.add_argument(
        "--zip", help="Zip with its dependencies",
        action='store_true'
    )
    pdbfile_parser.add_argument(
        "--remove", help="Remove from database",
        action='store_true',
    )
    pdbfile_parser.add_argument(
        "--reset", help="Reset data (useful to change it's PDB_TYPE)",
        action='store_true',
    )
    pdbfile_parser.add_argument(
        "--parse", help="Update metadata by parsing the .tex file",
        action='store_true'
    )

    ###########################
    # PDBFile -> Tags
    ###########################
    sub_sub_parser = pdbfile_parser.add_subparsers()
    tags_subparser = sub_sub_parser.add_parser(
        "tags",
        help="List or edit tags for selected PDBFile",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    tags_subparser.set_defaults(func=_tags)
    tags_subparser.add_argument(
        "--add", help="Add tags given as a comma separated list",
        type=Tags.validate, default=Tags({})
    )
    tags_subparser.add_argument(
        "--remove", help="Remove tags given as a comma separated list",
        type=Tags.validate, default=Tags({})
    )
    tags_subparser.add_argument(
        "--list", help="List tags", action='store_true'
    )

    ###########################
    # PdfLatex
    ###########################
    pdflatex_parser = sub_parser.add_parser(
        "pdflatex",
        help="Compile PDBFile, compile LaTeX documents or parse logs",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    pdflatex_parser.set_defaults(func=_pdflatex)
    pdflatex_parser.add_argument(
        "filename", help="PDBFile's uuid or regular path to LaTeX file",
    )
    pdflatex_parser.add_argument(
        "--output", help="Compile a LaTeX file and move pdf",
        type=PdfLatex.output
    )
    pdflatex_parser.add_argument(
        "--logtex", help="Dislpay LaTeX .log file",
        action='store_true'
    )
    pdflatex_parser.add_argument(
        "--can-recompile", help="Compile a second time if the log file mentions the need",
        action='store_true'
    )
    pdflatex_parser.add_argument(
        "--raw-log", help="Display LaTeX raw error message",
        action='store_true'
    )
    pdflatex_parser.add_argument(
        "--clean", help="Remove LaTeX auxiliary files",
        action='store_true'
    )

    ###########################
    # evaluation
    ###########################
    evaluation_parser = sub_parser.add_parser(
        "evaluation",
        help="Manage evaluations",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    evaluation_parser.set_defaults(func=_evaluation)
    evaluation_parser.add_argument(
        "--klass-list-current", help="List classes of the current year",
        action='store_true'
    )
    evaluation_parser.add_argument(
        "--list-current", help="List current evaluations",
        action='store_true'
    )
    evaluation_parser.add_argument(
        "--create-for-klass", help="Create new evaluation klass",
    )
    evaluation_parser.add_argument(
        "--edit", help="Edit evaluation in extracted json file",
    )
    evaluation_parser.add_argument(
        "--update", help="Update evaluation",
    )
    evaluation_parser.add_argument(
        "--search", help="Search evaluations using given PDBFile",
    )

    return parser
