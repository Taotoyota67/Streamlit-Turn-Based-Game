import random
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt

from storage import PersistanceStorage
from entity import Player
from page.demo_homepage import demo_homepage
from page.choosing_status import choosing_status
from page.fight import fight

sess = PersistanceStorage(st)
sess.gset("page", "demo_homepage")

# Page execution
if sess["page"] == "demo_homepage":
    demo_homepage()
elif sess["page"] == "choosing_status":
    choosing_status()
elif sess["page"] == "fight":
    fight()

