import streamlit as st
import random

st.set_page_config(
    page_title="로그라이크 턴제 RPG",
    page_icon="⚔️",
    layout="centered"
)

# -------------------
# 초기화
# -------------------

def init_game():

    best_round = st.session_state.get("best_round", 1)

    st.session_state.player_hp = 100
    st.session_state.max_hp = 100

    st.session_state.level = 1
    st.session_state.exp = 0
    st.session_state.exp_needed = 100

    st.session_state.attack_bonus = 0

    st.session_state.heal_count = 3
    st.session_state.power_attack_count = 2

    st.session_state.round = 1

    st.session_state.logs = []
    st.session_state.game_over = False

    st.session_state.reward_pending = False

    st.session_state.best_round = best_round

    create_monster()

    add_log("🎮 게임 시작")


def add_log(text):
    st.session_state.logs.append(text)


def is_boss():
    return st.session_state.round % 5 == 0


# -------------------
# 몬스터 생성
# -------------------

def create_monster():

    round_num = st.session_state.round

    if is_boss():

        st.session_state.monster_name = "👹 보스"

        hp = 180 + round_num * 20

        attack = 18 + round_num

    else:

        st.session_state.monster_name = "👾 몬스터"

        hp = 80 + round_num * 15

        attack = 10 + round_num // 2

    st.session_state.monster_hp = hp
    st.session_state.monster_max_hp = hp
    st.session_state.monster_attack = attack


# -------------------
# 레벨업
# -------------------

def gain_exp(amount):

    st.session_state.exp += amount

    while st.session_state.exp >= st.session_state.exp_needed:

        st.session_state.exp -= st.session_state.exp_needed

        st.session_state.level += 1

        st.session_state.max_hp += 20

        st.session_state.player_hp = st.session_state.max_hp

        st.session_state.attack_bonus += 2

        st.session_state.exp_needed = int(
            st.session_state.exp_needed * 1.3
        )

        add_log(
            f"⭐ 레벨업! Lv.{st.session_state.level}"
        )


# -------------------
# 게임 종료
# -------------------

def game_over():

    st.session_state.game_over = True

    if st.session_state.round > st.session_state.best_round:
        st.session_state.best_round = st.session_state.round

    add_log("💀 게임 오버")


# -------------------
# 몬스터 턴
# -------------------

def monster_turn():

    if st.session_state.game_over:
        return

    if random.random() < 0.05:
        add_log("💨 회피 성공!")
        return

    damage = random.randint(
        st.session_state.monster_attack - 4,
        st.session_state.monster_attack + 4
    )

    st.session_state.player_hp -= damage

    add_log(
        f"{st.session_state.monster_name} 공격! {damage} 피해"
    )

    if st.session_state.player_hp <= 0:
        st.session_state.player_hp = 0
        game_over()


# -------------------
# 몬스터 처치
# -------------------

def monster_defeated():

    round_num = st.session_state.round

    if is_boss():

        gain_exp(150)

        add_log("🏆 보스 처치!")

        st.session_state.reward_pending = True

    else:

        gain_exp(50)

        heal = 15

        st.session_state.player_hp = min(
            st.session_state.max_hp,
            st.session_state.player_hp + heal
        )

        add_log(f"💚 전투 후 회복 +{heal}")

        st.session_state.round += 1

        create_monster()


# -------------------
# 플레이어 공격
# -------------------

def attack():

    if st.session_state.game_over:
        return

    if st.session_state.reward_pending:
        return

    damage = random.randint(
        10,
        20
    ) + st.session_state.attack_bonus

    if random.random() < 0.10:
        damage *= 2
        add_log("💥 치명타!")

    st.session_state.monster_hp -= damage

    add_log(f"⚔️ 공격! {damage} 피해")

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

        return

    monster_turn()


# -------------------
# 강공격
# -------------------

def power_attack():

    if st.session_state.game_over:
        return

    if st.session_state.reward_pending:
        return

    if st.session_state.power_attack_count <= 0:
        add_log("❌ 강공격 없음")
        return

    st.session_state.power_attack_count -= 1

    damage = random.randint(
        25,
        45
    ) + st.session_state.attack_bonus

    st.session_state.monster_hp -= damage

    add_log(f"🔥 강공격! {damage} 피해")

    if st.session_state.monster_hp <= 0:

        st.session_state.monster_hp = 0

        monster_defeated()

        return

    monster_turn()


# -------------------
# 회복
# -------------------

def heal():

    if st.session_state.game_over:
        return

    if st.session_state.reward_pending:
        return

    if st.session_state.heal_count <= 0:
        add_log("❌ 회복약 없음")
        return

    st.session_state.heal_count -= 1

    amount = random.randint(20, 35)

    st.session_state.player_hp = min(
        st.session_state.max_hp,
        st.session_state.player_hp + amount
    )

    add_log(f"💚 회복 +{amount}")

    monster_turn()


# -------------------
# 시작
# -------------------

if "player_hp" not in st.session_state:
    init_game()

# -------------------
# UI
# -------------------

st.title("⚔️ 로그라이크 턴제 RPG")

st.write(
    f"🏆 최고 기록: Round {st.session_state.best_round}"
)

st.header(f"Round {st.session_state.round}")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🧙 플레이어")

    st.progress(
        st.session_state.player_hp /
        st.session_state.max_hp
    )

    st.write(
        f"HP {st.session_state.player_hp}/"
        f"{st.session_state.max_hp}"
    )

    st.write(
        f"Lv.{st.session_state.level}"
    )

    st.write(
        f"EXP {st.session_state.exp}/"
        f"{st.session_state.exp_needed}"
    )

    st.write(
        f"공격력 보너스 +{st.session_state.attack_bonus}"
    )

with col2:

    st.subheader(
        st.session_state.monster_name
    )

    st.progress(
        max(st.session_state.monster_hp, 0)
        /
        st.session_state.monster_max_hp
    )

    st.write(
        f"HP {max(st.session_state.monster_hp,0)}/"
        f"{st.session_state.monster_max_hp}"
    )

st.divider()

# -------------------
# 보상 선택
# -------------------

if st.session_state.reward_pending:

    st.success("🎁 보스 보상 선택")

    reward = st.radio(
        "보상",
        [
            "공격력 +5",
            "최대체력 +30",
            "회복약 +2",
            "강공격 +2"
        ]
    )

    if st.button("보상 획득"):

        if reward == "공격력 +5":
            st.session_state.attack_bonus += 5

        elif reward == "최대체력 +30":
            st.session_state.max_hp += 30
            st.session_state.player_hp += 30

        elif reward == "회복약 +2":
            st.session_state.heal_count += 2

        elif reward == "강공격 +2":
            st.session_state.power_attack_count += 2

        add_log(f"🎁 획득: {reward}")

        st.session_state.reward_pending = False

        st.session_state.round += 1

        create_monster()

        st.rerun()

else:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button(
            "⚔️ 공격",
            use_container_width=True,
            on_click=attack
        )

    with c2:
        st.button(
            f"🔥 강공격 ({st.session_state.power_attack_count})",
            use_container_width=True,
            on_click=power_attack
        )

    with c3:
        st.button(
            f"💚 회복 ({st.session_state.heal_count})",
            use_container_width=True,
            on_click=heal
        )

st.divider()

if st.session_state.game_over:
    st.error("게임 오버")

if st.button("🔄 새 게임"):
    init_game()
    st.rerun()

st.subheader("📜 전투 로그")

for log in reversed(st.session_state.logs[-20:]):
    st.write(log)
