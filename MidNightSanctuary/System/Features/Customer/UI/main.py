from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
    QStackedLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

from Features.Customer.services import CategoryService
from Features.Customer.UI.home import Home
from Features.Customer.UI.cart import Cart
from Features.Customer.UI.order import Order


class Customer(QWidget):
    switch_admin = pyqtSignal()

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        bg_label = QLabel()
        logo = QPixmap("C:/Users/charl/OneDrive/Desktop/Food-Pics/M.png")
        logo_resized = logo.scaled(240, 60)
        bg_label.setPixmap(logo_resized)
        logo_layout.addWidget(bg_label)

        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #afeeee;")
        top_layout = QHBoxLayout(top_bar)

        home_button = QPushButton("HOME")
        order_button = QPushButton("ORDER")
        cart_button = QPushButton("CHECK CART")
        login_button = QPushButton("LOGIN")

        for btn in (home_button, order_button, cart_button, login_button):
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 5px;
                    background-color: transparent; 
                    color: black; 
                    font-size: 20px; 
                    font-weight: 800; 
                    font-family: Consolas;
                }
                QPushButton:hover {
                    background-color: #93c2a6;
                    text-decoration: overline underline;
                }
                QPushButton:focus {
                    text-decoration: overline underline;
                }
            """)

        filler = QWidget()
        top_layout.addWidget(logo_widget, 2)
        top_layout.addWidget(filler, 1)
        top_layout.addWidget(home_button, 1)
        top_layout.addWidget(order_button, 1)
        top_layout.addWidget(cart_button, 1)
        top_layout.addWidget(login_button, 1)

        stack = QStackedLayout()
        home_panel = Home()
        order_panel = Order()
        cart_panel = Cart(self)
        login_panel = self.build_login_panel()

        stack.addWidget(home_panel)
        stack.addWidget(order_panel)
        stack.addWidget(cart_panel)
        stack.addWidget(login_panel)

        center_panel = QWidget()
        center_panel.setObjectName("CenterPanel")
        center_panel.setLayout(stack)
        center_panel.setStyleSheet("#CenterPanel { background-color: #f5fffa; }")

        main_layout.addWidget(top_bar)
        main_layout.addWidget(center_panel)
        self.setLayout(main_layout)

        home_button.clicked.connect(lambda: stack.setCurrentWidget(home_panel))
        cart_button.clicked.connect(lambda: stack.setCurrentWidget(cart_panel))
        login_button.clicked.connect(lambda: stack.setCurrentWidget(login_panel))

        def setup_order_panel():
            svc = CategoryService()
            categories = svc.get_data()
            if not categories:
                QMessageBox.information(self, "Notice", "No categories found in database.")
            stack.setCurrentWidget(order_panel)

        order_panel.add_order.connect(cart_panel.add_to_cart)

        order_button.clicked.connect(setup_order_panel)

    def build_login_panel(self):
        panel = QWidget()
        panel_layout = QHBoxLayout(panel)

        login_panel = QWidget()
        login_layout = QVBoxLayout(login_panel)

        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.EchoMode.Password)

        user_label = QLabel("Username:")
        pass_label = QLabel("Password:")

        username.setPlaceholderText("Enter Username")
        password.setPlaceholderText("Enter Password")

        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: white; 
                color: black; 
                font-size: 20px; 
                font-weight: 800; 
                font-family: Consolas;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                text-decoration: underline;
            }
        """)

        def check_login():
            if username.text() == "admin" and password.text() == "12345":
                username.clear()
                password.clear()
                self.switch_admin.emit()
            else:
                QMessageBox.warning(self, "Error", "Wrong Username or Password!")

        login_button.clicked.connect(check_login)

        login_layout.addWidget(user_label)
        login_layout.addWidget(username)
        login_layout.addWidget(pass_label)
        login_layout.addWidget(password)
        login_layout.addWidget(login_button)

        login_panel.setFixedSize(300, 300)
        login_panel.setStyleSheet("background-color: #4682b4;")
        panel_layout.addWidget(login_panel, alignment=Qt.AlignmentFlag.AlignCenter)

        return panel
