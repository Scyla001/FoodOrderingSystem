from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget,
    QScrollArea, QGridLayout, QLabel, QComboBox, QSpinBox, QDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon

from Features.Customer.services import FoodService, CategoryService
from Features.Customer.model import Category


class Order(QWidget):
    add_order = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        food_drinks_tabs = QTabWidget()

        single_size_foods = QWidget()
        multi_size_foods = QWidget()
        drinks_order = QWidget()

        food_drinks_tabs.addTab(single_size_foods, "Single-Size Food")
        food_drinks_tabs.addTab(multi_size_foods, "Multi-Size Food")
        food_drinks_tabs.addTab(drinks_order, "Beverage")

        single_size_layout = QVBoxLayout()
        multi_size_layout = QVBoxLayout()
        drink_layout = QVBoxLayout()

        single_size_scroll = QScrollArea()
        multi_size_scroll = QScrollArea()
        drink_scroll = QScrollArea()

        single_size_container = QWidget()
        multi_size_container = QWidget()
        drink_container = QWidget()

        single_size_grid = QGridLayout(single_size_container)
        multi_size_grid = QGridLayout(multi_size_container)
        drink_grid = QGridLayout(drink_container)

        single_size_grid.setSpacing(10)
        single_size_grid.setContentsMargins(15, 15, 15, 15)

        multi_size_grid.setSpacing(10)
        multi_size_grid.setContentsMargins(15, 15, 15, 15)

        drink_grid.setSpacing(10)
        drink_grid.setContentsMargins(15, 15, 15, 15)

        single_size_scroll.setWidget(single_size_container)
        multi_size_scroll.setWidget(multi_size_container)
        drink_scroll.setWidget(drink_container)

        single_size_scroll.setWidgetResizable(True)
        multi_size_scroll.setWidgetResizable(True)
        drink_scroll.setWidgetResizable(True)

        single_size_foods.setLayout(single_size_layout)
        multi_size_foods.setLayout(multi_size_layout)
        drinks_order.setLayout(drink_layout)

        single_size_layout.addWidget(single_size_scroll)
        multi_size_layout.addWidget(multi_size_scroll)
        drink_layout.addWidget(drink_scroll)

        order_layout = QVBoxLayout()
        self.setLayout(order_layout)

        order_here = QLabel("Order Here")
        order_here.setObjectName("OrderHere")
        order_here.setStyleSheet(
            """
            #OrderHere {
                background-color: transparent; 
                color: black; 
                font-size: 20px; 
                font-weight: 700; 
                font-family: Arial Black;
            }
            """
        )

        food_drinks_tabs.setObjectName("FoodDrinks")
        food_drinks_tabs.setStyleSheet(
            """
            #FoodDrinks::pane{
            border: 2px solid #f0f8ff;
            background-color: #f0f8ff;
            border-radius: 8px;
            margin-top: 2px;
            }

            #FoodDrinks QTabBar::tab {
                background: #f0f8ff;
                color: black;
                border: 1px solid #b0b0b0;
                border-radius: 6px;
                min-width: 120px;
                min-height: 30px;
                margin: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }

            #FoodDrinks QTabBar::tab:hover {
                background: #d5d5d5;
            }

            #FoodDrinks QTabBar::tab:selected {
                background: black;
                color: white;
                border: 2px solid #7a734f;
            }
            """
        )

        main_order_panel = QWidget()  # tab location
        main_order_panel_layout = QHBoxLayout()
        main_order_panel.setLayout(main_order_panel_layout)
        main_order_panel_layout.addWidget(food_drinks_tabs)

        main_order_panel.setStyleSheet("background-color: #b0c4de")
        order_layout.addWidget(order_here)
        order_layout.addWidget(main_order_panel)

        self.setStyleSheet("background-color: white")
        add_categories(self, single_size_grid, multi_size_grid, drink_grid)

