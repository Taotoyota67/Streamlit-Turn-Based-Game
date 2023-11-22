import random
import time
from time import sleep

import altair as alt
import pandas as pd
import streamlit as st

from accounts import AccountAlreadyExists, Accounts
from game import Game, enums
from storage import PersistanceStorage
from utils.animate import animate_text
from utils.layout import load_game_css, load_remove_css

sess = PersistanceStorage(st)

acc = sess.gset("accounts", Accounts())
username = sess.gset("username", "")
password = sess.gset("password", "")
login_status = sess.gset("login_status", True)

MoveType = enums.MoveType

if "page" not in st.session_state:
    st.session_state["page"] = "main_page"


def change_page(page: str) -> None:
    st.session_state["page"] = page


def main_page():
    load_remove_css()

    _, col2, _ = st.columns([0.125, 0.75, 0.125])

    col2.markdown(
        "<h1 style='text-align: center; color: blue;'>PROJECT M</h1>", unsafe_allow_html=True)
    col2.markdown(
        "<h5 style='text-align: center;'>Is this your first time?</h5>", unsafe_allow_html=True)
    col2.title("")
    col2.title("")
    # Buttons
    col2.button("**:green[Yes]**", on_click=change_page, args=(
        "create_account_page", ), use_container_width=True)
    col2.title("")
    col2.button("**:red[No]**", on_click=change_page, args=(
        "login_page", ), use_container_width=True)


def create_account_page():
    load_remove_css()

    if acc.has(username):
        st.title(":red[Account Already Exists!]")
    else:
        st.title(":blue[Let's create an account then...]")

    st.write("What is your username?")
    if not username:
        st.write(
            "*The Confirm button will be disable if your username sucks.*"
        )
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
    load_remove_css()

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
    load_remove_css()

    st.title(":blue[Creating Account...]")
    try:
        acc.add(username, password)
    except AccountAlreadyExists:
        change_page("create_account_page")
        st.rerun()

    sleep(2.0)
    change_page("login")
    st.rerun()


def login_page():
    load_remove_css()

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
    load_remove_css()

    st.title(":blue[Logging in...]")
    try:
        success = acc.login(username, password)
    except KeyError:  # No account
        sess["login_status"] = False
        change_page("login_page")
        st.rerun()
        return  # Add return so IDE knows we left.

    if not success:
        sess["login_status"] = success
        change_page("login_page")
        st.rerun()

    sess["game"] = Game(username)
    change_page("choosing_status")
    st.rerun()


