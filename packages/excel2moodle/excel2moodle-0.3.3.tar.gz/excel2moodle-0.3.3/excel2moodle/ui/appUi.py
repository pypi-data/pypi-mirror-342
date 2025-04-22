"""This Module holds the extended  class mainWindow() and any other main Windows

It needs to be seperated from ``windowMain.py`` because that file will be changed by tho ``pyside6-uic`` command,
which generates the python code from the ``.ui`` file
"""

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6 import QtWidgets
from pathlib import Path
from excel2moodle import e2mMetadata
from excel2moodle.ui.windowMain import Ui_MoodleTestGenerator
from .windowEquationChecker import Ui_EquationChecker
from excel2moodle.ui import windowEquationChecker, dialogs
from excel2moodle.core.dataStructure import QuestionDB
from excel2moodle.ui.treewidget import QuestionItem, CategoryItem
from excel2moodle.extra import equationVerification as eqVerif
from excel2moodle import qSignalLogger
from excel2moodle.ui.settings import Settings
import logging as logging


logger = logging.getLogger(__name__)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, settings:Settings, testDB:QuestionDB)->None:
        super().__init__()
        self.settings = settings
        self.excelPath: Path|None = None
        self.mainPath = (self.excelPath.parent if self.excelPath is not None else None)
        self.exportFile = Path()
        self.testDB = testDB
        self.ui = Ui_MoodleTestGenerator()
        self.ui.setupUi(self)

        self.ui.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.ui.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ui.checkBoxIncludeCategories.setChecked(self.settings.value("testGen/includeCats", type=bool))

        self.ui.retranslateUi(self)
        logger.info(f"Settings are stored under: {self.settings.fileName()}")
        self.ui.pointCounter.setReadOnly(True)
        self.ui.questionCounter.setReadOnly(True)
        self.setStatus("Wählen Sie bitte eine Excel Tabelle und einen Export Ordner für die Fragen aus")
        try:
            self.resize(self.settings.value("windowSize"))
            self.move(self.settings.value("windowPosition"))
        except Exception:
            pass
        self.connectEvents()

    def connectEvents(self)->None:
        self.ui.treeWidget.itemClicked.connect(self.onSelectionChanged)
        self.ui.checkBoxQuestionListSelectAll.checkStateChanged.connect(self.toggleQuestionSelectionState)
        qSignalLogger.emitter.signal.connect(self.updateLog)
        self.ui.actionEquationChecker.triggered.connect(self.onButOpenEqChecker)
        self.ui.checkBoxIncludeCategories.checkStateChanged.connect(self.setIncludeCategoriesSetting)
        # self.ui.buttonRefresh.clicked.connect(self.refreshList)
        self.ui.actionParseAll.triggered.connect(self.onParseAll )
        self.testDB.dataChanged.signal.connect(self.onParseAll)
        self.ui.buttonSpreadSheet.clicked.connect(self.onButSpreadsheet)
        self.ui.buttonTestGen.clicked.connect(self.onButGenTest)
        self.ui.actionPreviewQ.triggered.connect(self.previewQ)
        self.ui.actionAbout.triggered.connect(self.onAbout)
        self.settings.shPathChanged.connect(self.onSheetPathChanged)


    @QtCore.Slot(Path)
    def onSheetPathChanged(self, sheet:Path)->None:
        logger.debug("Slot, new Spreadsheet triggered")
        self.spreadSheetPath = sheet
        self.mainPath = sheet.parent
        self.ui.buttonSpreadSheet.setText(str(sheet.name))

    def updateLog(self,log)->None:
        self.ui.loggerWindow.append(log)

    def setIncludeCategoriesSetting(self):
        if self.ui.checkBoxIncludeCategories.isChecked():
            self.settings.set("testGen/includeCats", True)
            logger.debug("set includeCats to True")
        else:
            self.settings.set("testGen/includeCats", False)
            logger.debug("set includeCats to False")


    @QtCore.Slot()
    def onAbout(self):
        aboutMessage: str = f"""
        <h1> About {e2mMetadata['name']}</h1><br>
        <p style="text-align:center">

                <b><a href="{e2mMetadata['homepage']}">{e2mMetadata['name']}</a> - {e2mMetadata['description']}</b>
        </p>
        <p style="text-align:center"> 
            The documentation can be found under <b><a href="{e2mMetadata['documentation']}">{e2mMetadata['documentation']}</a></b>
            </br>
            </br>
            If you encounter any issues please report them under the <a href="{e2mMetadata['issues']}"> repositories issues page</a>
            </br>
        </p>
        <p style="text-align:center">
        This project is maintained by {e2mMetadata['author']}.
        <br>
        Development takes place at <a href="{e2mMetadata['homepage']}">{e2mMetadata['homepage']}</a>
        Contributions are very welcome
        <br>
        </p>
        <p style="text-align:center">
        <i>This project is published under {e2mMetadata['license']}, you are welcome, to share, modify and reuse the code.</i>
        </p>
        """
        QtWidgets.QMessageBox.information(self, 
                                               f"About {e2mMetadata['name']}",
                                               aboutMessage)

    def closeEvent(self, event):
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowPosition", self.pos())

    @QtCore.Slot()
    def onSelectionChanged(self, item, col):
        """Whenever the selection changes the total of selected points needs to be recalculated"""

        count: int = 0
        questions: int = 0
        selection = self.ui.treeWidget.selectedItems()
        for q in selection:
            questions += 1
            count += q.getQuestion().points

        logger.info(f'{questions} questions are selected with {count} points')
        self.ui.pointCounter.setValue(count)
        self.ui.questionCounter.setValue(questions)
        return None

    @QtCore.Slot()
    def toggleQuestionSelectionState(self, state):
        if state == Qt.Checked:
            setter = True
        else: setter = False
        root = self.ui.treeWidget.invisibleRootItem()
        childN = root.childCount()
        for i in range(childN):
            qs = root.child(i).childCount()
            for q in range(qs):
                root.child(i).child(q).setSelected(setter)

    @QtCore.Slot()
    def onButGenTest(self)->None:
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Select Output File", 
                                                     dir=f"{self.mainPath/"Testfile.xml"}", 
                                                     filter="xml Files (*.xml)")
        self.exportFile = Path(path[0])
        logger.info(f"New Export File is set{self.exportFile=}")
        selection:list[QuestionItem] = self.ui.treeWidget.selectedItems()
        self.testDB.appendQuestions(selection, self.exportFile)
        return None

    @QtCore.Slot()
    def onButSpreadsheet(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                     self.tr("Open Spreadsheet"),
                                                     dir = str(self.mainPath),
                                                     filter=self.tr("Spreadsheet(*.xlsx *.ods)"),
                                                     selectedFilter=("*.ods"))
        self.excelPath = Path(file[0]).resolve()
        self.settings.setSpreadsheet(self.excelPath)
        logger.debug(f'Saved Spreadsheet Path: {self.excelPath}\n')
        self.setStatus("[OK] Excel Tabelle wurde eingelesen")
        return None


    @QtCore.Slot()
    def onParseAll (self)->None:
        """Event triggered by the *Tools/Parse all Questions* Event

        It parses all the Questions found in the spreadsheet and then refreshes the list of questions.
        If successful it prints out a list of all exported Questions
        """
        self.ui.buttonTestGen.setEnabled(True)
        self.testDB.parseAll()
        self.setStatus("[OK] Alle Fragen wurden erfolgreich in XML-Dateien umgewandelt")
        # below is former refres method
        logger.info("starting List refresh")
        cats =  self.testDB.categories
        self.ui.treeWidget.clear()
        for cat in cats.values():
            catItem = CategoryItem(self.ui.treeWidget,cat)
            catItem.setFlags(catItem.flags() & ~Qt.ItemIsSelectable)
            for q in cat.questions.values():
                QuestionItem(catItem,q)
        self.setStatus("[OK] Fragen Liste wurde aktualisiert")
        return None

    @QtCore.Slot()
    def previewQ(self)->None:
        item = self.ui.treeWidget.currentItem()
        if isinstance(item, QuestionItem):
            dialog = dialogs.QuestinoPreviewDialog(self, item.getQuestion())
            dialog.show()
        else: logger.info(f"current Item is not a Question, can't preview")

    def setStatus(self, status):
        self.ui.statusbar.clearMessage()
        self.ui.statusbar.showMessage(self.tr(status))

    @QtCore.Slot()
    def onButOpenEqChecker(self):
        logger.debug(f"opening wEquationChecker \n")
        self.uiEqChecker = EqCheckerWindow()
        self.uiEqChecker.excelFile = self.excelPath
        self.uiEqChecker.show()


class EqCheckerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.excelFile = Path()
        self.ui = Ui_EquationChecker()
        self.ui.setupUi(self)
        self.ui.buttonRunCheck.clicked.connect(lambda: self.onButRunCheck(self.ui.catNumber.value(), self.ui.qNumber.value()))

    def onButRunCheck(self, catN:int, qN:int)->None:
        """
        Is Triggered by the ``Run Check now`` Button and runs the Equation Check
        """
        
        self.ui.textResultsOutput.clear()
        bullets, results, firstResult = eqVerif.equationChecker(f'KAT_{catN}',qN, self.excelFile)
        check = False
        self.ui.lineFirstResult.setText(f'{firstResult}')
        for i, calculation in enumerate(results):
            if i == 0 and firstResult !=0:
                check = eqVerif.checkResult(firstResult, calculation)
                self.ui.lineCalculatedRes.setText(f'{calculation}')
            self.ui.textResultsOutput.append(f"Ergebnis {i+1}: \t{calculation}\n\tMit den Werten: \n{bullets[i]}\n")

        if check == True:
            self.ui.lineCheckResult.setText("[OK]")
            logger.info(f"Das erste berechnete Ergebnis stimmt mit dem Wert in 'firstResult' überein\n")
        else:
            self.ui.lineCheckResult.setText("[ERROR]")

