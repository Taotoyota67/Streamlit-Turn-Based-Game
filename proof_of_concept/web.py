import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt

st.sidebar.write("Haha")
st.sidebar.button("Press")
text = st.sidebar.text_area("write something")


if st.sidebar.button("Hit"):
    if "damage" in st.session_state:
        st.session_state["damage"] += 5
    else:
        st.session_state["damage"] = 5

if "damage" in st.session_state:
    m_hp = 50-st.session_state["damage"]
else:
    m_hp = 50

hp = {'HP': ['bocchi', "me"], 'amount': [m_hp, 100]}
d_hp = pd.DataFrame(hp)
chart = alt.Chart(d_hp).mark_bar().encode(
    x="HP",
    y=alt.X("amount", scale=alt.Scale(domain=[0, 100]))
).properties(width=200)
st.sidebar.altair_chart(chart)

with st.sidebar.expander("expand it"):
    image = Image.open('bocchi.png')
    st.write("you entered the fobidden shrine")
    st.image(image)
