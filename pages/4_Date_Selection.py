import streamlit as st
import streamlit.components.v1 as components
import requests
import calendar
from datetime import date, timedelta
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 및 환경 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Date Selection | The Element", page_icon="📆", layout="wide")

# 언어 설정
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

# 🔑 [마스터 키 & 구매 링크]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/date_selection" # (가상의 링크, 필요시 수정)
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정 (다크 테마 + 프린트 최적화)
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
        
        /* 캘린더 카드 스타일 */
        .date-card {
            background: rgba(30, 41, 59, 0.95); border: 1px solid #475569; padding: 20px;
            border-radius: 12px; margin-bottom: 15px;
        }
        .date-badge {
            display: inline-block; padding: 5px 12px; border-radius: 20px; 
            font-weight: bold; font-size: 0.9em; margin-bottom: 5px; color: white;
        }
        
        /* 잠금 오버레이 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #f472b6;
            box-shadow: 0 0 20px rgba(244, 114, 182, 0.3);
        }

        /* 🖨️ 프린트 설정 */
        @media print {
            section[data-testid="stSidebar"], header, footer { display: none !important; }
            .stApp { background: white !important; color: black !important; }
            .date-card { background: white !important; border: 1px solid #ccc !important; color: black !important; }
            h1, h2, h3, p, div { color: black !important; text-shadow: none !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 및 로직 (오행 관계 계산)
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

# 6개 국어 해석 데이터
meanings = {
    "Wealth": {
        "bg": "#059669", # Green
        "ko": {"t": "💰 재물운 (결과/수확)", "d": "돈이 들어오거나, 쇼핑, 투자, 중요한 결과를 맺기 좋은 날입니다."},
        "en": {"t": "💰 Wealth Day", "d": "Best for income, shopping, investments, and getting results."},
        "fr": {"t": "💰 Jour de Richesse", "d": "Idéal pour les revenus, le shopping et les investissements."},
        "es": {"t": "💰 Día de Riqueza", "d": "Mejor para ingresos, compras e inversiones."},
        "ja": {"t": "💰 財運の日", "d": "収入、買い物、投資、結果を出すのに最適な日です。"},
        "zh": {"t": "💰 财运日", "d": "适合收入、购物、投资和取得成果的日子。"}
    },
    "Power": {
        "bg": "#2563eb", # Blue
        "ko": {"t": "⚖️ 명예운 (관운/승진)", "d": "면접, 승진 시험, 관공서 업무, 리더십을 발휘하기 좋은 날입니다."},
        "en": {"t": "⚖️ Power/Career Day", "d": "Best for interviews, promotions, official tasks, and leadership."},
        "fr": {"t": "⚖️ Jour de Pouvoir", "d": "Idéal pour les entretiens, promotions et tâches officielles."},
        "es": {"t": "⚖️ Día de Poder", "d": "Mejor para entrevistas, ascensos y asuntos oficiales."},
        "ja": {"t": "⚖️ 名誉の日", "d": "面接、昇進、役所の仕事、リーダーシップを発揮するのに良い日です。"},
        "zh": {"t": "⚖️ 官运日", "d": "适合面试、晋升、公务处理和发挥领导力的日子。"}
    },
    "Output": {
        "bg": "#db2777", # Pink
        "ko": {"t": "🎨 표현운 (매력/연애)", "d": "데이트, 고백, 발표, 창의적인 활동을 하기에 최고의 날입니다."},
        "en": {"t": "🎨 Output/Creativity Day", "d": "Best for dating, confessions, presentations, and creativity."},
        "fr": {"t": "🎨 Jour d'Expression", "d": "Idéal pour les rendez-vous, l'art et les présentations."},
        "es": {"t": "🎨 Día de Expresión", "d": "Mejor para citas, arte y presentaciones."},
        "ja": {"t": "🎨 表現の日", "d": "デート、告白、発表、創造的な活動に最高の日です。"},
        "zh": {"t": "🎨 表现日", "d": "最适合约会、表白、演讲和创意活动的日子。"}
    },
    "Resource": {
        "bg": "#d97706", # Amber
        "ko": {"t": "📚 문서운 (계약/공부)", "d": "계약서 작성, 공부, 힐링, 윗사람의 도움을 받기 좋은 날입니다."},
        "en": {"t": "📚 Resource/Study Day", "d": "Best for contracts, studying, healing, and getting help."},
        "fr": {"t": "📚 Jour de Ressources", "d": "Idéal pour les contrats, l'étude et le repos."},
        "es": {"t": "📚 Día de Recursos", "d": "Mejor para contratos, estudios y descanso."},
        "ja": {"t": "📚 知恵の日", "d": "契約、勉強、癒し、目上の人の助けを得るのに良い日です。"},
        "zh": {"t": "📚 印星日", "d": "适合签合同、学习、疗愈和获得长辈帮助的日子。"}
    },
    "Same": {
        "bg": "#475569", # Slate
        "ko": {"t": "🤝 사람운 (친구/경쟁)", "d": "친구를 만나거나 협업하기 좋지만, 돈 거래는 피해야 하는 날입니다."},
        "en": {"t": "🤝 Social Day", "d": "Good for networking and friends, but avoid lending money."},
        "fr": {"t": "🤝 Jour Social", "d": "Bon pour le réseautage, évitez de prêter de l'argent."},
        "es": {"t": "🤝 Día Social", "d": "Bueno para networking, evita prestar dinero."},
        "ja": {"t": "🤝 社交の日", "d": "友人との会合や協力には良いですが、お金の貸し借りは避けましょう。"},
        "zh": {"t": "🤝 社交日", "d": "适合聚会和合作，但要避免借钱。"}
    }
}

# ----------------------------------------------------------------
# 4. 사이드바 (언어 설정 - 통일)
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
# 5. 메인 로직
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    st.stop()

# UI 텍스트 (6개 국어)
ui = {
    "ko": {
        "title": "📆 길일 택일 (Date Selection)", "sub": "결혼, 이사, 계약 등 중요한 일정을 잡기에 가장 좋은 날을 찾아드립니다.",
        "sel_date": "원하는 시기 선택 (년/월)", "btn_anal": "캘린더 생성하기",
        "lock_title": "🔒 택일 리포트 잠금 (VIP)", "lock_msg": "이번 달의 재물운, 연애운, 계약운 날짜를 모두 확인하세요.",
        "btn_buy": "전체 리포트 해제 ($10)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "legend": "범례 (Legend)"
    },
    "en": {
        "title": "📆 Date Selection", "sub": "Find the most auspicious dates for marriage, moving, signing contracts, etc.",
        "sel_date": "Select Month (Year/Month)", "btn_anal": "Generate Calendar",
        "lock_title": "🔒 Calendar Locked (VIP)", "lock_msg": "Unlock full calendar with Wealth, Love, and Career dates.",
        "btn_buy": "Unlock Report ($10)", "btn_unlock": "Unlock", "key_label": "License Key",
        "legend": "Legend"
    },
    "fr": {"title": "📆 Sélection de Date", "sub": "Trouvez les meilleurs jours.", "sel_date": "Sélectionner Mois", "btn_anal": "Générer", "lock_title": "🔒 Calendrier VIP", "lock_msg": "Débloquez tout.", "btn_buy": "Débloquer ($10)", "btn_unlock": "Déverrouiller", "key_label": "Clé", "legend": "Légende"},
    "es": {"title": "📆 Selección de Fechas", "sub": "Encuentra los mejores días.", "sel_date": "Seleccionar Mes", "btn_anal": "Generar", "lock_title": "🔒 Calendario VIP", "lock_msg": "Desbloquear todo.", "btn_buy": "Desbloquear ($10)", "btn_unlock": "Desbloquear", "key_label": "Clave", "legend": "Leyenda"},
    "ja": {"title": "📆 択日 (吉日選び)", "sub": "結婚、引っ越し、契約に最適な日を見つけます。", "sel_date": "年月を選択", "btn_anal": "カレンダー作成", "lock_title": "🔒 VIPカレンダー", "lock_msg": "全ての吉日を解除。", "btn_buy": "解除 ($10)", "btn_unlock": "解除", "key_label": "キー", "legend": "凡例"},
    "zh": {"title": "📆 择吉日", "sub": "寻找结婚、搬家、签约的最佳日期。", "sel_date": "选择年月", "btn_anal": "生成日历", "lock_title": "🔒 VIP日历", "lock_msg": "解锁所有吉日。", "btn_buy": "解锁 ($10)", "btn_unlock": "解锁", "key_label": "密钥", "legend": "图例"}
}
if lang not in ui: t = ui['en']
else: t = ui[lang]

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#cbd5e1; margin-bottom:30px;'>{t['sub']}</div>", unsafe_allow_html=True)

# 1. 월 선택
with st.container(border=True):
    st.subheader(t['sel_date'])
    c1, c2 = st.columns(2)
    with c1:
        target_year = st.selectbox("Year", range(2024, 2031), index=1) # 2025 default
    with c2:
        target_month = st.selectbox("Month", range(1, 13), index=date.today().month - 1)
        
    analyze_btn = st.button(t['btn_anal'], type="primary", use_container_width=True)

# 2. 분석 및 결과
if analyze_btn or st.session_state.get('date_analyzed'):
    st.session_state['date_analyzed'] = True
    
    # 내 사주 정보
    my_info = calculate_day_gan(st.session_state["birth_date"])
    
    # 오행 변환 함수
    def map_elem(input_val):
        valid_english = ["Wood", "Fire", "Earth", "Metal", "Water"]
        if input_val in valid_english: return input_val
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(input_val, 'Wood')

    my_elem = map_elem(my_info['element'])
    
    st.divider()
    
    # 🔒 잠금 상태 확인
    if "unlocked_date" not in st.session_state: st.session_state["unlocked_date"] = False
    
    if not st.session_state["unlocked_date"]:
        # 블러 처리된 가짜 결과
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(10px); opacity: 0.6; pointer-events: none;'>
                <div class='date-card'><h3>💰 Wealth Day: 2025-05-01</h3><p>Excellent day for investment.</p></div>
                <div class='date-card'><h3>❤️ Love Day: 2025-05-05</h3><p>Perfect for a date.</p></div>
                <div class='date-card'><h3>📚 Study Day: 2025-05-10</h3><p>Focus on your exams.</p></div>
            </div>
            <div class='lock-overlay'>
                <h3 style='color: #f472b6;'>{t['lock_title']}</h3>
                <p style='color: #e2e8f0; margin-bottom: 20px; font-size: 1.1em;'>{t['lock_msg']}</p>
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
                if st.button(t['btn_unlock']):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_date"] = True
                        st.success("Unlocked!")
                        st.rerun()
                    else:
                        try:
                            # 1. 단품 확인
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={"product_permalink": "date_selection", "license_key": k_in}).json()
                            if r.get("success"):
                                st.session_state["unlocked_date"] = True
                                st.rerun()
                            else:
                                # 2. 올패스 확인
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={"product_permalink": "all-access_pass", "license_key": k_in}).json()
                                if r2.get("success"):
                                    st.session_state["unlocked_date"] = True
                                    st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: st.error("Error")
    else:
        # 🔓 해제됨: 진짜 캘린더 생성
        st.success("🔓 VIP Calendar Unlocked!")
        
        # 월별 날짜 순회
        _, last_day = calendar.monthrange(target_year, target_month)
        
        # 결과를 저장할 딕셔너리
        categorized_days = {"Wealth": [], "Power": [], "Output": [], "Resource": [], "Same": []}
        
        for day in range(1, last_day + 1):
            curr_date = date(target_year, target_month, day)
            day_info = calculate_day_gan(curr_date)
            day_elem = map_elem(day_info['element'])
            
            rel = get_relationship(my_elem, day_elem)
            categorized_days[rel].append(curr_date)

        # 결과 출력 (탭으로 구성)
        tabs = st.tabs([
            meanings["Wealth"][lang]["t"], 
            meanings["Output"][lang]["t"], 
            meanings["Power"][lang]["t"], 
            meanings["Resource"][lang]["t"]
        ])
        
        # 1. 재물운 탭
        with tabs[0]:
            info = meanings["Wealth"][lang]
            st.info(info["d"])
            if not categorized_days["Wealth"]:
                st.write("No specific dates found this month.")
            for d in categorized_days["Wealth"]:
                st.markdown(f"""
                    <div class='date-card'>
                        <span class='date-badge' style='background:{meanings['Wealth']['bg']}'>Wealth</span>
                        <span style='font-size:1.2em; font-weight:bold; color:#f8fafc; margin-left:10px;'>
                            {d.strftime('%Y-%m-%d')} ({d.strftime('%A')})
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        # 2. 표현/연애운 탭
        with tabs[1]:
            info = meanings["Output"][lang]
            st.info(info["d"])
            if not categorized_days["Output"]:
                st.write("No specific dates found this month.")
            for d in categorized_days["Output"]:
                st.markdown(f"""
                    <div class='date-card'>
                        <span class='date-badge' style='background:{meanings['Output']['bg']}'>Love & Creativity</span>
                        <span style='font-size:1.2em; font-weight:bold; color:#f8fafc; margin-left:10px;'>
                            {d.strftime('%Y-%m-%d')} ({d.strftime('%A')})
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        # 3. 명예/직장운 탭
        with tabs[2]:
            info = meanings["Power"][lang]
            st.info(info["d"])
            if not categorized_days["Power"]:
                st.write("No specific dates found this month.")
            for d in categorized_days["Power"]:
                st.markdown(f"""
                    <div class='date-card'>
                        <span class='date-badge' style='background:{meanings['Power']['bg']}'>Career & Honor</span>
                        <span style='font-size:1.2em; font-weight:bold; color:#f8fafc; margin-left:10px;'>
                            {d.strftime('%Y-%m-%d')} ({d.strftime('%A')})
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        # 4. 문서/공부운 탭
        with tabs[3]:
            info = meanings["Resource"][lang]
            st.info(info["d"])
            if not categorized_days["Resource"]:
                st.write("No specific dates found this month.")
            for d in categorized_days["Resource"]:
                st.markdown(f"""
                    <div class='date-card'>
                        <span class='date-badge' style='background:{meanings['Resource']['bg']}'>Study & Contract</span>
                        <span style='font-size:1.2em; font-weight:bold; color:#f8fafc; margin-left:10px;'>
                            {d.strftime('%Y-%m-%d')} ({d.strftime('%A')})
                        </span>
                    </div>
                """, unsafe_allow_html=True)
        
        st.write("")
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:30px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;'>🖨️ Save Calendar</button></div>""", height=80)
