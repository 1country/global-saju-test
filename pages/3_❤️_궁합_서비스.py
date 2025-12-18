import streamlit as st
import streamlit.components.v1 as components
from utils import verify_license_flexible

st.set_page_config(page_title="Compatibility", page_icon="❤️", layout="wide")

# 배경 설정
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
    </style>
""", unsafe_allow_html=True)

# 1. 사이드바 설정
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["한국어", "English"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Home" if lang=="en" else "👈 홈으로 돌아가기")

# 2. 홈 정보 확인
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

# 3. 메인 콘텐츠
CURRENT_PRODUCT_ID = "compatibility_check" # 궁합 전용 상품 ID
ALL_ACCESS_ID = "all_access_pass"

st.title(f"❤️ {'Relationship Compatibility' if lang=='en' else '궁합 분석 (Chemistry)'}")
name = st.session_state["user_name"]
st.write(f"Checking compatibility for **{name}**...")

# 상대방 정보 입력 (궁합이니까 상대방이 필요하죠!)
st.markdown("### " + ("Partner's Details" if lang=='en' else "상대방 정보 입력"))
col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input("Partner Name", "Partner")
with col2:
    p_date = st.date_input("Partner Birthday")

# 잠금 로직
if "unlocked_love" not in st.session_state: st.session_state["unlocked_love"] = False

if not st.session_state["unlocked_love"]:
    st.divider()
    st.info("🔒 Premium Content ($10)")
    key = st.text_input("License Key", type="password")
    
    if st.button("Unlock"):
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        if is_valid:
            st.session_state["unlocked_love"] = True
            st.rerun()
        else:
            st.error(msg)
else:
    st.success("✅ Unlocked!")
    st.markdown(f"### {name} ❤️ {p_name}")
    st.write("두 분의 궁합은 천생연분입니다! (상세 분석 내용...)")
    
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Result</button>""", height=50)
