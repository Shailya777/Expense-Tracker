from abc import ABC, abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def to_dict(self):
        # Method Body will be implemented in Separate Classes Inheriting from it.
        pass