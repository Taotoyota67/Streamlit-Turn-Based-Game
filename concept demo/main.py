import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import time
import random

from slime import Slime
# from good_boy import Good_Boy
monster = Slime()
image = Image.open("bocchi.png")

# Disable weird shits using css
hide_img_fs = '''<style>
button[title="View fullscreen"] {
    visibility: hidden; /* disable view full screen on image */
}
.stApp a:first-child {
    display: none; /* disable title link on markdown */
}
details {
    display: none; /* disable save button on graph */
}
</style>'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

hit_act = False
skill_act = False
if "using_heal" not in st.session_state:
    st.session_state["using_heal"] = False
    act = False
else:
    if st.session_state["using_heal"]:
        act = True
    else:
        act = False

st.sidebar.title(":blue[Journey of Momo]")

# Losing mana or not
if "l_m" not in st.session_state:
    l_m = 0
else:
    l_m = st.session_state["l_m"]

# Losing HP or not
if "l_hp" not in st.session_state:
    l_hp = 0
else:
    l_hp = st.session_state["l_hp"]

# Healing or not
if "I_heal" not in st.session_state:
    I_heal = 0
else:
    I_heal = st.session_state["I_heal"]

# Player status chart
status = {'Status': ['HP', "MANA"], 'amount': [100 - l_hp + I_heal, 100-l_m]}
d_hp = pd.DataFrame(status)
my_chart = alt.Chart(d_hp).mark_bar().encode(
    x="Status",
    y=alt.X("amount", scale=alt.Scale(domain=[0, 100]))
).properties(width=200)
st.sidebar.altair_chart(my_chart)

# If I have already using heal the previous rerun, the button will be disabled
if not st.session_state["using_heal"]:
    # Hit button
    if st.sidebar.button("Hit"):
        if not skill_act:
            hit = 5
            act = True
            hit_act = True
            if "I_hit" in st.session_state:
                st.session_state["I_hit"] += 10
            else:
                st.session_state["I_hit"] = 10

            st.session_state["using_heal"] = False

    # Skill button
    if st.sidebar.button("Skill"):
        if not hit_act:
            heal = 5
            act = True
            skill_act = True
            st.session_state["using_heal"] = True

            if "l_m" in st.session_state:
                st.session_state["l_m"] += 10
            else:
                st.session_state["l_m"] = 10

            if "I_heal" in st.session_state:
                st.session_state["I_heal"] += 10
            else:
                st.session_state["I_heal"] = 10


# Writing after using skill or hit
side_empty1 = st.sidebar.empty()
# Writing text after using skill
if skill_act:
    with side_empty1:
        for i in range(len("Using skil !!!")):
            time.sleep(0.1)
            st.write("Using skil !!!"[:i+1])
        time.sleep(2)
        for i in range(len("\"Let this divine power be as satisfying nourishment, giving one who has lost their strength the strength to rise again!\"")):
            time.sleep(0.03)
            st.write(
                "\"Let this divine power be as satisfying nourishment, giving one who has lost their strength the strength to rise again!\""[:i+1])
        time.sleep(2)
    side_empty1.empty()
    st.rerun()

# Writing text after using hit
if hit_act:
    with side_empty1:
        for i in range(len("Dealing Damage !!!")):
            time.sleep(0.1)
            st.write("Dealing Damage !!!"[:i+1])
        time.sleep(2)
        for i in range(len("\"I know things are difficult right now, but I also know you've got what it takes to get through it.\"")):
            time.sleep(0.03)
            st.write(
                "\"I know things are difficult right now, but I also know you've got what it takes to get through it.\""[:i+1])
        time.sleep(2)
    side_empty1.empty()

# Monster losing HP or not
if "I_hit" not in st.session_state:
    I_hit = 0
else:
    I_hit = st.session_state["I_hit"]

# Monster heal or not
if "mon_heal" not in st.session_state:
    mon_heal = 0
else:
    mon_heal = st.session_state["mon_heal"]

# Monster status chart
mon_hp = {'Status': ['HP'], 'amount': [50 - I_hit + mon_heal]}
d_mon_hp = pd.DataFrame(mon_hp)
mon_chart = alt.Chart(d_mon_hp).mark_bar().encode(
    x=alt.X("amount", scale=alt.Scale(domain=[0, 50])),
    y="Status"
).properties(height=105, width=500)

# Monster display
st.title(":red[Bocchi the slime]")
st.altair_chart(mon_chart)
st.image(image, caption="wild Bocchi appeared !!!", width=300)

# Monster empty
mon_empty = st.empty()

# Writing text after monster being hit
if act:
    if hit_act:
        with mon_empty:
            mon_got_hit_text = random.choice(monster.got_hit)
            for i in range(len(mon_got_hit_text)):
                time.sleep(0.03)
                st.write(mon_got_hit_text[:i+1])
            time.sleep(2)
        mon_empty.empty()

    # Monster act
    skill_or_hit = random.choice(["hit", "skill"])
    if skill_or_hit == "hit":
        if "l_hp" in st.session_state:
            st.session_state["l_hp"] += monster.hit
        else:
            st.session_state["l_hp"] = monster.hit

        # Writing text after monster using hit
        with mon_empty:
            mon_do_hit_text = random.choice(monster.do_hit)
            for i in range(len("Bochhi is hitting !!!")):
                time.sleep(0.1)
                st.write("Bochhi is hitting !!!"[:i+1])
            time.sleep(2)
            for i in range(len(mon_do_hit_text)):
                time.sleep(0.03)
                st.write(mon_do_hit_text[:i+1])
            time.sleep(2)
        mon_empty.empty()
    else:
        skill_random = random.choice(monster.skill)
        if skill_random == "heal":
            if "mon_heal" in st.session_state:
                st.session_state["mon_heal"] += monster.heal
            else:
                st.session_state["mon_heal"] = monster.heal
            mon_do_skill_text = random.choice(monster.do_heal)

        # Writing text after monster using skill
        with mon_empty:
            for i in range(len("Bochhi is healing !!!")):
                time.sleep(0.1)
                st.write("Bochhi is healing !!!"[:i+1])
            time.sleep(2)
            for i in range(len(mon_do_skill_text)):
                time.sleep(0.03)
                st.write(mon_do_skill_text[:i+1])
            time.sleep(2)
        mon_empty.empty()

    st.session_state["using_heal"] = False
    st.rerun()
