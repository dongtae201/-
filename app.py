import streamlit as st
import random

# =====================================
# 설정
# =====================================

st.set_page_config(
    page_title="로그라이크 RPG",
    page_icon="⚔️",
    layout="wide"
)

# =====================================
# 데이터
# =====================================

RARITY_MULTI = {
    "일반": 1,
    "고급": 1.5,
    "희귀": 2,
    "영웅": 3,
    "전설": 5
}

WEAPONS = [
    "철검",
    "강철검",
    "기사검",
    "마검",
    "용검"
]

ARMORS = [
    "천갑옷",
    "가죽갑옷",
    "철갑옷",
    "기사갑옷",
    "용비늘갑옷"
]

# =====================================
# 로그
# =====================================

def add_log(text):

    st.session_state.logs.append(text)

# =====================================
# 희귀도
# =====================================

def get_rarity():

    roll = random.randint(1, 100)

    if roll <= 50:
        return "일반"

    elif roll <= 80:
        return "고급"

    elif roll <= 95:
        return "희귀"

    elif roll <= 99:
        return "영웅"

    return "전설"

# =====================================
# 무기 생성
# =====================================

def generate_weapon(round_num):

    rarity = get_rarity()

    atk = int(
        (
            round_num +
            random.randint(3, 8)
        )
        *
        RARITY_MULTI[rarity]
    )

    return {
        "type": "weapon",
        "name": f"{rarity} {random.choice(WEAPONS)}",
        "atk": atk,
        "rarity": rarity
    }

# =====================================
# 방어구 생성
# =====================================

def generate_armor(round_num):

    rarity = get_rarity()

    defense = int(
        (
            round_num +
            random.randint(2, 6)
        )
        *
        RARITY_MULTI[rarity]
    )

    return {
        "type": "armor",
        "name": f"{rarity} {random.choice(ARMORS)}",
        "def": defense,
        "rarity": rarity
    }

# =====================================
# 드롭 생성
# =====================================

def generate_drop():

    if random.random() < 0.5:

        return generate_weapon(
            st.session_state.round
        )

    return generate_armor(
        st.session_state.round
    )

# =====================================
# 몬스터 생성
# =====================================

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

# =====================================
# 경험치
# =====================================

def gain_exp(amount):

    st.session_state.exp += amount

    while (
        st.session_state.exp
        >=
        st.session_state.exp_needed
    ):

        st.session_state.exp -= (
            st.session_state.exp_needed
        )

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

# =====================================
# 게임 초기화
# =====================================

def init_game():

    st.session_state.round = 1

    st.session_state.gold = 0

    st.session_state.level = 1

    st.session_state.exp = 0

    st.session_state.exp_needed = 50

    st.session_state.player_hp = 100

    st.session_state.player_max_hp = 100

    st.session_state.player_atk = 10

    st.session_state.weapon = {
        "name": "맨손",
        "atk": 0,
        "rarity": "-"
    }

    st.session_state.armor = {
        "name": "천옷",
        "def": 0,
        "rarity": "-"
    }

    st.session_state.drop_item = None

    st.session_state.logs = [
        "🎮 게임 시작!"
    ]

    create_monster()

# =====================================
# 첫 실행
# =====================================

if "round" not in st.session_state:

    init_game()# =====================================
# 몬스터 처치
# =====================================

def monster_defeated():

    boss = st.session_state.monster["boss"]

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

    # 아이템 드롭

    if random.random() < 0.4:

        st.session_state.drop_item = (
            generate_drop()
        )

        add_log(
            "🎁 아이템 드롭!"
        )

    st.session_state.round += 1

    create_monster()

# =====================================
# 공격
# =====================================

