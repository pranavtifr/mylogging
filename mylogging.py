"""Module for logging."""
import logging
import sys


def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle Exceptions in log."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


class LoggerWriter(object):
    """Make Print statements go to Log."""

    def __init__(self, writer):
        """init."""
        self._writer = writer
        self._msg = ''

    def write(self, message):
        """write."""
        self._msg = self._msg + message
        while '\n' in self._msg:
            pos = self._msg.find('\n')
            self._writer(self._msg[:pos])
            self._msg = self._msg[pos+1:]

    def flush(self):
        """flush."""
        if self._msg != '':
            self._writer(self._msg)
            self._msg = ''


def setloglevel(filename, log):
    """
    Set log level and filename.

    Parameters:
    filename: String, Filename
        If None, Write to STDERR
    log: String, LogLevel
        Same levels as the logging module

    """
    loglevel = log.upper()
    if not filename:
        logging.basicConfig(format='(%(asctime)s %(filename)s %(levelname)s) '
                            + '%(funcName)s %(lineno)d >> %(message)s',
                            level=getattr(logging, loglevel, None))
    else:
        logging.basicConfig(format='(%(asctime)s %(filename)s %(levelname)s) '
                            + '%(funcName)s %(lineno)d >> %(message)s',
                            filename=filename,
                            filemode='w',
                            level=getattr(logging, loglevel, None))

    logging.captureWarnings(True)
    log = logging.getLogger()
    sys.stdout = LoggerWriter(log.info)
    sys.stderr = LoggerWriter(log.warning)
    sys.excepthook = handle_exception
