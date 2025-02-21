import streamlit as st
from supabase import create_client, Client
import os

def delete():
    
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("Supabase URL and Key are required.")
        return

    supabase: Client = create_client(url, key)

    nama = st.text_input('Nama')
    if st.button('Delete'):
        data = supabase.table("mahasiswa").delete().eq('nama',nama).execute()
        st.success("Data Berhasil di Hapus")
    datalis = supabase.table('mahasiswa').select('*').execute().data
    
    col1,col2,col3= st.columns(3);
    with col1:
        st.write("")
    with col2:
        st.write("Data dari Supabase")
        st.dataframe(datalis)
    with col3:
        st.write("")