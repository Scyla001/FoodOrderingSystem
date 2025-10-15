class Food:
    def __init__(self, id=None, type="single-size", category="", variety="", price=0, size="N/A"):
        self.id = id
        self.type = type
        self.category = category
        self.variety = variety
        self.price = price
        self.size = size

class Logs:
    def __init__(self, id=None, date_and_time=None, category="", variety="", price=0, size="N/A", qty=0, total=0):
        self.id = id
        self.date_and_time = date_and_time
        self.category = category
        self.variety = variety
        self.price = price
        self.size = size
        self.qty = qty
        self.total = total

class Category:
    def __init__(self, id=None, title="", path="", type="single-size"):
        self.id = id
        self.title = title
        self.path = path
        self.type = type
