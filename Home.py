import streamlit as st
from datetime import date, time
# utils.py가 같은 폴더에 있어야 합니다.
from utils import calculate_day_gan 

# 1. 페이지 설정 (가장 먼저 와야 함)
st.set_page_config(page_title="The Element: Destiny Map", page_icon="🧭", layout="wide")

# ----------------------------------------------------------------
# [스타일] 배경 및 디자인 설정
# ----------------------------------------------------------------
st.markdown("""
    <style>
        /* 배경 그래픽 적용 */
        .stApp {
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
                url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }
        .main-title {font-size: 2.5em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 5px;}
        .sub-desc {font-size: 1.1em; color: #64748b; text-align: center; margin-bottom: 30px;}
        .card {background: rgba(255, 255, 255, 0.9); padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# [사이드바] 언어 설정 & 커피 후원
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["한국어", "English"])
    lang = "ko" if "한국어" in lang_opt else "en"
    
    st.markdown("---")
    coffee_title = "☕ 개발자 응원하기" if lang == "ko" else "☕ Buy me a coffee"
    coffee_msg = "운명의 코드를 응원해 주세요!" if lang == "ko" else "Support the developer!"
    
    st.header(coffee_title)
    st.markdown(f"""
        <div style="text-align: center;">
            <a href="https://buymeacoffee.com/5codes" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                    style="width: 180px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 5px;">
            </a>
            <p style="font-size: 14px; color: #555; margin-top: 10px;">{coffee_msg}</p>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------
# [메인] UI 텍스트 사전 (언어별)
# ----------------------------------------------------------------
txt = {
    "ko": {
        "title": "🧭 운명의 나침반",
        "sub": "당신의 태어난 순간이 말해주는 운명의 지도를 펼쳐보세요.",
        "input_h": "👤 사주 정보 입력 (필수)",
        "name": "이름", "birth": "생년월일", "gender": "성별", "time": "태어난 시간", "unknown": "시간 모름",
        "btn": "✨ 내 운명 확인하기 (Free)",
        "warn_name": "이름을 입력해주세요.",
        "res_hello": "반갑습니다,",
        "res_msg": "당신은 **'{e_name}'**의 기운을 타고났습니다.",
        "menu_h": "💎 프리미엄 운세 스토어",
        "m1_t": "🔮 2026 신년 운세", "m1_d": "내년의 재물, 연애, 직장운을 정밀하게 분석합니다.", "m1_b": "2026 운세 보기 ($10)",
        "m2_t": "📆 택일 (좋은 날짜)", "m2_d": "결혼, 이사, 계약 등 중요한 날짜를 잡아드립니다.", "m2_b": "좋은 날짜 받기 ($5)",
        "m3_t": "👑 프리패스 (All-Access)", "m3_d": "모든 유료 서비스를 한 번에 이용하세요!", "m3_b": "👉 프리패스 구매 ($20)"
    },
    "en": {
        "title": "🧭 The Element: Destiny Map",
        "sub": "Discover the map of destiny hidden in your birth moment.",
        "input_h": "👤 Enter Your Details",
        "name": "Name", "birth": "Date of Birth", "gender": "Gender", "time": "Birth Time", "unknown": "Unknown Time",
        "btn": "✨ Analyze My Destiny (Free)",
        "warn_name": "Please enter your name.",
        "res_hello": "Hello,",
        "res_msg": "You are born with the energy of **'{e_name}'**.",
        "menu_h": "💎 Premium Store",
        "m1_t": "🔮 2026 Forecast", "m1_d": "Detailed analysis of wealth, love, and career.", "m1_b": "View 2026 Forecast ($10)",
        "m2_t": "📆 Date Selection", "m2_d": "Best dates for wedding, moving, or contracts.", "m2_b": "Get Best Dates ($5)",
        "m3_t": "👑 All-Access Pass", "m3_d": "Unlock ALL premium services at once!", "m3_b": "👉 Buy Pass ($20)"
    }
}
t = txt[lang] # 현재 언어 선택

# ----------------------------------------------------------------
# [메인] 화면 구성
# ----------------------------------------------------------------
st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-desc'>{t['sub']}</div>", unsafe_allow_html=True)

# 세션 초기화
if "user_name" not in st.session_state: st.session_state["user_name"] = ""
if "birth_date" not in st.session_state: st.session_state["birth_date"] = date(1990, 1, 1)
if "birth_time" not in st.session_state: st.session_state["birth_time"] = time(12, 00)
if "time_unknown" not in st.session_state: st.session_state["time_unknown"] = False
if "gender" not in st.session_state: st.session_state["gender"] = "Male"
if "analyzed" not in st.session_state: st.session_state["analyzed"] = False

# 입력창 컨테이너
st.markdown(f"### {t['input_h']}")
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input(t['name'], value=st.session_state["user_name"])
        g_opts = ["Male", "Female"] if lang == "en" else ["남성", "여성"]
        gender_val = st.radio(t['gender'], g_opts, horizontal=True)
        gender = "Male" if gender_val in ["Male", "남성"] else "Female"
    with c2:
        b_date = st.date_input(t['birth'], min_value=date(1920,1,1), value=st.session_state["birth_date"])
        tc1, tc2 = st.columns([2, 1])
        with tc2:
            st.write("")
            st.write("")
            is_unknown = st.checkbox(t['unknown'], value=st.session_state["time_unknown"])
        with tc1:
            b_time = st.time_input(t['time'], value=st.session_state["birth_time"], disabled=is_unknown)

    if st.button(t['btn'], type="primary", use_container_width=True):
        if name:
            st.session_state["user_name"] = name
            st.session_state["birth_date"] = b_date
            st.session_state["gender"] = gender
            st.session_state["time_unknown"] = is_unknown
            st.session_state["birth_time"] = None if is_unknown else b_time
            st.session_state["analyzed"] = True
            st.rerun()
        else:
            st.warning(t['warn_name'])

# ----------------------------------------------------------------
# [결과] 무료 분석 + 유료 메뉴판
# ----------------------------------------------------------------
if st.session_state["analyzed"]:
    st.divider()
    day_info = calculate_day_gan(st.session_state["birth_date"])
    element_name = day_info[lang] # utils에서 한/영 자동 가져옴
    
    st.markdown(f"""
    <div class='card' style='text-align:center;'>
        <h3 style='color:#475569;'>{t['res_hello']} <b>{st.session_state['user_name']}</b>!</h3>
        <p style='font-size:1.2em; margin-top:10px;'>
            {t['res_msg'].format(e_name=element_name)}
        </p>
        <p style='color:#64748b; font-size:0.9em; margin-top:5px;'>({day_info['desc']})</p>
    </div>
    """, unsafe_allow_html=True)

    # 유료 메뉴판
    st.subheader(t['menu_h'])
    mc1, mc2, mc3 = st.columns(3)
    
    with mc1:
        st.info(f"**{t['m1_t']}**\n\n{t['m1_d']}")
        if st.button(t['m1_b'], use_container_width=True):
            st.switch_page("pages/1_🔮_2026_새해운세.py")
    
    with mc2:
        st.success(f"**{t['m2_t']}**\n\n{t['m2_d']}")
        if st.button(t['m2_b'], use_container_width=True):
            st.switch_page("pages/2_📆_택일_서비스.py")
            
    with mc3:
        st.warning(f"**{t['m3_t']}**\n\n{t['m3_d']}")
        st.link_button(t['m3_b'], "https://gum.co/demo_product", use_container_width=True)

    st.sidebar.success("✅ Analysis Complete!")
