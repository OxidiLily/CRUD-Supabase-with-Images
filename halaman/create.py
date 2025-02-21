import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

def create():
    # Ambil Supabase URL dan Key dari environment variables
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Supabase URL and Key are required.")
        return
    
    # Inisialisasi klien Supabase
    supabase: Client = create_client(url, key)
    
    # Input form untuk nama dan nim
    nama = st.text_input('Nama',placeholder="Masukkan Nama")
    nim = st.number_input('NIM',step=1,value=None,placeholder="Masukkan NIM")
    
    # Upload gambar
    image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    # Tombol untuk menyimpan data
    if st.button('Save'):
        if not nama or not nim:
            st.error("Nama dan NIM harus diisi.")
            return
        try:
            # Jika ada gambar yang diunggah
            if image is not None:
                # Baca byte gambar dan simpan nama file
                image_bytes = image.read()
                image_name = image.name
                
                # Unggah gambar ke Supabase Storage
                response = supabase.storage.from_("images").upload(
                    path=image_name,
                    file=image_bytes,  # Kirim sebagai bytes langsung, bukan BytesIO
                    file_options={"content-type": image.type}
                )
                
                # Dapatkan URL publik gambar
                image_url = supabase.storage.from_("images").get_public_url(image_name)
                
                # Simpan data ke tabel Supabase
                data = supabase.table("mahasiswa").insert({
                    "nama": nama,
                    "nim": nim,
                    "image_url": image_url
                }).execute()
            else:
                # Jika tidak ada gambar, simpan hanya nama dan nim
                data = supabase.table("mahasiswa").insert({
                    "nama": nama,
                    "nim": nim
                }).execute()
            
            # Tampilkan pesan sukses jika tidak ada error
            st.success("Data Berhasil Disimpan")
        
        except Exception as e:
            # Tangani kesalahan jika terjadi
            st.error("Failed to save data.")
            st.info("Pastikan nim berupa Angka")
    
    # Ambil data dari tabel Supabase
    try:
        datalis = supabase.table('mahasiswa').select('*').execute().data
        
        # Tampilkan data dalam kolom
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("")
        with col2:
            st.write("Data dari Supabase")
            st.dataframe(datalis)
        with col3:
            st.write("")
    
    except Exception as e:
        st.error(f"Failed to fetch data from Supabase: {str(e)}")