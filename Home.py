import streamlit as st
from datetime import date, time
from utils import calculate_day_gan, get_interpretation 

# 1. 페이지 설정
st.set_page_config(page_title="The Element: Destiny Map", page_icon="🧭", layout="wide")

# 2. 스타일 및 배경 설정
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }

        .main-title {
            font-size: 3.0em; 
            color: #1e293b; 
            text-align: center; 
            font-weight: 800; 
            margin-bottom: 10px;
            font-family: 'Gowun Batang', serif;
        }
        .sub-desc {
            font-size: 1.3em;
            color: #475569; 
            text-align: center; 
            margin-bottom: 40px;
            font-weight: 500;
        }

        /* 입력창 라벨 */
        .stTextInput label p, .stDateInput label p, .stTimeInput label p, .stRadio label p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
        }

        /* 카드 스타일 */
        .card {
            background: rgba(255, 255, 255, 0.95); 
            padding: 30px; 
            border-radius: 15px; 
            border: 1px solid #e2e8f0; 
            margin-bottom: 20px; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
            text-align: center;
            font-family: 'Gowun Batang', serif;
        }
        
        /* 버튼 스타일 강화 */
        .stButton button {width: 100%; height: 50px; font-weight: bold; border-radius: 8px; font-size: 1rem; transition: all 0.3s;}
        .stLinkButton a {width: 100%; height: 50px; font-weight: bold; border-radius: 8px; text-align: center; display: flex; align-items: center; justify-content: center; font-size: 1rem;}
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바 설정
with st.sidebar:
    st.header("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
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

# 4. 텍스트 데이터
txt = {
    "ko": {
        "title": "🧭 운명의 나침반",
        "sub": "당신의 태어난 순간이 말해주는 운명의 지도를 펼쳐보세요.",
        "input_h": "👤 사주 정보 입력 (필수)",
        "name": "이름", "birth": "생년월일", "gender": "성별", "time": "태어난 시간", "unknown": "시간 모름",
        "btn": "✨ 내 운명 확인하기 (Free)",
        "warn_name": "이름을 입력해주세요.",
        "res_hello": "반갑습니다,",
        "res_msg": "당신은 <span style='color:#4f46e5; font-weight:bold;'>'{e_name}'</span>의 기운을 타고났습니다.",
        "menu_h": "💎 프리미엄 운세 스토어",
        "btn_check": "확인하기 ($10)",
        "btn_buy": "구매하기 ($30)",
        
        "s1_t": "🔮 2026 신년 운세", "s1_d": "2026년의 재물, 연애, 직장운을 미리 봅니다. 다가올 미래를 준비하세요.",
        "s2_t": "📅 그날의 운세", "s2_d": "면접, 데이트, 계약일 등 중요한 날의 기운을 미리 확인하세요.",
        "s3_t": "❤️ 사랑 궁합 (Love Match)", "s3_d": "그 사람과 나는 천생연분일까? 속마음과 연애 성향 분석.",
        "s4_t": "📆 택일 (좋은 날짜)", "s4_d": "결혼, 이사, 개업! 인생의 중요한 시작, 최고의 날짜를 잡아드립니다.",
        "s5_t": "🤝 비즈니스 파트너 궁합", "s5_d": "상사, 동업자, 직원과의 관계 분석. 성공적인 파트너십을 위한 처세술.",
        "s6_t": "👑 프리패스 (VIP)", "s6_d": "고민하지 마세요. 모든 유료 서비스를 한 번에 소장하세요! (할인)"
    },
    "en": {
        "title": "🧭 The Element: Destiny Map",
        "sub": "Discover the map of destiny hidden in your birth moment.",
        "input_h": "👤 Enter Your Details",
        "name": "Name", "birth": "Date of Birth", "gender": "Gender", "time": "Birth Time", "unknown": "Unknown Time",
        "btn": "✨ Analyze My Destiny (Free)",
        "warn_name": "Please enter your name.",
        "res_hello": "Hello,",
        "res_msg": "You are born with the energy of <span style='color:#4f46e5; font-weight:bold;'>'{e_name}'</span>.",
        "menu_h": "💎 Premium Store",
        "btn_check": "Check ($10)",
        "btn_buy": "Buy Pass ($30)",
        
        "s1_t": "🔮 2026 Forecast", "s1_d": "Prepare for 2026. Detailed analysis of Wealth, Love, and Career.",
        "s2_t": "📅 Specific Day Forecast", "s2_d": "Interview? Date? Check your luck for any specific day.",
        "s3_t": "❤️ Love Compatibility", "s3_d": "Are we a match? Analyze romantic chemistry with your partner.",
        "s4_t": "📆 Date Selection", "s4_d": "Wedding, Moving, Opening! Find the most auspicious dates.",
        "s5_t": "🤝 Business Compatibility", "s5_d": "Boss? Co-founder? Analyze professional synergy and teamwork.",
        "s6_t": "👑 All-Access Pass", "s6_d": "Unlock EVERYTHING at once. Best value for VIPs."
    }
}
t = txt[lang]

# 이미지 주소 설정
imgs = {
    "s1": "https://cdn-icons-png.flaticon.com/512/4333/4333609.png", 
    "s2": "https://cdn-icons-png.flaticon.com/512/9322/9322127.png", 
    "s3": "https://raw.githubusercontent.com/1country/global-saju-test/main/unnamed.jpg", 
    "s4": "https://cdn-icons-png.flaticon.com/512/1057/1057240.png", 
    "s5": "https://cdn-icons-png.flaticon.com/512/950/950575.png", 
    "s6": "https://cdn-icons-png.flaticon.com/512/6941/6941697.png" 
}

# 5. 메인 화면 구성
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

# --- 카드 그리기 도우미 함수 ---
def draw_premium_card(title, desc, btn_text, img_url, click_page=None, link_url=None):
    with st.container(border=True):
        col_img, col_text, col_btn = st.columns([1.2, 3.3, 1.5], gap="medium")
        
        with col_img:
            st.write("") 
            st.markdown(f"""
                <img src="{img_url}" 
                     style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            """, unsafe_allow_html=True)
            
        with col_text:
            st.subheader(title)
            st.write(desc)
            
        with col_btn:
            st.write("") 
            st.write("") 
            if click_page:
                # [수정됨] 페이지 이동 버튼
                if st.button(btn_text, key=title, use_container_width=True):
                    st.switch_page(click_page)
            elif link_url:
                # [수정됨] 외부 링크 버튼 (All-Access Pass용)
                st.link_button(btn_text, link_url, type="primary", use_container_width=True)

# 6. 결과 및 프리미엄 스토어
if st.session_state["analyzed"]:
    st.divider()
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    description = day_info['desc'] if lang == 'ko' else day_info['desc_en']
    detail_text = get_interpretation(day_info['element'], lang)
    
    st.markdown(f"""
    <div class='card'>
        <h3 style='color:#475569; margin:0;'>{t['res_hello']} <b>{st.session_state['user_name']}</b>!</h3>
        <p style='font-size:1.6em; margin-top:15px; color:#1e293b; line-height: 1.6;'>
            {t['res_msg'].format(e_name=day_info[lang])}
        </p>
        <p style='font-size:1em; color:#64748b; margin-top:5px;'>({description})</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(detail_text) 
        
    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader(t['menu_h'])

    # [수정 완료] VIP 프리패스: 구매 링크로 바로 이동 (실제 주소 적용)
    draw_premium_card(t['s6_t'], t['s6_d'], t['btn_buy'], imgs['s6'], link_url="https://5codes.gumroad.com/l/all-access_pass")
    
    # [수정 완료] 각 페이지 파일명 및 이모지를 실제 파일과 100% 일치시킴
    draw_premium_card(t['s1_t'], t['s1_d'], t['btn_check'], imgs['s1'], click_page="pages/1_🔮_2026_Forecast.py")
    
    # 2번 페이지 이름 수정 (Specific_Day.py)
    draw_premium_card(t['s2_t'], t['s2_d'], t['btn_check'], imgs['s2'], click_page="pages/2_📅_Specific_Day.py")
    
    # 3번 페이지 이름 및 이모지 수정 (💘)
    draw_premium_card(t['s3_t'], t['s3_d'], t['btn_check'], imgs['s3'], click_page="pages/3_💘_Love_Compatibility.py")
    
    # 4번 페이지 이름 및 이모지 수정 (🗓️)
    draw_premium_card(t['s4_t'], t['s4_d'], t['btn_check'], imgs['s4'], click_page="pages/4_🗓️_Date_Selection.py")
    
    # 5번 페이지 이름 및 이모지 수정 (💼)
    draw_premium_card(t['s5_t'], t['s5_d'], t['btn_check'], imgs['s5'], click_page="pages/5_💼_Business_Compatibility.py")
    

    st.divider()
    coffee_msg_bottom = "이 서비스가 도움이 되셨나요? 따뜻한 커피 한 잔은 개발자에게 큰 힘이 됩니다! ☕" if lang == "ko" else "Did you enjoy the service? A coffee would be a great support! ☕"
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; background-color: #f1f5f9; border-radius: 15px; margin-top: 20px;">
            <p style="font-size: 1.1em; color: #475569; margin-bottom: 20px; font-weight: bold; font-family: 'Gowun Batang', serif;">
                {coffee_msg_bottom}
            </p>
            <a href="https://buymeacoffee.com/5codes" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                    style="width: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 5px; transition: transform 0.2s;">
            </a>
        </div>
    """, unsafe_allow_html=True)
