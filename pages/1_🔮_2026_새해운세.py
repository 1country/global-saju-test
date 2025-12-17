import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
# 방금 만든 utils.py에서 도구를 빌려옵니다
from utils import calculate_day_gan, verify_license_flexible 

st.set_page_config(page_title="2026 신년 운세", page_icon="🔮")

# ----------------------------------------------------
# [설정] 상품 ID (나중에 Gumroad ID로 꼭 바꾸세요!)
# ----------------------------------------------------
CURRENT_PRODUCT_ID = "2026_forecast"   # 이 페이지 전용 ID ($10)
ALL_ACCESS_ID = "all_access_pass"      # 프리패스 ID ($20)

st.title("🔮 2026년 정밀 신년 운세")

# 1. 홈에서 입력한 정보가 없으면 내쫓기
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("⚠️ 메인 화면(Home)에서 정보를 먼저 입력해주세요.")
    st.switch_page("Home.py") # 홈으로 강제 이동

name = st.session_state["user_name"]
st.write(f"**{name}**님의 2026년 운명을 분석합니다...")

# 2. 잠금 확인
if "unlocked_2026" not in st.session_state: st.session_state["unlocked_2026"] = False

if not st.session_state["unlocked_2026"]:
    st.info("🔒 이 정보는 유료 콘텐츠입니다. ($10)")
    
    # 탭으로 구매 방식 안내
    tab1, tab2 = st.tabs(["단품 구매 ($10)", "프리패스 소지자"])
    
    with tab1:
        st.markdown(f"운세만 보시려면? [👉 구매하러 가기 (Click)](https://gum.co/{CURRENT_PRODUCT_ID})")
    with tab2:
        st.markdown("20불 프리패스를 구매하셨다면 해당 코드를 입력하세요.")

    # 코드 입력창
    key = st.text_input("라이센스 키 입력", type="password")
    
    if st.button("잠금 해제 (Unlock)"):
        # utils.py에 있는 만능 검증기 사용!
        is_valid, msg = verify_license_flexible(key, CURRENT_PRODUCT_ID, ALL_ACCESS_ID)
        
        if is_valid:
            st.session_state["unlocked_2026"] = True
            st.toast(msg, icon="✅")
            st.rerun()
        else:
            st.error(msg)

else:
    # ------------------------------------------------
    # 3. [유료] 잠금 해제된 결과 화면
    # ------------------------------------------------
    st.success("✅ 정품 인증 완료! 2026년 운세를 공개합니다.")
    
    # 내년 운세 로직 (간단 예시)
    day_info = calculate_day_gan(st.session_state["birth_date"])
    element = day_info['element']
    
    st.markdown(f"### 🌊 {day_info['ko']}의 2026년 흐름")
    st.write("내년에는 정말 대박이 나실 겁니다! (여기에 상세 운세 데이터가 들어갑니다)")
    
    # 인쇄 버튼
    st.divider()
    components.html(
        """<script>function printParent() { window.parent.print(); }</script>
           <button onclick="printParent()">🖨️ 결과 인쇄하기</button>""", 
        height=50
    )
