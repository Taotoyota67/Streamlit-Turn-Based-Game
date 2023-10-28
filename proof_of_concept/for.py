import time
import streamlit as st

if st.button("Press"):
    for i in range(10):
        time.sleep(0.5)
        st.write("me")
