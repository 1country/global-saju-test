import streamlit as st
import streamlit.components.v1 as components
from utils import verify_license_flexible, calculate_day_gan

# 1. 페이지 설정
st.set_page_config(page_title="2026 Forecast", page_icon="🔮", layout="wide")

# 🔑 [통일된 비밀번호]
UNLOCK_CODE = "MASTER2026"

# 2. 스타일 설정
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.0em; font-weight: bold; color: #1e293b; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Home" if lang=="en" else "👈 홈으로 돌아가기")

if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

txt = {
    "ko": {"title": "🔮 2026년 신년 운세", "lock": "🔒 유료 서비스 ($10)", "label": "이메일 또는 키 입력", "btn": "확인", "res": "운세 분석 결과"},
    "en": {"title": "🔮 2026 Forecast", "lock": "🔒 Premium Service ($10)", "label": "Enter Email or Key", "btn": "Unlock", "res": "Analysis Result"}
}
t = txt[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)

# 잠금 로직
if "unlocked_2026" not in st.session_state: st.session_state["unlocked_2026"] = False

if not st.session_state["unlocked_2026"]:
    with st.container(border=True):
        st.write(t['lock'])
        key = st.text_input(t['label'], type="password")
        if st.button(t['btn']):
            if key == UNLOCK_CODE: # 마스터키 체크
                st.session_state["unlocked_2026"] = True
                st.rerun()
            is_valid, msg = verify_license_flexible(key, "2026_forecast")
            if is_valid:
                st.session_state["unlocked_2026"] = True
                st.rerun()
            else:
                st.error(msg)
    st.stop()

# 결과 화면
st.divider()
day_info = calculate_day_gan(st.session_state["birth_date"])
st.success(f"Welcome, {st.session_state['user_name']}!")
st.info(f"Your Element: {day_info['element']}")
st.write("2026년은 병오년(붉은 말의 해)입니다. 당신의 기운과 2026년의 조화를 분석합니다...")

st.markdown("---")
components.html("""<script>function printPage(){window.parent.print();}</script>
<button onclick="printPage()" style='padding:10px; cursor:pointer;'>🖨️ Print Report</button>""", height=50)
