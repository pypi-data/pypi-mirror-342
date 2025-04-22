from asteval import Interpreter
import lxml.etree as ET
from pathlib import Path
import pandas as pd
import base64 as base64
import logging as logging

from excel2moodle.core import question
from excel2moodle.core.exceptions import NanException, QNotParsedException
import excel2moodle.core.etHelpers as eth

from excel2moodle.core.globals import XMLTags, TextElements, DFIndex, questionTypes, parserSettings, feedbackStr, feedBElements
from excel2moodle.core import stringHelpers
from excel2moodle.core.question import Picture, Question
import re as re

from excel2moodle import settings


logger = logging.getLogger(__name__)
f = Path("../Fragensammlung/Abbildungen_SVG/").resolve()
settings.set("core/pictureFolder", f)
svgFolder =  settings.get("core/pictureFolder", default=f)
print(svgFolder)

class QuestionParser():
    def __init__(self, question:Question, data:dict):
        self.question:Question = question
        self.rawInput = data
        logger.debug(f"The following Data was provided for the question {self.question.id}:\n {self.rawInput =}")
        self.genFeedbacks:list[XMLTags] = []

    def hasPicture(self)->bool:
        """Creates a ``Picture`` object inside ``question``, if the question needs a pic"""

        picKey = self.rawInput[DFIndex.PICTURE]
        if picKey != 0 and picKey != 'nan':
            if not hasattr(self.question, 'picture'):
                self.question.picture = Picture(picKey, svgFolder, self.question)
            if self.question.picture.ready:
                return True
        return False

    def setMainText(self)->None:
        paragraphs:list[ET._Element]=[TextElements.PLEFT.create()]
        ET.SubElement(paragraphs[0],"b").text = f"ID {self.question.id}"
        text = self.rawInput[DFIndex.TEXT]
        pcount = 0
        for t in text:
            if not pd.isna(t):
                pcount +=1
                paragraphs.append(TextElements.PLEFT.create())
                paragraphs[-1].text = t
        self.question.qtextParagraphs = paragraphs
        logger.debug(f"Created main Text {self.question.id} with:{pcount} paragraphs")
        return None
 
    def setBPoints(self)->None:
        """If there bulletPoints are set in the Spreadsheet it creates an unordered List-Element in ``Question.bulletList``"""
        if DFIndex.BPOINTS in self.rawInput:
            bps:str = self.rawInput[DFIndex.BPOINTS]
            try:
                bulletList = self.formatBulletList(bps)
            except IndexError as e:
                raise QNotParsedException(f"konnt Bullet Liste {self.question.id} nicht generieren", self.question.id, exc_info=e)
            logger.debug(f"Generated BPoint List: \n {ET.tostring(bulletList, encoding='unicode')}")
            self.question.bulletList = bulletList
        return None

    def formatBulletList(self,bps:str)->ET.Element:
        logger.debug(f"Formatting the bulletpoint list")
        li:list[str] = stringHelpers.stripWhitespace( bps.split(';'))
        name = []
        var = []
        quant = []
        unit = []
        unorderedList = TextElements.ULIST.create()
        for item in li:
            sc_split = item.split()
            name.append(sc_split[0])
            var.append(sc_split[1])
            quant.append(sc_split[3])
            unit.append(sc_split[4])
        for i in range(0, len(name)):
            if re.fullmatch(r"{\w+}", quant[i]):
                logger.debug(f"Got an variable bulletItem")
                num_s = quant[i]
            else:
                logger.debug(f"Got a normal bulletItem")
                num = quant[i].split(',')
                if len(num)==2:
                    num_s = f"{str(num[0])},\\!{str(num[1])}~"
                else: num_s = f"{str(num[0])},\\!0~"
            bullet = TextElements.LISTITEM.create()
            bullet.text=(f"{ name[i] }: \\( {var[i]} = {num_s} \\mathrm{{ {unit[i]}  }}\\)\n")
            unorderedList.append(bullet)
        return unorderedList

    def appendToTmpEle(self, eleName: str, text:str|DFIndex, txtEle=False, **attribs ):
        """Appends the text to the temporary Element"""
        t = self.rawInput[text] if isinstance(text, DFIndex) else text
        if txtEle is False:
            self.tmpEle.append(eth.getElement(eleName, t, **attribs))
        elif txtEle is True:
            self.tmpEle.append(eth.getTextElement(eleName, t, **attribs))

    def appendFromSettings(self, key="standards")->None:
        """Appends 1 to 1 mapped Elements defined in the parserSettings to the element"""
        parser = ["Parser"]
        if isinstance(self, MCQuestionParser):
                parser.append("MCParser")
        elif isinstance(self, NFQuestionParser):
            parser.append("NFParser")
        for p in parser:
            try:
                for k, v in parserSettings[p][key].items():
                    self.appendToTmpEle(k, text=v)
            except KeyError as e:
                msg = f"Invalider Input aus den Einstellungen Parser: {type(p) = }"
                logger.error(msg, exc_info=e)
                raise QNotParsedException(msg, self.question.id, exc_info=e)
        return None

    def parse(self, xmlTree: ET._Element|None=None)->None:
        """Parses the Question
        
        Generates an new Question Element stored as ``self.tmpEle:ET.Element``
        if no Exceptions are raised, ``self.tmpEle`` is passed to ``self.question.element``
        """
        logger.info(f"Starting to parse {self.question.id}")
        self.tmpEle = ET.Element(XMLTags.QUESTION, type = self.question.moodleType)
        # self.tmpEle.set(XMLTags.TYPE, self.question.moodleType)
        self.appendToTmpEle(XMLTags.NAME, text=DFIndex.NAME, txtEle=True)
        self.appendToTmpEle(XMLTags.ID, text=self.question.id)
        if self.hasPicture() :
            self.tmpEle.append(self.question.picture.element)
        self.tmpEle.append(ET.Element(XMLTags.QTEXT, format = "html"))
        self.appendToTmpEle(XMLTags.POINTS, text=str(self.question.points))
        self.appendToTmpEle(XMLTags.PENALTY, text="0.3333")
        self.appendFromSettings()
        for feedb in self.genFeedbacks:
            self.tmpEle.append(eth.getFeedBEle(feedb))
        if xmlTree is not None:
            xmlTree.append(self.tmpEle)
        ansList = self.setAnswers()
        self.setMainText()
        self.setBPoints()
        if ansList is not None:
            for ele in ansList:
                self.tmpEle.append(ele)
        logger.info(f"Sucessfully parsed {self.question.id}")
        self.question.element = self.tmpEle
        return None

    def getFeedBEle(self, feedback:XMLTags, text:str|None=None, style: TextElements | None = None)->ET.Element:
        if style is None:
            span = feedBElements[feedback]
        else: 
            span = style.create()
        if text is None:
            text = feedbackStr[feedback]
        ele = ET.Element(feedback, format="html")
        par = TextElements.PLEFT.create()
        span.text = text
        par.append(span)
        ele.append(eth.getCdatTxtElement(par))
        return ele
    
    def setAnswers(self)->list[ET.Element]|None:
        """Needs to be implemented in the type-specific subclasses"""
        return None

    @staticmethod
    def getNumericAnsElement(result:int|float, 
                             tolerance:float = 0.01, 
                             fraction:int|float = 100, 
                             format:str = "moodle_auto_format")->ET.Element:
        """Returns an ``<answer/>`` Element specific for the numerical Question
        The element contains those childs:
            ``<text/>`` which holds the value of the answer
            ``<tolerace/>`` with the *relative* tolerance for the result
            ``<feedback/>`` with general feedback for a true answer
        """

        ansEle:ET.Element = eth.getTextElement(XMLTags.ANSWER, text = str(result), fraction = str(fraction), format = format)
        ansEle.append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, feedbackStr["right1Percent"], TextElements.SPANGREEN))
        tol = abs(round(result*tolerance, 3))
        ansEle.append(eth.getElement(XMLTags.TOLERANCE, text = str(tol)))
        return ansEle

