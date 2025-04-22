# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QDoubleSpinBox, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QTextEdit, QToolBar,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MoodleTestGenerator(object):
    def setupUi(self, MoodleTestGenerator):
        if not MoodleTestGenerator.objectName():
            MoodleTestGenerator.setObjectName(u"MoodleTestGenerator")
        MoodleTestGenerator.resize(936, 1198)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogQuestion))
        MoodleTestGenerator.setWindowIcon(icon)
        self.actionInput_Spreadsheet = QAction(MoodleTestGenerator)
        self.actionInput_Spreadsheet.setObjectName(u"actionInput_Spreadsheet")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.actionInput_Spreadsheet.setIcon(icon1)
        self.actionOutput_Folder = QAction(MoodleTestGenerator)
        self.actionOutput_Folder.setObjectName(u"actionOutput_Folder")
        self.actionEquationChecker = QAction(MoodleTestGenerator)
        self.actionEquationChecker.setObjectName(u"actionEquationChecker")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ToolsCheckSpelling))
        self.actionEquationChecker.setIcon(icon2)
        self.actionParseAll = QAction(MoodleTestGenerator)
        self.actionParseAll.setObjectName(u"actionParseAll")
        icon3 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.actionParseAll.setIcon(icon3)
        self.actionPreviewQ = QAction(MoodleTestGenerator)
        self.actionPreviewQ.setObjectName(u"actionPreviewQ")
        icon4 = QIcon(QIcon.fromTheme(u"document-print-preview"))
        self.actionPreviewQ.setIcon(icon4)
        self.actionAbout = QAction(MoodleTestGenerator)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon(QIcon.fromTheme(u"help-about"))
        self.actionAbout.setIcon(icon5)
        self.actionDocumentation = QAction(MoodleTestGenerator)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionDocumentation.setIcon(icon5)
        self.actionSetting = QAction(MoodleTestGenerator)
        self.actionSetting.setObjectName(u"actionSetting")
        icon6 = QIcon(QIcon.fromTheme(u"preferences-system"))
        self.actionSetting.setIcon(icon6)
        self.mainWidget = QWidget(MoodleTestGenerator)
        self.mainWidget.setObjectName(u"mainWidget")
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 14)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(3, -1, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxQuestionListSelectAll = QCheckBox(self.mainWidget)
        self.checkBoxQuestionListSelectAll.setObjectName(u"checkBoxQuestionListSelectAll")

        self.horizontalLayout.addWidget(self.checkBoxQuestionListSelectAll)

        self.horizontalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.line_4 = QFrame(self.mainWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(self.mainWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.treeWidget = QTreeWidget(self.mainWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignLeading|Qt.AlignVCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setBaseSize(QSize(0, 60))
        self.treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setMinimumSectionSize(8)

        self.verticalLayout_4.addWidget(self.treeWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.mainWidget)
        self.label_5.setObjectName(u"label_5")
        font1 = QFont()
        font1.setPointSize(15)
        self.label_5.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_5)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(5, 5, 5, 5)
        self.label_6 = QLabel(self.mainWidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.pointCounter = QDoubleSpinBox(self.mainWidget)
        self.pointCounter.setObjectName(u"pointCounter")
        self.pointCounter.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pointCounter.sizePolicy().hasHeightForWidth())
        self.pointCounter.setSizePolicy(sizePolicy)
        self.pointCounter.setBaseSize(QSize(190, 0))
        font2 = QFont()
        font2.setPointSize(13)
        self.pointCounter.setFont(font2)
        self.pointCounter.setAutoFillBackground(False)
        self.pointCounter.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.pointCounter.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.pointCounter.setDecimals(1)
        self.pointCounter.setMaximum(999.899999999999977)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pointCounter)

        self.label_7 = QLabel(self.mainWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.questionCounter = QDoubleSpinBox(self.mainWidget)
        self.questionCounter.setObjectName(u"questionCounter")
        self.questionCounter.setFont(font2)
        self.questionCounter.setDecimals(0)
        self.questionCounter.setMaximum(300.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.questionCounter)

        self.label_8 = QLabel(self.mainWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.categoriesCounter = QSpinBox(self.mainWidget)
        self.categoriesCounter.setObjectName(u"categoriesCounter")
        self.categoriesCounter.setFont(font2)
        self.categoriesCounter.setMaximum(999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.categoriesCounter)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.line_3 = QFrame(self.mainWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_2 = QLabel(self.mainWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout_2.addWidget(self.label_2)

        self.buttonSpreadSheet = QPushButton(self.mainWidget)
        self.buttonSpreadSheet.setObjectName(u"buttonSpreadSheet")
#if QT_CONFIG(tooltip)
        self.buttonSpreadSheet.setToolTip(u"<html><head/><body><p>Select the Spreadsheet File with all the Questions inside</p></body></html>")
#endif // QT_CONFIG(tooltip)

        self.verticalLayout_2.addWidget(self.buttonSpreadSheet)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.horizontalSpacer_2)

        self.line_2 = QFrame(self.mainWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.label_3 = QLabel(self.mainWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_9 = QLabel(self.mainWidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_9)

        self.checkBoxIncludeCategories = QCheckBox(self.mainWidget)
        self.checkBoxIncludeCategories.setObjectName(u"checkBoxIncludeCategories")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.checkBoxIncludeCategories)

        self.spinBoxDefaultQVariant = QSpinBox(self.mainWidget)
        self.spinBoxDefaultQVariant.setObjectName(u"spinBoxDefaultQVariant")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.spinBoxDefaultQVariant)

        self.checkBoxUseDefQVariant = QCheckBox(self.mainWidget)
        self.checkBoxUseDefQVariant.setObjectName(u"checkBoxUseDefQVariant")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.checkBoxUseDefQVariant)

        self.label_10 = QLabel(self.mainWidget)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_10)

        self.label_11 = QLabel(self.mainWidget)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_11)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.buttonTestGen = QPushButton(self.mainWidget)
        self.buttonTestGen.setObjectName(u"buttonTestGen")
        self.buttonTestGen.setEnabled(False)
#if QT_CONFIG(tooltip)
        self.buttonTestGen.setToolTip(u"<html><head/><body><p>exporst all selected questions to the test File</p></body></html>")
#endif // QT_CONFIG(tooltip)

        self.verticalLayout_2.addWidget(self.buttonTestGen)

        self.line = QFrame(self.mainWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(self.mainWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.loggerWindow = QTextEdit(self.mainWidget)
        self.loggerWindow.setObjectName(u"loggerWindow")
        self.loggerWindow.setMinimumSize(QSize(0, 0))
        self.loggerWindow.setMaximumSize(QSize(16777215, 373))
        self.loggerWindow.setBaseSize(QSize(0, 30))
        self.loggerWindow.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout.addWidget(self.loggerWindow)

        MoodleTestGenerator.setCentralWidget(self.mainWidget)
        self.menubar = QMenuBar(MoodleTestGenerator)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 936, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MoodleTestGenerator.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MoodleTestGenerator)
        self.statusbar.setObjectName(u"statusbar")
        MoodleTestGenerator.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MoodleTestGenerator)
        self.toolBar.setObjectName(u"toolBar")
        MoodleTestGenerator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.toolBar_3 = QToolBar(MoodleTestGenerator)
        self.toolBar_3.setObjectName(u"toolBar_3")
        MoodleTestGenerator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_3)
        self.toolBar_2 = QToolBar(MoodleTestGenerator)
        self.toolBar_2.setObjectName(u"toolBar_2")
        MoodleTestGenerator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_2)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionInput_Spreadsheet)
        self.menuTools.addAction(self.actionEquationChecker)
        self.menuTools.addAction(self.actionParseAll)
        self.menuTools.addAction(self.actionPreviewQ)
        self.menuTools.addAction(self.actionSetting)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionDocumentation)
        self.toolBar.addAction(self.actionInput_Spreadsheet)
        self.toolBar.addAction(self.actionParseAll)
        self.toolBar.addSeparator()
        self.toolBar_3.addAction(self.actionEquationChecker)
        self.toolBar_3.addAction(self.actionPreviewQ)
        self.toolBar_2.addAction(self.actionDocumentation)
        self.toolBar_2.addAction(self.actionSetting)

        self.retranslateUi(MoodleTestGenerator)

        QMetaObject.connectSlotsByName(MoodleTestGenerator)
    # setupUi

    def retranslateUi(self, MoodleTestGenerator):
        MoodleTestGenerator.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"excel 2 moodle", None))
        self.actionInput_Spreadsheet.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Input Spreadsheet", None))
