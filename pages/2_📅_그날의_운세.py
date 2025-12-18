import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from utils import calculate_day_gan, verify_license_flexible

st.set_page_config(page_title="Specific Day Fortune", page_icon="📅", layout="wide")

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

# 1. 사이드바
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

# ----------------------------------------------------
# [설정] 상품 ID
# ----------------------------------------------------
CURRENT_PRODUCT_ID = "specific_day_forecast"  # 새 상품 ID ($3~$5 정도 추천)
ALL_ACCESS_ID = "all_access_pass"

# 텍스트
txt = {
    "ko": {
        "title": "📅 그날의 운세 (특정일 분석)",
        "intro": "중요한 약속이 있는 날, 면접일, 혹은 그냥 내일의 운세가 궁금하신가요?",
        "label": "궁금한 날짜를 선택하세요",
        "lock": "🔒 유료 서비스입니다 ($5)",
        "res": "의 그날 운세 분석",
        "my_energy": "나의 기운",
        "day_energy": "그날의 기운",
        "advice": "💡 그날의 조언"
    },
    "en": {
        "title": "📅 Specific Day Forecast",
        "intro": "Check your luck for a specific date (Interview, Date, or Tomorrow).",
        "label": "Select a Date",
        "lock": "🔒 Premium Service ($5)",
        "res": "'s Forecast",
        "my_energy": "My Energy",
        "day_energy": "Day's Energy",
        "advice": "💡 Advice"
    }
}
t = txt[lang]

# 3. 메인 화면
st.title(t['title'])
st.write(t['intro'])

# 날짜 선택기
target_date = st.date_input(t['label'], min_value=date.today())

# 4. 잠금 로직
if "unlocked_specific_day" not in st.session_state: st.session_state["unlocked_specific_day"] = False

if not st.session_state["unlocked_specific_day"]:
    st.divider()
    st.info(t['lock'])
    key = st.text_input("License Key", type="password")
    
    if st.button("Unlock"):
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        if is_valid:
            st.session_state["unlocked_specific_day"] = True
            st.rerun()
        else:
            st.error(msg)
else:
    # ------------------------------------------------
    # 5. [해제됨] 분석 결과
    # ------------------------------------------------
    st.success("✅ Unlocked!")
    st.divider()
    
    name = st.session_state["user_name"]
    
    # 1) 내 정보 & 그날 정보 계산
    my_info = calculate_day_gan(st.session_state["birth_date"])
    day_info = calculate_day_gan(target_date)
    
    my_elem = my_info['element'] # Wood, Fire...
    day_elem = day_info['element']
    
    st.subheader(f"{target_date} {t['res']}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"**{t['my_energy']}**")
        st.info(f"{my_info[lang]}")
    with c2:
        st.markdown(f"**VS**")
    with c3:
        st.markdown(f"**{t['day_energy']}**")
        st.warning(f"{day_info[lang]}")
        
    st.markdown("---")
    
    # 2) 간단한 상생상극 로직 (예시)
    # 실제로는 더 복잡하지만, 여기서는 오행 관계로 간단한 조언을 출력
    relations = {
        ("Wood", "Wood"): "친구를 만난 듯 편안하지만 경쟁이 있을 수 있습니다.",
        ("Wood", "Fire"): "당신의 능력을 마음껏 펼칠 수 있는 날입니다! (표현/활동)",
        ("Wood", "Earth"): "노력한 만큼 재물이 들어오는 날입니다. (결실)",
        ("Wood", "Metal"): "스트레스나 압박이 있을 수 있으니 언행을 조심하세요. (관제)",
        ("Wood", "Water"): "도움을 받고 아이디어가 샘솟는 날입니다. (충전)",
        
        ("Fire", "Wood"): "귀인의 도움을 받아 일이 술술 풀립니다.",
        ("Fire", "Fire"): "열정이 넘치지만 다툼을 조심해야 합니다.",
        ("Fire", "Earth"): "재능을 발휘하고 인정받는 날입니다.",
        ("Fire", "Metal"): "뜻밖의 금전운이 따르는 날입니다.",
        ("Fire", "Water"): "예상치 못한 변화나 스트레스가 있으니 차분하세요.",
        
        ("Earth", "Wood"): "주변의 간섭이나 압박이 있을 수 있습니다.",
        ("Earth", "Fire"): "문서운이 좋고 윗사람의 덕을 봅니다.",
        ("Earth", "Earth"): "믿음직한 친구와 함께하는 느낌입니다.",
        ("Earth", "Metal"): "나의 주장을 펼치기 좋은 날입니다.",
        ("Earth", "Water"): "확실한 이득이나 돈이 생길 수 있습니다.",
        
        ("Metal", "Wood"): "목표를 달성하고 성과를 쟁취하는 날입니다.",
        ("Metal", "Fire"): "나를 단련시키는 시련이 있지만 성장합니다.",
        ("Metal", "Earth"): "마음이 편안하고 안정되는 날입니다.",
        ("Metal", "Metal"): "고집이 세질 수 있으니 유연하게 대처하세요.",
        ("Metal", "Water"): "재치와 센스가 넘쳐 인기가 많아집니다.",
        
        ("Water", "Wood"): "창의력이 발휘되고 타인을 도울 일이 생깁니다.",
        ("Water", "Fire"): "큰 재물을 다룰 기회가 옵니다.",
        ("Water", "Earth"): "책임감이 커지고 명예가 따르는 날입니다.",
        ("Water", "Metal"): "생각지 못한 도움이나 후원을 받습니다.",
        ("Water", "Water"): "경쟁자가 있거나 지출이 생길 수 있습니다."
    }
    
    # 기본값
    advice_msg = "평범하고 무난한 하루입니다. 흐름에 몸을 맡기세요."
    if (my_elem, day_elem) in relations:
        advice_msg = relations[(my_elem, day_elem)]
    
    st.markdown(f"### {t['advice']}")
    st.success(advice_msg)
    
    # 인쇄 버튼
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Result</button>""", height=50)
