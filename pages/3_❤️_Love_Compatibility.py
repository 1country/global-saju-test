import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Love Compatibility", page_icon="💘", layout="wide")

# 🔑 [마스터 키 & 검로드 설정] - 선생님이 수정할 곳!
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "love_compatibility"  # 검로드 주소 맨 끝 단어
GUMROAD_LINK = "https://gumroad.com/l/love_compatibility"

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #be185d; margin-bottom: 10px; text-align: center;}
        
        /* 리포트 컨테이너 스타일 */
        .report-container {
            background-color: white; padding: 40px; border-radius: 20px;
            box-shadow: 0 10px 40px rgba(236, 72, 153, 0.15); border: 1px solid #fce7f3;
        }
        .section-box {
            margin-bottom: 30px; padding: 25px; border-radius: 15px; background-color: #fff1f2;
        }
        .section-title {
            font-size: 1.4em; font-weight: bold; color: #9d174d; margin-bottom: 15px; display: flex; align-items: center;
        }
        .content-text { font-size: 1.1em; line-height: 1.8; color: #374151; text-align: justify; }
        .score-display { text-align: center; font-size: 3em; font-weight: bold; color: #be185d; margin: 20px 0; }
        
        .user-card {
            background: white; padding: 15px; border-radius: 10px; border: 1px solid #e5e7eb;
            text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .vs-badge {
            display: flex; justify-content: center; align-items: center; 
            font-size: 1.5em; font-weight: bold; color: #db2777; height: 100%;
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
# 3. 궁합 분석 로직 (성별/오행 정밀 분석)
# ----------------------------------------------------------------
def get_love_report(u_elem, p_elem, u_gender, p_gender, lang):
    # 오행 상생상극 관계 계산
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    rel = relations[u_elem][p_elem]
    
    # 텍스트 템플릿 (방대한 분량)
    # logic: u_gender 기준 (Male/Female)
    
    reports = {
        "Same": { # 비견 (친구 같은 관계)
            "score": 85,
            "title": "🤝 친구처럼 편안하지만, 자존심 대결이 필요한 커플",
            "chemistry": "두 분은 마치 거울을 보는 듯 서로 닮은 점이 많습니다. 처음 만났을 때부터 대화가 잘 통하고, 서로의 생각이나 취향이 비슷해 금방 가까워졌을 것입니다. '말하지 않아도 아는' 텔레파시가 통하는 사이입니다. 하지만 두 분 다 자아가 강해서 한번 싸움이 붙으면 누구 하나 굽히지 않고 불같이 다툴 수 있습니다.",
            "conflict": "가장 큰 걸림돌은 '자존심'입니다. 서로가 서로를 너무 잘 알기에, 상대방의 아픈 구석을 찌르는 말을 할 수 있습니다. 특히 의견 차이가 있을 때 논리로 이기려 들면 관계가 급격히 냉각됩니다.",
            "intimacy": "속궁합이나 스킨십 호흡은 아주 좋습니다. 친구처럼 장난치듯 시작해서 열정적으로 변하는 타입입니다. 서로의 컨디션을 잘 이해해주기 때문에 편안한 관계를 유지합니다.",
            "advice": "서로를 '연인'이면서 동시에 '가장 친한 친구'로 대하세요. 싸울 때는 잠시 시간을 갖고 열을 식히는 것이 필수입니다. 남자가 조금 더 져주는 척하면 여자는 금방 마음을 풉니다."
        },
        "Output": { # 내가 생해주는 관계 (헌신)
            "score": 90,
            "title": "💖 내가 더 많이 아껴주고 챙겨주는 '찐사랑' 커플",
            "chemistry": f"당신({u_elem})이 상대방({p_elem})을 자식처럼 예뻐하고 챙겨주는 형국입니다. 당신의 눈에는 상대방이 마냥 귀엽고 사랑스러워 보입니다. 상대방 역시 당신의 보살핌 속에서 편안함을 느끼고 의지하게 됩니다. 주는 기쁨과 받는 기쁨이 조화를 이루는 아주 이상적인 관계입니다.",
            "conflict": "당신이 너무 퍼주다 보면 어느 순간 '나만 노력하나?'라는 서운함이 몰려올 수 있습니다. 상대방이 당신의 배려를 당연하게 여기기 시작할 때 갈등이 생깁니다. 잔소리가 늘어날 수 있으니 주의해야 합니다.",
            "intimacy": "당신이 리드하고 상대방이 따라오는 형태입니다. 감정적인 교감이 풍부하며, 분위기를 중요하게 생각하는 로맨틱한 시간이 될 것입니다.",
            "advice": "일방적인 희생은 오래가지 못합니다. 상대방에게도 작은 역할을 맡기세요. '이거 해줘서 고마워'라는 칭찬을 자주 주고받아야 사랑이 더욱 단단해집니다."
        },
        "Wealth": { # 내가 극하는 관계 (소유/관리)
            "score": 80,
            "title": "🔥 강렬한 끌림, 서로를 원하지만 주도권 싸움이 있는 커플",
            "chemistry": f"당신({u_elem})에게 상대방({p_elem})은 '내 것으로 만들고 싶은' 매력적인 존재입니다. 남자가 여자를 만났을 때 가장 이상적인 배치 중 하나입니다(남자가 여자를 리드함). 하지만 여자가 남자를 만난 경우라면, 여자가 남자를 쥐락펴락하며 리드하는 '카리스마 커플'이 됩니다. 서로에 대한 소유욕이 강합니다.",
            "conflict": "당신이 상대방을 통제하려 들 때 숨막힘을 느낄 수 있습니다. '너를 위해서'라는 핑계로 상대방의 일거수일투족을 간섭하면 큰 싸움이 됩니다. 집착은 금물입니다.",
            "intimacy": "성적인 매력이 가장 강하게 작용하는 관계입니다. 서로를 강렬하게 원하며, 육체적인 만족도가 매우 높습니다. 권태기가 쉽게 오지 않는 뜨거운 커플입니다.",
            "advice": "상대방을 내 뜻대로 바꾸려 하지 말고 있는 그대로 인정해주세요. 서로의 사생활을 존중해줄 때 관계가 롱런할 수 있습니다."
        },
        "Power": { # 나를 극하는 관계 (압박/존경)
            "score": 75,
            "title": "⚖️ 긴장감과 존경심 사이, 서로를 성장시키는 커플",
            "chemistry": f"상대방({p_elem})이 당신({u_elem})을 통제하거나 억누르는 기운입니다. 여자가 남자를 만났을 때 가장 전통적이고 안정적인 배치입니다(남자가 여자를 보호하고 리드함). 하지만 남자가 여자를 만난 경우라면, 여자의 기가 세서 남자가 눈치를 보는 '공처가' 스타일이 될 수 있습니다.",
            "conflict": "상대방의 말이나 행동이 당신에게는 스트레스로 다가올 수 있습니다. 상대방은 '조언'이라고 하지만 당신에게는 '지적'으로 들립니다. 이로 인한 억울함이 쌓이면 폭발할 수 있습니다.",
            "intimacy": "다소 보수적이거나 상대방의 페이스에 말려들 수 있습니다. 하지만 신뢰가 쌓이면 깊은 안정감을 주는 관계입니다.",
            "advice": "당신이 느끼는 압박감을 솔직하게 표현하세요. 상대방은 당신을 힘들게 하려는 게 아니라 잘되게 하려는 마음이 큽니다. 대화의 방식을 부드럽게 바꾸면 최고의 파트너가 됩니다."
        },
        "Resource": { # 나를 생해주는 관계 (받음)
            "score": 95,
            "title": "🍼 엄마와 아이처럼, 조건 없는 사랑을 받는 커플",
            "chemistry": f"상대방({p_elem})이 당신({u_elem})을 헌신적으로 도와주고 아껴주는 관계입니다. 당신은 가만히 있어도 사랑받는 느낌을 받습니다. 힘들 때 가장 먼저 생각나는 안식처 같은 사람입니다. 정서적인 안정감이 최고조에 달하는 찰떡궁합입니다.",
            "conflict": "너무 편안하다 보니 관계가 루즈해지거나, 당신이 게을러질 수 있습니다. 또한 상대방의 과잉보호가 간섭으로 느껴질 때 다툼이 생깁니다. '엄마 잔소리'처럼 듣지 않도록 주의하세요.",
            "intimacy": "포근하고 부드러운 스킨십이 주를 이룹니다. 자극적인 것보다는 서로를 위로하고 감싸주는 힐링의 시간이 됩니다.",
            "advice": "받는 것에 익숙해지지 말고, 고마움을 자주 표현하세요. 상대방도 가끔은 당신에게 기대고 싶어 합니다. 작은 선물이나 이벤트로 감동을 주세요."
        }
    }
    
    # 성별에 따른 미세 조정 (Logic)
    data = reports[rel]
    
    # 남자가 여자를 만났을 때 (Traditional View adjustment)
    if u_gender == "Male" and p_gender == "Female":
        if rel == "Wealth": data['title'] += " (남자가 리드하는 이상적 관계)"
        if rel == "Power": data['title'] += " (여자의 기가 조금 센 관계)"
    
    # 여자가 남자를 만났을 때
    if u_gender == "Female" and p_gender == "Male":
        if rel == "Power": data['title'] += " (남자가 듬직하게 지켜주는 관계)"
        if rel == "Wealth": data['title'] += " (여자가 남자를 휘어잡는 관계)"

    return data

# ----------------------------------------------------------------
# 4. 메인 화면 로직
# ----------------------------------------------------------------

# (1) 사용자 정보 체크 (Home에서 입력 안했으면 쫓아내기)
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("⚠️ 홈 화면에서 본인 정보를 먼저 입력해주세요.")
    if st.button("홈으로 이동"): st.switch_page("Home.py")
    st.stop()

# 사용자 정보 로드
u_name = st.session_state["user_name"]
u_dob = st.session_state["birth_date"]
u_gender = st.session_state.get("gender", "Male")
u_time = st.session_state.get("birth_time", "Unknown")

ui = {
    "ko": {
        "title": "💘 프리미엄 궁합 분석",
        "sub": "두 사람의 영혼, 성격, 그리고 미래까지 꿰뚫어보는 심층 리포트",
        "p_info_title": "상대방 정보 입력 (Partner Info)",
        "p_name": "상대방 이름",
        "p_dob": "상대방 생년월일",
        "p_time": "태어난 시간 (모르면 무시)",
        "p_gender": "상대방 성별",
        "lock_title": "🔒 궁합 리포트 잠금 ($10)",
        "lock_desc": "결제 후 발급받은 라이센스 키를 입력하세요.",
        "lock_warn": "⚠️ 주의: 이 라이센스 키는 최대 3회까지만 조회 가능합니다.",
        "btn_buy": "💳 이용권 구매하기 ($10)",
        "btn_unlock": "결과 확인하기",
        "btn_print": "🖨️ 리포트 인쇄하기"
    },
    "en": {
        "title": "💘 Premium Love Compatibility",
        "sub": "Deep analysis of souls, personalities, and future.",
        "p_info_title": "Partner Information",
        "p_name": "Partner Name",
        "p_dob": "Partner DOB",
        "p_time": "Birth Time (Optional)",
        "p_gender": "Partner Gender",
        "lock_title": "🔒 Report Locked ($10)",
        "lock_desc": "Enter the license key after purchase.",
        "lock_warn": "⚠️ Warning: This key can be used up to 3 times only.",
        "btn_buy": "💳 Buy Access ($10)",
        "btn_unlock": "Unlock Report",
        "btn_print": "🖨️ Print Report"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.info(f"{t['sub']} (User: {u_name})")

# ----------------------------------------------------------------
# 5. 상대방 정보 입력 폼
# ----------------------------------------------------------------
with st.container(border=True):
    st.subheader(t['p_info_title'])
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input(t['p_name'])
        p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1990,1,1))
    with c2:
        # 성별 자동 제안 (내가 남자면 상대는 여자로 기본값)
        default_idx = 1 if u_gender == "Male" else 0
        p_gender = st.selectbox(t['p_gender'], ["Male", "Female"], index=default_idx)
        p_time = st.time_input(t['p_time'], value=None)

# ----------------------------------------------------------------
# 6. 잠금 및 결제 시스템 (3회 제한 팝업 포함)
# ----------------------------------------------------------------
if "unlocked_love" not in st.session_state: st.session_state["unlocked_love"] = False

if not st.session_state["unlocked_love"]:
    st.divider()
    with st.container(border=True):
        st.markdown(f"### {t['lock_title']}")
        st.write(t['lock_desc'])
        
        # 🚨 3회 제한 경고 (팝업 대신 눈에 띄는 경고 박스)
        st.warning(t['lock_warn'], icon="⚠️")
        
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        
        key = st.text_input("License Key", type="password")
        if st.button(t['btn_unlock'], type="primary"):
            if not p_name:
                st.error("상대방 이름을 입력해주세요.")
            else:
                # 1. 마스터키
                if key == UNLOCK_CODE:
                    st.session_state["unlocked_love"] = True
                    st.success("Developer Access Granted!")
                    st.rerun()
                
                # 2. 검로드 확인
                try:
                    response = requests.post(
                        "https://api.gumroad.com/v2/licenses/verify",
                        data={"product_permalink": PRODUCT_PERMALINK, "license_key": key}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        uses = data.get("uses", 0)
                        if uses > 3:
                            st.error(f"🚫 횟수 초과! (Used: {uses}/3). 추가 구매가 필요합니다.")
                        else:
                            st.session_state["unlocked_love"] = True
                            st.toast(f"✅ 인증 성공! (남은 횟수: {3-uses}회)")
                            st.rerun()
                    else:
                        st.error("🚫 유효하지 않은 키입니다.")
                except:
                    st.error("통신 오류가 발생했습니다.")
    st.stop()

# ----------------------------------------------------------------
# 7. 결과 리포트 생성
# ----------------------------------------------------------------
if st.session_state["unlocked_love"]:
    st.divider()
    
    # 오행 계산
    u_info = calculate_day_gan(u_dob)
    p_info = calculate_day_gan(p_dob)
    
    # 리포트 데이터 가져오기
    report = get_love_report(u_info['element'], p_info['element'], u_gender, p_gender, lang)
    
    # --- UI 렌더링 ---
    
    # 1. 대결 구도 (카드)
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.markdown(f"""
        <div class='user-card'>
            <div style='color:#6b7280;'>ME ({u_gender})</div>
            <div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{u_name}</div>
            <div style='font-size:1.2em; color:#db2777;'>{u_info[lang]} ({u_info['element']})</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-badge'>❤️</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='user-card'>
            <div style='color:#6b7280;'>PARTNER ({p_gender})</div>
            <div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{p_name}</div>
            <div style='font-size:1.2em; color:#db2777;'>{p_info[lang]} ({p_info['element']})</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. 메인 리포트
    st.markdown(f"""
    <div class='report-container'>
        <div class='score-display'>
            궁합 점수: {report['score']}점
        </div>
        <h2 style='text-align:center; color:#831843; margin-bottom:40px;'>{report['title']}</h2>
        
        <div class='section-box'>
            <div class='section-title'>🔮 성격과 케미 (Chemistry)</div>
            <div class='content-text'>{report['chemistry']}</div>
        </div>
        
        <div class='section-box'>
            <div class='section-title'>⚔️ 갈등 포인트 (Conflict)</div>
            <div class='content-text'>{report['conflict']}</div>
        </div>
        
        <div class='section-box'>
            <div class='section-title'>💋 속궁합 & 애정 (Intimacy)</div>
            <div class='content-text'>{report['intimacy']}</div>
        </div>
        
        <div class='section-box' style='background-color: #fdf2f8; border: 1px solid #fbcfe8;'>
            <div class='section-title'>🚀 관계를 위한 조언 (Advice)</div>
            <div class='content-text' style='font-weight:bold; color:#be185d;'>{report['advice']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. 인쇄 버튼
    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#be185d; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(190, 24, 93, 0.3);">
            {t['btn_print']}
            </button>
        </div>""", height=100
    )
