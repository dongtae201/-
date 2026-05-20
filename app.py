import streamlit as st
import random

# ---------------------------
# 초기 상태 설정
# ---------------------------
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "monster_hp" not in st.session_state:
    st.session_state.monster_hp = 100
if "turn" not in st.session_state:
    st.session_state.turn = "player"  # player 차례

st.title("간단 턴제 게임")

st.write(f"**플레이어 HP:** {st.session_state.player_hp}")
st.write(f"**몬스터 HP:** {st.session_state.monster_hp}")

# ---------------------------
# 턴제 로직
# ---------------------------
def player_attack():
    damage = random.randint(10, 20)
    st.session_state.monster_hp -= damage
    st.session_state.turn = "monster"
    st.write(f"플레이어가 몬스터에게 {damage} 피해를 주었습니다!")

def monster_attack():
    damage = random.randint(5, 15)
    st.session_state.player_hp -= damage
    st.session_state.turn = "player"
    st.write(f"몬스터가 플레이어에게 {damage} 피해를 주었습니다!")

# ---------------------------
# 버튼으로 턴 진행
# ---------------------------
if st.session_state.player_hp <= 0:
    st.write("💀 플레이어 패배!")
elif st.session_state.monster_hp <= 0:
    st.write("🏆 플레이어 승리!")
else:
    if st.session_state.turn == "player":
        if st.button("공격!"):
            player_attack()
            st.experimental_rerun()  # 화면 갱신
    else:
        monster_attack()
        st.experimental_rerun()  # 화면 갱신

# ---------------------------
# 게임 초기화 버튼
# ---------------------------
if st.button("게임 초기화"):
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 100
    st.session_state.turn = "player"
    st.experimental_rerun()
