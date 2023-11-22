import streamlit as st


def _load_css(path: str) -> None:
    with open(path) as f:
        css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)


def load_game_css() -> None:
    _load_css("utils/style.css")


def load_remove_css() -> None:
    _load_css("utils/remove.css")
