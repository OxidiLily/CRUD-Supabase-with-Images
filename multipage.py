from streamlit_option_menu import option_menu


from halaman.create import create
from halaman.read import read
from halaman.update import update
from halaman.delete import delete


def menu():
    selected = option_menu(
            menu_title =None,
            options = ['Create','Read', 'Update', 'Delete'],
            orientation = "horizontal",
            styles={
            "container": {"padding": "0!important","background-color": "#0000","font-style":"bold"},
            "nav-link": {"font-size": "25px", "--hover-color":"#1F201F"},
            "nav-link-selected": {"background-color": "white","color":"black"},
    }
    )

    if selected == "Create":
        create()
    elif selected == "Read":
        read()
    elif selected == "Update":
        update()
    elif selected == "Delete":
        delete()