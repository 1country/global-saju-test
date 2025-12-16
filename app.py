import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Pro", page_icon="🌌", layout="wide")

# 스타일 (CSS) - 인쇄(Print) 설정 추가
st.markdown("""
<style>
    /* 화면 디자인 */
    .main-header {font-size: 2.2em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 10px;}
    .sub-header {font-size: 1.0em; color: #64748b; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 20px;}
    .highlight {color: #2563eb; font-weight: bold;}
    
    /* 인쇄 버튼 스타일 */
    .print-btn {
        background-color: #4f46e5; color: white; border: none; padding: 10px 20px; 
        border-radius: 5px; cursor: pointer; font-size: 1em; margin-top: 10px; width: 100%;
    }
    .print-btn:hover {background-color: #4338ca;}

    /* 🖨️ 인쇄 모드 (종이에 출력될 때만 적용되는 규칙) */
    @media print {
        /* 사이드바, 입력창, 버튼, 탭 메뉴 숨기기 */
        [data-testid="stSidebar"], 
        [data-testid="stHeader"], 
        .stTextInput, .stDateInput, .stTimeInput, .stButton, 
        .stTabs [data-baseweb="tab-list"],
        footer {
            display: none !important;
        }
        /* 배경색 강제 출력 */
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        /* 리포트 카드 디자인 유지 */
        .card {
            border: 1px solid #ccc !important;
            box-shadow: none !important;
            break-inside: avoid; /* 페이지 넘어갈 때 박스 잘림 방지 */
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 만세력 엔진 (일주 계산) ---
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1) # 갑술일
    delta = birth_date - base_date
    days_passed = delta.days
    
    if days_passed < 0: return 0 
    
    gan_index = days_passed % 10
    
    gans = [
        {"ko": "갑목(甲)", "en": "Yang Wood (Gap)", "element": "Wood", "pol": "+"},
        {"ko": "을목(乙)", "en": "Yin Wood (Eul)", "element": "Wood", "pol": "-"},
        {"ko": "병화(丙)", "en": "Yang Fire (Byeong)", "element": "Fire", "pol": "+"},
        {"ko": "정화(丁)", "en": "Yin Fire (Jeong)", "element": "Fire", "pol": "-"},
        {"ko": "무토(戊)", "en": "Yang Earth (Mu)", "element": "Earth", "pol": "+"},
        {"ko": "기토(己)", "en": "Yin Earth (Gi)", "element": "Earth", "pol": "-"},
        {"ko": "경금(庚)", "en": "Yang Metal (Gyeong)", "element": "Metal", "pol": "+"},
        {"ko": "신금(辛)", "en": "Yin Metal (Sin)", "element": "Metal", "pol": "-"},
        {"ko": "임수(壬)", "en": "Yang Water (Im)", "element": "Water", "pol": "+"},
        {"ko": "계수(癸)", "en": "Yin Water (Gye)", "element": "Water", "pol": "-"}
    ]
    return gans[gan_index]

# --- 3. 데이터베이스 (성격 및 운세) ---
def get_interpretation(element, lang):
    # 1. 한국어 성격 데이터 (4단 상세 분석)
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
    # 2. 영어 성격 데이터 (4단 상세 분석)
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
    # 2026년(병오년-불) 총평
    forecast_ko = {}
    if element == "Wood":
        forecast_ko = {"title": "🔥 재능 폭발의 해", "gen": "일이 쏟아지고 능력을 인정받습니다. 너무 바빠서 건강을 챙겨야 합니다.", "money": "수입도 늘고 지출도 늡니다.", "love": "연애운 최상입니다."}
    elif element == "Fire":
        forecast_ko = {"title": "🤝 경쟁과 협력의 해", "gen": "자존심이 강해지고 경쟁자가 나타납니다. 혼자보다는 함께할 때 성공합니다.", "money": "돈 거래는 피하세요.", "love": "친구가 연인이 됩니다."}
    elif element == "Earth":
        forecast_ko = {"title": "📜 문서와 귀인의 해", "gen": "윗사람의 도움을 받고 계약운이 좋습니다. 공부하거나 자격증 따기 좋습니다.", "money": "부동산/문서 이득.", "love": "사랑받는 시기입니다."}
    elif element == "Metal":
        forecast_ko = {"title": "🔨 명예와 승진의 해", "gen": "책임감이 커지고 압박이 있지만, 견디면 승진합니다. 직장운이 좋습니다.", "money": "고정 수입 상승.", "love": "남자는 자식운, 여자는 남편운."}
    elif element == "Water":
        forecast_ko = {"title": "💰 재물 쟁취의 해", "gen": "큰 돈을 벌 기회가 오지만 치열하게 싸워야 합니다. 결과가 확실합니다.", "money": "투자 수익 기대.", "love": "남자는 여자운 상승."}

    # 영어 임시
    forecast_en = {"title": "2026 Forecast", "gen": "Year of Fire Horse", "money": "Financial change", "love": "Romance luck"}

    if lang == "ko": return traits_ko[element], forecast_ko
    else: return traits_en[element], forecast_en

# --- 4. [핵심] 월별 정밀 운세 로직 ---
def get_monthly_forecast(element, month):
    # 2026년(병오년)의 월별 흐름 (절기력 기준)
    # 봄(2,3월:나무) / 여름(5,6월:불) / 가을(8,9월:쇠) / 겨울(11,12,1월:물) / 환절기(4,7,10월:흙)
    
    season = ""
    if month in [2, 3]: season = "Wood"   
    elif month in [5, 6]: season = "Fire" 
    elif month in [8, 9]: season = "Metal"
    elif month in [11, 12, 1]: season = "Water" 
    else: season = "Earth" 

    msg = ""
    score = ""

    # 1. 나무(Wood) 일간인 경우
    if element == "Wood":
        if season == "Wood": msg, score = "경쟁자가 나타나 내 밥그릇을 노립니다. 동업 제안은 거절하고 내 실속을 챙겨야 합니다.", "⭐⭐"
        elif season == "Fire": msg, score = "당신의 재능이 꽃을 피우는 시기입니다. 바쁘게 움직일수록 돈이 됩니다. 활동하기 최적기!", "⭐⭐⭐⭐⭐"
        elif season == "Earth": msg, score = "뜻밖의 꽁돈이 생기거나 보너스를 받습니다. 재물운이 아주 좋습니다.", "⭐⭐⭐⭐"
        elif season == "Metal": msg, score = "직장에서 스트레스를 받거나 책임질 일이 많아집니다. 건강 관리에 유의하세요.", "⭐⭐"
        elif season == "Water": msg, score = "계약서에 도장 찍을 일이 생깁니다. 윗사람의 도움으로 문제가 해결됩니다.", "⭐⭐⭐⭐"

    # 2. 불(Fire) 일간인 경우
    elif element == "Fire":
        if season == "Wood": msg, score = "귀인의 도움을 받습니다. 자격증 시험이나 승진 시험에 아주 좋은 달입니다.", "⭐⭐⭐⭐⭐"
        elif season == "Fire": msg, score = "자신감이 지나쳐 독단적인 행동을 할 수 있습니다. 친구나 동료와 다툼을 주의하세요.", "⭐⭐"
        elif season == "Earth": msg, score = "말과 아이디어로 돈을 법니다. 당신의 능력을 사람들이 인정해줍니다.", "⭐⭐⭐⭐"
        elif season == "Metal": msg, score = "재물운이 폭발합니다. 투자 수익이나 큰 돈이 들어올 기회가 있습니다.", "⭐⭐⭐⭐⭐"
        elif season == "Water": msg, score = "직장에서 압박을 받거나 과로할 수 있습니다. 무리하지 말고 휴식하세요.", "⭐"

    # 3. 흙(Earth) 일간인 경우
    elif element == "Earth":
        if season == "Wood": msg, score = "명예운이 상승하여 승진하거나 좋은 직장으로 이직할 기회입니다.", "⭐⭐⭐⭐"
        elif season == "Fire": msg, score = "문서운이 최고입니다. 부동산 계약이나 중요 서류를 처리하기 좋습니다.", "⭐⭐⭐⭐⭐"
        elif season == "Earth": msg, score = "사람들과 어울리느라 돈이 나갑니다. 고집을 부리면 손해를 봅니다.", "⭐⭐"
        elif season == "Metal": msg, score = "새로운 일을 벌이거나 창작 활동을 하기에 좋습니다. 표현력이 좋아집니다.", "⭐⭐⭐"
        elif season == "Water": msg, score = "큰 돈이 눈앞에 보이지만 욕심내면 탈이 납니다. 돌다리도 두들겨 보세요.", "⭐⭐⭐"

    # 4. 쇠(Metal) 일간인 경우
    elif element == "Metal":
        if season == "Wood": msg, score = "노력한 만큼 재물이 들어옵니다. 성과급이나 보너스를 기대해볼 만합니다.", "⭐⭐⭐⭐⭐"
        elif season == "Fire": msg, score = "관재구설(시비, 소송)을 조심해야 합니다. 묵묵히 일하면 오히려 전화위복이 됩니다.", "⭐"
        elif season == "Earth": msg, score = "부동산이나 계약 관련 좋은 소식이 있습니다. 부모님이나 윗사람의 덕을 봅니다.", "⭐⭐⭐⭐"
        elif season == "Metal": msg, score = "경쟁심이 강해져 주변과 충돌할 수 있습니다. 유연한 태도가 필요합니다.", "⭐⭐"
        elif season == "Water": msg, score = "재능을 발휘하여 문제를 해결합니다. 인기가 많아지고 찾는 사람이 늘어납니다.", "⭐⭐⭐⭐"

    # 5. 물(Water) 일간인 경우
    elif element == "Water":
        if season == "Wood": msg, score = "새로운 프로젝트를 시작하기 좋습니다. 자녀에게 좋은 일이 생깁니다.", "⭐⭐⭐⭐"
        elif season == "Fire": msg, score = "일확천금의 기회가 오지만 위험도 따릅니다. 신중하게 투자하면 대박입니다.", "⭐⭐⭐"
        elif season == "Earth": msg, score = "직장에서 승진하거나 감투를 쓰게 됩니다. 어깨가 무거워지지만 명예롭습니다.", "⭐⭐⭐"
        elif season == "Metal": msg, score = "공부와 자격증 취득에 최적의 시기입니다. 돕는 귀인이 나타납니다.", "⭐⭐⭐⭐⭐"
        elif season == "Water": msg, score = "내 밥그릇을 노리는 경쟁자가 나타납니다. 돈 거래는 절대 금물입니다.", "⭐⭐"

    return msg, score
# --- 5. 메인 UI ---
def main():
    with st.sidebar:
        st.title("Settings")
        lang_opt = st.radio("Language", ["Korean (한국어)", "English (미국)"])
        lang = "ko" if "Korean" in lang_opt else "en"
        st.info("💡 **Tip:** 일간(Day Master)과 2026년 월운(Monthly Energy)의 상호작용을 정밀 계산합니다.")

    ui = {
        "ko": {"title": "디 엘리먼트: 사주 프로", "sub": "당신의 운명 지도와 2026년 정밀 분석", "name": "이름", "btn": "운명 분석하기", "tab1": "🔮 타고난 기질", "tab2": "📅 2026년 월별 운세"},
        "en": {"title": "The Element: Pro", "sub": "Precise Day-Master Analysis", "name": "Name", "btn": "Analyze Destiny", "tab1": "Personality", "tab2": "2026 Forecast"}
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
            # 1. 일주 계산
            day_info = calculate_day_gan(b_date)
            element_type = day_info['element']
            trait, forecast = get_interpretation(element_type, lang)
            
            # --- 결과 화면 ---
            tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])
            
            # 탭 1: 성격
            with tab1:
                st.markdown(f"""
                <div class='card'>
                    <h3 style='color: #64748b;'>👋 {name}</h3>
                    <h1 style='color: #4f46e5; margin: 10px 0;'>{day_info[lang]}</h1>
                    <hr>
                    <div style='font-size: 1.1em; line-height: 1.8;'>{trait}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 인쇄 버튼 (HTML/JS 주입)
                st.markdown(f"""
                <button onclick="window.print()" class="print-btn">{txt['print']}</button>
                """, unsafe_allow_html=True)

            # 탭 2: 2026 운세
            with tab2:
                if lang == "ko":
                    st.markdown(f"""
                    <div class='card' style='border: 2px solid #ec4899; background-color: #fff1f2;'>
                        <h2 style='color: #be185d;'>👑 2026년 병오년(붉은 말) 핵심 요약</h2>
                        <h3 class='highlight'>{forecast['title']}</h3>
                        <p>{forecast['gen']}</p>
                        <ul style='margin-top:10px;'>
                            <li><b>💰 재물:</b> {forecast['money']}</li>
                            <li><b>❤️ 연애:</b> {forecast['love']}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("📅 2026년 월별 상세 흐름")
                    monthly_data = []
                    month_seq = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
                    month_names = ["2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월", "내년 1월"]

                    for idx, m_num in enumerate(month_seq):
                        msg, score = get_monthly_forecast(element_type, m_num)
                        monthly_data.append({"Month": month_names[idx], "Luck": score, "Advice": msg})
                    
                    st.table(pd.DataFrame(monthly_data))
                    
                    # 인쇄 버튼 (여기에도 추가)
                    st.markdown(f"""
                    <button onclick="window.print()" class="print-btn">{txt['print']}</button>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Full monthly forecast is currently available in Korean mode.")
        else:
            st.warning("Please enter your name.")

if __name__ == "__main__":
    main()