#if QT_CONFIG(shortcut)
        self.actionInput_Spreadsheet.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionOutput_Folder.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Output Folder", None))
        self.actionEquationChecker.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Equation Checker", None))
        self.actionParseAll.setText(QCoreApplication.translate("MoodleTestGenerator", u"&Parse all Questions", None))
#if QT_CONFIG(tooltip)
        self.actionParseAll.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"Parses all questions inside the spreadsheet", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionParseAll.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionPreviewQ.setText(QCoreApplication.translate("MoodleTestGenerator", u"Preview Question", None))
#if QT_CONFIG(shortcut)
        self.actionPreviewQ.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MoodleTestGenerator", u"About", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MoodleTestGenerator", u"Documentation", None))
#if QT_CONFIG(shortcut)
        self.actionDocumentation.setShortcut(QCoreApplication.translate("MoodleTestGenerator", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionSetting.setText(QCoreApplication.translate("MoodleTestGenerator", u"Settings", None))
        self.checkBoxQuestionListSelectAll.setText(QCoreApplication.translate("MoodleTestGenerator", u"Select all", None))
        self.label.setText(QCoreApplication.translate("MoodleTestGenerator", u"Question List", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MoodleTestGenerator", u"Variant", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MoodleTestGenerator", u"Points", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MoodleTestGenerator", u"Description", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MoodleTestGenerator", u"Question ID", None));
        self.label_5.setText(QCoreApplication.translate("MoodleTestGenerator", u"Selected:", None))
        self.label_6.setText(QCoreApplication.translate("MoodleTestGenerator", u"Points", None))
        self.pointCounter.setPrefix("")
        self.label_7.setText(QCoreApplication.translate("MoodleTestGenerator", u"Questions", None))
        self.questionCounter.setPrefix("")
        self.label_8.setText(QCoreApplication.translate("MoodleTestGenerator", u"Categories", None))
        self.categoriesCounter.setSuffix("")
        self.categoriesCounter.setPrefix("")
        self.label_2.setText(QCoreApplication.translate("MoodleTestGenerator", u"Input", None))
        self.buttonSpreadSheet.setText(QCoreApplication.translate("MoodleTestGenerator", u"Select spreadsheet", None))
        self.label_3.setText(QCoreApplication.translate("MoodleTestGenerator", u"Output", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"If enabled, all questions will be categorized, when importing into moodle. Otherwise they will all be imported into one category", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("MoodleTestGenerator", u"Include Questions in Categories", None))
        self.checkBoxIncludeCategories.setText("")
        self.checkBoxUseDefQVariant.setText("")
        self.label_10.setText(QCoreApplication.translate("MoodleTestGenerator", u"Default Question Variant", None))
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("MoodleTestGenerator", u"If enabled it will always use the question variant that is set below. If not, it will ask everytime, which question Variant should be used", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("MoodleTestGenerator", u"Use default question Variant", None))
        self.buttonTestGen.setText(QCoreApplication.translate("MoodleTestGenerator", u"export selected Questions to examfile", None))
        self.label_4.setText(QCoreApplication.translate("MoodleTestGenerator", u"Logger", None))
        self.menuFile.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MoodleTestGenerator", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"toolBar", None))
        self.toolBar_3.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"toolBar_3", None))
        self.toolBar_2.setWindowTitle(QCoreApplication.translate("MoodleTestGenerator", u"toolBar_2", None))
    # retranslateUi

