import streamlit as st
import streamlit.components.v1 as components
from utils import verify_license_flexible, calculate_day_gan

st.set_page_config(page_title="Business Compatibility", page_icon="🤝", layout="wide")

# 배경 설정
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .report-card {
            background-color: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# 1. 사이드바
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Home" if lang=="en" else "👈 홈으로 돌아가기")

# 2. 홈 정보 확인
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

# 텍스트 사전
txt = {
    "ko": {
        "title": "🤝 비즈니스 파트너 궁합",
        "intro": "직장 상사, 동업자, 혹은 거래처 직원과의 합을 분석합니다.",
        "p_label": "상대방 이름 (직장 상사, 동업자 등)",
        "d_label": "상대방 생년월일",
        "lock": "🔒 유료 서비스입니다 ($10)",
        "btn_unlock": "잠금 해제",
        "res_title": "님의 비즈니스 시너지 분석",
        "res_sub": "두 사람의 기운이 합쳐졌을 때 일어나는 화학작용을 분석합니다.",
        "card1": "💼 업무 스타일 및 성향 차이",
        "card2": "⚖️ 리더십과 팔로워십 (누가 주도해야 하나?)",
        "card3": "💰 재물 합 (동업 성과)",
        "advice": "💡 처세술 조언"
    },
    "en": {
        "title": "🤝 Business & Partner Synergy",
        "intro": "Analyze compatibility with your boss, co-founder, or colleague.",
        "p_label": "Partner's Name (Boss, Colleague, etc.)",
        "d_label": "Partner's Date of Birth",
        "lock": "🔒 Premium Service ($10)",
        "btn_unlock": "Unlock",
        "res_title": "'s Professional Synergy",
        "res_sub": "Analyzing the chemical reaction when your energies combine.",
        "card1": "💼 Working Style & Personality",
        "card2": "⚖️ Leadership Dynamics",
        "card3": "💰 Financial Synergy (For Partnership)",
        "advice": "💡 Strategic Advice"
    }
}
t = txt[lang]

# 3. 메인 화면
st.title(t['title'])
st.write(t['intro'])
st.divider()

col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input(t['p_label'], value="Partner")
with col2:
    p_date = st.date_input(t['d_label'])

# 4. 잠금 로직
CURRENT_PRODUCT_ID = "business_compatibility" 
ALL_ACCESS_ID = "all_access_pass"

if "unlocked_biz" not in st.session_state: st.session_state["unlocked_biz"] = False

if not st.session_state["unlocked_biz"]:
    st.info(t['lock'])
    key = st.text_input("License Key", type="password")
    
    if st.button(t['btn_unlock']):
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        if is_valid:
            st.session_state["unlocked_biz"] = True
            st.rerun()
        else:
            st.error(msg)
else:
    # --- 결과 화면 ---
    st.success("✅ Analysis Unlocked!")
    st.markdown("---")
    
    my_info = calculate_day_gan(st.session_state["birth_date"])
    p_info = calculate_day_gan(p_date)
    
    st.header(f"{st.session_state['user_name']} & {p_name}")
    st.subheader(t['res_title'])
    st.write(t['res_sub'])
    
    # 1. 업무 스타일
    st.markdown(f"#### {t['card1']}")
    st.info(f"**Me ({my_info['element']}) vs Partner ({p_info['element']})**")
    st.write("서로의 일 처리 방식이 다를 수 있습니다. (상세 분석 내용이 들어갑니다...)")
    
    # 2. 리더십
    st.markdown(f"#### {t['card2']}")
    st.warning("수평적인 관계보다는 한쪽이 명확하게 리드하는 것이 효율적일 수 있습니다.")
    
    # 3. 재물합
    st.markdown(f"#### {t['card3']}")
    st.success("두 분이 함께하면 재물운이 상승하는 시너지가 있습니다.")
    
    # 4. 조언
    st.markdown(f"#### {t['advice']}")
    advice_ko = "상대방은 명분을 중요시하므로, 논리적으로 설득하기보다 체면을 세워주는 것이 유리합니다."
    advice_en = "Your partner values reputation. Giving them credit publicly works better than logical arguments."
    st.write(advice_ko if lang == "ko" else advice_en)

    # 인쇄 버튼
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Report</button>""", height=50)
