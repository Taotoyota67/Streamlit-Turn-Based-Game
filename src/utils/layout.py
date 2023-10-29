from types import ModuleType


def setup_page(st: ModuleType):
    st.set_page_config(layout="wide")

    # Disable weird shits using css
    hide_img_fs = f"<style>{open('utils/style.css').read()}</style>"
    st.markdown(hide_img_fs, unsafe_allow_html=True)
