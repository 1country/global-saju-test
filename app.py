import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Pro Report", page_icon="🖨️", layout="wide")

# 스타일 (CSS) - 인쇄 및 디자인 설정
st.markdown("""
<style>
    .main-header {font-size: 2.2em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 10px;}
    .sub-header {font-size: 1.0em; color: #64748b; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 20px;}
    .highlight {color: #2563eb; font-weight: bold;}
    
    /* 인쇄 버튼 스타일 (링크 형태) */
    .print-btn {
        display: block; background-color: #4f46e5; color: white !important; 
        text-align: center; text-decoration: none !important; padding: 12px 20px; 
        border-radius: 8px; font-size: 1.1em; font-weight: bold; margin-top: 20px; 
        width: 100%; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer;
    }
    .print-btn:hover {background-color: #4338ca;}

    /* 🖨️ 인쇄 모드 설정 (강제 잉크 절약 및 레이아웃) */
    @media print {
        body * { visibility: hidden; }
        .card, .card * { visibility: visible; }
        .card {
            position: absolute; left: 0; top: 0; width: 100%;
            margin: 0; padding: 20px;
            background-color: white !important; color: black !important;
            border: 2px solid #333 !important; box-shadow: none !important;
        }
        [data-testid="stSidebar"], [data-testid="stHeader"], .print-btn, footer { display: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 만세력 엔진 (일주 계산) ---
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1) # 기준일
    delta = birth_date - base_date
    days_passed = delta.days
    if days_passed < 0: return 0 
    
    gan_index = days_passed % 10
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

    # 2026년 운세 총평
    forecast_ko = {}
    forecast_en = {}
    
    if element == "Wood":
        forecast_ko = {"title": "🔥 재능 폭발의 해 (식상운)", "gen": "나를 태워 세상을 밝히는 형국입니다. 당신의 재능이 꽃을 피우고, 바쁘게 움직일수록 성과가 따릅니다. 다만, 너무 많은 일을 벌이면 건강을 해칠 수 있으니 선택과 집중이 필요합니다.", "money": "수입이 늘어나지만 그만큼 품위 유지비나 투자로 인한 지출도 늘어납니다.", "love": "표현력이 좋아져 인기가 많아집니다. 연애하기 최적의 시기입니다."}
        forecast_en = {"title": "🔥 A Year of Explosive Talent (Output)", "gen": "You will burn bright like a fire. Your talents will bloom, and being busy will lead to success. However, taking on too much can hurt your health, so focus is key.", "money": "Income increases, but expenses for investments or lifestyle will also rise.", "love": "Your expressiveness improves, boosting your popularity. Great time for romance."}
    elif element == "Fire":
        forecast_ko = {"title": "🤝 경쟁과 협력의 해 (비겁운)", "gen": "불이 불을 만난 격이라 에너지가 넘칩니다. 자존심이 강해지고 경쟁자가 나타나지만, 혼자보다는 동료와 협력할 때 더 큰 성과를 냅니다. 독립하고 싶은 욕구가 강해집니다.", "money": "공동 투자는 신중해야 합니다. 친구나 형제간의 돈 거래는 피하세요.", "love": "친구가 연인으로 발전할 수 있습니다. 경쟁자가 생길 수도 있습니다."}
        forecast_en = {"title": "🤝 Year of Competition & Cooperation", "gen": "Fire meets Fire, creating immense energy. Your pride grows, and rivals appear. You will achieve more by cooperating rather than working alone. Desire for independence grows.", "money": "Be careful with joint investments. Avoid lending money to friends.", "love": "Friends may turn into lovers. Be aware of potential romantic rivals."}
    elif element == "Earth":
        forecast_ko = {"title": "📜 문서와 귀인의 해 (인성운)", "gen": "불이 흙을 단단하게 구워줍니다. 윗사람의 도움을 받고, 학업이나 계약에서 좋은 성과를 냅니다. 부동산 취득이나 자격증 시험에 아주 유리한 시기입니다.", "money": "현금보다는 문서(부동산, 주식, 계약권)로 재산을 늘리는 것이 유리합니다.", "love": "사랑받는 시기입니다. 나를 챙겨주는 듬직한 사람을 만납니다."}
        forecast_en = {"title": "📜 Year of Documents & Mentors (Resource)", "gen": "Fire strengthens the Earth. You will receive help from superiors and succeed in studies or contracts. Excellent time for real estate or certifications.", "money": "Better to grow wealth through assets (documents/real estate) than cash.", "love": "You will be loved. You might meet someone reliable who takes care of you."}
    elif element == "Metal":
        forecast_ko = {"title": "🔨 명예와 승진의 해 (관성운)", "gen": "불이 쇠를 녹여 도구를 만듭니다. 직장에서 책임감이 커지고 압박이 있지만, 이를 견디면 확실한 승진과 명예가 따릅니다. 조직에서 자리를 잡는 중요한 해입니다.", "money": "고정 수입이 늘어나거나 직급 상승에 따른 인센티브가 있습니다.", "love": "여자는 남자가 들어오는 운이며, 남자는 자녀와 관련된 기쁜 일이 있습니다."}
        forecast_en = {"title": "🔨 Year of Honor & Promotion (Power)", "gen": "Fire shapes Metal. Responsibility and pressure at work will increase, but enduring it brings promotion and honor. A crucial year for your career.", "money": "Fixed income increases, or bonuses come from higher status.", "love": "Women may meet a partner; Men may have good news regarding children."}
    elif element == "Water":
        forecast_ko = {"title": "💰 재물 쟁취의 해 (재성운)", "gen": "물이 불을 끄려 합니다. 불은 당신에게 '재물'입니다. 큰 돈을 벌 기회가 오지만, 그만큼 치열하게 싸워야 쟁취할 수 있습니다. 결과가 확실하게 나오는 해입니다.", "money": "사업 확장이나 투자를 통해 큰 수익을 기대할 수 있습니다. 과욕은 금물.", "love": "남자는 매력적인 이성을 만나게 됩니다. 즐거운 일이 많아집니다."}
        forecast_en = {"title": "💰 Year of Wealth Conquest (Wealth)", "gen": "Water controls Fire. Fire represents money to you. Huge financial opportunities arise, but you must fight to claim them. Results will be clear.", "money": "Expect gains from business expansion or investments. Don't be too greedy.", "love": "Men will meet attractive partners. A year full of joy."}

    if lang == "ko": return traits_ko[element], forecast_ko
    else: return traits_en[element], forecast_en

# --- 4. 월별 운세 로직 (상세 & 영어 포함) ---
def get_monthly_forecast(element, month, lang):
    season = ""
    if month in [2, 3]: season = "Wood"   
    elif month in [5, 6]: season = "Fire" 
    elif month in [8, 9]: season = "Metal"
    elif month in [11, 12, 1]: season = "Water" 
    else: season = "Earth" 

    msg = ""
    score = ""
    
    # 한국어/영어 멘트 설정
    # 1. 나무(Wood)
    if element == "Wood":
        if season == "Wood": 
            score = "⭐⭐"
            msg = "경쟁자가 나타나 내 성과를 나누자고 합니다. 동업 제안은 신중히 하고 실속을 챙기세요." if lang == "ko" else "Competitors appear. Be careful with partnerships and focus on your own benefits."
        elif season == "Fire": 
            score = "⭐⭐⭐⭐⭐"
            msg = "당신의 재능이 꽃을 피웁니다. 바쁘게 움직일수록 돈과 명예가 따릅니다. 활동 최적기!" if lang == "ko" else "Your talents bloom. The busier you are, the more success you gain. Best time to act!"
        elif season == "Earth": 
            score = "⭐⭐⭐⭐"
            msg = "뜻밖의 꽁돈이나 보너스 운이 있습니다. 재물운이 아주 좋습니다." if lang == "ko" else "Unexpected bonus or windfall. Financial luck is very good."
        elif season == "Metal": 
            score = "⭐⭐"
            msg = "직장 스트레스를 조심하세요. 책임질 일이 많아지니 건강 관리가 필수입니다." if lang == "ko" else "Beware of work stress. Responsibilities increase, so health care is essential."
        elif season == "Water": 
            score = "⭐⭐⭐⭐"
            msg = "계약운이 좋습니다. 윗사람이나 귀인의 도움으로 문제가 해결됩니다." if lang == "ko" else "Good contract luck. Problems are solved with help from mentors."

    # 2. 불(Fire)
    elif element == "Fire":
        if season == "Wood": 
            score = "⭐⭐⭐⭐⭐"
            msg = "귀인의 도움을 받습니다. 자격증 시험이나 승진에 아주 유리한 시기입니다." if lang == "ko" else "Help from mentors. Excellent time for exams or promotions."
        elif season == "Fire": 
            score = "⭐⭐"
            msg = "자신감이 과해 다툼이 생길 수 있습니다. 주변과 충돌하지 않도록 겸손하세요." if lang == "ko" else "Overconfidence may lead to conflicts. Stay humble to avoid clashes."
        elif season == "Earth": 
            score = "⭐⭐⭐⭐"
            msg = "당신의 말과 아이디어로 돈을 법니다. 능력을 인정받아 성과를 냅니다." if lang == "ko" else "You make money with your ideas. Your abilities are recognized."
        elif season == "Metal": 
            score = "⭐⭐⭐⭐⭐"
            msg = "재물운이 폭발합니다! 투자 수익이나 큰 돈이 들어올 기회입니다." if lang == "ko" else "Explosive financial luck! Great chance for investment gains."
        elif season == "Water": 
            score = "⭐"
            msg = "과로를 주의하세요. 직장에서 압박감을 느낄 수 있으니 휴식이 필요합니다." if lang == "ko" else "Beware of overwork. You may feel pressure at work; rest is needed."

    # 3. 흙(Earth)
    elif element == "Earth":
        if season == "Wood": 
            score = "⭐⭐⭐⭐"
            msg = "명예운이 상승합니다. 승진하거나 더 좋은 조건의 이직 제안이 옵니다." if lang == "ko" else "Honor rises. Promotion or a better job offer is coming."
        elif season == "Fire": 
            score = "⭐⭐⭐⭐⭐"
            msg = "문서운이 최고입니다. 부동산 계약이나 중요 서류를 처리하기에 적기입니다." if lang == "ko" else "Best luck for documents. Great time for real estate or contracts."
        elif season == "Earth": 
            score = "⭐⭐"
            msg = "사람들과 어울리느라 지출이 큽니다. 고집을 부리면 손해를 봅니다." if lang == "ko" else "High expenses from socializing. Stubbornness leads to loss."
        elif season == "Metal": 
            score = "⭐⭐⭐"
            msg = "창작 활동에 좋습니다. 새로운 일을 벌이거나 표현하기 좋은 때입니다." if lang == "ko" else "Good for creativity. A good time to start something new."
        elif season == "Water": 
            score = "⭐⭐⭐"
            msg = "큰 돈이 눈앞에 보이지만 욕심내면 탈이 납니다. 신중하게 접근하세요." if lang == "ko" else "Big money is visible, but greed brings trouble. Be cautious."

    # 4. 쇠(Metal)
    elif element == "Metal":
        if season == "Wood": 
            score = "⭐⭐⭐⭐⭐"
            msg = "노력한 만큼 확실한 보상을 받습니다. 성과급이나 수익을 기대하세요." if lang == "ko" else "Sure rewards for your efforts. Expect bonuses or profits."
        elif season == "Fire": 
            score = "⭐"
            msg = "관재구설(시비)을 조심하세요. 나서지 말고 묵묵히 일하면 전화위복됩니다." if lang == "ko" else "Beware of disputes. Work quietly to turn things around."
        elif season == "Earth": 
            score = "⭐⭐⭐⭐"
            msg = "부동산이나 계약 관련 좋은 소식이 있습니다. 부모님의 덕을 볼 수 있습니다." if lang == "ko" else "Good news regarding real estate or contracts. Help from parents."
        elif season == "Metal": 
            score = "⭐⭐"
            msg = "고집이 세져서 주변과 충돌할 수 있습니다. 유연한 태도가 필요합니다." if lang == "ko" else "Stubbornness may cause conflicts. Be flexible."
        elif season == "Water": 
            score = "⭐⭐⭐⭐"
            msg = "재능을 발휘하여 문제를 해결합니다. 인기가 많아지고 찾는 사람이 늘어납니다." if lang == "ko" else "Solve problems with your talent. Your popularity rises."

    # 5. 물(Water)
    elif element == "Water":
        if season == "Wood": 
            score = "⭐⭐⭐⭐"
            msg = "새로운 프로젝트를 시작하기 좋습니다. 자녀에게 좋은 일이 생깁니다." if lang == "ko" else "Great to start new projects. Good news for your children."
        elif season == "Fire": 
            score = "⭐⭐⭐"
            msg = "일확천금의 기회가 오지만 위험도 따릅니다. 신중하게 투자하면 대박입니다." if lang == "ko" else "High risk, high return. Careful investment brings big wins."
        elif season == "Earth": 
            score = "⭐⭐⭐"
            msg = "승진하거나 감투를 씁니다. 어깨가 무거워지지만 명예로운 시기입니다." if lang == "ko" else "Promotion or new title. Heavy responsibility but honorable."
        elif season == "Metal": 
            score = "⭐⭐⭐⭐⭐"
            msg = "공부하기 딱 좋은 시기입니다. 나를 돕는 귀인이 나타납니다." if lang == "ko" else "Perfect time for study. A helpful mentor appears."
        elif season == "Water": 
            score = "⭐⭐"
            msg = "경쟁자가 내 돈을 노립니다. 돈 거래는 절대 금물입니다." if lang == "ko" else "Rivals eye your money. Do not lend money."

    return msg, score

# --- 5. 메인 실행 ---
def main():
    with st.sidebar:
        st.title("Settings")
        lang_opt = st.radio("Language", ["Korean (한국어)", "English (미국)"])
        lang = "ko" if "Korean" in lang_opt else "en"
        st.info("💡 **Print Tip:** Press the 'Print Report' button to save as PDF.")

    ui = {
        "ko": {
            "title": "디 엘리먼트: 사주 프로", "sub": "당신의 운명 지도와 2026년 정밀 분석", 
            "name": "이름", "btn": "운명 분석하기", 
            "tab1": "🔮 타고난 기질", "tab2": "📅 2026년 정밀 운세", 
            "print": "🖨️ 리포트 인쇄하기",
            "t_mon": "월 (Month)", "t_sco": "운세 점수", "t_adv": "상세 조언"
        },
        "en": {
            "title": "The Element: Pro", "sub": "Precise Day-Master Analysis", 
            "name": "Name", "btn": "Analyze Destiny", 
            "tab1": "Personality", "tab2": "2026 Forecast", 
            "print": "🖨️ Print Report",
            "t_mon": "Month", "t_sco": "Luck Score", "t_adv": "Detailed Advice"
        }
    }
    txt = ui[lang]

    st.markdown(f"<div class='main-header'>{txt['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{txt['sub']}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: name = st.text_input(txt['name'])
    with c2: b_date = st.date_input("Date of Birth", min_value=date(1900,1,1), value=date(1990,1,1))
    with c3: b_time = st.time_input("Time of Birth", value=None)

    if st.button(txt['btn'], use_container_width=True):
        if name:
            day_info = calculate_day_gan(b_date)
            element_type = day_info['element']
            trait, forecast = get_interpretation(element_type, lang)
            
            # --- 결과 화면 ---
            tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])
            
            with tab1: # 성격
                st.markdown(f"""
                <div class='card'>
                    <h3 style='color: #64748b;'>👋 {name}</h3>
                    <h1 style='color: #4f46e5; margin: 10px 0;'>{day_info[lang]}</h1>
                    <hr>
                    <div style='font-size: 1.1em; line-height: 1.8;'>{trait}</div>
                </div>
                """, unsafe_allow_html=True)
                # 인쇄 버튼 (링크 태그)
                st.markdown(f'<a href="#" onclick="window.print(); return false;" class="print-btn">{txt["print"]}</a>', unsafe_allow_html=True)

            with tab2: # 운세
                # 1. 2026년 총평 박스
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
                
                # 2. 월별 운세 테이블 (언어 적용)
                st.subheader(f"📅 2026 {txt['t_adv']}")
                monthly_data = []
                month_seq = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
                month_names_ko = ["2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월", "내년 1월"]
                month_names_en = ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"]
                
                month_names = month_names_ko if lang == "ko" else month_names_en

                for idx, m_num in enumerate(month_seq):
                    # 이제 lang 변수를 전달하여 영어 멘트도 가져옵니다.
                    msg, score = get_monthly_forecast(element_type, m_num, lang)
                    monthly_data.append({
                        txt['t_mon']: month_names[idx], 
                        txt['t_sco']: score, 
                        txt['t_adv']: msg
                    })
                
                st.table(pd.DataFrame(monthly_data))
                
                # 인쇄 버튼
                st.markdown(f'<a href="#" onclick="window.print(); return false;" class="print-btn">{txt["print"]}</a>', unsafe_allow_html=True)

        else:
            st.warning("Please enter your name.")

if __name__ == "__main__":
    main()
