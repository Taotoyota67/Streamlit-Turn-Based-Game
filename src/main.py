import streamlit as st

from accounts import Accounts, AccountAlreadyExists
from game import Game
from utils.layout import setup_page

# My import

# from entity2 import Player
from storage import PersistanceStorage
import random
from time import sleep
import pandas as pd
import altair as alt

# My import

sess = PersistanceStorage(st)
acc = sess.gset("accounts", Accounts())
username = sess.gset("username", "")
password = sess.gset("password", "")
login_status = sess.gset("login_status", True)
game = sess.gset("game", Game("admin"))


if "page" not in st.session_state:
    st.session_state["page"] = "main_page"


def change_page(page: str) -> None:
    st.session_state["page"] = page


def main_page():
    # setup_page(st)
    col1, col2, col3 = st.columns([0.125, 0.75, 0.125])
    col2.markdown(
        "<h1 style='text-align: center; color: blue;'>PROJECT M</h1>", unsafe_allow_html=True)
    col2.markdown(
        "<h5 style='text-align: center;'>Is this your first time?</h5>", unsafe_allow_html=True)
    col2.title("")
    col2.title("")
    # Buttons
    col2.button("**:blue[Yes]**", on_click=change_page, args=(
        "create_account_page", ), use_container_width=True)
    col2.title("")
    # st.button("No", on_click=change_page, args=("login", ))
    col2.button("**No**", on_click=change_page, args=(
        "login_page", ), use_container_width=True)


def create_account_page():
    # setup_page(st)
    global username
    if acc.has(username):
        st.title(":red[Account already exists!]")
    else:
        st.title(":blue[Let's create an account then...]")

    st.write("What is your username?")
    if not username:
        st.write(
            "*The Confirm button will be disable if your username sucks.*")
    else:
        st.write(f"Your username is :blue[**{username}**]")

    # Text input
    text = st.text_input(
        "Username", max_chars=16,
        placeholder="Enter a username", label_visibility="hidden")

    # Rerun after changing text
    if text != username:
        sess["username"] = text
        st.rerun()

    # Buttons
    st.button("Confirm", on_click=change_page,
              disabled=acc.check_username(username),
              args=("create_password_page",))
    st.button("Back", on_click=change_page, args=("main_page",))


def create_password_page():
    # setup_page(st)
    global username, password
    st.title(":blue[Good name!]")
    st.write(f"Now :blue[**{username}**], What is your password?")

    # Text input
    text = st.text_input("password", placeholder="Enter a password",
                         label_visibility="hidden",
                         type="password")

    # Rerun after changing text
    if text != password:
        sess["password"] = text
        st.rerun()

    # Buttons
    st.button("Confirm", on_click=change_page,
              disabled=len(password) < 3, args=("create_account",))
    st.button("Back", on_click=change_page, args=("create_account_page",))


def create_account():
    # setup_page(st)
    global acc, username, password
    st.title(":blue[Creating account...]")
    try:
        acc.add(username, password)
    except AccountAlreadyExists:
        change_page("create_account_page")
        st.rerun()

    sleep(2.0)
    change_page("login")
    st.rerun()


def login_page():
    # setup_page(st)
    global acc, username, password

    st.title(
        ":blue[Welcome back!]" if login_status else ":red[Incorrect username or password :(]"
    )
    st.write("I promise I won't leak it.")

    # Text inputs
    user_text = st.text_input(
        "Username", max_chars=16,
        placeholder="Enter a username", label_visibility="hidden")
    pass_text = st.text_input("password", placeholder="Enter a password",
                              label_visibility="hidden",
                              type="password")

    if user_text != username:
        sess["username"] = user_text
        st.rerun()
    if pass_text != password:
        sess["password"] = pass_text
        st.rerun()

    # Buttons
    st.button("Login", on_click=change_page, args=("login",))
    st.button("Back", on_click=change_page, args=("main_page",))


def login():
    # setup_page(st)
    global acc, username, password
    st.title(":blue[Logging in...]")
    try:
        success = acc.login(username, password)
    except KeyError:  # No account
        sess["login_status"] = False
        change_page("login_page")
        st.rerun()

    if not success:
        sess["login_status"] = success
        change_page("login_page")
        st.rerun()

    sess["game"] = Game(username)
    change_page("choosing_status")
    st.rerun()


def choosing_status():
    st.write("Not out yet")


pages = {
    "main_page": main_page,
    "create_account_page": create_account_page,
    "create_password_page": create_password_page,
    "create_account": create_account,
    "login_page": login_page,
    "login": login,
    "choosing_status": choosing_status
}


pages[st.session_state.page]()
