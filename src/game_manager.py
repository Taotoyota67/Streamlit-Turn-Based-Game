from time import sleep
from typing import Optional

import streamlit as st

from accounts import Accounts, AccountAlreadyExists
from game import Game


class GameManager:
    def __init__(self, acc: Accounts) -> None:
        self.acc = acc
        self.col1, self.col2 = None, None
        self.page = st.empty()

        self.playerdata = None
        self.game: Optional[Game] = None
        self.main_page()

    def clear_page(self, clear: bool = True) -> None:
        self.page.empty()
        if clear:
            self.page = st.empty()

    def main_page(self) -> None:
        self.clear_page()
        self.page.title("Welcome to THE GAME")
        st.write("Is this your first time?")

        # Buttons
        st.button("Yes", on_click=self.create_account_page)
        st.button("No", on_click=self.login_page)

    def create_account_page(self, text: str = ""):
        self.clear_page()
        self.page.title("Let's create an account then...")
        st.write("What is your username?")
        if not text:
            st.write(
                "*The Confirm button will be disable if your username sucks.*")
        else:
            st.write(text)

        # Text input
        text = st.text_input(
            "Username", max_chars=16, on_change=self.create_account_page,
            placeholder="Enter a username", label_visibility="hidden")

        # Buttons
        st.button("Confirm", on_click=self.create_password_page,
                  disabled=self.acc.check_username(text),
                  args=(text,))
        st.button("Back", on_click=self.main_page)

    def create_password_page(self, username: str):
        self.clear_page()
        self.page.title("Good name!")
        st.write(f"Now **{username}**, What is your password?")

        # Text input
        password = st.text_input("password", placeholder="Enter a password",
                                 on_change=self.create_password_page,
                                 label_visibility="hidden",
                                 type="password", args=(username,))

        # Buttons
        st.button("Confirm", on_click=self.create_account,
                  disabled=len(password) < 3, args=(username, password))
        st.button("Back", on_click=self.create_account_page)

    def create_account(self, username: str, password: str):
        self.clear_page()
        self.page.title("Creating account...")
        try:
            self.acc.add(username, password)
        except AccountAlreadyExists:
            self.create_account_page("Account already exists!")
            return
        sleep(2.0)
        self.login(username, password)

    def login_page(self, success: bool = True):
        self.clear_page()
        self.page.title(
            "Welcome back!" if success else "Incorrect username/password :("
        )
        st.write("I promise I won't leak it.")

        # Text inputs
        username = st.text_input(
            "Username", max_chars=16, on_change=self.login_page,
            placeholder="Enter a username", label_visibility="hidden")
        password = st.text_input("password", placeholder="Enter a password",
                                 on_change=self.login_page, label_visibility="hidden",
                                 type="password")

        # Buttons
        st.button("Login", on_click=self.login, args=(username, password))
        st.button("Back", on_click=self.main_page)

    def login(self, username: str, password: str):
        self.clear_page()
        self.page.title("Logging in...")
        try:
            success = self.acc.login(username, password)
        except KeyError:  # No account
            self.login_page(False)
            return

        if not success:
            self.login_page(success)
            return

        self.game = Game(username)
        self.stats_page()

    def stats_page(self):
        self.page.empty()

        if self.game is None:
            raise NameError("Game is not yet define.")

        # Work around of an error 'setIn' cannot be called on an ElementNode
        # Which happen when I make columns and empty object at the same time.
        self.col1, self.col2 = st.columns([1, 3])

        self.col1.title("Menu")
        # self.col1.button("Stats", on_click=self.stats_page)
        # self.col1.button("Upgrade", on_click=self.stats_page)
        # self.col1.button("Test", on_click=self.stats_page)

        self.col2.title("Stats")
        # stats = self.game.player.stats
        # self.col2.write(f"Attack Damage: {stats.damage}")
        # self.col2.write(f"Defense: {stats.defense}")
        # self.col2.write(f"Health: {stats.health}")
        # self.col2.write(f"Mana: {stats.mana}")

    def upgrade_page(self):
        ...
