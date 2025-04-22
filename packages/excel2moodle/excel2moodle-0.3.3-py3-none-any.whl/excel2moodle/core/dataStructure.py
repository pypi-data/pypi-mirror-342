"""Main Module which does the heavy lifting 

At the heart is the class ``xmlTest``
"""

from pathlib import Path
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTreeWidget
import pandas as pd
import lxml.etree as ET
import logging

from excel2moodle import QSignaler
from excel2moodle.core import stringHelpers
from excel2moodle.core.category import Category
from excel2moodle.ui.dialogs import QuestionVariantDialog
from excel2moodle.ui.treewidget import QuestionItem, CategoryItem
from excel2moodle.core.questionValidator import Validator
from excel2moodle.ui.settings import Settings
from excel2moodle.core.question import Question
from excel2moodle.core.exceptions import InvalidFieldException, QNotParsedException


logger = logging.getLogger(__name__)


class QuestionDB():
    """oberste Klasse für den Test"""
    dataChanged = QSignaler()

    def __init__(self, settings:Settings):
        self.settings = settings
        self.spreadSheetPath = Path()
        self.mainPath = Path()
        self.window:QMainWindow|None = None
        self.version = None
        self.categoriesMetaData = pd.DataFrame()
        self.categories:dict[str,Category]={}
        self.settings.shPathChanged.connect(self.onSheetPathChanged)

    @QtCore.Slot(Path)
    def onSheetPathChanged(self, sheet:Path)->None:
        logger.debug("Slot, new Spreadsheet triggered")
        self.spreadSheetPath = sheet
        self.svgFolder = (self.spreadSheetPath.parent / 'Abbildungen_SVG')
        self.retrieveCategoriesData()
        self.parseAll()

    def retrieveCategoriesData(self)->None:
        """Scans through the sheet with the metadata for all the question categories

        The information that will be shown in the UI like description and points is retrieved from one spreadsheet sheet.
        This method gathers this information and stores it in the ``categoriesMetaData`` dataframe
        """

        logger.info("Start Parsing the Excel Metadata Sheet\n")
        with open(self.spreadSheetPath, 'rb') as f:
            excelFile = pd.ExcelFile(f)
            self.categoriesMetaData = pd.read_excel(f, sheet_name="Kategorien", 
                                                    usecols=["Kategorie", "Beschreibung", "Punkte", "Version"],
                                                    index_col=0)
            logger.info("Sucessfully read categoriesMetaData")
            print(self.categoriesMetaData)
            self.categories = {}
            for sh in excelFile.sheet_names:
                if sh.startswith("KAT"):
                    n = int(sh[4:])
                    katDf = pd.read_excel(f, sheet_name=str(sh), index_col=0, header=None)
                    if not katDf.empty:
                        p = self.categoriesMetaData["Punkte"].iloc[n-1]
                        points = (p if not pd.isna(p) else 1)
                        v = self.categoriesMetaData["Version"].iloc[n-1]
                        version = (v if not pd.isna(v) else 0)
                        self.categories[sh] = Category(n,sh, 
                                                       self.categoriesMetaData["Beschreibung"].iloc[n-1],
                                                       dataframe=katDf, 
                                                       points=points,
                                                       version=version)
        self.dataChanged.signal.emit("whoo")
        return None


    def parseAll(self):
        self.mainTree = ET.Element("quiz")
        for c in self.categories.values():
            validator = Validator(c)
            for q in c.dataframe.columns:
                logger.debug(f"Starting to check Validity of {q}")
                qdat = c.dataframe[q]
                if isinstance(qdat, pd.Series):
                    validator.setup(qdat, q)
                    check = False
                    try:
                        check = validator.validate()
                    except InvalidFieldException as e:
                        logger.error(f"Question {c.id}{q:02d} is invalid.", exc_info=e)
                    if check: 
                        c.questions[q]=validator.question
                        try:
                            c.parseQ(c.questions[q], validator.qdata)
                        except QNotParsedException as e:
                            logger.error(f"Frage {c.questions[q].id} konnte nicht erstellt werden", exc_info=e)

    def appendQuestions(self, questions:list[QuestionItem], file:Path|None=None):
        tree = ET.Element("quiz")
        catdict:dict[Category,list[Question]]={}
        for q in questions:
            logger.debug(f"got a question to append {q=}")
            cat = q.parent().getCategory()
            if cat not in catdict:
                catdict[cat] = []
            print(f"Category is parent of Q {cat=}")
            catdict[cat].append(q.getQuestion())
        for cat, qlist in catdict.items():
            print(f"{cat = }, mit fragen {qlist = }")
            self.appendQElements(cat, qlist, tree=tree, includeHeader=self.settings.value("testGen/includeCats"))
        stringHelpers.printDom(tree, file=file)

    def appendQElements(self,cat:Category,  qList:list[Question], tree:ET.Element, includeHeader:bool=True)->None:
        if includeHeader:
            tree.append( cat.getCategoryHeader())
            logger.debug(f"Appended a new category item {cat=}")
        sameVariant = False
        variant = 1
        for q in qList:
            if cat.parseQ(q):
                if q.variants is not None:
                    if sameVariant is False:
                        dialog = QuestionVariantDialog(self.window, q)
                        if dialog.exec() == QtWidgets.QDialog.Accepted:
                            variant = dialog.variant
                            sameVariant = dialog.categoryWide
                            logger.debug(f"Die Fragen-Variante {variant} wurde gewählt")
                            q.assemble(variant)
                        else: print("skipping this question")
                else:
                    q.assemble()
                tree.append(q.element)
            else: logger.warning(f"Frage {q} wurde nicht erstellt")
        return None


