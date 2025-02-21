import streamlit as st
from supabase import create_client, Client
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def read():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("Supabase URL and Key are required.")
        return

    supabase: Client = create_client(url, key)

    datalis = supabase.table('mahasiswa').select('*').execute().data

    df = pd.DataFrame(columns=["NO ID", "Nama", "Nim", "Image URL"])
    for i in range(len(datalis)):
        currentItem = datalis[i]
        df.loc[i] = [currentItem["id"], currentItem["nama"], currentItem["nim"], currentItem.get("image_url", "")]

    cari = st.text_input('Cari Data')
    if st.button('Cari nama'):
        data = supabase.table("mahasiswa").select('*').eq('nama', cari).execute().data
        st.write("Data nama yang dicari")
        st.dataframe(data)
        for item in data:
            if "image_url" in item and item["image_url"]:
                st.image(item["image_url"], caption=item["nama"])
    if st.button('Cari Nim'):
        data = supabase.table("mahasiswa").select('*').eq('nim', cari).execute().data
        st.write("Data nim yang dicari")
        st.dataframe(data)
        for item in data:
            if "image_url" in item and item["image_url"]:
                st.image(item["image_url"], caption=item["nama"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.write("Data dari Supabase")
        st.dataframe(datalis)
        for item in datalis:
            if "image_url" in item and item["image_url"]:
                st.image(item["image_url"], caption=item["nama"])
    with col3:
        st.write("")

if __name__ == "__main__":
    read()