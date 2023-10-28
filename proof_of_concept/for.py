import streamlit as st
import time

if st.button("Press") :
    for i in range(10) :
        time.sleep(0.5)
        st.write("me")