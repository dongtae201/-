import streamlit as st
import random

# =====================
# 기본 설정
# =====================

st.set_page_config(
    page_title="로그라이크 RPG",
    page_icon="⚔️",
    layout="wide"
)

# =====================
# 게임 초기화
# =====================

def init_game():

    st.session_state.round = 1
    st.session_state.gold = 0

    st.session_state.level = 1
    st.session_state.exp = 0
    st.session_state.exp_needed = 50

    st.session_state.player_hp = 100
    st.session_state.player_max_hp = 100
    st.session_state.player_atk = 10

    st.session_state.logs = [
        "🎮 게임 시작!"
    ]

    create_monster()

# =====================
# 로그
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
# 경험치
# =====================

def gain_exp(amount):

    st.session_state.exp += amount

    while st.session_state.exp >= st.session_state.exp_needed:

        st.session_state.exp -= st.session_state.exp_needed

        st.session_state.level += 1

        st.session_state.exp_needed = int(
            st.session_state.exp_needed * 1.5
        )

        st.session_state.player_max_hp += 20
        st.session_state.player_hp = (
            st.session_state.player_max_hp
        )

        st.session_state.player_atk += 3

        add_log(
            f"⭐ 레벨업! Lv.{st.session_state.level}"
        )

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

    # 몬스터 처치

    if st.session_state.monster["hp"] <= 0:

        add_log(
            f"👹 {st.session_state.monster['name']} 처치!"
        )

        boss = st.session_state.monster.get(
            "boss",
            False
        )

        if boss:

            exp_reward = 50
            gold_reward = 100

        else:

            exp_reward = 20
            gold_reward = 15

        gain_exp(exp_reward)

        st.session_state.gold += gold_reward

        add_log(
            f"⭐ EXP +{exp_reward}"
        )

        add_log(
            f"💰 Gold +{gold_reward}"
        )

        st.session_state.round += 1

        create_monster()

        return

    # 몬스터 반격

    monster_damage = random.randint(
        st.session_state.monster["atk"],
        st.session_state.monster["atk"] + 3
    )

    st.session_state.player_hp -= monster_damage

    add_log(
        f"💥 몬스터 공격! {monster_damage} 피해"
    )

    if st.session_state.player_hp <= 0:

        st.session_state.player_hp = 0

        add_log("💀 게임 오버")

# =====================
# 최초 실행
# =====================

if "round" not in st.session_state:
    init_game()

# =====================
# 화면
# =====================

st.title("⚔️ 로그라이크 RPG")

st.subheader(
    f"🏹 Round {st.session_state.round}"
)

col1, col2 = st.columns(2)

# 플레이어

with col1:

    st.write("### 🧙 플레이어")

    hp_ratio = (
        st.session_state.player_hp
        /
        st.session_state.player_max_hp
    )

    st.progress(
        max(0, min(1, hp_ratio))
    )

    st.write(
        f"HP: "
        f"{st.session_state.player_hp}"
        f"/"
        f"{st.session_state.player_max_hp}"
    )

    st.write(
        f"Lv.{st.session_state.level}"
    )

    st.write(
        f"EXP "
        f"{st.session_state.exp}"
        f"/"
        f"{st.session_state.exp_needed}"
    )

    st.write(
        f"💰 Gold "
        f"{st.session_state.gold}"
    )

    st.write(
        f"⚔️ 공격력 "
        f"{st.session_state.player_atk}"
    )

# 몬스터

with col2:

    monster = st.session_state.monster

    st.write(
        f"### 👹 {monster['name']}"
    )

    monster_ratio = (
        monster["hp"]
        /
        monster["max_hp"]
    )

    st.progress(
        max(0, min(1, monster_ratio))
    )

    st.write(
        f"HP: "
        f"{monster['hp']}"
        f"/"
        f"{monster['max_hp']}"
    )

    if monster["boss"]:
        st.error(
            "👑 보스 몬스터"
        )

# =====================
# 전투
# =====================

if st.session_state.player_hp > 0:

    if st.button(
        "⚔️ 공격",
        use_container_width=True
    ):
        attack()
        st.rerun()

# =====================
# 로그
# =====================

st.divider()

st.subheader("📜 전투 로그")

for log in reversed(
    st.session_state.logs[-15:]
):
    st.write(log)

# =====================
# 새 게임
# =====================

st.divider()

if st.button(
    "🔄 새 게임",
    use_container_width=True
):
    init_game()
    st.rerun()
