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
    sess.gset("choose", "unknown")
    sess.gset("anable_confirm", False)
    sess.gset("confirm", False)
    sess.gset("skills_list", [])
    col1, col2 = st.columns([0.7, 0.3], gap="large")
    col1.title(":blue[Choose your status]")

    def write_status(hp, mana, atk, heal):
        col2.title(" ")

        status = {'Status': ['HP', "MANA", "ATK", "HEAL"],
                  'amount': [hp, mana, atk, heal]}
        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("amount", scale=alt.Scale(domain=[0, 150]))
        ).properties(width=200)

        col2.altair_chart(my_chart)
        col2.subheader(":blue[Chosen Status]")

        col2.write(f"HP: {hp}")
        col2.write(f"MANA: {mana}")
        col2.write(f"ATK: {atk}")
        col2.write(f"HEAL: {heal}")

    def write_skills():
        col2.subheader(":blue[Chosen Skills]")
        for num, skill in enumerate(sess["skills_list"]):
            col2.write(f"{num + 1}. {skill}")

    # Status Choice
    if col1.button("1st status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "1st"
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("2nd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "2nd"
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("3rd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "3rd"
        sess["anable_confirm"] = True
        st.rerun()

    col1.title(":blue[Choose your skills]")
    col1.write("choose 3 from 5 skills")

    # Skills multiselect
    skills_list = col1.multiselect(label="", options=["DAMAGE BUFF", "HEAL", "POISON", "LIFE STEAL", "STUN"],
                                   default=sess["skills_list"],
                                   max_selections=3,
                                   disabled=sess["confirm"],
                                   label_visibility="collapsed")

    if skills_list != sess["skills_list"]:
        sess["skills_list"] = skills_list
        st.rerun()

    if col1.button("CONFIRM STATUS AND SKILLS", disabled=(not (sess["anable_confirm"])) or (not len(sess["skills_list"]) == 3) or sess["confirm"]):
        sess["confirm"] = True
        st.rerun()

    # Write status after clicking button
    if sess["choose"] != "unknown":
        if sess["choose"] == "1st":
            write_status(100, 100, 10, 10)
            # sess.gset("player", Player(100, 10, 10, 100))
        elif sess["choose"] == "2nd":
            write_status(150, 50, 20, 5)
            # sess.gset("player", Player(150, 20, 5, 50))
        elif sess["choose"] == "3rd":
            write_status(50, 150, 20, 20)
            # sess.gset("player", Player(50, 20, 20, 150))

    # Write skills after clicking confirm
    if sess["confirm"]:
        write_skills()


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
