import streamlit as st
from supabase import create_client, Client
import os

# Fungsi untuk menginisialisasi koneksi Supabase
def init_supabase():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("Pastikan SUPABASE_URL dan SUPABASE_KEY telah diatur di environment variables.")
        st.stop()
    return create_client(url, key)

# Fungsi utama untuk update data
def update():
    supabase = init_supabase()

    # Input untuk mencari data
    cari = st.text_input('Cari Data', placeholder="Masukkan Nama atau NIM")
    
    if cari == '':
        st.warning("Silakan masukkan data yang akan di-update.")
    else:
        # Pilih jenis data yang akan di-update
        pilih = st.selectbox(
            "Pilih Data yang akan di-Update",
            ('NIM', 'Nama', 'Gambar'),
            index=None,
            placeholder="Pilih metode kontak..."
        )

        if pilih == 'NIM':
            # Cari data berdasarkan NIM
            data = supabase.table("mahasiswa").select('*').eq('nim', cari).execute().data
            if not data:
                st.warning("Data dengan NIM tersebut tidak ditemukan.")
            else:
                st.write("Data NIM yang akan diubah:")
                st.dataframe(data)
                
                nim_baru = st.text_input('NIM Baru', placeholder="Masukkan NIM Baru")
                if st.button('Update NIM'):
                    updated_data = supabase.table("mahasiswa").update({"nim": nim_baru}).eq("nim", cari).execute().data
                    st.success("NIM berhasil diperbarui!")
                    st.write("Data Setelah di-Update:")
                    st.dataframe(updated_data)

        elif pilih == 'Nama':
            # Cari data berdasarkan Nama
            data = supabase.table("mahasiswa").select('*').eq('nama', cari).execute().data
            if not data:
                st.warning("Data dengan nama tersebut tidak ditemukan.")
            else:
                st.write("Data Nama yang akan diubah:")
                st.dataframe(data)
                
                nama_baru = st.text_input('Nama Baru')
                if st.button('Update Nama'):
                    updated_data = supabase.table("mahasiswa").update({"nama": nama_baru}).eq("nama", cari).execute().data
                    st.success("Nama berhasil diperbarui!")
                    st.write("Data Setelah di-Update:")
                    st.dataframe(updated_data)

        elif pilih == 'Gambar':
            # Cari data berdasarkan NIM untuk update gambar
            data = supabase.table("mahasiswa").select('*').eq('nim', cari).execute().data
            if not data:
                st.warning("Data dengan NIM tersebut tidak ditemukan.")
            else:
                st.write("Data Gambar yang akan diubah:")
                st.dataframe(data)
                
                nim_image = cari
                uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])
                
                if st.button('Update Gambar') and nim_image:
                    if uploaded_file is not None:
                        try:
                            # Baca byte gambar dan simpan nama file
                            image_bytes = uploaded_file.read()
                            image_name = uploaded_file.name
                            
                            # Unggah gambar ke Supabase Storage
                            supabase.storage.from_("images").upload(
                                path=image_name,
                                file=image_bytes,
                                file_options={"content-type": uploaded_file.type}
                            )
                            
                            # Dapatkan URL publik gambar
                            image_url = supabase.storage.from_("images").get_public_url(image_name)
                            
                            # Update kolom `image_url` di tabel `mahasiswa`
                            updated_data = supabase.table("mahasiswa").update({"image_url": image_url}).eq("nim", nim_image).execute()
                            
                            if updated_data.data:
                                st.success("Gambar berhasil diperbarui!")
                                st.write("Data Setelah di Update:")
                                st.dataframe(updated_data.data)
                            else:
                                st.error("Gagal memperbarui gambar.")
                        
                        except Exception as e:
                            st.error(f"Terjadi kesalahan saat mengunggah/memperbarui gambar: {str(e)}")
                    else:
                        st.warning("Silakan pilih gambar untuk diperbarui.")

    # Tampilkan semua data dari tabel mahasiswa
    if st.button('Lihat Data'):
        datalis = supabase.table('mahasiswa').select('*').execute().data
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write("Data dari Supabase")
            st.dataframe(datalis)