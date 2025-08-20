from fastapi import FastAPI, HTTPException
from library import Library
from schemas import BookCreate, BookUpdate, BookModel

app = FastAPI(title="Python Kütüphane API", version="1.0")
library = Library()

# ------------------- Kitapları Listele -------------------
@app.get("/books", response_model=list[BookModel])
def list_books():
    return [b.to_dict() for b in library.list_books()]

# ------------------- Yeni Kitap Ekle -------------------
@app.post("/books", response_model=BookModel)
def add_book_endpoint(book: BookCreate):
    try:
        new_book = library.add_book(book.isbn)
        return new_book.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

# ------------------- Kitap Güncelle -------------------
@app.patch("/books/{isbn}", response_model=BookModel)
def update_book_endpoint(isbn: str, book: BookUpdate):
    try:
        updated = library.update_book(isbn, book.title, book.author)
        return updated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ------------------- Kitap Sil -------------------
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    try:
        library.remove_book(isbn)
        return {"message": "Kitap silindi"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
