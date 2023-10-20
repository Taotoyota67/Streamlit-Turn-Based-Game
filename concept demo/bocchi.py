import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt

st.header('Bocchi the slime')

if st.button("Hit") :
    if 'x' in st.session_state :
        st.session_state['x'] += 5
    else:
        st.session_state['x'] = 0

    if 'h' in st.session_state :
        st.session_state['h'] += 0.5
    else :
        st.session_state['h'] = 0

if 'x' in st.session_state :
    hp = {'bocchi': ['HP'], 'amount': [50-st.session_state['h']]}
    d_hp = pd.DataFrame(hp)
    chart = alt.Chart(d_hp).mark_bar().encode(
        x = alt.X('amount', scale=alt.Scale(domain=[0, 50-st.session_state['h']])),
        y = 'bocchi'
    ).properties(height=100, width=500-st.session_state['x'])
    st.altair_chart(chart)
else :
    hp = {'bocchi': ['HP'], 'amount': [50]}
    d_hp = pd.DataFrame(hp)
    chart = alt.Chart(d_hp).mark_bar().encode(
        x='amount',
        y='bocchi'
    ).properties(height=100, width=500)
    st.altair_chart(chart)

if 'h' in st.session_state :
    st.write('Bocchi HP =', 50-st.session_state['h'])
else :
    st.write('Bocchi HP =', 50)

image = Image.open('bocchi.jpg')
st.image(image, caption = 'Bocchi', width = 500)