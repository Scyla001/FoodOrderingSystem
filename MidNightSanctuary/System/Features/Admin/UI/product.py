from PyQt6.QtGui import QPixmap, QIntValidator
from Features.Admin.model import Food, Logs, Category
from Features.Admin.services import FoodService, ReadLogs, CategoryService
from Features.Admin.services import Util

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QTabWidget, QScrollArea, QGridLayout, QLabel,
    QStackedLayout, QComboBox, QTableWidget, QLineEdit,
    QMessageBox, QSpinBox, QDialog, QTextEdit,
    QFileDialog, QTableWidgetItem, QHeaderView
)

class Products(QWidget):
    def __init__(self):
        super().__init__()
        prod_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        prod_layout.addLayout(menu_layout)
        self.prod_table = QTableWidget()
        prod_layout.addWidget(self.prod_table)

        add_btn = QPushButton("Add Product")
        edit_btn = QPushButton("Edit Product")
        delete_btn = QPushButton("Delete Product")
        search_btn = QPushButton("Search")
        search_field = QLineEdit()
        search_field.setPlaceholderText("Enter keyword")

        menu_layout.addWidget(add_btn, 1)
        menu_layout.addWidget(edit_btn, 1)
        menu_layout.addWidget(delete_btn, 1)
        menu_layout.addWidget(search_btn, 1)
        menu_layout.addWidget(search_field, 2)

        self.prod_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.prod_table.setColumnCount(6)
        self.prod_table.setHorizontalHeaderLabels(["ID", "Type", "Category", "Variety", "Sizes", "Price"])
        header = self.prod_table.horizontalHeader()
        for i in range(2, 6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.prod_table.setColumnHidden(0, True)
        self.prod_table.setColumnHidden(1, True)
        self.prod_table.setObjectName("ProductTable")
        self.prod_table.setStyleSheet("""
                #ProductTable QHeaderView::section {
                    background-color: #36c4f4;
                    color: #ffffff;
                    font-weight: bold;
                    border: 2px solid #4c98b9;
                    font-family: Consolas;
                }
                #ProductTable {
                    background-color: #71afdb;
                    color: white
                }
            """)

        def add_product_dialog():
            dialog = QDialog()
            dialog.setWindowTitle("Add Product")
            layout = QVBoxLayout()
            dialog.setLayout(layout)

            select_cate = QLabel("Select Product Category")
            layout.addWidget(select_cate)

            service = CategoryService()
            items = service.get_data()

            single_btn = QPushButton("Single-Size Product")
            layout.addWidget(single_btn)

            def single_product_dialog():
                spd = QDialog()
                spd.setWindowTitle("Add Single-Size Product")
                spd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                single_titles = [item.title for item in items if item.type == "Single-size"]
                category_combobox.addItems(single_titles)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(variety_label)
                left_layout.addWidget(variety_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(spd.close)

                right_layout = QVBoxLayout()
                variety_price_table = QTableWidget()
                variety_price_table.setColumnCount(2)
                variety_price_table.setHorizontalHeaderLabels(["Variety", "Price"])
                variety_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(variety_price_table)
                right_layout.addWidget(delete_varpri)

                def delete_varpri_handler():
                    row = variety_price_table.currentRow()
                    if row >= 0:
                        variety_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table():
                    variety = variety_field.text().strip()
                    price = price_field.text().strip()
                    if not variety or not price:
                        QMessageBox.warning(spd, "Empty Fields", "Please fill in both Variety and Price fields.")
                        return
                    row_count = variety_price_table.rowCount()
                    variety_price_table.insertRow(row_count)
                    variety_price_table.setItem(row_count, 0, QTableWidgetItem(variety))
                    variety_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    variety_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table)

                def save_and_load():
                    variety_list = []
                    price_list = []
                    row_count = variety_price_table.rowCount()
                    for row in range(row_count):
                        variety = variety_price_table.item(row, 0)
                        price = variety_price_table.item(row, 1)
                        if variety and price:
                            variety_list.append(variety.text().title())
                            price_list.append(price.text())
                    save = Food()
                    save.type = "Single-size"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.insert_data(save)
                    load_products(fs, self.prod_table)
                    spd.close()

                save_button.clicked.connect(save_and_load)
                spd_layout.addLayout(left_layout)
                spd_layout.addLayout(right_layout)
                spd.setLayout(spd_layout)
                spd.exec()

            single_btn.clicked.connect(single_product_dialog)

            multi_btn = QPushButton("Multi-Size Product")
            layout.addWidget(multi_btn)

            def multi_product_dialog():
                mpd = QDialog()
                mpd.setWindowTitle("Add Multi-Size Product")
                mpd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                single_titles = [item.title for item in items if item.type == "Multi-size"]
                category_combobox.addItems(single_titles)
                size_label = QLabel("Size:")
                size_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(size_label)
                left_layout.addWidget(size_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(mpd.close)

                center_layout = QVBoxLayout()
                variety_table = QTableWidget()
                variety_table.setColumnCount(1)
                variety_table.setHorizontalHeaderLabels(["Variety"])
                variety_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                add_variety = QPushButton("Add Variety")
                delete_variety = QPushButton("Delete Variety")
                center_layout.addWidget(variety_table)
                center_layout.addWidget(variety_label)
                center_layout.addWidget(variety_field)
                center_layout.addWidget(add_variety)
                center_layout.addWidget(delete_variety)

                def add_variety_to_table():
                    text = variety_field.text().strip()
                    if not text:
                        QMessageBox.warning(mpd, "Empty Field", "Please enter a variety name.")
                        return
                    row = variety_table.rowCount()
                    variety_table.insertRow(row)
                    variety_table.setItem(row, 0, QTableWidgetItem(text))
                    variety_field.clear()

                add_variety.clicked.connect(add_variety_to_table)

                def delete_variety_handler():
                    row = variety_table.currentRow()
                    if row >= 0:
                        variety_table.removeRow(row)

                delete_variety.clicked.connect(delete_variety_handler)

                right_layout = QVBoxLayout()
                size_price_table = QTableWidget()
                size_price_table.setColumnCount(2)
                size_price_table.setHorizontalHeaderLabels(["Size", "Price"])
                size_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(size_price_table)
                right_layout.addWidget(delete_varpri)

                def delete_varpri_handler2():
                    row = size_price_table.currentRow()
                    if row >= 0:
                        size_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler2)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table():
                    size = size_field.text().strip()
                    price = price_field.text().strip()
                    if not size or not price:
                        QMessageBox.warning(mpd, "Empty Fields", "Please fill in both Size and Price fields.")
                        return
                    row_count = size_price_table.rowCount()
                    size_price_table.insertRow(row_count)
                    size_price_table.setItem(row_count, 0, QTableWidgetItem(size))
                    size_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    size_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table)

                def save_and_load():
                    variety_list = []
                    size_list = []
                    price_list = []
                    row_count = size_price_table.rowCount()
                    var_count = variety_table.rowCount()
                    for row in range(row_count):
                        size = size_price_table.item(row, 0)
                        price = size_price_table.item(row, 1)
                        if size and price:
                            size_list.append(size.text().title())
                            price_list.append(price.text())
                    for row in range(var_count):
                        var = variety_table.item(row, 0)
                        if var:
                            variety_list.append(var.text().title())
                    save = Food()
                    save.type = "Multi-size"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.size = Util.list_to_string(size_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.insert_data(save)
                    load_products(fs, self.prod_table)
                    mpd.close()

                save_button.clicked.connect(save_and_load)
                mpd_layout.addLayout(left_layout)
                mpd_layout.addLayout(center_layout)
                mpd_layout.addLayout(right_layout)
                mpd.setLayout(mpd_layout)
                mpd.exec()

            multi_btn.clicked.connect(multi_product_dialog)

            drinks_btn = QPushButton("Beverages")
            layout.addWidget(drinks_btn)

            def drinks_product_dialog():
                dpd = QDialog()
                dpd.setWindowTitle("Add Beverage Product")
                dpd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                single_titles = [item.title for item in items if item.type == "Drinks"]
                category_combobox.addItems(single_titles)
                size_label = QLabel("Size:")
                size_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(size_label)
                left_layout.addWidget(size_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(dpd.close)

                center_layout = QVBoxLayout()
                variety_table = QTableWidget()
                variety_table.setColumnCount(1)
                variety_table.setHorizontalHeaderLabels(["Variety"])
                variety_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                add_variety = QPushButton("Add Variety")
                delete_variety = QPushButton("Delete Variety")
                center_layout.addWidget(variety_table)
                center_layout.addWidget(variety_label)
                center_layout.addWidget(variety_field)
                center_layout.addWidget(add_variety)
                center_layout.addWidget(delete_variety)

                def add_variety_to_table_dpd():
                    text = variety_field.text().strip()
                    if not text:
                        QMessageBox.warning(dpd, "Empty Field", "Please enter a variety name.")
                        return
                    row = variety_table.rowCount()
                    variety_table.insertRow(row)
                    variety_table.setItem(row, 0, QTableWidgetItem(text))
                    variety_field.clear()

                add_variety.clicked.connect(add_variety_to_table_dpd)

                def delete_variety_handler_dpd():
                    row = variety_table.currentRow()
                    if row >= 0:
                        variety_table.removeRow(row)

                delete_variety.clicked.connect(delete_variety_handler_dpd)

                right_layout = QVBoxLayout()
                size_price_table = QTableWidget()
                size_price_table.setColumnCount(2)
                size_price_table.setHorizontalHeaderLabels(["Size", "Price"])
                size_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(size_price_table)
                right_layout.addWidget(delete_varpri)

                def delete_varpri_handler3():
                    row = size_price_table.currentRow()
                    if row >= 0:
                        size_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler3)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table_dpd():
                    size = size_field.text().strip()
                    price = price_field.text().strip()
                    if not size or not price:
                        QMessageBox.warning(dpd, "Empty Fields", "Please fill in both Size and Price fields.")
                        return
                    row_count = size_price_table.rowCount()
                    size_price_table.insertRow(row_count)
                    size_price_table.setItem(row_count, 0, QTableWidgetItem(size))
                    size_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    size_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table_dpd)

                def save_and_load_dpd():
                    variety_list = []
                    size_list = []
                    price_list = []
                    row_count = size_price_table.rowCount()
                    var_count = variety_table.rowCount()
                    for row in range(row_count):
                        size = size_price_table.item(row, 0)
                        price = size_price_table.item(row, 1)
                        if size and price:
                            size_list.append(size.text().title())
                            price_list.append(price.text())
                    for row in range(var_count):
                        var = variety_table.item(row, 0)
                        if var:
                            variety_list.append(var.text().title())
                    save = Food()
                    save.type = "Drinks"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.size = Util.list_to_string(size_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.insert_data(save)
                    load_products(fs, self.prod_table)
                    dpd.close()

                save_button.clicked.connect(save_and_load_dpd)
                dpd_layout.addLayout(left_layout, 1)
                dpd_layout.addLayout(center_layout, 1)
                dpd_layout.addLayout(right_layout, 2)
                dpd.setLayout(dpd_layout)
                dpd.exec()

            drinks_btn.clicked.connect(drinks_product_dialog)
            dialog.exec()

        def edit_product():
            row = self.prod_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Warning", "No row selected.")
                return
            product_id = int(self.prod_table.item(row, 0).text())

            service = CategoryService()
            items = service.get_data()

            if self.prod_table.item(row, 1).text() == "Single-size":
                spd = QDialog()
                spd.setWindowTitle("Add Single-Size Product")
                spd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                category_combobox.setCurrentText(self.prod_table.item(row, 2).text())
                for item in items:
                    if item.type == "Single-size":
                        category_combobox.addItem(item.title)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(variety_label)
                left_layout.addWidget(variety_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(spd.close)

                right_layout = QVBoxLayout()
                variety_price_table = QTableWidget()
                variety_price_table.setColumnCount(2)
                variety_price_table.setHorizontalHeaderLabels(["Variety", "Price"])
                variety_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(variety_price_table)
                right_layout.addWidget(delete_varpri)

                variety_split = self.prod_table.item(row, 3).text().split(";")
                price_split = self.prod_table.item(row, 4).text().split(";")
                row_length = len(variety_split)

                variety_price_table.setRowCount(row_length)
                for idx in range(row_length):
                    variety_price_table.setItem(idx, 0, QTableWidgetItem(variety_split[idx]))
                    variety_price_table.setItem(idx, 1, QTableWidgetItem(price_split[idx]))

                def delete_varpri_handler():
                    row = variety_price_table.currentRow()
                    if row >= 0:
                        variety_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table():
                    variety = variety_field.text().strip()
                    price = price_field.text().strip()
                    if not variety or not price:
                        QMessageBox.warning(spd, "Empty Fields", "Please fill in both Variety and Price fields.")
                        return
                    row_count = variety_price_table.rowCount()
                    variety_price_table.insertRow(row_count)
                    variety_price_table.setItem(row_count, 0, QTableWidgetItem(variety))
                    variety_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    variety_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table)

                def save_and_load():
                    variety_list = []
                    price_list = []
                    row_count = variety_price_table.rowCount()
                    for row in range(row_count):
                        variety = variety_price_table.item(row, 0)
                        price = variety_price_table.item(row, 1)
                        if variety and price:
                            variety_list.append(variety.text().title())
                            price_list.append(price.text())
                    save = Food()
                    save.type = "Single-size"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.update_data(save)
                    load_products(fs, self.prod_table)
                    spd.close()

                save_button.clicked.connect(save_and_load)
                spd_layout.addLayout(left_layout)
                spd_layout.addLayout(right_layout)
                spd.setLayout(spd_layout)
                spd.exec()
            elif self.prod_table.item(row, 1).text() == "Multi-size":
                mpd = QDialog()
                mpd.setWindowTitle("Add Multi-Size Product")
                mpd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                for item in items:
                    if item.type == "Multi-size":
                        category_combobox.addItem(item.title)
                size_label = QLabel("Size:")
                size_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(size_label)
                left_layout.addWidget(size_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(mpd.close)

                center_layout = QVBoxLayout()
                variety_table = QTableWidget()
                variety_table.setColumnCount(1)
                variety_table.setHorizontalHeaderLabels(["Variety"])
                variety_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                add_variety = QPushButton("Add Variety")
                delete_variety = QPushButton("Delete Variety")
                center_layout.addWidget(variety_table)
                center_layout.addWidget(variety_label)
                center_layout.addWidget(variety_field)
                center_layout.addWidget(add_variety)
                center_layout.addWidget(delete_variety)

                def add_variety_to_table():
                    text = variety_field.text().strip()
                    if not text:
                        QMessageBox.warning(mpd, "Empty Field", "Please enter a variety name.")
                        return
                    row = variety_table.rowCount()
                    variety_table.insertRow(row)
                    variety_table.setItem(row, 0, QTableWidgetItem(text))
                    variety_field.clear()

                add_variety.clicked.connect(add_variety_to_table)

                def delete_variety_handler():
                    row = variety_table.currentRow()
                    if row >= 0:
                        variety_table.removeRow(row)

                delete_variety.clicked.connect(delete_variety_handler)

                right_layout = QVBoxLayout()
                size_price_table = QTableWidget()
                size_price_table.setColumnCount(2)
                size_price_table.setHorizontalHeaderLabels(["Size", "Price"])
                size_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(size_price_table)
                right_layout.addWidget(delete_varpri)

                size_split = self.prod_table.item(row, 5).text().split(";")
                price_split = self.prod_table.item(row, 4).text().split(";")
                row_length = len(size_split)
                size_price_table.setRowCount(row_length)
                for idx in range(row_length):
                    size_price_table.setItem(idx, 0, QTableWidgetItem(size_split[idx]))
                    size_price_table.setItem(idx, 1, QTableWidgetItem(price_split[idx]))

                def delete_varpri_handler2():
                    row = size_price_table.currentRow()
                    if row >= 0:
                        size_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler2)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table():
                    size = size_field.text().strip()
                    price = price_field.text().strip()
                    if not size or not price:
                        QMessageBox.warning(mpd, "Empty Fields", "Please fill in both Size and Price fields.")
                        return
                    row_count = size_price_table.rowCount()
                    size_price_table.insertRow(row_count)
                    size_price_table.setItem(row_count, 0, QTableWidgetItem(size))
                    size_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    size_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table)

                def save_and_load():
                    variety_list = []
                    price_list = []
                    row_count = size_price_table.rowCount()
                    for row in range(row_count):
                        variety = size_price_table.item(row, 0)
                        price = size_price_table.item(row, 1)
                        if variety and price:
                            variety_list.append(variety.text().title())
                            price_list.append(price.text())
                    save = Food()
                    save.type = "Multi-size"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.update_data(save)
                    load_products(fs, self.prod_table)
                    mpd.close()

                save_button.clicked.connect(save_and_load)
                mpd_layout.addLayout(left_layout)
                mpd_layout.addLayout(center_layout)
                mpd_layout.addLayout(right_layout)
                mpd.setLayout(mpd_layout)
                mpd.exec()
            elif self.prod_table.item(row, 1).text() == "Drinks":
                dpd = QDialog()
                dpd.setWindowTitle("Add Beverage Product")
                dpd_layout = QHBoxLayout()

                left_layout = QVBoxLayout()
                category_label = QLabel("Category: ")
                category_combobox = QComboBox()
                category_combobox.setPlaceholderText("Select a Category")
                for item in items:
                    if item.type == "Drinks":
                        category_combobox.addItem(item.title)
                size_label = QLabel("Size:")
                size_field = QLineEdit()
                price_label = QLabel("Price:")
                price_field = QLineEdit()
                add_to_table = QPushButton("Add to table")
                cancel_button = QPushButton("Cancel")
                save_button = QPushButton("Save")
                left_layout.addWidget(category_label)
                left_layout.addWidget(category_combobox)
                left_layout.addWidget(size_label)
                left_layout.addWidget(size_field)
                left_layout.addWidget(price_label)
                left_layout.addWidget(price_field)
                left_layout.addWidget(add_to_table)
                left_layout.addWidget(cancel_button)
                left_layout.addWidget(save_button)

                cancel_button.clicked.connect(dpd.close)

                center_layout = QVBoxLayout()
                variety_table = QTableWidget()
                variety_table.setColumnCount(1)
                variety_table.setHorizontalHeaderLabels(["Variety"])
                variety_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                variety_label = QLabel("Variety:")
                variety_field = QLineEdit()
                add_variety = QPushButton("Add Variety")
                delete_variety = QPushButton("Delete Variety")
                center_layout.addWidget(variety_table)
                center_layout.addWidget(variety_label)
                center_layout.addWidget(variety_field)
                center_layout.addWidget(add_variety)
                center_layout.addWidget(delete_variety)

                variety_split = self.prod_table.item(row, 3).text().split(";")
                row_length = len(variety_split)
                for idx in range(row_length):
                    variety_table.setRowCount(row_length)
                    variety_table.setItem(idx, 0, QTableWidgetItem(variety_split[idx]))

                def add_variety_to_table_dpd():
                    text = variety_field.text().strip()
                    if not text:
                        QMessageBox.warning(dpd, "Empty Field", "Please enter a variety name.")
                        return
                    row = variety_table.rowCount()
                    variety_table.insertRow(row)
                    variety_table.setItem(row, 0, QTableWidgetItem(text))
                    variety_field.clear()

                add_variety.clicked.connect(add_variety_to_table_dpd)

                def delete_variety_handler_dpd():
                    row = variety_table.currentRow()
                    if row >= 0:
                        variety_table.removeRow(row)

                delete_variety.clicked.connect(delete_variety_handler_dpd)

                right_layout = QVBoxLayout()
                size_price_table = QTableWidget()
                size_price_table.setColumnCount(2)
                size_price_table.setHorizontalHeaderLabels(["Size", "Price"])
                size_price_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                delete_varpri = QPushButton("Delete")
                right_layout.addWidget(size_price_table)
                right_layout.addWidget(delete_varpri)

                size_split = self.prod_table.item(row, 5).text().split(";")
                price_split = self.prod_table.item(row, 4).text().split(";")
                row_length = len(size_split)
                size_price_table.setRowCount(row_length)
                for idx in range(row_length):
                    size_price_table.setItem(idx, 0, QTableWidgetItem(size_split[idx]))
                    size_price_table.setItem(idx, 1, QTableWidgetItem(price_split[idx]))

                def delete_varpri_handler3():
                    row = size_price_table.currentRow()
                    if row >= 0:
                        size_price_table.removeRow(row)

                delete_varpri.clicked.connect(delete_varpri_handler3)

                validator = QIntValidator(0, 999999999)
                price_field.setValidator(validator)

                def to_table_dpd():
                    size = size_field.text().strip()
                    price = price_field.text().strip()
                    if not size or not price:
                        QMessageBox.warning(dpd, "Empty Fields", "Please fill in both Size and Price fields.")
                        return
                    row_count = size_price_table.rowCount()
                    size_price_table.insertRow(row_count)
                    size_price_table.setItem(row_count, 0, QTableWidgetItem(size))
                    size_price_table.setItem(row_count, 1, QTableWidgetItem(price))
                    size_field.clear()
                    price_field.clear()

                add_to_table.clicked.connect(to_table_dpd)

                def save_and_load():
                    variety_list = []
                    price_list = []
                    row_count = size_price_table.rowCount()
                    for row in range(row_count):
                        variety = size_price_table.item(row, 0)
                        price = size_price_table.item(row, 1)
                        if variety and price:
                            variety_list.append(variety.text().title())
                            price_list.append(price.text())
                    save = Food()
                    save.type = "Drinks"
                    save.category = category_combobox.currentText()
                    save.variety = Util.list_to_string(variety_list)
                    save.price = Util.list_to_string(price_list)
                    fs = FoodService()
                    fs.update_data(save)
                    load_products(fs, self.prod_table)
                    dpd.close()

                save_button.clicked.connect(save_and_load)
                dpd_layout.addLayout(left_layout)
                dpd_layout.addLayout(center_layout)
                dpd_layout.addLayout(right_layout)
                dpd.setLayout(dpd_layout)
                dpd.exec()

        edit_btn.clicked.connect(edit_product)

        def delete_product():
            row = self.prod_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Warning", "No row selected.")
                return
            product_id = int(self.prod_table.item(row, 0).text())

            service = FoodService()
            if service.delete_data(product_id):
                self.prod_table.removeRow(row)
                QMessageBox.information(self, "Deleted", "Product deleted successfully.")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete product.")

        def search_product():
            key = search_field.text().strip().lower()
            service = FoodService()
            items = service.get_data()
            filtered = [item for item in items if key in item.variety.lower() or key in item.category.lower()]
            search_load(filtered, self.prod_table)

        def search_load(data_list, table: QTableWidget):
            table.setRowCount(0)
            table.setRowCount(len(data_list))
            for row, item in enumerate(data_list):
                table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table.setItem(row, 1, QTableWidgetItem(item.type))
                table.setItem(row, 2, QTableWidgetItem(item.category))
                table.setItem(row, 3, QTableWidgetItem(item.variety))
                if item.type == "Single-size":
                    table.setItem(row, 4, QTableWidgetItem(""))
                    table.setItem(row, 5, QTableWidgetItem(str(item.price)))
                else:
                    table.setItem(row, 4, QTableWidgetItem(item.size))
                    table.setItem(row, 5, QTableWidgetItem(item.price))

        add_btn.clicked.connect(add_product_dialog)
        delete_btn.clicked.connect(delete_product)
        search_btn.clicked.connect(search_product)

        self.setLayout(prod_layout)
        load_products(FoodService(), self.prod_table)


def load_products(service: FoodService, table: QTableWidget):
    table.setRowCount(0)
    data = service.get_data()
    table.setRowCount(len(data))
    for row, item in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(str(item.id)))
        table.setItem(row, 1, QTableWidgetItem(item.type))
        table.setItem(row, 2, QTableWidgetItem(item.category))
        table.setItem(row, 3, QTableWidgetItem(item.variety))
        if item.type == "Single-size":
            table.setItem(row, 4, QTableWidgetItem(""))
            table.setItem(row, 5, QTableWidgetItem(str(item.price)))
        else:
            table.setItem(row, 4, QTableWidgetItem(item.size))
            table.setItem(row, 5, QTableWidgetItem(item.price))
