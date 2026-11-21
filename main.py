

import sys
import api
import json

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)
from PySide6.QtCore import (QObject, QRunnable, QThreadPool, Signal)

class WorkerSignals(QObject):
    # This sends the API result.
    finished = Signal(object)
    # This sends the error message.
    failed = Signal(str)

# This class is for background threading the API calls, so the window doesn't feeze when fetching API data.
class ApiWorker(QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    # Will try to run the API worker, emitting sucess or failure signals to be caught by other functions.
    def run(self):
        try:
            result = self.fn(*self.args)
        except Exception as e:
            self.signals.failed.emit(str(e))
        else:
            self.signals.finished.emit(result)


class MainWindow(QWidget):
    # Window is a subclass of QWidget, and runs its own setup first.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deadlock Stats")
        self.resize(600, 500)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Account ID")
        self.button = QPushButton("Search")
        self.status = QLabel("")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.pool = QThreadPool.globalInstance()

        # Horizontal widget arrangement, left to right.
        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(self.button)

        # Vertical arrangement, top to bottom.
        VLayout = QVBoxLayout(self)
        VLayout.addLayout(row)
        VLayout.addWidget(self.status)
        VLayout.addWidget(self.output)

        # Signals emitted by widgets.
        self.button.clicked.connect(self.search)
        self.input.returnPressed.connect(self.search)

    def search(self):
        text = self.input.text().strip()

        # Ensures that the user enters a number. If it isn't of proper length as it will print bad account ID anyways.
        if not text.isdigit():
            self.status.setText("Enter a numeric account ID.")
            return

        # Waits for the widgets to handle pending events to show loading. To be replaced later when threading is implemented.
        self.button.setEnabled(False)
        self.status.setText("Loading...")
        worker = ApiWorker(api.get_hero_stats, int(text))
        worker.signals.finished.connect(self.on_result)
        worker.signals.failed.connect(self.on_error)
        self.pool.start(worker)

    # Upon the thread successfully completing the task.
    def on_result(self, data):
        self.output.setPlainText(json.dumps(data, indent = 2))
        self.status.setText("Done.")
        self.button.setEnabled(True)

    # When the thread doesn't work as intended.
    def on_error(self, message):
        self.output.clear()
        self.status.setText(message)
        self.button.setEnabled(True)

# Actually starts the GUI.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())