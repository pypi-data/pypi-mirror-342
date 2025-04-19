import sys
import logging

try:
    from phystool.config_prod import MyConfig
    config = MyConfig(dev_mode=False)
    _DEFAULT_LOGLEVEL = "INFO"
except ModuleNotFoundError:
    from phystool.config_dev import MyConfig
    config = MyConfig(dev_mode=True)
    _DEFAULT_LOGLEVEL = "DEBUG"


########################################################################
# LOGGER ###############################################################
def _handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = _handle_uncaught_exception
LOGGER_BOTH = {
    'handlers': ['default', 'file_handler'],
    'level': 'DEBUG',
    'propagate': False
}
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(lineno)d: %(message)s'
        },
        'minimal': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': _DEFAULT_LOGLEVEL,
            'formatter': 'minimal',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'file_handler': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': config.LOGFILE_PATH,
            'mode': 'a',
            'maxBytes': 200000,
            'backupCount': 2
        },
    },
    'loggers': {
        '': LOGGER_BOTH,  # root logger
        '__main__': LOGGER_BOTH,  # if __name__ == '__main__'
        'dmenuphys': LOGGER_BOTH,
        'helper': LOGGER_BOTH,
        'latex': LOGGER_BOTH,
        'metadata': LOGGER_BOTH,
        'pdbfile': LOGGER_BOTH,
        'physgit': LOGGER_BOTH,
        'qt': LOGGER_BOTH,
        'pytex': LOGGER_BOTH,
        'tags': LOGGER_BOTH,
    }
}
