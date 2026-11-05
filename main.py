

import sys
import api
import json

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)

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
        self.status.setText("Loading...")
        QApplication.processEvents()

        try:
            data = api.get_hero_stats(int(text))
            self.output.setPlainText(json.dumps(data, indent = 2))
            self.status.setText("Done.")

        # Passes the exception errors, if any.
        except api.ApiErrorException as e:
            self.output.clear()
            self.status.setText(str(e))

# Actually starts the GUI.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())