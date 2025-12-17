import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime, date

# 🔑 잠금 해제 비밀번호
UNLOCK_CODE = "2026RICH"

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Pro Report", page_icon="🔮", layout="wide")

# ----------------------------------------------------------------
# [인쇄 스타일 설정: 1페이지 꽉 채우기 (Page Break 방지)]
# ----------------------------------------------------------------
st.markdown("""
    <style>
        /* 1. 화면용 디자인 (평소대로) */
        .main-header {font-size: 2.5em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 10px;}
        .sub-header {font-size: 1.1em; color: #64748b; text-align: center; margin-bottom: 30px;}
        .card {background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 25px;}

        /* 2. 🖨️ 인쇄 모드 (공간 확보 최적화) */
        @media print {
            /* (1) 방해꾼 숨기기 */
            [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, .stDeployButton, button, .stButton, iframe {
                display: none !important;
            }
            
            /* (2) 종이 여백 최소화 (공간 넓히기) */
            @page {
                margin: 1.5cm; /* 종이 끝 여백 조정 */
            }
            html, body, .stApp {
                background: white !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                max-width: 100% !important;
            }

            /* (3) ★핵심★ 제목 사이즈 줄여서 공간 만들기 */
            .main-header {
                font-size: 1.8em !important; /* 제목 크기 줄임 */
                margin-bottom: 5px !important;
                margin-top: 0 !important;
            }
            .sub-header {
                display: none !important; /* 부제목은 인쇄할 때 숨겨서 공간 확보 */
            }
            
            /* (4) 입력창 주변 여백 삭제 */
            div[data-testid="stVerticalBlock"] > div {
                gap: 0.5rem !important; /* 요소 사이 간격 좁힘 */
            }

            /* (5) ★핵심★ 카드가 다음 장으로 도망가지 않게 설정 */
            .card {
                border: 1px solid #000 !important;
                box-shadow: none !important;
                margin-bottom: 10px !important; /* 카드 간격 좁힘 */
                padding: 15px !important; /* 카드 안쪽 여백 줄임 */
                
                /* 중요: 내용이 많아도 억지로 다음 장으로 넘기지 않음 */
                break-inside: auto !important; 
                page-break-inside: auto !important;
            }
            
            /* (6) 헤더와 내용 사이 거리 좁히기 */
            h1, h2, h3, h4 {
                margin-top: 0 !important;
                margin-bottom: 5px !important;
                padding-top: 10px !important;
            }
            
            /* (7) 글자색 검정 */
            * {
                color: black !important;
                -webkit-print-color-adjust: exact !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. 만세력 엔진 (일주 계산 - 한영 표현력 강화) ---
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1)
    delta = birth_date - base_date
    if delta.days < 0: return 0
    gan_index = delta.days % 10
    gans = [
        # 한국어: [이름(한자) - 상징] / 영어: [발음 (한자) - 상징]
        {"ko": "갑목(甲) - 곧게 뻗은 거목", "en": "Gap (甲) - The Giant Tree", "element": "Wood"},
        {"ko": "을목(乙) - 적응력 강한 화초", "en": "Eul (乙) - The Resilient Flower", "element": "Wood"},
        {"ko": "병화(丙) - 세상을 비추는 태양", "en": "Byeong (丙) - The Blazing Sun", "element": "Fire"},
        {"ko": "정화(丁) - 온기를 주는 촛불", "en": "Jeong (丁) - The Warm Candle", "element": "Fire"},
        {"ko": "무토(戊) - 묵직한 태산", "en": "Mu (戊) - The Great Mountain", "element": "Earth"},
        {"ko": "기토(己) - 생명을 품은 텃밭", "en": "Gi (己) - The Fertile Soil", "element": "Earth"},
        {"ko": "경금(庚) - 단단한 원석", "en": "Gyeong (庚) - The Iron Ore", "element": "Metal"},
        {"ko": "신금(辛) - 빛나는 보석", "en": "Sin (辛) - The Shining Jewelry", "element": "Metal"},
        {"ko": "임수(壬) - 포용하는 바다", "en": "Im (壬) - The Vast Ocean", "element": "Water"},
        {"ko": "계수(癸) - 스며드는 빗물", "en": "Gye (癸) - The Gentle Rain", "element": "Water"}
    ]
    return gans[gan_index]
 
    
# --- 3. 데이터베이스 (성격 & 운세 - 대폭 보강 버전) ---
def get_interpretation(element, lang):
    # 한국어 상세 데이터 (전문가 수준의 깊이 있는 해석)
    traits_ko = {
        "Wood": """#### 🌲 본성 (Nature): 뚫고 나가는 봄의 에너지
당신은 얼어붙은 땅을 뚫고 올라오는 새싹이나 거목처럼 **강력한 상승 욕구**와 **추진력**을 가졌습니다. '인자함(仁)'을 상징하여 마음이 따뜻하고 어린아이 같은 순수함이 있지만, 한번 목표를 정하면 앞만 보고 달리는 기질이 있습니다. 남의 간섭을 극도로 싫어하며, 자신이 주도권을 쥐어야 직성이 풀리는 대장부 스타일입니다.

#### 💰 재물운 (Wealth): 시간을 먹고 자라는 거목
당신에게 재물은 '나무를 키우는 것'과 같습니다. 요행이나 일확천금보다는, 자신의 능력과 노력으로 정직하게 재산을 불려 나가는 것이 맞습니다. 처음에는 성과가 더디게 보일지라도, 시간이 지날수록 뿌리가 깊어져 중년 이후에는 흔들리지 않는 **탄탄한 부**를 축적하게 됩니다. 부동산, 교육, 창작물 등 '시간이 지날수록 가치가 오르는 자산'에 투자하세요.

#### 💼 직업/적성 (Career): 기획과 교육의 리더
무언가를 새롭게 시작하고, 기획하고, 사람을 길러내는 일이 천직입니다.
* **추천 분야:** 교육, 건축/인테리어, 기획, 문학/예술, 패션, 스타트업 창업
* **직장 생활:** 반복적인 업무보다는 자신이 아이디어를 내고 프로젝트를 주도할 수 있는 곳에서 빛을 발합니다.

#### ❤️ 연애/관계 (Love): 내 사람은 내가 지킨다
연애할 때도 주도적입니다. 상대방을 이끌고 보호해주려는 '가장' 같은 책임감이 강합니다. 하지만 자신의 방식대로만 하려는 고집 때문에 상대방이 숨 막혀 할 수 있습니다. 가끔은 상대방의 의견을 묵묵히 들어주는 '큰 나무의 그늘' 같은 여유가 필요합니다.""",

        "Fire": """#### 🔥 본성 (Nature): 세상을 밝히는 화려한 열정
당신은 태양이나 촛불처럼 **자신을 태워 주변을 밝히는 에너지**를 가졌습니다. '예의(禮)'를 중시하여 매너가 좋고, 감정을 숨기지 못하는 솔직하고 투명한 성격 덕분에 어디서나 인기가 많습니다. 직관력이 뛰어나고 행동이 빠르지만, 그만큼 빨리 싫증을 내거나 욱하는 기질도 있어 '냄비 근성'을 조심해야 합니다.

#### 💰 재물운 (Wealth): 흐름이 빠른 화려한 돈
돈을 버는 능력도 탁월하고, 쓰는 씀씀이도 화끈합니다. 재물이 잘 들어오지만, 기분에 따라 겉치레나 유흥으로 나가는 돈도 많습니다. 당신에게 돈은 '흐르는 에너지'입니다. 현금으로 쥐고 있으면 다 써버리기 쉬우니, 문서나 저작권, 브랜드 가치 등 **'남들에게 보여지는 자산'**으로 묶어두는 것이 부자가 되는 지름길입니다.

#### 💼 직업/적성 (Career): 무대 체질, 말과 표현의 달인
자신을 드러내고 표현하는 곳에서 능력이 200% 발휘됩니다. 남들의 시선을 즐기는 편입니다.
* **추천 분야:** 방송/연예, 유튜브/SNS, 마케팅/영업, 정치, 디자인/미용, 강연
* **직장 생활:** 조용한 사무직은 병이 날 수 있습니다. 사람을 만나고 활동적인 부서, 혹은 화려한 조명을 받는 일이 딱입니다.

#### ❤️ 연애/관계 (Love): 첫눈에 반하는 뜨거운 사랑
'금사빠(금방 사랑에 빠지는)' 기질이 있습니다. 마음에 들면 앞뒤 재지 않고 직진하는 스타일입니다. 열정적인 사랑을 하지만, 식을 때도 차갑게 식을 수 있습니다. 복잡한 밀당보다는 화끈하고 솔직한 고백이 통하는 타입이며, 외모나 스타일이 좋은 상대에게 끌립니다.""",

        "Earth": """#### ⛰️ 본성 (Nature): 모든 것을 품어주는 신용의 땅
당신은 묵묵히 자리를 지키는 산이나 밭처럼 **믿음직스럽고 포용력**이 있습니다. '신용(信)'을 목숨처럼 여기기 때문에 주변 사람들의 비밀 상담사가 되어주는 경우가 많습니다. 중립을 잘 지키며, 어떤 쪽에도 치우치지 않습니다. 다만, 속마음을 잘 드러내지 않아 겉으로는 답답해 보이거나 융통성이 없어 보일 수 있습니다.

#### 💰 재물운 (Wealth): 알부자가 많은 부동산의 제왕
오행 중 재물과 가장 인연이 깊고 실속이 있습니다. 특히 **부동산, 땅, 건물**과 찰떡궁합입니다. 현금 유동성은 약할 수 있으나, 묵혀두면 오르는 자산을 보는 눈이 탁월합니다. 절약 정신이 투철하고 안전 지향적이라, 티끌 모아 태산을 만드는 전형적인 '알부자' 유형이 많습니다.

#### 💼 직업/적성 (Career): 중재자 그리고 관리자
사람과 사람, 일과 일 사이를 연결하고 조정하는 능력이 뛰어납니다.
* **추천 분야:** 부동산, 컨설팅, 종교/철학, 농업/조경, 인사/총무 관리, 토목
* **직장 생활:** 변화가 심하고 불안정한 곳보다는, 안정적이고 시스템이 갖춰진 조직에서 오래 일할수록 빛을 봅니다.

#### ❤️ 연애/관계 (Love): 은근하게 끓어오르는 뚝배기
표현이 서툴러 재미없는 사람으로 오해받을 수 있지만, 한번 마음을 주면 변치 않는 **해바라기**입니다. 화려한 이벤트보다는 진심 어린 배려와 신뢰를 중요시하며, 결혼 상대로서 최고의 점수를 받습니다. 당신의 묵직함을 알아주는 지혜로운 상대를 만나는 것이 좋습니다.""",

        "Metal": """#### ⚔️ 본성 (Nature): 맺고 끊음이 확실한 결단의 칼
당신은 원석이나 잘 제련된 칼처럼 **냉철한 이성**과 **강한 의리**를 가졌습니다. '의(義)'를 중시하여 옳고 그름(시비)을 가리는 것을 좋아하고, 한번 결정하면 뒤돌아보지 않는 무시무시한 결단력이 있습니다. 차가워 보이지만 내 사람에게는 확실하게 정을 주는 '츤데레' 매력이 있으며, 완벽주의 성향이 강합니다.

#### 💰 재물운 (Wealth): 확실한 결과와 성과 중심
일한 만큼, 노력한 만큼 확실한 보상이 주어져야 직성이 풀립니다. 불확실한 투자보다는, 자신의 기술이나 전문성을 통해 벌어들이는 **정재(고정 수입)**가 탄탄합니다. 승부욕이 강해 남들보다 더 높은 성과를 올려 인센티브를 챙기거나, 기술력을 인정받아 고수익을 올리는 능력이 있습니다.

#### 💼 직업/적성 (Career): 원칙과 권력의 조화
규칙이 분명하고 전문성이 필요한 분야, 혹은 남을 심판하거나 고치는 일이 어울립니다.
* **추천 분야:** 군인/경찰, 법조계, 금융/회계, 엔지니어, 의료/수술, 금속/기계
* **직장 생활:** 흐지부지한 것을 못 참습니다. 리더가 되면 카리스마 있게 조직을 장악하고 이끌어갑니다.

#### ❤️ 연애/관계 (Love): 확실한 내 편 만들기
썸 타는 기간이 길어지거나 애매한 관계를 싫어합니다. "사귀는 거야, 마는 거야?" 확실하게 관계 정립을 원합니다. 상대방에게도 의리와 도리를 요구하며, 한번 맺은 인연은 끝까지 책임지려는 멋진 연인입니다. 다만, 말로 상대방에게 상처를 줄 수 있으니 조금 부드럽게 표현하세요.""",

        "Water": """#### 🌊 본성 (Nature): 어디든 흐르는 유연한 지혜
당신은 흐르는 물처럼 **어떤 환경에도 적응하는 유연함**과 **깊은 지혜(智)**를 가졌습니다. 두뇌 회전이 빠르고 기획력이 뛰어나며, 겉으로는 부드러워 보이나 속은 냉철한 계산이 서 있습니다. 비밀이 많고 자신의 속마음을 완벽하게 보여주지 않아 신비로운 매력을 풍깁니다. 생각이 꼬리에 꼬리를 무는 타입이라 철학적입니다.

#### 💰 재물운 (Wealth): 흐름을 읽는 투자의 귀재
돈의 흐름을 본능적으로 읽어냅니다. 한곳에 고정된 자산보다는 주식, 코인, 환율, 무역 등 **유동적인 자산** 투자를 선호하며, 남들이 보지 못하는 틈새시장을 찾아내는 눈이 있습니다. 물이 모이는 곳이 곧 돈이 모이는 곳이니, 유통이나 해외 관련 비즈니스에서 큰돈을 만질 수 있습니다.

#### 💼 직업/적성 (Career): 보이지 않는 곳의 전략가
몸을 쓰는 일보다는 머리를 쓰고 전략을 짜는 일이 맞습니다.
* **추천 분야:** 무역/유통, 기획/마케팅, 연구원, 심리 상담, 예술/창작, 요식업/카페
* **직장 생활:** 9 to 6의 딱딱한 조직보다는 자유로운 분위기나 해외 출장이 잦은 곳, 혹은 밤에 일하는 직업과도 인연이 있습니다.

#### ❤️ 연애/관계 (Love): 알다가도 모를 치명적 매력
상대방의 기분을 잘 맞춰주는 배려심이 뛰어나지만, 정작 자신의 깊은 속은 다 보여주지 않습니다. 이런 알 수 없는 모호함이 상대방을 애타게 만드는 매력이 됩니다. 구속받는 것을 싫어하며, 육체적인 사랑과 정신적인 교감을 모두 중요하게 생각합니다."""
    }

    # 영어 상세 데이터 (English - Expert Version)
    traits_en = {
        "Wood": """#### 🌲 Nature: The Benevolent Pioneer
Like a tree stretching towards the sky, you possess a **strong drive** and ambition. You symbolize 'Spring' and 'Growth'. You are creative, benevolent, and a natural planner. However, you can be stubborn and dislike being controlled by others. You prefer to lead rather than follow.

#### 💰 Wealth: Steady Accumulation
You build wealth through honest effort and solid foundations rather than gambling. Like tree rings, your assets grow larger and deeper over time, leading to great prosperity in later years. Long-term investments in education or real estate suit you well.

#### 💼 Career: Planner & Educator
You excel in fields involving growth, teaching, or designing.
* **Best Fits:** Education, Architecture, Startups, Arts, Design.
* **Work Style:** You thrive in project-based environments where you can initiate new ideas.

#### ❤️ Love: Protective Leader
You lead relationships with responsibility. You act like a sheltering tree for your partner but need to be careful not to be too controlling. Try to listen more to your partner's opinions.""",

        "Fire": """#### 🔥 Nature: The Passionate Visionary
You shine like the sun, full of **energy, honesty, and politeness**. You are expressive and popular. You act on intuition and are very transparent; your emotions show clearly on your face. However, your passion can cool down as quickly as it heats up.

#### 💰 Wealth: High Flow & Visibility
You have great earning potential but also high expenses due to your generous nature. Managing your savings is crucial. Investing in your personal brand, intellectual property, or 'visible assets' is beneficial.

#### 💼 Career: Born for the Stage
You thrive where you can express yourself and receive attention.
* **Best Fits:** Media, Sales, Politics, Marketing, Entertainment, YouTube.
* **Work Style:** Avoid quiet, repetitive office jobs. You need dynamic environments.

#### ❤️ Love: Hot & Fast
You fall in love quickly and passionately. You prefer direct confessions and dislike playing mind games. You are attracted to stylish and expressive partners.""",

        "Earth": """#### ⛰️ Nature: The Guardian of Trust
You are steady like a mountain, valuing **trust and consistency** above all. You are a good listener and often act as a counselor for others. You keep your own feelings hidden, which may make you seem stubborn, but you are incredibly reliable.

#### 💰 Wealth: The Real Estate King
Among the five elements, you have the best luck with **real estate and land**. You are excellent at saving and protecting assets, often becoming wealthy quietly over time. You prefer safety over high risk.

#### 💼 Career: Mediator & Manager
You excel at connecting people, mediating conflicts, and managing stable systems.
* **Best Fits:** Real Estate, Consulting, HR, Agriculture, Religion.
* **Work Style:** You shine in stable, well-structured organizations.

#### ❤️ Love: The Steady Sunflower
You are not flashy, but your love is unchanging and loyal. You prefer sincere trust over exciting events. You are considered the best partner for a long-term marriage.""",

        "Metal": """#### ⚔️ Nature: The Decisive Warrior
You are like a sharp blade or a solid rock, valuing **justice, principles, and loyalty**. You are decisive and hate ambiguity. You may seem cold on the outside, but you are warm and loyal to your own people. You strive for perfection.

#### 💰 Wealth: Result-Oriented
You believe in clear rewards for performance. You build wealth through professional skills and competitive achievements rather than luck. You have a strong desire to win and earn high incentives.

#### 💼 Career: Power & Expertise
You suit fields requiring precision, principles, and authority.
* **Best Fits:** Finance, Law, Military, Engineering, Medicine, Technology.
* **Work Style:** You are a charismatic leader who hates inefficiency.

#### ❤️ Love: Clear Boundaries
You dislike ambiguous relationships. Once you commit, you are a loyal and responsible partner who values duty. You want a clear definition of the relationship.""",

        "Water": """#### 🌊 Nature: The Wise Strategist
Like flowing water, you are **adaptable, flexible, and wise**. You are a deep thinker with great planning skills. You are mysterious and keep your true thoughts secret. You have a philosophical side and a quick mind.

#### 💰 Wealth: Master of Flow
You instinctively understand the flow of money. You can succeed in trade, investments (stocks/crypto), and global business. You can find niche markets that others miss. Money flows to you like water.

#### 💼 Career: The Brain Player
You excel in intellectual and strategic fields rather than physical labor.
* **Best Fits:** Trade, Research, Psychology, Planning, Arts, Nightlife business.
* **Work Style:** You prefer freedom over strict 9-to-5 rules.

#### ❤️ Love: Mysterious Charm
You are caring and adaptable, but your mysterious side makes you attractive. You dislike being controlled or restricted. You value both mental connection and physical chemistry."""
    }

    # ----------------------------------------------------------------
    # 2026년 총평 (Expert Version: 구체적이고 깊이 있는 해석)
    # ----------------------------------------------------------------
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