def attack():

    total_atk = (
        st.session_state.player_atk
        +
        st.session_state.weapon["atk"]
    )

    damage = random.randint(
        total_atk,
        total_atk + 5
    )

    st.session_state.monster["hp"] -= damage

    add_log(
        f"⚔️ 공격! {damage} 피해"
    )

    # 몬스터 사망

    if st.session_state.monster["hp"] <= 0:

        add_log(
            f"👹 "
            f"{st.session_state.monster['name']} "
            f"처치!"
        )

        monster_defeated()

        return

    # 반격

    monster_damage = random.randint(
        st.session_state.monster["atk"],
        st.session_state.monster["atk"] + 3
    )

    monster_damage -= (
        st.session_state.armor["def"]
    )

    monster_damage = max(
        1,
        monster_damage
    )

    st.session_state.player_hp -= (
        monster_damage
    )

    add_log(
        f"💥 몬스터 공격! "
        f"{monster_damage} 피해"
    )

    if st.session_state.player_hp <= 0:

        st.session_state.player_hp = 0

        add_log(
            "💀 게임 오버"
        )

# =====================================
# 장착
# =====================================

def equip_item():

    item = st.session_state.drop_item

    if item is None:
        return

    if item["type"] == "weapon":

        st.session_state.weapon = item

    else:

        st.session_state.armor = item

    add_log(
        f"✨ 장착: {item['name']}"
    )

    st.session_state.drop_item = None

# =====================================
# UI 상단
# =====================================

st.title("⚔️ 로그라이크 RPG")

st.subheader(
    f"🏹 Round {st.session_state.round}"
)

col1, col2 = st.columns(2)

# =====================================
# 플레이어
# =====================================

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
        f"⚔️ 무기: "
        f"{st.session_state.weapon['name']}"
    )

    st.write(
        f"🛡️ 방어구: "
        f"{st.session_state.armor['name']}"
    )

# =====================================
# 몬스터
# =====================================

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
        max(
            0,
            min(1, monster_ratio)
        )
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

# =====================================
# 드롭 아이템
# =====================================

if st.session_state.drop_item:

    item = st.session_state.drop_item

    st.success(
        f"🎁 {item['name']}"
    )

    if item["type"] == "weapon":

        st.write(
            f"공격력 +{item['atk']}"
        )

    else:

        st.write(
            f"방어력 +{item['def']}"
        )

    if st.button(
        "장착하기"
    ):

        equip_item()

        st.rerun()# =====================================
# 전투 버튼
# =====================================

st.divider()

if st.session_state.player_hp > 0:

    if st.button(
        "⚔️ 공격",
        use_container_width=True
    ):

        attack()

        st.rerun()

else:

    st.error(
        "💀 게임 오버"
    )

# =====================================
# 로그
# =====================================

st.divider()

st.subheader(
    "📜 전투 로그"
)

for log in reversed(
    st.session_state.logs[-20:]
):

    st.write(log)

# =====================================
# 현재 능력치
# =====================================

st.divider()

st.subheader(
    "📊 능력치"
)

weapon_atk = (
    st.session_state.weapon["atk"]
)

armor_def = (
    st.session_state.armor["def"]
)

total_atk = (
    st.session_state.player_atk
    +
    weapon_atk
)

st.write(
    f"기본 공격력: "
    f"{st.session_state.player_atk}"
)

st.write(
    f"무기 공격력: "
    f"{weapon_atk}"
)

st.write(
    f"총 공격력: "
    f"{total_atk}"
)

st.write(
    f"방어력: "
    f"{armor_def}"
)

# =====================================
# 최고 기록
# =====================================

if "best_round" not in st.session_state:

    st.session_state.best_round = 1

if (
    st.session_state.round
    >
    st.session_state.best_round
):

    st.session_state.best_round = (
        st.session_state.round
    )

st.divider()

st.write(
    f"🏆 최고 기록: "
    f"Round {st.session_state.best_round}"
)

# =====================================
# 새 게임
# =====================================

st.divider()

if st.button(
    "🔄 새 게임",
    use_container_width=True
):

    best_round = (
        st.session_state.best_round
    )

    init_game()

    st.session_state.best_round = (
        best_round
    )

    st.rerun()
