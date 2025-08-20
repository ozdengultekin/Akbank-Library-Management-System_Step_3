import unittest
from unittest.mock import patch, MagicMock
from library import Library, Book

class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Test için boş bir JSON dosyası adı veriyoruz
        self.library = Library(filename="test_library.json")
        self.library.books = []  # Her test öncesi temiz liste

    def tearDown(self):
        # Test sonrası dosyayı temizle
        import os
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    @patch("httpx.get")
    def test_add_book_success(self, mock_get):
        # Open Library API mock
        mock_response_book = MagicMock()
        mock_response_book.status_code = 200
        mock_response_book.json.return_value = {
            "title": "Test Kitap",
            "authors": [{"key": "/authors/OL123A"}]
        }
        mock_response_author = MagicMock()
        mock_response_author.status_code = 200
        mock_response_author.json.return_value = {"name": "Test Yazar"}

        # Farklı URL'ler için farklı dönüş
        def side_effect(url, *args, **kwargs):
            if "authors" in url:
                return mock_response_author
            return mock_response_book

        mock_get.side_effect = side_effect

        book = self.library.add_book("1234567890")
        self.assertEqual(book.title, "Test Kitap")
        self.assertEqual(book.author, "Test Yazar")
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(len(self.library.books), 1)

    def test_add_duplicate_book(self):
        self.library.books.append(Book("Başlık", "Yazar", "123"))
        with self.assertRaises(ValueError):
            self.library.add_book("123")

    def test_update_book_success(self):
        self.library.books.append(Book("Eski Başlık", "Eski Yazar", "111"))
        updated = self.library.update_book("111", "Yeni Başlık", "Yeni Yazar")
        self.assertEqual(updated.title, "Yeni Başlık")
        self.assertEqual(updated.author, "Yeni Yazar")

    def test_update_book_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.library.update_book("999", "Başlık", "Yazar")

    def test_update_book_empty_fields(self):
        self.library.books.append(Book("Başlık", "Yazar", "222"))
        with self.assertRaises(ValueError):
            self.library.update_book("222", "", "")

    def test_remove_book_success(self):
        self.library.books.append(Book("Başlık", "Yazar", "333"))
        self.library.remove_book("333")
        self.assertEqual(len(self.library.books), 0)

    def test_remove_book_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.library.remove_book("999")

    def test_find_book(self):
        book = Book("Başlık", "Yazar", "444")
        self.library.books.append(book)
        found = self.library.find_book("444")
        self.assertEqual(found, book)

    def test_list_books(self):
        book1 = Book("Kitap1", "Yazar1", "555")
        book2 = Book("Kitap2", "Yazar2", "666")
        self.library.books.extend([book1, book2])
        books = self.library.list_books()
        self.assertEqual(books, [book1, book2])


if __name__ == "__main__":
    unittest.main()
