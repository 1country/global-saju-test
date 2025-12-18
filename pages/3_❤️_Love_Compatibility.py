import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Love Compatibility", page_icon="💘", layout="wide")

# 🔑 [마스터 키 & 검로드 설정]
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "love_match" 
GUMROAD_LINK = "https://gumroad.com/l/선생님의_궁합상품_주소"

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
# 3. 궁합 분석 로직 (영어 데이터 추가됨!)
# ----------------------------------------------------------------
def get_love_report(u_elem, p_elem, u_gender, p_gender, lang):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    rel = relations[u_elem][p_elem]
    
    # 리포트 데이터 (한국어/영어 분리)
    reports = {
        "Same": {
            "score": 85,
            "ko": {
                "title": "🤝 친구처럼 편안하지만, 자존심 대결이 필요한 커플",
                "chemistry": "두 분은 마치 거울을 보는 듯 서로 닮은 점이 많습니다. '말하지 않아도 아는' 텔레파시가 통하는 사이입니다. 하지만 두 분 다 자아가 강해서 한번 싸움이 붙으면 불같이 다툴 수 있습니다.",
                "conflict": "가장 큰 걸림돌은 '자존심'입니다. 서로가 서로를 너무 잘 알기에, 아픈 구석을 찌르는 말을 할 수 있습니다.",
                "intimacy": "속궁합은 아주 좋습니다. 친구처럼 장난치듯 시작해서 열정적으로 변하는 타입입니다.",
                "advice": "서로를 '연인'이면서 동시에 '가장 친한 친구'로 대하세요. 남자가 조금 더 져주는 척하면 여자는 금방 마음을 풉니다."
            },
            "en": {
                "title": "🤝 Like Friends, But Watch Out for Ego Clashes",
                "chemistry": "You two are like mirrors reflecting each other. Telepathy works between you. However, since both have strong egos, fights can be intense.",
                "conflict": "The biggest obstacle is 'Pride'. You know each other so well that words can hurt deeply.",
                "intimacy": "Physical chemistry is excellent. It starts playfully like friends and becomes passionate.",
                "advice": "Treat each other as 'Best Friends' and lovers. If the man yields a little, the woman will soften quickly."
            }
        },
        "Output": {
            "score": 90,
            "ko": {
                "title": "💖 내가 더 많이 아껴주고 챙겨주는 '찐사랑' 커플",
                "chemistry": f"당신({u_elem})이 상대방({p_elem})을 자식처럼 예뻐하고 챙겨주는 형국입니다. 주는 기쁨과 받는 기쁨이 조화를 이루는 아주 이상적인 관계입니다.",
                "conflict": "당신이 너무 퍼주다 보면 '나만 노력하나?'라는 서운함이 몰려올 수 있습니다. 잔소리가 늘어날 수 있으니 주의해야 합니다.",
                "intimacy": "당신이 리드하고 상대방이 따라오는 형태입니다. 감정적인 교감이 풍부한 로맨틱한 관계입니다.",
                "advice": "일방적인 희생은 금물입니다. 상대방에게도 작은 역할을 맡기세요."
            },
            "en": {
                "title": "💖 True Love: You Care More & Give More",
                "chemistry": f"You ({u_elem}) care for your partner ({p_elem}) like a parent cares for a child. It's an ideal balance of giving and receiving.",
                "conflict": "You might feel unfair if you give too much. Beware of becoming too nagging.",
                "intimacy": "You lead, and your partner follows. A very romantic and emotional connection.",
                "advice": "One-sided sacrifice won't last. Let your partner take some responsibilities too."
            }
        },
        "Wealth": {
            "score": 80,
            "ko": {
                "title": "🔥 강렬한 끌림, 주도권 싸움이 있는 커플",
                "chemistry": f"당신({u_elem})에게 상대방({p_elem})은 '내 것으로 만들고 싶은' 매력적인 존재입니다. 소유욕과 끌림이 매우 강합니다.",
                "conflict": "상대방을 통제하려 들 때 숨막힘을 느낄 수 있습니다. 집착은 금물입니다.",
                "intimacy": "성적인 매력이 가장 강하게 작용하는 관계입니다. 육체적인 만족도가 매우 높습니다.",
                "advice": "상대방을 내 뜻대로 바꾸려 하지 말고 있는 그대로 인정해주세요."
            },
            "en": {
                "title": "🔥 Intense Attraction with Power Struggles",
                "chemistry": f"You ({u_elem}) find your partner ({p_elem}) irresistibly attractive and want to 'possess' them.",
                "conflict": "Controlling behavior can suffocate the relationship. Avoid obsession.",
                "intimacy": "Sexual attraction is strongest here. Physical satisfaction is very high.",
                "advice": "Don't try to change your partner. Respect them as they are."
            }
        },
        "Power": {
            "score": 75,
            "ko": {
                "title": "⚖️ 긴장감과 존경심 사이, 서로를 성장시키는 커플",
                "chemistry": f"상대방({p_elem})이 당신({u_elem})을 리드하거나 억누르는 기운입니다. 다소 보수적일 수 있지만 안정적인 관계입니다.",
                "conflict": "상대방의 조언이 당신에게는 '지적'이나 '스트레스'로 들릴 수 있습니다.",
                "intimacy": "신뢰가 쌓이면 깊은 안정감을 주는 관계입니다.",
                "advice": "당신이 느끼는 압박감을 솔직하게 표현하세요. 대화가 중요합니다."
            },
            "en": {
                "title": "⚖️ Tension & Respect: Growing Together",
                "chemistry": f"Your partner ({p_elem}) leads or pressures you ({u_elem}). It can be traditional but stable.",
                "conflict": "Their advice might feel like criticism or stress to you.",
                "intimacy": "Provides deep stability once trust is built.",
                "advice": "Express your feelings of pressure honestly. Communication is key."
            }
        },
        "Resource": {
            "score": 95,
            "ko": {
                "title": "🍼 엄마와 아이처럼, 조건 없는 사랑을 받는 커플",
                "chemistry": f"상대방({p_elem})이 당신({u_elem})을 헌신적으로 도와줍니다. 정서적인 안정감이 최고조에 달하는 찰떡궁합입니다.",
                "conflict": "너무 편안해서 관계가 루즈해지거나, 상대방의 과잉보호가 간섭으로 느껴질 수 있습니다.",
                "intimacy": "포근하고 부드러운 스킨십이 주를 이룹니다. 힐링이 되는 관계입니다.",
                "advice": "고마움을 자주 표현하세요. 작은 선물이나 이벤트로 감동을 주세요."
            },
            "en": {
                "title": "🍼 Unconditional Love: Like Mother & Child",
                "chemistry": f"Your partner ({p_elem}) supports you devotedly. You feel emotionally secure and loved.",
                "conflict": "Comfort might lead to laziness, or care might feel like interference.",
                "intimacy": "Cozy and gentle physical connection. A healing relationship.",
                "advice": "Express gratitude often. Surprise them with small gifts."
            }
        }
    }
    
    # 1. 점수 가져오기
    base_data = reports[rel]
    score = base_data["score"]
    
    # 2. 언어에 맞는 데이터 가져오기 (ko 또는 en)
    data = base_data[lang]
    
    # 3. 성별 미세 조정 (Logic)
    # 영어 모드에서도 제목에 뉘앙스를 추가해줍니다.
    add_on = ""
    if u_gender == "Male" and p_gender == "Female":
        if rel == "Wealth": 
            add_on = " (Ideal: Man leads)" if lang == "en" else " (남자가 리드하는 이상적 관계)"
        if rel == "Power": 
            add_on = " (Woman is strong)" if lang == "en" else " (여자의 기가 조금 센 관계)"
    
    if u_gender == "Female" and p_gender == "Male":
        if rel == "Power": 
            add_on = " (Ideal: Man protects)" if lang == "en" else " (남자가 듬직하게 지켜주는 관계)"
        if rel == "Wealth": 
            add_on = " (Woman takes lead)" if lang == "en" else " (여자가 남자를 휘어잡는 관계)"

    return {
        "score": score,
        "title": data['title'] + add_on,
        "chemistry": data['chemistry'],
        "conflict": data['conflict'],
        "intimacy": data['intimacy'],
        "advice": data['advice']
    }

