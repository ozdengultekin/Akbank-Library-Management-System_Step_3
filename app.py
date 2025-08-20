import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("📚 Kütüphane Yönetim Sistemi")
menu = ["Kitapları Listele", "Yeni Kitap Ekle", "Kitap Güncelle", "Kitap Sil"]
choice = st.sidebar.selectbox("Menü", menu)

# ------------------- Listeleme -------------------
if choice == "Kitapları Listele":
    try:
        response = requests.get(f"{BASE_URL}/books")
        data = response.json()
        if response.status_code == 200:
            if data:
                for b in data:
                    st.write(f"**{b['title']}** - {b['author']} (ISBN: {b['isbn']})")
            else:
                st.info("Kütüphanede kitap bulunmuyor.")
        else:
            st.error(data.get("detail", "Bilinmeyen hata"))
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API’ye bağlanılamıyor! Hata: {e}")

# ------------------- Yeni Kitap Ekle -------------------
elif choice == "Yeni Kitap Ekle":
    isbn = st.text_input("ISBN girin (13 haneli):")
    if st.button("Kitap Ekle"):
        try:
            response = requests.post(f"{BASE_URL}/books", json={"isbn": isbn})
            data = response.json()
            if response.status_code == 200:
                st.success("Kitap eklendi!")
                st.write(data)
            else:
                st.error(data.get("detail", "Bilinmeyen hata"))
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API’ye bağlanılamıyor! Hata: {e}")

# ------------------- Kitap Güncelle -------------------
elif choice == "Kitap Güncelle":
    isbn = st.text_input("Güncellenecek ISBN:")
    if isbn:
        try:
            response = requests.get(f"{BASE_URL}/books")
            data = response.json()
            book = next((b for b in data if b['isbn'].replace("-", "") == isbn.replace("-", "")), None)
            if book:
                title = st.text_input("Yeni Başlık:", value=book['title'])
                author = st.text_input("Yeni Yazar:", value=book['author'])
                if st.button("Güncelle"):
                    patch_resp = requests.patch(f"{BASE_URL}/books/{isbn}", json={"title": title, "author": author})
                    patch_data = patch_resp.json()
                    if patch_resp.status_code == 200:
                        st.success("Kitap güncellendi!")
                        st.write(patch_data)
                    else:
                        st.error(patch_data.get("detail", "Bilinmeyen hata"))
            else:
                st.warning("Girilen ISBN ile kitap bulunamadı")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API’ye bağlanılamıyor! Hata: {e}")

# ------------------- Kitap Sil -------------------
elif choice == "Kitap Sil":
    isbn = st.text_input("Silinecek ISBN:")
    if st.button("Sil"):
        try:
            response = requests.delete(f"{BASE_URL}/books/{isbn}")
            data = response.json()
            if response.status_code == 200:
                st.success("Kitap silindi!")
            else:
                st.error(data.get("detail", "Bilinmeyen hata"))
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API’ye bağlanılamıyor! Hata: {e}")
