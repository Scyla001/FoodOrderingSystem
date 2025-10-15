#from Features.Customer.model import food_type, category, logs
from Features.Customer.services import FoodService, LogsService, ReadCategory

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QTabWidget,
    QScrollArea,
    QGridLayout,
    QLabel,
    QStackedLayout,
    QComboBox,
    QTableWidget,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QDialog
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap, QIntValidator, QIcon

class Home(QWidget):
    def __init__(self):
        super().__init__()
        home_layout = QHBoxLayout()

        label = QLabel("This is home")
        home_layout.addWidget(label)

        self.setLayout(home_layout)

