from Features.Customer.repository import ReadFood, SaveLogs, ReadCategory
from Features.Customer.model import Food, Category, Logs
from Core.db import get_conn

class FoodService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = ReadFood(self.conn)

    def get_data(self) -> list[Food]:
        return self.repo.retrieve_all()

class LogsService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = SaveLogs(self.conn)

    def save_logs(self, x: Logs):
        return self.repo.save_all(x)

class CategoryService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = ReadCategory(self.conn)

    def get_data(self) -> list[Category]:
        return self.repo.retrieve_all()
