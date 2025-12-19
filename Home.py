import streamlit as st
from datetime import date, time
import time as tm # 로딩 애니메이션을 위해 필요
from utils import calculate_day_gan, get_interpretation 

# 1. 페이지 설정
st.set_page_config(page_title="The Element: Destiny Map", page_icon="🧭", layout="wide")

# 2. 스타일 및 배경 설정
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

        .stApp {
            /* 배경 이미지: 어두운 밤하늘 느낌으로 교체 (아이콘과 어울리게) */
            background-image: linear-gradient(rgba(20, 30, 48, 0.9), rgba(36, 59, 85, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #e2e8f0; /* 전체 텍스트 색상 밝게 변경 */
        }

        .main-title {
            font-size: 3.0em; 
            color: #f8fafc; /* 제목 밝은색 */
            font-weight: 800; 
            margin-bottom: 10px;
            font-family: 'Gowun Batang', serif;
        }
        .sub-desc {
            font-size: 1.3em;
            color: #cbd5e1; /* 부제목 밝은 회색 */
            margin-bottom: 40px;
            font-weight: 500;
        }

        /* 입력창 라벨 */
        .stTextInput label p, .stDateInput label p, .stTimeInput label p, .stRadio label p, .stCheckbox label p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #e2e8f0 !important; /* 라벨 밝은색 */
        }

        /* 카드 스타일 (어두운 배경에 맞춤) */
        .card {
            background: rgba(30, 41, 59, 0.95); /* 어두운 카드 배경 */
            padding: 30px; 
            border-radius: 15px; 
            border: 1px solid #334155; 
            margin-bottom: 20px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3); 
            text-align: center;
            font-family: 'Gowun Batang', serif;
            color: #f1f5f9;
        }
        
        /* 컨테이너 스타일 */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
             background: rgba(30, 41, 59, 0.8); /* 입력창 등 컨테이너 배경 */
             border: 1px solid #475569;
        }

        /* 버튼 스타일 강화 */
        .stButton button {width: 100%; height: 50px; font-weight: bold; border-radius: 8px; font-size: 1rem; transition: all 0.3s; background-color: #3b82f6; color: white; border: none;}
        .stButton button:hover {background-color: #2563eb;}
        .stLinkButton a {width: 100%; height: 50px; font-weight: bold; border-radius: 8px; text-align: center; display: flex; align-items: center; justify-content: center; font-size: 1rem; background-color: #8b5cf6; color: white;}
        
        h1, h2, h3, h4, p { color: #e2e8f0; } /* 기본 텍스트 밝게 */
        .stRadio div[role="radiogroup"] label { color: #e2e8f0 !important; }
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
            <p style="font-size: 14px; color: #cbd5e1; margin-top: 10px;">{coffee_msg}</p>
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
        "res_msg": "당신은 <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>의 기운을 타고났습니다.",
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
        "res_msg": "You are born with the energy of <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>.",
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

# 깃허브 기본 주소 (선생님 저장소 기준)
base_url = "https://raw.githubusercontent.com/1country/global-saju-test/main/images"

imgs = {
    "s1": f"{base_url}/s1.png", 
    "s2": f"{base_url}/s2.png", 
    "s3": f"{base_url}/s3.png", 
    "s4": f"{base_url}/s4.png", 
    "s5": f"{base_url}/s5.png", 
    "s6": f"{base_url}/s6.png" 
}

# 5. 메인 화면 구성 (Hero Section - 상단 디자인 강화)
with st.container():
    col1, col2 = st.columns([1, 2.5]) # 왼쪽: 이미지, 오른쪽: 텍스트
    
    with col1:
        # 브랜드 메인 이미지 (All-Access Pass 이미지 활용)
        st.image(imgs['s6'], use_container_width=True)
        
    with col2:
        st.markdown(f"<div style='text-align: left; margin-top: 20px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='main-title' style='text-align: left;'>{t['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sub-desc' style='text-align: left; margin-bottom: 20px;'>{t['sub']}</div>", unsafe_allow_html=True)
        
        # 신뢰감 뱃지
        st.markdown(f"""
            <div style='display: flex; gap: 15px;'>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>✨ AI Based Analysis</span>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>📜 Asian Wisdom</span>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>🔒 Privacy Protected</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") 
st.write("") 

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

    st.write("")
    # [애니메이션 효과] 버튼 클릭 시 로딩 연출
    if st.button(t['btn'], type="primary", use_container_width=True):
        if name:
            # 로딩 메시지와 함께 스피너 표시
            loading_msg = '운명의 지도를 펼치는 중입니다...' if lang == 'ko' else 'Unfolding your destiny map...'
            with st.spinner(loading_msg):
                tm.sleep(2.0) # 2초간 딜레이를 주어 분석하는 느낌 연출
                
                st.session_state["user_name"] = name
                st.session_state["birth_date"] = b_date
                st.session_state["gender"] = gender
                st.session_state["time_unknown"] = is_unknown
                st.session_state["birth_time"] = None if is_unknown else b_time
                st.session_state["analyzed"] = True
                st.rerun()
        else:
            st.warning(t['warn_name'])

# [신뢰감 형성 섹션] 입력창 아래 아이콘 (결과 나오기 전)
if not st.session_state["analyzed"]:
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 아이콘 주소
    icon_url_1 = f"{base_url}/icon1.png"
    icon_url_2 = f"{base_url}/icon2.png"
    icon_url_3 = f"{base_url}/icon3.png"
    
    # ⭐ [핵심] 아이콘 스타일: 부드럽게 녹아드는 원형 마스크 효과 ⭐
    # mask-image를 사용하여 중심부는 선명하고(black), 가장자리는 투명하게(transparent) 만듭니다.
    icon_style = """
        width: 110px;
        height: 110px;
        object-fit: cover;
        border-radius: 50%; /* 기본 원형 */
        margin-bottom: 15px;
        /* 크롬, 사파리용 마스크 */
        -webkit-mask-image: radial-gradient(circle at center, black 50%, transparent 100%);
        /* 표준 마스크 */
        mask-image: radial-gradient(circle at center, black 50%, transparent 100%);
    """
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_1}" style="{icon_style}">
                <h4 style="margin-top: 0; color: #f8fafc;">Ancient Wisdom</h4>
                <p style="color: #cbd5e1; font-size: 0.9em;">동양의 깊은 명리학적 지혜</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_f2:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_2}" style="{icon_style}">
                <h4 style="margin-top: 0; color: #f8fafc;">Modern Insight</h4>
                <p style="color: #cbd5e1; font-size: 0.9em;">AI 기술을 결합한 정밀 분석</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_f3:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_3}" style="{icon_style}">
                <h4 style="margin-top: 0; color: #f8fafc;">Premium Keys</h4>
                <p style="color: #cbd5e1; font-size: 0.9em;">인생의 해답을 여는 마스터 키</p>
            </div>
        """, unsafe_allow_html=True)


# --- 카드 그리기 도우미 함수 ---
def draw_premium_card(title, desc, btn_text, img_url, click_page=None, link_url=None):
    with st.container(border=True):
        col_img, col_text, col_btn = st.columns([1.2, 3.3, 1.5], gap="medium")
        
        with col_img:
            st.write("") 
            st.markdown(f"""
                <img src="{img_url}" 
                     style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            """, unsafe_allow_html=True)
            
        with col_text:
            st.subheader(title)
            st.write(desc)
            
        with col_btn:
            st.write("") 
            st.write("") 
            if click_page:
                if st.button(btn_text, key=title, use_container_width=True):
                    st.switch_page(click_page)
            elif link_url:
                st.link_button(btn_text, link_url, type="primary", use_container_width=True)

# 6. 결과 및 프리미엄 스토어
if st.session_state["analyzed"]:
    st.divider()
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    description = day_info['desc'] if lang == 'ko' else day_info['desc_en']
    detail_text = get_interpretation(day_info['element'], lang)
    
    st.markdown(f"""
    <div class='card'>
        <h3 style='color:#cbd5e1; margin:0;'>{t['res_hello']} <b>{st.session_state['user_name']}</b>!</h3>
        <p style='font-size:1.6em; margin-top:15px; color:#f8fafc; line-height: 1.6;'>
            {t['res_msg'].format(e_name=day_info[lang])}
        </p>
        <p style='font-size:1em; color:#94a3b8; margin-top:5px;'>({description})</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(detail_text) 
        
    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader(t['menu_h'])

    # VIP 프리패스
    draw_premium_card(t['s6_t'], t['s6_d'], t['btn_buy'], imgs['s6'], link_url="https://5codes.gumroad.com/l/all-access_pass")
    
    # 각 서비스별 페이지 연결
    draw_premium_card(t['s1_t'], t['s1_d'], t['btn_check'], imgs['s1'], click_page="pages/1_🔮_2026_Forecast.py")
    draw_premium_card(t['s2_t'], t['s2_d'], t['btn_check'], imgs['s2'], click_page="pages/2_📅_Specific_Day.py")
    draw_premium_card(t['s3_t'], t['s3_d'], t['btn_check'], imgs['s3'], click_page="pages/3_💘_Love_Compatibility.py")
    draw_premium_card(t['s4_t'], t['s4_d'], t['btn_check'], imgs['s4'], click_page="pages/4_🗓️_Date_Selection.py")
    draw_premium_card(t['s5_t'], t['s5_d'], t['btn_check'], imgs['s5'], click_page="pages/5_💼_Business_Compatibility.py")
    

    st.divider()
    coffee_msg_bottom = "이 서비스가 도움이 되셨나요? 따뜻한 커피 한 잔은 개발자에게 큰 힘이 됩니다! ☕" if lang == "ko" else "Did you enjoy the service? A coffee would be a great support! ☕"
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: rgba(30, 41, 59, 0.8); border-radius: 15px; margin-top: 20px; border: 1px solid #475569;">
            <p style="font-size: 1.1em; color: #cbd5e1; margin-bottom: 20px; font-weight: bold; font-family: 'Gowun Batang', serif;">
                {coffee_msg_bottom}
            </p>
            <a href="https://buymeacoffee.com/5codes" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                    style="width: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 5px; transition: transform 0.2s;">
            </a>
        </div>
    """, unsafe_allow_html=True)
