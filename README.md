# Akbank-Library-Management-System_Step_3

# Kütüphane Yönetim Sistemi (RESTful API)
## GİRİŞ
Bu repo, Global AI Hub Python 202 Bootcamp sürecinde geliştirilen bitirme projesi kapsamında hazırlanmıştır.<br>
Proje, FastAPI kullanılarak inşa edilmiş RESTful bir kütüphane yönetim sistemidir.<br>
Sistem, kullanıcıların kitap ekleme, silme, güncelleme, arama ve listeleme işlemlerini API uç noktaları (endpoints) üzerinden yapmasına imkan tanır. Kitap bilgileri JSON dosyasında kalıcı olarak saklanır.<br>
Proje, Pydantic ile veri doğrulama, Open Library API ile ISBN’den kitap bilgilerini otomatik alma ve pytest ile test edilmiş sağlam bir yapı sunar.<br>

## 🚀Teknolojiler
Python 3.10+
FastAPI (REST API için) <br>
Uvicorn (ASGI server) <br>
Pydantic (Veri doğrulama için)<br>
Requests (Open Library API çağrıları için)<br>
Streamlit (Kullanıcı arayüzü için) <br>

## ⚙️ Kurulum

1.  Ortamı aktif edin:

    python -m venv .venv
    source .venv/bin/activate   # Mac/Linux
    .venv\Scripts\activate      # Windows

2.  Bağımlılıkları yükleyin:

    pip install -r requirements.txt

3.   Terminalden API sunucusunu başlatın:

    uvicorn api:app --reload

4.  Tarayıcıdan açın:
    👉 http://127.0.0.1:8000/docs burada swagger arayüzünde test işlemi yapabilirsiniz. 

5. http://127.0.0.1:8000/docs çalıştığına emin olduktan sonra terminalden streamlit run app.py

