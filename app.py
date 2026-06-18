import streamlit as st
import random

# =====================================

# 기본 설정

# =====================================

st.set_page_config(
page_title="로그라이크 RPG",
page_icon="⚔️",
layout="wide"
)

# =====================================

# 희귀도

# =====================================

RARITIES = {
"일반": 50,
"고급": 30,
"희귀": 15,
"영웅": 4,
"전설": 1
}

RARITY_MULTIPLIER = {
"일반": 1,
"고급": 1.5,
"희귀": 2,
"영웅": 3,
"전설": 5
}

# =====================================

# 장비 이름

# =====================================

WEAPON_NAMES = [
"철검",
"강철검",
"기사검",
"마검",
"용검"
]

ARMOR_NAMES = [
"천갑옷",
"가죽갑옷",
"철갑옷",
"기사갑옷",
"용비늘갑옷"
]

# =====================================

# 스킬 이름

# =====================================

SKILL_NAMES = {
"warrior": "검술 수련",
"tank": "강인함",
"assassin": "치명타 전문가",
"alchemy": "연금술"
}

# =====================================

# 로그

# =====================================

def add_log(text):
st.session_state.logs.append(text)

# =====================================

# 희귀도 선택

# =====================================

def get_rarity():

```
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
```

# =====================================

# 무기 생성

# =====================================

def generate_weapon(round_num):

```
rarity = get_rarity()

atk = int(
    (
        random.randint(3, 8)
        + round_num
    )
    * RARITY_MULTIPLIER[rarity]
)

return {
    "type": "weapon",
    "name": f"{rarity} {random.choice(WEAPON_NAMES)}",
    "atk": atk,
    "rarity": rarity
}
```

# =====================================

# 방어구 생성

# =====================================

def generate_armor(round_num):

```
rarity = get_rarity()

defense = int(
    (
        random.randint(2, 6)
        + round_num // 2
    )
    * RARITY_MULTIPLIER[rarity]
)

return {
    "type": "armor",
    "name": f"{rarity} {random.choice(ARMOR_NAMES)}",
    "def": defense,
    "rarity": rarity
}
```

# =====================================

# 몬스터 생성

# =====================================

def create_monster():

```
round_num = st.session_state.round

boss = round_num % 5 == 0

if boss:

    hp = 200 + round_num * 25
    atk = 15 + round_num

    name = random.choice([
        "독거미 여왕",
        "화염 드래곤",
        "얼음 군주"
    ])

else:

    hp = 80 + round_num * 12
    atk = 8 + round_num

    name = random.choice([
        "고블린",
        "오크",
        "스켈레톤",
        "늑대"
    ])

st.session_state.monster = {
    "name": name,
    "boss": boss,
    "hp": hp,
    "max_hp": hp,
    "atk": atk
}
```

# =====================================

# 게임 초기화

# =====================================

def init_game():

```
best_round = st.session_state.get(
    "best_round",
    1
)

st.session_state.best_round = best_round

st.session_state.round = 1

st.session_state.gold = 0

st.session_state.level = 1
st.session_state.exp = 0
st.session_state.exp_needed = 100

st.session_state.skill_points = 0

st.session_state.skills = {
    "warrior": 0,
    "tank": 0,
    "assassin": 0,
    "alchemy": 0
}

st.session_state.player = {
    "hp": 100,
    "max_hp": 100,
    "atk": 10,
    "crit": 0.10
}

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

st.session_state.heals = 3
st.session_state.power_attacks = 2

st.session_state.effects = []

st.session_state.logs = []

st.session_state.drop_item = None

st.session_state.reward_pending = False

st.session_state.shop_open = False

st.session_state.game_over = False

create_monster()

add_log("🎮 게임 시작!")
```

# =====================================

# 첫 실행

# =====================================

if "player" not in st.session_state:
init_game()
