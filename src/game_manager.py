from types import ModuleType
from time import sleep

from accounts import Accounts, AccountAlreadyExists
from db import Database
from playerdata import PlayerData


class GameManager:
    def __init__(self, st: ModuleType, db: Database, acc: Accounts) -> None:
        self.st = st
        self.db = db
        self.acc = acc
        self.cols = st.columns([1, 2])
        self.page = st.empty()
        self.playerdata = None
        self.main_page()

    def clear_page(self) -> None:
        self.page.empty()
        self.page = self.st.empty()

    def main_page(self) -> None:
        self.clear_page()
        self.page.title("Welcome to THE GAME")
        self.st.write("Is this your first time?")
        self.st.button("Yes", on_click=self.create_account_page)
        self.st.button("No", on_click=self.login_page)

    def create_account_page(self):
        self.clear_page()
        self.page.title("Let's create an account then...")
        self.st.write("What is your username?")
        self.st.write(
            "*The Confirm button will be disable if your username sucks.*")
        text = self.st.text_input(
            "Username", max_chars=16, on_change=self.create_account_page,
            placeholder="Enter a username", label_visibility="hidden")
        self.st.button("Confirm", on_click=self.create_password_page,
                       disabled=self.acc.check_username(text),
                       args=(text,))
        self.st.button("Back", on_click=self.main_page)

    def create_password_page(self, username: str):
        self.clear_page()
        self.page.title("Good name!")
        self.st.write(f"Now **{username}**, What is your password?")
        password = self.st.text_input("password", placeholder="Enter a password",
                                      on_change=self.create_password_page,
                                      label_visibility="hidden",
                                      type="password", args=(username,))
        self.st.button("Confirm", on_click=self.create_account,
                       disabled=len(password) < 3, args=(username, password))
        self.st.button("Back", on_click=self.create_account_page)

    def create_account(self, username: str, password: str):
        self.clear_page()
        self.page.title("Creating account...")
        try:
            self.acc.add(username, password)
        except AccountAlreadyExists:
            return self.create_account_page()
        sleep(2)
        self.login(username, password)

    def login_page(self, success: bool=True):
        self.clear_page()
        self.page.title(
            "Welcome back!" if success else "Incorrect username/password :("
        )
        self.st.write("I promise I won't leak it.")
        username = self.st.text_input(
            "Username", max_chars=16, on_change=self.login_page,
            placeholder="Enter a username", label_visibility="hidden")
        password = self.st.text_input("password", placeholder="Enter a password",
                                      on_change=self.login_page, label_visibility="hidden",
                                      type="password")
        self.st.button("Login", on_click=self.login, args=(username, password))
        self.st.button("Back", on_click=self.main_page)

    def login(self, username: str, password: str):
        self.clear_page()
        self.page.title("Logging in...")

        success = self.acc.login(username, password)
        sleep(2)
        if not success:
            self.login_page(success)
            return

        self.playerdata = PlayerData(username, self.db)
        self.game_page()

    def game_page(self):
        self.clear_page()
        self.st.write("Yes")
