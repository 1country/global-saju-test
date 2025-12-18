import requests
import streamlit as st
from datetime import date

# 1. 만세력 엔진 (일주 계산기 - 영문 수정 완료)
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1)
    delta = birth_date - base_date
    if delta.days < 0: return 0
    gan_index = delta.days % 10
    
    # gans 리스트 (한글/영어 완벽 대응)
    gans = [
        {"ko": "갑목(甲)", "desc": "곧게 뻗은 거목", "desc_en": "Straight and tall tree", "element": "Wood", "en": "Wood"},
        {"ko": "을목(乙)", "desc": "적응력 강한 화초", "desc_en": "Adaptable and resilient flower", "element": "Wood", "en": "Wood"},
        {"ko": "병화(丙)", "desc": "태양 같은 열정", "desc_en": "Passion like the blazing sun", "element": "Fire", "en": "Fire"},
        {"ko": "정화(丁)", "desc": "촛불 같은 온기", "desc_en": "Warmth of a gentle candle", "element": "Fire", "en": "Fire"},
        {"ko": "무토(戊)", "desc": "묵직한 태산", "desc_en": "Heavy and majestic mountain", "element": "Earth", "en": "Earth"},
        {"ko": "기토(己)", "desc": "생명을 품은 텃밭", "desc_en": "Fertile soil embracing life", "element": "Earth", "en": "Earth"},
        {"ko": "경금(庚)", "desc": "단단한 원석", "desc_en": "Solid and unrefined iron ore", "element": "Metal", "en": "Metal"},
        {"ko": "신금(辛)", "desc": "빛나는 보석", "desc_en": "Shining and precious gemstone", "element": "Metal", "en": "Metal"},
        {"ko": "임수(壬)", "desc": "포용하는 바다", "desc_en": "Vast and embracing ocean", "element": "Water", "en": "Water"},
        {"ko": "계수(癸)", "desc": "스며드는 빗물", "desc_en": "Gentle and permeating rain", "element": "Water", "en": "Water"}
    ]
    return gans[gan_index]

# 2. 라이센스 검증기 (마스터키 지원)
def verify_license_flexible(key, current_product_id, all_access_id="all_access_pass"):
    if key == "test": return True, "테스트 통과 (개발자 모드)"
    
    if _check_gumroad(key, current_product_id):
        return True, "✅ 정품 인증 완료! (개별 구매)"
        
    if _check_gumroad(key, all_access_id):
        return True, "👑 프리패스 회원님 환영합니다! (전체 이용 가능)"
        
    return False, "🚫 유효하지 않은 키입니다."

# (내부용) 실제 검로드 통신 함수
def _check_gumroad(key, permalink):
    try:
        response = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={"product_permalink": permalink, "license_key": key, "increment_uses_count": "true"}
        )
        data = response.json()
        if data.get("success") and not data["license_key"]["refunded"] and not data["license_key"]["chargebacked"]:
            return True
        return False
    except:
        return False

# 3. [NEW] 상세 본질 분석 데이터 (선생님이 주신 내용 추가)
def get_interpretation(element, lang):
    # 한국어 상세 데이터
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

    # 영어 상세 데이터
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

    # [핵심] 언어에 따라 해당 데이터를 반환하는 로직 (이게 없으면 작동 안 함)
    if lang == "ko":
        return traits_ko[element]
    else:
        return traits_en[element]
