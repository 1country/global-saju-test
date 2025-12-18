import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from utils import calculate_day_gan, verify_license_flexible

# 1. 페이지 설정
st.set_page_config(page_title="Love Compatibility", page_icon="❤️", layout="wide")

# 🔑 [추가됨] 마스터 비밀번호 설정
UNLOCK_CODE = "MASTER2026"

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

# 2. 사이드바
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    st.info("👈 Home" if lang=="en" else "👈 홈으로 돌아가기")

# 3. 홈 정보 확인
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

# 상품 ID
CURRENT_PRODUCT_ID = "love_compatibility"
ALL_ACCESS_ID = "all_access_pass"

# 텍스트 데이터
txt = {
    "ko": {
        "title": "❤️ 사랑 궁합 (Love Match)",
        "intro": "그 사람과 나는 운명일까요? 서로의 기운이 만났을 때의 화학작용을 분석합니다.",
        "p_name": "상대방 이름 (Partner Name)",
        "p_birth": "상대방 생년월일 (Partner Birthday)",
        "lock": "🔒 유료 서비스입니다 ($10)",
        "btn_check": "궁합 확인하기",
        "res": "두 분의 궁합 분석",
        "my_energy": "나의 기운",
        "p_energy": "상대의 기운",
        "advice": "💡 연애 조언"
    },
    "en": {
        "title": "❤️ Love Compatibility",
        "intro": "Are we destined? Analyzing the chemistry when your energies meet.",
        "p_name": "Partner Name",
        "p_birth": "Partner Birthday",
        "lock": "🔒 Premium Service ($10)",
        "btn_check": "Check Compatibility",
        "res": "Compatibility Analysis",
        "my_energy": "My Energy",
        "p_energy": "Partner Energy",
        "advice": "💡 Relationship Advice"
    }
}
t = txt[lang]

# 메인 화면
st.title(t['title'])
st.write(t['intro'])

# ---------------------------------------------------------------------------
# 4. [수정됨] 잠금 로직 (마스터키 기능 추가)
# ---------------------------------------------------------------------------
if "unlocked_love" not in st.session_state: 
    st.session_state["unlocked_love"] = False

