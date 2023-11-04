import random
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt
import sys
sys.path.append('..')
from storage import PersistanceStorage

sess = PersistanceStorage(st)
sess.gset("choose", "unknown")
sess.gset("anable_confirm", False)
sess.gset("confirm", False)
col1, col2 = st.columns([0.7, 0.3], gap="large")
col1.title(":blue[Choose your status]")
def write_status(hp, mana, atk, heal):
    col1.write(f"HP: {hp}")
    col1.write(f"MANA: {mana}")
    col1.write(f"ATK: {atk}")
    col1.write(f"HEAL: {heal}")
    status = {'Status': ['HP', "MANA", "ATK", "HEAL"], 'amount': [hp, mana, atk, heal]}
    col2.title(" ")
    col2.title(" ")
    col2.title(" ")
    d_hp = pd.DataFrame(status)
    my_chart = alt.Chart(d_hp).mark_bar().encode(
        x="Status",
        y=alt.X("amount", scale=alt.Scale(domain=[0, 150]))
    ).properties(width=200)
    col2.altair_chart(my_chart)

if col1.button("1st status",disabled=sess["confirm"], use_container_width=True):
    write_status(100, 100, 10, 10)
    sess["choose"] = "1st"
    sess["anable_confirm"] = True
if col1.button("2nd status",disabled=sess["confirm"], use_container_width=True):
    write_status(150, 50, 20, 5)
    sess["choose"] = "2nd"
    sess["anable_confirm"] = True
if col1.button("3rd status",disabled=sess["confirm"], use_container_width=True):
    write_status(50, 150, 20, 20)
    sess["choose"] = "3rd"
    sess["anable_confirm"] = True

if col1.button("CONFIRM", disabled=not sess["anable_confirm"]):
    sess["confirm"] = True
    st.rerun()

if sess["confirm"]:
    col1.subheader(":blue[Choosed Status]")
    if sess["choose"] == "1st":
        write_status(100, 100, 10, 10)
    elif sess["choose"] == "2nd":
        write_status(150, 50, 20, 5)
    elif sess["choose"] == "3rd":
        write_status(50, 150, 20, 20)