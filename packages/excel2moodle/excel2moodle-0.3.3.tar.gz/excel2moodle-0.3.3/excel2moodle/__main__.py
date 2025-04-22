"""Main Function to make the Package executable"""

from PySide6 import QtWidgets, sys

from  excel2moodle.core import dataStructure
from excel2moodle.ui import appUi as ui
from excel2moodle.ui.settings import Settings


def main()->None:
    app = QtWidgets.QApplication(sys.argv)
    settings = Settings()
    database:dataStructure.QuestionDB = dataStructure.QuestionDB(settings)
    window = ui.MainWindow(settings, database)
    database.window = window
    window.show()
    sys.exit(app.exec())

if __name__ =="__main__":
    main()

