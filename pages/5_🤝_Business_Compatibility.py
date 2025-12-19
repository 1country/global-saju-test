.import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Business Compatibility", page_icon="💼", layout="wide")

# 🔑 [마스터 키 & 검로드 설정] - 선생님이 설정한 URL로 수정됨!
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "business_compatibility" 
GUMROAD_LINK = "https://5codes.gumroad.com/l/business_compatibility" 

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #1e3a8a; margin-bottom: 10px; text-align: center;}
        
        /* 리포트 컨테이너 스타일 */
        .report-container {
            background-color: white; padding: 50px; border-radius: 20px;
            box-shadow: 0 10px 40px rgba(30, 58, 138, 0.15); border: 1px solid #dbeafe;
        }
        .section-box {
            margin-bottom: 35px; padding-bottom: 25px; border-bottom: 1px dashed #93c5fd;
        }
        .section-box:last-child { border-bottom: none; }
        
        .section-title {
            font-size: 1.5em; font-weight: bold; color: #1e40af; margin-bottom: 20px; 
            display: flex; align-items: center; border-left: 5px solid #2563eb; padding-left: 15px;
        }
        .content-text { font-size: 1.1em; line-height: 1.9; color: #334155; text-align: justify; letter-spacing: -0.02em; }
        .score-display { text-align: center; font-size: 3.5em; font-weight: bold; color: #1e3a8a; margin: 30px 0; }
        
        .user-card {
            background: #eff6ff; padding: 20px; border-radius: 15px; border: 1px solid #bfdbfe;
            text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .vs-badge {
            display: flex; justify-content: center; align-items: center; 
            font-size: 2em; font-weight: bold; color: #2563eb; height: 100%;
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
# 3. [초대형] 비즈니스 궁합 데이터
# ----------------------------------------------------------------
def get_biz_report(u_elem, p_elem, lang):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    rel = relations[u_elem][p_elem]
    
    # 🌟 비즈니스 시나리오 (A4 1장 분량)
    reports = {
        "Same": { # 비견 (동업, 경쟁)
            "score": 80,
            "ko": {
                "title": "🤝 어깨를 나란히 하는 '공동 대표' 스타일",
                "synergy": "두 사람은 비즈니스 파트너로서 아주 대등한 관계입니다. 서로의 능력, 야망, 추진력이 비슷하여 '의기투합'하기에 최적입니다. 창업 초기에는 누구보다 든든한 동지가 되어주며, 시너지 효과가 폭발합니다. 마치 형제처럼 서로를 밀어주고 끌어주는 강력한 '원팀(One Team)'이 될 수 있습니다.",
                "finance": "수익 배분(Share)이 가장 중요한 이슈입니다. 둘 다 욕심이 있고 계산이 빠르기 때문에, 이익 배분이 불투명하면 바로 갈등으로 이어집니다. '좋은 게 좋은 거지'라는 식의 주먹구구식 운영은 절대 금물입니다. 계약서에 지분율과 역할 분담을 명확히 명시해야 합니다.",
                "conflict": "의견 충돌이 발생하면 누구도 굽히지 않아 '치킨 게임'으로 갈 수 있습니다. 자존심 싸움이 비즈니스를 망칠 수 있으니 주의해야 합니다. 특히 회사가 커질수록 주도권 싸움이 치열해질 수 있습니다.",
                "role": "두 분 모두 '공동 대표' 직함이 어울립니다. 혹은 한 명이 대외 영업(CEO)을 맡고, 다른 한 명이 내부 관리(COO)를 맡는 식으로 영역을 완전히 분리하는 것이 좋습니다.",
                "advice": "1. **계약서 필수:** 수익 배분, 지분율, 출구 전략(Exit Plan)까지 문서화하세요.\n2. **영역 분리:** 서로 간섭하지 않는 고유 업무 영역을 정하세요.\n3. **경쟁심 활용:** 서로를 자극제로 삼아 선의의 경쟁을 하세요."
            },
            "en": {
                "title": "🤝 Equal Partners: Co-Founders with Strong Synergy",
                "synergy": "You are equals in business. Your ambition and drive align perfectly, creating explosive synergy in the early stages. You act like brothers in arms, pushing each other forward as a powerful 'One Team'.",
                "finance": "Profit sharing is the critical issue. Ambiguity in finances will lead to immediate conflict. Avoid handshake deals; clearly document equity and profit distribution in a contract.",
                "conflict": "Ego clashes are the biggest risk. Neither of you likes to back down, which can lead to a stalemate. Power struggles may arise as the company grows.",
                "role": "Both suit the 'Co-CEO' title. Alternatively, split roles completely: one handles external sales (CEO), the other internal operations (COO).",
                "advice": "1. **Contracts are Vital:** Document everything, including exit strategies.\n2. **Separate Domains:** Define distinct areas of responsibility.\n3. **Healthy Competition:** Use your rivalry to fuel growth."
            }
        },
        "Output": { # 내가 생함 (내가 아이디어 제공, 상대가 실행)
            "score": 90,
            "ko": {
                "title": "💡 내가 기획하고 파트너가 실현하는 '창조적' 관계",
                "synergy": "당신(본인)이 아이디어와 비전을 제시하면, 파트너가 그것을 현실로 만들어주는 관계입니다. 당신은 파트너의 재능을 키워주고, 파트너는 당신의 비전을 따릅니다. R&D, 디자인, 마케팅 등 창의성이 필요한 분야에서 최고의 궁합을 자랑합니다. 당신은 '투자자'나 '기획자'의 포지션, 파트너는 '기술자'나 '실무자' 포지션이 적합합니다.",
                "finance": "당신이 자금을 대고 파트너가 기술을 대는 형태가 많습니다. 당장의 수익보다는 미래 가치를 보고 투자하는 형국입니다. 파트너의 능력이 발휘될 때까지 당신이 기다려줘야 하는 시간이 필요합니다.",
                "conflict": "당신은 파트너가 답답해 보일 수 있고, 파트너는 당신의 요구사항이 너무 많다고 느낄 수 있습니다. '잔소리'가 심해지면 파트너가 의욕을 잃고 떠날 수 있으니 주의해야 합니다.",
                "role": "**당신: 회장/기획이사 (Visionary)**, **파트너: 사장/개발팀장 (Executor)**. 당신이 판을 깔아주면 파트너가 춤을 추는 구조입니다.",
                "advice": "1. **믿고 맡기기:** 실무에 너무 깊게 관여하지 마세요.\n2. **보상 체계:** 파트너에게 충분한 인센티브를 제공하여 동기 부여를 하세요.\n3. **인내심:** 성과가 나올 때까지 시간이 걸릴 수 있음을 인지하세요."
            },
            "en": {
                "title": "💡 Creative Duo: You Envision, They Execute",
                "synergy": "You provide the vision and ideas; your partner turns them into reality. Excellent for R&D, design, or marketing. You are the 'Investor' or 'Planner', while they are the 'Technician' or 'Doer'.",
                "finance": "Often, you provide capital, and they provide skills. You invest in future value rather than immediate profit. Patience is required until their skills bear fruit.",
                "conflict": "You might find them slow; they might find you demanding. excessive micromanagement can demotivate your partner.",
                "role": "**You: Chairman/Visionary**, **Partner: CEO/Executor**. You set the stage, and they perform.",
                "advice": "1. **Trust Them:** Don't micromanage execution.\n2. **Incentives:** Motivate them with proper rewards.\n3. **Patience:** Understand that results may take time."
            }
        },
        "Wealth": { # 내가 극함 (내가 관리, 상대가 자산)
            "score": 85,
            "ko": {
                "title": "💰 내가 리드하고 관리하는 '오너와 경영인' 관계",
                "synergy": "당신(본인)이 주도권을 쥐고 파트너를 관리하는 관계입니다. 파트너는 당신에게 실질적인 이익(돈)을 가져다주는 존재입니다. 당신의 경영 능력과 파트너의 실무 능력이 결합하여 높은 수익을 창출할 수 있습니다. 비즈니스의 목적이 '이윤 추구'라면 가장 이상적인 배치입니다.",
                "finance": "재물운이 가장 좋습니다. 파트너가 열심히 일해서 벌어온 돈을 당신이 관리하고 불리는 형국입니다. 자금의 흐름을 당신이 꽉 쥐고 있어야 회사가 안정적으로 돌아갑니다.",
                "conflict": "당신이 파트너를 너무 부리려 하거나, 성과를 독차지하려 할 때 문제가 생깁니다. 파트너가 '나는 일만 하는 기계인가?'라는 불만을 가질 수 있습니다. 인간적인 존중이 결여되면 파트너는 경쟁사로 이직하거나 당신의 노하우를 가지고 독립할 수 있습니다.",
                "role": "**당신: CEO/오너 (Owner)**, **파트너: 영업이사/CFO (Manager)**. 당신이 지시하고 파트너가 따르는 수직적인 구조가 효율적입니다.",
                "advice": "1. **확실한 보상:** 파트너가 벌어온 만큼 확실하게 금전적으로 보상하세요.\n2. **인격적 대우:** 상하 관계가 아니라 비즈니스 파트너로서 존중하세요.\n3. **권한 위임:** 믿을 수 있는 범위 내에서는 전결권을 주세요."
            },
            "en": {
                "title": "💰 The Boss & The Asset: Profit-Driven Partnership",
                "synergy": "You hold the reins and manage the partner. The partner brings you tangible profit. Ideally suited for profit-maximization businesses. Your management skills meet their operational skills.",
                "finance": "Best financial luck. You manage and multiply the money they earn. Keep a tight grip on cash flow for stability.",
                "conflict": "Issues arise if you treat them like a machine or hog the credit. Without respect, they might leave with your trade secrets.",
                "role": "**You: CEO/Owner**, **Partner: Sales Director/Manager**. A vertical structure where you lead and they follow is efficient.",
                "advice": "1. **Fair Compensation:** Pay them well for their results.\n2. **Respect:** Treat them as a partner, not a subordinate.\n3. **Delegation:** Grant authority within trusted limits."
            }
        },
        "Power": { # 나를 극함 (상대가 나를 통제)
            "score": 75,
            "ko": {
                "title": "⚖️ 파트너의 원칙과 시스템을 따르는 '안정적' 관계",
                "synergy": "파트너가 주도권을 쥐고 당신을 이끌어가는 관계입니다. 혹은 파트너가 당신에게 엄격한 규칙이나 시스템을 요구합니다. 처음에는 답답할 수 있지만, 파트너의 꼼꼼함과 원칙주의가 사업의 리스크를 줄여줍니다. 프랜차이즈 가맹점주(본인)와 본사(파트너)의 관계와 비슷합니다.",
                "finance": "대박보다는 '안정'을 추구합니다. 파트너가 재무 관리를 하거나 결재권을 가질 때 회사가 탄탄해집니다. 당신이 무리한 투자를 하려 할 때 파트너가 브레이크를 걸어주어 손실을 막아줍니다.",
                "conflict": "파트너의 간섭이나 지시가 심해지면 당신이 스트레스를 받습니다. '내 사업인데 내 마음대로 못 하나?'라는 반발심이 생길 수 있습니다. 당신의 자율성이 침해받을 때 갈등이 폭발합니다.",
                "role": "**당신: 홍보/영업 (Face)**, **파트너: CEO/감사 (Controller)**. 당신은 밖에서 뛰고, 파트너는 안에서 살림을 챙기고 규율을 잡아야 합니다.",
                "advice": "1. **시스템 존중:** 파트너가 만든 규칙을 따르는 것이 이득입니다.\n2. **리스크 관리:** 파트너의 조언은 쓴약이니 귀담아들으세요.\n3. **역할 인정:** 내가 2인자가 되는 것을 두려워하지 마세요."
            },
            "en": {
                "title": "⚖️ Structured Growth: Partner Leads with Discipline",
                "synergy": "Your partner leads or sets strict rules. It might feel restrictive, but their meticulousness reduces business risks. Think of it as a Franchisee (You) vs. HQ (Partner) relationship.",
                "finance": "Pursues stability over jackpot hits. Financial health improves when the partner manages the funds. They act as a brake on your risky investments.",
                "conflict": "Excessive interference causes stress. You might feel your autonomy is violated. Conflict erupts if you feel stifled.",
                "role": "**You: PR/Sales (Face)**, **Partner: CEO/Auditor (Controller)**. You work the field; they manage the house and rules.",
                "advice": "1. **Respect the System:** Following their rules pays off.\n2. **Risk Mgmt:** Listen to their 'bitter pill' advice.\n3. **Acceptance:** Don't be afraid to be the number two."
            }
        },
        "Resource": { # 나를 생함 (상대가 나를 도움)
            "score": 95,
            "ko": {
                "title": "🍼 든든한 후원자이자 멘토를 만난 '귀인' 관계",
                "synergy": "파트너가 당신을 전적으로 믿고 지지해주는 관계입니다. 파트너는 당신의 부족한 점을 채워주고, 노하우를 전수해주며, 심리적인 안정감을 줍니다. 당신은 비즈니스에만 집중할 수 있는 최고의 환경을 얻게 됩니다. 투자자(파트너)와 스타트업 대표(본인)로서 아주 훌륭한 궁합입니다.",
                "finance": "문서운과 계약운이 좋습니다. 파트너의 도움으로 좋은 계약을 따내거나, 부동산/지식재산권 등 자산을 늘릴 수 있습니다. 당장의 현금 흐름보다 회사의 '브랜드 가치'가 올라갑니다.",
                "conflict": "당신이 파트너에게 너무 의존하여 나태해질 수 있습니다. 또한, 파트너가 과보호하거나 보수적인 조언만 하여 회사의 성장 속도가 느려질 수 있습니다. '온실 속의 화초'가 되지 않도록 경계해야 합니다.",
                "role": "**당신: CEO (Operator)**, **파트너: 회장/고문 (Mentor)**. 파트너는 뒤에서 묵묵히 지원하고, 당신이 전면에 나서서 스포트라이트를 받습니다.",
                "advice": "1. **감사 표현:** 후원자의 도움을 당연하게 여기지 마세요.\n2. **독립성 유지:** 최종 결정은 당신이 내려야 회사가 젊어집니다.\n3. **비전 공유:** 파트너에게 회사의 성장 비전을 자주 브리핑하세요."
            },
            "en": {
                "title": "🍼 The Mentor & Protege: Supported Success",
                "synergy": "Your partner fully trusts and supports you. They fill your gaps and provide stability. Ideally suited for an Investor (Partner) and Startup CEO (You) relationship.",
                "finance": "Excellent luck with contracts and assets. Brand value grows. You gain assets (IP, Real Estate) with their help.",
                "conflict": "You might become too dependent or lazy. Their conservative advice could slow down growth. Avoid becoming a 'flower in a greenhouse'.",
                "role": "**You: CEO (Operator)**, **Partner: Chairman/Mentor (Advisor)**. They support from the shadows; you take the spotlight.",
                "advice": "1. **Gratitude:** Never take their support for granted.\n2. **Independence:** Make final decisions yourself to keep the company agile.\n3. **Share Vision:** Regularly brief them on the company's growth."
            }
        }
    }
    
    base_data = reports[rel]
    data = base_data[lang]
    
    return {
        "score": base_data["score"],
        "title": data['title'],
        "synergy": data['synergy'],
        "finance": data['finance'],
        "conflict": data['conflict'],
        "role": data['role'],
        "advice": data['advice']
    }

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
        "title": "💼 비즈니스 파트너 궁합",
        "sub": "동업을 해도 될까? 역할 분담은? 성공을 위한 전략적 파트너십 분석",
        "p_info_title": "파트너 정보 입력",
        "p_name": "파트너 이름",
        "p_dob": "파트너 생년월일",
        "p_gender": "파트너 성별",
        "lock_title": "🔒 비즈니스 리포트 잠금 ($10)",
        "lock_desc": "결제 후 발급받은 라이센스 키를 입력하세요.",
        "lock_warn": "⚠️ 주의: 이 키는 3회까지만 조회 가능합니다.",
        "btn_buy": "💳 이용권 구매하기 ($10)",
        "btn_unlock": "결과 확인하기",
        "btn_print": "🖨️ 리포트 인쇄하기",
        "sec_syn": "🚀 파트너십 시너지 (Synergy)",
        "sec_fin": "💰 재무 & 이익 (Finance)",
        "sec_con": "⚔️ 잠재적 갈등 (Risk)",
        "sec_rol": "👔 최적 역할 분담 (Roles)",
        "sec_adv": "💡 성공을 위한 조언 (Advice)",
        "score_label": "사업 궁합 점수"
    },
    "en": {
        "title": "💼 Business Compatibility",
        "sub": "Strategic partnership analysis: Co-founding, Roles, and Success.",
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
        "sec_syn": "🚀 Partnership Synergy",
        "sec_fin": "💰 Finance & Profit",
        "sec_con": "⚔️ Potential Conflict",
        "sec_rol": "👔 Optimal Roles",
        "sec_adv": "💡 Strategy for Success",
        "score_label": "Compatibility Score"
    }
}
t = ui[lang]

# 🌟 팝업창(Dialog) 함수
@st.dialog("⚠️ Usage Limit Warning")
def show_limit_warning():
    st.warning(t['lock_warn'], icon="⚠️")
    st.write("Checking this result will deduct 1 credit from your license.")
    if st.button("I Understand & Proceed", type="primary"):
        st.rerun()

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.info(f"{t['sub']} (User: {u_name})")

# 5. 파트너 정보 입력
with st.container(border=True):
    st.subheader(t['p_info_title'])
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input(t['p_name'])
        p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1985,1,1))
    with c2:
        p_gender = st.selectbox(t['p_gender'], ["Male", "Female"])

