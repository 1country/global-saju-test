import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date, timedelta
import os
# utils.py 파일이 같은 폴더에 있어야 합니다.
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

# ----------------------------------------------------------------
# 2. 스타일 설정 (가독성 끝판왕 버전)
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        
        /* ✨ 배경: 웨딩/파티 테마 (이미지 유지) */
        .stApp {
            background-image: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.4)),
            url("https://images.unsplash.com/photo-1519225421980-715cb0215aed?q=80&w=2070&auto=format&fit=crop");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #f8fafc;
        }

        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        
        /* 메인 타이틀 */
        .main-title {
            font-size: 3.5em; font-weight: 800; color: #fce7f3; text-align: center; margin-bottom: 20px;
            font-family: 'Gowun Batang', serif; 
            /* 타이틀에도 진한 그림자 */
            text-shadow: 2px 2px 4px #000000;
        }
        .sub-title {
            text-align: center; color: #fff; font-size: 1.5em; margin-bottom: 40px; font-weight: bold;
            text-shadow: 2px 2px 4px #000000;
        }

        /* 🚨 [최종 수정] 라벨(질문) 글씨만 정확히 타격 🚨 */
        /* label 태그와 그 안의 p 태그, div 태그를 모두 강제 변환 */
        .stSelectbox label, .stDateInput label, div[data-testid="stWidgetLabel"] p {
            color: #ffffff !important;          /* 1. 무조건 흰색 */
            font-size: 22px !important;         /* 2. 글자 크기 아주 크게 */
            font-weight: 900 !important;        /* 3. 아주 두껍게 */
            
            /* 4. 글자 외곽선(Stroke) 효과 - 검은색 그림자를 4방향으로 줘서 테두리처럼 보이게 함 */
            text-shadow: 
                -1px -1px 0 #000,  
                 1px -1px 0 #000,
                -1px  1px 0 #000,
                 1px  1px 0 #000,
                 2px  2px 4px rgba(0,0,0,0.8) !important;
            
            background-color: transparent !important; /* 배경색 없음 (글자만 둥둥 뜨게) */
            margin-bottom: 8px !important;
        }
        
        /* 입력창 박스 디자인 (글자가 아니라 박스) */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"], 
        div[data-baseweb="base-input"] {
            background-color: rgba(255, 255, 255, 0.95) !important; /* 흰색 배경 */
            color: #000000 !important; /* 입력되는 글자는 검정 */
            font-size: 18px !important;
            border: 2px solid #f472b6 !important; /* 핑크색 테두리 */
            border-radius: 12px !important;
        }
        
        /* 버튼 스타일 */
        .stButton button {
            font-size: 20px !important;
            font-weight: bold !important;
            padding: 15px 30px !important;
            border-radius: 30px !important;
            border: 2px solid white !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* 결과 카드 스타일 */
        .rec-card {
            background: rgba(255, 255, 255, 0.95);
            border: 3px solid #f472b6; 
            padding: 25px;
            border-radius: 20px; 
            margin-bottom: 20px; 
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            color: #334155;
        }
        .rec-rank { font-size: 2em; margin-bottom:10px; display:block;}
        .rec-date { font-size: 2.2em; font-weight: 800; color: #be185d; display:block; margin-bottom: 5px;}
        .rec-star { font-size: 1.5em; color: #f59e0b; display:block;}
        
        /* 상단 조언 박스 */
        .advice-box {
            background-color: rgba(0, 0, 0, 0.8);
            border: 2px solid #f472b6;
            color: #fff;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 30px;
        }
        
        /* 잠금 오버레이 */
        .lock-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: flex; flex-direction: column;
            justify-content: center; align-items: center; text-align: center;
            border-radius: 15px; z-index: 10; padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)
# ----------------------------------------------------------------
# 3. 데이터 및 6개 국어 번역
# ----------------------------------------------------------------

intent_list = [
    # 💰 Wealth
    {"id": "invest", "elem": "Wealth", "ko": "💰 투자 / 주식 / 코인", "en": "💰 Investment / Trading", "fr": "💰 Investissement", "es": "💰 Inversión", "ja": "💰 投資・株", "zh": "💰 投资/股票"},
    {"id": "lottery", "elem": "Wealth", "ko": "🎰 로또 / 복권 구매", "en": "🎰 Lottery / Ticket", "fr": "🎰 Loterie", "es": "🎰 Lotería", "ja": "🎰 宝くじ", "zh": "🎰 彩票"},
    {"id": "shop", "elem": "Wealth", "ko": "🛍️ 명품 구매 / 쇼핑", "en": "🛍️ Luxury Shopping", "fr": "🛍️ Shopping", "es": "🛍️ Compras", "ja": "🛍️ 買い物", "zh": "🛍️ 购物"},
    # 🎨 Output
    {"id": "date", "elem": "Output", "ko": "💘 데이트 / 고백", "en": "💘 Date / Confession", "fr": "💘 Rendez-vous", "es": "💘 Cita", "ja": "💘 デート", "zh": "💘 约会"},
    {"id": "propose", "elem": "Output", "ko": "💍 프러포즈 / 약혼", "en": "💍 Propose / Engagement", "fr": "💍 Mariage", "es": "💍 Propuesta", "ja": "💍 プロポーズ", "zh": "💍 求婚"},
    {"id": "create", "elem": "Output", "ko": "🎨 창작 / 발표", "en": "🎨 Creative Work", "fr": "🎨 Création", "es": "🎨 Creatividad", "ja": "🎨 創作", "zh": "🎨 创作"},
    # 📚 Resource
    {"id": "contract", "elem": "Resource", "ko": "📝 중요 계약 체결", "en": "📝 Important Contract", "fr": "📝 Contrat", "es": "📝 Contrato", "ja": "📝 契約", "zh": "📝 合同"},
    {"id": "wedding", "elem": "Resource", "ko": "👰 결혼식 / 상견례", "en": "👰 Wedding / Meeting", "fr": "👰 Mariage", "es": "👰 Boda", "ja": "👰 結婚式", "zh": "👰 婚礼"},
    {"id": "move", "elem": "Resource", "ko": "🚚 이사 / 입주", "en": "🚚 Moving House", "fr": "🚚 Déménagement", "es": "🚚 Mudanza", "ja": "🚚 引越し", "zh": "🚚 搬家"},
    {"id": "study", "elem": "Resource", "ko": "📚 공부 / 등록", "en": "📚 Study / Registration", "fr": "📚 Études", "es": "📚 Estudio", "ja": "📚 勉強", "zh": "📚 学习"},
    # ⚖️ Power
    {"id": "interview", "elem": "Power", "ko": "⚖️ 면접 / 오디션", "en": "⚖️ Interview", "fr": "⚖️ Entretien", "es": "⚖️ Entrevista", "ja": "⚖️ 面接", "zh": "⚖️ 面试"},
    {"id": "exam", "elem": "Power", "ko": "💯 시험 / 자격증", "en": "💯 Exam", "fr": "💯 Examen", "es": "💯 Examen", "ja": "💯 試験", "zh": "💯 考试"},
    {"id": "promo", "elem": "Power", "ko": "🏆 승진 / 취임", "en": "🏆 Promotion", "fr": "🏆 Promotion", "es": "🏆 Promoción", "ja": "🏆 昇進", "zh": "🏆 晋升"},
    # 🤝 Same
    {"id": "social", "elem": "Same", "ko": "🤝 파티 / 모임", "en": "🤝 Party / Gathering", "fr": "🤝 Fête", "es": "🤝 Fiesta", "ja": "🤝 パーティー", "zh": "🤝 聚会"},
]

# 결과 조언 멘트 (상단에 한 번만 출력됨)
advice_msg = {
    "Wealth": {
        "ko": "💰 <b>재물운이 아주 강한 날입니다!</b><br>투자를 결정하거나, 복권을 사거나, 큰 쇼핑을 하기에 최적의 타이밍입니다.",
        "en": "💰 <b>Strong financial energy!</b><br>Best days for investments, lottery tickets, or major purchases.",
        "fr": "💰 <b>Forte énergie financière !</b><br>Idéal pour investir ou acheter.",
        "es": "💰 <b>¡Fuerte energía financiera!</b><br>Ideal para invertir o comprar.",
        "ja": "💰 <b>金運がとても強い日です！</b><br>投資や買い物、宝くじに最適です。",
        "zh": "💰 <b>财运亨通的一天！</b><br>非常适合投资、买彩票或购物。"
    },
    "Output": {
        "ko": "💘 <b>당신의 매력이 빛나는 날입니다.</b><br>데이트를 하거나, 고백을 하거나, 창의적인 영감을 펼치세요.",
        "en": "💘 <b>Your charm shines today.</b><br>Perfect for dating, confessing love, or creative activities.",
        "fr": "💘 <b>Votre charme opère.</b><br>Parfait pour les rendez-vous ou la création.",
        "es": "💘 <b>Tu encanto brilla.</b><br>Perfecto para citas o creatividad.",
        "ja": "💘 <b>あなたの魅力が輝く日です。</b><br>デートや告白、創作活動に最適です。",
        "zh": "💘 <b>你的魅力四射。</b><br>非常适合约会、表白或发挥创意。"
    },
    "Resource": {
        "ko": "📝 <b>안정적인 기운이 당신을 돕습니다.</b><br>계약서에 도장을 찍거나, 결혼, 이사, 공부를 시작하기에 완벽합니다.",
        "en": "📝 <b>Stable energy supports you.</b><br>Perfect for signing contracts, weddings, moving, or studying.",
        "fr": "📝 <b>Énergie stable.</b><br>Idéal pour les contrats, mariages ou déménagements.",
        "es": "📝 <b>Energía estable.</b><br>Ideal para contratos, bodas o mudanzas.",
        "ja": "📝 <b>安定した運気が助けてくれます。</b><br>契約、結婚、引越しに最適な日です。",
        "zh": "📝 <b>稳定的气场助你一臂之力。</b><br>非常适合签约、结婚、搬家或学习。"
    },
    "Power": {
        "ko": "🏆 <b>명예와 합격운이 따르는 날입니다.</b><br>면접을 보거나, 시험을 치거나, 승진 기회를 잡으세요.",
        "en": "🏆 <b>Day of honor and success.</b><br>Great for interviews, exams, or career advancement.",
        "fr": "🏆 <b>Jour d'honneur.</b><br>Idéal pour les entretiens ou examens.",
        "es": "🏆 <b>Día de honor.</b><br>Ideal para entrevistas o exámenes.",
        "ja": "🏆 <b>名誉と成功の日です。</b><br>面接や試験、昇進に有利な日です。",
        "zh": "🏆 <b>名誉与成功之日。</b><br>非常适合面试、考试或晋升。"
    },
    "Same": {
        "ko": "🤝 <b>사람들과의 관계가 좋아지는 날입니다.</b><br>친구를 만나거나 파티를 열어 인맥을 넓히세요.",
        "en": "🤝 <b>Great day for social bonds.</b><br>Meet friends, throw a party, or network.",
        "fr": "🤝 <b>Bon pour le social.</b><br>Rencontrez des amis ou faites la fête.",
        "es": "🤝 <b>Bueno para lo social.</b><br>Reúnete con amigos o haz una fiesta.",
        "ja": "🤝 <b>対人運が良い日です。</b><br>友人に会ったりパーティーを開くのに良いでしょう。",
        "zh": "🤝 <b>社交运极佳。</b><br>适合见朋友、聚会或拓展人脉。"
    }
}

ui = {
    "ko": {
        "title": "📆 나만의 길일 찾기", 
        "sub": "결혼, 이사, 투자 등 중요한 일정을 위한 최고의 날짜 Top 3를 추천합니다.",
        "q1": "1. 어떤 중요한 일을 계획 중인가요?", 
        "q2": "2. 언제쯤으로 원하시나요? (기준일)",
        "btn": "🏆 최고의 날짜 찾기", 
        "res_h": "당신을 위한 최고의 길일",
        "lock_t": "🔒 VIP 리포트 잠금", 
        "lock_m": "당신의 사주에 딱 맞는 정밀 분석 결과를 확인하세요.", 
        "btn_buy": "잠금 해제 ($3)"
    },
    "en": {
        "title": "📆 Find Best Dates", 
        "sub": "We recommend the Top 3 perfect dates for your important events.",
        "q1": "1. What is your goal?", 
        "q2": "2. Around which date?",
        "btn": "🏆 Find Top 3 Dates", 
        "res_h": "Top 3 Auspicious Dates",
        "lock_t": "🔒 VIP Report Locked", 
        "lock_m": "Unlock the precise analysis tailored to your destiny.", 
        "btn_buy": "Unlock ($3)"
    },
    "fr": {
        "title": "📆 Meilleures Dates", 
        "sub": "Trouvez les 3 meilleures dates pour vos événements importants.",
        "q1": "1. Quel est votre objectif ?", 
        "q2": "2. Vers quelle date ?",
        "btn": "🏆 Trouver les dates", 
        "res_h": "Top 3 des dates propices",
        "lock_t": "🔒 Rapport VIP Verrouillé", 
        "lock_m": "Débloquez l'analyse précise adaptée à votre destin.", 
        "btn_buy": "Débloquer (3$)"
    },
    "es": {
        "title": "📆 Mejores Fechas", 
        "sub": "Encuentra las 3 mejores fechas para tus eventos importantes.",
        "q1": "1. ¿Cuál es tu objetivo?", 
        "q2": "2. ¿Alrededor de qué fecha?",
        "btn": "🏆 Buscar Fechas", 
        "res_h": "Top 3 Fechas Auspiciosas",
        "lock_t": "🔒 Informe VIP Bloqueado", 
        "lock_m": "Desbloquee el análisis preciso adaptado a su destino.", 
        "btn_buy": "Desbloquear ($3)"
    },
    "ja": {
        "title": "📆 吉日探し", 
        "sub": "結婚、引越し、投資など、重要なイベントに最適な日付トップ3を推薦します。",
        "q1": "1. どのようなご予定ですか？", 
        "q2": "2. いつ頃をご希望ですか？",
        "btn": "🏆 吉日を探す", 
        "res_h": "あなただけの吉日 Top 3",
        "lock_t": "🔒 VIPレポート ロック中", 
        "lock_m": "あなたの運勢に合わせた精密な分析結果をご覧ください。", 
        "btn_buy": "解除する ($3)"
    },
    "zh": {
        "title": "📆 择吉日", 
        "sub": "为您的婚礼、搬家、投资等重要事项推荐最佳日期。",
        "q1": "1. 您有什么计划？", 
        "q2": "2. 大约在什么时候？",
        "btn": "🏆 查找吉日", 
        "res_h": "为您推荐的吉日 Top 3",
        "lock_t": "🔒 VIP报告已锁定", 
        "lock_m": "查看为您运势量身定制的精准分析结果。", 
        "btn_buy": "解锁 ($3)"
    }
}
# Fallback logic for other languages
current_ui = ui.get(lang, ui['en'])

# ----------------------------------------------------------------
# 4. 로직 함수
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

# ----------------------------------------------------------------
# 5. 사이드바
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Language: **{lang_map.get(lang, 'English')}**")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("🇺🇸 EN"): st.session_state['lang']='en'; st.rerun()
    if c2.button("🇰🇷 KO"): st.session_state['lang']='ko'; st.rerun()
    if c3.button("🇫🇷 FR"): st.session_state['lang']='fr'; st.rerun()
    c4, c5, c6 = st.columns(3)
    if c4.button("🇪🇸 ES"): st.session_state['lang']='es'; st.rerun()
    if c5.button("🇯🇵 JA"): st.session_state['lang']='ja'; st.rerun()
    if c6.button("🇨🇳 ZH"): st.session_state['lang']='zh'; st.rerun()

    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 6. 메인 화면
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first to enter your birth info.")
    st.stop()

st.markdown(f"<div class='main-title'>{current_ui['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#cbd5e1; margin-bottom:40px; font-weight:bold;'>{current_ui['sub']}</div>", unsafe_allow_html=True)

# 입력 컨테이너
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    def format_intent(option):
        return option.get(lang, option['en'])

    selected_intent = st.selectbox(current_ui['q1'], intent_list, format_func=format_intent)
    target_element_relation = selected_intent['elem']

    target_date = st.date_input(current_ui['q2'], min_value=date.today())
    
    st.write("")
    analyze_btn = st.button(current_ui['btn'], type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 7. 결과 분석
if analyze_btn or st.session_state.get('date_analyzed_2'):
    st.session_state['date_analyzed_2'] = True
    
    my_info = calculate_day_gan(st.session_state["birth_date"])
    
    def map_elem(input_val):
        valid_english = ["Wood", "Fire", "Earth", "Metal", "Water"]
        if input_val in valid_english: return input_val
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(input_val, 'Wood')

    my_elem = map_elem(my_info['element'])
    
    st.divider()
    
    # 잠금 로직
    if "unlocked_date_2" not in st.session_state: st.session_state["unlocked_date_2"] = False
    
    if not st.session_state["unlocked_date_2"]:
        # 블러 처리된 미리보기 (심플 버전으로 변경)
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(10px); opacity: 0.5; pointer-events: none;'>
                <div class='advice-box'>
                    💰 Best days for Wealth...
                </div>
                <div class='rec-card'>
                    <div class='rec-rank'>🥇</div>
                    <div class='rec-date'>2025-05-01 (Fri)</div>
                    <div class='rec-star'>⭐⭐⭐⭐⭐</div>
                </div>
                <div class='rec-card'>
                    <div class='rec-rank'>🥈</div>
                    <div class='rec-date'>2025-05-08 (Thu)</div>
                    <div class='rec-star'>⭐⭐⭐⭐</div>
                </div>
            </div>
            <div class='lock-overlay'>
                <h3 style='color: #f472b6;'>{current_ui['lock_t']}</h3>
                <p style='color: #e2e8f0; margin-bottom: 20px; font-size: 1.1em;'>{current_ui['lock_m']}</p>
                <a href="{GUMROAD_LINK_SPECIFIC}" target="_blank" 
                   style="background-color: #ec4899; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; display: inline-block;">
                   {current_ui['btn_buy']}
                </a>
            </div>
        </div>
        """
        st.markdown(blur_html, unsafe_allow_html=True)
        
        with st.expander("🔑 License Key"):
            c1, c2 = st.columns([3, 1])
            with c1: k_in = st.text_input("Key", type="password", label_visibility="collapsed")
            with c2: 
                if st.button("Unlock"):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_date_2"] = True
                        st.rerun()
                    else:
                        try:
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={"product_permalink": "date_selection", "license_key": k_in}).json()
                            if r.get("success"):
                                st.session_state["unlocked_date_2"] = True
                                st.rerun()
                            else:
                                st.error("Invalid Key")
                        except: st.error("Error")
    else:
        # 🔓 잠금 해제: 실제 분석 로직 (중복 텍스트 제거 및 구조 개선)
        st.success(f"🔓 {current_ui['res_h']}")
        
        # 1. 상단에 '총평(Advice)'을 한 번만 크게 출력
        msg_dict = advice_msg.get(target_element_relation, advice_msg['Same'])
        desc_text = msg_dict.get(lang, msg_dict['en'])
        
        st.markdown(f"<div class='advice-box'>{desc_text}</div>", unsafe_allow_html=True)

        # 2. 날짜 탐색 및 리스트 출력
        start_date = target_date - timedelta(days=15)
        end_date = target_date + timedelta(days=15)
        
        found_dates = []
        curr = start_date
        while curr <= end_date:
            day_info = calculate_day_gan(curr)
            day_elem = map_elem(day_info['element'])
            rel = get_relationship(my_elem, day_elem)
            
            if rel == target_element_relation:
                dist = abs((curr - target_date).days)
                stars = "⭐⭐⭐⭐⭐" if dist <= 5 else ("⭐⭐⭐⭐" if dist <= 10 else "⭐⭐⭐")
                found_dates.append({"date": curr, "star": stars, "dist": dist})
            curr += timedelta(days=1)
            
        found_dates.sort(key=lambda x: x['dist'])
        top_3 = found_dates[:3]
        
        if not top_3:
            st.warning("No perfect dates found nearby.")
        else:
            for idx, item in enumerate(top_3):
                d_str = item['date'].strftime('%Y-%m-%d')
                weekday = item['date'].strftime('%A')
                medal = "🥇" if idx == 0 else ("🥈" if idx == 1 else "🥉")
                
                # 심플한 카드 (설명 텍스트 제거)
                st.markdown(f"""
                    <div class='rec-card'>
                        <div class='rec-rank'>{medal}</div>
                        <div class='rec-date'>{d_str} <span style='font-size:0.7em; color:#94a3b8;'>({weekday})</span></div>
                        <div class='rec-star'>{item['star']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
        st.write("")
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:30px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;'>🖨️ Print Result</button></div>""", height=80)
