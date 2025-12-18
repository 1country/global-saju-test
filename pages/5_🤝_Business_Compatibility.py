import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from utils import verify_license_flexible, calculate_day_gan

# 1. 페이지 설정
st.set_page_config(page_title="Business Compatibility", page_icon="🤝", layout="wide")

# 🔑 [추가됨] 마스터 비밀번호 설정
UNLOCK_CODE = "MASTER2026"

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
    p_date = st.date_input(t['d_label'], min_value=date(1950,1,1))

# 4. 잠금 로직
CURRENT_PRODUCT_ID = "business_compatibility" 
ALL_ACCESS_ID = "all_access_pass"

if "unlocked_biz" not in st.session_state: st.session_state["unlocked_biz"] = False

if not st.session_state["unlocked_biz"]:
    st.info(t['lock'])
    # 입력창 라벨 수정
    key = st.text_input("License Key or Password", type="password")
    
    if st.button(t['btn_unlock']):
        # 1. 마스터키 확인
        if key == UNLOCK_CODE:
            st.session_state["unlocked_biz"] = True
            st.rerun()

        # 2. 라이센스 확인
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
    
    my_elem = my_info['element']
    p_elem = p_info['element']
    
    st.header(f"{st.session_state['user_name']} & {p_name}")
    st.subheader(t['res_title'])
    st.write(t['res_sub'])
    
    # [핵심] 비즈니스 궁합 데이터
    # 1. 업무 스타일 (Key: (내오행, 상대오행))
    work_style = {
        ("Wood", "Wood"): "서로 비슷해서 편하지만, 추진력만 있고 마무리가 약할 수 있습니다.",
        ("Wood", "Fire"): "당신이 기획하고 상대가 실행하는 최고의 파트너입니다.",
        ("Wood", "Earth"): "당신이 리더가 되어 상대를 관리해야 성과가 납니다.",
        ("Wood", "Metal"): "의견 충돌이 잦습니다. 상대의 비판을 수용해야 발전합니다.",
        ("Wood", "Water"): "상대가 당신을 도와줍니다. 멘토나 지원군으로 삼으세요.",
        
        ("Fire", "Wood"): "상대의 아이디어를 당신이 현실로 만드는 구조입니다.",
        ("Fire", "Fire"): "열정은 넘치지만 충동적인 결정을 조심해야 합니다.",
        ("Fire", "Earth"): "당신이 상대를 키워주는 관계입니다. 부하 직원으로 좋습니다.",
        ("Fire", "Metal"): "당신이 상대를 압박할 수 있습니다. 부드러운 리더십이 필요합니다.",
        ("Fire", "Water"): "상대가 당신의 열정을 식힐 수 있습니다. 감정 조절이 중요합니다.",
        
        ("Earth", "Wood"): "상대에게 휘둘릴 수 있습니다. 명확한 계약 관계가 필요합니다.",
        ("Earth", "Fire"): "상대의 도움으로 당신의 입지가 단단해집니다.",
        ("Earth", "Earth"): "변화보다는 안정을 추구하는 보수적인 파트너십입니다.",
        ("Earth", "Metal"): "당신의 자본이나 지원으로 상대가 성과를 냅니다.",
        ("Earth", "Water"): "당신이 상대를 통제하고 관리해야 재물이 모입니다.",
        
        ("Metal", "Wood"): "당신의 결단력으로 상대를 이끌어야 합니다.",
        ("Metal", "Fire"): "상대가 당신을 힘들게 하지만, 그 덕분에 당신이 성장합니다.",
        ("Metal", "Earth"): "상대의 묵묵한 지원을 받을 수 있습니다. 믿을만한 파트너.",
        ("Metal", "Metal"): "타협이 어렵습니다. 역할 분담을 확실히 해야 합니다.",
        ("Metal", "Water"): "당신의 노하우를 상대에게 전수해주는 관계입니다.",
        
        ("Water", "Wood"): "당신이 기획하고 투자하여 상대를 성장시킵니다.",
        ("Water", "Fire"): "당신이 주도권을 잡으면 큰 성과(재물)를 낼 수 있습니다.",
        ("Water", "Earth"): "상대의 간섭이 심할 수 있습니다. 스트레스 관리 필요.",
        ("Water", "Metal"): "상대로부터 지적 자산이나 노하우를 배울 수 있습니다.",
        ("Water", "Water"): "비밀이 많을 수 있습니다. 투명한 소통이 핵심입니다."
    }

    # 1. 업무 스타일 출력
    st.markdown(f"#### {t['card1']}")
    st.info(f"**Me ({my_elem}) vs Partner ({p_elem})**")
    st.write(work_style.get((my_elem, p_elem), "서로 다른 관점을 가진 파트너입니다."))
    
    # 2. 리더십 조언
    st.markdown(f"#### {t['card2']}")
    leadership_advice = "수평적인 관계가 좋습니다."
    if my_elem in ["Wood"] and p_elem in ["Earth"]: leadership_advice = "당신이 확실하게 리드해야 합니다."
    elif my_elem in ["Fire"] and p_elem in ["Metal"]: leadership_advice = "당신의 카리스마로 압도해야 합니다."
    elif my_elem in ["Earth"] and p_elem in ["Water"]: leadership_advice = "자금 관리나 실권은 당신이 쥐어야 합니다."
    elif my_elem in ["Metal"] and p_elem in ["Wood"]: leadership_advice = "원칙대로 상대를 이끌어야 합니다."
    elif my_elem in ["Water"] and p_elem in ["Fire"]: leadership_advice = "감정보다는 이성적으로 상대를 제어해야 합니다."
    st.warning(leadership_advice)
    
    # 3. 재물합 (간단 로직)
    st.markdown(f"#### {t['card3']}")
    money_luck = "보통입니다. 노력한 만큼 얻습니다."
    # 내가 극하는 오행(재성)이나 나를 생해주는 오행(인성)일 때 좋음
    if (my_elem, p_elem) in [("Wood", "Earth"), ("Fire", "Metal"), ("Earth", "Water"), ("Metal", "Wood"), ("Water", "Fire")]:
        money_luck = "💰 매우 좋습니다! 상대가 당신에게 돈을 벌어다 주는 형국입니다."
    elif (my_elem, p_elem) in [("Wood", "Water"), ("Fire", "Wood"), ("Earth", "Fire"), ("Metal", "Earth"), ("Water", "Metal")]:
        money_luck = "📈 좋습니다. 상대의 지원으로 사업이 확장됩니다."
    
    st.success(money_luck)
    
    # 4. 처세술 조언
    st.markdown(f"#### {t['advice']}")
    advice_msg = "상대방을 존중하고 경청하는 것이 성공의 열쇠입니다."
    # 상대가 나를 극하는 경우 (관성) -> 조심해야 함
    if (p_elem, my_elem) in [("Wood", "Earth"), ("Fire", "Metal"), ("Earth", "Water"), ("Metal", "Wood"), ("Water", "Fire")]:
        advice_msg = "상대방의 자존심을 건드리지 마세요. 겉으로는 져주는 척하면서 실리를 챙겨야 합니다."
        
    st.write(advice_msg)

    # 인쇄 버튼
    st.markdown("---")
    components.html("""<script>function printParent(){window.parent.print();}</script>
    <button onclick="printParent()" style='padding:10px; cursor:pointer;'>🖨️ Print Report</button>""", height=50)
