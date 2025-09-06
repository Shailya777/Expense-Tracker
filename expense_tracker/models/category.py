from models.base_model import BaseModel

class Category(BaseModel):

    def __init__(self, category_id, category_name, parent_id, is_income):
        self.category_id = category_id,
        self.category_name = category_name
        self.parent_id = parent_id,
        self.is_income = is_income

    def to_dict(self):
        return {
            'category_id' : self.category_id,
            'category_name' : self.category_name,
            'parent_id' : self.parent_id,
            'is_income' : self.is_income
        }