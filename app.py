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
    # 성격 데이터
    traits_ko = {
        "Wood": "성장과 시작의 에너지. 곧게 뻗어나가는 의지와 추진력이 강합니다. 명예를 중시합니다.",
        "Fire": "열정과 확산의 에너지. 솔직하고 화끈하며 예의가 바릅니다. 감정 표현이 풍부합니다.",
        "Earth": "포용과 중재의 에너지. 믿음직스럽고 묵직합니다. 속마음을 잘 드러내지 않지만 신용이 있습니다.",
        "Metal": "결단과 정의의 에너지. 맺고 끊음이 확실하고 의리가 있습니다. 리더십이 강합니다.",
        "Water": "지혜와 유연함의 에너지. 상황 대처 능력이 뛰어나고 머리가 비상합니다. 생각이 깊습니다."
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
    # 2026년의 월별 오행 흐름 (절기 기준 대략적 분류)
    # 2,3월(목) / 4월(토) / 5,6월(화) / 7월(토) / 8,9월(금) / 10월(토) / 11,12월(수) / 1월(수/토)
    
    season_element = ""
    if month in [2, 3]: season_element = "Wood"   # 봄
    elif month in [5, 6]: season_element = "Fire" # 여름
    elif month in [8, 9]: season_element = "Metal"# 가을
    elif month in [11, 12, 1]: season_element = "Water" # 겨울
    else: season_element = "Earth" # 환절기 (4, 7, 10월)

    # 오행별 월별 운세 멘트 생성기
    msg = ""
    score = "⭐⭐⭐"

    if element == "Wood": # 나무인 사람
        if season_element == "Wood": msg, score = "경쟁자가 나타납니다. 내 몫을 뺏기지 않게 주의하세요.", "⭐⭐"
        elif season_element == "Fire": msg, score = "아이디어가 넘치고 일이 술술 풀립니다. 활동하기 최고입니다.", "⭐⭐⭐⭐⭐"
        elif season_element == "Earth": msg, score = "뜻밖의 꽁돈이 생기거나 재물운이 좋습니다.", "⭐⭐⭐⭐"
        elif season_element == "Metal": msg, score = "직장에서 스트레스를 받거나 책임질 일이 생깁니다.", "⭐⭐"
        elif season_element == "Water": msg, score = "윗사람의 도움을 받거나 계약하기 좋은 달입니다.", "⭐⭐⭐⭐"
        
    elif element == "Fire": # 불인 사람
        if season_element == "Wood": msg, score = "귀인의 도움으로 문서 계약이나 합격 소식이 있습니다.", "⭐⭐⭐⭐⭐"
        elif season_element == "Fire": msg, score = "자신감이 넘치지만 독단적인 행동으로 다툼이 생길 수 있습니다.", "⭐⭐"
        elif season_element == "Earth": msg, score = "말과 행동으로 능력을 인정받습니다. 표현하세요.", "⭐⭐⭐⭐"
        elif season_element == "Metal": msg, score = "재물운이 폭발합니다. 보너스나 수익이 기대됩니다.", "⭐⭐⭐⭐⭐"
        elif season_element == "Water": msg, score = "과로하거나 직장에서 압박을 받을 수 있습니다.", "⭐"

    elif element == "Earth": # 흙인 사람
        if season_element == "Wood": msg, score = "직장 변동이나 이직 제안이 올 수 있습니다. 명예운 상승.", "⭐⭐⭐"
        elif season_element == "Fire": msg, score = "공부하기 좋고 윗사람에게 인정받습니다. 문서운 최고.", "⭐⭐⭐⭐⭐"
        elif season_element == "Earth": msg, score = "친구나 동료와 어울리며 돈을 쓸 일이 많아집니다.", "⭐⭐"
        elif season_element == "Metal": msg, score = "새로운 일을 벌이거나 창작 활동에 좋습니다.", "⭐⭐⭐⭐"
        elif season_element == "Water": msg, score = "큰 돈이 들어오지만 욕심내면 탈이 납니다.", "⭐⭐⭐"

    elif element == "Metal": # 쇠인 사람
        if season_element == "Wood": msg, score = "노력한 만큼 재물이 들어옵니다. 성과급 기대.", "⭐⭐⭐⭐⭐"
        elif season_element == "Fire": msg, score = "관재구설(시비)를 조심하세요. 묵묵히 일하면 승진합니다.", "⭐⭐"
        elif season_element == "Earth": msg, score = "부동산이나 계약 관련 좋은 소식이 있습니다.", "⭐⭐⭐⭐"
        elif season_element == "Metal": msg, score = "고집이 세져서 주변과 충돌할 수 있습니다. 유연하세요.", "⭐⭐"
        elif season_element == "Water": msg, score = "재능을 발휘하여 문제를 해결합니다. 인기가 많아집니다.", "⭐⭐⭐⭐"

    elif element == "Water": # 물인 사람
        if season_element == "Wood": msg, score = "새로운 프로젝트를 시작하거나 자녀에게 좋은 일이 있습니다.", "⭐⭐⭐⭐"
        elif season_element == "Fire": msg, score = "돈 욕심이 생겨 투자하지만 신중해야 합니다. 결과는 큽니다.", "⭐⭐⭐"
        elif season_element == "Earth": msg, score = "직장에서 인정받고 승진할 기회입니다. 부담감은 큽니다.", "⭐⭐⭐"
        elif season_element == "Metal": msg, score = "공부와 자격증 취득에 최적의 시기입니다. 돕는 이가 있습니다.", "⭐⭐⭐⭐⭐"
        elif season_element == "Water": msg, score = "경쟁 심리가 발동합니다. 내 것을 지키는 데 집중하세요.", "⭐⭐"

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
