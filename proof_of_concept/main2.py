import random
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt

from entity import Slime, Player
from storage import PersistanceStorage
from functions import animate_text

sess = PersistanceStorage(st)

# Set up webpage, load CSS
st.set_page_config(layout="wide")  # type: ignore

col1, col2 = st.columns([2, 4])

# Disable weird shits using css
with open('mylifesad.css') as f:
    hide_img_fs = f"<style>{f.read()}</style>"

st.markdown(hide_img_fs, unsafe_allow_html=True)


# mon_name = sess.gset("mon_name", "Bocchi")
already_dead = sess.gset("already_dead", False)
monster = sess.gset("monster", Slime(50, 10, heal=5).set_name("Bocchi"))
player = sess.gset("player", Player(100, 10, 10, 100))


hit_act = False
skill_act = False

col1.title(":blue[Journey of Momo]")

# Player status chart
chart_empty = col1.empty()


def update_player_status_chart():
    status = {
        'Status': ['HP', "MANA"],
        'amount': [player.current_hp, player.current_mana]
    }
    d_hp = pd.DataFrame(status)
    my_chart = alt.Chart(d_hp).mark_bar().encode(
        x="Status",
        y=alt.X("amount", scale=alt.Scale(domain=[0, 100]))
    ).properties(width=200)
    chart_empty.altair_chart(my_chart)


update_player_status_chart()

# Hit button
if col1.button("Hit"):  # TODO: Use call back instead of this shit.
    if not skill_act:
        hit_act = True
        monster.reduce_health(player.damage)

# Skill button
if col1.button("Skill"):
    if not hit_act:
        skill_act = True
        player.heal()
        player.reduce_mana(10)

        update_player_status_chart()


# Writing after using skill or hit
text_empty = col1.empty()
# Writing text after using skill
if skill_act:
    animate_text(text_empty, "Using skill...", time_per_sentence=2)
    sleep(2)
    animate_text(
        text_empty,
        "\"Let this divine power be as satisfying nourishment, \
        giving one who has lost their strength the strength to rise again!\"",
        time_per_sentence=3
    )
    sleep(2)
    text_empty.empty()

# Writing text after using hit
if hit_act:
    animate_text(text_empty, "Dealing Damage...", time_per_sentence=1)
    sleep(2)
    animate_text(
        text_empty,
        "\"I know things are difficult right now, \
        but I also know you've got what it takes to get through it.\"",
        time_per_sentence=3
    )
    sleep(2)
    text_empty.empty()

# Monster status chart


def update_monster_status_chart():
    mon_hp = {
        'Status': ['HP'],
        'amount': [monster.current_hp]
    }
    d_mon_hp = pd.DataFrame(mon_hp)
    mon_chart = alt.Chart(d_mon_hp).mark_bar().encode(
        x=alt.X("amount", scale=alt.Scale(
            domain=[0, st.session_state["monster"].max_hp])),
        y="Status"
    ).properties(height=105, width=500)
    col2.altair_chart(mon_chart)


# Monster display
col2.title(f":red[{monster.name}]")
update_monster_status_chart()
col2.image(
    monster.image,
    width=300
)

# Monster empty
mon_empty = col2.empty()

# Writing text after monster being hit
if (hit_act or skill_act) and (monster.is_alive):
    # if player hit
    if hit_act:
        animate_text(mon_empty, monster.text.get(
            "got_hit"), time_per_sentence=2)
        sleep(2)
        mon_empty.empty()

    # Monster act
    skill_or_hit = random.choice(["hit", "skill"])
    if skill_or_hit == "hit":
        player.reduce_health(monster.damage)

        # Writing text after monster using hit
        animate_text(
            mon_empty, f"{monster.name} is attacking...", time_per_letter=0.1)
        sleep(2)
        animate_text(mon_empty, monster.text.get(
            "do_hit"), time_per_letter=0.1)
        sleep(2)
        mon_empty.empty()
    else:
        monster.heal()
        animate_text(
            mon_empty, f"{monster.name} is healing...", time_per_letter=0.1)
        sleep(2)
        animate_text(mon_empty, monster.text.get(
            "do_heal"), time_per_sentence=2)
        sleep(2)
        mon_empty.empty()

    st.rerun()

if not (monster.is_alive or already_dead):
    sess["already_dead"] = True
    st.rerun()
