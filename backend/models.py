from datetime import datetime

from pydantic import BaseModel


class NewItem(BaseModel):
    name: str


class Item(NewItem):
    id: int
    date: datetime
