import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Specific Day Forecast", page_icon="📅", layout="wide")

# 🔑 [마스터 키] (개발자용 프리패스)
UNLOCK_CODE = "MASTER2026"

# 🛒 [검로드 설정]
# 주소 맨 뒤에 있는 단어 (예: https://.../specific_day 라면 specific_day)
PRODUCT_PERMALINK = "specific_day" 
# 구매 페이지 주소
GUMROAD_LINK = "https://gumroad.com/l/선생님의_상품주소"

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 1.8em; font-weight: bold; color: #334155; margin-bottom: 10px;}
        .card {
            background-color: white; padding: 20px; border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #e2e8f0;
        }
        .score-box {
            font-size: 2em; font-weight: bold; text-align: center; margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 2. 사이드바
# ----------------------------------------------------------------
with st.sidebar:
    st.title("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    
    st.markdown("---")
    if st.button("👈 Home" if lang=="en" else "👈 홈으로"):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. 로직 함수
# ----------------------------------------------------------------
def analyze_specific_day(user_element, target_element, lang):
    relations = {
        "Wood": {"Water": 5, "Wood": 4, "Fire": 4, "Earth": 3, "Metal": 2},
        "Fire": {"Wood": 5, "Fire": 4, "Earth": 4, "Metal": 3, "Water": 2},
        "Earth": {"Fire": 5, "Earth": 4, "Metal": 4, "Water": 3, "Wood": 2},
        "Metal": {"Earth": 5, "Metal": 4, "Water": 4, "Wood": 3, "Fire": 2},
        "Water": {"Metal": 5, "Water": 4, "Wood": 4, "Fire": 3, "Earth": 2}
    }
    score = relations.get(user_element, {}).get(target_element, 3)
    
    result_ko = {
        5: "🌟 **최상의 날 (Excellent)**\n기운이 나를 도와주는 날입니다.",
        4: "✨ **좋은 날 (Good)**\n순조롭고 편안한 하루입니다.",
        3: "😐 **보통의 날 (Normal)**\n무난한 하루입니다.",
        2: "⚠️ **주의하는 날 (Caution)**\n기운이 조금 부딪힐 수 있습니다.",
        1: "🚫 **쉬어가는 날 (Rest)**\n중요한 결정은 미루고 휴식하세요."
    }
    result_en = {
        5: "🌟 **Excellent Day**\nEnergy supports you perfectly.",
        4: "✨ **Good Day**\nSmooth and comfortable.",
        3: "😐 **Normal Day**\nA standard day.",
        2: "⚠️ **Cautionary Day**\nEnergies might clash slightly.",
        1: "🚫 **Rest Day**\nDelay major decisions."
    }
    msg = result_ko[score] if lang == "ko" else result_en[score]
    return score, msg

# ----------------------------------------------------------------
# 4. UI 텍스트
# ----------------------------------------------------------------
ui = {
    "ko": {
        "title": "📅 특정일 운세 (Specific Day)",
        "sub": "궁금한 날짜를 선택하면, 그날의 기운이 나에게 맞는지 알려드립니다.",
        "lock_msg": "🔒 유료 기능입니다 ($3)",
        "label": "라이센스 키 입력",
        "btn_unlock": "확인 (Unlock)",
        "btn_buy": "💳 구매하러 가기",
        "user_date": "나의 생년월일",
        "target_date": "확인하고 싶은 날짜",
        "btn_analyze": "운세 확인하기",
        "result": "분석 결과",
        "print": "🖨️ 결과 인쇄하기"
    },
    "en": {
        "title": "📅 Specific Day Forecast",
        "sub": "Check the energy compatibility of a specific date.",
        "lock_msg": "🔒 Premium Feature ($3)",
        "label": "Enter License Key",
        "btn_unlock": "Unlock",
        "btn_buy": "💳 Buy Access",
        "user_date": "Your Birth Date",
        "target_date": "Date to Check",
        "btn_analyze": "Check Forecast",
        "result": "Analysis Result",
        "print": "🖨️ Print Result"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 5. 잠금 장치 (검로드 연동 + 3회 제한 경찰 로직)
# ----------------------------------------------------------------
if "unlocked_specific" not in st.session_state: 
    st.session_state["unlocked_specific"] = False

if not st.session_state["unlocked_specific"]:
    with st.container(border=True):
        st.info(t['sub'])
        st.write(f"### {t['lock_msg']}")
        
        # 구매 링크 버튼
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock']):
            # 1. 마스터키 (개발자용)
            if key == UNLOCK_CODE:
                st.session_state["unlocked_specific"] = True
                st.success("Master Key Accepted!")
                st.rerun()
            
            # 2. 검로드 API 호출 (선생님이 원하시는 로직!)
            try:
                response = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={
                        "product_permalink": PRODUCT_PERMALINK,
                        "license_key": key
                    }
                )
                data = response.json()

                # 👇 [여기가 바로 선생님이 말씀하신 '내 사이트에서 막는' 부분입니다]
                if data.get("success"):
                    # (1) 사용 횟수 확인
                    current_uses = data.get("uses", 0)
                    
                    # (2) 3회 초과 시 강제 차단 (검로드 설정 무시)
                    if current_uses > 3:
                        st.error("🚫 사용 한도(3회)를 초과했습니다. (License limit exceeded)")
                    else:
                        st.session_state["unlocked_specific"] = True
                        st.success(f"인증 성공! (현재 사용 횟수: {current_uses}회)")
                        st.rerun()
                else:
                    st.error("🚫 유효하지 않은 키입니다. (Invalid Key)")
            
            except Exception as e:
                st.error("인터넷 연결 오류 (Connection Error)")
    
    st.stop() # 잠겨있으면 아래 코드 실행 안 함

# ----------------------------------------------------------------
# 6. 메인 기능 (잠금 해제 후)
# ----------------------------------------------------------------
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        if "saved_date" not in st.session_state:
            st.session_state["saved_date"] = date(1990, 1, 1)
        birth_date = st.date_input(t['user_date'], value=st.session_state["saved_date"], min_value=date(1900,1,1))
        st.session_state["saved_date"] = birth_date
        
    with col2:
        target_date = st.date_input(t['target_date'], value=date.today(), min_value=date.today())

    if st.button(t['btn_analyze'], type="primary", use_container_width=True):
        st.divider()
        
        user_info = calculate_day_gan(birth_date)
        target_info = calculate_day_gan(target_date)
        
        u_elem = user_info['element']
        t_elem = target_info['element']
        
        score, msg = analyze_specific_day(u_elem, t_elem, lang)
        
        st.subheader(t['result'])
        
        color_map = {5: "#22c55e", 4: "#3b82f6", 3: "#64748b", 2: "#f59e0b", 1: "#ef4444"}
        res_color = color_map[score]
        
        st.markdown(f"""
        <div class='card' style='border-top: 5px solid {res_color}; text-align: center;'>
            <h3 style='color: #64748b; margin-bottom: 20px;'>{target_date.strftime('%Y-%m-%d')}</h3>
            <div style='display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px;'>
                <div>
                    <div style='font-size:0.9em; color:#999;'>ME</div>
                    <div style='font-size:1.5em; font-weight:bold; color:#333;'>{user_info[lang]}</div>
                    <div style='font-size:0.8em; color:#666;'>({u_elem})</div>
                </div>
                <div style='font-size:1.2em; color:#ccc;'>vs</div>
                <div>
                    <div style='font-size:0.9em; color:#999;'>DAY</div>
                    <div style='font-size:1.5em; font-weight:bold; color:#333;'>{target_info[lang]}</div>
                    <div style='font-size:0.8em; color:#666;'>({t_elem})</div>
                </div>
            </div>
            <hr style='margin: 20px 0;'>
            <div class='score-box' style='color: {res_color}; white-space: pre-line;'>{msg}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 인쇄 버튼
        st.divider()
        components.html(
            f"""
            <script>function printParent() {{ window.parent.print(); }}</script>
            <div style="display: flex; justify-content: center;">
                <button onclick="printParent()" style="
                    background-color: #64748b; color: white; border: none; padding: 12px 24px; 
                    text-align: center; font-size: 16px; cursor: pointer; border-radius: 8px; font-weight: bold;
                ">
                    {t['print']}
                </button>
            </div>
            """, height=100
        )