class NFQuestionParser(QuestionParser):
    def __init__(self, *args)->None:
        super().__init__(*args)
        self.genFeedbacks=[XMLTags.GENFEEDB]

    def setAnswers(self)->list[ET.Element]:
        result = self.rawInput[DFIndex.RESULT]
        ansEle:list[ET.Element]=[]
        ansEle.append(self.getNumericAnsElement( result = result ))
        return ansEle

class NFMQuestionParser(QuestionParser):
    def __init__(self, *args):
        super().__init__(*args)
        self.genFeedbacks=[XMLTags.GENFEEDB]
        self.astEval = Interpreter()

    def setAnswers(self)->None:
        equation = self.rawInput[DFIndex.RESULT]
        bps = str( self.rawInput[DFIndex.BPOINTS] )
        ansElementsList:list[ET.Element]=[]
        varNames:list[str]= self._getVarsList(bps)
        self.question.variables, number = self._getVariablesDict(varNames)
        for n in range(number):
            self._setupAstIntprt(self.question.variables, n)
            result = self.astEval(equation)
            if isinstance(result, float):
                ansElementsList.append(self.getNumericAnsElement( result = round(result,3) ))
        self.question.answerVariants = ansElementsList
        self.setVariants(len(ansElementsList))
        return None

    def setVariants(self, number:int):
        self.question.variants = number
        mvar = self.question.category.maxVariants
        if mvar is None:
            self.question.category.maxVariants = number
        else:
            self.question.category.maxVariants = number if number <= mvar else mvar


    def _setupAstIntprt(self, var:dict[str, list[float|int]], index:int)->None:
        """Ubergibt die Parameter mit entsprechenden Variablen-Namen an den asteval-Interpreter.

        Dann kann dieser die equation lesen.
        """
        for name,value in var.items():
            self.astEval.symtable[name] = value[index]
        return None

    def _getVariablesDict(self, keyList: list)-> tuple[dict[str,list[float]],int]:
        """Liest alle Variablen-Listen deren Name in ``keyList`` ist aus dem DataFrame im Column[index]"""
        dic:dict = {}
        num:int = 0
        for k in keyList:
            val = self.rawInput[k]
            if isinstance(val, str)  :
                li =  stringHelpers.stripWhitespace(val.split(";"))
                num = len(li)
                vars:list[float] =  [ float(i.replace(",",".")) for i in li ]
                dic[str(k)] = vars
            else: 
                dic[str(k)] = [str(val)]
                num = 1
        print(f"Folgende Variablen wurden gefunden:\n{dic}\n")
        return dic, num

    @staticmethod
    def _getVarsList(bps: str|list[str])->list:
        """
        Durchsucht den bulletPoints String nach den Variablen, die als "{var}" gekennzeichnet sind
        """
        vars = []
        if isinstance(bps, list):
            for p in bps:
                vars.extend(re.findall(r"\{\w\}", str(bps)))
        else:
            vars = re.findall(r"\{\w\}", str(bps))
        variablen=[]
        for v in vars:
            variablen.append(v.strip("{}"))
        return variablen

