import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 및 스타일 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="2026 Forecast", page_icon="🔮", layout="wide")

# 🔑 [마스터 키 & 검로드 설정]
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "2026_forecast"
GUMROAD_LINK = "https://5codes.gumroad.com/l/2026_forecast" 

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.0em; font-weight: bold; color: #1e293b; margin-bottom: 20px;}
        .sub-header {font-size: 1.2em; color: #64748b; margin-bottom: 30px;}
        .card {
            background-color: white; padding: 20px; border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 2. 사이드바 설정 (언어 + 커피 후원)
# ----------------------------------------------------------------
with st.sidebar:
    st.title("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    
    st.markdown("---")
    if st.button("👈 Home" if lang=="en" else "👈 홈으로"):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. 데이터 및 함수 정의 (2026 총평 & 월별 운세)
# ----------------------------------------------------------------
def get_interpretation(element, lang):
    # (참고) 성격 특성 데이터
    traits_ko = {
        "Wood": "당신은 '나무(Wood)'입니다. 성장을 지향하며 창의적이고 인자한 성품을 가졌습니다.",
        "Fire": "당신은 '불(Fire)'입니다. 열정적이고 예의가 바르며 표현력이 뛰어납니다.",
        "Earth": "당신은 '흙(Earth)'입니다. 신용을 중시하며 포용력이 있고 묵직합니다.",
        "Metal": "당신은 '쇠(Metal)'입니다. 결단력이 있고 의리가 있으며 냉철합니다.",
        "Water": "당신은 '물(Water)'입니다. 지혜롭고 유연하며 적응력이 뛰어납니다."
    }
    traits_en = {
        "Wood": "You are 'Wood'. You are growth-oriented, creative, and benevolent.",
        "Fire": "You are 'Fire'. You are passionate, polite, and expressive.",
        "Earth": "You are 'Earth'. You value trust, are inclusive, and reliable.",
        "Metal": "You are 'Metal'. You are decisive, loyal, and sharp.",
        "Water": "You are 'Water'. You are wise, flexible, and adaptable."
    }

    # 2026년 총평 (Expert Version)
    forecast_ko = {}
    forecast_en = {}

    if element == "Wood":
        forecast_ko = {
            "title": "🔥 재능이 불타오르는 '표현'의 해 (식상운)",
            "gen": "2026년은 당신의 잠재력이 화산처럼 폭발하는 시기입니다. 가만히 있어도 아이디어가 샘솟고, 나를 표현하고 싶은 욕구가 강해집니다. 당신의 말과 행동이 돈이 되는 해이니, 겸손하게 숨기보다는 과감하게 드러내세요. 다만, 너무 바쁘게 움직이다가 건강을 놓칠 수 있으니 '휴식'도 스케줄에 넣어야 합니다.",
            "money": "활동하는 만큼 정직하게 통장이 불어납니다. 다만, 보여주기 위한 품위 유지비나 충동구매 지출도 함께 늘어나니 카드값 관리가 필수입니다.",
            "love": "매력이 넘쳐흘러 가만히 있어도 이성이 꼬입니다. 썸을 타기엔 최고지만, 기혼자는 구설수를 조심하세요."
        }
        forecast_en = {
            "title": "🔥 Year of Expression & Talent (Output)",
            "gen": "2026 is a year where your hidden potential explodes like a volcano. Your creativity is at its peak. Do not hide your talents; express them boldly, as your words and actions will turn into profit. However, beware of burnout.",
            "money": "Income grows as much as you move. Be careful of impulse buying for luxury items.",
            "love": "Your charm is irresistible. Great for singles, but married couples should avoid misunderstandings."
        }
    elif element == "Fire":
        forecast_ko = {
            "title": "🤝 경쟁과 도약의 '자립'의 해 (비겁운)",
            "gen": "자신감이 하늘을 찌르는 해입니다. '나도 할 수 있다'는 독립심이 강해져 창업이나 프리랜서 선언을 하기 좋습니다. 필연적으로 강력한 경쟁자가 나타나지만, 그 경쟁자가 오히려 나를 성장시키는 자극제가 됩니다. 혼자 다 하려 하지 말고, 적까지도 내 편으로 만드는 리더십이 승패를 가릅니다.",
            "money": "들어오는 돈은 많지만 나가는 돈도 만만치 않습니다. 특히 친구나 동료와의 금전 거래나 공동 투자는 99% 손해를 보니 절대 금물입니다.",
            "love": "친구처럼 편안한 사람과 연인으로 발전할 수 있습니다. 이미 연인이 있다면 고집 때문에 다툴 수 있으니 한 발 물러서세요."
        }
        forecast_en = {
            "title": "🤝 Year of Self-Reliance & Competition",
            "gen": "Your confidence skyrockets. It's a great year to start a business or go independent. Strong rivals will appear, but they will motivate you to grow. The key to success is turning enemies into allies.",
            "money": "High income, high expenses. Never lend money to friends or make joint investments this year.",
            "love": "Friends may turn into lovers. If taken, suppress your ego to avoid conflicts."
        }
    elif element == "Earth":
        forecast_ko = {
            "title": "📜 결실을 맺고 인정받는 '문서'의 해 (인성운)",
            "gen": "지난 몇 년간 고생한 노력의 보상을 받는 해입니다. 윗사람(상사, 부모님, 귀인)의 도움을 받아 승진하거나 좋은 계약을 맺게 됩니다. 몸을 쓰는 일보다는 자격증 공부, 학위 취득, 부동산 계약 등 '머리와 문서'를 쓰는 일에서 대박이 터집니다. 차분하게 내실을 다지기 가장 좋은 시기입니다.",
            "money": "현금보다는 문서가 좋습니다. 집을 사거나, 주식/청약에 당첨되는 등 자산 가치가 오르는 행운이 따릅니다.",
            "love": "사랑받고 보호받는 운세입니다. 나를 아껴주는 듬직하고 배울 점이 많은 인연을 만나게 됩니다."
        }
        forecast_en = {
            "title": "📜 Year of Recognition & Resources",
            "gen": "You will be rewarded for your past efforts. Help from superiors or mentors will lead to promotion or good contracts. Focus on intellectual pursuits like certifications, degrees, or real estate deals.",
            "money": "Great luck with assets like real estate or stocks. Focus on long-term value.",
            "love": "You will be loved and cared for. You might meet a mature and reliable partner."
        }
    elif element == "Metal":
        forecast_ko = {
            "title": "🔨 명예와 권력을 쥐는 '승진'의 해 (관성운)",
            "gen": "어깨가 무거워지지만 그만큼 자리가 높아지는 해입니다. 직장에서 승진하거나 중요한 프로젝트의 책임을 맡게 됩니다. 스트레스와 압박감이 있겠지만, 이를 견뎌내면 사회적 지위와 명예가 확실하게 올라갑니다. '왕관을 쓰려는 자, 그 무게를 견뎌라'라는 말이 딱 맞는 한 해입니다.",
            "money": "월급이 오르거나 보너스를 받는 등 고정 수입이 늘어납니다. 안정적인 저축을 통해 목돈을 만들기 좋습니다.",
            "love": "여자는 능력 있고 카리스마 있는 남자를 만날 운이며, 남자는 자녀 운이 있거나 가정에 책임감이 커집니다."
        }
        forecast_en = {
            "title": "🔨 Year of Honor & Authority",
            "gen": "Heavier responsibilities bring higher status. Expect promotions or leading major projects. It will be stressful, but overcoming it will grant you honor and power. 'Heavy is the head that wears the crown.'",
            "money": "Stable income increases through salary raises. Good for saving.",
            "love": "Women may meet capable partners. Men will feel more responsibility towards family."
        }
    elif element == "Water":
        forecast_ko = {
            "title": "💰 결과물을 사냥하는 '재물'의 해 (재성운)",
            "gen": "눈앞에 사냥감(돈/목표)이 보이는 해입니다. 가만히 있으면 아무것도 얻지 못하니, 사냥꾼처럼 치열하게 움직여서 쟁취해야 합니다. 사업을 확장하거나 투자를 하기에 아주 좋은 타이밍입니다. 과정은 힘들 수 있어도 결과물(통장 잔고)을 보며 웃게 될 것입니다. 현실적인 감각이 최고조에 달합니다.",
            "money": "재물운이 가장 강력합니다. 다만 하이 리스크 하이 리턴이니, 확실한 곳에 과감하게 투자하세요.",
            "love": "남자는 매력적인 이성을 만나 연애할 확률이 매우 높습니다. 여자는 현실적인 능력이 좋은 남자를 선호하게 됩니다."
        }
        forecast_en = {
            "title": "💰 Year of Wealth & Achievement",
            "gen": "The prey (money/goals) is in sight. You must act like a hunter to seize it. It is the perfect time for business expansion or investment. The process may be tough, but the financial results will be rewarding.",
            "money": "Strongest wealth luck. High risk, high return. Invest boldly where you are certain.",
            "love": "Men are very likely to meet attractive partners. Women will prefer capable, realistic partners."
        }
        
    if lang == "ko": return traits_ko[element], forecast_ko
    else: return traits_en[element], forecast_en

def get_monthly_forecast_unique(element, lang):
    # (월, 한국어 조언, 영어 조언, ★별점)
    data = {
        "Wood": [
            ("1월", "지인이나 친구가 금전 부탁을 해옵니다. 냉정하게 거절하지 않으면 돈도 잃고 사람도 잃습니다.", "People may ask for money. Refuse firmly to save both money and friends.", "⭐⭐"),
            ("2월", "강력한 경쟁자가 나타나 내 밥그릇을 노립니다. 감정적으로 대응하지 말고 실속만 챙기세요.", "A strong rival appears. Focus on benefits, not emotions.", "⭐⭐⭐"),
            ("3월", "사람들이 모이는 곳에서 말실수를 할 수 있습니다. '낮말은 새가 듣고 밤말은 쥐가 듣는다'를 명심하세요.", "Watch your words in social gatherings. A slip of the tongue causes trouble.", "⭐⭐"),
            ("4월", "뜻밖의 횡재수가 있습니다. 생각지도 못한 보너스나 공돈이 들어오니 기분 좋은 달입니다.", "Unexpected windfall! You might receive a bonus or unexpected money.", "⭐⭐⭐⭐⭐"),
            ("5월", "머리 회전이 빨라지고 아이디어가 폭발합니다. 기획이나 창작 활동에서 최고의 성과를 냅니다.", "Ideas flow endlessly. Best month for planning or creative work.", "⭐⭐⭐⭐⭐"),
            ("6월", "몸이 열 개라도 모자랄 만큼 바쁩니다. 과로로 쓰러질 수 있으니 영양제를 챙겨 드세요.", "Extremely busy. Take care of your health to avoid burnout.", "⭐⭐"),
            ("7월", "재물 흐름이 아주 안정적입니다. 헛돈 쓰지 말고 차곡차곡 저축하기 가장 좋은 시기입니다.", "Financial flow is stable. Best time to save money.", "⭐⭐⭐⭐"),
            ("8월", "직장에서 스트레스가 극에 달합니다. 욱하고 사표 던지지 마세요. 참는 자에게 복이 옵니다.", "Work stress peaks. Don't quit impulsively. Patience brings rewards.", "⭐⭐"),
            ("9월", "어깨가 무거워지지만 그만큼 인정받는 시기입니다. 승진이나 리더 자리를 제안받을 수 있습니다.", "Responsibilities grow, but so does recognition. Promotion is possible.", "⭐⭐⭐⭐"),
            ("10월", "문서 운이 아주 좋습니다. 부동산 계약이나 중요한 도장을 찍기에 길한 달입니다.", "Great luck with documents. Good for real estate or contracts.", "⭐⭐⭐⭐⭐"),
            ("11월", "꽉 막혔던 일이 귀인(윗사람)의 도움으로 시원하게 뚫립니다. 조언을 구하세요.", "Blocked problems are solved with help from a mentor.", "⭐⭐⭐⭐"),
            ("12월", "학업이나 자격증 시험에 행운이 따릅니다. 새로운 것을 배우기에 딱 좋은 연말입니다.", "Good luck with studies or exams. Perfect time to learn.", "⭐⭐⭐⭐")
        ],
        "Fire": [
            ("1월", "생각이 너무 많아 머리가 아픕니다. 스트레스성 두통을 주의하고 멍 때리는 시간을 가지세요.", "Too many thoughts cause headaches. Relax and clear your mind.", "⭐⭐"),
            ("2월", "귀인이 나타나 나를 끌어줍니다. 취업이나 합격 소식을 듣기에 아주 좋은 달입니다.", "A noble person appears. Great month for job offers or passing exams.", "⭐⭐⭐⭐⭐"),
            ("3월", "마음이 호수처럼 편안해집니다. 중요한 계약이나 약속을 잡기에 적합합니다.", "Peace of mind returns. Suitable for important contracts.", "⭐⭐⭐⭐"),
            ("4월", "자신감을 가지고 나를 드러내세요. 내 매력이 돈이 되고 기회가 되는 시기입니다.", "Express yourself. Your charm turns into money and opportunities.", "⭐⭐⭐⭐"),
            ("5월", "주변 사람들과 의견 충돌이 잦습니다. 이기려 하지 말고 '그럴 수도 있지' 하고 넘기세요.", "Conflicts increase. Don't try to win every argument.", "⭐⭐"),
            ("6월", "고집을 부리다가 다 된 밥에 재 뿌릴 수 있습니다. 동료와 협력해야만 이득을 봅니다.", "Stubbornness leads to failure. Cooperation is the only way.", "⭐⭐"),
            ("7월", "말 한마디로 천 냥 빚을 갚습니다. 영업이나 미팅에서 최고의 성과를 올립니다.", "Your words have power. Great results in sales or meetings.", "⭐⭐⭐⭐⭐"),
            ("8월", "큰 돈이 들어올 기회가 보입니다. 다만, 들어온 만큼 나갈 수 있으니 지갑을 닫으세요.", "Opportunity for big money, but expenses rise too. Manage spending.", "⭐⭐⭐"),
            ("9월", "재물운이 폭발하지만 지출도 큽니다. 기분파 쇼핑을 조심해야 하는 달입니다.", "Wealth luck explodes, but beware of emotional shopping.", "⭐⭐⭐⭐"),
            ("10월", "그동안의 노력에 대한 확실한 보상을 받습니다. 인센티브나 상을 받을 수 있습니다.", "Sure rewards for your efforts. Expect incentives or awards.", "⭐⭐⭐⭐⭐"),
            ("11월", "상사의 압박이나 업무량이 과도합니다. 지금은 납작 엎드려 때를 기다려야 합니다.", "High pressure from bosses. Stay low and wait for the right time.", "⭐⭐"),
            ("12월", "일은 힘들지만 명예는 올라갑니다. 사람들이 당신의 능력을 알아주기 시작합니다.", "Hard work leads to honor. People recognize your abilities.", "⭐⭐⭐⭐")
        ],
        "Earth": [
            ("1월", "이직이나 이사 등 이동수가 있습니다. 섣불리 움직이지 말고 신중하게 결정하세요.", "Possibility of moving or changing jobs. Decide carefully.", "⭐⭐⭐"),
            ("2월", "명예운이 상승합니다. 남들이 부러워할 만한 감투를 쓰거나 스카우트 제의가 옵니다.", "Honor rises. You might get a prestigious title or scout offer.", "⭐⭐⭐⭐⭐"),
            ("3월", "능력을 인정받아 승진하거나 중요한 직책을 맡게 됩니다. 리더십을 발휘하세요.", "Promotion or important role awaits. Show your leadership.", "⭐⭐⭐⭐"),
            ("4월", "오랜만에 친구들을 만나 회포를 풉니다. 지출은 좀 있겠지만 즐거운 한 달입니다.", "Meeting friends brings joy. Expenses rise, but it's happy.", "⭐⭐⭐"),
            ("5월", "집중력이 최고조에 달합니다. 미뤄뒀던 공부나 연구를 하기에 최적의 시기입니다.", "Concentration peaks. Best time to study or research.", "⭐⭐⭐⭐"),
            ("6월", "문서운이 대길합니다. 집을 사거나 중요한 계약을 하기에 더할 나위 없습니다.", "Great document luck. Perfect for buying a house.", "⭐⭐⭐⭐⭐"),
            ("7월", "혼자 끙끙 앓던 문제를 동료와 함께 해결합니다. 팀워크가 빛을 발합니다.", "Solve problems with colleagues. Teamwork shines.", "⭐⭐⭐⭐"),
            ("8월", "새로운 취미나 예술 활동을 시작해보세요. 의외의 재능을 발견하게 됩니다.", "Start a new hobby. You might discover unexpected talents.", "⭐⭐⭐⭐"),
            ("9월", "말주변이 좋아져서 어딜 가나 인기가 많습니다. 인맥을 넓히기 좋은 달입니다.", "Eloquence improves. Good month to expand your network.", "⭐⭐⭐⭐"),
            ("10월", "생각지도 못한 용돈이나 수익이 생깁니다. 작게라도 투자를 해봐도 좋습니다.", "Unexpected profit. Small investments are okay.", "⭐⭐⭐⭐"),
            ("11월", "눈앞에 큰 돈이 보이지만 욕심내면 낭패를 봅니다. 돌다리도 두들겨 보고 건너세요.", "Big money is visible, but greed causes failure. Be cautious.", "⭐⭐"),
            ("12월", "사업이나 프로젝트의 결실을 맺습니다. 수금하기 좋고 통장이 두둑해집니다.", "Reap rewards of projects. Good for collecting payments.", "⭐⭐⭐⭐⭐")
        ],
        "Metal": [
            ("1월", "먹을 복이 터졌습니다. 재물운도 좋으니 맛있는 것을 먹으며 자신을 대접하세요.", "Good luck with food and money. Treat yourself.", "⭐⭐⭐⭐"),
            ("2월", "요행을 바라지 마세요. 땀 흘린 만큼 정확하게 통장에 꽂히는 정직한 달입니다.", "Don't expect luck. You earn exactly what you work for.", "⭐⭐⭐"),
            ("3월", "예상치 못한 보너스나 성과급을 받습니다. 기분 좋은 비명을 지르게 됩니다.", "Unexpected bonus or incentive. Screaming with joy.", "⭐⭐⭐⭐⭐"),
            ("4월", "문서 계약 시 꼼꼼히 확인하세요. 작은 글씨를 못 봐서 손해 볼 수 있습니다.", "Check documents carefully. Missing fine print causes loss.", "⭐⭐"),
            ("5월", "관재구설(법적 다툼이나 말썽)이 따를 수 있습니다. 입을 무겁게 하고 조용히 지내세요.", "Legal issues or gossip may arise. Keep quiet.", "⭐⭐"),
            ("6월", "직장 스트레스가 최고조입니다. '이 또한 지나가리라'는 마음으로 멘탈을 잡으세요.", "Work stress is extreme. Keep your mental balance.", "⭐⭐"),
            ("7월", "위기 상황에서 윗사람이 구원의 손길을 내밉니다. 자존심 굽히고 도움을 받으세요.", "Superiors help in crisis. Swallow pride and accept help.", "⭐⭐⭐"),
            ("8월", "주관이 뚜렷해지는 건 좋지만, 남들이 볼 땐 똥고집입니다. 유연함이 필요합니다.", "Strong will is good, but don't be stubborn. Be flexible.", "⭐⭐"),
            ("9월", "누구와 붙어도 이길 수 있는 에너지가 있습니다. 경쟁이나 입찰에서 승리합니다.", "Energy to win against anyone. Victory in competition.", "⭐⭐⭐⭐⭐"),
            ("10월", "나를 물심양면으로 도와주는 귀인이 나타납니다. 인복이 터지는 달입니다.", "A noble person appears. Luck with people explodes.", "⭐⭐⭐⭐⭐"),
            ("11월", "나의 재능을 맘껏 펼치고 박수받습니다. 무대 위 주인공이 되는 시기입니다.", "Show off talents and get applause. You are the star.", "⭐⭐⭐⭐"),
            ("12월", "연말 모임에서 말실수로 오해를 살 수 있습니다. 술자리에서 특히 조심하세요.", "Slip of the tongue at parties causes misunderstanding.", "⭐⭐")
        ],
        "Water": [
            ("1월", "창의력이 화수분처럼 쏟아집니다. 예술이나 기획 분야라면 대박을 터뜨립니다.", "Creativity flows endlessly. Success in arts or planning.", "⭐⭐⭐⭐⭐"),
            ("2월", "새로운 일을 시작하거나 계획하기 딱 좋습니다. 시작이 반입니다.", "Perfect time to start new things. Well begun is half done.", "⭐⭐⭐⭐"),
            ("3월", "아랫사람이나 자녀에게 좋은 일이 생깁니다. 덕분에 나까지 웃게 됩니다.", "Good news for subordinates or children. It makes you smile.", "⭐⭐⭐⭐"),
            ("4월", "직장에서 승진하거나 중요한 책임을 맡습니다. 어깨가 무겁지만 기회입니다.", "Promotion or heavy responsibility. A burden but an opportunity.", "⭐⭐⭐⭐"),
            ("5월", "일확천금의 유혹이 옵니다. 투기나 도박은 패가망신의 지름길이니 절대 금지.", "Temptation of jackpot. Gambling leads to ruin.", "⭐⭐"),
            ("6월", "돈은 많이 들어오는데 나갈 구멍도 많습니다. 가계부를 꼼꼼히 써야 합니다.", "Money comes in but leaks out. Keep a strict budget.", "⭐⭐⭐"),
            ("7월", "명예가 올라가고 여기저기서 나를 찾습니다. 인기 관리를 잘해야 합니다.", "Honor rises and people seek you. Manage popularity.", "⭐⭐⭐⭐"),
            ("8월", "깊이 있는 공부나 연구에 몰두하면 큰 성과를 냅니다. 전문가로 인정받습니다.", "Focus on study brings results. Recognized as an expert.", "⭐⭐⭐⭐"),
            ("9월", "국가 자격증이나 학위 취득 등 문서와 관련된 경사가 있습니다.", "Good news regarding certifications or degrees.", "⭐⭐⭐⭐"),
            ("10월", "사사건건 방해하는 경쟁자가 나타나 스트레스를 줍니다. 무시하는 게 답입니다.", "Annoying competitors cause stress. Ignore them.", "⭐⭐"),
            ("11월", "친한 친구와 돈 문제로 의 상할 수 있습니다. 밥은 사되 돈은 빌려주지 마세요.", "Money issues with friends. Don't lend cash.", "⭐⭐"),
            ("12월", "자존심 때문에 사랑하는 사람과 다툴 수 있습니다. 이번 한 번만 져주세요.", "Pride causes fights with loved ones. Just lose this time.", "⭐⭐")
        ]
    }
    
    months = data[element]
    result = []
    
    for mon_ko, text_ko, text_en, star_rating in months:
        msg = text_ko if lang == "ko" else text_en
        month_label = mon_ko
        if lang != "ko":
            month_map = {"1월":"Jan", "2월":"Feb", "3월":"Mar", "4월":"Apr", "5월":"May", "6월":"Jun", "7월":"Jul", "8월":"Aug", "9월":"Sep", "10월":"Oct", "11월":"Nov", "12월":"Dec"}
            month_label = month_map.get(mon_ko, mon_ko)
        
        result.append({"Month": month_label, "Luck": star_rating, "Advice": msg})
    
    return result

# ----------------------------------------------------------------
# 4. 메인 로직 시작
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    st.stop()

# 텍스트 리소스
ui = {
    "ko": {
        "title": "디 엘리먼트: 2026년 정밀 운세",
        "lock": "🔒 유료 서비스 ($10)",
        "label": "이메일로 받은 라이센스 키 입력",
        "btn": "확인 (Unlock)",
        "lock_warn": "⚠️ 주의: 이 키는 3회까지만 사용할 수 있습니다.",
        "welcome": f"환영합니다, {st.session_state['user_name']}님!",
        "h_trait": "🔮 타고난 기질",
        "h_fore": "📅 2026년 운세 분석",
        "print_btn": "🖨️ 결과 인쇄하기 (Print Result)"
    },
    "en": {
        "title": "The Element: 2026 Forecast",
        "lock": "🔒 Premium Service ($10)",
        "label": "Enter License Key from Email",
        "btn": "Unlock",
        "lock_warn": "⚠️ Warning: This key can be used up to 3 times only.",
        "welcome": f"Welcome, {st.session_state['user_name']}!",
        "h_trait": "🔮 Personality",
        "h_fore": "📅 2026 Forecast",
        "print_btn": "🖨️ Print Result"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 5. 잠금 해제 (Gumroad + MasterKey)
# ----------------------------------------------------------------
if "unlocked_2026" not in st.session_state: st.session_state["unlocked_2026"] = False

# 🌟 팝업창(Dialog) 함수
@st.dialog("⚠️ Usage Limit Warning")
def show_limit_warning():
    st.warning(t['lock_warn'], icon="⚠️")
    st.write("Checking this result will deduct 1 credit from your license.")
    if st.button("I Understand & Proceed", type="primary"):
        st.rerun()

if not st.session_state["unlocked_2026"]:
    with st.container(border=True):
        st.write(t['lock'])
        
        # 3회 제한 팝업 버튼
        if st.button("⚠️ Check Limit Info", type="secondary"):
            show_limit_warning()
            
        st.link_button("💳 Buy Now ($10)", GUMROAD_LINK)
        
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn']):
            if key == UNLOCK_CODE:
                st.session_state["unlocked_2026"] = True
                st.success("Master Key Accepted!")
                st.rerun()
            
            try:
                response = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={
                        "product_permalink": PRODUCT_PERMALINK,
                        "license_key": key
                    }
                )
                data = response.json()

                if data.get("success"):
                    current_uses = data.get("uses", 0)
                    if current_uses > 3:
                        st.error("🚫 Limit exceeded (Max 3 uses).")
                    else:
                        st.session_state["unlocked_2026"] = True
                        st.success("Success!")
                        st.rerun()
                else:
                    st.error("🚫 Invalid License Key.")
            
            except Exception as e:
                st.error("Connection Error.")
    st.stop()

# ----------------------------------------------------------------
# 6. 결과 화면 (잠금 해제 후)
# ----------------------------------------------------------------
st.divider()

day_info = calculate_day_gan(st.session_state["birth_date"])
e_type = day_info['element']
trait, forecast = get_interpretation(e_type, lang)

# 1. 성격 분석
st.subheader(f"{t['h_trait']}")
st.markdown(f"""
<div class='card'>
    <h3 style='color:#64748b'>👋 {st.session_state['user_name']}</h3>
    <h1 style='color:#4f46e5'>{day_info[lang]} ({e_type})</h1>
    <div style='margin-top:10px;'>{trait}</div>
</div>
""", unsafe_allow_html=True)

# 2. 2026 운세
st.subheader(f"{t['h_fore']}")
st.markdown(f"""
<div class='card' style='border:1px solid #ec4899'>
    <h2 style='color:#be185d'>👑 {forecast['title']}</h2>
    <p>{forecast['gen']}</p>
    <p><b>💰 Money:</b> {forecast['money']} <br> <b>❤️ Love:</b> {forecast['love']}</p>
</div>
""", unsafe_allow_html=True)

# 3. 월별 표
monthly_data = get_monthly_forecast_unique(e_type, lang)
df = pd.DataFrame(monthly_data)
df = df.set_index(list(df.columns)[0]) 
st.table(df)

# 4. 인쇄 버튼
st.divider()
components.html(
    f"""
    <script>
        function printParent() {{
            window.parent.print();
        }}
    </script>
    <div style="display: flex; justify-content: center;">
        <button onclick="printParent()" style="
            background-color: #FF4B4B; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            text-align: center; 
            font-size: 16px; 
            cursor: pointer;
            border-radius: 8px;
            font-family: sans-serif;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        ">
            {t['print_btn']}
        </button>
    </div>
    """,
    height=100
)
