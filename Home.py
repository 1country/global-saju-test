import streamlit as st
from datetime import date, time
# utils.py가 같은 폴더에 있어야 합니다. (만세력 도구)
from utils import calculate_day_gan 

# 페이지 설정
st.set_page_config(
    page_title="운명의 나침반", 
    page_icon="🧭", 
    layout="wide"
)

# 세션 상태 초기화 (다른 페이지에서도 이 정보를 씁니다)
if "user_name" not in st.session_state: st.session_state["user_name"] = ""
if "birth_date" not in st.session_state: st.session_state["birth_date"] = date(1990, 1, 1)
if "birth_time" not in st.session_state: st.session_state["birth_time"] = time(12, 00)
if "time_unknown" not in st.session_state: st.session_state["time_unknown"] = False
if "gender" not in st.session_state: st.session_state["gender"] = "남성"
if "analyzed" not in st.session_state: st.session_state["analyzed"] = False

# --- 1. 헤더 ---
st.markdown("<h1 style='text-align: center; color: #1e293b;'>🧭 운명의 나침반</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1em;'>당신의 태어난 순간이 말해주는 운명의 지도를 펼쳐보세요.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 2. 사용자 정보 입력 (카드 형태 디자인) ---
st.markdown("### 👤 사주 정보 입력 (필수)")

with st.container():
    # 2단 컬럼 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("이름 (Name)", value=st.session_state["user_name"])
        gender = st.radio("성별 (Gender)", ["남성", "여성"], horizontal=True, index=0 if st.session_state["gender"]=="남성" else 1)
    
    with col2:
        b_date = st.date_input("생년월일 (Date of Birth)", 
                               min_value=date(1920,1,1), 
                               value=st.session_state["birth_date"])
        
        # [핵심] 시간 입력 + 모름 체크박스
        c_time, c_check = st.columns([2, 1])
        with c_check:
            st.write("") # 줄맞춤용 공백
            st.write("") 
            is_unknown = st.checkbox("시간 모름", value=st.session_state["time_unknown"])
        with c_time:
            b_time = st.time_input("태어난 시간 (Time)", 
                                   value=st.session_state["birth_time"], 
                                   disabled=is_unknown) # 체크하면 비활성화됨

    # 분석 시작 버튼
    if st.button("✨ 내 운명 확인하기 (Free)", type="primary", use_container_width=True):
        if name:
            # 세션에 저장 (전역 변수처럼 사용)
            st.session_state["user_name"] = name
            st.session_state["birth_date"] = b_date
            st.session_state["gender"] = gender
            st.session_state["time_unknown"] = is_unknown
            if not is_unknown:
                st.session_state["birth_time"] = b_time
            else:
                st.session_state["birth_time"] = None # 시간 모르면 None 저장
            
            st.session_state["analyzed"] = True # 분석 완료 플래그
            st.rerun() # 화면 새로고침
        else:
            st.warning("이름을 입력해주세요.")

# --- 3. 무료 결과 및 유료 메뉴판 ---
if st.session_state["analyzed"]:
    st.divider()
    
    # (1) 무료 본질 분석 결과 (일주)
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    st.success(f"반갑습니다, **{st.session_state['user_name']}**님!")
    
    # 결과 카드 디자인
    st.markdown(f"""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; margin-bottom: 30px;">
        <h3 style="color: #475569; margin:0;">당신은 <b>'{day_info['ko']}'</b>의 기운을 타고났습니다.</h3>
        <p style="color: #64748b; margin-top: 10px;">{day_info['desc']}</p>
        <div style="margin-top: 15px; font-size: 0.9em; color: #94a3b8;">
            (이것은 당신의 '본질'입니다. 더 자세한 미래가 궁금하다면 아래 서비스를 이용하세요.)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # (2) 유료 서비스 메뉴판 (Grid Layout)
    st.subheader("💎 프리미엄 운세 스토어")
    st.markdown("원하는 서비스를 선택하면 상세 페이지로 이동합니다.")

    menu_col1, menu_col2, menu_col3 = st.columns(3)

    # 메뉴 1: 2026 신년운세
    with menu_col1:
        st.info("🔮 **2026 신년 운세**\n\n내년의 재물, 연애, 직장운을 정밀하게 분석합니다.")
        if st.button("2026 운세 보기 ($10)"):
            st.switch_page("pages/1_🔮_2026_새해운세.py")

    # 메뉴 2: 택일 서비스
    with menu_col2:
        st.success("📆 **택일 (좋은 날짜)**\n\n결혼, 이사, 계약 등 중요한 날짜를 잡아드립니다.")
        if st.button("좋은 날짜 받기 ($5)"):
            st.switch_page("pages/2_📆_택일_서비스.py")

    # 메뉴 3: 궁합 or 프리패스
    with menu_col3:
        st.warning("👑 **프리패스 (All-Access)**\n\n모든 유료 서비스를 한 번에 이용하세요!")
        # 프리패스는 보통 페이지 이동보다는 구매 링크로 바로 유도하거나 안내 페이지로 감
        st.link_button("👉 프리패스 구매 ($20)", "https://gum.co/demo_product")

    # [추가] 사이드바 안내
    st.sidebar.info("👈 왼쪽 메뉴를 눌러서도 이동할 수 있습니다.")
