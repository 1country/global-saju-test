import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date, timedelta
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 및 환경 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Date Selection | The Element", page_icon="📆", layout="wide")

if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/date_selection"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        
        .stApp {
            background-image: linear-gradient(rgba(20, 30, 48, 0.9), rgba(36, 59, 85, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        
        .main-title {
            font-size: 2.5em; font-weight: 800; color: #f472b6; text-align: center; margin-bottom: 10px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);
        }
        
        /* 추천 카드 스타일 */
        .rec-card {
            background: rgba(30, 41, 59, 0.95); border: 1px solid #f472b6; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; text-align: center;
            box-shadow: 0 4px 15px rgba(244, 114, 182, 0.15);
        }
        .rec-date {
            font-size: 1.8em; font-weight: bold; color: #f8fafc; margin-bottom: 5px;
        }
        .rec-star {
            font-size: 1.5em; margin-bottom: 15px; text-shadow: 0 0 5px #fbbf24;
        }
        .rec-desc {
            font-size: 1.1em; color: #e2e8f0; line-height: 1.6;
        }
        
        /* 입력 라벨 밝게 */
        .stSelectbox label p, .stDateInput label p {
            color: #e2e8f0 !important; font-weight: 600 !important; font-size: 1.1rem !important;
        }

        /* 잠금 오버레이 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #f472b6;
            box-shadow: 0 0 20px rgba(244, 114, 182, 0.3);
        }
        
        @media print {
            section[data-testid="stSidebar"], header, footer { display: none !important; }
            .stApp { background: white !important; color: black !important; }
            .rec-card { border: 1px solid #ccc !important; color: black !important; background: white !important; }
            h1, h2, h3, p, span { color: black !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 로직 및 데이터
# ----------------------------------------------------------------
def get_relationship(user_elem, day_elem):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Wood": "Resource", "Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power"},
        "Earth": {"Wood": "Power", "Fire": "Resource", "Earth": "Same", "Metal": "Output", "Water": "Wealth"},
        "Metal": {"Wood": "Wealth", "Fire": "Power", "Earth": "Resource", "Metal": "Same", "Water": "Output"},
        "Water": {"Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource", "Water": "Same"},
    }
    return relations.get(user_elem, {}).get(day_elem, "Same")

# 목적 선택 옵션 (6개 국어)
goals = {
    "Wealth": {
        "ko": "💰 재물/투자/쇼핑 (Wealth)", "en": "💰 Wealth & Investment", "fr": "💰 Richesse", 
        "es": "💰 Riqueza", "ja": "💰 財運・投資", "zh": "💰 财运/投资"
    },
    "Output": {
        "ko": "🎨 연애/고백/창작 (Love/Creativity)", "en": "🎨 Love & Creativity", "fr": "🎨 Amour", 
        "es": "🎨 Amor", "ja": "🎨 恋愛・告白", "zh": "🎨 恋爱/创作"
    },
    "Resource": {
        "ko": "📚 계약/이사/공부 (Contract/Study)", "en": "📚 Contract & Study", "fr": "📚 Contrat", 
        "es": "📚 Contrato", "ja": "📚 契約・引越し", "zh": "📚 合同/搬家"
    },
    "Power": {
        "ko": "⚖️ 승진/면접/관운 (Career/Promotion)", "en": "⚖️ Career & Promotion", "fr": "⚖️ Carrière", 
        "es": "⚖️ Carrera", "ja": "⚖️ 昇進・面接", "zh": "⚖️ 事业/晋升"
    },
    "Same": {
        "ko": "🤝 친목/모임/협업 (Social/Meeting)", "en": "🤝 Social & Networking", "fr": "🤝 Social", 
        "es": "🤝 Social", "ja": "🤝 親睦・集まり", "zh": "🤝 社交/聚会"
    }
}

# 결과 멘트 (6개 국어)
advice_msg = {
    "Wealth": {
        "ko": "금전운이 강하게 들어오는 날입니다. 투자를 하거나, 중요한 물건을 사거나, 결과를 내기에 최적의 타이밍입니다.",
        "en": "Strong financial energy. Best day for investments, major purchases, or finalizing deals.",
        "fr": "Excellente énergie financière. Idéal pour investir.",
        "es": "Gran energía financiera. Ideal para invertir.",
        "ja": "金運が強い日です。投資や買い物に最適です。",
        "zh": "财运很强。适合投资或购物。"
    },
    "Output": {
        "ko": "당신의 매력과 표현력이 빛나는 날입니다. 데이트를 하거나, 고백을 하거나, 창의적인 일을 하기에 완벽합니다.",
        "en": "Your charm shines today. Perfect for dating, confessing love, or creative work.",
        "fr": "Votre charme opère. Parfait pour les rendez-vous.",
        "es": "Tu encanto brilla. Perfecto para citas.",
        "ja": "魅力が輝く日です。デートや告白に最適です。",
        "zh": "魅力四射的一天。适合约会或表白。"
    },
    "Resource": {
        "ko": "안정적인 기운이 돕는 날입니다. 계약서에 도장을 찍거나, 이사를 가거나, 차분히 공부하기에 가장 좋습니다.",
        "en": "Stable energy supports you. Best for signing contracts, moving, or studying.",
        "fr": "Énergie stable. Idéal pour les contrats.",
        "es": "Energía estable. Ideal para contratos.",
        "ja": "安定した運気です。契約や勉強に良い日です。",
        "zh": "气场稳定。适合签约或学习。"
    },
    "Power": {
        "ko": "명예와 권위가 따르는 날입니다. 면접을 보거나, 승진 시험을 치거나, 중요한 책임을 맡기에 유리합니다.",
        "en": "Day of honor and authority. Great for interviews, exams, or taking responsibility.",
        "fr": "Jour d'honneur. Bon pour les entretiens.",
        "es": "Día de honor. Bueno para entrevistas.",
        "ja": "名誉の日です。面接や昇進試験に有利です。",
        "zh": "名誉之日。适合面试或晋升。"
    },
    "Same": {
        "ko": "사람들과의 유대가 강해지는 날입니다. 파티를 열거나, 친구를 만나거나, 동업자와 회의하기 좋습니다.",
        "en": "Strong social bonds. Good for parties, meeting friends, or networking.",
        "fr": "Liens sociaux forts. Bon pour les fêtes.",
        "es": "Lazos sociales fuertes. Bueno para fiestas.",
        "ja": "絆が深まる日です。友人との集まりに最適。",
        "zh": "社交运强。适合聚会或见朋友。"
    }
}

# ----------------------------------------------------------------
# 4. 사이드바
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Current Mode: **{lang_map.get(lang, 'English')}**")
    
    st.write("Change Language:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🇺🇸 EN"): st.session_state['lang']='en'; st.rerun()
    with c2: 
        if st.button("🇰🇷 KO"): st.session_state['lang']='ko'; st.rerun()
    with c3: 
        if st.button("🇫🇷 FR"): st.session_state['lang']='fr'; st.rerun()
    c4, c5, c6 = st.columns(3)
    with c4: 
        if st.button("🇪🇸 ES"): st.session_state['lang']='es'; st.rerun()
    with c5: 
        if st.button("🇯🇵 JA"): st.session_state['lang']='ja'; st.rerun()
    with c6: 
        if st.button("🇨🇳 ZH"): st.session_state['lang']='zh'; st.rerun()

    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 5. 메인 UI
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    st.stop()

# UI 텍스트
ui = {
    "ko": {
        "title": "📆 길일 택일 (Best Dates)", "sub": "가장 중요한 일을 하기에 완벽한 날짜 3개를 찾아드립니다.",
        "q1": "1. 어떤 날을 찾으시나요?", "q2": "2. 언제쯤으로 원하시나요?",
        "btn": "🏆 최고의 날짜 3개 찾기", "res_h": "당신을 위한 최고의 길일 Top 3",
        "lock_t": "🔒 택일 리포트 잠금 (VIP)", "lock_m": "당신의 사주에 딱 맞는 길일 3개를 확인하세요.",
        "btn_buy": "잠금 해제 ($10)", "key_label": "라이센스 키"
    },
    "en": {
        "title": "📆 Find Best Dates", "sub": "We recommend the Top 3 perfect dates for your important events.",
        "q1": "1. What is your goal?", "q2": "2. Around which date?",
        "btn": "🏆 Find Top 3 Dates", "res_h": "Top 3 Auspicious Dates for You",
        "lock_t": "🔒 Report Locked", "lock_m": "Unlock the best dates tailored to your destiny.",
        "btn_buy": "Unlock ($10)", "key_label": "License Key"
    },
    # (다른 언어 생략 - 영어 fallback)
}
if lang not in ui: t = ui['en']
else: t = ui[lang]

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#cbd5e1; margin-bottom:40px;'>{t['sub']}</div>", unsafe_allow_html=True)

# 1. 입력 섹션
with st.container(border=True):
    # 목적 선택
    goal_options = list(goals.keys()) # Wealth, Output...
    # 보여지는 텍스트 매핑
    format_func = lambda x: goals[x][lang]
    
    selected_goal_key = st.selectbox(t['q1'], goal_options, format_func=format_func)
    
    # 기준 날짜 선택
    target_date = st.date_input(t['q2'], min_value=date.today())
    
    st.write("")
    analyze_btn = st.button(t['btn'], type="primary", use_container_width=True)

# 2. 분석 및 결과
if analyze_btn or st.session_state.get('date_analyzed_2'):
    st.session_state['date_analyzed_2'] = True
    
    # 내 사주
    my_info = calculate_day_gan(st.session_state["birth_date"])
    
    def map_elem(input_val):
        valid_english = ["Wood", "Fire", "Earth", "Metal", "Water"]
        if input_val in valid_english: return input_val
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(input_val, 'Wood')

    my_elem = map_elem(my_info['element'])
    
    st.divider()
    
    # 🔒 잠금 확인
    if "unlocked_date_2" not in st.session_state: st.session_state["unlocked_date_2"] = False
    
    if not st.session_state["unlocked_date_2"]:
        # 블러 처리된 가짜 결과
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(12px); opacity: 0.6; pointer-events: none;'>
                <div class='rec-card'>
                    <div class='rec-date'>2025-05-01 (Friday)</div>
                    <div class='rec-star'>⭐⭐⭐⭐⭐</div>
                    <p>This is the perfect day for your goal...</p>
                </div>
                <div class='rec-card'>
                    <div class='rec-date'>2025-05-05 (Monday)</div>
                    <div class='rec-star'>⭐⭐⭐⭐</div>
                </div>
            </div>
            <div class='lock-overlay'>
                <h3 style='color: #f472b6;'>{t['lock_t']}</h3>
                <p style='color: #e2e8f0; margin-bottom: 20px; font-size: 1.1em;'>{t['lock_m']}</p>
                <a href="{GUMROAD_LINK_SPECIFIC}" target="_blank" 
                   style="background-color: #ec4899; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; display: inline-block;">
                   {t['btn_buy']}
                </a>
            </div>
        </div>
        """
        st.markdown(blur_html, unsafe_allow_html=True)
        
        with st.expander(f"{t['key_label']} Input"):
            c1, c2 = st.columns([3, 1])
            with c1: k_in = st.text_input(t['key_label'], type="password", label_visibility="collapsed")
            with c2: 
                if st.button("Unlock"):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_date_2"] = True
                        st.success("Unlocked!")
                        st.rerun()
                    else:
                        try:
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={"product_permalink": "date_selection", "license_key": k_in}).json()
                            if r.get("success"):
                                st.session_state["unlocked_date_2"] = True
                                st.rerun()
                            else:
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={"product_permalink": "all-access_pass", "license_key": k_in}).json()
                                if r2.get("success"):
                                    st.session_state["unlocked_date_2"] = True
                                    st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: st.error("Error")
    else:
        # 🔓 해제됨: 진짜 추천 로직
        st.success("🔓 Top 3 Dates Found!")
        st.subheader(t['res_h'])
        
        # 날짜 탐색 (기준일 전후 15일 = 총 30일 탐색)
        start_date = target_date - timedelta(days=10)
        end_date = target_date + timedelta(days=20)
        
        found_dates = []
        
        # 30일간 순회하며 조건 맞는 날 찾기
        curr = start_date
        while curr <= end_date:
            day_info = calculate_day_gan(curr)
            day_elem = map_elem(day_info['element'])
            rel = get_relationship(my_elem, day_elem)
            
            # 목적과 관계가 일치하면 후보에 추가
            if rel == selected_goal_key:
                # 점수 계산 (기준일과 가까울수록 가산점)
                dist = abs((curr - target_date).days)
                # 별점 로직: 거리가 가까우면 5점, 멀면 4점
                stars = "⭐⭐⭐⭐⭐" if dist <= 7 else "⭐⭐⭐⭐"
                found_dates.append({
                    "date": curr,
                    "star": stars,
                    "dist": dist
                })
            curr += timedelta(days=1)
            
        # 거리순 정렬 후 상위 3개 추출
        found_dates.sort(key=lambda x: x['dist'])
        top_3 = found_dates[:3]
        
        if not top_3:
            st.warning("No matching dates found in this range. Try changing the target date.")
        else:
            # 카드 출력
            for idx, item in enumerate(top_3):
                d_str = item['date'].strftime('%Y-%m-%d')
                weekday = item['date'].strftime('%A')
                desc = advice_msg[selected_goal_key].get(lang, advice_msg[selected_goal_key]['en'])
                
                # 1등은 금색 테두리 효과 (CSS 클래스 활용) or 아이콘
                medal = "🥇" if idx == 0 else ("🥈" if idx == 1 else "🥉")
                
                st.markdown(f"""
                    <div class='rec-card'>
                        <div style='font-size:1.2em; color:#f472b6; margin-bottom:5px;'>{medal} Recommendation</div>
                        <div class='rec-date'>{d_str} <span style='font-size:0.7em; color:#cbd5e1;'>({weekday})</span></div>
                        <div class='rec-star'>{item['star']}</div>
                        <div class='rec-desc'>{desc}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.write("")
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:30px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;'>🖨️ Print Top 3</button></div>""", height=80)
