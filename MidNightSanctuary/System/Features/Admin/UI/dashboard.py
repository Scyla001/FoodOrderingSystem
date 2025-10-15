from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Features.Admin.services import FoodService, LogsService, CategoryService

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
    QDialog,
    QTextEdit,
    QFileDialog,
    QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import pyqtSignal, Qt

dashboard_list = [[], []]

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        dash_layout_bar = QHBoxLayout()
        dash_layout_pie = QHBoxLayout()
        dash_layout = QVBoxLayout(self)
        dash_layout.addLayout(dash_layout_bar)
        dash_layout.addLayout(dash_layout_pie)

        bar_label = QLabel("This shows the most sold product")
        pie_label = QLabel("This shows the most product we get our income")
        bar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bar_canvas = FigureCanvas(Figure())
        pie_canvas = FigureCanvas(Figure())

        dash_layout_bar.addWidget(bar_canvas, 2)
        dash_layout_bar.addWidget(bar_label, 1)
        dash_layout_pie.addWidget(pie_label, 1)
        dash_layout_pie.addWidget(pie_canvas, 2)

        service = LogsService()
        plot_bar(bar_canvas, dashboard_list)
        plot_pie(pie_canvas, dashboard_list)


def plot_bar(canvas, data):
    canvas.figure.clf()
    ax = canvas.figure.add_subplot(111)
    if not data:
        canvas.draw()
        return
    categories = [item.name for item in data[0]]
    values = [item.sold for item in data[1]]
    ax.bar(categories, values, color="cornflowerblue")
    ax.set_title("Drink Sales")
    ax.set_xlabel("Drink Type")
    ax.set_ylabel("Units Sold")
    canvas.draw()


def plot_pie(canvas, data):
    canvas.figure.clf()
    ax = canvas.figure.add_subplot()
    if not data:
        canvas.draw()
        return
    labels = [item.name for item in data[0]]
    values = [item.sold for item in data[1]]
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Drink Sales Distribution")
    canvas.draw()

def load_dashboard():
    logss = LogsService()
    records = logss.get_logs()

    for record in records:
        if record.category in dashboard_list[1]:
            idx = dashboard_list[1].index(record.category)
            value = dashboard_list[0][idx]
            dashboard_list[0].pop(idx)
            dashboard_list[1].pop(idx)
            dashboard_list[0].append(record.qty + value)
            dashboard_list[1].append(record.category)
        else:
            dashboard_list[0].append(record.qty)
            dashboard_list[1].append(record.category)