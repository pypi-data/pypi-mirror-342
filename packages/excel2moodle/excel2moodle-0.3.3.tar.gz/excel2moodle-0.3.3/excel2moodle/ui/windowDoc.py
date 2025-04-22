import os
import sys
from PySide6 import QtWidgets, QtWebEngineWidgets, QtCore
from excel2moodle import dirDocumentation

class DocumentationWindow(QtWidgets.QMainWindow):
    def __init__(self, documentationDirectory, parent=None):
        super().__init__(parent)

        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Load the HTML documentation

        index_file = os.path.join(documentationDirectory, "index.html")
        url = QtCore.QUrl.fromLocalFile(index_file)
        self.web_view.setUrl(url)

        # Set up navigation events
        self.web_view.page().linkHovered.connect(self.link_hovered)
        self.web_view.page().loadFinished.connect(self.load_finished)

    def link_hovered(self, url):
        print(f"Link hovered: {url}")

    def load_finished(self, ok):
        print(f"Load finished: {ok}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = DocumentationWindow(dirDocumentation)
    window.show()

    sys.exit(app.exec())
