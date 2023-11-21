import time
import streamlit as st

from accounts import Accounts, AccountAlreadyExists
from game import Game
from utils.layout import setup_page
from utils.animate import animate_text

# My import

# from entity2 import Player
from storage import PersistanceStorage
import random
from time import sleep
import pandas as pd
import altair as alt

# My import

sess = PersistanceStorage(st)
acc = sess.gset("accounts", Accounts())
username = sess.gset("username", "")
password = sess.gset("password", "")
login_status = sess.gset("login_status", True)
game = sess.gset("game", Game("admin"))
player = sess.gset("player", game.player)
MoveType = game.enums.MoveType


if "page" not in st.session_state:
    st.session_state["page"] = "main_page"


def change_page(page: str) -> None:
    st.session_state["page"] = page


def main_page():
    # setup_page(st)
    col1, col2, col3 = st.columns([0.125, 0.75, 0.125])
    col2.markdown(
        "<h1 style='text-align: center; color: blue;'>PROJECT M</h1>", unsafe_allow_html=True)
    col2.markdown(
        "<h5 style='text-align: center;'>Is this your first time?</h5>", unsafe_allow_html=True)
    col2.title("")
    col2.title("")
    # Buttons
    col2.button("**:blue[Yes]**", on_click=change_page, args=(
        "create_account_page", ), use_container_width=True)
    col2.title("")
    # st.button("No", on_click=change_page, args=("login", ))
    col2.button("**No**", on_click=change_page, args=(
        "login_page", ), use_container_width=True)


def create_account_page():
    # setup_page(st)
    global username
    if acc.has(username):
        st.title(":red[Account already exists!]")
    else:
        st.title(":blue[Let's create an account then...]")

    st.write("What is your username?")
    if not username:
        st.write(
            "*The Confirm button will be disable if your username sucks.*")
    else:
        st.write(f"Your username is :blue[**{username}**]")

    # Text input
    text = st.text_input(
        "Username", max_chars=16,
        placeholder="Enter a username", label_visibility="hidden")

    # Rerun after changing text
    if text != username:
        sess["username"] = text
        st.rerun()

    # Buttons
    st.button("Confirm", on_click=change_page,
              disabled=acc.check_username(username),
              args=("create_password_page",))
    st.button("Back", on_click=change_page, args=("main_page",))


def create_password_page():
    # setup_page(st)
    global username, password
    st.title(":blue[Good name!]")
    st.write(f"Now :blue[**{username}**], What is your password?")

    # Text input
    text = st.text_input("password", placeholder="Enter a password",
                         label_visibility="hidden",
                         type="password")

    # Rerun after changing text
    if text != password:
        sess["password"] = text
        st.rerun()

    # Buttons
    st.button("Confirm", on_click=change_page,
              disabled=len(password) < 3, args=("create_account",))
    st.button("Back", on_click=change_page, args=("create_account_page",))


def create_account():
    # setup_page(st)
    global acc, username, password
    st.title(":blue[Creating account...]")
    try:
        acc.add(username, password)
    except AccountAlreadyExists:
        change_page("create_account_page")
        st.rerun()

    sleep(2.0)
    change_page("login")
    st.rerun()


def login_page():
    # setup_page(st)
    global acc, username, password

    st.title(
        ":blue[Welcome back!]" if login_status else ":red[Incorrect username or password :(]"
    )
    st.write("I promise I won't leak it.")

    # Text inputs
    user_text = st.text_input(
        "Username", max_chars=16,
        placeholder="Enter a username", label_visibility="hidden")
    pass_text = st.text_input("password", placeholder="Enter a password",
                              label_visibility="hidden",
                              type="password")

    if user_text != username:
        sess["username"] = user_text
        st.rerun()
    if pass_text != password:
        sess["password"] = pass_text
        st.rerun()

    # Buttons
    st.button("Login", on_click=change_page, args=("login",))
    st.button("Back", on_click=change_page, args=("main_page",))


def login():
    # setup_page(st)
    global acc, username, password
    st.title(":blue[Logging in...]")
    try:
        success = acc.login(username, password)
    except KeyError:  # No account
        sess["login_status"] = False
        change_page("login_page")
        st.rerun()

    if not success:
        sess["login_status"] = success
        change_page("login_page")
        st.rerun()

    sess["game"] = Game(username)
    change_page("choosing_status")
    st.rerun()


