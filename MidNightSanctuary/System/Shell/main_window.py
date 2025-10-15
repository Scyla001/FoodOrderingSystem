from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from Features.Admin.UI.main import Admin
from Features.Customer.UI.main import Customer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mid-Night Sanctuary!!")
        self.statusBar().showMessage("Grab Your Favourite Food Now!")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.admin = Admin()
        self.customer = Customer()

        self.stack.addWidget(self.customer)
        self.stack.addWidget(self.admin)

        self.customer.switch_admin.connect(self.show_admin)
        self.admin.switch_customer.connect(self.show_customer)

        self.show_customer()

    def show_customer(self):
        self.stack.setCurrentIndex(0)

    def show_admin(self):
        self.stack.setCurrentIndex(1)
