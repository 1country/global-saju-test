import streamlit as st
import random

# 1. 화면 설정
st.set_page_config(page_title="Global Destiny Reader", page_icon="🔮")

# 2. 제목과 설명
st.title("🔮 Destiny Reader for Global Nomads")
st.subheader("Discover your inner element based on Asian Wisdom.")
st.write("---") # 가로줄 긋기

# 3. 사용자 입력 (사주 정보)
col1, col2 = st.columns(2) # 화면을 2단으로 나누기
with col1:
    name = st.text_input("Your English Name", placeholder="e.g. Jessica")
with col2:
    birth_date = st.date_input("Your Birth Date")

# 4. 버튼 클릭 시 결과 (데모 버전)
if st.button("Reveal My Destiny"):
    if name:
        # 지금은 랜덤이지만, 나중에 선생님의 '진짜 만세력 로직'이 들어갈 자리입니다.
        elements = ["Giant Tree (Gap-Mok)", "Candle Fire (Jeong-Hwa)", "Ocean Water (Im-Su)", "Golden Sword (Gyeong-Geum)"]
        my_element = random.choice(elements)
        
        st.success(f"Hello, {name}!")
        st.markdown(f"### 🌟 Your Core Element is: **{my_element}**")
        st.info(f"Analysis for {birth_date}: You are born with a special energy. This site is currently in Beta version.")
    else:
        st.error("Please enter your name first!")
