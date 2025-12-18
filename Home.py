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
        .stButton button {width: 100%; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["한국어", "English"])
    lang = "ko" if "한국어" in lang_opt else "en"
    
    st.markdown("---")
    st.info("👈 Use the menu to navigate" if lang=="en" else "👈 왼쪽 메뉴를 눌러 이동하세요")

# 4. 텍스트 사전 (궁합 추가됨!)
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
        # 메뉴 텍스트
        "m1_t": "🔮 2026 신년 운세", "m1_d": "재물, 연애, 직장운 정밀 분석", "m1_b": "보기 ($10)",
        "m2_t": "📆 택일 (좋은 날짜)", "m2_d": "결혼, 이사, 계약 날짜 잡기", "m2_b": "받기 ($5)",
        "m3_t": "❤️ 궁합 (케미스트리)", "m3_d": "그 사람과 나의 인연 분석", "m3_b": "확인 ($10)",
        "m4_t": "👑 프리패스 (VIP)", "m4_d": "모든 유료 서비스를 한 번에!", "m4_b": "구매 ($20)"
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
        # Menu Texts
        "m1_t": "🔮 2026 Forecast", "m1_d": "Wealth, Love, Career Analysis", "m1_b": "View ($10)",
        "m2_t": "📆 Date Selection", "m2_d": "Best dates for big events", "m2_b": "Get ($5)",
        "m3_t": "❤️ Compatibility", "m3_d": "Check chemistry with partner", "m3_b": "Check ($10)",
        "m4_t": "👑 All-Access Pass", "m4_d": "Unlock ALL services at once!", "m4_b": "Buy ($20)"
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

# 6. 결과 및 메뉴판 (4단 구성!)
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

    # 💎 유료 메뉴판 (업데이트됨)
    st.subheader(t['menu_h'])
    
    # 1열: 주요 운세 (2026, 그날의 운세)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"🔮 **{t['m1_t']}**\n\n{t['m1_d']}") # 2026
        if st.button(t['m1_b'], use_container_width=True): st.switch_page("pages/1_🔮_2026_새해운세.py")
    
    with col_b:
        st.success(f"📅 **{'Specific Day Forecast' if lang=='en' else '그날의 운세 (NEW)'}**\n\n{'Check your luck for tomorrow or any specific date.' if lang=='en' else '내일, 면접일, 데이트 날 등 특정일의 운세를 미리 보세요.'}")
        # 새로 만든 2번 파일로 이동
        if st.button(f"{'Check' if lang=='en' else '확인하기 ($5)'}", use_container_width=True): st.switch_page("pages/2_📅_그날의_운세.py")

    # 2열: 관계 및 택일
    col_c, col_d = st.columns(2)
    with col_c:
        st.error(f"❤️ **{t['m3_t']}**\n\n{t['m3_d']}") # 궁합
        if st.button(t['m3_b'], use_container_width=True): st.switch_page("pages/3_❤️_궁합_서비스.py")
            
    with col_d:
        st.warning(f"📆 **{t['m2_t']}**\n\n{t['m2_d']}") # 택일 (이제 4번 파일로 이동)
        # 파일명을 4번으로 바꿨으므로 여기도 바꿔줍니다
        if st.button(t['m2_b'], use_container_width=True): st.switch_page("pages/4_📆_택일_서비스.py")

    # 3열: 프리패스 (배너처럼 길게)
    st.markdown("---")
    st.info(f"👑 **{t['m4_t']}** : {t['m4_d']}")
    st.link_button(t['m4_b'], "https://gum.co/demo_product", use_container_width=True)

    st.sidebar.success("✅ Analysis Complete!")