def add_categories(self, grid1: QGridLayout, grid2: QGridLayout, grid3: QGridLayout):
    service = CategoryService()
    categories = service.get_data()

    max_column = 3
    for i, category in enumerate(categories):
        row = int(i / max_column)
        col = i % max_column

        btn = QPushButton(category.title)
        if category.path:
            btn.setIcon(QIcon(category.path))
        else:
            btn.setIcon(QIcon("C:\\Users\\charl\\OneDrive\\Desktop\\Food-Pics\\M.png"))
        btn.setIconSize(QSize(64, 64))
        btn.setFixedSize(100, 100)
        btn.clicked.connect(lambda _, x=category: open_pop(self, x))

        t = category.type.lower()
        if t == "single-size":
            grid1.addWidget(btn, row, col)
        elif t == "multi-size":
            grid2.addWidget(btn, row, col)
        elif t == "drinks":
            grid3.addWidget(btn, row, col)


def open_pop(self, x: Category):
    preview_panel = QDialog()
    preview_panel.setWindowTitle(f"{x.title} Preview")
    preview_panel.setFixedSize(300, 300)

    layout = QVBoxLayout(preview_panel)

    quantity_spin = QSpinBox()
    quantity_spin.setRange(1, 99)
    quantity_spin.setValue(0)

    total_value = QLabel("0")

    title_label = QLabel("Food Preview")

    qty_label = QLabel("Quantity:")
    cont = QWidget()
    cont_layout = QHBoxLayout(cont)
    cont_layout.addWidget(qty_label)
    cont_layout.addWidget(quantity_spin)

    variety_label = QLabel("Variety:")
    variety_combo_box = QComboBox()
    size_label = QLabel("Size:")
    size_combo_box = QComboBox()
    total_label = QLabel("Total:")
    add_to_cart_btn = QPushButton("ADD TO CART")

    service = FoodService()
    foods = service.get_data()

    xtype = x.type.lower()

    pricelist = []

    for item in foods:
        if x.title == item.category:
            if xtype == "single-size":
                for v in item.variety.split(";"):
                    variety_combo_box.addItem(v.strip())
                for p in str(item.price).split(";"):
                    pricelist.append(int(p))
                size_label.hide()
                size_combo_box.hide()


            elif xtype in ("multi-size", "drinks"):
                sizes = item.size.split(";") if item.size != "N/A" else []
                varieties = item.variety.split(";")
                prices = str(item.price).split(";")

                for s in sizes:
                    size_combo_box.addItem(s.strip())
                for v in varieties:
                    variety_combo_box.addItem(v.strip())
                for p in prices:
                    pricelist.append(float(p))

    total = 0

    def update_total(typex: str):
        nonlocal total
        if typex == "single-size":
            qty = quantity_spin.value()
            price = pricelist[variety_combo_box.currentIndex()]
            total = qty * price
            total_value.setText(str(total))
        else:
            qty = quantity_spin.value()
            price = pricelist[size_combo_box.currentIndex()]
            total = qty * price
            total_value.setText(str(total))


    quantity_spin.valueChanged.connect(lambda: update_total(xtype))

    food_var = QWidget()
    food_var_L = QHBoxLayout(food_var)
    food_var_L.addWidget(variety_label)
    food_var_L.addWidget(variety_combo_box)

    size_var = QWidget()
    size_var_L = QHBoxLayout(size_var)
    size_var_L.addWidget(size_label)
    size_var_L.addWidget(size_combo_box)

    total_var = QWidget()
    total_var_L = QHBoxLayout(total_var)
    total_var_L.addWidget(total_label)
    total_var_L.addWidget(total_value)

    layout.addWidget(title_label)
    layout.addWidget(food_var)
    layout.addWidget(size_var)
    layout.addWidget(cont)
    layout.addWidget(total_var)
    layout.addWidget(add_to_cart_btn)

    def save_and_send(self):
        if xtype == "single-size":
            items = [x.title,
                     variety_combo_box.currentText(),
                     pricelist[variety_combo_box.currentIndex()],
                     "N/A",
                     quantity_spin.value(),
                     total]
            self.add_order.emit(items)
            preview_panel.close()
        else:
            items = [x.title,
                     variety_combo_box.currentText(),
                     size_combo_box.currentText(),
                     pricelist[variety_combo_box.currentIndex()],
                     quantity_spin.value(),
                     total]
            self.add_order.emit(items)
            preview_panel.close()

    add_to_cart_btn.clicked.connect(lambda: save_and_send(self))

    preview_panel.exec()
