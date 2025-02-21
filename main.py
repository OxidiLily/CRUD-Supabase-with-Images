import streamlit as st
import datetime
from multipage import menu


#Judul Page
st.set_page_config(page_title='CRUD Supabase - OxidiLily',layout='wide')
hidden_menu = """
<style>
/* Hide Streamlit Branding */
#MainMenu{
    visibility : hidden;
}
header{
    visibility: hidden;
}

footer {
    visibility : hidden;
    }
body{
    background-color:#0000

}
</style>
"""
#Menghilangkan watermark footer
st.markdown(hidden_menu,unsafe_allow_html=True)

col1, col2, col3 = st.columns([11,10,1.5])
x = datetime.datetime.now()
with col1:
    st.write(x.strftime("%d"),x.strftime("%B"),x.strftime("%Y"))
with col3:
    st.write(" ")






if __name__ == "__main__":
    menu()