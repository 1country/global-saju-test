import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date, timedelta
import random
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Date Selection", page_icon="🗓️", layout="wide")

# 🔑 [키 설정]
UNLOCK_CODE = "MASTER2026"

# (1) 이 페이지 전용 상품 (3회 제한)
PRODUCT_PERMALINK_SPECIFIC = "date_selection"
# (2) 만능 패스 상품 (10회 제한)
PRODUCT_PERMALINK_ALL = "all-access_pass"

# 구매 링크
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/date_selection"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #059669; margin-bottom: 10px; text-align: center;}
        
        /* 카드 디자인 */
        .date-card {
            background-color: white; padding: 30px; border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 25px; border: 1px solid #e2e8f0;
            transition: transform 0.2s;
        }
        .date-card:hover { transform: translateY(-5px); border-color: #34d399; }
        
        .rank-badge {
            background-color: #059669; color: white; padding: 5px 15px; border-radius: 20px;
            font-weight: bold; font-size: 0.9em; display: inline-block; margin-bottom: 10px;
        }
        .date-header { font-size: 1.8em; font-weight: bold; color: #1e293b; margin: 10px 0; }
        .star-rating { font-size: 1.4em; color: #f59e0b; margin-bottom: 15px; }
        
        .section-title { font-weight: bold; color: #334155; font-size: 1.1em; margin-top: 15px; }
        .desc-text { font-size: 1.05em; line-height: 1.7; color: #475569; text-align: justify; }
        
        .user-info-box {
            background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0;
            color: #166534; font-size: 0.95em; margin-bottom: 20px; text-align: center;
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
    if st.button("👈 Home"): st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. 택일 분석 로직
# ----------------------------------------------------------------
def get_auspicious_dates(user_elem, target_date, event_type, lang):
    event_keywords = {
        "Wedding": {"ko": "결혼/약혼", "en": "Wedding/Engagement"},
        "Moving": {"ko": "이사/이전", "en": "Moving"},
        "Business": {"ko": "개업/계약", "en": "Opening Business"},
        "Travel": {"ko": "여행/출장", "en": "Travel"},
        "Surgery": {"ko": "수술/시술", "en": "Surgery/Medical"}
    }
    evt_name = event_keywords[event_type][lang]
    
    # 추천 날짜 생성 (시뮬레이션)
    results = [
        {
            "rank": 1,
            "date": target_date + timedelta(days=6),
            "stars": 5,
            "theme_ko": "✨ 천을귀인(天乙貴人)이 돕는 최고의 길일",
            "theme_en": "✨ Day of Noble Help: Best Auspicious Day",
            "desc_ko": f"이 날은 당신({user_elem})에게 최고의 행운을 가져다주는 '귀인'의 에너지가 들어오는 날입니다. '{evt_name}'을(를) 진행하기에 이보다 완벽할 순 없습니다. 모든 장애물이 눈 녹듯 사라지고, 주변 사람들이 발 벗고 나서서 당신을 도와줍니다. 시작이 좋으면 끝도 좋다는 말처럼, 이날 시작한 일은 오랫동안 번창하고 행복한 결실을 맺을 것입니다. 특히 오전 9시~11시 사이가 황금 시간대입니다.",
            "desc_en": f"This involves the energy of a 'Noble Person' who brings the best luck to you ({user_elem}). It is the perfect day for {evt_name}. All obstacles will disappear, and people around you will support you. As the saying goes, 'A good beginning makes a good ending,' what you start today will flourish. Best hours: 09:00 - 11:00."
        },
        {
            "rank": 2,
            "date": target_date + timedelta(days=14),
            "stars": 4,
            "theme_ko": "💰 재물과 실속이 따르는 알짜배기 날",
            "theme_en": "💰 Day of Wealth & Substance",
            "desc_ko": f"현실적인 이득이 매우 큰 날입니다. '{evt_name}'을(를) 통해 금전적인 이득을 보거나, 가성비 좋은 결과를 얻을 수 있습니다. 화려함보다는 실속을 챙기기에 적합합니다. 다만, 너무 계산적으로 보이지 않도록 주의하세요. 에너지가 안정적이라 큰 변수 없이 계획대로 착착 진행될 것입니다. 오후 1시~3시 사이에 중요한 결정을 하세요.",
            "desc_en": f"A day of great realistic gain. Through {evt_name}, you can expect financial benefits or cost-effective results. It represents substance over flashiness. The energy is stable, so everything will proceed according to plan. Best hours: 13:00 - 15:00."
        },
        {
            "rank": 3,
            "date": target_date + timedelta(days=22),
            "stars": 4,
            "theme_ko": "❤️ 합(合)이 들어와 조화롭고 평화로운 날",
            "theme_en": "❤️ Day of Harmony & Peace",
            "desc_ko": f"우주의 기운이 당신과 부드럽게 화합하는 날입니다. '{evt_name}' 과정에서 생길 수 있는 갈등이나 잡음이 최소화됩니다. 마음이 편안하고 컨디션이 최상으로 유지됩니다. 혹시 모를 실수가 있어도 웃으며 넘어갈 수 있는 여유가 생깁니다. 무리하게 욕심내지 말고 순리대로 진행하면 기대 이상의 성과를 얻습니다.",
            "desc_en": f"The universe's energy harmonizes gently with you. Conflicts or noise regarding {evt_name} will be minimized. Your mind will be at peace. Even if there are mistakes, they will be forgiven. Do not be greedy; follow the flow, and you will achieve more than expected."
        }
    ]
    return results

# ----------------------------------------------------------------
# 4. 메인 화면 UI
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("Please enter your info at Home first." if lang == "en" else "⚠️ 홈 화면에서 본인 정보를 먼저 입력해주세요.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

u_name = st.session_state["user_name"]
u_dob = st.session_state["birth_date"]
u_gender = st.session_state.get("gender", "Male")

ui = {
    "ko": {
        "title": "📅 프리미엄 택일 (Date Selection)",
        "sub": "결혼, 이사, 중요한 계약... 인생을 바꾸는 최고의 날짜를 찾아드립니다.",
        "input_label": "어떤 행사를 계획 중이신가요?",
        "date_label": "언제쯤(기준일)으로 알아볼까요?",
        "btn_check": "최고의 날짜 확인하기",
        "lock_title": "🔒 택일 리포트 잠금",
        "lock_desc": "결제 후 받은 라이센스 키를 입력하세요.",
        "lock_warn": "⚠️ 주의: 라이센스 키 사용 횟수가 차감됩니다.",
        "label": "구매 후 받은 라이센스 키 입력",
        "btn_unlock": "잠금 해제",
        "btn_buy_sp": "💳 단품 구매 ($10 / 3회)",
        "btn_buy_all": "🎟️ All-Access 패스 구매 ($30 / 10회)",
        "print": "🖨️ 리포트 인쇄하기"
    },
    "en": {
        "title": "📅 Premium Date Selection",
        "sub": "Wedding, Moving, Contracts... Find the best date to change your life.",
        "input_label": "What is the event?",
        "date_label": "Target Reference Date (Search around...)",
        "btn_check": "Find Best Dates",
        "lock_title": "🔒 Report Locked",
        "lock_desc": "Enter your license key.",
        "lock_warn": "⚠️ Warning: This will consume 1 usage credit.",
        "label": "Enter License Key",
        "btn_unlock": "Unlock",
        "btn_buy_sp": "💳 Buy Single ($10 / 3 Uses)",
        "btn_buy_all": "🎟️ Buy All-Access ($30 / 10 Uses)",
        "print": "🖨️ Print Report"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='user-info-box'>👤 {u_name} ({u_gender}, {u_dob})</div>", unsafe_allow_html=True)
st.info(t['sub'])

# (2) 입력 폼
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        event_type = st.selectbox(
            t['input_label'],
            ["Wedding", "Moving", "Business", "Travel", "Surgery"]
        )
    with col2:
        ref_date = st.date_input(t['date_label'], value=date.today(), min_value=date.today())

# (3) 잠금 및 3회 제한 로직
if "unlocked_date" not in st.session_state: st.session_state["unlocked_date"] = False

# 🌟 팝업창(Dialog) 함수 정의
@st.dialog("⚠️ Usage Limit Warning")
def show_limit_warning():
    st.warning(t['lock_warn'], icon="⚠️")
    st.write("Checking this result will deduct 1 credit from your license.")
    if st.button("I Understand & Proceed", type="primary"):
        st.rerun()

if not st.session_state["unlocked_date"]:
    st.divider()
    with st.container(border=True):
        st.markdown(f"### {t['lock_title']}")
        st.write(t['lock_desc'])
        
        # 3회 제한 경고 버튼
        if st.button("⚠️ Check Limit Info", type="secondary"):
            show_limit_warning()
            
        c1, c2 = st.columns(2)
        with c1: st.link_button(t['btn_buy_sp'], GUMROAD_LINK_SPECIFIC)
        with c2: st.link_button(t['btn_buy_all'], GUMROAD_LINK_ALL)
        
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock'], type="primary"):
            if key == UNLOCK_CODE:
                st.session_state["unlocked_date"] = True
                st.success("Developer Access Granted!")
                st.rerun()
            try:
                # (A) 단품 상품 확인
                response_specific = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={"product_permalink": PRODUCT_PERMALINK_SPECIFIC, "license_key": key}
                )
                data_specific = response_specific.json()

                if data_specific.get("success"):
                    if data_specific.get("uses", 0) > 3:
                        st.error(f"🚫 Limit exceeded (Max 3 uses).")
                    else:
                        st.session_state["unlocked_date"] = True
                        st.success("Success!")
                        st.rerun()
                else:
                    # (B) All-Access 패스 확인
                    response_all = requests.post(
                        "https://api.gumroad.com/v2/licenses/verify",
                        data={"product_permalink": PRODUCT_PERMALINK_ALL, "license_key": key}
                    )
                    data_all = response_all.json()
                    
                    if data_all.get("success"):
                        if data_all.get("uses", 0) > 10:
                            st.error(f"🚫 All-Access Pass Limit Exceeded ({data_all.get('uses')}/10)")
                        else:
                            st.session_state["unlocked_date"] = True
                            st.success("All-Access Pass Accepted!")
                            st.rerun()
                    else:
                        st.error("🚫 Invalid Key.")
            except:
                st.error("Connection Error")
    st.stop()

# (4) 결과 리포트 (Top 3 날짜)
if st.session_state["unlocked_date"]:
    st.divider()
    
    # 오행 계산
    u_info = calculate_day_gan(u_dob)
    
    # 날짜 추천 데이터 가져오기
    dates = get_auspicious_dates(u_info['element'], ref_date, event_type, lang)
    
    st.markdown(f"<h2 style='text-align:center; color:#334155; margin-bottom:30px;'>✨ Top 3 Dates for {event_type}</h2>", unsafe_allow_html=True)
    
    # 3개의 카드로 출력
    for d in dates:
        stars_icon = "⭐" * d['stars']
        theme = d['theme_ko'] if lang == "ko" else d['theme_en']
        desc = d['desc_ko'] if lang == "ko" else d['desc_en']
        
        # HTML 한 줄로 작성 (화면 깨짐 방지)
        html_card = f"""
        <div class='date-card'>
            <span class='rank-badge'>TOP {d['rank']}</span>
            <div class='star-rating'>{stars_icon}</div>
            <div class='date-header'>{d['date'].strftime('%Y-%m-%d (%A)')}</div>
            <div class='section-title'>{theme}</div>
            <div style='margin: 10px 0; border-bottom: 1px dashed #cbd5e1;'></div>
            <div class='desc-text'>{desc}</div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)

    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#059669; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);">
            {t['print']}
            </button>
        </div>""", height=100
    )
