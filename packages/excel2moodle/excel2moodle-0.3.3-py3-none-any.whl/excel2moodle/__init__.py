"""This Python program helps to create Moodle questions in less time.

The aim is to put alle the information for the questions into a spreadsheet file, and then parse it, to generate Moodle compliant XML-Files.
Furthermore this program lets you create a single ``.xml``-File with a selection of questions, that then can be imported to a Moodle-Test.

Concept
=========
The concept is, to store the different questions into categories of similar types and difficulties of questions, for each of which, a separated sheet in the Spreadsheet document should be created.

There Should be a sheet called *"Kategorien"*, where an overview over the different categories is stored.
This sheet stores The names and descriptions, for all categories. The name have to be the same as the actual sheet names with the questions.
Furthermore the points used for grading, are set in the "Kategorien" sheet

Functionality
===============
* Parse multiple Choice Questions, each into one XML file
* Parse Numeric Questions, each into one XML file
* create single XML File from a selection of questions
"""
from importlib import metadata
from importlib.metadata import version
try:
    __version__ = version("excel2moodle")
except Exception:
    __version__ = "unknown"


if not __package__ == None:
    meta = metadata.metadata(__package__)
    e2mMetadata:dict = {
        "version": __version__,
        "name": meta['name'],
        "description": meta['summary'],
        "author": meta['author'],
        "license": meta['license-expression'],
        "documentation": "https://jbosse3.gitlab.io/excel2moodle",
        "homepage": meta['project-url'].split()[1],
        "issues": "https://gitlab.com/jbosse3/excel2moodle/issues",
    } 

# from excel2moodle.core import klausurGenerator
# from excel2moodle.core import numericMultiQ
# from excel2moodle.core import questionWriter
# from excel2moodle.core import questionParser
# from excel2moodle.core import stringHelpers
# from excel2moodle.core import globals
#
# from excel2moodle.ui import kGeneratorQt
from excel2moodle.ui import settings

from PySide6.QtCore import QObject, Signal
import logging as logging
from logging import config as logConfig

loggerConfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'excel2moodle.questionParser': { 
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
    } 
}

class QSignaler(QObject):
    signal = Signal(str)

class LogHandler(logging.Handler):
    def __init__(self, *args, **kwargs)->None:
        super().__init__(*args,**kwargs)
        self.emitter = QSignaler()
         # Define a formatter with log level and module
        log_format = "[%(levelname)s] %(module)s: %(message)s"
        self.formatter = logging.Formatter(log_format)
        self.setFormatter(self.formatter)
        self.logLevelColors = {
            'DEBUG': 'gray',
            'INFO': 'green',
            'WARNING': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'pink'
        }

    def emit(self, record)->None:
        log_message = self.format(record)
        color = self.logLevelColors.get(record.levelname, 'black')
        prettyMessage = f'<span style="color:{color};">{log_message}</span>'
        self.emitter.signal.emit(prettyMessage)
        return None


settings = settings.Settings()

logger = logging.getLogger(__name__)
logging.config.dictConfig(config=loggerConfig)

qSignalLogger = LogHandler()
logger.addHandler(qSignalLogger)


for k,v in e2mMetadata.items():
    print(f"{k}: \t {v}\n")
