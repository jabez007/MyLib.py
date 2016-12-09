import logging
import os

LOG_PATH = os.path.dirname(os.path.realpath(__file__))


class MyLog(logging.Logger):

    def __init__(self, name=__name__, level="INFO", file_ext="log"):
        """

        :param name:
        :param level: DEBUG, INFO, WARN, ERROR, CRITICAL - the logger will write everything at that level and down
        :param file_ext:
        """
        level = level.upper()
        log_level = getattr(logging, level, "INFO")
        logging.Logger.__init__(self, name, log_level)

        # create a file handler
        log_filename = ".".join([name, level, file_ext])
        handler = logging.FileHandler(os.path.join(LOG_PATH, log_filename))
        handler.setLevel(log_level)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.addHandler(handler)

# # # #


if __name__ == "__main__":
    levels = ['debug', 'info', 'warn', 'error', 'critical']
    for lvl in levels:
        my_log = MyLog(level=lvl, log_file="test.log")
        my_log.debug('Hello World')
        my_log.info('Hello World')
        my_log.warn('Hello World')
        my_log.error('Hello World', exc_info=True)
        my_log.exception('Hello World')  # same as above
        my_log.critical('Hello World')
        del my_log
