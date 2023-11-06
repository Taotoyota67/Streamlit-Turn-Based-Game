import streamlit as st
from storage import PersistanceStorage
sess = PersistanceStorage(st)

def demo_homepage():
    col1, col2, col3 = st.columns([20, 60, 20])
    col2.title(":blue[DEMO HOMEPAGE]")

    col2.title(" ")

    if col2.button("PLAY", type="primary", use_container_width=True):
        sess["page"] = "choosing_status"
        st.rerun()
    
    col2.title(" ")

    if col2.button("QUIT", use_container_width=True):
        col2.write("Please don't (T^T)")