from Features.Admin.services import FoodService, CategoryService
from Features.Admin.UI.category import CategoryUI
from Features.Admin.UI.product import Products
from Features.Admin.UI.dashboard import Dashboard

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



class Admin(QWidget):
    switch_customer = pyqtSignal()

    def __init__(self):
        super().__init__()

        style = """
                QPushButton {
                    min-height: 40px;
                    padding-top: 15px;
                    padding-bottom: 15px;
                    border: none; 
                    background-color: transparent; 
                    color: white; 
                    font-size: 15px; 
                    font-weight: 500; 
                    font-family: Consolas;
                }

                QPushButton:hover {
                    background-color: lightgray;
                    color: black;
                    text-decoration: underline;
                }
                """

        main_layout = QHBoxLayout()

        left_navigation = QWidget()
        left_navigation_layout = QVBoxLayout()
        left_navigation.setLayout(left_navigation_layout)
        left_navigation.setStyleSheet("background-color: #71afdb")

        dashboard_button = QPushButton("Dashboard")
        mng_category_btn = QPushButton("Manage Category")
        mng_products_btn = QPushButton("Manage Products")
        logout_button = QPushButton("Logout")

        dashboard_button.setStyleSheet(style)
        mng_products_btn.setStyleSheet(style)
        mng_category_btn.setStyleSheet(style)
        logout_button.setStyleSheet(style)

        def confirm_logout():
            msg = QMessageBox(self)
            msg.setWindowTitle("Confirmation")
            msg.setText("Are you sure you want to logout?")
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            result = msg.exec()

            if result == QMessageBox.StandardButton.Ok:
                self.switch_customer.emit()


        left_navigation_layout.addWidget(dashboard_button, 1)
        left_navigation_layout.addWidget(mng_category_btn, 1)
        left_navigation_layout.addWidget(mng_products_btn, 1)
        left_navigation_layout.addWidget(QWidget(), 6)
        left_navigation_layout.addWidget(logout_button, 1)

        def populate_product_table():
            self.food_service = FoodService()
            stack.setCurrentWidget(prod_panel)

        def populate_category_table():
            self.category_service = CategoryService()
            stack.setCurrentWidget(category_panel)

        stack = QStackedLayout()

        center_panel = QWidget()
        center_panel.setLayout(stack)

        dashboard_panel = Dashboard()
        prod_panel = Products()
        category_panel = CategoryUI()

        stack.addWidget(dashboard_panel)
        stack.addWidget(prod_panel)
        stack.addWidget(category_panel)

        dashboard_button.clicked.connect(lambda: stack.setCurrentWidget(dashboard_panel))
        mng_products_btn.clicked.connect(lambda: populate_product_table())
        logout_button.clicked.connect(lambda: confirm_logout())
        mng_category_btn.clicked.connect(lambda: populate_category_table())

        main_layout.addWidget(left_navigation, 2)
        main_layout.addWidget(center_panel, 8)
        self.setLayout(main_layout)
