import streamlit as st
from datetime import datetime, time

# --- 1. 페이지 설정 (디자인) ---
st.set_page_config(page_title="The Element: Discover Your True Self", page_icon="🔮", layout="wide")

# 스타일 꾸미기 (CSS)
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em; 
        color: #2C3E50; 
        text-align: center; 
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2em; 
        color: #7F8C8D; 
        text-align: center; 
        margin-top: 0;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .highlight {
        color: #E67E22;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 사주 데이터 (DB) ---
def get_element_from_year(year):
    last_digit = int(str(year)[-1])
    
    elements = {
        4: {
            "type": "Wood (Gap) 🌲",
            "archetype": "The Pioneer (The Giant Tree)",
            "desc": "You possess the energy of a giant pine tree stretching towards the sky. You are straightforward, honest, and have a strong drive for growth. Once you set a goal, you move forward without looking back. Your leadership is natural, and you prefer to lead rather than follow.",
            "keywords": "Growth, Leadership, Resilience"
        },
        5: {
            "type": "Wood (Eul) 🌿",
            "archetype": "The Survivor (The Wild Flower)",
            "desc": "You are like a resilient vine or a flower that blooms even in harsh conditions. Unlike the rigid tree, you are flexible and adaptable. You have strong survival instincts and a practical mind. Your gentle exterior hides a very strong inner will.",
            "keywords": "Flexibility, Adaptability, Networking"
        },
        6: {
            "type": "Fire (Byeong) ☀️",
            "archetype": "The Visionary (The Sun)",
            "desc": "You are the sun shining brightly in the sky. You are passionate, open-hearted, and full of energy. You can't hide your emotions, and you love being the center of attention. Your presence naturally warms the people around you and gives them hope.",
            "keywords": "Passion, Public Speaking, Optimism"
        },
        7: {
            "type": "Fire (Jeong) 🔥",
            "archetype": "The Mentor (The Candle Light)",
            "desc": "You are like a warm candlelight or a guiding star in the dark. Unlike the sun, your fire is focused and intense. You are sensitive, artistic, and have a sacrificing spirit to help others. You have great intuition and can see things others miss.",
            "keywords": "Insight, Sacrifice, Detail-oriented"
        },
        8: {
            "type": "Earth (Mu) ⛰️",
            "archetype": "The Guardian (The Big Mountain)",
            "desc": "You stand tall like a majestic mountain range. You are trustworthy, steady, and hold a heavy sense of responsibility. People naturally rely on you. You may seem slow to move, but once you make a decision, your persistence is unstoppable.",
            "keywords": "Trust, Stability, Persistence"
        },
        9: {
            "type": "Earth (Gi) 🪴",
            "archetype": "The Nurturer (The Fertile Soil)",
            "desc": "You are the fertile soil of a garden that grows crops. You are practical, nurturing, and multifaceted. You know how to embrace others and help them succeed. You are very realistic and have a talent for managing assets.",
            "keywords": "Nurturing, Practicality, Multitasking"
        },
        0: {
            "type": "Metal (Gyeong) ⚔️",
            "archetype": "The Warrior (The Iron Sword)",
            "desc": "You are like raw steel or a powerful sword. You value loyalty and justice above all else. You are decisive and have strong executive power. You dislike ambiguity and prefer clear-cut conclusions. You are a natural reformer.",
            "keywords": "Justice, Loyalty, Decisiveness"
        },
        1: {
            "type": "Metal (Sin) 💎",
            "archetype": "The Perfectionist (The Gemstone)",
            "desc": "You are a polished jewel, shining and sharp. You have a delicate and sensitive aesthetic sense. You aim for perfection in everything you do. Although you look elegant on the outside, you have a very sharp mind and high standards.",
            "keywords": "Elegance, Precision, Self-Respect"
        },
        2: {
            "type": "Water (Im) 🌊",
            "archetype": "The Strategist (The Ocean)",
            "desc": "You are the wide ocean. Wise, adaptable, and you have deep thoughts. Like the ocean, your depth is hard to measure. You flow around obstacles rather than fighting them, but your power can be overwhelming when unleashed.",
            "keywords": "Wisdom, Flow, Big Picture"
        },
        3: {
            "type": "Water (Gye) 🌧️",
            "archetype": "The Thinker (The Gentle Rain)",
            "desc": "You are the spring rain that nurtures life. You are quiet, intelligent, and very logical. You prefer planning behind the scenes rather than standing in front. You are sensitive to others' feelings and have a kind, introverted nature.",
            "keywords": "Intelligence, Empathy, Planning"
        }
    }
    return elements[last_digit]

# --- 3. 화면 구성 (UI) ---
st.markdown("<h1 class='main-title'>The Element: Discover Your True Self</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Ancient Asian Wisdom Decoded for the Modern Soul</p>", unsafe_allow_html=True)

st.write("---")

# [변경 포인트] 3개의 컬럼으로 나누어 시간 입력 추가
col1, col2, col3 = st.columns([1.2, 1, 1]) 

with col1:
    name = st.text_input("Name", placeholder="Enter your name")
with col2:
    birth_date = st.date_input("Birth Date", min_value=datetime(1920, 1, 1), value=datetime(1990, 1, 1))
with col3:
    # 시간 입력 추가 (기본값 없음, 라벨에 Optional 표시)
    birth_time = st.time_input("Birth Time (Optional)", value=None)

# 버튼 클릭 처리
if st.button("🔮 Analyze My Soul Energy", use_container_width=True):
    if name:
        year = birth_date.year
        result = get_element_from_year(year)
        
        # 시간이 입력되었는지 확인 (나중에 정밀 분석에 사용)
        time_str = birth_time.strftime("%H:%M") if birth_time else "Unknown"
        
        st.write("") 
        
        # HTML 코드 (공백 제거 버전)
        html_content = f"""
<div class="result-box">
<h2 style="color: #333; margin-bottom: 10px;">Hello, {name}.</h2>
<p style="font-size: 1.1em; color: #555;">Born in <b>{year}</b> (Time: {time_str}), your core energy is:</p>
<h1 style="color: #4A90E2; font-size: 2.5em; margin: 20px 0;">{result['type']}</h1>
<p style="font-size: 1.3em; font-weight: bold;">Archetype: <span class="highlight">{result['archetype']}</span></p>
<hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
<p style="line-height: 1.6; font-size: 1.1em; color: #444;">{result['desc']}</p>
<div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-top: 20px;">
<span style="font-weight: bold; color: #555;">🔑 Your Key Traits:</span><br>
{result['keywords']}
</div>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)
        
    else:
        st.warning("Please enter your name to begin the journey.")

st.write("---")
st.markdown("<div style='text-align: center; color: #888;'>© 2025 The Element Lab. <br> This analysis is based on the 'Year Pillar' of the Four Pillars of Destiny.</div>", unsafe_allow_html=True)
