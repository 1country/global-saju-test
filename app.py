import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Pro", page_icon="🌌", layout="wide")

# 스타일 (CSS)
st.markdown("""
<style>
    .main-header {font-size: 2.2em; color: #1e293b; text-align: center; font-weight: 800; margin-bottom: 10px;}
    .sub-header {font-size: 1.0em; color: #64748b; text-align: center; margin-bottom: 30px;}
    .card {background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 20px;}
    .highlight {color: #2563eb; font-weight: bold;}
    .lucky-score {color: #f59e0b; font-size: 1.2em;}
    .warn {color: #ef4444; font-weight: bold;}
    /* 표 스타일 */
    thead tr th {background-color: #f1f5f9 !important; color: #334155 !important; font-weight: bold !important;}
    tbody tr:nth-child(even) {background-color: #f8fafc;}
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
    # 1. 성격 데이터 (상세 버전)
    traits_ko = {
        "Wood": """**[핵심: 성장과 자존심]**<br>
        당신은 하늘을 향해 곧게 뻗어 올라가는 나무의 기운을 타고났습니다. 성격이 대쪽 같고 솔직하며, 성장하고자 하는 욕구가 매우 강합니다. 남의 밑에 있기보다는 우두머리가 되기를 좋아합니다.<br><br>
        **[장점]** 추진력이 강하고 인자한 성품을 지녔습니다. 목표가 생기면 뒤를 돌아보지 않고 직진합니다.<br>
        **[단점]** 굽히기를 싫어해서 부러질 수 있습니다. 융통성을 조금만 기르면 대성할 재목입니다.""",
        
        "Fire": """**[핵심: 열정과 표현]**<br>
        당신은 세상을 환하게 비추는 태양이나 촛불입니다. 매사에 열정적이고 에너지가 넘쳐흐릅니다. 자신의 감정을 숨기지 못하고 얼굴에 다 드러나는 투명한 사람입니다.<br><br>
        **[장점]** 예의가 바르고 화끈하며 뒤끝이 없습니다. 어디서나 분위기 메이커 역할을 합니다.<br>
        **[단점]** 성격이 급해서 실수를 할 수 있습니다. 시작은 화려하나 마무리가 약할 수 있으니 끈기가 필요합니다.""",
        
        "Earth": """**[핵심: 신용과 중재]**<br>
        당신은 묵직한 산이나 넓은 대지입니다. 가볍게 움직이지 않으며, 믿음과 신용을 목숨처럼 중요하게 생각합니다. 포용력이 넓어 많은 사람들이 당신에게 의지하려 합니다.<br><br>
        **[장점]** 입이 무겁고 뚝심이 있어 한번 맡은 일은 끝까지 해냅니다. 중재자 역할을 잘합니다.<br>
        **[단점]** 속마음을 잘 드러내지 않아 답답해 보일 수 있습니다. 때로는 과감한 표현이 필요합니다.""",
        
        "Metal": """**[핵심: 결단과 의리]**<br>
        당신은 단단한 바위나 날카로운 칼입니다. 의리와 정의를 가장 중요하게 생각합니다. 흐지부지한 것을 싫어하고, 맺고 끊음이 확실한 '상남자/걸크러시' 스타일입니다.<br><br>
        **[장점]** 리더십이 있고 결단력이 빠릅니다. 내 사람이라고 생각하면 끝까지 책임집니다.<br>
        **[단점]** 말이 직설적이라 본의 아니게 남에게 상처를 줄 수 있습니다. 조금 더 부드러운 화법이 필요합니다.""",
        
        "Water": """**[핵심: 지혜와 유연함]**<br>
        당신은 흐르는 물이나 바다입니다. 어떤 그릇에도 담길 수 있는 유연함과 상황 대처 능력을 가졌습니다. 머리가 비상하고 기획력이 뛰어나며 지혜롭습니다.<br><br>
        **[장점]** 임기응변에 강하고 친화력이 좋습니다. 조용히 실속을 챙기는 능력이 탁월합니다.<br>
        **[단점]** 생각이 꼬리에 꼬리를 물어 우울해지거나, 비밀이 너무 많아 속을 알 수 없다는 평을 듣기도 합니다."""
    }
    traits_en = {"Wood": "Energy of Growth", "Fire": "Energy of Passion", "Earth": "Energy of Stability", "Metal": "Energy of Justice", "Water": "Energy of Wisdom"}

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
            
            with tab1: # 기본 성격
                st.markdown(f"""
                <div class='card'>
                    <h3 style='color: #64748b;'>👋 {name}님의 타고난 본질</h3>
                    <h1 style='color: #4f46e5; margin: 10px 0;'>{day_info[lang]}</h1>
                    <hr>
                    <p style='font-size: 1.1em; line-height: 1.8;'>{trait}</p>
                </div>
                """, unsafe_allow_html=True)

            with tab2: # 2026 운세 (유료급)
                if lang == "ko":
                    # 총평
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
                    
                    # 월별 상세 운세 (표 생성)
                    st.subheader("📅 2026년 월별 상세 흐름")
                    
                    monthly_data = []
                    # 2026년 2월(입춘)부터 2027년 1월까지 순서대로
                    month_seq = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
                    month_names = ["2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월", "내년 1월"]

                    for idx, m_num in enumerate(month_seq):
                        msg, score = get_monthly_forecast(element_type, m_num)
                        monthly_data.append({
                            "월(Month)": month_names[idx], 
                            "운세 점수": score, 
                            "상세 코멘트 (Advice)": msg
                        })
                    
                    df = pd.DataFrame(monthly_data)
                    st.table(df) # 깔끔한 표 출력
                else:
                    st.info("Full monthly forecast is currently available in Korean mode.")
        else:
            st.warning("Please enter your name.")

if __name__ == "__main__":
    main()
