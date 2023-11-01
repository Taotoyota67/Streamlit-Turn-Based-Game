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
        self.col1, self.col2 = None, None
        self.page = st.empty()
        self.playerdata = None
        self.main_page()
        # self.stats_page()

    def clear_page(self, clear: bool = True) -> None:
        self.page.empty()
        if clear:
            self.page = self.st.empty()

    def main_page(self) -> None:
        self.clear_page()
        self.page.title("Welcome to THE GAME")
        self.st.write("Is this your first time?")

        # Buttons
        self.st.button("Yes", on_click=self.create_account_page)
        self.st.button("No", on_click=self.login_page)

    def create_account_page(self):
        self.clear_page()
        self.page.title("Let's create an account then...")
        self.st.write("What is your username?")
        self.st.write(
            "*The Confirm button will be disable if your username sucks.*")

        # Text input
        text = self.st.text_input(
            "Username", max_chars=16, on_change=self.create_account_page,
            placeholder="Enter a username", label_visibility="hidden")

        # Buttons
        self.st.button("Confirm", on_click=self.create_password_page,
                       disabled=self.acc.check_username(text),
                       args=(text,))
        self.st.button("Back", on_click=self.main_page)

    def create_password_page(self, username: str):
        self.clear_page()
        self.page.title("Good name!")
        self.st.write(f"Now **{username}**, What is your password?")

        # Text input
        password = self.st.text_input("password", placeholder="Enter a password",
                                      on_change=self.create_password_page,
                                      label_visibility="hidden",
                                      type="password", args=(username,))

        # Buttons
        self.st.button("Confirm", on_click=self.create_account,
                       disabled=len(password) < 3, args=(username, password))
        self.st.button("Back", on_click=self.create_account_page)

    def create_account(self, username: str, password: str):
        self.clear_page()
        self.page.title("Creating account...")
        try:
            self.acc.add(username, password)
        except AccountAlreadyExists:
            self.create_account_page()
            return
        sleep(2)
        self.login(username, password)

    def login_page(self, success: bool = True):
        self.clear_page()
        self.page.title(
            "Welcome back!" if success else "Incorrect username/password :("
        )
        self.st.write("I promise I won't leak it.")

        # Text inputs
        username = self.st.text_input(
            "Username", max_chars=16, on_change=self.login_page,
            placeholder="Enter a username", label_visibility="hidden")
        password = self.st.text_input("password", placeholder="Enter a password",
                                      on_change=self.login_page, label_visibility="hidden",
                                      type="password")

        # Buttons
        self.st.button("Login", on_click=self.login, args=(username, password))
        self.st.button("Back", on_click=self.main_page)

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

        self.playerdata = PlayerData(username, self.db)
        self.stats_page()

    def stats_page(self):
        self.page.empty()

        # Work around of an error 'setIn' cannot be called on an ElementNode
        # Which happen when I make columns and empty object at the same time.
        self.col1, self.col2 = self.st.columns([1, 3])

        self.col1.title("Menu")
        self.col1.button("Stats", on_click=self.stats_page)
        self.col1.button("Upgrade", on_click=self.stats_page)
        self.col1.button("Test", on_click=self.stats_page)

        self.col2.title("Monster and Menu details goes here.")
