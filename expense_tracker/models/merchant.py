from models.base_model import BaseModel

class Merchant(BaseModel):

    def __init__(self, merchant_id, merchant_name):
        self.merchant_id = merchant_id,
        self.merchant_name = merchant_name

    def to_dict(self):
        return {
            'merchant_id' : self.merchant_id,
            'merchant_name' : self.merchant_name
        }