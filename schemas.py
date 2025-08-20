from pydantic import BaseModel, Field, constr

# ------------------- POST (Yeni Kitap) -------------------
class BookCreate(BaseModel):
    isbn: constr(min_length=13, max_length=13) = Field(..., description="13 haneli ISBN numarası")

# ------------------- PATCH (Kitap Güncelle) -------------------
class BookUpdate(BaseModel):
    title: constr(min_length=1) = Field(..., description="Kitap başlığı boş olamaz")
    author: constr(min_length=1) = Field(..., description="Yazar adı boş olamaz")

# ------------------- GET (Response Model) -------------------
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str
