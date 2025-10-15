from Features.Admin.repository import SaveFood, ReadLogs, SaveCategory
from Features.Admin.model import Food, Category, Logs
from Core.db import get_conn

class FoodService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = SaveFood(self.conn)

    def insert_data(self, food: Food) -> bool:
        if not self._validate(food):
            return False
        self.repo.save_all(food)
        return True

    def get_data(self) -> list[Food]:
        return self.repo.retrieve_all()

    def update_data(self, food: Food) -> bool:
        if not self._validate(food, updating=True):
            return False
        self.repo.update(food)
        return True

    def delete_data(self, food_id: int) -> bool:
        return self.repo.delete(food_id)

    def _validate(self, x: Food, updating=False) -> bool:
        if not x.category or not x.variety:
            return False
        # price should be string for multi-size or a number for single
        if x.type == "single-type" or x.type == "single-size":
            try:
                float(x.price)
            except Exception:
                return False
            return True
        else:
            prices = [p for p in str(x.price).replace(",", ";").split(";") if p.strip()]
            sizes = [s for s in x.size.replace(",", ";").split(";") if s.strip()]
            return bool(sizes and prices)

class LogsService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = ReadLogs(self.conn)

    def get_logs(self):
        return self.repo.retrieve_all()

class CategoryService:
    def __init__(self):
        self.conn = get_conn()
        self.repo = SaveCategory(self.conn)

    def insert_data(self, cat: Category) -> bool:
        if not self._validate(cat):
            return False
        self.repo.save_all(cat)
        return True

    def get_data(self) -> list[Category]:
        return self.repo.retrieve_all()

    def update_data(self, cat: Category) -> bool:
        if not self._validate(cat, updating=True):
            return False
        self.repo.update(cat)
        return True

    def delete_data(self, cat_id: int) -> bool:
        if cat_id:
            self.repo.delete(cat_id)
            return True
        return False

    def _validate(self, x: Category, updating=False) -> bool:
        if not x.title or not x.path:
            return False
        return True


class Util:
    @staticmethod
    def string_to_list(x: str) -> list:
        return x.split(";")

    @staticmethod
    def list_to_string(x: list) -> str:
        return ";".join(x)