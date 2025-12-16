import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime, date

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Pro Report", page_icon="🔮", layout="wide")

# 스타일 (CSS) - 인쇄 최적화 및 디자인
st.markdown("""
<style>
    .main-header {font-size: 2.5em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 10px;}
    .sub-header {font-size: 1.1em; color: #64748b; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 25px;}
    .highlight {color: #4f46e5; font-weight: bold;}
    
    /* 인쇄 버튼 스타일 */
    div.stButton > button {
        background-color: #4f46e5; color: white; border: none; padding: 10px 20px; 
        border-radius: 8px; font-weight: bold; width: 100%; margin-top: 10px;
    }
    div.stButton > button:hover {background-color: #4338ca;}

    /* 🖨️ 인쇄 모드 (종이 출력 시 적용) */
    @media print {
        body * { visibility: hidden; }
        .card, .card * { visibility: visible; }
        .card {
            position: absolute; left: 0; top: 0; width: 100%;
            margin: 0; padding: 20px;
            background-color: white !important; color: black !important;
            border: none !important; box-shadow: none !important;
        }
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, footer { display: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 만세력 엔진 (일주 계산) ---
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1)
    delta = birth_date - base_date
    if delta.days < 0: return 0
    gan_index = delta.days % 10
    gans = [
        {"ko": "갑목(甲)", "en": "Yang Wood (Gap)", "element": "Wood"},
        {"ko": "을목(乙)", "en": "Yin Wood (Eul)", "element": "Wood"},
        {"ko": "병화(丙)", "en": "Yang Fire (Byeong)", "element": "Fire"},
        {"ko": "정화(丁)", "en": "Yin Fire (Jeong)", "element": "Fire"},
        {"ko": "무토(戊)", "en": "Yang Earth (Mu)", "element": "Earth"},
        {"ko": "기토(己)", "en": "Yin Earth (Gi)", "element": "Earth"},
        {"ko": "경금(庚)", "en": "Yang Metal (Gyeong)", "element": "Metal"},
        {"ko": "신금(辛)", "en": "Yin Metal (Sin)", "element": "Metal"},
        {"ko": "임수(壬)", "en": "Yang Water (Im)", "element": "Water"},
        {"ko": "계수(癸)", "en": "Yin Water (Gye)", "element": "Water"}
    ]
    return gans[gan_index]
    
# --- 3. 데이터베이스 (성격 & 운세) ---
def get_interpretation(element, lang):
    # 한국어 상세 데이터
    traits_ko = {
        "Wood": """#### 🌲 총론: 곧게 뻗는 성장의 아이콘
당신은 뚫고 나가는 힘이 강한 '개척자'입니다. 인정이 많고 착하지만, 한번 고집을 피우면 아무도 못 말립니다. 남의 밑에 있기보다 내가 대장이 되어야 직성이 풀리는 스타일입니다.

#### 💰 재물운: 차곡차곡 쌓는 거목
요행을 바라기보다 자신의 노력으로 정직하게 부를 축적합니다. 처음에는 느려 보여도 시간이 갈수록 뿌리가 깊어져 말년에는 큰 부자가 될 그릇입니다.

#### 💼 직장/사업운: 기획과 교육의 리더
새로운 일을 기획하거나 사람을 가르치는 일이 천직입니다. (교육, 건축, 디자인, 스타트업). 융통성만 조금 더한다면 조직의 최고 자리에 오를 수 있습니다.

#### ❤️ 연애운: 내 사람은 내가 지킨다
연애할 때도 리드하는 것을 좋아합니다. 상대방을 책임지려는 마음이 강합니다. 다만 가끔은 상대방의 의견을 굽혀주는 부드러움이 필요합니다.""",

        "Fire": """#### 🔥 총론: 세상을 밝히는 열정의 태양
당신은 에너지가 넘치고 솔직한 '비전가'입니다. 예의가 바르고 화끈해서 주변에 사람이 끊이지 않습니다. 비밀이 없고 감정이 얼굴에 다 드러나는 투명한 사람입니다.

#### 💰 재물운: 화려하지만 관리가 필요해
돈을 버는 능력은 탁월하나, 쓰는 씀씀이도 큽니다. 기분에 따라 한턱내는 것을 좋아해 돈이 모이기 힘들 수 있습니다. 통장 관리를 꼼꼼히 해야 부자가 됩니다.

#### 💼 직장/사업운: 무대 체질, 말로 먹고산다
자신을 드러내는 일이 맞습니다. (방송, 예술, 영업, 정치, 유튜버). 반복적이고 지루한 사무직보다는 변화가 많은 곳에서 능력을 발휘합니다.

#### ❤️ 연애운: 금방 뜨거워지는 사랑
첫눈에 반하는 금사빠 기질이 있습니다. 열정적인 사랑을 하지만 빨리 식을 수도 있습니다. 밀당보다는 직설적인 고백이 통하는 스타일입니다.""",

        "Earth": """#### ⛰️ 총론: 묵직한 신용의 수호자
당신은 모든 것을 품어주는 넓은 땅입니다. 입이 무겁고 신용을 목숨처럼 아낍니다. 속마음을 잘 드러내지 않아 답답해 보일 수 있지만, 한번 믿은 사람은 끝까지 배신하지 않습니다.

#### 💰 재물운: 부동산이 최고의 파트너
현금보다는 땅이나 건물 같은 '문서' 형태의 재산이 잘 맞습니다. 묵묵히 저축하고 지키는 능력이 뛰어나 알부자가 많습니다.

#### 💼 직장/사업운: 중간 관리자와 중개자
사람과 사람 사이를 연결하거나 갈등을 중재하는 능력이 탁월합니다. (부동산, 컨설팅, 농업, 종교). 변화가 적고 안정적인 조직에서 빛을 발합니다.

#### ❤️ 연애운: 은근하고 오래가는 뚝배기
표현이 서툴러 재미없다는 소리를 들을 수 있지만, 한결같은 해바라기입니다. 화려한 이벤트보다 진심 어린 믿음을 주는 연애를 선호합니다.""",

        "Metal": """#### ⚔️ 총론: 결단력 있는 정의의 사도
당신은 맺고 끊음이 확실한 '장군'감입니다. 의리를 중요시하고 불의를 보면 참지 못합니다. 차가워 보이지만 내 사람에게는 확실하게 정을 주는 '츤데레' 매력이 있습니다.

#### 💰 재물운: 확실한 결과와 성과
일한 만큼 확실하게 보상받아야 직성이 풀립니다. 승부욕이 강해 경쟁을 통해 남보다 더 많은 부를 쟁취해냅니다.

#### 💼 직장/사업운: 권력과 기술의 조화
원칙이 중요한 분야가 어울립니다. (군인, 경찰, 금융, 엔지니어, 의료). 흐지부지한 것을 싫어해 리더가 되면 카리스마 있게 조직을 이끕니다.

#### ❤️ 연애운: 확실한 내 편 만들기
좋고 싫음이 분명합니다. 질질 끄는 썸을 싫어하고 확실한 관계 정립을 원합니다. 한번 마음을 주면 변치 않는 의리 있는 사랑을 합니다.""",

        "Water": """#### 🌊 총론: 유연한 지혜의 전략가
당신은 어디든 흐르는 물처럼 적응력이 뛰어납니다. 머리가 비상하고 기획력이 좋으며, 겉으로는 부드러워 보이나 속은 깊고 냉철합니다.

#### 💰 재물운: 흐름을 읽는 투자의 귀재
돈의 흐름을 본능적으로 읽어냅니다. 유통, 무역, 투자 등 돈이 도는 길목을 지키면 큰돈을 만집니다. 해외와 인연이 깊습니다.

#### 💼 직장/사업운: 두뇌 플레이어
몸을 쓰는 일보다 머리를 쓰는 일이 맞습니다. (기획, 연구, 무역, 심리 상담). 남들이 보지 못하는 틈새시장을 찾아내는 눈이 있습니다.

#### ❤️ 연애운: 매력적인 미스터리
상대방의 마음을 잘 맞춰주는 배려심이 있습니다. 하지만 자신의 속은 다 보여주지 않아 신비로운 매력을 풍깁니다. 집착보다는 자유로운 연애를 지향합니다."""
    }

    # 영어 상세 데이터
    traits_en = {
        "Wood": """#### 🌲 General: The Icon of Growth
You are a 'Pioneer' with strong drive. You are benevolent but stubborn. You prefer to lead rather than follow.

#### 💰 Wealth: Steady Accumulation
You build wealth through honest effort rather than luck. Like a tree, your assets grow larger and deeper over time.

#### 💼 Career: Planner & Educator
You excel in planning or teaching. (Education, Design, Startups). You can reach the top if you learn to be a bit more flexible.

#### ❤️ Love: Protective Leader
You like to lead in relationships. You have a strong desire to protect your partner. Try to listen more to your partner's opinions.""",

        "Fire": """#### 🔥 General: Passionate Visionary
You are like the sun—energetic and honest. You are polite and transparent; your emotions show clearly on your face.

#### 💰 Wealth: High Flow
You are great at making money but also great at spending it. You need to manage your expenses carefully to build true wealth.

#### 💼 Career: Born for the Stage
You shine in jobs where you can express yourself. (Arts, Media, Sales, Politics). You thrive in dynamic environments.

#### ❤️ Love: Hot & Fast
You fall in love quickly and passionately. You prefer direct confessions over playing hard-to-get.""",

        "Earth": """#### ⛰️ General: Guardian of Trust
You are steady like a mountain. You value trust above all else. You don't reveal your feelings easily, but you never betray a friend.

#### 💰 Wealth: Real Estate Expert
Assets like land or buildings suit you better than cash. You have a talent for saving and protecting your wealth.

#### 💼 Career: Mediator & Manager
You excel at connecting people or resolving conflicts. (Real Estate, Consulting, Religion). You shine in stable organizations.

#### ❤️ Love: Steady Sunflower
You might seem quiet, but your love is unchanging. You prefer sincere trust over flashy events.""",

        "Metal": """#### ⚔️ General: Decisive Warrior
You value justice and loyalty. You are decisive and hate ambiguity. You have a 'tough on the outside, soft on the inside' charm.

#### 💰 Wealth: Result-Oriented
You want clear rewards for your work. Your competitive spirit helps you earn more than others.

#### 💼 Career: Power & Tech
You suit fields where principles matter. (Finance, Engineering, Military, Medicine). You are a charismatic leader.

#### ❤️ Love: Clear Boundaries
You dislike ambiguous relationships. Once you commit, you offer a loyal and responsible love.""",

        "Water": """#### 🌊 General: Wise Strategist
You are adaptable like water. You are incredibly smart and a deep thinker. You appear soft, but your mind is sharp.

#### 💰 Wealth: Master of Flow
You instinctively read the flow of money. You can succeed in trade, investment, or distribution.

#### 💼 Career: Brain Player
You excel in intellectual fields. (Planning, Research, Trade, Psychology). You can find niche markets others miss.

#### ❤️ Love: Mysterious Charisma
You are caring and adaptable, but you keep a secret side. This mystery makes you attractive to others."""
    }

    # 2026 총평
    forecast_ko = {}
    forecast_en = {}
    
    if element == "Wood":
        forecast_ko = {"title": "🔥 재능 폭발의 해 (식상운)", "gen": "나를 태워 세상을 밝히는 형국입니다. 당신의 재능이 꽃을 피우고, 바쁘게 움직일수록 성과가 따릅니다. 다만 건강을 해칠 수 있으니 선택과 집중이 필요합니다.", "money": "수입 증가, 품위 유지비 지출 증가.", "love": "표현력이 좋아져 인기가 많아집니다."}
        forecast_en = {"title": "🔥 Year of Talent (Output)", "gen": "You burn bright. Your talents bloom. Being busy leads to success, but avoid burnout.", "money": "Income rises, but expenses also rise.", "love": "Popularity increases. Great for romance."}
    elif element == "Fire":
        forecast_ko = {"title": "🤝 경쟁과 협력의 해 (비겁운)", "gen": "에너지가 넘칩니다. 자존심이 강해지고 경쟁자가 나타나지만, 동료와 협력할 때 더 큰 성과를 냅니다. 독립 욕구가 강해집니다.", "money": "공동 투자 신중. 돈 거래 금지.", "love": "친구가 연인으로 발전 가능."}
        forecast_en = {"title": "🤝 Year of Competition", "gen": "Energy is high. Rivals appear. Cooperate to win. Desire for independence grows.", "money": "Caution with joint investments.", "love": "Friends may turn into lovers."}
    elif element == "Earth":
        forecast_ko = {"title": "📜 문서와 귀인의 해 (인성운)", "gen": "윗사람의 도움을 받고, 학업이나 계약에서 좋은 성과를 냅니다. 부동산 취득이나 자격증 시험에 아주 유리한 시기입니다.", "money": "부동산, 주식 등 문서 이득.", "love": "사랑받는 시기. 듬직한 인연."}
        forecast_en = {"title": "📜 Year of Resources", "gen": "Help from superiors. Success in contracts and studies. Good for real estate.", "money": "Gains from assets/documents.", "love": "You will be loved and cared for."}
    elif element == "Metal":
        forecast_ko = {"title": "🔨 명예와 승진의 해 (관성운)", "gen": "직장에서 책임감이 커지고 압박이 있지만, 이를 견디면 확실한 승진과 명예가 따릅니다. 조직에서 자리를 잡는 중요한 해입니다.", "money": "고정 수입 증가, 승진 보너스.", "love": "여자는 남자가 들어오는 운."}
        forecast_en = {"title": "🔨 Year of Honor", "gen": "More responsibility at work. Enduring pressure brings promotion. Crucial career year.", "money": "Stable income increases.", "love": "Women may meet a partner."}
    elif element == "Water":
        forecast_ko = {"title": "💰 재물 쟁취의 해 (재성운)", "gen": "큰 돈을 벌 기회가 오지만, 치열하게 싸워야 쟁취할 수 있습니다. 결과가 확실하게 나오는 해입니다.", "money": "사업 확장, 투자 수익 기대.", "love": "남자는 매력적인 이성 만남."}
        forecast_en = {"title": "💰 Year of Wealth", "gen": "Huge financial opportunities. You must fight to claim them. Clear results.", "money": "Business expansion gains.", "love": "Men will meet attractive partners."}

    if lang == "ko": return traits_ko[element], forecast_ko
    else: return traits_en[element], forecast_en

