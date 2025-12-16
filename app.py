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
    th {background-color: #f8fafc !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. 진짜 만세력 엔진 (일주 계산 로직) ---
# 1900년 1월 1일은 '갑술(甲戌)'일 입니다. 이를 기준으로 날짜를 계산합니다.
def calculate_day_gan(birth_date):
    # 기준일: 1900-01-01 (월요일)
    base_date = date(1900, 1, 1)
    
    # 기준일로부터 며칠 지났는지 계산
    delta = birth_date - base_date
    days_passed = delta.days
    
    # 천간(10개): 갑(0), 을(1), 병(2), 정(3), 무(4), 기(5), 경(6), 신(7), 임(8), 계(9)
    # 1900.1.1은 갑(0)술일이므로, days_passed % 10 하면 오늘의 천간 인덱스가 나옴.
    if days_passed < 0:
        return 0 # 예외처리 (1900년 이전)
        
    gan_index = days_passed % 10
    
    # 천간 데이터 (한/영)
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
    # 진짜 사주는 "일간(Day Master)"을 기준으로 봅니다.
    # 내용이 길어서 일부만 예시로 넣지만, 실제로는 각 오행별로 다르게 나옵니다.
    
    # 1. 성격 데이터 (일간 기준)
    traits_ko = {
        "Wood": "당신은 성장과 시작의 에너지를 타고났습니다. (갑/을) 나무처럼 위로 뻗어나가려는 의지가 강하며, 인자하고 부드러운 성품 속에 강한 고집이 있습니다. 남에게 굽히기 싫어하고 명예를 중요하게 생각합니다.",
        "Fire": "당신은 열정과 확산의 에너지입니다. (병/정) 태양이나 촛불처럼 자신을 태워 세상을 밝힙니다. 예의가 바르고 화끈하며 뒤끝이 없습니다. 하지만 감정 기복이 심하고 급한 성격이 단점일 수 있습니다.",
        "Earth": "당신은 포용과 중재의 에너지입니다. (무/기) 넓은 땅처럼 믿음직스럽고 신용이 있습니다. 남의 말을 잘 들어주지만 속마음을 잘 드러내지 않습니다. 고집이 세지만 한번 내 편이면 끝까지 지켜줍니다.",
        "Metal": "당신은 결단과 정의의 에너지입니다. (경/신) 단단한 바위나 보석처럼 맺고 끊음이 확실합니다. 의리가 있고 리더십이 강합니다. 차가워 보일 수 있지만 내 사람에게는 확실합니다.",
        "Water": "당신은 지혜와 유연함의 에너지입니다. (임/계) 흐르는 물처럼 어디든 적응합니다. 머리가 비상하고 기획력이 뛰어납니다. 생각이 너무 많아 우울해질 수 있으니 주의해야 합니다."
    }
    
    traits_en = {
        "Wood": "You represent the energy of Growth. Like a tree, you are upward-looking, benevolent, and stubborn. You value honor and dislike being controlled.",
        "Fire": "You represent Passion. Like the sun or fire, you express yourself openly. You are polite but can be impatient. You are the center of attention.",
        "Earth": "You represent Stability. Like a mountain, you are trustworthy and steady. You don't reveal your feelings easily but are very loyal.",
        "Metal": "You represent Justice. Like steel or a gem, you are decisive and sharp. You value loyalty and have strong leadership qualities.",
        "Water": "You represent Wisdom. Like the ocean, you are adaptable and smart. You are a deep thinker but can sometimes overthink."
    }
    
    # 2. 2026년 운세 로직 (십성 관계 분석)
    # 2026년 = 병오(丙午)년 = 강력한 불(Fire)의 해
    # 내 일간(Day Master)과 2026년(Fire)의 관계를 봅니다.
    
    forecast_ko = {}
    
    if element == "Wood": # 목생화 (식상운)
        forecast_ko = {
            "title": "🔥 재능이 폭발하고 일이 많아지는 해 (식상운)",
            "gen": "나무가 불을 만나니 활활 타오릅니다. 당신의 능력을 세상에 보여줄 기회가 쏟아집니다. 일이 너무 많아 몸이 바쁘고, 새로운 진로를 열게 됩니다. 다만 과로를 조심하세요.",
            "money": "돈을 벌 기회는 많으나, 투자나 지출도 같이 늘어납니다.",
            "love": "표현력이 좋아져 연애운이 상승합니다. 자녀운도 있습니다."
        }
    elif element == "Fire": # 화화 (비겁운)
        forecast_ko = {
            "title": "🤝 경쟁자와 협력자가 공존하는 해 (비겁운)",
            "gen": "불이 불을 만났습니다. 자존심과 경쟁심이 강해집니다. 주변에 사람이 모여들지만, 내 몫을 나눠야 할 수도 있습니다. 독립하고 싶은 마음이 커집니다.",
            "money": "돈 거래는 절대 금물입니다. 공동 투자는 신중해야 합니다.",
            "love": "친구가 연인이 되거나, 경쟁자가 생길 수 있습니다."
        }
    elif element == "Earth": # 화생토 (인성운)
        forecast_ko = {
            "title": "📜 귀인의 도움과 문서 계약의 해 (인성운 - 대길)",
            "gen": "불이 흙을 단단하게 만들어줍니다. 윗사람의 도움을 받고, 공부나 자격증 취득에 최적의 시기입니다. 부동산 계약이나 승진 등 문서운이 아주 좋습니다.",
            "money": "문서(집, 주식, 계약서)로 재산을 불리는 운입니다.",
            "love": "사랑받는 시기입니다. 연상이나 배울 점이 있는 사람을 만납니다."
        }
    elif element == "Metal": # 화극금 (관성운)
        forecast_ko = {
            "title": "🔨 압박감 속에서 명예가 오르는 해 (관성운)",
            "gen": "불이 쇠를 녹여 도구를 만듭니다. 직장에서 책임감이 커지고 스트레스를 받을 수 있지만, 이를 견디면 승진과 명예가 따릅니다. 조직에서 자리를 잡는 시기입니다.",
            "money": "고정 수입이 늘거나 직급이 오릅니다.",
            "love": "여자는 남자가 들어오는 운입니다. 남자는 자식운이 있습니다."
        }
    elif element == "Water": # 수극화 (재성운)
        forecast_ko = {
            "title": "💰 재물을 쟁취하기 위해 싸우는 해 (재성운)",
            "gen": "물이 불을 끄려 합니다. 불은 당신에게 '재물'입니다. 큰 돈을 벌 기회가 오지만, 그만큼 치열하게 움직여야 합니다. 결과가 확실하게 나오는 해입니다.",
            "money": "사업 확장, 투자 수익 등 금전운이 가장 강합니다.",
            "love": "남자는 여자운이 강하게 들어옵니다. 즐거운 일이 많습니다."
        }

    # 영어 운세는 간략히 매핑 (실제론 번역 필요)
    forecast_en = {
        "title": "2026 Forecast for " + element,
        "gen": "Detailed forecast is currently optimized for Korean language. (Translating logic...)",
        "money": "Financial opportunities arise.",
        "love": "Relationship luck fluctuates."
    }

    # 언어 선택 반환
    if lang == "ko":
        return traits_ko[element], forecast_ko
    else:
        return traits_en[element], forecast_en

# --- 4. 메인 UI ---
def main():
    # 사이드바
    with st.sidebar:
        st.title("Settings")
        lang_opt = st.radio("Language", ["Korean (한국어)", "English (미국)"])
        lang = "ko" if "Korean" in lang_opt else "en"
        st.info("💡 **Tip:** 이제 생일을 하루만 바꿔도 결과가 달라집니다. (일주 정밀 계산 적용)")

    # UI 텍스트 설정
    ui = {
        "ko": {"title": "디 엘리먼트: 사주 프로", "sub": "당신의 생년월일시를 분석한 정밀 리포트", "name": "이름", "btn": "운명 분석하기", "tab1": "🔮 타고난 기질 (성격)", "tab2": "📅 2026년 정밀 운세"},
        "en": {"title": "The Element: Pro", "sub": "Precise Day-Master Analysis", "name": "Name", "btn": "Analyze Destiny", "tab1": "Core Personality", "tab2": "2026 Forecast"}
    }
    txt = ui[lang]

    st.markdown(f"<div class='main-header'>{txt['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{txt['sub']}</div>", unsafe_allow_html=True)

    # 입력창 (3단)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        name = st.text_input(txt['name'])
    with c2:
        # 1900년부터 선택 가능
        b_date = st.date_input("Date of Birth", min_value=date(1900,1,1), value=date(1990,1,1))
    with c3:
        b_time = st.time_input("Time of Birth", value=None)

    # 버튼 클릭
    if st.button(txt['btn'], use_container_width=True):
        if name:
            # 1. 일주(Day Gan) 계산 - 핵심 로직
            day_info = calculate_day_gan(b_date)
            element_type = day_info['element'] # Wood, Fire...
            
            # 2. 해석 데이터 가져오기
            trait, forecast = get_interpretation(element_type, lang)
            
            # --- 결과 화면 ---
            
            # [탭 1] 기본 성격
            tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])
            
            with tab1:
                st.markdown(f"""
                <div class='card'>
                    <h3>👋 {name}님의 타고난 에너지는...</h3>
                    <h1 style='color: #4f46e5;'>{day_info[lang]}</h1>
                    <p style='color: #64748b;'>기준일: {b_date} (일주 기준 분석)</p>
                    <hr>
                    <div style='line-height: 1.8; font-size: 1.1em;'>
                        {trait}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # [탭 2] 2026년 운세 (풍성하게)
            with tab2:
                if lang == "ko":
                    st.markdown(f"""
                    <div class='card' style='border: 2px solid #8b5cf6; background-color: #fdf4ff;'>
                        <h2 style='color: #7c3aed;'>👑 2026년 병오년(붉은 말) 총평</h2>
                        <h3 class='highlight'>{forecast['title']}</h3>
                        <p style='font-size: 1.1em; margin-top: 15px;'>{forecast['gen']}</p>
                        <br>
                        <p><b>💰 재물/직업:</b> {forecast['money']}</p>
                        <p><b>❤️ 연애/대인:</b> {forecast['love']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 월별 운세 표 (Table)
                    st.subheader("📅 2026년 월별 흐름표")
                    
                    # 오행별로 월별 운세가 다르게 나옴 (간략 로직)
                    monthly_data = []
                    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
                    
                    for i, m in enumerate(months):
                        # 임시 로직: 여름(4,5,6월)에 불이 강함 -> 일간별로 해석 달라짐
                        luck = "⭐⭐⭐"
                        msg = "무난한 흐름입니다."
                        
                        if i in [4, 5, 6]: # 여름
                            if element_type in ["Water", "Earth"]: 
                                luck = "⭐⭐⭐⭐⭐"
                                msg = "기운이 가장 강한 시기입니다. 기회를 잡으세요!"
                            else:
                                luck = "⭐⭐"
                                msg = "스트레스 관리가 필요합니다. 휴식하세요."
                        
                        monthly_data.append({"월(Month)": m, "운세 점수": luck, "주요 흐름": msg})
                        
                    df = pd.DataFrame(monthly_data)
                    st.table(df)
                    
                else:
                    st.info("English forecast requires detailed translation. Currently showing Korean logic structure.")
                    st.write(forecast)
                    
        else:
            st.warning("Please enter your name.")

if __name__ == "__main__":
    main()
