
import logging
import pandas as pd
import lxml.etree as ET

from excel2moodle.core.exceptions import InvalidFieldException
from excel2moodle.core.questionValidator import Validator
logger = logging.getLogger(__name__)
from excel2moodle.core.question import Question

from excel2moodle.core.globals import XMLTags, TextElements, DFIndex, questionTypes, parserSettings
from excel2moodle.core.parser import NFMQuestionParser, NFQuestionParser, MCQuestionParser, QNotParsedException

class Category():
    def __init__(self, n:int, name:str, description:str, dataframe: pd.DataFrame, points:float=0, version:int=0)->None:
        self.n = n
        self.NAME = name
        self.desc = str(description)
        self.dataframe:pd.DataFrame = dataframe
        self.points = points
        self.version = int(version)
        self.questions:dict[int,Question] = {}
        self.maxVariants:int|None = None
        logger.info(f"initializing {self.NAME =}")

    @property
    def name(self):
        return self.NAME

    @property
    def id(self):
        return f"{self.version}{self.n:02d}"

    def __hash__(self) -> int:
        return hash(self.NAME)

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Category):
            return self.NAME == other.NAME
        return False

    def parseQ(self, q:Question, questionData:dict|None=None, xmlTree:ET._Element|None=None)->bool:
        if q.element is not None:
            logger.info(f"Question {q.id} is already parsed")
            return True
        else:
            if q.qtype == "NF":
                parser = NFQuestionParser( q, questionData)
                logger.debug(f"setup a new NF parser ")
            elif q.qtype == "MC":
                parser = MCQuestionParser( q, questionData)
                logger.debug(f"setup a new MC parser ")
            elif q.qtype == "NFM":
                parser = NFMQuestionParser( q, questionData)
                logger.debug(f"setup a new NFM parser ")
            else: 
                logger.error(f"ERROR, couldn't setup Parser")
                return False
            try:
                parser.parse(xmlTree=xmlTree)
                return True
            except QNotParsedException as e:
                logger.critical(f"The Question {q.id} couldn't be parsed", exc_info=e, stack_info=True)
                return False
            finally:
                del parser

    def getCategoryHeader(self)->ET.Element:
        """vor den Fragen einer Kategorie wird ein <question type='category'> eingefügt mit Name und Beschreibung"""
        header = ET.Element('question', type='category')
        cat = ET.SubElement(header,"category")
        info = ET.SubElement(header,"info", format='html')
        ET.SubElement(cat,"text").text = f"$module$/top/{self.NAME}"
        ET.SubElement(info,"text").text = str(self.desc)
        ET.SubElement(header,"idnumber").text = str(self.n)
        ET.indent(header)
        return header


