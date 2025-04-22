from PySide6.QtCore import QSettings, QTimer, Signal
from pathlib import Path

class Settings(QSettings):
    shPathChanged = Signal(Path)
    def __init__(self):
        super().__init__("jbosse3", "excel2moodle")
        if self.contains("core/spreadsheet"):
            self.sheet = self.value("core/spreadsheet")
            try:
                self.sheet.resolve(strict=True)
                if self.sheet.is_file():
                    QTimer.singleShot(0,self._emitSpreadsheetChanged)
            except Exception:
                return None

    def _emitSpreadsheetChanged(self)->None:
        self.shPathChanged.emit(self.sheet)
        print("Emitting Spreadsheet Changed Event")


    def get(self, value, default=None):
        return self.value(value, default)


    def set(self, setting, value):
        self.setValue(setting, value)

    def setSpreadsheet(self, sheet:Path)->None:
        if isinstance(sheet, Path):
            self.sheet = sheet.resolve(strict=True)
            self.setValue("core/spreadsheet", self.sheet)
            self.shPathChanged.emit(sheet)
            return None

