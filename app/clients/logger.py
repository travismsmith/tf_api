import logging

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        'DEBUG': grey,
        'INFO': green,
        'WARNING': yellow,
        'ERROR': red,
        'CRITICAL': bold_red
    }

    def format(self, record):
        levelname = self.FORMATS[record.levelname] + record.levelname + self.reset
        record.levelname = levelname
        return formatter.format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(name)s:%(lineno)d - %(message)s')
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)
