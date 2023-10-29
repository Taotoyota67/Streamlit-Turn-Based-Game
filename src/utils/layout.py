from types import ModuleType


def setup_page(st: ModuleType):
    st.set_page_config(layout="wide")

    # Disable weird shits using css
    with open('utils/style.css') as f:
        hide_img_fs = f"<style>{f.read()}</style>"
    st.markdown(hide_img_fs, unsafe_allow_html=True)
