import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import time
import random

from slime import Slime
from good_boy import Good_Boy
from player import Player

# random monster
if "mon_name" not in st.session_state :
    mon_name = random.choice(["Bocchi", "Good Boy"])
    st.session_state["mon_name"] = mon_name
else :
    mon_name = st.session_state["mon_name"]

# create session state with class object value
if "monster" not in st.session_state :
    if mon_name == "Bocchi" :
        monster = Slime()
        st.session_state["monster"] = monster
    elif mon_name == "Good Boy" :
        monster = Good_Boy()
        st.session_state["monster"] = monster
if "player" not in st.session_state :
    player = Player()
    st.session_state["player"] = player
# create monster image
if st.session_state["monster"].hp != 0 :
    if mon_name == "Bocchi" :
        image = Image.open("bocchi.png")
    if mon_name == "Good Boy" :
        image = Image.open("good_boy.png")
else :
    if mon_name == "Bocchi" :
        image = Image.open("bocchi_dead.png")
    elif mon_name == "Good Boy" :
        image = Image.open("good_boy_dead.jpg")

st.set_page_config(layout="wide")

col1, col2 = st.columns([2, 4])

# Disable weird shits using css
hide_img_fs = "<style>{}</style>".format(open("mylifesad.css").read())

st.markdown(hide_img_fs, unsafe_allow_html=True)

hit_act = False
skill_act = False
if "already dead" not in st.session_state :
    st.session_state["already dead"] = False

col1.title(":blue[Journey of Momo]")

# Player status chart
chart_empty = col1.empty()
status = {'Status': ['HP', "MANA"], 'amount': [st.session_state["player"].hp, st.session_state["player"].mana]}
d_hp = pd.DataFrame(status)
my_chart = alt.Chart(d_hp).mark_bar().encode(
    x="Status",
    y=alt.X("amount", scale=alt.Scale(domain=[0, 100]))
).properties(width=200)
chart_empty.altair_chart(my_chart)

# Hit button
if col1.button("Hit"):
    if not skill_act:
        hit_act = True
        st.session_state["monster"].lose_hp(st.session_state["player"].hit)

# Skill button
if col1.button("Skill"):
    if not hit_act:
        skill_act = True
        st.session_state["player"].heal()
        st.session_state["player"].lose_mana()

        # update player chart
        status = {'Status': ['HP', "MANA"], 'amount': [st.session_state["player"].hp, st.session_state["player"].mana]}
        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("amount", scale=alt.Scale(domain=[0, 100]))
        ).properties(width=200)
        chart_empty.altair_chart(my_chart)


# Writing after using skill or hit
text_empty = col1.empty()
# Writing text after using skill
if skill_act:
    with text_empty:
        for i in range(len("Using skil !!!")):
            time.sleep(0.1)
            st.write("Using skil !!!"[:i+1])
        time.sleep(2)
        for i in range(len("\"Let this divine power be as satisfying nourishment, giving one who has lost their strength the strength to rise again!\"")):
            time.sleep(0.03)
            st.write(
                "\"Let this divine power be as satisfying nourishment, giving one who has lost their strength the strength to rise again!\""[:i+1])
        time.sleep(2)
    text_empty.empty()

# Writing text after using hit
if hit_act:
    with text_empty:
        for i in range(len("Dealing Damage !!!")):
            time.sleep(0.1)
            st.write("Dealing Damage !!!"[:i+1])
        time.sleep(2)
        for i in range(len("\"I know things are difficult right now, but I also know you've got what it takes to get through it.\"")):
            time.sleep(0.03)
            st.write(
                "\"I know things are difficult right now, but I also know you've got what it takes to get through it.\""[:i+1])
        time.sleep(2)
    text_empty.empty()

# Monster status chart
mon_hp = {'Status': ['HP'], 'amount': [st.session_state["monster"].hp]}
d_mon_hp = pd.DataFrame(mon_hp)
mon_chart = alt.Chart(d_mon_hp).mark_bar().encode(
    x=alt.X("amount", scale=alt.Scale(domain=[0, st.session_state["monster"].max_hp])),
    y="Status"
).properties(height=105, width=500)

# Monster display
col2.title(f":red[{mon_name}]")
col2.altair_chart(mon_chart)
col2.image(image, caption=f"wild {mon_name} appeared !!!", width=300)

# Monster empty
mon_empty = col2.empty()

# Writing text after monster being hit
if (hit_act or skill_act) and (st.session_state["monster"].hp != 0):
    # if player hit
    if hit_act:
        with mon_empty:
            mon_got_hit_text = random.choice(st.session_state["monster"].got_hit)
            for i in range(len(mon_got_hit_text)):
                time.sleep(0.03)
                st.write(mon_got_hit_text[:i+1])
            time.sleep(2)
        mon_empty.empty()

    # Monster act
    skill_or_hit = random.choice(["hit", "skill"])
    if skill_or_hit == "hit":
        st.session_state["player"].lose_hp(st.session_state["monster"].hit)

        # Writing text after monster using hit
        with mon_empty:
            mon_do_hit_text = random.choice(st.session_state["monster"].do_hit)
            for i in range(len(f"{mon_name} is hitting !!!")):
                time.sleep(0.1)
                st.write(f"{mon_name} is hitting !!!"[:i+1])
            time.sleep(2)
            for i in range(len(mon_do_hit_text)):
                time.sleep(0.03)
                st.write(mon_do_hit_text[:i+1])
            time.sleep(2)
        mon_empty.empty()
    else:
        skill_random = random.choice(st.session_state["monster"].skill)

        # if monster heal
        if skill_random == "heal":
            st.session_state["monster"].heal()
            mon_heal_text = random.choice(st.session_state["monster"].do_heal)

            # Writing text after monster using heal
            with mon_empty:
                for i in range(len(f"{mon_name} is healing !!!")):
                    time.sleep(0.1)
                    st.write(f"{mon_name} is healing !!!"[:i+1])
                time.sleep(2)
                for i in range(len(mon_heal_text)):
                    time.sleep(0.03)
                    st.write(mon_heal_text[:i+1])
                time.sleep(2)
            mon_empty.empty()

        # if monster charge
        elif skill_random == "charge" :
            st.session_state["monster"].charge()
            mon_charge_text = random.choice(st.session_state["monster"].do_charge)

            # Writng text after monster using charge
            with mon_empty:
                for i in range(len(f"{mon_name} is charging !!!...its attack damage + 10")):
                    time.sleep(0.1)
                    st.write(f"{mon_name} is charging !!!...its attack damage + 10"[:i+1])
                time.sleep(2)
                for i in range(len(mon_charge_text)):
                    time.sleep(0.03)
                    st.write(mon_charge_text[:i+1])
                time.sleep(2)
            mon_empty.empty()
    st.rerun() #########

if (st.session_state["monster"].hp == 0) and not(st.session_state["already dead"]) :
    st.session_state["already dead"] = True
    st.rerun() #########