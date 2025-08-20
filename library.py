import json
import os
import httpx


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

    @staticmethod
    def from_dict(data: dict):
        return Book(data["title"], data["author"], data["isbn"])


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def add_book(self, isbn: str):
        if any(b.isbn == isbn for b in self.books):
            raise ValueError("Bu kitap zaten kütüphanede mevcut")

        url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(url, timeout=10, follow_redirects=True)
            if response.status_code == 404:
                raise FileNotFoundError(f"Kitap Open Library'de bulunamadı (ISBN: {isbn})")
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                raise ValueError(f"Open Library’den geçersiz veri geldi (ISBN: {isbn})")

            title = data.get("title", "Bilinmeyen Başlık")
            authors = []
            for author in data.get("authors", []):
                key = author.get("key")
                if key:
                    author_resp = httpx.get(f"https://openlibrary.org{key}.json", timeout=10)
                    if author_resp.status_code == 200:
                        try:
                            authors.append(author_resp.json().get("name", "Bilinmeyen Yazar"))
                        except ValueError:
                            authors.append("Bilinmeyen Yazar")
            author_str = ", ".join(authors) if authors else "Bilinmeyen Yazar"

            book = Book(title, author_str, isbn)
            self.books.append(book)
            self.save_books()
            return book

        except httpx.RequestError as e:
            raise ConnectionError(f"Open Library’e bağlanılamıyor: {e}")
        # --------------- Kitap Güncelle ----------------

    def update_book(self, isbn: str, title: str, author: str):
        book = self.find_book(isbn)
        if not book:
            raise FileNotFoundError("Güncellenecek kitap bulunamadı")
        if not title or not author:
            raise ValueError("Başlık ve yazar boş olamaz")
        book.title = title
        book.author = author
        self.save_books()
        return book
    def remove_book(self, isbn: str):
        book = self.find_book(isbn)
        if not book:
            raise FileNotFoundError("Silinecek kitap bulunamadı")
        self.books = [b for b in self.books if b.isbn != isbn]
        self.save_books()

    def list_books(self):
        return self.books

    def find_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.books = [Book.from_dict(b) for b in data]
                except json.JSONDecodeError:
                    self.books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4, ensure_ascii=False)
