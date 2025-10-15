from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QLineEdit, QMessageBox, QDialog, QFileDialog,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from Features.Admin.model import Category
from Features.Admin.services import CategoryService


class CategoryUI(QWidget):
    def __init__(self):
        super().__init__()

        def load_category():
            if self.cate_table.rowCount() > 0:
                self.cate_table.setRowCount(0)
            service = CategoryService()
            data = service.get_data()
            self.cate_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.cate_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                self.cate_table.setItem(row, 1, QTableWidgetItem(item.title))
                self.cate_table.setItem(row, 2, QTableWidgetItem(item.path))
                self.cate_table.setItem(row, 3, QTableWidgetItem(item.type))

        cate_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        cate_layout.addLayout(menu_layout)
        self.cate_table = QTableWidget()
        cate_layout.addWidget(self.cate_table)
        self.cate_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        add_btn = QPushButton("Add Category")
        edit_btn = QPushButton("Edit Category")
        delete_btn = QPushButton("Delete Category")
        search_btn = QPushButton("Search")
        search_field = QLineEdit()
        search_field.setPlaceholderText("Enter keyword")

        def add_dialog():
            add_pop = QDialog()
            add_pop.setWindowTitle("Add Category")
            layout = QVBoxLayout()
            add_pop.setLayout(layout)

            select_cate = QLabel("Select Category")
            single_btn = QPushButton("Single Size Category")
            multi_btn = QPushButton("Multi Size Category")
            drinks_btn = QPushButton("Beverages")

            layout.addWidget(select_cate)
            layout.addWidget(single_btn)
            layout.addWidget(multi_btn)
            layout.addWidget(drinks_btn)

            def single_dialog(type: str):
                single_pop = QDialog()
                single_pop.setWindowTitle("Add Single-Size Category")
                single_layout = QVBoxLayout()
                single_pop.setLayout(single_layout)

                type_label = QLabel(f"Type: {type}")
                title_label = QLabel("Enter Title:")
                title_field = QLineEdit()
                image_label = QLabel("No image selected")
                select_btn = QPushButton("Select Image")
                save_btn = QPushButton("Save Category")

                file_path = ""

                def select_image():
                    nonlocal file_path
                    file_path, _ = QFileDialog.getOpenFileName(
                        None,
                        "Select Image",
                        "C:/Users/charl/OneDrive/Desktop/Food-Pics",
                        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                    )
                    if file_path:
                        logo = QPixmap(file_path)
                        logo_resized = logo.scaled(150, 150)
                        image_label.setPixmap(logo_resized)
                        image_label.setScaledContents(False)
                    else:
                        image_label.setText("No image selected")

                def save():
                    data = Category()
                    data.type = type
                    data.title = title_field.text()
                    data.path = file_path
                    single_pop.close()
                    service = CategoryService()
                    if service.insert_data(data):
                        QMessageBox.information(self, "Success!", "Data Saved Successfully!!")
                        load_category()
                    else:
                        QMessageBox.warning(self, "Notice", "Some Data You Enter Is Not Valid...")

                select_btn.clicked.connect(select_image)
                save_btn.clicked.connect(save)

                single_layout.addWidget(type_label)
                single_layout.addWidget(title_label)
                single_layout.addWidget(title_field)
                single_layout.addWidget(select_btn)
                single_layout.addWidget(image_label)
                single_layout.addWidget(save_btn)

                single_pop.exec()

            def multi_dialog(type: str):
                multi_pop = QDialog()
                multi_pop.setWindowTitle("Add Multi-Size Category")
                multi_layout = QVBoxLayout()
                multi_pop.setLayout(multi_layout)

                type_label = QLabel(f"Type: {type}")
                title_label = QLabel("Enter Title:")
                title_field = QLineEdit()
                image_label = QLabel("No image selected")
                select_btn = QPushButton("Select Image")
                save_btn = QPushButton("Save Category")

                file_path = ""

                def select_image():
                    nonlocal file_path
                    file_path, _ = QFileDialog.getOpenFileName(
                        None,
                        "Select Image",
                        "C:/Users/charl/OneDrive/Desktop/Food-Pics",
                        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                    )
                    if file_path:
                        logo = QPixmap(file_path)
                        logo_resized = logo.scaled(150, 150)
                        image_label.setPixmap(logo_resized)
                        image_label.setScaledContents(False)
                    else:
                        image_label.setText("No image selected")

                def save():
                    data = Category()
                    data.type = type
                    data.title = title_field.text()
                    data.path = file_path
                    multi_pop.close()
                    service = CategoryService()
                    if service.insert_data(data):
                        QMessageBox.information(self, "Success!", "Data Saved Successfully!!")
                        load_category()
                    else:
                        QMessageBox.warning(self, "Notice", "Some Data You Enter Is Not Valid...")

                select_btn.clicked.connect(select_image)
                save_btn.clicked.connect(save)

                multi_layout.addWidget(type_label)
                multi_layout.addWidget(title_label)
                multi_layout.addWidget(title_field)
                multi_layout.addWidget(select_btn)
                multi_layout.addWidget(image_label)
                multi_layout.addWidget(save_btn)

                multi_pop.exec()

            def drinks_dialog(type: str):
                drinks_pop = QDialog()
                drinks_pop.setWindowTitle("Add Beverage Category")
                drinks_layout = QVBoxLayout()
                drinks_pop.setLayout(drinks_layout)

                type_label = QLabel(f"Type: {type}")
                title_label = QLabel("Enter Title:")
                title_field = QLineEdit()
                image_label = QLabel("No image selected")
                select_btn = QPushButton("Select Image")
                save_btn = QPushButton("Save Category")

                file_path = ""

                def select_image():
                    nonlocal file_path
                    file_path, _ = QFileDialog.getOpenFileName(
                        None,
                        "Select Image",
                        "C:/Users/charl/OneDrive/Desktop/Food-Pics",
                        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                    )
                    if file_path:
                        logo = QPixmap(file_path)
                        logo_resized = logo.scaled(150, 150)
                        image_label.setPixmap(logo_resized)
                        image_label.setScaledContents(False)
                    else:
                        image_label.setText("No image selected")

                def save():
                    data = Category()
                    data.type = type
                    data.title = title_field.text()
                    data.path = file_path
                    drinks_pop.close()
                    service = CategoryService()
                    if service.insert_data(data):
                        QMessageBox.information(self, "Success!", "Data Saved Successfully!!")
                        load_category()
                    else:
                        QMessageBox.warning(self, "Notice", "Some Data You Enter Is Not Valid...")

                select_btn.clicked.connect(select_image)
                save_btn.clicked.connect(save)

                drinks_layout.addWidget(type_label)
                drinks_layout.addWidget(title_label)
                drinks_layout.addWidget(title_field)
                drinks_layout.addWidget(select_btn)
                drinks_layout.addWidget(image_label)
                drinks_layout.addWidget(save_btn)

                drinks_pop.exec()

            single_btn.clicked.connect(lambda: single_dialog("Single-size"))
            multi_btn.clicked.connect(lambda: multi_dialog("Multi-size"))
            drinks_btn.clicked.connect(lambda: drinks_dialog("Drinks"))

            add_pop.exec()

        def edit_dialog():
            row = self.cate_table.currentRow()
            if row == -1:
                QMessageBox.information(self, "No selection", "Please select a row to edit.")
                return

            cat_id = int(self.cate_table.item(row, 0).text())
            title = self.cate_table.item(row, 1).text()
            path = self.cate_table.item(row, 2).text()
            type_ = self.cate_table.item(row, 3).text()

            edit_pop = QDialog()
            edit_pop.setWindowTitle("Edit Category")
            edit_layout = QVBoxLayout()
            edit_pop.setLayout(edit_layout)

            type_label = QLabel(f"Type: {type_}")
            title_label = QLabel("Enter Title:")
            title_field = QLineEdit(title)

            image_label = QLabel()
            current_image_path = path

            if path and not QPixmap(path).isNull():
                pixmap = QPixmap(path).scaled(150, 150)
                image_label.setPixmap(pixmap)
            else:
                image_label.setText("No image selected")

            select_btn = QPushButton("Select Image")
            save_btn = QPushButton("Save Changes")

            def select_image():
                nonlocal current_image_path
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Select Image",
                    "C:/Users/charl/OneDrive/Desktop/Food-Pics",
                    "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                )
                if file_path and QPixmap(file_path).isNull() is False:
                    pixmap = QPixmap(file_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                    current_image_path = file_path
                else:
                    image_label.setText("No image selected")
                    image_label.setPixmap(QPixmap())
                    current_image_path = ""

            select_btn.clicked.connect(select_image)

            def save_changes():
                cat_model = Category()
                cat_model.id = cat_id
                cat_model.title = title_field.text()
                cat_model.path = current_image_path
                cat_model.type = type_

                service = CategoryService()
                service.update_data(cat_model)

                row = self.cate_table.currentRow()
                self.cate_table.setItem(row, 1, QTableWidgetItem(cat_model.title))
                self.cate_table.setItem(row, 2, QTableWidgetItem(cat_model.path))

                edit_pop.accept()

            save_btn.clicked.connect(save_changes)

            edit_layout.addWidget(type_label)
            edit_layout.addWidget(title_label)
            edit_layout.addWidget(title_field)
            edit_layout.addWidget(select_btn)
            edit_layout.addWidget(image_label)
            edit_layout.addWidget(save_btn)

            edit_pop.exec()

        def delete_dialog():
            row = self.cate_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Warning", "No row selected")
                return

            record_id = int(self.cate_table.item(row, 0).text())
            svc = CategoryService()
            svc.delete_data(record_id)
            load_category()
            QMessageBox.information(self, "Deleted", "Category deleted.")

        def search_engine():
            key = search_field.text().strip().lower()
            service = CategoryService()
            items = service.get_data()
            filtered = [item for item in items if key in item.title.lower()]
            table = self.cate_table
            table.setRowCount(len(filtered))
            for row, item in enumerate(filtered):
                table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table.setItem(row, 1, QTableWidgetItem(item.title))
                table.setItem(row, 2, QTableWidgetItem(item.path))
                table.setItem(row, 3, QTableWidgetItem(item.type))

        add_btn.clicked.connect(lambda: add_dialog())
        edit_btn.clicked.connect(lambda: edit_dialog())
        delete_btn.clicked.connect(lambda: delete_dialog())
        search_btn.clicked.connect(lambda: search_engine())

        menu_layout.addWidget(add_btn, 1)
        menu_layout.addWidget(edit_btn, 1)
        menu_layout.addWidget(delete_btn, 1)
        menu_layout.addWidget(search_btn, 1)
        menu_layout.addWidget(search_field, 2)

        self.cate_table.setColumnCount(4)
        self.cate_table.setHorizontalHeaderLabels(["ID", "Title", "Path", "Type"])
        header = self.cate_table.horizontalHeader()
        for i in range(2, 4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.cate_table.setColumnHidden(0, True)
        self.cate_table.setObjectName("CategoryTable")
        self.cate_table.setStyleSheet("""
                #CategoryTable QHeaderView::section {
                    background-color: #36c4f4;
                    color: #ffffff;
                    font-weight: bold;
                    border: 2px solid #4c98b9;
                    font-family: Consolas;
                }
                #CategoryTable {
                    background-color: #71afdb;
                    color: white
                }
                """)
        self.setLayout(cate_layout)
        load_category()