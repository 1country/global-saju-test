import streamlit as st
import streamlit.components.v1 as components
from utils import calculate_day_gan, verify_license_flexible

st.set_page_config(page_title="2026 Forecast", page_icon="🔮", layout="wide")

# 1. 배경 그래픽 (페이지마다 넣어줘야 유지됩니다)
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 사이드바 (언어 설정 유지)
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["한국어", "English"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Return to Home" if lang=="en" else "👈 홈으로 돌아가기")

# 3. 홈 정보 확인
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home and enter your details first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

# 4. 메인 내용
CURRENT_PRODUCT_ID = "2026_forecast"
ALL_ACCESS_ID = "all_access_pass"

st.title(f"🔮 2026 {'Forecast' if lang=='en' else '신년 운세'}")
name = st.session_state["user_name"]
st.write(f"Analyzing for **{name}**...")

# 잠금 확인
if "unlocked_2026" not in st.session_state: st.session_state["unlocked_2026"] = False

if not st.session_state["unlocked_2026"]:
    st.info("🔒 Premium Content ($10)")
    key = st.text_input("License Key", type="password")
    
    if st.button("Unlock"):
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        if is_valid:
            st.session_state["unlocked_2026"] = True
            st.rerun()
        else:
            st.error(msg)
else:
    # 잠금 해제됨
    st.success("✅ Unlocked!")
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    st.markdown(f"### 🌊 {day_info[lang]}")
    st.write("당신의 2026년은 기회가 가득할 것입니다. (여기에 상세 데이터가 나옵니다)")
    
    # 인쇄 버튼
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Result</button>""", height=50)