# 6. 잠금 및 결제 로직
if "unlocked_biz" not in st.session_state: st.session_state["unlocked_biz"] = False

if not st.session_state["unlocked_biz"]:
    st.divider()
    with st.container(border=True):
        st.markdown(f"### {t['lock_title']}")
        st.write(t['lock_desc'])
        
        if st.button("⚠️ Check Limit Info", type="secondary"):
            show_limit_warning()
            
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        
        key = st.text_input("License Key", type="password")
        if st.button(t['btn_unlock'], type="primary"):
            if not p_name:
                st.error("Please enter partner's name.")
            else:
                if key == UNLOCK_CODE:
                    st.session_state["unlocked_biz"] = True
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
                            st.error(f"🚫 Limit Exceeded ({uses}/3)")
                        else:
                            st.session_state["unlocked_biz"] = True
                            st.success("Success!")
                            st.rerun()
                    else:
                        st.error("Invalid Key")
                except:
                    st.error("Connection Error")
    st.stop()

# 7. 결과 리포트
if st.session_state["unlocked_biz"]:
    st.divider()
    u_info = calculate_day_gan(u_dob)
    p_info = calculate_day_gan(p_dob)
    report = get_biz_report(u_info['element'], p_info['element'], lang)
    
    # 대결 구도
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.markdown(f"""<div class='user-card'><div style='color:#64748b;'>ME ({u_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1e293b;'>{u_name}</div><div style='font-size:1.2em; color:#2563eb;'>{u_info[lang]} ({u_info['element']})</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-badge'>🤝</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='user-card'><div style='color:#64748b;'>PARTNER ({p_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1e293b;'>{p_name}</div><div style='font-size:1.2em; color:#2563eb;'>{p_info[lang]} ({p_info['element']})</div></div>""", unsafe_allow_html=True)

    # 메인 리포트 (화면 깨짐 방지: 한 줄 처리)
    html_content = f"""<div class='report-container'><div class='score-display'>{t['score_label']}: {report['score']}</div><h2 style='text-align:center; color:#1e40af; margin-bottom:40px;'>{report['title']}</h2><div class='section-box'><div class='section-title'>{t['sec_syn']}</div><div class='content-text'>{report['synergy']}</div></div><div class='section-box'><div class='section-title'>{t['sec_fin']}</div><div class='content-text'>{report['finance']}</div></div><div class='section-box'><div class='section-title'>{t['sec_con']}</div><div class='content-text'>{report['conflict']}</div></div><div class='section-box' style='background-color:#eff6ff; border:1px solid #bfdbfe;'><div class='section-title'>{t['sec_rol']}</div><div class='content-text' style='font-weight:bold; color:#1e3a8a;'>{report['role']}</div></div><div class='section-box' style='border:none;'><div class='section-title'>{t['sec_adv']}</div><div class='content-text' style='white-space: pre-line; font-weight:bold; color:#1d4ed8;'>{report['advice']}</div></div></div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#1e3a8a; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3);">
            {t['btn_print']}
            </button>
        </div>""", height=100
    )
