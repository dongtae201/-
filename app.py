import streamlit as st
import random

st.set_page_config(
page_title="로그라이크 RPG",
page_icon="⚔️",
layout="wide"
)

# =========================

# 희귀도

# =========================

RARITY_WEIGHTS = {
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

WEAPONS = [
"철검",
"장검",
"대검",
"마검",
"용검",
"암흑검"
]

ARMORS = [
"가죽갑옷",
"철갑옷",
"기사갑옷",
"마갑",
"용비늘갑옷"
]

# =========================

# 스킬트리

# =========================

SKILL_NAMES = {
"warrior": "검술 수련",
"tank": "강인함",
"assassin": "치명타 전문가",
"alchemy": "연금술"
}

# =========================

# 유틸

# =========================

def log(text):
st.session_state.logs.append(text)

def choose_rarity():

```
roll = random.uniform(0, 100)

current = 0

for rarity, chance in RARITY_WEIGHTS.items():

    current += chance

    if roll <= current:
        return rarity

return "일반"
```

# =========================

# 장비 생성

# =========================

def generate_weapon(round_num):

```
rarity = choose_rarity()

atk = int(
    random.randint(3, 8)
    * RARITY_MULTIPLIER[rarity]
    + round_num
)

return {
    "type": "weapon",
    "name": f"{rarity} {random.choice(WEAPONS)}",
    "atk": atk,
    "rarity": rarity
}
```

def generate_armor(round_num):

```
rarity = choose_rarity()

defense = int(
    random.randint(2, 6)
    * RARITY_MULTIPLIER[rarity]
    + round_num // 2
)

return {
    "type": "armor",
    "name": f"{rarity} {random.choice(ARMORS)}",
    "def": defense,
    "rarity": rarity
}
```

# =========================

# 몬스터 생성

# =========================

def create_monster():

```
round_num = st.session_state.round

boss = round_num % 5 == 0

if boss:

    monster = {
        "name": random.choice([
            "독거미 여왕",
            "화염 드래곤",
            "얼음 군주"
        ]),
        "boss": True,
        "hp": 200 + round_num * 25,
        "atk": 18 + round_num
    }

else:

    monster = {
        "name": random.choice([
            "고블린",
            "오크",
            "스켈레톤",
            "늑대"
        ]),
        "boss": False,
        "hp": 80 + round_num * 15,
        "atk": 8 + round_num
    }

st.session_state.monster = monster
```

# =========================

# 초기화

# =========================

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

st.session_state.effects = []

st.session_state.logs = []

st.session_state.shop_open = False

st.session_state.reward_pending = False

st.session_state.game_over = False

create_monster()

log("🎮 게임 시작!")
```

# =========================

# 첫 실행

# =========================

if "player" not in st.session_state:
init_game()
# =========================

# 경험치 / 레벨업

# =========================

def gain_exp(amount):

```
st.session_state.exp += amount

while st.session_state.exp >= st.session_state.exp_needed:

    st.session_state.exp -= st.session_state.exp_needed

    st.session_state.level += 1

    st.session_state.skill_points += 1

    st.session_state.player["max_hp"] += 20

    st.session_state.player["hp"] = (
        st.session_state.player["max_hp"]
    )

    st.session_state.player["atk"] += 2

    st.session_state.exp_needed = int(
        st.session_state.exp_needed * 1.3
    )

    log(
        f"⭐ 레벨업! Lv.{st.session_state.level}"
    )
```

# =========================

# 스킬 계산

# =========================

def get_attack_bonus():

```
return (
    st.session_state.skills["warrior"] * 2
)
```

def get_hp_bonus():

```
return (
    st.session_state.skills["tank"] * 15
)
```

def get_crit_bonus():

```
return (
    st.session_state.skills["assassin"] * 0.03
)
```

def get_heal_bonus():

```
return (
    st.session_state.skills["alchemy"] * 0.20
)
```

# =========================

# 상태이상 부여

# =========================

def add_effect(name, turns):

```
st.session_state.effects.append({
    "name": name,
    "turns": turns
})

log(f"💀 상태이상: {name}")
```

# =========================

# 상태이상 처리

# =========================

def process_effects():

```
if len(st.session_state.effects) == 0:
    return False

frozen = False

remaining = []

for effect in st.session_state.effects:

    if effect["name"] == "독":

        st.session_state.player["hp"] -= 5

        log("☠️ 독 피해 5")

    elif effect["name"] == "화상":

        st.session_state.player["hp"] -= 3

        log("🔥 화상 피해 3")

    elif effect["name"] == "빙결":

        frozen = True

        log("❄️ 빙결! 행동 불가")

    effect["turns"] -= 1

    if effect["turns"] > 0:
        remaining.append(effect)

st.session_state.effects = remaining

if st.session_state.player["hp"] <= 0:

    st.session_state.player["hp"] = 0

    game_over()

return frozen
```

# =========================

# 게임오버

# =========================

def game_over():

```
st.session_state.game_over = True

if (
    st.session_state.round
    >
    st.session_state.best_round
):
    st.session_state.best_round = (
        st.session_state.round
    )

log("💀 게임 오버")
```

# =========================

# 몬스터 공격

# =========================

def monster_attack():

```
if st.session_state.game_over:
    return

dodge = random.random()

if dodge < 0.05:

    log("💨 회피 성공!")

    return

monster = st.session_state.monster

damage = random.randint(
    monster["atk"] - 3,
    monster["atk"] + 3
)

damage -= st.session_state.armor["def"]

damage = max(1, damage)

st.session_state.player["hp"] -= damage

log(
    f"👹 {monster['name']} 공격 "
    f"{damage} 피해"
)

# 보스 특수효과

if monster["boss"]:

    chance = random.random()

    if (
        monster["name"]
        ==
        "독거미 여왕"
        and chance < 0.25
    ):
        add_effect("독", 3)

    elif (
        monster["name"]
        ==
        "화염 드래곤"
        and chance < 0.25
    ):
        add_effect("화상", 3)

    elif (
        monster["name"]
        ==
        "얼음 군주"
        and chance < 0.20
    ):
        add_effect("빙결", 1)

if st.session_state.player["hp"] <= 0:

    st.session_state.player["hp"] = 0

    game_over()
```

# =========================

# 플레이어 공격력

# =========================

def get_total_attack():

```
return (
    st.session_state.player["atk"]
    +
    st.session_state.weapon["atk"]
    +
    get_attack_bonus()
)
```

# =========================

# 일반 공격

# =========================

def attack():

```
if st.session_state.game_over:
    return

frozen = process_effects()

if frozen:
    monster_attack()
    return

monster = st.session_state.monster

damage = random.randint(
    get_total_attack(),
    get_total_attack() + 10
)

crit_rate = (
    st.session_state.player["crit"]
    +
    get_crit_bonus()
)

if random.random() < crit_rate:

    damage *= 2

    log("💥 치명타!")

monster["hp"] -= damage

log(
    f"⚔️ 공격! {damage} 피해"
)

if monster["hp"] <= 0:

    monster["hp"] = 0

    monster_defeated()

    return

monster_attack()
```

# =========================

# 강공격

# =========================

def power_attack():

```
if st.session_state.game_over:
    return

if (
    st.session_state.get(
        "power_attacks",
        2
    )
    <= 0
):
    log("❌ 강공격 없음")
    return

st.session_state.power_attacks = (
    st.session_state.get(
        "power_attacks",
        2
    )
    - 1
)

frozen = process_effects()

if frozen:
    monster_attack()
    return

damage = random.randint(
    get_total_attack() + 15,
    get_total_attack() + 30
)

st.session_state.monster["hp"] -= damage

log(
    f"🔥 강공격! {damage} 피해"
)

if (
    st.session_state.monster["hp"]
    <= 0
):

    st.session_state.monster["hp"] = 0

    monster_defeated()

    return

monster_attack()
```

# =========================

# 회복

# =========================

def heal_player():

```
if st.session_state.game_over:
    return

if (
    st.session_state.get(
        "heals",
        3
    )
    <= 0
):
    log("❌ 회복약 없음")
    return

st.session_state.heals = (
    st.session_state.get(
        "heals",
        3
    )
    - 1
)

heal = random.randint(20, 35)

heal = int(
    heal
    *
    (
        1
        +
        get_heal_bonus()
    )
)

st.session_state.player["hp"] = min(
    st.session_state.player["max_hp"]
    +
    get_hp_bonus(),
    st.session_state.player["hp"]
    +
    heal
)

log(
    f"💚 회복 {heal}"
)

monster_attack()
```
# =========================

# 드롭 아이템 저장

# =========================

if "drop_item" not in st.session_state:
st.session_state.drop_item = None

# =========================

# 장비 장착

# =========================

def equip_drop():

```
item = st.session_state.drop_item

if item is None:
    return

if item["type"] == "weapon":

    st.session_state.weapon = item

    log(
        f"⚔️ 장착: {item['name']}"
    )

elif item["type"] == "armor":

    st.session_state.armor = item

    log(
        f"🛡️ 장착: {item['name']}"
    )

st.session_state.drop_item = None
```

# =========================

# 드롭 생성

# =========================

def generate_drop():

```
roll = random.random()

if roll < 0.50:

    return generate_weapon(
        st.session_state.round
    )

elif roll < 0.90:

    return generate_armor(
        st.session_state.round
    )

return None
```

# =========================

# 보스 보상 대기

# =========================

def boss_reward():

```
st.session_state.reward_pending = True
```

# =========================

# 몬스터 처치

# =========================

def monster_defeated():

```
monster = st.session_state.monster

round_num = st.session_state.round

if monster["boss"]:

    exp_reward = (
        150
        +
        round_num * 5
    )

    gold_reward = (
        100
        +
        round_num * 10
    )

else:

    exp_reward = (
        40
        +
        round_num * 3
    )

    gold_reward = (
        15
        +
        round_num
    )

gain_exp(exp_reward)

st.session_state.gold += gold_reward

log(
    f"⭐ EXP +{exp_reward}"
)

log(
    f"💰 골드 +{gold_reward}"
)

# 아이템 드롭

if random.random() < 0.35:

    item = generate_drop()

    if item:

        st.session_state.drop_item = item

        log(
            f"🎁 드롭: "
            f"{item['name']}"
        )

# 보스

if monster["boss"]:

    log(
        "🏆 보스 처치!"
    )

    boss_reward()

    return

# 일반 몬스터

st.session_state.round += 1

# 10라운드 상점

if (
    st.session_state.round % 10
    == 0
):

    st.session_state.shop_open = True

create_monster()
```

# =========================

# 보스 보상 적용

# =========================

def apply_boss_reward(reward):

```
if reward == "공격력 +5":

    st.session_state.player["atk"] += 5

    log(
        "⚔️ 공격력 +5"
    )

elif reward == "최대체력 +30":

    st.session_state.player["max_hp"] += 30

    st.session_state.player["hp"] += 30

    log(
        "❤️ 최대체력 +30"
    )

elif reward == "회복약 +2":

    st.session_state.heals = (
        st.session_state.get(
            "heals",
            3
        )
        \+ 2
    )

    log(
        "💚 회복약 +2"
    )

elif reward == "강공격 +2":

    st.session_state.power_attacks = (
        st.session_state.get(
            "power_attacks",
            2
        )
        \+ 2
    )

    log(
        "🔥 강공격 +2"
    )

elif reward == "전설 장비":

    if random.random() < 0.5:

        item = {
            "type": "weapon",
            "name": "전설 용검",
            "atk": 50,
            "rarity": "전설"
        }

    else:

        item = {
            "type": "armor",
            "name": "전설 용갑",
            "def": 25,
            "rarity": "전설"
        }

    st.session_state.drop_item = item

    log(
        f"✨ {item['name']} 획득"
    )

st.session_state.reward_pending = False

st.session_state.round += 1

if (
    st.session_state.round % 10
    == 0
):
    st.session_state.shop_open = True

create_monster()
```

# =========================

# 상점 데이터

# =========================

SHOP_ITEMS = [

```
{
    "name": "회복약 +3",
    "price": 50
},

{
    "name": "강공격 +2",
    "price": 80
},

{
    "name": "공격력 +3",
    "price": 100
},

{
    "name": "최대체력 +20",
    "price": 120
}
```

]

# =========================

# 구매

# =========================

def buy_item(item):

```
if (
    st.session_state.gold
    <
    item["price"]
):
    log(
        "❌ 골드 부족"
    )
    return

st.session_state.gold -= item["price"]

if item["name"] == "회복약 +3":

    st.session_state.heals = (
        st.session_state.get(
            "heals",
            3
        )
        \+ 3
    )

elif item["name"] == "강공격 +2":

    st.session_state.power_attacks = (
        st.session_state.get(
            "power_attacks",
            2
        )
        \+ 2
    )

elif item["name"] == "공격력 +3":

    st.session_state.player["atk"] += 3

elif item["name"] == "최대체력 +20":

    st.session_state.player["max_hp"] += 20

    st.session_state.player["hp"] += 20

log(
    f"🛒 구매: {item['name']}"
)
```

# =========================

# 상점 종료

# =========================

def leave_shop():

```
st.session_state.shop_open = False

create_monster()

log(
    "🏪 상점 종료"
)
```
# =========================

# UI

# =========================

st.title("⚔️ 로그라이크 RPG")

st.write(
f"🏆 최고 기록: Round {st.session_state.best_round}"
)

# -----------------

# 플레이어 정보

# -----------------

left, right = st.columns(2)

with left:

```
st.subheader("🧙 플레이어")

max_hp = (
    st.session_state.player["max_hp"]
    +
    get_hp_bonus()
)

hp_ratio = (
    st.session_state.player["hp"]
    / max_hp
)

hp_ratio = max(
    0,
    min(1, hp_ratio)
)

st.progress(hp_ratio)

st.write(
    f"HP: "
    f"{st.session_state.player['hp']}"
    f"/{max_hp}"
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
    f"💰 {st.session_state.gold} Gold"
)

st.write(
    f"⚔️ "
    f"{st.session_state.weapon['name']}"
)

st.write(
    f"🛡️ "
    f"{st.session_state.armor['name']}"
)

st.write(
    f"공격력 "
    f"{get_total_attack()}"
)
```

with right:

```
monster = st.session_state.monster

st.subheader(
    f"👹 {monster['name']}"
)

monster_ratio = (
    monster["hp"]
    /
    monster["hp"]
    if monster["hp"] > 0
    else 0
)

st.progress(
    max(
        0,
        min(
            1,
            monster["hp"]
            /
            (
                200
                +
                st.session_state.round
                * 25
            )
        )
    )
)

st.write(
    f"HP: {monster['hp']}"
)

if monster["boss"]:
    st.error("보스 몬스터")
```

st.divider()

# -----------------

# 라운드

# -----------------

st.header(
f"🏹 Round {st.session_state.round}"
)

# -----------------

# 상태이상

# -----------------

if st.session_state.effects:

```
st.subheader("상태이상")

for effect in st.session_state.effects:

    st.write(
        f"{effect['name']} "
        f"({effect['turns']}턴)"
    )
```

# -----------------

# 드롭 아이템

# -----------------

if st.session_state.drop_item:

```
item = st.session_state.drop_item

st.success(
    f"🎁 획득: {item['name']}"
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
    equip_drop()
    st.rerun()
```

st.divider()

# -----------------

# 보스 보상

# -----------------

if st.session_state.reward_pending:

```
st.subheader("🏆 보스 보상")

reward = st.radio(
    "보상 선택",
    [
        "공격력 +5",
        "최대체력 +30",
        "회복약 +2",
        "강공격 +2",
        "전설 장비"
    ]
)

if st.button(
    "보상 획득"
):

    apply_boss_reward(
        reward
    )

    st.rerun()
```

# -----------------

# 상점

# -----------------

elif st.session_state.shop_open:

```
st.subheader("🏪 상점")

for item in SHOP_ITEMS:

    c1, c2 = st.columns([4,1])

    with c1:

        st.write(
            f"{item['name']}"
            f" ({item['price']}G)"
        )

    with c2:

        if st.button(
            "구매",
            key=item["name"]
        ):
            buy_item(item)
            st.rerun()

if st.button(
    "상점 나가기"
):
    leave_shop()
    st.rerun()
```

# -----------------

# 전투

# -----------------

elif not st.session_state.game_over:

```
c1, c2, c3 = st.columns(3)

with c1:

    st.button(
        "⚔️ 공격",
        on_click=attack,
        use_container_width=True
    )

with c2:

    st.button(
        f"🔥 강공격 "
        f"({st.session_state.get('power_attacks',2)})",
        on_click=power_attack,
        use_container_width=True
    )

with c3:

    st.button(
        f"💚 회복 "
        f"({st.session_state.get('heals',3)})",
        on_click=heal_player,
        use_container_width=True
    )
```

st.divider()

# -----------------

# 스킬트리

# -----------------

st.subheader("🌳 스킬 트리")

st.write(
f"스킬 포인트: "
f"{st.session_state.skill_points}"
)

skill_cols = st.columns(4)

skill_keys = [
"warrior",
"tank",
"assassin",
"alchemy"
]

for idx, key in enumerate(skill_keys):

```
with skill_cols[idx]:

    st.write(
        SKILL_NAMES[key]
    )

    st.write(
        f"Lv."
        f"{st.session_state.skills[key]}"
    )

    if st.button(
        "+",
        key=f"skill_{key}"
    ):

        if (
            st.session_state.skill_points
            > 0
        ):

            st.session_state.skills[key] += 1

            st.session_state.skill_points -= 1

            st.rerun()
```

st.divider()

# -----------------

# 로그

# -----------------

st.subheader("📜 전투 로그")

for msg in reversed(
st.session_state.logs[-25:]
):

```
st.write(msg)
```

st.divider()

# -----------------

# 게임오버

# -----------------

if st.session_state.game_over:

```
st.error(
    "💀 게임 오버"
)
```

# -----------------

# 새 게임

# -----------------

if st.button(
"🔄 새 게임"
):

```
init_game()

st.rerun()
```
