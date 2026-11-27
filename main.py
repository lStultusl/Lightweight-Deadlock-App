

import sys
import api
import json

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)
from PySide6.QtCore import (QObject, QRunnable, QThreadPool, Signal)
from datetime import datetime, timezone
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

# Columns of fetched states for searched player
COLUMNS = ["Hero ID", "Matches", "Win %", "KDA", "Dmg/min", "Last played"]

# Dictionary of ID : Hero Name
# To be updated (maybe swap to API mapping calls) as new heroes are added
HERO_MAPPING = {
    6 : "Abrams",
    15 : "Bebop",
    11 : "Dynamo",
    17 : "Grey Talon",
    13 : "Haze",
    1 : "Infernus",
    20 : "Ivy",
    12 : "Kelvin",
    4 : "Lady Geist",
    31 : "Lash",
    8 : "McGinnis",
    18 : "Mo & Krill",
    10 : "Paradox",
    50 : "Pocket",
    2 : "Seven",
    3 : "Vindicta",
    25 : "Warden",
    7 : "Wraith",
    27 : "Yamato",
    35 : "Viscous",
    19 : "Shiv",
    52 : "Mirage",
    16 : "Calico",
    14 : "Holliday",
    60 : "Sinclair",
    58 : "Vyper",
    63 : "Mina",
    72 : "Billy",
    69 : "The Doorman",
    67 : "Paige",
    64 : "Drifter",
    66 : "Victor",
    79 : "Rem",
    76 : "Graves",
    80 : "Silver",
    65 : "Venator",
    81 : "Celeste",
    77 : "Apollo",
    84 : "Rat King",
    88 : "Baba",
    85 : "Solomon",
    78 : "Deadman Danny",
    86 : "Violet",
    87 : "Nurse Harrow"
}

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
        self.resize(800, 650)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Account ID")
        self.button = QPushButton("Search")
        self.status = QLabel("")
        self.table = QTableWidget(0, len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #self.output.setReadOnly(True)
        self.pool = QThreadPool.globalInstance()

        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(self.button)

        VLayout = QVBoxLayout(self)
        VLayout.addLayout(row)
        VLayout.addWidget(self.status)
        #VLayout.addWidget(self.output)
        VLayout.addWidget(self.table)

        self.button.clicked.connect(self.search)
        self.input.returnPressed.connect(self.search)

    def show_hero_stats(self, heroes):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(heroes))
        for row, h in enumerate(heroes):
            games = h["matches_played"]

            if games:
                win_rate = 100 * h["wins"] / games
            else:
                win_rate = 0.0
            
            kda = (h["kills"] + h["assists"]) / max(h["deaths"], 1)
            last = datetime.fromtimestamp(h["last_played"], tz=timezone.utc).strftime("%Y-%m-%d")

            hero_name = HERO_MAPPING.get(h["hero_id"], f"Hero {h['hero_id']}")

            values = [hero_name, games, round(win_rate, 1), round(kda, 2), round(h["damage_per_min"]), last]

            for col, v in enumerate(values):
                item = QTableWidgetItem()
                # Enables numbers to sort numerically.
                item.setData(Qt.ItemDataRole.DisplayRole, v)
                self.table.setItem(row, col, item)

        # Sorting after all of the data has been added will allow for data based on win-count to be sorted first.
        self.table.setSortingEnabled(True)
        # Most played character will be shown first.
        self.table.sortItems(1, Qt.SortOrder.DescendingOrder)

    def search(self):
        text = self.input.text().strip()

        if not text.isdigit():
            self.status.setText("Enter a numeric account ID.")
            return

        # Waits for the widgets to handle pending events to show loading while the thread works.
        self.button.setEnabled(False)
        self.status.setText("Loading...")
        worker = ApiWorker(api.get_hero_stats, int(text))
        worker.signals.finished.connect(self.on_result)
        worker.signals.failed.connect(self.on_error)
        self.pool.start(worker)

    # Thread success
    def on_result(self, data):
        self.show_hero_stats(data)
        self.status.setText(f"{len(data)} heroes")
        self.button.setEnabled(True)

    # Thread failure
    def on_error(self, message):
        self.table.setRowCount(0)
        self.status.setText(message)
        self.button.setEnabled(True)

# Actually starts the GUI window to run for the user.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())