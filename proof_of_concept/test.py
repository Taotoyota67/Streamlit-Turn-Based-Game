import streamlit as st

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col3:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg")
