from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import fitz
import os

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

items_db = []

@app.get("/")
def read_root():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample.pdf")
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return {"content": text[:500000000]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/items", response_model=Item)
def create_item(item: Item):
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(index)
            return {"message": "Item deleted"}
    return {"error": "Item not found"}
