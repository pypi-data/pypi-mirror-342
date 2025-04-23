from logging.config import dictConfig

from phystool.config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


def phystool() -> None:
    """Run the command line interface"""
    from phystool.cli import get_parser
    args = get_parser().parse_args()
    args.func(args)


def physnoob() -> None:
    """Run the graphical user interface"""
    try:
        from phystool.qt import PhysQt
        qt = PhysQt()
        qt.exec()
    except Exception as e:
        # If a tex file is missing from the DB (was manually removed), physnoob
        # will fail to start because it tries to display all pdb_files stored
        # in the db. It won't be able to sort the files and will raise an
        # exception. Here we just try to consolidate the metadata to start from
        # a clean DB
        from logging import getLogger
        from phystool.metadata import Metadata
        logger = getLogger(__name__)
        logger.exception(e)
        metadata = Metadata()
        metadata.consolidate()
