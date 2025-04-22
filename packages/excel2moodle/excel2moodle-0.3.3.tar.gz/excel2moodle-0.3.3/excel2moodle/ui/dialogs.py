"""This Module hosts the various Dialog Classes, that can be shown from main Window
"""
from PySide6 import QtWidgets, QtGui
import lxml.etree as ET
from PySide6.QtSvgWidgets import QGraphicsSvgItem

from excel2moodle.core.question import Question
from excel2moodle.ui.variantDialog import Ui_Dialog
from excel2moodle.ui.questionPreviewDialog import Ui_QuestionPrevDialog


class QuestionVariantDialog(QtWidgets.QDialog):
    def __init__(self,  parent, question:Question):
        super().__init__(parent)
        self.setWindowTitle("Question Variant Dialog")
        self.maxVal = question.variants
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.spinBox.setRange(1, self.maxVal)
        self.ui.catLabel.setText(f"{question.katName}")
        self.ui.qLabel.setText(f"{question.name}")
        self.ui.idLabel.setText(f"{question.id}")

    @property
    def variant(self):
        return self.ui.spinBox.value()

    @property
    def categoryWide(self):
        return self.ui.checkBox.isChecked()


class QuestinoPreviewDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, question:Question) -> None:
        super().__init__(parent)
        self.question = question
        self.ui = Ui_QuestionPrevDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Question - {question.id} - Preview")
        self.setupQuestion()

    def setupQuestion(self)->None:
        self.ui.qNameLine.setText(self.question.name)
        self.ui.qTypeLine.setText(self.question.qtype)
        self.setText()
        self.setAnswers()
        self.setPicture()

    def setPicture(self)->None:
        if hasattr(self.question, "picture") and self.question.picture.ready:
            self.picScene = QtWidgets.QGraphicsScene(self)
            self.ui.graphicsView.setScene(self.picScene)
            path = self.question.picture.path
            if path.suffix =='.svg':
                picItem = QGraphicsSvgItem(str(self.question.picture.path))
            else:
                pic = QtGui.QPixmap(self.question.picture.path)
                aspRat = pic.height() // pic.width()
                width = 400
                scaleHeight = aspRat * width
                picItem = QtWidgets.QGraphicsPixmapItem(pic.scaled(width, scaleHeight, QtGui.Qt.AspectRatioMode.KeepAspectRatio))
            self.picScene.addItem(picItem)
        else:
            self.ui.graphicsView.setFixedHeight(1)

    def setText(self)->None:
        t = []
        for text in self.question.qtextParagraphs:
            t.append(ET.tostring(text, encoding='unicode'))
        t.append(ET.tostring(self.question.bulletList, encoding='unicode'))
        self.ui.questionText.setText("\n".join(t))

    def setAnswers(self)->None:
        if self.question.qtype == "NFM":
            for i,ans in enumerate(self.question.answerVariants):
                a = ans.find('text').text
                text = QtWidgets.QLineEdit(a, self )
                self.ui.answersFormLayout.addRow(f'Answer {i+1}', text)