# --- 4. 월별 정밀 운세 (최종 완성: 수동 별점 적용 & 기준 명시) ---
def get_monthly_forecast_unique(element, lang):
    
    # [별점 부여 기준 (Criteria)] 
    # 아래 기준에 맞춰서 모든 데이터를 수동으로 검수하여 입력했습니다.
    # ⭐⭐ (주의): 조심, 경고, 스트레스, 다툼, 손해
    # ⭐⭐⭐ (보통): 노력, 과정, 이동, 변동
    # ⭐⭐⭐⭐ (좋음): 이득, 성과, 해결, 인기, 상승
    # ⭐⭐⭐⭐⭐ (최고): 횡재, 대박, 귀인, 합격, 승진

    # 데이터 구조: (월, 한국어 조언, 영어 조언, ★별점)
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
    
    # 1. 입력받은 오행(element)에 해당하는 12개월 데이터를 가져옵니다.
    months = data[element]
    result = []
    
    # 2. 반복문을 돌면서 언어에 맞게 변환하고 리스트에 담습니다.
    # ★ 여기서 4개의 값(월, 한글, 영어, 별점)을 정확히 꺼냅니다.
    for mon_ko, text_ko, text_en, star_rating in months:
        msg = text_ko if lang == "ko" else text_en
        
        # 월 표시 (영어 변환)
        month_label = mon_ko
        if lang != "ko":
            month_map = {"1월":"Jan", "2월":"Feb", "3월":"Mar", "4월":"Apr", "5월":"May", "6월":"Jun", "7월":"Jul", "8월":"Aug", "9월":"Sep", "10월":"Oct", "11월":"Nov", "12월":"Dec"}
            month_label = month_map.get(mon_ko, mon_ko)
            
        result.append({"Month": month_label, "Luck": star_rating, "Advice": msg})
    
    # 3. 최종 결과 반환 (여기서 함수가 끝납니다!)
    return result