class MCQuestionParser(QuestionParser):
    def __init__(self, *args)->None:
        super().__init__(*args)
        self.genFeedbacks=[
            XMLTags.CORFEEDB,
            XMLTags.PCORFEEDB,
            XMLTags.INCORFEEDB,
            ]

    def getAnsElementsList(self, answerList:list, fraction:float=50, format="html")->list[ET.Element]:
        elementList: list[ET.Element] = []
        for ans in answerList:
            p = TextElements.PLEFT.create()
            p.text = str(ans)
            text = eth.getCdatTxtElement(p)
            elementList.append(ET.Element(XMLTags.ANSWER, fraction=str(fraction), format=format))
            elementList[-1].append(text)
            if fraction < 0:
                elementList[-1].append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, 
                                                        text = feedbackStr["wrong"], 
                                                        style = TextElements.SPANRED))
            elif fraction > 0:
                elementList[-1].append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, 
                                                        text=feedbackStr["right"], 
                                                        style=TextElements.SPANGREEN))
        return elementList


    def setAnswers(self)->list[ET.Element]:
        ansStyle = self.rawInput[DFIndex.ANSTYPE]
        true = stringHelpers.stripWhitespace(self.rawInput[DFIndex.TRUE].split(';'))
        trueAnsList = stringHelpers.texWrapper(true, style=ansStyle)
        false = stringHelpers.stripWhitespace(self.rawInput[DFIndex.FALSE].split(';'))
        falseAnsList= stringHelpers.texWrapper(false, style=ansStyle)
        truefrac = 1/len(trueAnsList)*100
        falsefrac = 1/len(trueAnsList)*(-100)
        self.tmpEle.find(XMLTags.PENALTY).text=str(round(truefrac/100, 4))
        ansList = self.getAnsElementsList(trueAnsList, fraction=round(truefrac, 4))
        ansList.extend(self.getAnsElementsList(falseAnsList, fraction=round(falsefrac, 4)))
        return ansList

