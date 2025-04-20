import logging as log
from argparse import Namespace, ArgumentParser
from enum import IntEnum
from logging import basicConfig, StreamHandler
from logging.handlers import RotatingFileHandler

INFO_FORMAT = '%(message)s'
DEBUG_FORMAT = '[%(name)s] [%(levelname)s] %(message)s'
TRACE_FORMAT = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'

TRACE_LEVEL = 5
TRACE_NAME = 'TRACE'


class LogLevel(IntEnum):
    FATAL = log.FATAL
    ERROR = log.ERROR
    WARNING = log.WARNING
    INFO = log.INFO
    DEBUG = log.DEBUG
    TRACE = TRACE_LEVEL

    def __str__(self):
        return self.name


def cli_logg_util_setup_parser(parser: ArgumentParser):
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity')
    parser.add_argument('--log-file', help='Rotating log file name pattern i.e. ')
    parser.add_argument('--log-file-level', type=LogLevel, default=LogLevel.INFO, choices=list(LogLevel),
                        help='Increase verbosity')
    parser.add_argument('--log-file-backups', type=int, default=10, help='Maximum number of backup log files to keep')
    parser.add_argument('--log-file-size', type=int, default=100 * 1024 * 1024, help='Maximum log file size in bytes')

    if not hasattr(log, "TRACE"):
        log.TRACE = TRACE_LEVEL
        log.addLevelName(TRACE_LEVEL, TRACE_NAME)

        def trace(self, message, *args, **kws):
            if self.isEnabledFor(TRACE_LEVEL):
                # Yes, logger takes its '*args' as 'args'.
                self._log(TRACE_LEVEL, message, args, **kws)

        log.Logger.trace = trace


def cli_logg_util_setup(args: Namespace):
    log_level = log.INFO
    format_ = INFO_FORMAT

    if args.verbose == 1:
        log_level = log.DEBUG
        format_ = DEBUG_FORMAT
    elif args.verbose == 2:
        log_level = log.TRACE
        format_ = TRACE_FORMAT

    handlers = [StreamHandler()]

    if args.log_file is not None:
        rfh = RotatingFileHandler(args.log_file, 'a', args.log_file_size, args.log_file_backups)
        handlers.append(rfh)
    basicConfig(
        level=log_level,
        format=format_,
        handlers=handlers
    )