# --- 4. 월별 정밀 운세 (1월~12월 순서로 정렬) ---
def get_monthly_forecast_unique(element, lang):
    # 각 오행별 12개월(1월~12월) 순서대로 정렬
    data = {
        "Wood": [
            ("1월", "친구가 돈을 빌려달라고 합니다. 거절하세요.", "Friends may ask for money. Refuse politely."),
            ("2월", "경쟁자가 나타납니다. 실속을 챙기세요.", "Competition arises. Focus on benefits."),
            ("3월", "사람들과 어울리며 말실수 조심.", "Socializing increases. Watch your words."),
            ("4월", "뜻밖의 재물이 들어옵니다. 꽁돈 운!", "Unexpected money or bonus comes in."),
            ("5월", "아이디어가 샘솟습니다. 활동하기 최고입니다.", "Great ideas flow. Best time for action."),
            ("6월", "몸이 열 개라도 모자랍니다. 건강 챙기세요.", "Extremely busy. Take care of health."),
            ("7월", "재물운이 안정적입니다. 저축하기 좋은 달.", "Financial stability. Good month to save."),
            ("8월", "직장 스트레스. 참는 자에게 복이 옵니다.", "Stress at work. Patience brings luck."),
            ("9월", "책임질 일이 늘어납니다. 인정받는 시기.", "Responsibilities grow. Success brings recognition."),
            ("10월", "부동산이나 계약 관련 좋은 소식.", "Good news regarding real estate or contracts."),
            ("11월", "윗사람의 도움으로 막힌 일이 뚫립니다.", "Help from superiors solves problems."),
            ("12월", "공부나 자격증 취득에 행운이 따릅니다.", "Good luck with studies or certifications.")
        ],
        "Fire": [
            ("1월", "스트레스성 두통 주의. 건강검진 필요.", "Watch out for stress. Get a checkup."),
            ("2월", "귀인이 나타나 도와줍니다. 합격운 대길.", "Mentors appear. Good luck for exams."),
            ("3월", "마음이 편안하고 계약하기 좋은 달입니다.", "Peaceful mind. Good for signing contracts."),
            ("4월", "자신감을 표현하면 돈이 됩니다.", "Express confidence to make money."),
            ("5월", "경쟁이 치열합니다. 다툼 주의.", "Fierce competition. Avoid arguments."),
            ("6월", "고집을 부리면 손해를 봅니다. 협력하세요.", "Stubbornness leads to loss. Cooperate."),
            ("7월", "말 한마디로 천 냥 빚을 갚습니다. 영업운 최고.", "Your words have power. Great for sales."),
            ("8월", "큰 돈이 들어올 기회입니다. 투자 검토.", "Opportunity for big money. Consider investing."),
            ("9월", "재물운 폭발. 다만 지출도 큽니다.", "Explosive wealth luck, but high expenses."),
            ("10월", "성과에 대한 확실한 보상을 받습니다.", "Sure rewards for your performance."),
            ("11월", "상사의 압박이 심합니다. 휴식 필요.", "Pressure from bosses. Rest is needed."),
            ("12월", "업무량이 많아지지만 명예는 올라갑니다.", "Workload increases, but honor rises.")
        ],
        "Earth": [
            ("1월", "직장 변동수. 신중하게 결정하세요.", "Job change possible. Decide carefully."),
            ("2월", "명예운 상승. 승진이나 스카우트 제의.", "Honor rises. Promotion or scout offers."),
            ("3월", "능력을 인정받아 감투를 씁니다.", "Recognized at work, get a new title."),
            ("4월", "친구들과 만나 돈 쓸 일이 많아집니다.", "Spending money with friends increases."),
            ("5월", "공부하기 딱 좋은 시기. 집중력 최고.", "Perfect for study. Concentration improves."),
            ("6월", "계약서에 도장 찍을 일. 문서운 대길.", "Signing contracts. Great document luck."),
            ("7월", "동료와 협력하여 문제를 해결합니다.", "Solve problems with colleagues."),
            ("8월", "새로운 취미나 창작 활동 시작.", "Start a new hobby or creative activity."),
            ("9월", "말주변이 좋아져 인기가 많아집니다.", "Eloquence improves, popularity rises."),
            ("10월", "생각지도 못한 용돈이나 수익.", "Unexpected allowance or profit."),
            ("11월", "큰 돈이 보이지만 욕심내면 낭패.", "Big money visible, but greed causes failure."),
            ("12월", "사업 성과가 나타납니다. 수금하세요.", "Business results appear. Collect payments.")
        ],
        "Metal": [
            ("1월", "재물운이 좋습니다. 맛있는 것 드세요.", "Good financial luck. Treat yourself."),
            ("2월", "노력한 만큼 돈이 쌓입니다. 성실함이 무기.", "Hard work pays off. Diligence is key."),
            ("3월", "예상치 못한 보너스를 받습니다.", "Unexpected bonus possible."),
            ("4월", "문서 계약 시 꼼꼼히 확인하세요.", "Check documents carefully."),
            ("5월", "관재구설 주의. 조용히 지내세요.", "Avoid disputes. Stay low profile."),
            ("6월", "직장 스트레스 최고조. 멘탈 관리.", "Extreme work stress. Mental care needed."),
            ("7월", "윗사람의 도움으로 위기를 넘깁니다.", "Help from superiors saves the day."),
            ("8월", "주관이 뚜렷해지지만 고집으로 보일 수 있음.", "Strong will, but may seem stubborn."),
            ("9월", "경쟁심이 생겨 성과를 냅니다. 이기는 달.", "Competitive spirit leads to results."),
            ("10월", "나를 도와주는 귀인이 나타납니다.", "A helpful noble person appears."),
            ("11월", "재능 발휘로 박수받는 달.", "Solve problems with talent. Applause."),
            ("12월", "말을 아끼세요. 오해가 생깁니다.", "Save your words. Misunderstandings possible.")
        ],
        "Water": [
            ("1월", "창의력이 폭발합니다. 예술 활동 대길.", "Creativity explodes. Great for arts."),
            ("2월", "새로운 일을 기획하기 좋습니다.", "Great to plan or start new things."),
            ("3월", "자녀 경사 혹은 아랫사람 덕을 봅니다.", "Good news for children or help from juniors."),
            ("4월", "승진하거나 책임이 무거워집니다.", "Promotion or heavy responsibility at work."),
            ("5월", "일확천금 꿈은 위험합니다. 투기 금지.", "Dream of jackpot but risky. No speculation."),
            ("6월", "재물운 좋지만 지출도 큽니다.", "Good wealth luck but high expenses."),
            ("7월", "명예가 올라가고 사람들이 찾습니다.", "Honor rises, people seek you out."),
            ("8월", "공부나 연구에 몰두하면 큰 성과.", "Focus on study/research brings results."),
            ("9월", "자격증을 따거나 계약하기 좋은 달.", "Good for certifications or contracts."),
            ("10월", "방해하는 경쟁자가 나타납니다.", "Competitors appear to hinder you."),
            ("11월", "친구와 돈 문제로 다투지 마세요.", "Don't fight over money with friends."),
            ("12월", "자존심 때문에 충돌 주의.", "High pride may cause conflicts.")
        ]
    }
    
    months = data[element]
    result = []
    
    for mon_ko, text_ko, text_en in months:
        msg = text_ko if lang == "ko" else text_en
        score = "⭐⭐⭐"
        if "주의" in text_ko or "조심" in text_ko or "스트레스" in text_ko: score = "⭐⭐"
        if "최고" in text_ko or "대길" in text_ko or "폭발" in text_ko or "행운" in text_ko: score = "⭐⭐⭐⭐⭐"
        if "좋은" in text_ko or "이득" in text_ko: score = "⭐⭐⭐⭐"
        
        # 날짜 포맷 (영어는 Jan, Feb...)
        month_label = mon_ko
        if lang != "ko":
            month_map = {"1월":"Jan", "2월":"Feb", "3월":"Mar", "4월":"Apr", "5월":"May", "6월":"Jun", "7월":"Jul", "8월":"Aug", "9월":"Sep", "10월":"Oct", "11월":"Nov", "12월":"Dec"}
            month_label = month_map.get(mon_ko, mon_ko)
            
        result.append({"Month": month_label, "Luck": score, "Advice": msg})
        
    return result

