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
# 2. 스타일 설정 (가독성 획기적 개선)
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        
        /* 배경 설정 (어두운 오버레이 추가) */
        .stApp {
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #f8fafc;
        }

        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        
        /* 메인 타이틀 */
        .main-title {
            font-size: 2.5em; font-weight: 800; color: #f472b6; text-align: center; margin-bottom: 10px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 15px rgba(244, 114, 182, 0.8);
        }

        /* 🟢 [가독성 핵심] 입력창 컨테이너 스타일 */
        .input-container {
            background-color: rgba(15, 23, 42, 0.85); /* 아주 진한 남색 반투명 */
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #475569;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            margin-bottom: 30px;
        }

        /* 🟢 [가독성 핵심] 라벨 텍스트 강제 흰색 + 그림자 */
        .stSelectbox label p, .stDateInput label p {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.9) !important;
        }
        
        /* 드롭다운 내부 텍스트 색상 (브라우저 기본값 방지) */
        div[data-baseweb="select"] > div {
            background-color: #1e293b;
            color: white;
        }

        /* 결과 카드 스타일 */
        .rec-card {
            background: rgba(30, 41, 59, 0.95); border: 1px solid #f472b6; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; text-align: center;
            box-shadow: 0 4px 15px rgba(244, 114, 182, 0.2);
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
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 및 6개 국어 번역
# ----------------------------------------------------------------

# (1) 확장된 메뉴 리스트 (6개 국어 지원)
intent_list = [
    # 💰 Wealth (재물)
    {
        "id": "invest", "elem": "Wealth",
        "ko": "💰 투자 / 주식 / 코인", "en": "💰 Investment / Trading", "fr": "💰 Investissement", 
        "es": "💰 Inversión", "ja": "💰 投資・株", "zh": "💰 投资/股票"
    },
    {
        "id": "lottery", "elem": "Wealth",
        "ko": "🎰 로또 / 복권 구매", "en": "🎰 Lottery / Ticket", "fr": "🎰 Loterie", 
        "es": "🎰 Lotería", "ja": "🎰 宝くじ", "zh": "🎰 彩票"
    },
    {
        "id": "shop", "elem": "Wealth",
        "ko": "🛍️ 명품 구매 / 쇼핑", "en": "🛍️ Luxury Shopping", "fr": "🛍️ Shopping de luxe", 
        "es": "🛍️ Compras de lujo", "ja": "🛍️ 高級品の購入", "zh": "🛍️ 购物/奢侈品"
    },
    
    # 🎨 Output (표현/연애)
    {
        "id": "date", "elem": "Output",
        "ko": "💘 데이트 / 고백", "en": "💘 Date / Confession", "fr": "💘 Rendez-vous / Aveu", 
        "es": "💘 Cita / Confesión", "ja": "💘 デート・告白", "zh": "💘 约会/表白"
    },
    {
        "id": "propose", "elem": "Output",
        "ko": "💍 프러포즈 / 약혼", "en": "💍 Propose / Engagement", "fr": "💍 Demande en mariage", 
        "es": "💍 Propuesta / Compromiso", "ja": "💍 プロポーズ", "zh": "💍 求婚/订婚"
    },
    {
        "id": "create", "elem": "Output",
        "ko": "🎨 창작 / 발표 / 기획", "en": "🎨 Creative Work / Pres.", "fr": "🎨 Création / Prés.", 
        "es": "🎨 Trabajo creativo", "ja": "🎨 創作・発表", "zh": "🎨 创作/发表"
    },
    
    # 📚 Resource (문서/계약/안정)
    {
        "id": "contract", "elem": "Resource",
        "ko": "📝 중요 계약 체결", "en": "📝 Important Contract", "fr": "📝 Contrat important", 
        "es": "📝 Contrato importante", "ja": "📝 重要な契約", "zh": "📝 重要合同"
    },
    {
        "id": "wedding", "elem": "Resource",
        "ko": "👰 결혼식 / 상견례", "en": "👰 Wedding / Meeting", "fr": "👰 Mariage", 
        "es": "👰 Boda", "ja": "👰 結婚式", "zh": "👰 婚礼"
    },
    {
        "id": "move", "elem": "Resource",
        "ko": "🚚 이사 / 입주", "en": "🚚 Moving House", "fr": "🚚 Déménagement", 
        "es": "🚚 Mudanza", "ja": "🚚 引越し", "zh": "🚚 搬家"
    },
    {
        "id": "study", "elem": "Resource",
        "ko": "📚 공부 / 입학 / 등록", "en": "📚 Study / Registration", "fr": "📚 Études / Inscription", 
        "es": "📚 Estudio / Inscripción", "ja": "📚 勉強・入学", "zh": "📚 学习/注册"
    },
    
    # ⚖️ Power (명예/승진)
    {
        "id": "interview", "elem": "Power",
        "ko": "⚖️ 면접 / 오디션", "en": "⚖️ Interview / Audition", "fr": "⚖️ Entretien", 
        "es": "⚖️ Entrevista", "ja": "⚖️ 面接", "zh": "⚖️ 面试"
    },
    {
        "id": "exam", "elem": "Power",
        "ko": "💯 시험 응시 / 자격증", "en": "💯 Exam / Certification", "fr": "💯 Examen", 
        "es": "💯 Examen", "ja": "💯 試験", "zh": "💯 考试"
    },
    {
        "id": "promo", "elem": "Power",
        "ko": "🏆 승진 / 취임", "en": "🏆 Promotion", "fr": "🏆 Promotion", 
        "es": "🏆 Promoción", "ja": "🏆 昇進", "zh": "🏆 晋升"
    },

    # 🤝 Same (친목)
    {
        "id": "social", "elem": "Same",
        "ko": "🤝 파티 / 모임 / 동창회", "en": "🤝 Party / Gathering", "fr": "🤝 Fête / Réunion", 
        "es": "🤝 Fiesta / Reunión", "ja": "🤝 パーティー・集まり", "zh": "🤝 聚会/派对"
    },
]

# (2) 결과 조언 멘트 (6개 국어)
advice_msg = {
    "Wealth": {
        "ko": "재물운이 아주 강한 날입니다! 투자를 결정하거나, 복권을 사거나, 큰 쇼핑을 하기에 최적의 타이밍입니다.",
        "en": "Strong financial energy! Best day for investments, lottery tickets, or major purchases.",
        "fr": "Forte énergie financière ! Idéal pour investir ou acheter.",
        "es": "¡Fuerte energía financiera! Ideal para invertir o comprar.",
        "ja": "金運がとても強い日です！投資や買い物、宝くじに最適です。",
        "zh": "财运亨通的一天！非常适合投资、买彩票或购物。"
    },
    "Output": {
        "ko": "당신의 매력이 빛나는 날입니다. 데이트를 하거나, 고백을 하거나, 창의적인 영감을 펼치세요.",
        "en": "Your charm shines today. Perfect for dating, confessing love, or creative activities.",
        "fr": "Votre charme opère. Parfait pour les rendez-vous ou la création.",
        "es": "Tu encanto brilla. Perfecto para citas o creatividad.",
        "ja": "あなたの魅力が輝く日です。デートや告白、創作活動に最適です。",
        "zh": "你的魅力四射。非常适合约会、表白或发挥创意。"
    },
    "Resource": {
        "ko": "안정적인 기운이 당신을 돕습니다. 계약서에 도장을 찍거나, 결혼, 이사, 공부를 시작하기에 완벽합니다.",
        "en": "Stable energy supports you. Perfect for signing contracts, weddings, moving, or studying.",
        "fr": "Énergie stable. Idéal pour les contrats, mariages ou déménagements.",
        "es": "Energía estable. Ideal para contratos, bodas o mudanzas.",
        "ja": "安定した運気が助けてくれます。契約、結婚、引越しに最適な日です。",
        "zh": "稳定的气场助你一臂之力。非常适合签约、结婚、搬家或学习。"
    },
    "Power": {
        "ko": "명예와 합격운이 따르는 날입니다. 면접을 보거나, 시험을 치거나, 승진 기회를 잡으세요.",
        "en": "Day of honor and success. Great for interviews, exams, or career advancement.",
        "fr": "Jour d'honneur. Idéal pour les entretiens ou examens.",
        "es": "Día de honor. Ideal para entrevistas o exámenes.",
        "ja": "名誉と成功の日です。面接や試験、昇進に有利な日です。",
        "zh": "名誉与成功之日。非常适合面试、考试或晋升。"
    },
    "Same": {
        "ko": "사람들과의 관계가 좋아지는 날입니다. 친구를 만나거나 파티를 열어 인맥을 넓히세요.",
        "en": "Great day for social bonds. Meet friends, throw a party, or network.",
        "fr": "Bon pour le social. Rencontrez des amis ou faites la fête.",
        "es": "Bueno para lo social. Reúnete con amigos o haz una fiesta.",
        "ja": "対人運が良い日です。友人に会ったりパーティーを開くのに良いでしょう。",
        "zh": "社交运极佳。适合见朋友、聚会或拓展人脉。"
    }
}

# (3) UI 텍스트 (6개 국어)
ui = {
    "ko": {
        "title": "📆 나만의 길일 찾기", "sub": "결혼, 이사, 투자 등 중요한 일정을 위한 최고의 날짜 Top 3를 추천합니다.",
        "q1": "1. 어떤 중요한 일을 계획 중인가요?", "q2": "2. 언제쯤으로 원하시나요? (기준일)",
        "btn": "🏆 최고의 날짜 찾기", "res_h": "당신을 위한 최고의 길일",
        "lock_t": "🔒 VIP 리포트 잠금", "lock_m": "당신의 사주에 딱 맞는 정밀 분석 결과를 확인하세요.", "btn_buy": "잠금 해제 ($10)"
    },
    "en": {
        "title": "📆 Find Best Dates", "sub": "We recommend the Top 3 perfect dates for your important events.",
        "q1": "1. What is your goal?", "q2": "2. Around which date?",
        "btn": "🏆 Find Top 3 Dates", "res_h": "Top 3 Auspicious Dates",
        "lock_t": "🔒 Report Locked", "lock_m": "Unlock the best dates tailored to your destiny.", "btn_buy": "Unlock ($10)"
    },
    "fr": {
        "title": "📆 Meilleures Dates", "sub": "Trouvez les 3 meilleures dates pour vos événements importants.",
        "q1": "1. Quel est votre objectif ?", "q2": "2. Vers quelle date ?",
        "btn": "🏆 Trouver les dates", "res_h": "Top 3 des dates propices",
        "lock_t": "🔒 Rapport Verrouillé", "lock_m": "Débloquez les meilleures dates pour votre destin.", "btn_buy": "Débloquer (10$)"
    },
    "es": {
        "title": "📆 Mejores Fechas", "sub": "Encuentra las 3 mejores fechas para tus eventos importantes.",
        "q1": "1. ¿Cuál es tu objetivo?", "q2": "2. ¿Alrededor de qué fecha?",
        "btn": "🏆 Buscar Fechas", "res_h": "Top 3 Fechas Auspiciosas",
        "lock_t": "🔒 Informe Bloqueado", "lock_m": "Desbloquea las mejores fechas para tu destino.", "btn_buy": "Desbloquear ($10)"
    },
    "ja": {
        "title": "📆 吉日探し", "sub": "結婚、引越し、投資など、重要なイベントに最適な日付トップ3を推薦します。",
        "q1": "1. どのようなご予定ですか？", "q2": "2. いつ頃をご希望ですか？",
        "btn": "🏆 吉日を探す", "res_h": "あなただけの吉日 Top 3",
        "lock_t": "🔒 レポートはロックされています", "lock_m": "運命に合わせた詳細な吉日を確認してください。", "btn_buy": "解除する ($10)"
    },
    "zh": {
        "title": "📆 择吉日", "sub": "为您的婚礼、搬家、投资等重要事项推荐最佳日期。",
        "q1": "1. 您有什么计划？", "q2": "2. 大约在什么时候？",
        "btn": "🏆 查找吉日", "res_h": "为您推荐的吉日 Top 3",
        "lock_t": "🔒 报告已锁定", "lock_m": "解锁为您量身定制的最佳日期。", "btn_buy": "解锁 ($10)"
    }
}
t = ui.get(lang, ui['en']) # 기본값 영어

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
# 5. 사이드바 (언어 설정)
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Language: **{lang_map.get(lang, 'English')}**")
    
    st.write("Change Language:")
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
# 6. 메인 화면 구성
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first to enter your birth info.")
    st.stop()

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#cbd5e1; margin-bottom:40px; font-weight:bold;'>{t['sub']}</div>", unsafe_allow_html=True)

# 🟢 가독성을 위한 Dark Container 시작
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # 1. 목적 선택 (확장된 메뉴 + 6개 국어)
    def format_intent(option):
        # 현재 언어에 맞는 텍스트 반환, 없으면 영어
        return option.get(lang, option['en'])

    selected_intent = st.selectbox(
        t['q1'], 
        intent_list, 
        format_func=format_intent
    )
    
    # 선택된 목적의 오행(Element) 값 추출 (예: 'Wealth')
    target_element_relation = selected_intent['elem']

    # 2. 기준 날짜 선택
    target_date = st.date_input(t['q2'], min_value=date.today())
    
    st.write("")
    analyze_btn = st.button(t['btn'], type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Container 닫기

# 7. 결과 분석
if analyze_btn or st.session_state.get('date_analyzed_2'):
    st.session_state['date_analyzed_2'] = True
    
    # 내 사주 정보 계산
    my_info = calculate_day_gan(st.session_state["birth_date"])
    
    # 오행 한글/한자 -> 영문 매핑
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
        # 블러 처리된 미리보기 화면
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(10px); opacity: 0.5; pointer-events: none;'>
                <div class='rec-card'>
                    <div class='rec-date'>2025-05-01 (Friday)</div>
                    <div class='rec-star'>⭐⭐⭐⭐⭐</div>
                    <p>Perfect day for {format_intent(selected_intent)}...</p>
                </div>
                <div class='rec-card'><div class='rec-date'>2025-05-08</div></div>
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
            with c1: k_in = st.text_input("Key", type="password", label_visibility="collapsed")
            with c2: 
                if st.button("Unlock"):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_date_2"] = True
                        st.rerun()
                    else:
                        # Gumroad API Verification
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
        # 🔓 잠금 해제: 실제 분석 로직
        st.success(f"🔓 {t['res_h']}")
        
        # 탐색 범위: 기준일 전후 15일
        start_date = target_date - timedelta(days=15)
        end_date = target_date + timedelta(days=15)
        
        found_dates = []
        curr = start_date
        
        while curr <= end_date:
            day_info = calculate_day_gan(curr)
            day_elem = map_elem(day_info['element'])
            
            # 나와 그날의 관계
            rel = get_relationship(my_elem, day_elem)
            
            # 선택한 목적(Wealth 등)과 관계가 일치하면 후보 등록
            if rel == target_element_relation:
                dist = abs((curr - target_date).days)
                stars = "⭐⭐⭐⭐⭐" if dist <= 5 else ("⭐⭐⭐⭐" if dist <= 10 else "⭐⭐⭐")
                
                found_dates.append({
                    "date": curr,
                    "star": stars,
                    "dist": dist
                })
            curr += timedelta(days=1)
            
        # 거리순 정렬 후 상위 3개
        found_dates.sort(key=lambda x: x['dist'])
        top_3 = found_dates[:3]
        
        if not top_3:
            st.warning("No perfect dates found nearby. Try different dates.")
        else:
            for idx, item in enumerate(top_3):
                d_str = item['date'].strftime('%Y-%m-%d')
                weekday = item['date'].strftime('%A')
                
                # 조언 멘트 (6개 국어 지원)
                msg_dict = advice_msg.get(target_element_relation, advice_msg['Same'])
                desc_text = msg_dict.get(lang, msg_dict['en'])
                
                medal = "🥇" if idx == 0 else ("🥈" if idx == 1 else "🥉")
                
                st.markdown(f"""
                    <div class='rec-card'>
                        <div style='font-size:1.2em; color:#f472b6; margin-bottom:5px;'>{medal} Recommendation</div>
                        <div class='rec-date'>{d_str} <span style='font-size:0.7em; color:#cbd5e1;'>({weekday})</span></div>
                        <div class='rec-star'>{item['star']}</div>
                        <div class='rec-desc'>{desc_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                
        st.write("")
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:30px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;'>🖨️ Print Result</button></div>""", height=80)
