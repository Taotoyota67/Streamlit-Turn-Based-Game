import streamlit as st

from utils.layout import setup_page
from game_manager import GameManager
from accounts import Accounts

setup_page(st)

if "gameManager" not in st.session_state:
    acc = Accounts()
    st.session_state["gameManager"] = GameManager(st, acc)
