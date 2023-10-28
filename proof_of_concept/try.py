import streamlit as st
from slime import Slime
import time

mon = Slime()
st.write(mon.hp)
if st.button("skill"):
    mon.heal()
    st.write(mon.hp)
    time.sleep(2)
    st.rerun()
