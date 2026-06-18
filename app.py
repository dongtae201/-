import streamlit as st
import random

st.set_page_config(
    page_title="로그라이크 RPG",
    page_icon="⚔️",
    layout="wide"
)

# =====================
# 세션 초기화
# =====================

def init_game():

    st.session_state.round = 1
    st.session_state.gold = 0

    st.session_state.player_hp = 100
    st.session_state.player_max_hp = 100
    st.session_state.player_atk = 10

    st.session_state.monster = {
        "name": "고블린",
        "hp": 50,
        "max_hp": 50,
        "atk": 5
    }

    st.session_state.logs = [
        "🎮 게임 시작!"
    ]

# 최초 실행

if "round" not in st.session_state:
    init_game()

# =====================
# 로그 함수
# =====================

def add_log(text):
    st.session_state.logs.append(text)

# =====================
# 몬스터 생성
# =====================

def create_monster():

    round_num = st.session_state.round

    boss = round_num % 5 == 0

    if boss:

        hp = 150 + round_num * 20
        atk = 15 + round_num

        name = random.choice([
            "독거미 여왕",
            "화염 드래곤",
            "얼음 군주"
        ])

    else:

        hp = 50 + round_num * 10
        atk = 5 + round_num

        name = random.choice([
            "고블린",
            "오크",
            "스켈레톤",
            "늑대"
        ])

    st.session_state.monster = {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "atk": atk,
        "boss": boss
    }

# =====================
# 공격
# =====================

def attack():

    damage = random.randint(
        st.session_state.player_atk,
        st.session_state.player_atk + 5
    )

    st.session_state.monster["hp"] -= damage

    add_log(
        f"⚔️ 공격! {damage} 피해"
    )

    if st.session_state.monster["hp"] <= 0:

        add_log(
            f"👹 {st.session_state.monster['name']} 처치!"
        )

        st.session_state.round += 1

        create_monster()

        return

    monster_damage = random.randint(
        st.session_state.monster["atk"],
        st.session_state.monster["atk"] + 3
    )

    st.session_state.player_hp -= monster_damage

    add_log(
        f"💥 몬스터 공격! {monster_damage} 피해"
    )

# =====================
# 화면
# =====================

st.title("⚔️ 로그라이크 RPG")

st.subheader(
    f"🏹 Round {st.session_state.round}"
)

col1, col2 = st.columns(2)

with col1:

    st.write("### 플레이어")

    st.progress(
        st.session_state.player_hp /
        st.session_state.player_max_hp
    )

    st.write(
        f"HP: {st.session_state.player_hp}/{st.session_state.player_max_hp}"
    )

with col2:

    monster = st.session_state.monster

    st.write(
        f"### 👹 {monster['name']}"
    )

    st.progress(
        monster["hp"] /
        monster["max_hp"]
    )

    st.write(
        f"HP: {monster['hp']}/{monster['max_hp']}"
    )

if st.button("⚔️ 공격"):

    attack()

    st.rerun()

st.divider()

st.subheader("📜 전투 로그")

for log in reversed(st.session_state.logs[-10:]):
    st.write(log)

if st.button("🔄 새 게임"):
    init_game()
    st.rerun()
