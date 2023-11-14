import streamlit as st

from accounts import Accounts

# My import

from entity2 import Player
from storage import PersistanceStorage
import random
from time import sleep
import pandas as pd
import altair as alt

# My import

account = Accounts()


if "page" not in st.session_state:
    st.session_state["page"] = "main_menu"


def change_page(page: str) -> None:
    st.session_state["page"] = page


def main():
    st.title("Welcome to THE GAME")
    st.write("Is this your first time?")

    # Buttons
    st.button("Yes", on_click=change_page, args=("create_account", ))
    # st.button("No", on_click=change_page, args=("login", ))
    st.button("No", on_click=change_page, args=("choosing_status", ))


def login_page():
    ...


def create_account_page(text: str = None):
    st.title("Let's create an account then...")
    st.write("What is your username?")
    if text:
        st.write(text)
    else:
        st.write("*The Confirm button will be disable if your username sucks.*")

    # Text input
    text = st.text_input(
        "Username",
        max_chars=16,
        placeholder="Enter a username",
        label_visibility="hidden"
    )

    # Buttons
    st.button("Confirm", on_click=None,
              disabled=account.check_username(text),
              )
    st.button("Back", on_click=change_page, args=("main_menu", ))


def choosing_status():
    sess = PersistanceStorage(st)
    sess.gset("choose", "unknown")
    sess.gset("anable_confirm", False)
    sess.gset("confirm", False)
    # st.write("<style>text-align: center;</style>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.7, 0.3], gap="large")
    col1.title(":blue[Choose your status]")

    def write_status(hp, mana, atk, heal):
        col1.write(f"HP: {hp}")
        col1.write(f"MANA: {mana}")
        col1.write(f"ATK: {atk}")
        col1.write(f"HEAL: {heal}")
        status = {'Status': ['HP', "MANA", "ATK", "HEAL"],
                  'amount': [hp, mana, atk, heal]}
        col2.title(" ")
        col2.title(" ")
        col2.title(" ")
        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("amount", scale=alt.Scale(domain=[0, 150]))
        ).properties(width=200)
        col2.altair_chart(my_chart)

    # Status Choice
    if col1.button("1st status", disabled=sess["confirm"], use_container_width=True):
        write_status(100, 100, 10, 10)
        sess["choose"] = "1st"
        sess["anable_confirm"] = True
    if col1.button("2nd status", disabled=sess["confirm"], use_container_width=True):
        write_status(150, 50, 20, 5)
        sess["choose"] = "2nd"
        sess["anable_confirm"] = True
    if col1.button("3rd status", disabled=sess["confirm"], use_container_width=True):
        write_status(50, 150, 20, 20)
        sess["choose"] = "3rd"
        sess["anable_confirm"] = True

    if col1.button("CONFIRM", disabled=not sess["anable_confirm"]):
        sess["confirm"] = True
        st.rerun()

    # Showing status after confirm
    if sess["confirm"]:
        col1.subheader(":blue[Chose Status]")
        if sess["choose"] == "1st":
            write_status(100, 100, 10, 10)
            sess.gset("player", Player(100, 10, 10, 100))
        elif sess["choose"] == "2nd":
            write_status(150, 50, 20, 5)
            sess.gset("player", Player(150, 20, 5, 50))
        elif sess["choose"] == "3rd":
            write_status(50, 150, 20, 20)
            sess.gset("player", Player(50, 20, 20, 150))

        if col1.button("NEXT"):
            sess["page"] = "fight"
            st.rerun()


pages = {
    "main_menu": main,
    "login": login_page,
    "create_account": create_account_page,
    "choosing_status": choosing_status
}


pages[st.session_state.page]()
