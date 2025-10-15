
import datetime
import random

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QLineEdit, QLabel, QMessageBox, QTableWidgetItem
)
from PyQt6.QtGui import QIntValidator

from Features.Customer.model import Logs
from Features.Customer.services import LogsService


random_time = {5, 10, 15, 20, 25, 30}
random_location = {"Bolton", "Matina", "Bunawan", "Maa", "Tibungco"}

class Cart(QWidget):
    ordered = []
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["Category", "Food Variety", "Price", "Size", "Quantity", "Total"])
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.setObjectName("OrderTable")
        self.order_table.setStyleSheet("""
                                #OrderTable QHeaderView::section {
                                    background-color: #add8e6;
                                    color: #000000;
                                    font-weight: bold;
                                    border: 2px solid #eoffff;
                                }
                                #OrderTable {
                                    background-color: #f0ffff;
                                    color: black;
                                }
                                """)

        self.number_field = QLineEdit()
        self.address_field = QLineEdit()
        validator = QIntValidator(0, 999999999)
        self.number_field.setValidator(validator)
        self.number_field.setMaxLength(10)

        self.number_field.setObjectName("NameField")
        self.address_field.setObjectName("AddressField")

        self.number_label = QLabel("Number: 09")
        self.address_label = QLabel("Address: ")

        self.number_label.setObjectName("NumberLabel")
        self.number_label.setStyleSheet("""
                    #NumberLabel {
                        border: 2px solid black;
                        border-radius: 5px;
                        padding: 5px;
                        background-color: #8cb5f0;
                        color: black;
                    }
                """)
        self.address_label.setObjectName("AddressLabel")
        self.address_label.setStyleSheet("""
                    #AddressLabel {
                        border: 2px solid black;
                        border-radius: 5px;
                        padding: 5px;
                        background-color: #8cb5f0;
                        color: black;
                    }
                """)

        self.number_field.setObjectName("Number")
        self.number_field.setStyleSheet("""
            #Number {
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                background-color: #8cb5f0;
                color: black;
            }
            #Number:hover {
                border: 2px solid #0078D7;
                background-color: #f0f8ff;
            }
        """)
        self.address_field.setObjectName("Address")
        self.address_field.setStyleSheet("""
            #Address {
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                background-color: #8cb5f0;
                color: black;
            }
            #Address:hover {
                border: 2px solid #0078D7;
                background-color: #f0f8ff;
            }
        """)


        self.check_out_button = QPushButton("Check-Out")
        self.check_out_button.setObjectName("CheckOutButton")
        self.check_out_button.setStyleSheet("""
            #CheckOutButton {
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                background-color: #8cb5f0;
                color: black;
            }
            #CheckOutButton:hover {
                border: 2px solid #0078D7;
                background-color: #f0f8ff;
            }
        """)

        cart_layout = QVBoxLayout(self)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.number_label, 1)
        layout1.addWidget(self.number_field, 2)
        layout1.addWidget(self.address_label, 1)
        layout1.addWidget(self.address_field, 2)

        fields = QWidget()
        fields.setLayout(layout1)

        cart_layout.addWidget(self.order_table)
        cart_layout.addWidget(fields)
        cart_layout.addWidget(self.check_out_button)

        self.setLayout(cart_layout)
        self.setStyleSheet("background-color: white")

        self.check_out_button.clicked.connect(self.handle_checkout)

        self.populate_table()

    def populate_table(self):
        self.order_table.setRowCount(0)

        for item in self.ordered:
            try:
                category_name, variety, price, size, qty, total = item
            except Exception:
                continue

            row = self.order_table.rowCount()
            self.order_table.insertRow(row)

            self.order_table.setItem(row, 0, QTableWidgetItem(str(category_name)))
            self.order_table.setItem(row, 1, QTableWidgetItem(str(variety)))
            self.order_table.setItem(row, 2, QTableWidgetItem(str(price)))
            self.order_table.setItem(row, 3, QTableWidgetItem(str(size)))
            self.order_table.setItem(row, 4, QTableWidgetItem(str(qty)))
            self.order_table.setItem(row, 5, QTableWidgetItem(str(total)))

    def handle_checkout(self):
        if not self.ordered:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Empty Cart")
            msg.setText("Your cart is empty. Add items before checkout.")
            msg.setStyleSheet("QLabel{ color: black; } QPushButton{ color: black; }")
            msg.exec()
            return

        number = self.number_field.text().strip()
        address = self.address_field.text().strip()

        if not number:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Missing Number")
            msg.setText("Please enter a contact number in the Number field.")
            msg.setStyleSheet("QLabel{ color: black; } QPushButton{ color: black; }")
            msg.exec()
            return

        if not address:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Missing Address")
            msg.setText("Please enter a delivery address.")
            msg.setStyleSheet("QLabel{ color: black; } QPushButton{ color: black; }")
            msg.exec()
            return

        log_service = LogsService()
        saved_count = 0
        errors = []

        for item in self.ordered:
            try:
                category_name, variety, price, size, qty, total = item
            except Exception:
                continue

            log_item = Logs(
                category=str(category_name),
                variety=str(variety),
                price=float(price) if str(price).replace('.', '', 1).isdigit() else 0,
                size=str(size),
                qty=int(qty) if str(qty).isdigit() else 0,
                total=float(total) if str(total).replace('.', '', 1).isdigit() else 0
            )

            try:
                log_service.save_logs(log_item)
                saved_count += 1
            except Exception as e:
                errors.append(str(e))

        if errors:
            QMessageBox.critical(self, "Error", "Some items failed to save to logs:\n" + "\n".join(errors))
            return

        self.ordered.clear()
        self.order_table.setRowCount(0)

        arrival = random.choice(list(random_time))
        location = random.choice(list(random_location))

        self.number_field.clear()
        self.address_field.clear()
        okay = QMessageBox(self)
        okay.setObjectName("OrderPlacedMessage")
        okay.setIcon(QMessageBox.Icon.Information)
        okay.setWindowTitle("Order Placed")
        okay.setText(f"Thank you! Your order was placed.\n"
                     f"Estimated arrival: {arrival} minutes.\n"
                     f"Delivery area: {location}")
        okay.setStyleSheet("""
            #OrderPlacedMessage QLabel {
                color: black;
            }
            #OrderPlacedMessage QPushButton {
                color: black;
            }
        """)
        okay.setStandardButtons(QMessageBox.StandardButton.Ok)
        okay.exec()

    def add_to_cart(self, order_item):
        self.ordered.append(order_item)
        self.populate_table()