# ----------------------------------------------------------------
# 4. 메인 화면 로직
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("Please enter your info at Home first." if lang == "en" else "⚠️ 홈 화면에서 본인 정보를 먼저 입력해주세요.")
    if st.button("Go Home" if lang == "en" else "홈으로 이동"): st.switch_page("Home.py")
    st.stop()

u_name = st.session_state["user_name"]
u_dob = st.session_state["birth_date"]
u_gender = st.session_state.get("gender", "Male")

# UI 텍스트 (영어/한글)
ui = {
    "ko": {
        "title": "💘 프리미엄 궁합 분석",
        "sub": "두 사람의 영혼, 성격, 그리고 미래까지 꿰뚫어보는 심층 리포트",
        "p_info_title": "상대방 정보 입력",
        "p_name": "상대방 이름",
        "p_dob": "상대방 생년월일",
        "p_gender": "상대방 성별",
        "lock_title": "🔒 궁합 리포트 잠금 ($10)",
        "lock_desc": "결제 후 발급받은 라이센스 키를 입력하세요.",
        "lock_warn": "⚠️ 주의: 이 라이센스 키는 최대 3회까지만 조회 가능합니다.",
        "btn_buy": "💳 이용권 구매하기 ($10)",
        "btn_unlock": "결과 확인하기",
        "btn_print": "🖨️ 리포트 인쇄하기",
        "sec_chem": "🔮 성격과 케미 (Chemistry)",
        "sec_conf": "⚔️ 갈등 포인트 (Conflict)",
        "sec_inti": "💋 속궁합 & 애정 (Intimacy)",
        "sec_adv": "🚀 관계를 위한 조언 (Advice)",
        "score_label": "궁합 점수"
    },
    "en": {
        "title": "💘 Premium Love Compatibility",
        "sub": "Deep analysis of souls, personalities, and future.",
        "p_info_title": "Partner Information",
        "p_name": "Partner Name",
        "p_dob": "Partner DOB",
        "p_gender": "Partner Gender",
        "lock_title": "🔒 Report Locked ($10)",
        "lock_desc": "Enter the license key after purchase.",
        "lock_warn": "⚠️ Warning: This key can be used up to 3 times only.",
        "btn_buy": "💳 Buy Access ($10)",
        "btn_unlock": "Unlock Report",
        "btn_print": "🖨️ Print Report",
        "sec_chem": "🔮 Chemistry & Personality",
        "sec_conf": "⚔️ Conflict Points",
        "sec_inti": "💋 Intimacy & Love",
        "sec_adv": "🚀 Advice for Relationship",
        "score_label": "Compatibility Score"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.info(f"{t['sub']} (User: {u_name})")

# 5. 상대방 정보 입력
with st.container(border=True):
    st.subheader(t['p_info_title'])
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input(t['p_name'])
        p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1990,1,1))
    with c2:
        default_idx = 1 if u_gender == "Male" else 0
        p_gender = st.selectbox(t['p_gender'], ["Male", "Female"], index=default_idx)