def choosing_status():  # pylint: disable=too-many-branches,too-many-statements
    if sess["game"] is None:
        raise RuntimeError("Game object is not initialized.")

    load_remove_css()

    player = sess["game"].player

    sess.nset("choose", 0)
    sess.nset("anable_confirm", False)
    sess.nset("confirm", False)
    sess.nset("skills_list", [])
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
        sess["choose"] = 1
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("2nd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = 2
        sess["anable_confirm"] = True
        st.rerun()
    if col1.button("3rd status", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = 3
        sess["anable_confirm"] = True
        st.rerun()

    col1.title(":blue[Choose Your Skills]")
    col1.write("You may choose 3 from 5 skills")

    # Skills multiselect
    skills_list = col1.multiselect(
        label="",
        options=["DAMAGE x2", "HEAL", "POISON", "LIFE STEAL", "STUN"],
        default=sess["skills_list"],
        max_selections=3,
        disabled=sess["confirm"],
        label_visibility="collapsed"
    )

    if skills_list != sess["skills_list"]:
        sess["skills_list"] = skills_list
        st.rerun()

    if col1.button(
        "CONFIRM STATUS AND SKILLS",
        disabled=(not sess["anable_confirm"]
                  or len(sess["skills_list"]) != 3
                  or sess["confirm"])
    ):
        sess["confirm"] = True
        st.rerun()

    # Write status after clicking button
    if sess["choose"] == 1:
        write_status(50, 30, 5)
        player.stats.max_health.set(50)
        player.stats.health.set(50)
        player.stats.max_mana.set(30)
        player.stats.mana.set(30)
        player.stats.damage.set(5)
    elif sess["choose"] == 2:
        write_status(70, 15, 8)
        player.stats.max_health.set(70)
        player.stats.health.set(70)
        player.stats.max_mana.set(15)
        player.stats.mana.set(15)
        player.stats.damage.set(8)
    elif sess["choose"] == 3:
        write_status(30, 60, 7)
        player.stats.max_health.set(30)
        player.stats.health.set(30)
        player.stats.max_mana.set(60)
        player.stats.mana.set(60)
        player.stats.damage.set(7)

    # Write skills after clicking confirm and anable "NEXT" button
    if sess["confirm"]:
        write_skills()
        if "DAMAGE x2" in sess["skills_list"]:
            player.skills.grant(MoveType.DAMAGE_BUFF)
        if "HEAL" in sess["skills_list"]:
            player.skills.grant(MoveType.HEAL)
        if "POISON" in sess["skills_list"]:
            player.skills.grant(MoveType.POISON)
        if "LIFE STEAL" in sess["skills_list"]:
            player.skills.grant(MoveType.LIFE_STEAL)
        if "STUN" in sess["skills_list"]:
            player.skills.grant(MoveType.STUN)

        if col1.button("NEXT"):
            del st.session_state["choose"]
            del st.session_state["confirm"]
            del st.session_state["anable_confirm"]
            change_page("fight")
            st.rerun()


def fight():  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    if sess["game"] is None:
        raise RuntimeError("Game object is not initialized.")

    game: Game = sess["game"]
    player = game.player

    st.set_page_config(layout="wide")
    load_remove_css()
    load_game_css()

    room = sess.gset("room", 1)

    all_mon_list = sess.gset("all_mon_list", game.monsters.get_all_names())
    boss_list = ["The Gatekeeper", "The Soul Collector", "The Corrupted",
                 "The Rhinoceros", "The Dark Wizard", "The Inferno"]
    mon_list = [name for name in all_mon_list if name not in boss_list]

    sess.nset("pass_mon_turn", True)
    sess.nset("press_hit_skill", False)
    sess.nset("do_skill", None)

    # Choosing between MONSTER and BOSS
    if room in [4, 8, 12]:
        monster = sess.gset(
            "monster",
            game.get_monster(random.choice(boss_list))
        )
    else:
        monster = sess.gset(
            "monster",
            game.get_monster(random.choice(mon_list))
        )

    col1, col2 = st.columns([2, 4])

    if sess["pass_mon_turn"]:
        player.tick()

    if room <= 4:
        floor = 1
    elif 5 <= room <= 8:
        floor = 2
        monster.stats.max_health.set(
            int(1.5 * monster.stats.get("max_health"))
        )
        monster.stats.health.set(
            int(1.5 * monster.stats.get("health"))
        )
        monster.stats.damage.set(
            int(1.5 * monster.stats.get("damage"))
        )
    else:
        floor = 3
        monster.stats.max_health.set(
            int(2.5 * monster.stats.get("max_health"))
        )
        monster.stats.health.set(
            int(2.5 * monster.stats.get("health"))
        )
        monster.stats.damage.set(
            int(2.5 * monster.stats.get("damage"))
        )

    col1.title(f":blue[FLOOR {floor} | ROOM {room % 5}]")
    chart_empty = col1.empty()

    def update_player_status_chart():
        status = {
            'Status': ['HP', "MANA"],
            'Amount': [player.stats.health.get(), player.stats.mana.get()]
        }

        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("Amount", scale=alt.Scale(
                domain=[0, max(player.stats.max_health.get(), player.stats.max_mana.get())]))
        ).properties(width=200)
        chart_empty.altair_chart(my_chart)

    update_player_status_chart()

    def dissable_button() -> bool:
        return not player.is_alive() or player.is_stun() or sess["press_hit_skill"]

    def dissable_skill(move: MoveType) -> bool:
        return dissable_button() and player.skills.can_use(move)

    # Still don't pass monster turn
    def skill_click(move_type=None):
        sess["do_skill"] = move_type
        sess["pass_mon_turn"] = False
        sess["press_hit_skill"] = True

    player_text = col1.empty()

    # Animate text
    def write_text(empty,
                   move_text: str,
                   talk_text: str,
                   move_text_time: float,
                   talk_text_time: float):
        animate_text(empty, move_text, time_per_sentence=move_text_time)
        sleep(2)
        animate_text(
            empty,
            talk_text,
            time_per_sentence=talk_text_time
        )
        sleep(2)
        empty.empty()

    for skill in player.skills.get_all():
        col1.button(
            skill.name.replace("_", " ").replace("DAMAGE BUFF", "DAMAGE x2"),
            key=skill.name,
            disabled=dissable_skill(skill),
            on_click=skill_click,
            args=(skill,))

    # KILL MONSTER button
    if st.sidebar.button("KILL MONSTER", disabled=dissable_button(), on_click=skill_click):
        player.entity.attack(monster, 1000)
        st.rerun()

    # KILL PLAYER button
    if st.sidebar.button("KILL PLAYER", disabled=dissable_button(), on_click=skill_click):
        monster.attack(player.entity, 1000)
        st.rerun()

    if sess["do_skill"] is not None:
        player_move_amount = player.make_move(sess["do_skill"], monster)

        # Animate player text
        if sess["do_skill"] == MoveType.ATTACK:
            write_text(
                player_text,
                f"Dealt {player_move_amount} damage.",
                "\"Whatever it takes... Keep moving.\"", 1, 1.5
            )
        elif sess["do_skill"] == MoveType.DAMAGE_BUFF:
            write_text(
                player_text,
                f"Dealt {player_move_amount} damage.",
                "\"The strength for the mighty one.\"", 1, 1.5
            )
        elif sess["do_skill"] == MoveType.HEAL:
            write_text(
                player_text,
                f"You used heal... Your health has increased for {player_move_amount} health.",
                "\"There is something you need to do right?\"", 1, 1.5
            )
        elif sess["do_skill"] == MoveType.POISON:
            write_text(
                player_text,
                f"You used POISON... {monster.name} is poisoned for {player_move_amount} turns.",
                "\"A gradual decay... The inevitable plight of mortal\"", 1.5, 1.5
            )
        elif sess["do_skill"] == MoveType.LIFE_STEAL:
            write_text(
                player_text,
                f"You used LIFE STEAL... You stole enemy health for {player_move_amount} health.",
                "\"A valuable source of life... Don't let anyone take it from you\"", 1.5, 1.5
            )
        elif sess["do_skill"] == MoveType.STUN:
            write_text(
                player_text,
                f"You used STUN... {monster.name} is stunned for 1 round",
                "\"A little rest won't hurt.\"", 1, 1
            )

        # Update player chart
        update_player_status_chart()
        sess["do_skill"] = None

    if (player.is_stun() or sess["press_hit_skill"]) and monster.is_alive():
        monster.tick()

    # Monster display
    if monster.name in boss_list:
        col2.title(f":red[{monster.name}]")
    else:
        col2.title(f":blue[{monster.name}]")

    def update_monster_status_chart():
        mon_hp = {
            'Status': ['HP'],
            'Amount': [monster.stats.health.get()]
        }

        d_mon_hp = pd.DataFrame(mon_hp)
        mon_chart = alt.Chart(d_mon_hp).mark_bar().encode(
            x=alt.X("Amount", scale=alt.Scale(
                domain=[0, monster.stats.max_health.get()])),
            y="Status"
        ).properties(height=105, width=500)
        col2.altair_chart(mon_chart)

    update_monster_status_chart()
    col2.image(monster.image, width=650)
    mon_text = col2.empty()

    # Monster make move
    if (player.is_stun() or sess["press_hit_skill"]) and player.is_alive():
        if monster.is_stun():
            # Animate text
            write_text(mon_text, f"{monster.name} is STUNNED.",
                       monster.text.get("got_attack"), 1, 1.5)

            time.sleep(3)
            sess["press_hit_skill"] = False
            sess["pass_mon_turn"] = True
            st.rerun()

        # If monster is not stunned and alive
        elif monster.is_alive():
            mon_move = monster.random_move()
            mon_move_amount = monster.make_move(mon_move, player.entity)

            move_text = "Something went wrong!"
            monster_text = monster.text.get(f"do_{mon_move.value}")

            # Animate text
            if mon_move == MoveType.ATTACK:
                move_text = f"{monster.name} ATTACKED you for {mon_move_amount} damage."
            elif mon_move == MoveType.DAMAGE_BUFF:
                move_text = f"{monster.name} ATTCKED using 2x DAMAGE for {mon_move_amount} damage."
            elif mon_move == MoveType.HEAL:
                move_text = f"{monster.name} used HEAL and recovered {mon_move_amount} health."
            elif mon_move == MoveType.POISON:
                move_text = f"{monster.name} used POISON. "
                move_text += f"YOU are poisoned for {mon_move_amount} turns."
            elif mon_move == MoveType.LIFE_STEAL:
                move_text = f"{monster.name} used LIFE STEAL. It stole {mon_move_amount} health."
            elif mon_move == MoveType.STUN:
                move_text = f"{monster.name} used STUN. YOU will are stunned for 1 turn"
            elif mon_move == MoveType.MANA_DRAIN:
                move_text = f"{monster.name} drained YOUR MANA for {mon_move_amount} mana."

            write_text(mon_text, move_text, monster_text, 1, 1.5)

            time.sleep(1.5)
            sess["press_hit_skill"] = False
            sess["pass_mon_turn"] = True
            st.rerun()

    # if monster is not alive
    if (not monster.is_alive()) or (not player.is_alive()):
        if col1.button("NEXT"):
            sess["press_hit_skill"] = False
            sess["room"] += 1
            # Temp fix, unknown bug caused by very competent frontend
            if monster.name in sess["all_mon_list"]:
                sess["all_mon_list"].remove(monster.name)

            del st.session_state["monster"]

            if (sess["room"] in [13]) or not player.is_alive():
                change_page("end")
            elif sess["room"] in [3, 5, 7, 9, 11]:
                change_page("buff")
            st.rerun()


def buff():  # pylint: disable=too-many-statements
    if sess["game"] is None:
        raise RuntimeError("Game object is not initialized.")

    game: Game = sess["game"]
    player = game.player

    st.set_page_config(layout="centered")
    load_remove_css()

    sess.nset("choose", 0)
    sess.nset("anable_confirm", False)
    sess.nset("confirm", False)

    max_hp = player.stats.max_health.get()
    max_mana = player.stats.max_mana.get()
    atk = player.stats.damage.get()

    col1, col2 = st.columns([0.7, 0.3], gap="large")
    col1.title(":blue[Choose Your BUFF]")

    def write_buff(hp, mana, atk):
        col2.title(" ")

        status = {'Status': ['HP', "MANA", "ATK"],
                  'Amount': [hp, mana, atk]}
        d_hp = pd.DataFrame(status)
        my_chart = alt.Chart(d_hp).mark_bar().encode(
            x="Status",
            y=alt.X("Amount", scale=alt.Scale(domain=[0, 150]))
        ).properties(width=200)

        col2.altair_chart(my_chart)
        col2.subheader(":blue[Chosen Status]")

        col2.write(f"HP: {hp}")
        col2.write(f"MANA: {mana}")
        col2.write(f"ATK: {atk}")

    if col1.button("+10 MAX HP", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = 1
        sess["anable_confirm"] = True
        write_buff(max_hp+10, max_mana, atk)
    if col1.button("+10 MAX MANA", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = 2
        sess["anable_confirm"] = True
        write_buff(max_hp, max_mana+10, atk)
    if col1.button("+5 ATK", disabled=sess["confirm"], use_container_width=True):
        sess["choose"] = 3
        sess["anable_confirm"] = True
        write_buff(max_hp, max_mana, atk+5)

    if col1.button("CONFIRM", disabled=not sess["anable_confirm"] or sess["confirm"]):
        sess["confirm"] = True
        st.rerun()

    if sess["confirm"]:
        if sess["choose"] == 1:
            player.stats.max_health.increase(10)
            player.stats.health.increase(10)
            sess["choose"] = 0
        elif sess["choose"] == 2:
            player.stats.max_mana.increase(10)
            player.stats.mana.increase(10)
            sess["choose"] = 0

        elif sess["choose"] == 3:
            player.stats.damage.increase(5)
            sess["choose"] = 0

        write_buff(
            player.stats.max_health.get(),
            player.stats.max_mana.get(),
            player.stats.damage.get()
        )

        if col1.button("NEXT"):
            sess["room"] += 1
            del st.session_state["choose"]
            del st.session_state["confirm"]
            del st.session_state["anable_confirm"]
            change_page("fight")
            st.rerun()


def end():
    if sess["game"] is None:
        raise RuntimeError("Game object is not initialized.")

    game: Game = sess["game"]
    player = game.player

    st.set_page_config(layout="centered")
    load_remove_css()

    _, col2, _ = st.columns(3)

    if player.is_alive():
        col2.markdown(
            "<h1 style='text-align: center; color: blue;'>VICTORY</h1>", unsafe_allow_html=True
        )
    else:
        col2.markdown(
            "<h1 style='text-align: center; color: blue;'>LOSE</h1>", unsafe_allow_html=True
        )

    if col2.button("HOME PAGE", use_container_width=True):
        st.session_state.clear()
        change_page("main_page")
        st.rerun()


pages = {
    "main_page": main_page,
    "create_account_page": create_account_page,
    "create_password_page": create_password_page,
    "create_account": create_account,
    "login_page": login_page,
    "login": login,
    "choosing_status": choosing_status,
    "fight": fight,
    "buff": buff,
    "end": end
}


pages[st.session_state.page]()
