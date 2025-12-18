import streamlit as st
from datetime import date, time
from utils import calculate_day_gan 

# 1. 페이지 설정
st.set_page_config(page_title="The Element: Destiny Map", page_icon="🧭", layout="wide")

# 2. 스타일 및 배경
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-title {font-size: 2.5em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 5px;}
        .sub-desc {font-size: 1.1em; color: #64748b; text-align: center; margin-bottom: 30px;}
        .card {background: rgba(255, 255, 255, 0.9); padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);}
        /* 버튼 스타일 통일 */
        .stButton button {width: 100%; border-radius: 8px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바 (군더더기 제거됨)
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

# 4. 텍스트 사전 (가격 $10로 수정완료!)
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
        
        # [수정됨] 메뉴 텍스트 (가격 $10 통일 / 프리패스 $30)
        "m1_t": "🔮 2026 신년 운세 ($10)", "m1_d": "내년의 재물, 연애, 직장운을 정밀하게 분석합니다.", 
        "m2_t": "📅 그날의 운세 ($10)", "m2_d": "면접, 데이트, 계약 등 특정 날짜의 운세를 미리 확인하세요.",
        "m3_t": "❤️ 궁합 서비스 ($10)", "m3_d": "그 사람과 나의 케미스트리(속궁합/겉궁합) 분석.",
        "m4_t": "📆 택일 서비스 ($10)", "m4_d": "결혼, 이사, 개업 등 중요한 행사를 위한 최고의 날짜 추천.",
        "m5_t": "👑 프리패스 VIP ($30)", "m5_d": "모든 유료 서비스를 제한 없이 한 번에 이용하세요!",
        "btn_common": "확인하기", "btn_buy": "구매하기"
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
        
        # [Updated] Menu Texts ($10 unified / Pass $30)
        "m1_t": "🔮 2026 Forecast ($10)", "m1_d": "Detailed analysis of wealth, love, and career for 2026.",
        "m2_t": "📅 Daily Forecast ($10)", "m2_d": "Check your luck for a specific date (Interview, Date, etc).",
        "m3_t": "❤️ Compatibility ($10)", "m3_d": "Check chemistry and relationship potential with your partner.",
        "m4_t": "📆 Date Selection ($10)", "m4_d": "Find the most auspicious dates for Wedding, Moving, etc.",
        "m5_t": "👑 All-Access Pass ($30)", "m5_d": "Unlock ALL premium services at once!",
        "btn_common": "Check Now", "btn_buy": "Buy Pass"
    }
}
t = txt[lang]

# 5. 화면 구성
st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-desc'>{t['sub']}</div>", unsafe_allow_html=True)

# 세션 초기화
if "user_name" not in st.session_state: st.session_state["user_name"] = ""
if "birth_date" not in st.session_state: st.session_state["birth_date"] = date(1990, 1, 1)
if "birth_time" not in st.session_state: st.session_state["birth_time"] = time(12, 00)
if "time_unknown" not in st.session_state: st.session_state["time_unknown"] = False
if "gender" not in st.session_state: st.session_state["gender"] = "Male"
if "analyzed" not in st.session_state: st.session_state["analyzed"] = False

# 입력창
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

# 6. 결과 및 메뉴판
if st.session_state["analyzed"]:
    st.divider()
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    st.markdown(f"""
    <div class='card' style='text-align:center;'>
        <h3 style='color:#475569;'>{t['res_hello']} <b>{st.session_state['user_name']}</b>!</h3>
        <p style='font-size:1.2em; margin-top:10px;'>
            {t['res_msg'].format(e_name=day_info[lang])}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 💎 유료 메뉴판
    st.subheader(t['menu_h'])
    
    # 1열
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**{t['m1_t']}**") # 2026 운세
        if st.button(t['btn_common'], key="btn1", help=t['m1_d'], use_container_width=True): 
            st.switch_page("pages/1_🔮_2026_새해운세.py")
    
    with col_b:
        st.success(f"**{t['m2_t']}**") # 그날의 운세
        if st.button(t['btn_common'], key="btn2", help=t['m2_d'], use_container_width=True): 
            st.switch_page("pages/2_📅_그날의_운세.py")

    # 2열
    col_c, col_d = st.columns(2)
    with col_c:
        st.error(f"**{t['m3_t']}**") # 궁합
        if st.button(t['btn_common'], key="btn3", help=t['m3_d'], use_container_width=True): 
            st.switch_page("pages/3_❤️_궁합_서비스.py")
            
    with col_d:
        st.warning(f"**{t['m4_t']}**") # 택일
        if st.button(t['btn_common'], key="btn4", help=t['m4_d'], use_container_width=True): 
            st.switch_page("pages/4_📆_택일_서비스.py")

    # 3열: 프리패스
    st.markdown("---")
    st.info(f"👑 **{t['m5_t']}**")
    # Gumroad 링크는 나중에 선생님의 실제 '프리패스 상품 링크'로 바꾸셔야 합니다!
    st.link_button(t['btn_buy'], "https://gum.co/demo_product", help=t['m5_d'], use_container_width=True)