# 6. 잠금 및 결제 (3회 제한 경고 영어 지원)
if "unlocked_love" not in st.session_state: st.session_state["unlocked_love"] = False

if not st.session_state["unlocked_love"]:
    st.divider()
    with st.container(border=True):
        st.markdown(f"### {t['lock_title']}")
        st.write(t['lock_desc'])
        st.warning(t['lock_warn'], icon="⚠️") # 이제 영어일 땐 영어 경고가 나옵니다
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        
        key = st.text_input("License Key", type="password")
        if st.button(t['btn_unlock'], type="primary"):
            if not p_name:
                st.error("Please enter partner's name." if lang=="en" else "상대방 이름을 입력해주세요.")
            else:
                if key == UNLOCK_CODE:
                    st.session_state["unlocked_love"] = True
                    st.success("Developer Access Granted!")
                    st.rerun()
                try:
                    response = requests.post(
                        "https://api.gumroad.com/v2/licenses/verify",
                        data={"product_permalink": PRODUCT_PERMALINK, "license_key": key}
                    )
                    data = response.json()
                    if data.get("success"):
                        uses = data.get("uses", 0)
                        if uses > 3:
                            st.error(f"🚫 Limit Exceeded ({uses}/3)" if lang=="en" else f"🚫 횟수 초과! ({uses}/3)")
                        else:
                            st.session_state["unlocked_love"] = True
                            st.success("Success!")
                            st.rerun()
                    else:
                        st.error("Invalid Key")
                except:
                    st.error("Connection Error")
    st.stop()

# 7. 결과 리포트 (HTML 들여쓰기 제거됨)
if st.session_state["unlocked_love"]:
    st.divider()
    u_info = calculate_day_gan(u_dob)
    p_info = calculate_day_gan(p_dob)
    report = get_love_report(u_info['element'], p_info['element'], u_gender, p_gender, lang)
    
    # 대결 구도
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.markdown(f"""<div class='user-card'><div style='color:#6b7280;'>ME ({u_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{u_name}</div><div style='font-size:1.2em; color:#db2777;'>{u_info[lang]} ({u_info['element']})</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-badge'>❤️</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='user-card'><div style='color:#6b7280;'>PARTNER ({p_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{p_name}</div><div style='font-size:1.2em; color:#db2777;'>{p_info[lang]} ({p_info['element']})</div></div>""", unsafe_allow_html=True)

    # 메인 리포트 (들여쓰기 완전 제거)
    html_content = f"""
<div class='report-container'>
<div class='score-display'>
{t['score_label']}: {report['score']}
</div>
<h2 style='text-align:center; color:#831843; margin-bottom:40px;'>{report['title']}</h2>
<div class='section-box'>
<div class='section-title'>{t['sec_chem']}</div>
<div class='content-text'>{report['chemistry']}</div>
</div>
<div class='section-box'>
<div class='section-title'>{t['sec_conf']}</div>
<div class='content-text'>{report['conflict']}</div>
</div>
<div class='section-box'>
<div class='section-title'>{t['sec_inti']}</div>
<div class='content-text'>{report['intimacy']}</div>
</div>
<div class='section-box' style='background-color: #fdf2f8; border: 1px solid #fbcfe8;'>
<div class='section-title'>{t['sec_adv']}</div>
<div class='content-text' style='font-weight:bold; color:#be185d;'>{report['advice']}</div>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#be185d; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(190, 24, 93, 0.3);">
            {t['btn_print']}
            </button>
        </div>""", height=100
    )
