import streamlit as st
from datetime import datetime

# --- 1. 페이지 설정 (디자인) ---
st.set_page_config(page_title="The Element", page_icon="🌌")

# 스타일 꾸미기 (CSS)
st.markdown("""
<style>
    .main-title {font-size: 3em; color: #4A90E2; text-align: center; margin-bottom: 0;}
    .sub-title {font-size: 1.2em; color: #555; text-align: center; margin-top: 0;}
    .result-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4A90E2;}
</style>
""", unsafe_allow_html=True)

# --- 2. 진짜 사주 계산 로직 (만세력 엔진) ---
def get_element_from_year(year):
    # 천간(Heavenly Stems) 계산: 연도 끝자리에 따라 결정됨
    # 4:갑(Wood), 5:을(Wood), 6:병(Fire), 7:정(Fire), 8:무(Earth), 9:기(Earth), 0:경(Metal), 1:신(Metal), 2:임(Water), 3:계(Water)
    
    last_digit = int(str(year)[-1])
    
    elements = {
        4: {"name": "Green Wood (Gap)", "type": "Wood 🌲", "desc": "You are like a giant tree. Straight, honest, and upward-growing."},
        5: {"name": "Flower Wood (Eul)", "type": "Wood 🌿", "desc": "You are like a vine or flower. Flexible, resilient, and survive anywhere."},
        6: {"name": "Burning Sun (Byeong)", "type": "Fire ☀️", "desc": "You are the sun. Passionate, fair, and you love to be the center of attention."},
        7: {"name": "Candle Light (Jeong)", "type": "Fire 🔥", "desc": "You are a warm candle. Sensitive, artistic, and you guide people in the dark."},
        8: {"name": "Great Mountain (Mu)", "type": "Earth ⛰️", "desc": "You are a massive mountain. Trustworthy, steady, and stubborn."},
        9: {"name": "Garden Soil (Gi)", "type": "Earth 🪴", "desc": "You are fertile soil. Practical, nurturing, and you grow talents in others."},
        0: {"name": "Iron Sword (Gyeong)", "type": "Metal ⚔️", "desc": "You are raw steel. Strong, decisive, and loyal."},
        1: {"name": "Gold Jewelry (Sin)", "type": "Metal 💎", "desc": "You are a polished gem. Sharp, delicate, and you value perfection."},
        2: {"name": "Ocean Water (Im)", "type": "Water 🌊", "desc": "You are the wide ocean. Wise, adaptable, and you have deep thoughts."},
        3: {"name": "Rain Water (Gye)", "type": "Water 🌧️", "desc": "You are gentle rain. Quiet, intelligent, and you gently change the world."}
    }
    return elements[last_digit]

# --- 3. 화면 구성 (UI) ---
st.markdown("<h1 class='main-title'>The Element</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Discover the ancient energy code hidden in your birth date.</p>", unsafe_allow_html=True)

st.write("---")

# 입력창
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", placeholder="Your Name")
with col2:
    # 1900년~현재까지 선택 가능
    birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1))

# 버튼 및 결과 처리
if st.button("Analyze My Energy 🔮", use_container_width=True):
    if name:
        # 로직 실행
        year = birth_date.year
        result = get_element_from_year(year)
        
        # 결과 화면 출력
        st.write("") # 여백
        st.success(f"Analysis Complete for {name}")
        
        # 결과 카드
        st.markdown(f"""
        <div class="result-box">
            <h3>🌟 Your Root Energy is: {result['type']}</h3>
            <p><strong>Archetype:</strong> {result['name']}</p>
            <p>{result['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 This result is based on your 'Birth Year Stem' (The Foundation of Life). Full analysis coming soon!")
        
    else:
        st.error("Please enter your name to start.")

# 푸터
st.write("---")
st.caption("© 2025 The Element Lab. Based on Asian Metaphysics.")
