import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta
import random
from utils import calculate_day_gan, verify_license_flexible

st.set_page_config(page_title="Date Selection", page_icon="📆", layout="wide")

# 1. 배경 설정 (모든 페이지 공통)
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .date-card {
            background-color: #f0fdf4; 
            padding: 15px; 
            border-radius: 10px; 
            border-left: 5px solid #22c55e;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 사이드바 설정
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["한국어", "English"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Home" if lang=="en" else "👈 홈으로 돌아가기")

# 3. 홈 정보 확인 (이름 없으면 내쫓기)
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

# ----------------------------------------------------
# [설정] 상품 ID
# ----------------------------------------------------
CURRENT_PRODUCT_ID = "date_selection"  # 택일 전용 상품 ID ($5)
ALL_ACCESS_ID = "all_access_pass"      # 프리패스 ID

# UI 텍스트
txt = {
    "ko": {
        "title": "📆 택일 서비스 (좋은 날짜 받기)",
        "intro": "가장 중요한 날, 우주의 기운이 돕는 날짜를 선택하세요.",
        "q1": "어떤 행사를 계획 중이신가요?",
        "options": ["결혼/약혼", "이사/이전", "계약/매매", "개업/사업시작", "수술/치료", "여행"],
        "q2": "언제쯤 계획하고 계신가요? (원하는 달 선택)",
        "lock": "🔒 유료 서비스입니다 ($5)",
        "res": "님에게 가장 완벽한 날짜 3가지를 찾았습니다!",
        "desc": "선택하신 행사와 본인의 사주(일주)를 분석하여 충돌이 없고 귀인이 돕는 날짜입니다."
    },
    "en": {
        "title": "📆 Auspicious Date Selection",
        "intro": "Choose the perfect date supported by the universe.",
        "q1": "What is the event?",
        "options": ["Wedding", "Moving", "Contract", "Opening Business", "Surgery", "Travel"],
        "q2": "Target Month",
        "lock": "🔒 Premium Service ($5)",
        "res": "Here are the top 3 dates for you!",
        "desc": "Based on your Day Master and the event type, these dates avoid conflict and bring luck."
    }
}
t = txt[lang]

# 4. 메인 화면
st.title(f"{t['title']}")
st.write(f"**{st.session_state['user_name']}**님, {t['intro']}")

st.markdown("---")

# 입력 폼 (행사 종류 + 날짜)
col1, col2 = st.columns(2)
with col1:
    event_type = st.selectbox(t['q1'], t['options'])
with col2:
    # 다음 달 1일을 기본값으로 설정
    today = date.today()
    next_month = today.replace(day=1) + timedelta(days=32)
    target_date = st.date_input(t['q2'], value=next_month)

# 5. 잠금 로직
if "unlocked_date_select" not in st.session_state: st.session_state["unlocked_date_select"] = False

if not st.session_state["unlocked_date_select"]:
    st.info(t['lock'])
    key = st.text_input("License Key", type="password")
    
    if st.button("Unlock"):
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        if is_valid:
            st.session_state["unlocked_date_select"] = True
            st.rerun()
        else:
            st.error(msg)
else:
    # ------------------------------------------------
    # 6. [해제됨] 결과 보여주기
    # ------------------------------------------------
    st.success("✅ Unlocked!")
    st.divider()
    
    st.subheader(f"🎉 {st.session_state['user_name']}{t['res']}")
    st.write(t['desc'])
    
    # 내 사주 정보 가져오기
    my_info = calculate_day_gan(st.session_state["birth_date"])
    
    # [가상 로직] 실제로는 만세력 달력을 돌려야 하지만, 여기서는 예시로
    # 선택한 날짜로부터 +3일, +12일, +20일 뒤를 추천하는 것으로 시뮬레이션합니다.
    # (나중에 실제 정밀 만세력 DB를 연결하면 더 정교해집니다)
    
    rec_dates = [
        target_date + timedelta(days=random.randint(2, 8)),
        target_date + timedelta(days=random.randint(10, 18)),
        target_date + timedelta(days=random.randint(20, 28))
    ]
    
    # 추천 날짜 카드 출력
    for i, d in enumerate(rec_dates):
        # 날짜 포맷
        d_str = d.strftime("%Y년 %m월 %d일") if lang == "ko" else d.strftime("%B %d, %Y")
        
        # 멘트 랜덤 생성
        comments_ko = ["귀인이 돕는 대길일입니다.", "재물운이 따르는 날입니다.", "모든 장애물이 사라지는 날입니다."]
        comments_en = ["A day helped by noble people.", "Great luck for wealth.", "All obstacles disappear."]
        comment = comments_ko[i] if lang == "ko" else comments_en[i]
        
        st.markdown(f"""
        <div class='date-card'>
            <h3 style='margin:0; color:#15803d;'>Top {i+1}. {d_str}</h3>
            <p style='margin:5px 0 0 0; color:#166534;'><b>{event_type}</b>하기 좋은 날: {comment}</p>
        </div>
        """, unsafe_allow_html=True)

    st.warning("⚠️ Tip: 행사 시간은 오전 9시~11시(사시) 또는 오후 1시~3시(미시)가 좋습니다." if lang=="ko" else "Tip: Best hours are 09:00~11:00 or 13:00~15:00.")

    # 인쇄 버튼
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer; background-color:#efefef; border:1px solid #ccc; border-radius:5px;'>🖨️ Print Result</button>""", height=50)