# --- 5. 메인 실행 ---
def main():
    with st.sidebar:
        st.title("Settings")
        lang_opt = st.radio("Language", ["한국어", "English"])
        lang = "ko" if "Korean" in lang_opt else "en"
        st.info("💡 **Tip:** Click 'Print Report' to save as PDF.")

    ui = {
        "ko": {
            "title": "디 엘리먼트: 사주 프로", "sub": "당신의 운명 지도와 2026년 정밀 분석", 
            "name": "이름", "btn": "운명 분석하기", 
            "tab1": "🔮 타고난 기질", "tab2": "📅 2026년 정밀 운세", 
            "print": "🖨️ 리포트 인쇄하기",
            "t_mon": "월 (Month)", 
            "t_sco": "운세 점수 (5점 만점)", 
            "t_adv": "상세 조언",
            "legend": "※ 별점 기준: ⭐⭐⭐⭐⭐ (최고) ~ ⭐ (주의)"
        },
        "en": {
            "title": "The Element: Pro", "sub": "Precise Day-Master Analysis", 
            "name": "Name", "btn": "Analyze Destiny", 
            "tab1": "Personality", "tab2": "2026 Forecast", 
            "print": "🖨️ Print Report",
            "t_mon": "Month", 
            "t_sco": "Luck Score (Max 5)", 
            "t_adv": "Detailed Advice",
            "legend": "※ Scale: ⭐⭐⭐⭐⭐ (Best) ~ ⭐ (Caution)"
        }
    }
    txt = ui[lang]

    st.markdown(f"<div class='main-header'>{txt['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{txt['sub']}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: name = st.text_input(txt['name'])
    with c2: b_date = st.date_input("Date of Birth", min_value=date(1900,1,1), value=date(1990,1,1))
    with c3: b_time = st.time_input("Time of Birth", value=None)

    # 상태 유지 로직
    if "analyzed" not in st.session_state:
        st.session_state["analyzed"] = False

    if st.button(txt['btn'], use_container_width=True):
        if name:
            st.session_state["analyzed"] = True
        else:
            st.warning("Please enter your name.")

    if st.session_state["analyzed"]:
        day_info = calculate_day_gan(b_date)
        element_type = day_info['element']
        trait, forecast = get_interpretation(element_type, lang)
        
        tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])
        
        with tab1:
            st.markdown(f"""
            <div class='card'>
                <h3 style='color: #64748b;'>👋 {name}</h3>
                <h1 style='color: #4f46e5; margin: 10px 0;'>{day_info[lang]}</h1>
                <hr>
                <div style='font-size: 1.1em; line-height: 1.8;'>{trait}</div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown(f"""
            <div class='card' style='border: 2px solid #ec4899; background-color: #fff1f2;'>
                <h2 style='color: #be185d;'>👑 {forecast['title']}</h2>
                <p style='font-size:1.1em;'>{forecast['gen']}</p>
                <ul style='margin-top:10px;'>
                    <li><b>💰 Wealth:</b> {forecast['money']}</li>
                    <li><b>❤️ Love:</b> {forecast['love']}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader(f"📅 2026 {txt['t_adv']}")
            st.caption(txt['legend'])
            
            raw_data = get_monthly_forecast_unique(element_type, lang)
            
            table_data = []
            for row in raw_data:
                table_data.append({
                    txt['t_mon']: row['Month'], 
                    txt['t_sco']: row['Luck'], 
                    txt['t_adv']: row['Advice']
                })
            
            # --- 숫자 인덱스 제거 로직 ---
            df = pd.DataFrame(table_data)
            # 1. Index를 '월' 컬럼으로 지정하여 0,1,2 숫자 제거
            df = df.set_index(txt['t_mon'])
            # 2. Table 출력
            st.table(df)

        st.write("---")
        if st.button(txt['print'], key="final_print"):
            components.html("<script>window.print();</script>", height=0, width=0)

if __name__ == "__main__":
    main()
