import asyncio
from sqlite3 import Connection
from typing import List

from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from .database import get_db, queries
from .models import Item, NewItem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items", response_model=List[Item])
def get_items(db=Depends(get_db)):
    return queries.get_items(db)


@app.get("/items/{id}", response_model=Item)
def get_item(id: int, db: Connection = Depends(get_db)):
    return queries.get_item(db, id=id)


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: NewItem, db: Connection = Depends(get_db)):
    id = queries.create_item(db, name=item.name)
    db.commit()
    return queries.get_item(db, id=id)


@app.put("/items/{id}", response_model=Item)
def update_item(id, item: NewItem, db: Connection = Depends(get_db)):
    queries.update_item(db, id=id, name=item.name)
    db.commit()
    return queries.get_item(db, id=id)


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Connection = Depends(get_db)):
    queries.delete_item(db, id=id)
    db.commit()


for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name
