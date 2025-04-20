
from lb2ticket.model.base_model import BaseModel
from dataclasses import dataclass

@dataclass
class Comment(BaseModel):
    id = None
    comment = None

    def __init__(self, comment=None, id=None):
        self.comment = comment
        self.id=id

    # @property
    def serialize(self):
        return {
           'id': self.id,
           'comment': self.comment
        }