# --- 5. 메인 실행 (수정판: 체크박스 삭제 & 진짜 인쇄 버튼) ---
def main():
    # 세션 상태 초기화
    if "saved_name" not in st.session_state: st.session_state["saved_name"] = ""
    if "saved_date" not in st.session_state: st.session_state["saved_date"] = date(1990, 1, 1)

    with st.sidebar:
        st.title("Settings")
        lang_opt = st.radio("Language", ["English", "한국어"])
        lang = "ko" if "한국어" in lang_opt else "en"
        
        # [커피 후원]
        coffee_head = "☕ 개발자 응원하기" if lang == "ko" else "☕ Support"
        coffee_msg = "운명의 코드를 응원해 주세요!" if lang == "ko" else "Fuel the code!"
        
        st.sidebar.markdown("---")
        st.sidebar.header(coffee_head)
        st.sidebar.markdown(f'<a href="https://buymeacoffee.com/5codes" target="_blank" style="text-decoration:none;color:#4f46e5;font-weight:bold;">{coffee_msg}</a>', unsafe_allow_html=True)

    ui = {
        "ko": {
            "title": "디 엘리먼트: 사주 프로", "sub": "당신의 운명 지도와 2026년 정밀 분석", 
            "name": "이름", "btn": "운명 분석하기", 
            "h_trait": "🔮 타고난 기질", "h_fore": "📅 2026년 정밀 운세 ($5)",
            "locked_msg": "🔒 유료 콘텐츠입니다.", "locked_desc": "결제 후 코드를 입력하세요.",
            "code_label": "잠금 해제 코드", "unlock_btn": "해제 (Unlock)", "err": "코드가 틀렸습니다.",
            "print_btn": "🖨️ 결과 인쇄하기 (Print Result)"
        },
        "en": {
            "title": "The Element: Pro", "sub": "Precise Day-Master Analysis", 
            "name": "Name", "btn": "Analyze Destiny", 
            "h_trait": "🔮 Personality", "h_fore": "📅 2026 Forecast ($5)",
            "locked_msg": "🔒 Premium Content", "locked_desc": "Enter code after payment.",
            "code_label": "Enter Code", "unlock_btn": "Unlock", "err": "Invalid Code.",
            "print_btn": "🖨️ Print Result"
        }
    }
    txt = ui[lang]

    # 입력창 (항상 표시)
    st.markdown(f"<div class='main-header'>{txt['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{txt['sub']}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1: 
        name = st.text_input(txt['name'], value=st.session_state["saved_name"])
        st.session_state["saved_name"] = name
    with c2: 
        b_date = st.date_input("Date", min_value=date(1900,1,1), value=st.session_state["saved_date"])
        st.session_state["saved_date"] = b_date

    if st.button(txt['btn'], type="primary", use_container_width=True):
        if name: st.session_state["analyzed"] = True
        else: st.warning("Name required.")

    # 결과 화면 (탭 없이 쭉 보여줍니다 -> 그래야 인쇄가 잘 됩니다!)
    if st.session_state.get("analyzed"):
        st.divider()
        # 선생님의 데이터베이스 함수 사용
        day_info = calculate_day_gan(b_date)
        e_type = day_info['element']
        trait, forecast = get_interpretation(e_type, lang)

        # 1. 성격 분석 카드
        st.subheader(f"{txt['h_trait']}")
        st.markdown(f"""
        <div class='card'>
            <h3 style='color:#64748b'>👋 {name}</h3>
            <h1 style='color:#4f46e5'>{day_info[lang]}</h1>
            <div style='margin-top:10px;'>{trait}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 2026 운세 (잠금 기능)
        st.subheader(f"{txt['h_fore']}")
        if "is_unlocked" not in st.session_state: st.session_state["is_unlocked"] = False
        
        if not st.session_state["is_unlocked"]:
            st.warning(f"{txt['locked_msg']} / {txt['locked_desc']}")
            c_code, c_btn = st.columns([3, 1])
            with c_code: user_code = st.text_input(txt['code_label'], type="password", label_visibility="collapsed")
            with c_btn: 
                if st.button(txt['unlock_btn']):
                    if user_code == UNLOCK_CODE:
                        st.session_state["is_unlocked"] = True
                        st.rerun()
                    else:
                        st.error(txt['err'])
        else:
            # 잠금 해제 내용
            st.success("🔓 Unlocked!")
            st.markdown(f"""
            <div class='card' style='border:1px solid #ec4899'>
                <h2 style='color:#be185d'>👑 {forecast['title']}</h2>
                <p>{forecast['gen']}</p>
                <p><b>💰 Money:</b> {forecast['money']} / <b>❤️ Love:</b> {forecast['love']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 월별 표
            monthly_data = get_monthly_forecast_unique(e_type, lang)
            df = pd.DataFrame(monthly_data)
            df = df.set_index(list(df.columns)[0]) # 첫번째 컬럼(월)을 인덱스로
            st.table(df)

            # --------------------------------------------------------
            # ★ 진짜 인쇄 버튼 (여기가 핵심!)
            # --------------------------------------------------------
            st.divider()
            
            # 이 코드가 있어야 버튼을 눌렀을 때 '전체 화면'이 인쇄됩니다.
            # window.parent.print() <-- 이게 해결책입니다.
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
                        {txt['print_btn']}
                    </button>
                </div>
                """,
                height=100
            )

if __name__ == "__main__":
    main()