def choosing_status():
    global player, MoveType
    sess.gset("choose", "unknown")
    sess.gset("anable_confirm", False)
    sess.gset("confirm", False)
    sess.gset("skills_list", [])
    col1, col2 = st.columns([0.7, 0.3], gap="large")
    col1.title(":blue[Choose your status]")

    def write_status(hp, mana, atk):
        col2.title(" ")

        status = {'Status': ['HP', "MANA", "ATK"],
                  'amount': [hp, mana, atk]}
        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("amount", scale=alt.Scale(domain=[0, 150]))
        ).properties(width=200)

        col2.altair_chart(my_chart)
        col2.subheader(":blue[Chosen Status]")

        col2.write(f"HP: {hp}")
        col2.write(f"MANA: {mana}")
        col2.write(f"ATK: {atk}")

    def write_skills():
        col2.subheader(":blue[Chosen Skills]")
        for num, skill in enumerate(sess["skills_list"]):
            col2.write(f"{num + 1}. {skill}")

    # Status Choice
    if col1.button("1st status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "1st"
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("2nd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "2nd"
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("3rd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = "3rd"
        sess["anable_confirm"] = True
        st.rerun()

    col1.title(":blue[Choose your skills]")
    col1.write("choose 3 from 5 skills")

    # Skills multiselect
    skills_list = col1.multiselect(label="", options=["DAMAGE BUFF", "HEAL", "POISON", "LIFE STEAL", "STUN"],
                                   default=sess["skills_list"],
                                   max_selections=3,
                                   disabled=sess["confirm"],
                                   label_visibility="collapsed")

    if skills_list != sess["skills_list"]:
        sess["skills_list"] = skills_list
        st.rerun()

    if col1.button("CONFIRM STATUS AND SKILLS", disabled=(not (sess["anable_confirm"])) or (not len(sess["skills_list"]) == 3) or sess["confirm"]):
        sess["confirm"] = True
        st.rerun()

    # Write status after clicking button
    if sess["choose"] != "unknown":
        if sess["choose"] == "1st":
            write_status(100, 100, 5)
            player.stats.max_health.set(100)
            player.stats.health.set(100)
            player.stats.max_mana.set(100)
            player.stats.mana.set(100)
            player.stats.damage.set(5)
        elif sess["choose"] == "2nd":
            write_status(150, 50, 7)
            player.stats.max_health.set(150)
            player.stats.health.set(150)
            player.stats.max_mana.set(50)
            player.stats.mana.set(50)
            player.stats.damage.set(7)
        elif sess["choose"] == "3rd":
            write_status(50, 150, 7)
            player.stats.max_health.set(50)
            player.stats.health.set(50)
            player.stats.max_mana.set(150)
            player.stats.mana.set(150)
            player.stats.damage.set(7)

    # Write skills after clicking confirm and anable "NEXT" button
    if sess["confirm"]:
        write_skills()
        if "DAMAGE BUFF" in sess["skills_list"]:
            player.skills.grant(MoveType.DAMAGE_BUFF)
        if "HEAL" in sess["skills_list"]:
            player.skills.grant(MoveType.HEAL)
        if "POISON" in sess["skills_list"]:
            player.skills.grant(MoveType.POISON)
        if "LIFE STEAL" in sess["skills_list"]:
            player.skills.grant(MoveType.LIFE_STEAL)
        if "STUN" in sess["skills_list"]:
            player.skills.grant(MoveType.STUN)
        col1.button("NEXT", on_click=change_page, args=("fight",))


def fight():
    global player, MoveType
    room = sess.gset("room", 1)
    all_mon_list = sess.gset("all_mon_list", game.monsters.get_all_names())
    boss_list = ["The Gatekeeper", "The Soul Collector", "The Corrupted",
                 "The Rhinoceros", "The Dark Wizard", "The Inferno"]
    mon_list = [name for name in all_mon_list if name not in boss_list]
    sess.gset("pass_mon_turn", True)

    # Choosing between MONSTER and BOSS
    if room in [5, 11, 17]:
        monster = sess.gset(
            "monster", game.get_monster(random.choice(boss_list)))
    else:
        monster = sess.gset(
            "monster", game.get_monster(random.choice(mon_list)))
    sess.gset("press_hit_skill", False)

    # Set up webpage, load CSS
    st.set_page_config(layout="wide")  # type: ignore

    col1, col2 = st.columns([2, 4])

    # Disable weird shits using css
    with open('mylifesad.css') as f:
        hide_img_fs = f"<style>{f.read()}</style>"

    st.markdown(hide_img_fs, unsafe_allow_html=True)
    # sess.gset("setup_page", setup_page(st))

    # Set up player
    if sess["pass_mon_turn"]:
        player.tick()
    # Player display
    if room in [1, 2, 3, 4, 5, 6]:
        floor = 1
    elif room in [7, 8, 9, 10, 11, 12]:
        floor = 2
    else:
        floor = 3

    col1.title(f":blue[FLOOR {floor} | ROOM {room}]")
    chart_empty = col1.empty()

    def update_player_status_chart():
        if player.is_alive():
            status = {
                'Status': ['HP', "MANA"],
                'amount': [player.stats.health.get(), player.stats.mana.get()]
            }
        else:
            status = {
                'Status': ['HP', "MANA"],
                'amount': [0, player.stats.mana.get()]
            }

        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("amount", scale=alt.Scale(
                domain=[0, max(player.stats.max_health.get(), player.stats.max_mana.get())]))
        ).properties(width=200)
        chart_empty.altair_chart(my_chart)

    update_player_status_chart()

    # Disable player button if...
    def dis_but():
        if player.is_stun() or sess["press_hit_skill"]:
            return True
        else:
            return False

    # Still don't pass monster turn
    def not_pass_mon():
        sess["pass_mon_turn"] = False

    # Player text empty
    player_text = col1.empty()

    # Animate text
    def write_text(empty, move_text: str, talk_text: str, move_text_time: float, talk_text_time: float):
        animate_text(empty, move_text, time_per_sentence=move_text_time)
        sleep(2)
        animate_text(
            empty,
            talk_text,
            time_per_sentence=talk_text_time
        )
        sleep(2)
        empty.empty()

    # Hit button
    if col1.button("Hit", disabled=dis_but(), on_click=not_pass_mon):
        sess["press_hit_skill"] = True
        player_move_amount = player.make_move(MoveType.ATTACK, monster)
        # Animate text
        write_text(player_text, f"Dealing DAMAGE for {player_move_amount}.",
                   "\"Whatever it takes... keep moving\"", 1, 1.5)

        player.make_move(MoveType.ATTACK, monster)
        st.rerun()

    # Skill buttons
    if "DAMAGE BUFF" in sess["skills_list"]:
        if col1.button("DAMAGE BUFF", disabled=dis_but() or not player.skills.can_use(MoveType.DAMAGE_BUFF),  on_click=not_pass_mon):
            sess["press_hit_skill"] = True
            player_move_amount = player.make_move(
                MoveType.DAMAGE_BUFF, monster)

            # Animate text
            write_text(player_text, f"Your DAMAGE increase to {player_move_amount}",
                       "\"The strength for the mighty one\"", 1, 1.5)

            st.rerun()
    if "HEAL" in sess["skills_list"]:
        if col1.button("HEAL", disabled=dis_but() or not player.skills.can_use(MoveType.HEAL), on_click=not_pass_mon):
            sess["press_hit_skill"] = True
            player_move_amount = player.make_move(MoveType.HEAL, monster)

            # Animate text
            write_text(player_text, f"You are healing... increasing HP for {player_move_amount}",
                       "\"There is something you need to do right?\"", 1, 1.5)
            st.rerun()
    if "POISON" in sess["skills_list"]:
        if col1.button("POISON", disabled=dis_but() or not player.skills.can_use(MoveType.POISON), on_click=not_pass_mon):
            sess["press_hit_skill"] = True
            player_move_amount = player.make_move(MoveType.POISON, monster)

            # Animate text
            write_text(player_text, f"You used POISON... {monster.name} will take damage over time for {player_move_amount}.",
                       "\"A gradual decay... The inevitable plight of mortal\"", 1.5, 1.5)
            st.rerun()
    if "LIFE STEAL" in sess["skills_list"]:
        if col1.button("LIFE STEAL", disabled=dis_but() or not player.skills.can_use(MoveType.LIFE_STEAL), on_click=not_pass_mon):
            sess["press_hit_skill"] = True
            player_move_amount = player.make_move(MoveType.LIFE_STEAL, monster)

            # Animate text
            write_text(player_text, f"You used LIFE STEAL... decrease {monster.name} HP to increase yours for {player_move_amount}.",
                       "\"A valuable source of life... don't let anyone take it from you\"", 1.5, 1.5)
            st.rerun()
    if "STUN" in sess["skills_list"]:
        if col1.button("STUN", disabled=dis_but() or not player.skills.can_use(MoveType.STUN), on_click=not_pass_mon):
            sess["press_hit_skill"] = True
            player_move_amount = player.make_move(MoveType.STUN, monster)

            # Animate text
            write_text(player_text, f"You used STUN... {monster.name} will be incapable for 1 round",
                       "\"A little rest won't hurt.\"", 1, 1)

            st.rerun()

    # Set up monster
    if player.is_stun() or sess["press_hit_skill"]:
        monster.tick()
    # Monster display
    if monster.name in boss_list:
        col2.title(f":red[{monster.name}]")
    else:
        col2.title(f":blue[{monster.name}]")

    def update_monster_status_chart():
        if monster.is_alive():
            mon_hp = {
                'Status': ['HP'],
                'amount': [monster.stats.health.get()]
            }
        else:
            mon_hp = {
                'Status': ['HP'],
                'amount': [0]
            }

        d_mon_hp = pd.DataFrame(mon_hp)
        mon_chart = alt.Chart(d_mon_hp).mark_bar().encode(
            x=alt.X("amount", scale=alt.Scale(
                domain=[0, monster.stats.max_health.get()])),
            y="Status"
        ).properties(height=105, width=500)
        col2.altair_chart(mon_chart)

    update_monster_status_chart()
    col2.image(monster.image, width=1000)
    mon_text = col2.empty()

    # Monster make move
    if player.is_stun() or sess["press_hit_skill"]:
        if monster.is_stun():
            # # just testing text
            # col2.write(f"{monster.name} is stun")
            # time.sleep(3)
            # Animate text
            write_text(mon_text, f"{monster.name} is STUNNED.",
                       monster.text.get("got_attack"), 1, 1.5)

            time.sleep(3)
            # update_monster_status_chart()
            sess["press_hit_skill"] = False
            sess["pass_mon_turn"] = True
            st.rerun()

        # If monster is not stunned and alive
        elif monster.is_alive():
            mon_move = monster.random_move()
            mon_move_amount = monster.make_move(mon_move, player.entity)
            # # just testing text
            # col2.write(
            #     f"{monster.name} did {mon_move} for {mon_move_amount}")
            # time.sleep(3)
            # sess["press_hit_skill"] = False

            # Animate text
            if mon_move == MoveType.ATTACK:
                write_text(mon_text, f"{monster.name} is dealing DAMAGE for {mon_move_amount}.",
                           monster.text.get("got_attack"), 1, 1.5)
            elif mon_move == MoveType.DAMAGE_BUFF:
                write_text(mon_text, f"{monster.name} DAMAGE increase to {mon_move_amount}",
                           monster.text.get("do_damage_buff"), 1, 1.5)
            elif mon_move == MoveType.HEAL:
                write_text(mon_text, f"{monster.name} is healing... increasing its HP for {mon_move_amount}",
                           monster.text.get("do_heal"), 1, 1.5)
            elif mon_move == MoveType.POISON:
                write_text(mon_text, f"{monster.name} used POISON... PLAYER will take damage over time for {mon_move_amount}.",
                           monster.text.get("do_poison"), 1, 1.5)
            elif mon_move == MoveType.LIFE_STEAL:
                write_text(mon_text, f"{monster.name} used LIFE STEAL... decrease PLAYER HP to increase its for {mon_move_amount}.",
                           monster.text.get("do_life_steal"), 1, 1.5)
            elif mon_move == MoveType.STUN:
                write_text(mon_text, f"{monster.name} used STUN... PLAYER will be incapable for 1 round",
                           monster.text.get("do_stun"), 1, 1.5)
            elif mon_move == MoveType.MANA_DRAIN:
                write_text(mon_text, f"{monster.name} drained PLAYER MANA for {mon_move_amount}.",
                           monster.text.get("do_mana_drain"), 1, 1.5)

            time.sleep(3)
            # update_monster_status_chart()
            sess["press_hit_skill"] = False
            sess["pass_mon_turn"] = True
            st.rerun()


pages = {
    "main_page": main_page,
    "create_account_page": create_account_page,
    "create_password_page": create_password_page,
    "create_account": create_account,
    "login_page": login_page,
    "login": login,
    "choosing_status": choosing_status,
    "fight": fight
}


pages[st.session_state.page]()