if not st.session_state["unlocked_love"]:
    st.divider()
    with st.container(border=True):
        st.info(t['lock'])
        input_key = st.text_input("License Key or Password", type="password")
        
        if st.button("Unlock"):
            # 1. 마스터 비밀번호 확인
            if input_key == UNLOCK_CODE:
                st.session_state["unlocked_love"] = True
                st.rerun()
                
            # 2. 정품 라이센스 확인
            is_valid, msg = verify_license_flexible(input_key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
            if is_valid:
                st.session_state["unlocked_love"] = True
                st.rerun()
            else:
                st.error(msg)
    st.stop()

# ---------------------------------------------------------------------------
# 5. 분석 결과
# ---------------------------------------------------------------------------
st.success("✅ Unlocked!")
st.divider()

col1, col2 = st.columns(2)
with col1: p_name = st.text_input(t['p_name'])
with col2: p_date = st.date_input(t['p_birth'], min_value=date(1950,1,1))

if st.button(t['btn_check'], type="primary"):
    # 계산 로직
    my_info = calculate_day_gan(st.session_state["birth_date"])
    p_info = calculate_day_gan(p_date)
    
    my_elem = my_info['element']
    p_elem = p_info['element']
    
    st.markdown("---")
    st.subheader(f"{st.session_state['user_name']} ❤️ {p_name}")
    
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.markdown(f"**{t['my_energy']}**")
        st.info(f"{my_info[lang]}\n({my_elem})")
    with c2:
        st.markdown("<h2 style='text-align: center;'>⚡</h2>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"**{t['p_energy']}**")
        st.error(f"{p_info[lang]}\n({p_elem})")
        
    # --- [핵심] 오행 궁합 데이터 ---
    love_relations = {
        # (나, 상대)
        ("Wood", "Wood"): "친구 같은 편안함이 있지만, 서로 고집을 부리면 큰 싸움이 될 수 있습니다.",
        ("Wood", "Fire"): "당신이 상대를 도와주고 헌신하는 관계입니다. 상대방은 당신 덕분에 빛납니다.",
        ("Wood", "Earth"): "당신이 리드하는 관계입니다. 상대방은 당신에게 의지하며 안정감을 느낍니다.",
        ("Wood", "Metal"): "상대방이 당신을 다듬어주는 관계입니다. 잔소리처럼 들릴 수 있으나 성장합니다.",
        ("Wood", "Water"): "상대방이 당신에게 헌신하고 사랑을 줍니다. 엄마 같은 따뜻함을 느낍니다.",

        ("Fire", "Wood"): "상대방의 도움으로 당신의 열정이 더욱 타오릅니다. 시너지가 좋은 커플!",
        ("Fire", "Fire"): "불꽃 같은 사랑! 하지만 한번 싸우면 걷잡을 수 없으니 조심하세요.",
        ("Fire", "Earth"): "당신이 상대를 챙겨주고 이끌어주는 관계입니다. 헌신적인 사랑.",
        ("Fire", "Metal"): "당신이 상대를 압도하는 기운이 있습니다. 싸움이 잦을 수 있으니 배려가 필요합니다.",
        ("Fire", "Water"): "물과 불의 만남. 서로 너무 다르지만, 그 다름에 강렬하게 끌리는 '치명적 사랑'입니다.",

        ("Earth", "Wood"): "상대방이 당신을 구속하려 할 수 있습니다. 답답할 수 있지만 안정적입니다.",
        ("Earth", "Fire"): "상대방의 사랑을 듬뿍 받는 관계입니다. 당신은 사랑받기 위해 태어났군요.",
        ("Earth", "Earth"): "믿음과 신뢰로 뭉친 커플입니다. 재미는 덜해도 결혼 상대로 최고입니다.",
        ("Earth", "Metal"): "당신이 상대를 도와주는 관계입니다. 자식 키우듯 챙겨주게 됩니다.",
        ("Earth", "Water"): "당신이 상대를 통제할 수 있습니다. 주도권은 당신에게 있습니다.",

        ("Metal", "Wood"): "당신이 상대를 깎고 다듬으려 합니다. 상대가 상처받지 않게 말조심하세요.",
        ("Metal", "Fire"): "상대방이 당신을 힘들게 할 수 있지만, 그 과정에서 당신은 보석이 됩니다.",
        ("Metal", "Earth"): "상대방의 헌신적인 사랑을 받습니다. 든든한 배경이 되어줍니다.",
        ("Metal", "Metal"): "차가운 이성의 만남. 감정적인 교류보다는 의리와 원칙이 중요합니다.",
        ("Metal", "Water"): "당신이 상대를 위해 아낌없이 주는 나무가 됩니다. 퍼주는 사랑.",

        ("Water", "Wood"): "당신이 상대를 키워주는 관계입니다. 상대의 성장을 보며 기쁨을 느낍니다.",
        ("Water", "Fire"): "상대방을 이길 수 있는 힘이 당신에게 있습니다. 하지만 너무 끄려고 하지 마세요.",
        ("Water", "Earth"): "상대방이 당신을 가두려 합니다. 집착이나 구속이 있을 수 있습니다.",
        ("Water", "Metal"): "상대방의 끊임없는 사랑과 지원을 받습니다. 마르지 않는 샘물 같은 사랑.",
        ("Water", "Water"): "깊은 바다와 같은 사랑. 서로의 속마음을 다 알기 어렵지만 깊게 통합니다."
    }
    
    msg = love_relations.get((my_elem, p_elem), "서로 다른 매력에 끌리는 신비로운 관계입니다.")
    
    st.markdown(f"### {t['advice']}")
    st.success(msg)
    
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Result</button>""", height=50)
