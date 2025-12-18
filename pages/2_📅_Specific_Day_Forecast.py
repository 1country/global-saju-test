import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Specific Day Forecast", page_icon="📅", layout="wide")

# 🔑 [마스터 키 & 검로드 설정]
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "specific_day"
GUMROAD_LINK = "https://gumroad.com/l/선생님의_상품주소" 

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #1e293b; margin-bottom: 10px; text-align: center;}
        
        /* 리포트 스타일 */
        .report-container {
            background-color: white; padding: 40px; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;
        }
        .report-section {
            margin-bottom: 25px; padding-bottom: 20px; border-bottom: 1px dashed #cbd5e1;
        }
        .report-section:last-child { border-bottom: none; }
        
        .section-emoji { font-size: 1.5em; margin-right: 10px; }
        .section-title { font-size: 1.3em; font-weight: bold; color: #334155; display: inline-block; margin-bottom: 10px; }
        .content-text { font-size: 1.05em; line-height: 1.8; color: #475569; text-align: justify; }
        
        .user-info-box {
            background-color: #f1f5f9; padding: 15px 20px; border-radius: 10px;
            color: #475569; font-size: 0.95em; margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
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
    if st.button("👈 Home" if lang=="en" else "👈 홈으로"):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. 대용량 리포트 데이터
# ----------------------------------------------------------------
def get_long_report(user_elem, day_elem, lang):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    
    rel_type = relations.get(user_elem, {}).get(day_elem, "Same")
    
    scenarios = {
        "Same": {
            "ko": {
                "score": 3,
                "title": "🤝 자아가 강해지고 경쟁과 협력이 공존하는 날",
                "general": "오늘은 당신과 똑같은 기운이 들어오는 날입니다. 거울을 보는 것처럼 나를 닮은 사람들을 만나거나, 내 주관과 고집이 평소보다 훨씬 강해지는 하루가 될 것입니다. 누군가의 도움 없이도 스스로 해내려는 독립심이 불타오르지만, 자칫하면 독불장군이 되어 주변과 마찰을 빚을 수도 있습니다.",
                "money": "재물운은 '공유'의 키워드가 뜹니다. 혼자서 이익을 독차지하려 하면 오히려 손해를 보기 쉽습니다. 동업 제안이 들어오거나, 친구나 동료와 함께 돈을 쓸 일이 생깁니다. 베푸는 것이 액땜이 됩니다.",
                "love": "애정 전선에는 약간의 긴장감이 흐릅니다. 연인이 있다면 사소한 자존심 싸움이 큰 다툼으로 번질 수 있으니, 오늘만큼은 '져주는 것이 이기는 것'이라는 말을 명심하세요.",
                "health": "에너지가 넘치는 날이라 가만히 있으면 오히려 몸살이 납니다. 땀을 흠뻑 흘리는 운동을 하거나, 친구들과 수다를 떨며 스트레스를 풀어야 합니다.",
                "action": "1. 고집을 내려놓고 타인의 의견을 경청하세요.\n2. 밥값이나 커피값은 먼저 계산하세요.\n3. 경쟁보다는 협력을 택할 때 결과가 2배가 됩니다."
            },
            "en": {
                "score": 3,
                "title": "🤝 Day of Strong Self & Co-opetition",
                "general": "Today is filled with energy identical to yours. Your independence and willpower are at their peak. While you feel capable of achieving anything alone, this strong ego can lead to conflicts.",
                "money": "Wealth luck revolves around 'sharing'. Trying to take all profits alone may lead to losses. You might spend money on friends or colleagues. Being generous today acts as a remedy.",
                "love": "Tension exists in relationships. Small ego clashes can escalate, so remember that 'losing is winning' today.",
                "health": "High energy levels. Inactivity might make you feel sick. Engage in vigorous exercise or socialize to release stress.",
                "action": "1. Listen to others.\n2. Be the first to pay for meals.\n3. Cooperation yields double the results."
            }
        },
        "Output": {
            "ko": {
                "score": 4,
                "title": "🎨 창의력이 폭발하고 재능을 뽐내는 날",
                "general": "당신의 내면에 잠재된 끼와 재능이 밖으로 표출되는 날입니다. 머리 회전이 비상하게 빨라지고, 평소에 생각지도 못한 아이디어가 샘솟습니다. 답답했던 일들이 당신의 말 한마디, 손짓 하나로 시원하게 해결될 수 있는 '사이다' 같은 하루입니다.",
                "money": "당신의 능력 자체가 돈이 되는 날입니다. 프리랜서나 영업직, 창작 활동을 하는 분들에게는 최고의 날입니다. 다만, 기분파가 되어 충동구매를 하거나 유흥비로 지출이 커질 수 있습니다.",
                "love": "매력이 철철 넘치는 날입니다. 가만히 있어도 이성들이 당신에게 호감을 보일 것입니다. 썸을 타고 있다면 오늘 고백하거나 진도를 나가기에 아주 좋습니다.",
                "health": "에너지 소모가 극심한 날입니다. 정신없이 활동하다가 저녁이 되면 배터리가 방전된 것처럼 급격한 피로가 몰려올 수 있습니다. 당 충전이 필요합니다.",
                "action": "1. 새로운 프로젝트나 아이디어를 제안해보세요.\n2. 평소보다 조금 더 화려하게 꾸미고 나가세요.\n3. 말조심! 즐거운 분위기에 취해 실언하지 않도록 주의하세요."
            },
            "en": {
                "score": 4,
                "title": "🎨 Day of Explosive Creativity",
                "general": "Your inner talents are expressed outwardly today. Your mind is sharp, and ideas flow endlessly. Problems may be solved effortlessly by your words or actions.",
                "money": "Your skills turn into money today. Excellent for freelancers, sales, or creatives. However, beware of impulse buying.",
                "love": "You are overflowing with charm. Others will naturally be drawn to you. Great day to confess or advance a relationship.",
                "health": "High energy consumption. You might feel sudden exhaustion in the evening. Keep your sugar levels up.",
                "action": "1. Propose new ideas.\n2. Dress up a bit more than usual.\n3. Watch your tongue!"
            }
        },
        "Wealth": {
            "ko": {
                "score": 5,
                "title": "💰 노력의 결실을 맺고 목표를 달성하는 날",
                "general": "눈에 보이는 확실한 결과물이 주어지는 날입니다. 현실적인 감각이 최고조에 달해, 무엇이 이득이고 무엇이 손해인지 본능적으로 계산이 섭니다. 실속을 챙기며 하루를 알차게 채울 수 있는 '수확의 날'입니다.",
                "money": "금전운이 가장 강력한 날입니다. 예기치 않은 보너스가 들어오거나, 투자했던 곳에서 수익이 날 수 있습니다. 사업가라면 오늘은 매출이 오르거나 중요한 계약이 성사될 확률이 매우 높습니다.",
                "love": "남성분들에게는 최고의 연애운이 따릅니다. 여성분들은 현실적이고 능력 있는 남자를 만날 기회가 생깁니다. 맛있는 것을 먹으며 데이트하기에 딱 좋은 날입니다.",
                "health": "몸과 마음이 가볍지만, 너무 결과에 집착하다 보면 신경성 두통이 올 수 있습니다. 일도 좋지만 중간중간 휴식을 취하세요.",
                "action": "1. 중요한 계약이나 결정을 오늘 하세요.\n2. 복권이나 소액 투자를 재미로 해봐도 좋습니다.\n3. 오늘 들어온 돈은 바로 쓰지 말고 일부라도 저축하세요."
            },
            "en": {
                "score": 5,
                "title": "💰 Day of Harvest & Achievement",
                "general": "Tangible results appear today. Your realistic judgment is peaked. It's a day of substance over abstraction.",
                "money": "Strongest financial luck. Unexpected bonuses or investment returns are likely. Business owners may see sales spikes.",
                "love": "Excellent romance luck for men. Women may meet capable partners. Great day for a delicious date.",
                "health": "Light body and mind, but obsession with results may cause headaches. Rest in between work.",
                "action": "1. Make important decisions today.\n2. Buying a lottery ticket is okay.\n3. Save at least a portion of the money."
            }
        },
        "Power": {
            "ko": {
                "score": 2,
                "title": "⚖️ 책임감이 무겁지만 명예가 드높은 날",
                "general": "오늘은 조금 답답하고 어깨가 무거운 하루일 수 있습니다. 규칙, 마감 기한, 상사의 지시 등이 당신을 압박해옵니다. 하지만 이 압박감은 당신을 성장시키는 거름이 되며, 잘 견뎌내면 명예가 따라옵니다.",
                "money": "당장 큰 돈이 들어오는 날은 아닙니다. 오히려 세금이나 공과금 등 나가야 할 돈이 생길 수 있습니다. 직장인은 업무 성과를 인정받아 승진 기회를 잡을 수 있는 길일입니다.",
                "love": "여성분들에게는 카리스마 있는 남자가 들어오는 날입니다. 연인이 있는 경우, 상대방이 나를 통제하려 들 수 있으니 싸우지 말고 오늘은 그냥 들어주세요.",
                "health": "스트레스 지수가 높습니다. 뒷목이 뻐근하거나 소화불량이 올 수 있습니다. 멘탈 관리가 가장 중요합니다.",
                "action": "1. 약속 시간과 규칙을 칼같이 지키세요.\n2. 튀는 행동보다는 조직의 룰을 따르세요.\n3. 오늘 힘든 일은 훗날 반드시 보상받으니 참으세요."
            },
            "en": {
                "score": 2,
                "title": "⚖️ Day of Responsibility & Honor",
                "general": "You might feel restricted and burdened today. Rules and deadlines pressure you. However, enduring it brings recognition and honor.",
                "money": "Not immediate cash windfalls. Beware of expenses like taxes. Good day for employees to get recognized.",
                "love": "Women may meet charismatic partners. Those in relationships might feel controlled. Don't fight; just listen today.",
                "health": "High stress levels. Stiff neck or indigestion is possible. Mental care is crucial.",
                "action": "1. Strictly observe appointments.\n2. Follow the organization's lead.\n3. Endure today's hardships."
            }
        },
        "Resource": {
            "ko": {
                "score": 4,
                "title": "📚 사랑받고 에너지를 충전하는 힐링의 날",
                "general": "가만히 있어도 주변에서 떡을 주는 격입니다. 윗사람의 도움이 따르고 마음이 편안해집니다. 활동적으로 움직이기보다는 차분하게 책을 읽거나 계획을 세우기에 최적의 날입니다.",
                "money": "문서운이 아주 좋습니다. 부동산 계약이나 중요한 결재를 받기에 길한 날입니다. 당장 현금이 도는 것은 아니지만, 미래의 자산 가치를 높이는 일이 일어납니다.",
                "love": "사랑받는 날입니다. 내가 굳이 애쓰지 않아도 상대방이 나를 챙겨주고 배려해줍니다. 소개팅을 한다면 예의 바르고 배울 점이 많은 사람이 나옵니다.",
                "health": "신체 활동보다는 정신 활동이 활발한 날이라, 몸이 조금 처지고 게을러질 수 있습니다. 푹 자고 맛있는 것을 먹으며 쉬는 것이 최고의 보약입니다.",
                "action": "1. 멘토나 윗사람에게 조언을 구해보세요.\n2. 서점에 가서 책을 한 권 사보세요.\n3. 오늘은 나를 위해 게으름을 피워도 용서되는 날입니다."
            },
            "en": {
                "score": 4,
                "title": "📚 Day of Support & Healing",
                "general": "Help comes naturally today. Elders support you. Better for reading and planning than physical activity.",
                "money": "Excellent document luck. Good for contracts. Not immediate cash, but asset value grows.",
                "love": "You are loved. Your partner cares for you without you asking. Blind dates will bring polite partners.",
                "health": "You might feel lazy. Deep sleep and good food are the best medicine today.",
                "action": "1. Ask a mentor for advice.\n2. Buy a book.\n3. Being lazy is forgivable today."
            }
        }
    }
    return scenarios[rel_type][lang]

# ----------------------------------------------------------------
# 4. 메인 화면
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("⚠️ 홈 화면에서 먼저 정보를 입력해주세요.")
    if st.button("홈으로 이동"):
        st.switch_page("Home.py")
    st.stop()

user_name = st.session_state["user_name"]
birth_date = st.session_state["birth_date"]

ui = {
    "ko": {
        "title": "📅 특정일 운세 정밀 분석",
        "sub": "단순한 길흉을 넘어, A4 반 페이지 분량의 심층 리포트를 제공합니다.",
        "user_info": f"👤 **분석 대상:** {user_name}님 (생년월일: {birth_date})",
        "lock_msg": "🔒 프리미엄 리포트 잠금 ($10)",
        "label": "구매 후 받은 라이센스 키 입력",
        "btn_unlock": "리포트 잠금 해제",
        "btn_buy": "💳 프리미엄 리포트 구매 ($10)",
        "target_date": "분석하고 싶은 날짜 (D-Day)",
        "btn_analyze": "상세 운세 확인하기",
        "print": "🖨️ 리포트 인쇄하기"
    },
    "en": {
        "title": "📅 Specific Day: Deep Report",
        "sub": "In-depth analysis report (Half A4 size) beyond simple luck.",
        "user_info": f"👤 **User:** {user_name} (DOB: {birth_date})",
        "lock_msg": "🔒 Premium Report Locked ($10)",
        "label": "Enter License Key",
        "btn_unlock": "Unlock Report",
        "btn_buy": "💳 Buy Premium Report ($10)",
        "target_date": "Target Date (D-Day)",
        "btn_analyze": "Analyze Detail",
        "print": "🖨️ Print Report"
    }
}
t = ui[lang]

# 👇 [수정됨] 섹션 제목도 언어에 따라 바뀌도록 분리했습니다.
section_titles = {
    "ko": {
        "gen": "General Flow (총평)",
        "mon": "Wealth & Career (재물/사업)",
        "lov": "Love & Relationships (인간관계)",
        "hea": "Health & Condition (건강)",
        "act": "Action Plan (행동 지침)"
    },
    "en": {
        "gen": "General Flow",
        "mon": "Wealth & Career",
        "lov": "Love & Relationships",
        "hea": "Health & Condition",
        "act": "Action Plan"
    }
}
st_t = section_titles[lang] # 현재 언어에 맞는 제목 가져오기

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)

# 🔒 [잠금 로직]
if "unlocked_specific" not in st.session_state: st.session_state["unlocked_specific"] = False

if not st.session_state["unlocked_specific"]:
    with st.container(border=True):
        st.info(t['sub'])
        st.markdown(f"<div class='user-info-box'>{t['user_info']}</div>", unsafe_allow_html=True)
        st.write(f"### {t['lock_msg']}")
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock']):
            if key == UNLOCK_CODE:
                st.session_state["unlocked_specific"] = True
                st.success("Master Key Accepted!")
                st.rerun()
            try:
                response = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={"product_permalink": PRODUCT_PERMALINK, "license_key": key}
                )
                data = response.json()
                if data.get("success"):
                    if data.get("uses", 0) > 3:
                        st.error("🚫 Limit exceeded (Max 3 uses).")
                    else:
                        st.session_state["unlocked_specific"] = True
                        st.success("Success!")
                        st.rerun()
                else:
                    st.error("🚫 Invalid Key.")
            except:
                st.error("Connection Error.")
    st.stop()

# 🔓 [잠금 해제 후]
with st.container():
    st.markdown(f"<div class='user-info-box'>{t['user_info']}</div>", unsafe_allow_html=True)
    col_center, _ = st.columns([1, 2])
    with col_center:
        target_date = st.date_input(t['target_date'], value=date.today(), min_value=date.today())

    if st.button(t['btn_analyze'], type="primary"):
        user_info = calculate_day_gan(birth_date)
        target_info = calculate_day_gan(target_date)
        report = get_long_report(user_info['element'], target_info['element'], lang)
        
        st.divider()
        st.markdown(f"<h2 style='text-align:center; color:#334155;'>📅 {target_date.strftime('%Y-%m-%d')} Analysis Report</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 0.5, 1])
        with c1: 
            st.markdown(f"<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:15px; border:1px solid #e2e8f0;'><b>ME</b><br><span style='font-size:1.8em;'>{user_info[lang]}</span><br>({user_info['element']})</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div style='text-align:center; font-size:2em; padding-top:25px; color:#cbd5e1;'>VS</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:15px; border:1px solid #e2e8f0;'><b>DAY</b><br><span style='font-size:1.8em;'>{target_info[lang]}</span><br>({target_info['element']})</div>", unsafe_allow_html=True)

        st.write("") 
        
        score = report['score']
        stars = "⭐" * score + "🌑" * (5 - score)
        
        # 👇 [수정됨] 이제 제목(General Flow 등)도 언어 변수(st_t)를 사용합니다.
        html_content = f"""
<div class='report-container'>
<div style='text-align:center; margin-bottom:30px;'>
<div style='font-size:2em; color:#f59e0b; letter-spacing: 5px;'>{stars}</div>
<h1 style='color:#1e293b; margin-top: 10px; font-size: 1.8em;'>{report['title']}</h1>
</div>
<div class='report-section'>
<div class='section-title'><span class='section-emoji'>🔮</span>{st_t['gen']}</div>
<div class='content-text'>{report['general']}</div>
</div>
<div class='report-section'>
<div class='section-title'><span class='section-emoji'>💰</span>{st_t['mon']}</div>
<div class='content-text'>{report['money']}</div>
</div>
<div class='report-section'>
<div class='section-title'><span class='section-emoji'>❤️</span>{st_t['lov']}</div>
<div class='content-text'>{report['love']}</div>
</div>
<div class='report-section'>
<div class='section-title'><span class='section-emoji'>💪</span>{st_t['hea']}</div>
<div class='content-text'>{report['health']}</div>
</div>
<div class='report-section' style='background-color:#f0f9ff; padding:20px; border-radius:10px; border:none;'>
<div class='section-title' style='color:#0369a1;'><span class='section-emoji'>🚀</span>{st_t['act']}</div>
<div class='content-text' style='white-space: pre-line; font-weight:bold; color:#0c4a6e;'>{report['action']}</div>
</div>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)

        st.write("")
        components.html(
            f"""<script>function printParent() {{ window.parent.print(); }}</script>
            <div style="text-align:center;">
                <button onclick="printParent()" style="background-color:#475569; color:white; border:none; padding:15px 30px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                {t['print']}
                </button>
            </div>""", height=100
        )
