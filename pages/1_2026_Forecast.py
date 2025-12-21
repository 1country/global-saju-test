import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import os
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 및 환경 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="2026 Forecast | The Element", page_icon="🔮", layout="wide")

# [핵심 변경] 언어 설정 로직 개선
# 1. 세션 상태에 'lang'이 없으면 -> 환경변수(기본값)를 가져옴
# 2. 세션 상태에 'lang'이 있으면 -> 사용자가 선택한 언어를 유지함
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')

lang = st.session_state['lang'] # 이제 코드 전체에서 이 변수를 사용

# 🔑 [마스터 키 & 구매 링크 설정]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/2026_forecast"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"
# ----------------------------------------------------------------
# 2. 스타일 설정 (이 부분만 교체하세요!)
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        
        /* 메인 배경 */
        .stApp {
            background-image: linear-gradient(rgba(20, 30, 48, 0.9), rgba(36, 59, 85, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #e2e8f0;
        }
        
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        [data-testid="stSidebarNav"] span { font-size: 1.1rem !important; font-weight: 600 !important; color: #e2e8f0 !important; }
        
        /* 제목 및 카드 스타일 */
        .year-title {
            font-size: 2.5em; font-weight: 800; color: #fbbf24; text-align: center; margin-bottom: 10px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
        }
        .card {
            background: rgba(30, 41, 59, 0.8); border: 1px solid #475569; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; color: #e2e8f0;
        }
        
        /* ⭐ [핵심 수정] 표(Table) 가독성 해결 코드 추가 ⭐ */
        div[data-testid="stTable"] {
            background-color: rgba(30, 41, 59, 0.6) !important; /* 표 배경을 반투명 검정으로 */
            border-radius: 10px;
            padding: 10px;
            overflow: hidden;
        }
        div[data-testid="stTable"] table {
            color: #ffffff !important; /* 글씨를 무조건 흰색으로 */
        }
        div[data-testid="stTable"] th {
            color: #93c5fd !important; /* 헤더는 밝은 파란색 */
            font-size: 1.1em !important;
            border-bottom: 1px solid #475569 !important;
        }
        div[data-testid="stTable"] td {
            color: #e2e8f0 !important; /* 내용은 밝은 회색 */
            font-size: 1.0em !important;
        }
        
        /* 잠금 화면 스타일 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.85); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #fbbf24;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 및 함수 정의
# ----------------------------------------------------------------

def get_interpretation(element, lang):
    # 6개 국어 데이터베이스
    data = {
        "Wood": {
            "ko": "당신은 '나무(Wood)'입니다. 성장을 지향하며 창의적이고 인자한 성품을 가졌습니다.",
            "en": "You are 'Wood'. You are growth-oriented, creative, and benevolent.",
            "fr": "Vous êtes le 'Bois'. Vous visez la croissance, êtes créatif et bienveillant.",
            "es": "Eres 'Madera'. Buscas el crecimiento, eres creativo y benevolente.",
            "ja": "あなたは「木」です。成長を志向し、創造的で慈悲深い性格です。",
            "zh": "你是‘木’。向往成长，富有创造力且仁慈。"
        },
        "Fire": {
            "ko": "당신은 '불(Fire)'입니다. 열정적이고 예의가 바르며 표현력이 뛰어납니다.",
            "en": "You are 'Fire'. You are passionate, polite, and expressive.",
            "fr": "Vous êtes le 'Feu'. Vous êtes passionné, poli et expressif.",
            "es": "Eres 'Fuego'. Eres apasionado, educado y expresivo.",
            "ja": "あなたは「火」です。情熱的で礼儀正しく、表現力が豊かです。",
            "zh": "你是‘火’。热情、有礼貌且富有表现力。"
        },
        "Earth": {
            "ko": "당신은 '흙(Earth)'입니다. 신용을 중시하며 포용력이 있고 묵직합니다.",
            "en": "You are 'Earth'. You value trust, are inclusive, and reliable.",
            "fr": "Vous êtes la 'Terre'. Vous valorisez la confiance, êtes inclusif et fiable.",
            "es": "Eres 'Tierra'. Valoras la confianza, eres inclusivo y confiable.",
            "ja": "あなたは「土」です。信用を重んじ、包容力があり、頼りになります。",
            "zh": "你是‘土’。重视信用，具有包容力且稳重。"
        },
        "Metal": {
            "ko": "당신은 '쇠(Metal)'입니다. 결단력이 있고 의리가 있으며 냉철합니다.",
            "en": "You are 'Metal'. You are decisive, loyal, and sharp.",
            "fr": "Vous êtes le 'Métal'. Vous êtes décisif, loyal et tranchant.",
            "es": "Eres 'Metal'. Eres decidido, leal y agudo.",
            "ja": "あなたは「金」です。決断力があり、義理堅く、冷静です。",
            "zh": "你是‘金’。果断、讲义气且冷静。"
        },
        "Water": {
            "ko": "당신은 '물(Water)'입니다. 지혜롭고 유연하며 적응력이 뛰어납니다.",
            "en": "You are 'Water'. You are wise, flexible, and adaptable.",
            "fr": "Vous êtes l'Eau'. Vous êtes sage, flexible et adaptable.",
            "es": "Eres 'Agua'. Eres sabio, flexible y adaptable.",
            "ja": "あなたは「水」です。賢明で柔軟性があり、適応力に優れています。",
            "zh": "你是‘水’。智慧、灵活且适应力强。"
        }
    }

    # 해당 오행(element)의 데이터를 가져옴 (없으면 기본값 Wood)
    e_data = data.get(element, data["Wood"])
    
    # 선택된 언어(lang)의 텍스트를 반환 (해당 언어가 없으면 영어 반환)
    return e_data.get(lang, e_data['en'])

# (2) 2026년 운세 데이터 (6개 국어)
def get_forecast_data(element):
    data = {
        "Wood": {
            "ko": {"title": "🔥 재능이 불타오르는 '표현'의 해", "gen": "2026년은 당신의 잠재력이 폭발하는 시기입니다. 표현 욕구가 강해지고 말과 행동이 돈이 됩니다.", "money": "활동하는 만큼 통장이 불어납니다.", "love": "매력이 넘쳐 이성이 꼬입니다."},
            "en": {"title": "🔥 Year of Expression & Talent", "gen": "Your hidden potential explodes. Creativity peaks. Express your talents boldly.", "money": "Income grows as you move.", "love": "Irresistible charm."},
            "fr": {"title": "🔥 Année de l'Expression", "gen": "Votre potentiel caché explose. Votre créativité est à son comble.", "money": "Les revenus augmentent.", "love": "Charme irrésistible."},
            "es": {"title": "🔥 Año de Expresión", "gen": "Tu potencial oculto explota. La creatividad está en su punto máximo.", "money": "Los ingresos crecen.", "love": "Encanto irresistible."},
            "ja": {"title": "🔥 才能が燃え上がる「表現」の年", "gen": "潜在能力が爆発する時期です。表現欲求が強まります。", "money": "活動した分だけ収入が増えます。", "love": "魅力が溢れます。"},
            "zh": {"title": "🔥 才华燃烧的“表现”之年", "gen": "潜力爆发的一年。创意源源不断。", "money": "收入与活动量成正比。", "love": "魅力四射。"}
        },
        "Fire": {
            "ko": {"title": "🤝 경쟁과 도약의 '자립'의 해", "gen": "자신감이 하늘을 찌릅니다. 독립심이 강해져 창업하기 좋습니다.", "money": "들어오는 돈도 많고 나가는 돈도 많습니다.", "love": "친구 같은 연인을 만납니다."},
            "en": {"title": "🤝 Year of Self-Reliance", "gen": "Confidence skyrockets. Great year for startups.", "money": "High income, high expenses.", "love": "Friends turn into lovers."},
            "fr": {"title": "🤝 Année d'Autonomie", "gen": "La confiance monte en flèche. Excellente année pour les startups.", "money": "Revenus élevés, dépenses élevées.", "love": "Les amis deviennent des amants."},
            "es": {"title": "🤝 Año de Autosuficiencia", "gen": "La confianza se dispara. Gran año para emprendimientos.", "money": "Altos ingresos, altos gastos.", "love": "Amigos se vuelven amantes."},
            "ja": {"title": "🤝 競争と飛躍の「自立」の年", "gen": "自信が天を突きます。独立心が強まります。", "money": "入るお金も出るお金も多いです。", "love": "友人のような恋人に出会います。"},
            "zh": {"title": "🤝 竞争与飞跃的“自立”之年", "gen": "自信心爆棚。独立心增强。", "money": "进账多，开销也大。", "love": "朋友可能发展成恋人。"}
        },
        "Earth": {
            "ko": {"title": "📜 결실을 맺는 '문서'의 해", "gen": "지난 고생의 보상을 받습니다. 자격증, 부동산 등 문서운이 좋습니다.", "money": "현금보다 문서(부동산/주식)가 좋습니다.", "love": "사랑받고 보호받는 운세입니다."},
            "en": {"title": "📜 Year of Recognition", "gen": "Rewards for past efforts. Great luck with certifications or real estate.", "money": "Focus on assets like real estate.", "love": "You will be loved and cared for."},
            "fr": {"title": "📜 Année de Reconnaissance", "gen": "Récompenses pour les efforts passés. Chance avec l'immobilier.", "money": "Concentrez-vous sur les actifs.", "love": "Vous serez aimé."},
            "es": {"title": "📜 Año de Reconocimiento", "gen": "Recompensas por esfuerzos pasados. Suerte con bienes raíces.", "money": "Enfócate en activos.", "love": "Serás amado."},
            "ja": {"title": "📜 結実の「文書」の年", "gen": "過去の苦労が報われます。不動産などの文書運が良いです。", "money": "現金より文書が良いです。", "love": "愛され守られる運勢です。"},
            "zh": {"title": "📜 结出硕果的“文书”之年", "gen": "过去的辛苦得到回报。文书运极佳。", "money": "文书胜于现金。", "love": "是被爱和受保护的运势。"}
        },
        "Metal": {
            "ko": {"title": "🔨 명예를 쥐는 '승진'의 해", "gen": "어깨가 무거워지지만 자리가 높아집니다. 승진운이 강력합니다.", "money": "고정 수입이 늘어납니다.", "love": "능력 있는 이성을 만납니다."},
            "en": {"title": "🔨 Year of Honor & Authority", "gen": "Heavier responsibilities bring higher status. Promotion luck is strong.", "money": "Stable income increases.", "love": "Meet capable partners."},
            "fr": {"title": "🔨 Année d'Honneur", "gen": "Responsabilités plus lourdes, statut plus élevé.", "money": "Le revenu stable augmente.", "love": "Rencontrez des partenaires capables."},
            "es": {"title": "🔨 Año de Honor", "gen": "Mayores responsabilidades, estatus más alto.", "money": "El ingreso estable aumenta.", "love": "Conoce parejas capaces."},
            "ja": {"title": "🔨 名誉を握る「昇進」の年", "gen": "責任は重くなりますが地位は上がります。", "money": "固定収入が増えます。", "love": "能力のある異性に出会います。"},
            "zh": {"title": "🔨 掌握名誉的“晋升”之年", "gen": "虽然责任重了，但地位升高。", "money": "固定收入增加。", "love": "遇到有能力的异性。"}
        },
        "Water": {
            "ko": {"title": "💰 결과물을 사냥하는 '재물'의 해", "gen": "눈앞의 목표를 쟁취하는 해입니다. 사업 확장이나 투자에 좋습니다.", "money": "재물운 최강. 확실한 곳에 투자하세요.", "love": "매력적인 이성을 만납니다."},
            "en": {"title": "💰 Year of Wealth", "gen": "Seize your goals. Perfect time for business expansion.", "money": "Strongest wealth luck. Invest boldly.", "love": "Meet attractive partners."},
            "fr": {"title": "💰 Année de Richesse", "gen": "Saisissez vos objectifs. Moment parfait pour l'expansion.", "money": "Chance de richesse la plus forte.", "love": "Rencontrez des partenaires attrayants."},
            "es": {"title": "💰 Año de Riqueza", "gen": "Alcanza tus metas. Momento perfecto para la expansión.", "money": "La suerte de riqueza más fuerte.", "love": "Conoce parejas atractivas."},
            "ja": {"title": "💰 結果を狩る「財物」の年", "gen": "目標を勝ち取る年です。事業拡大に良いです。", "money": "財運最強。確実に投資してください。", "love": "魅力的な異性に出会います。"},
            "zh": {"title": "💰 狩猎成果的“财运”之年", "gen": "争取目标的一年。适合事业扩张。", "money": "财运最强。请果断投资。", "love": "遇到充满魅力的异性。"}
        }
    }
    e_data = data.get(element, data["Wood"]) 
    return e_data.get(lang, e_data["en"])

def get_monthly_forecast_unique(element, lang):
    # 5개 오행 x 12개월 x 6개 국어 데이터 베이스
    raw_data = {
        "Wood": [
            {
                "mon": "1월", "star": "⭐⭐",
                "ko": "지인이나 친구가 금전 부탁을 해옵니다. 냉정하게 거절하지 않으면 돈도 잃고 사람도 잃습니다.",
                "en": "People may ask for money. Refuse firmly to save both money and friends.",
                "fr": "Des proches pourraient vous demander de l'argent. Refusez fermement pour ne pas perdre votre argent et vos amis.",
                "es": "Amigos o conocidos podrían pedirte dinero. Niégate firmemente o perderás tanto el dinero como la amistad.",
                "ja": "知人や友人が金銭の頼み事をしてきます。冷静に断らなければ、お金も人も失います。",
                "zh": "熟人或朋友可能向你借钱。若不果断拒绝，恐将人财两失。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐",
                "ko": "강력한 경쟁자가 나타나 내 밥그릇을 노립니다. 감정적으로 대응하지 말고 실속만 챙기세요.",
                "en": "A strong rival appears. Focus on benefits, not emotions.",
                "fr": "Un rival puissant apparaît. Concentrez-vous sur vos intérêts, pas sur vos émotions.",
                "es": "Aparece un rival fuerte. Concéntrate en los beneficios, no en las emociones.",
                "ja": "強力なライバルが現れ、あなたの利益を狙います。感情的にならず実利を取りましょう。",
                "zh": "强劲的竞争对手出现。不要感情用事，只求实利。"
            },
            {
                "mon": "3월", "star": "⭐⭐",
                "ko": "사람들이 모이는 곳에서 말실수를 할 수 있습니다. '낮말은 새가 듣고 밤말은 쥐가 듣는다'를 명심하세요.",
                "en": "Watch your words in social gatherings. A slip of the tongue causes trouble.",
                "fr": "Surveillez vos paroles en public. Un lapsus pourrait causer des ennuis.",
                "es": "Cuida tus palabras en reuniones sociales. Un desliz verbal te causará problemas.",
                "ja": "人が集まる場所での失言に注意してください。「壁に耳あり障子に目あり」です。",
                "zh": "人多嘴杂，小心失言。切记“隔墙有耳”。"
            },
            {
                "mon": "4월", "star": "⭐⭐⭐⭐⭐",
                "ko": "뜻밖의 횡재수가 있습니다. 생각지도 못한 보너스나 공돈이 들어오니 기분 좋은 달입니다.",
                "en": "Unexpected windfall! You might receive a bonus or unexpected money.",
                "fr": "Rentrée d'argent inattendue ! Vous pourriez recevoir une prime surprise.",
                "es": "¡Ganancia inesperada! Podrías recibir un bono o dinero extra.",
                "ja": "思いがけない横財数（おうざいす）があります。予期せぬボーナスが入る嬉しい月です。",
                "zh": "有意外之财。可能会收到意想不到的奖金或钱财。"
            },
            {
                "mon": "5월", "star": "⭐⭐⭐⭐⭐",
                "ko": "머리 회전이 빨라지고 아이디어가 폭발합니다. 기획이나 창작 활동에서 최고의 성과를 냅니다.",
                "en": "Ideas flow endlessly. Best month for planning or creative work.",
                "fr": "Les idées fusent. Meilleur mois pour la planification ou la création.",
                "es": "Las ideas fluyen sin fin. El mejor mes para planificar o crear.",
                "ja": "頭の回転が速くなり、アイデアが爆発します。企画や創作活動で最高の成果を出せます。",
                "zh": "头脑灵活，灵感迸发。企划或创作活动将取得最佳成果。"
            },
            {
                "mon": "6월", "star": "⭐⭐",
                "ko": "몸이 열 개라도 모자랄 만큼 바쁩니다. 과로로 쓰러질 수 있으니 영양제를 챙겨 드세요.",
                "en": "Extremely busy. Take care of your health to avoid burnout.",
                "fr": "Extrêmement occupé. Prenez soin de votre santé pour éviter le surmenage.",
                "es": "Extremadamente ocupado. Cuida tu salud para evitar el agotamiento.",
                "ja": "体が十あっても足りないほど忙しいです。過労に注意し、栄養を摂ってください。",
                "zh": "忙得不可开交。注意劳逸结合，以免过劳。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐⭐",
                "ko": "재물 흐름이 아주 안정적입니다. 헛돈 쓰지 말고 차곡차곡 저축하기 가장 좋은 시기입니다.",
                "en": "Financial flow is stable. Best time to save money.",
                "fr": "Le flux financier est stable. Le meilleur moment pour épargner.",
                "es": "El flujo financiero es estable. El mejor momento para ahorrar dinero.",
                "ja": "財産の流れが非常に安定的です。無駄遣いせず貯蓄するのに最適な時期です。",
                "zh": "财运稳定。是储蓄的最佳时机，切勿乱花钱。"
            },
            {
                "mon": "8월", "star": "⭐⭐",
                "ko": "직장에서 스트레스가 극에 달합니다. 욱하고 사표 던지지 마세요. 참는 자에게 복이 옵니다.",
                "en": "Work stress peaks. Don't quit impulsively. Patience brings rewards.",
                "fr": "Le stress au travail culmine. Ne démissionnez pas sur un coup de tête. La patience paie.",
                "es": "El estrés laboral alcanza su punto máximo. No renuncies impulsivamente. La paciencia trae recompensas.",
                "ja": "職場のストレスが極に達します。カッとなって辞表を出さないでください。忍耐が福を呼びます。",
                "zh": "职场压力达到顶峰。千万别冲动辞职。忍一时风平浪静。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐",
                "ko": "어깨가 무거워지지만 그만큼 인정받는 시기입니다. 승진이나 리더 자리를 제안받을 수 있습니다.",
                "en": "Responsibilities grow, but so does recognition. Promotion is possible.",
                "fr": "Les responsabilités augmentent, mais la reconnaissance aussi. Une promotion est possible.",
                "es": "Crecen las responsabilidades, pero también el reconocimiento. Es posible un ascenso.",
                "ja": "責任は重くなりますが、その分認められる時期です。昇進やリーダー職の提案があるかもしれません。",
                "zh": "虽然责任重了，但也会得到认可。可能会有晋升或担任领导的机会。"
            },
            {
                "mon": "10월", "star": "⭐⭐⭐⭐⭐",
                "ko": "문서 운이 아주 좋습니다. 부동산 계약이나 중요한 도장을 찍기에 길한 달입니다.",
                "en": "Great luck with documents. Good for real estate or contracts.",
                "fr": "Grande chance avec les documents. Idéal pour l'immobilier ou les contrats.",
                "es": "Gran suerte con documentos. Bueno para bienes raíces o contratos.",
                "ja": "文書運が非常に良いです。不動産契約や重要な判子を押すのに吉な月です。",
                "zh": "文书运极佳。非常适合签订房产合同或重要文件。"
            },
            {
                "mon": "11월", "star": "⭐⭐⭐⭐",
                "ko": "꽉 막혔던 일이 귀인(윗사람)의 도움으로 시원하게 뚫립니다. 조언을 구하세요.",
                "en": "Blocked problems are solved with help from a mentor.",
                "fr": "Les problèmes bloqués sont résolus grâce à l'aide d'un mentor.",
                "es": "Los problemas bloqueados se resuelven con la ayuda de un mentor.",
                "ja": "行き詰まっていた事が、貴人（目上の人）の助けで解決します。助言を求めてください。",
                "zh": "停滞不前的事情在贵人（长辈）的帮助下迎刃而解。请多求教。"
            },
            {
                "mon": "12월", "star": "⭐⭐⭐⭐",
                "ko": "학업이나 자격증 시험에 행운이 따릅니다. 새로운 것을 배우기에 딱 좋은 연말입니다.",
                "en": "Good luck with studies or exams. Perfect time to learn.",
                "fr": "Bonne chance pour les études ou les examens. Le moment idéal pour apprendre.",
                "es": "Buena suerte con estudios o exámenes. Momento perfecto para aprender.",
                "ja": "学業や資格試験に幸運が伴います。新しいことを学ぶのに最適な年末です。",
                "zh": "学业或考证运势不错。非常适合学习新知识的年末。"
            }
        ],
        "Fire": [
            {
                "mon": "1월", "star": "⭐⭐",
                "ko": "생각이 너무 많아 머리가 아픕니다. 스트레스성 두통을 주의하고 멍 때리는 시간을 가지세요.",
                "en": "Too many thoughts cause headaches. Relax and clear your mind.",
                "fr": "Trop de pensées causent des maux de tête. Détendez-vous et videz votre esprit.",
                "es": "Demasiados pensamientos causan dolores de cabeza. Relájate y despeja tu mente.",
                "ja": "考えすぎて頭が痛くなります。ストレス性頭痛に注意し、ぼーっとする時間を持ちましょう。",
                "zh": "思虑过多导致头痛。注意压力，适当放空自己。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐⭐⭐",
                "ko": "귀인이 나타나 나를 끌어줍니다. 취업이나 합격 소식을 듣기에 아주 좋은 달입니다.",
                "en": "A noble person appears. Great month for job offers or passing exams.",
                "fr": "Une personne noble apparaît pour vous aider. Excellent mois pour l'emploi ou les examens.",
                "es": "Aparece una persona noble para ayudarte. Gran mes para ofertas de trabajo o exámenes.",
                "ja": "貴人が現れ、あなたを導いてくれます。就職や合格の知らせを聞くのに最適な月です。",
                "zh": "贵人出现提拔你。非常适合求职或通过考试的月份。"
            },
            {
                "mon": "3월", "star": "⭐⭐⭐⭐",
                "ko": "마음이 호수처럼 편안해집니다. 중요한 계약이나 약속을 잡기에 적합합니다.",
                "en": "Peace of mind returns. Suitable for important contracts.",
                "fr": "La tranquillité d'esprit revient. Propice aux contrats importants.",
                "es": "Vuelve la paz mental. Adecuado para contratos importantes.",
                "ja": "心が湖のように穏やかになります。重要な契約や約束をするのに適しています。",
                "zh": "内心平静如水。适合签订重要合同或约定。"
            },
            {
                "mon": "4월", "star": "⭐⭐⭐⭐",
                "ko": "자신감을 가지고 나를 드러내세요. 내 매력이 돈이 되고 기회가 되는 시기입니다.",
                "en": "Express yourself. Your charm turns into money and opportunities.",
                "fr": "Exprimez-vous. Votre charme se transforme en argent et en opportunités.",
                "es": "Exprésate. Tu encanto se convierte en dinero y oportunidades.",
                "ja": "自信を持って自分を表現してください。あなたの魅力がお金とチャンスになる時期です。",
                "zh": "自信地展现自己。你的魅力将转化为金钱和机会。"
            },
            {
                "mon": "5월", "star": "⭐⭐",
                "ko": "주변 사람들과 의견 충돌이 잦습니다. 이기려 하지 말고 '그럴 수도 있지' 하고 넘기세요.",
                "en": "Conflicts increase. Don't try to win every argument.",
                "fr": "Les conflits augmentent. N'essayez pas de gagner chaque dispute.",
                "es": "Aumentan los conflictos. No intentes ganar cada discusión.",
                "ja": "周囲の人と意見の衝突が増えます。勝とうとせず、「そんなこともある」と流しましょう。",
                "zh": "容易与周围人发生冲突。不要争强好胜，得过且过。"
            },
            {
                "mon": "6월", "star": "⭐⭐",
                "ko": "고집을 부리다가 다 된 밥에 재 뿌릴 수 있습니다. 동료와 협력해야만 이득을 봅니다.",
                "en": "Stubbornness leads to failure. Cooperation is the only way.",
                "fr": "L'entêtement mène à l'échec. La coopération est la seule voie.",
                "es": "La terquedad lleva al fracaso. La cooperación es el único camino.",
                "ja": "意地を張ると全てを台無しにする恐れがあります。同僚と協力してこそ利益が得られます。",
                "zh": "固执己见会坏事。只有与同事合作才能获利。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐⭐⭐",
                "ko": "말 한마디로 천 냥 빚을 갚습니다. 영업이나 미팅에서 최고의 성과를 올립니다.",
                "en": "Your words have power. Great results in sales or meetings.",
                "fr": "Vos paroles ont du pouvoir. Excellents résultats en vente ou en réunion.",
                "es": "Tus palabras tienen poder. Grandes resultados en ventas o reuniones.",
                "ja": "言葉一つで千両の借金を返せます。営業や会議で最高の成果を上げます。",
                "zh": "一言值千金。销售或会议将取得最佳成果。"
            },
            {
                "mon": "8월", "star": "⭐⭐⭐",
                "ko": "큰 돈이 들어올 기회가 보입니다. 다만, 들어온 만큼 나갈 수 있으니 지갑을 닫으세요.",
                "en": "Opportunity for big money, but expenses rise too. Manage spending.",
                "fr": "Opportunité de gros gains, mais les dépenses augmentent aussi. Gérez vos dépenses.",
                "es": "Oportunidad de mucho dinero, pero los gastos también suben. Controla tus gastos.",
                "ja": "大金が入る機会が見えます。ただ、入った分だけ出ていく可能性があるので財布の紐を締めて。",
                "zh": "有赚大钱的机会。但进多少出多少，请捂紧钱包。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐",
                "ko": "재물운이 폭발하지만 지출도 큽니다. 기분파 쇼핑을 조심해야 하는 달입니다.",
                "en": "Wealth luck explodes, but beware of emotional shopping.",
                "fr": "La chance financière explose, mais attention aux achats émotionnels.",
                "es": "La suerte financiera explota, pero cuidado con las compras emocionales.",
                "ja": "財運が爆発しますが支出も大きいです。気分による衝動買いに注意すべき月です。",
                "zh": "财运爆发，但开销也大。小心冲动购物。"
            },
            {
                "mon": "10월", "star": "⭐⭐⭐⭐⭐",
                "ko": "그동안의 노력에 대한 확실한 보상을 받습니다. 인센티브나 상을 받을 수 있습니다.",
                "en": "Sure rewards for your efforts. Expect incentives or awards.",
                "fr": "Récompenses assurées pour vos efforts. Attendez-vous à des primes ou des prix.",
                "es": "Recompensas seguras por tus esfuerzos. Espera incentivos o premios.",
                "ja": "これまでの努力に対する確実な報酬を受け取ります。インセンティブや賞をもらえるかも。",
                "zh": "过去的努力将得到切实回报。可能会获得奖金或奖项。"
            },
            {
                "mon": "11월", "star": "⭐⭐",
                "ko": "상사의 압박이나 업무량이 과도합니다. 지금은 납작 엎드려 때를 기다려야 합니다.",
                "en": "High pressure from bosses. Stay low and wait for the right time.",
                "fr": "Forte pression des patrons. Faites profil bas et attendez le bon moment.",
                "es": "Alta presión de los jefes. Mantén un perfil bajo y espera el momento adecuado.",
                "ja": "上司の圧力や業務量が過度です。今は平伏して時を待つべきです。",
                "zh": "上司施压或工作量过大。现在应低调行事，等待时机。"
            },
            {
                "mon": "12월", "star": "⭐⭐⭐⭐",
                "ko": "일은 힘들지만 명예는 올라갑니다. 사람들이 당신의 능력을 알아주기 시작합니다.",
                "en": "Hard work leads to honor. People recognize your abilities.",
                "fr": "Le travail acharné mène à l'honneur. Les gens reconnaissent vos capacités.",
                "es": "El trabajo duro lleva al honor. La gente reconoce tus habilidades.",
                "ja": "仕事は大変ですが名誉は上がります。人々があなたの能力を認め始めます。",
                "zh": "虽然工作辛苦但名誉提升。人们开始认可你的能力。"
            }
        ],
        "Earth": [
            {
                "mon": "1월", "star": "⭐⭐⭐",
                "ko": "이직이나 이사 등 이동수가 있습니다. 섣불리 움직이지 말고 신중하게 결정하세요.",
                "en": "Possibility of moving or changing jobs. Decide carefully.",
                "fr": "Possibilité de déménagement ou de changement d'emploi. Décidez avec soin.",
                "es": "Posibilidad de mudanza o cambio de trabajo. Decide con cuidado.",
                "ja": "転職や引越しなどの移動数があります。軽率に動かず慎重に決定してください。",
                "zh": "有跳槽或搬家等变动。切勿轻举妄动，需慎重决定。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐⭐⭐",
                "ko": "명예운이 상승합니다. 남들이 부러워할 만한 감투를 쓰거나 스카우트 제의가 옵니다.",
                "en": "Honor rises. You might get a prestigious title or scout offer.",
                "fr": "L'honneur monte. Vous pourriez obtenir un titre prestigieux ou une offre.",
                "es": "El honor aumenta. Podrías obtener un título prestigioso o una oferta.",
                "ja": "名誉運が上昇します。人が羨むような役職に就いたり、スカウトの話が来ます。",
                "zh": "名誉运上升。可能会获得令人羡慕的职位或被挖角。"
            },
            {
                "mon": "3월", "star": "⭐⭐⭐⭐",
                "ko": "능력을 인정받아 승진하거나 중요한 직책을 맡게 됩니다. 리더십을 발휘하세요.",
                "en": "Promotion or important role awaits. Show your leadership.",
                "fr": "Une promotion ou un rôle important vous attend. Montrez votre leadership.",
                "es": "Te espera un ascenso o un papel importante. Muestra tu liderazgo.",
                "ja": "能力が認められ昇進したり、重要な職責を任されます。リーダーシップを発揮してください。",
                "zh": "能力得到认可，有望晋升或担任要职。请发挥领导力。"
            },
            {
                "mon": "4월", "star": "⭐⭐⭐",
                "ko": "오랜만에 친구들을 만나 회포를 풉니다. 지출은 좀 있겠지만 즐거운 한 달입니다.",
                "en": "Meeting friends brings joy. Expenses rise, but it's happy.",
                "fr": "Rencontrer des amis apporte de la joie. Les dépenses augmentent, mais c'est joyeux.",
                "es": "Reunirse con amigos trae alegría. Los gastos suben, pero es feliz.",
                "ja": "久しぶりに友人と会い、旧交を温めます。出費はありますが楽しい一ヶ月です。",
                "zh": "久违地与朋友聚会叙旧。虽然有些开销，但是愉快的一个月。"
            },
            {
                "mon": "5월", "star": "⭐⭐⭐⭐",
                "ko": "집중력이 최고조에 달합니다. 미뤄뒀던 공부나 연구를 하기에 최적의 시기입니다.",
                "en": "Concentration peaks. Best time to study or research.",
                "fr": "La concentration est à son comble. Meilleur moment pour étudier ou faire des recherches.",
                "es": "La concentración está al máximo. El mejor momento para estudiar o investigar.",
                "ja": "集中力が最高潮に達します。先延ばしにしていた勉強や研究をするのに最適な時期です。",
                "zh": "注意力达到顶峰。最适合进行搁置的学习或研究。"
            },
            {
                "mon": "6월", "star": "⭐⭐⭐⭐⭐",
                "ko": "문서운이 대길합니다. 집을 사거나 중요한 계약을 하기에 더할 나위 없습니다.",
                "en": "Great document luck. Perfect for buying a house.",
                "fr": "Grande chance avec les documents. Parfait pour acheter une maison.",
                "es": "Gran suerte con documentos. Perfecto para comprar una casa.",
                "ja": "文書運が大吉です。家を買ったり重要な契約をするのに申し分ありません。",
                "zh": "文书运大吉。非常适合买房或签订重要合同。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐⭐",
                "ko": "혼자 끙끙 앓던 문제를 동료와 함께 해결합니다. 팀워크가 빛을 발합니다.",
                "en": "Solve problems with colleagues. Teamwork shines.",
                "fr": "Résolvez les problèmes avec des collègues. Le travail d'équipe brille.",
                "es": "Resuelve problemas con colegas. El trabajo en equipo brilla.",
                "ja": "一人で悩んでいた問題を同僚と共に解決します。チームワークが光を放ちます。",
                "zh": "与同事一起解决独自苦恼的问题。团队合作将大放异彩。"
            },
            {
                "mon": "8월", "star": "⭐⭐⭐⭐",
                "ko": "새로운 취미나 예술 활동을 시작해보세요. 의외의 재능을 발견하게 됩니다.",
                "en": "Start a new hobby. You might discover unexpected talents.",
                "fr": "Commencez un nouveau passe-temps. Vous pourriez découvrir des talents inattendus.",
                "es": "Empieza un nuevo pasatiempo. Podrías descubrir talentos inesperados.",
                "ja": "新しい趣味や芸術活動を始めてみてください。意外な才能を発見することになります。",
                "zh": "尝试开始新的爱好或艺术活动。会发现意想不到的才能。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐",
                "ko": "말주변이 좋아져서 어딜 가나 인기가 많습니다. 인맥을 넓히기 좋은 달입니다.",
                "en": "Eloquence improves. Good month to expand your network.",
                "fr": "L'éloquence s'améliore. Bon mois pour élargir votre réseau.",
                "es": "La elocuencia mejora. Buen mes para expandir tu red.",
                "ja": "口達者になり、どこへ行っても人気があります。人脈を広げるのに良い月です。",
                "zh": "口才变好，走到哪里都受欢迎。适合拓展人脉的月份。"
            },
            {
                "mon": "10월", "star": "⭐⭐⭐⭐",
                "ko": "생각지도 못한 용돈이나 수익이 생깁니다. 작게라도 투자를 해봐도 좋습니다.",
                "en": "Unexpected profit. Small investments are okay.",
                "fr": "Profit inattendu. Les petits investissements sont acceptables.",
                "es": "Beneficio inesperado. Las pequeñas inversiones están bien.",
                "ja": "思いがけないお小遣いや収益が生じます。小さくても投資をしてみても良いでしょう。",
                "zh": "会有意想不到的零花钱或收益。可以尝试小额投资。"
            },
            {
                "mon": "11월", "star": "⭐⭐",
                "ko": "눈앞에 큰 돈이 보이지만 욕심내면 낭패를 봅니다. 돌다리도 두들겨 보고 건너세요.",
                "en": "Big money is visible, but greed causes failure. Be cautious.",
                "fr": "De gros sous en vue, mais l'avidité mène à l'échec. Soyez prudent.",
                "es": "Se ve mucho dinero, pero la codicia lleva al fracaso. Sé cauteloso.",
                "ja": "目の前に大金が見えますが、欲を出すと失敗します。石橋を叩いて渡ってください。",
                "zh": "眼前虽有大钱，但贪心会坏事。请小心驶得万年船。"
            },
            {
                "mon": "12월", "star": "⭐⭐⭐⭐⭐",
                "ko": "사업이나 프로젝트의 결실을 맺습니다. 수금하기 좋고 통장이 두둑해집니다.",
                "en": "Reap rewards of projects. Good for collecting payments.",
                "fr": "Récoltez les fruits de vos projets. Bon pour encaisser les paiements.",
                "es": "Cosecha las recompensas de los proyectos. Bueno para cobrar pagos.",
                "ja": "事業やプロジェクトが実を結びます。集金に良く、通帳が潤います。",
                "zh": "事业或项目结出硕果。适合收款，钱包鼓鼓。"
            }
        ],
        "Metal": [
            {
                "mon": "1월", "star": "⭐⭐⭐⭐",
                "ko": "먹을 복이 터졌습니다. 재물운도 좋으니 맛있는 것을 먹으며 자신을 대접하세요.",
                "en": "Good luck with food and money. Treat yourself.",
                "fr": "Bonne chance avec la nourriture et l'argent. Faites-vous plaisir.",
                "es": "Buena suerte con la comida y el dinero. Date un capricho.",
                "ja": "食福に恵まれます。財運も良いので、美味しいものを食べて自分をもてなしてください。",
                "zh": "很有口福。财运也不错，吃点好吃的犒劳自己吧。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐",
                "ko": "요행을 바라지 마세요. 땀 흘린 만큼 정확하게 통장에 꽂히는 정직한 달입니다.",
                "en": "Don't expect luck. You earn exactly what you work for.",
                "fr": "N'attendez pas de chance. Vous gagnez exactement ce pour quoi vous travaillez.",
                "es": "No esperes suerte. Ganas exactamente lo que trabajas.",
                "ja": "僥倖（まぐれ）を望まないでください。汗を流した分だけ正確に通帳に入る正直な月です。",
                "zh": "别指望侥幸。是付出多少汗水就有多少回报的诚实月份。"
            },
            {
                "mon": "3월", "star": "⭐⭐⭐⭐⭐",
                "ko": "예상치 못한 보너스나 성과급을 받습니다. 기분 좋은 비명을 지르게 됩니다.",
                "en": "Unexpected bonus or incentive. Screaming with joy.",
                "fr": "Prime ou incitation inattendue. Crier de joie.",
                "es": "Bono o incentivo inesperado. Gritando de alegría.",
                "ja": "予期せぬボーナスや成果給を受け取ります。嬉しい悲鳴を上げることになります。",
                "zh": "收到意想不到的奖金或绩效。会高兴得尖叫。"
            },
            {
                "mon": "4월", "star": "⭐⭐",
                "ko": "문서 계약 시 꼼꼼히 확인하세요. 작은 글씨를 못 봐서 손해 볼 수 있습니다.",
                "en": "Check documents carefully. Missing fine print causes loss.",
                "fr": "Vérifiez soigneusement les documents. Manquer les petits caractères cause des pertes.",
                "es": "Revisa los documentos cuidadosamente. Perder la letra pequeña causa pérdidas.",
                "ja": "文書契約時は入念に確認してください。小さな文字を見落として損をする可能性があります。",
                "zh": "签合同要仔细确认。没看清小字可能会吃亏。"
            },
            {
                "mon": "5월", "star": "⭐⭐",
                "ko": "관재구설(법적 다툼이나 말썽)이 따를 수 있습니다. 입을 무겁게 하고 조용히 지내세요.",
                "en": "Legal issues or gossip may arise. Keep quiet.",
                "fr": "Des problèmes juridiques ou des potins peuvent survenir. Restez discret.",
                "es": "Pueden surgir problemas legales o chismes. Mantente callado.",
                "ja": "官製口舌（法的な争いやトラブル）が伴う可能性があります。口を慎んで静かに過ごしてください。",
                "zh": "可能有官司口舌。请谨言慎行。"
            },
            {
                "mon": "6월", "star": "⭐⭐",
                "ko": "직장 스트레스가 최고조입니다. '이 또한 지나가리라'는 마음으로 멘탈을 잡으세요.",
                "en": "Work stress is extreme. Keep your mental balance.",
                "fr": "Le stress au travail est extrême. Gardez votre équilibre mental.",
                "es": "El estrés laboral es extremo. Mantén tu equilibrio mental.",
                "ja": "職場のストレスが最高潮です。「これもまた過ぎ去るだろう」という気持ちでメンタルを保ってください。",
                "zh": "职场压力极大。请抱着“这一切都会过去”的心态调整心态。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐",
                "ko": "위기 상황에서 윗사람이 구원의 손길을 내밉니다. 자존심 굽히고 도움을 받으세요.",
                "en": "Superiors help in crisis. Swallow pride and accept help.",
                "fr": "Les supérieurs aident en cas de crise. Avalez votre fierté et acceptez l'aide.",
                "es": "Los superiores ayudan en la crisis. Trágate el orgullo y acepta ayuda.",
                "ja": "危機的状況で目上の人が救いの手を差し伸べます。プライドを曲げて助けを受けてください。",
                "zh": "危机时刻会有长辈伸出援手。请放下自尊接受帮助。"
            },
            {
                "mon": "8월", "star": "⭐⭐",
                "ko": "주관이 뚜렷해지는 건 좋지만, 남들이 볼 땐 똥고집입니다. 유연함이 필요합니다.",
                "en": "Strong will is good, but don't be stubborn. Be flexible.",
                "fr": "Une forte volonté est bonne, mais ne soyez pas têtu. Soyez flexible.",
                "es": "Una voluntad fuerte es buena, pero no seas terco. Sé flexible.",
                "ja": "主観がはっきりするのは良いですが、他人から見れば頑固です。柔軟性が必要です。",
                "zh": "有主见虽好，但在别人看来是固执。需要灵活变通。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐⭐",
                "ko": "누구와 붙어도 이길 수 있는 에너지가 있습니다. 경쟁이나 입찰에서 승리합니다.",
                "en": "Energy to win against anyone. Victory in competition.",
                "fr": "L'énergie pour gagner contre n'importe qui. Victoire en compétition.",
                "es": "Energía para ganar contra cualquiera. Victoria en la competencia.",
                "ja": "誰と戦っても勝てるエネルギーがあります。競争や入札で勝利します。",
                "zh": "拥有战胜任何人的能量。在竞争或投标中获胜。"
            },
            {
                "mon": "10월", "star": "⭐⭐⭐⭐⭐",
                "ko": "나를 물심양면으로 도와주는 귀인이 나타납니다. 인복이 터지는 달입니다.",
                "en": "A noble person appears. Luck with people explodes.",
                "fr": "Une personne noble apparaît. La chance avec les gens explose.",
                "es": "Aparece una persona noble. La suerte con la gente explota.",
                "ja": "あなたを物心両面で助けてくれる貴人が現れます。人徳が爆発する月です。",
                "zh": "出现物质和精神上都帮助你的贵人。人缘极佳的月份。"
            },
            {
                "mon": "11월", "star": "⭐⭐⭐⭐",
                "ko": "나의 재능을 맘껏 펼치고 박수받습니다. 무대 위 주인공이 되는 시기입니다.",
                "en": "Show off talents and get applause. You are the star.",
                "fr": "Montrez vos talents et soyez applaudi. Vous êtes la star.",
                "es": "Muestra tus talentos y recibe aplausos. Eres la estrella.",
                "ja": "自分の才能を存分に発揮して拍手喝采を浴びます。舞台の上の主人公になる時期です。",
                "zh": "尽情施展才华并获得掌声。是成为舞台主角的时期。"
            },
            {
                "mon": "12월", "star": "⭐⭐",
                "ko": "연말 모임에서 말실수로 오해를 살 수 있습니다. 술자리에서 특히 조심하세요.",
                "en": "Slip of the tongue at parties causes misunderstanding.",
                "fr": "Un lapsus lors de fêtes cause des malentendus. Attention à l'alcool.",
                "es": "Un desliz en fiestas causa malentendidos. Cuidado con el alcohol.",
                "ja": "年末の集まりで失言し誤解を招く恐れがあります。お酒の席では特に注意してください。",
                "zh": "年末聚会可能因失言造成误会。酒桌上要特别小心。"
            }
        ],
        "Water": [
            {
                "mon": "1월", "star": "⭐⭐⭐⭐⭐",
                "ko": "창의력이 화수분처럼 쏟아집니다. 예술이나 기획 분야라면 대박을 터뜨립니다.",
                "en": "Creativity flows endlessly. Success in arts or planning.",
                "fr": "La créativité coule à flots. Succès dans les arts ou la planification.",
                "es": "La creatividad fluye sin fin. Éxito en artes o planificación.",
                "ja": "創造力が湧き水のように溢れ出ます。芸術や企画分野なら大ヒットします。",
                "zh": "创造力如泉涌。若是艺术或企划领域，将大获成功。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐⭐",
                "ko": "새로운 일을 시작하거나 계획하기 딱 좋습니다. 시작이 반입니다.",
                "en": "Perfect time to start new things. Well begun is half done.",
                "fr": "Moment idéal pour commencer de nouvelles choses. Bien commencé est à moitié fait.",
                "es": "Momento perfecto para empezar cosas nuevas. Bien empezado es medio hecho.",
                "ja": "新しいことを始めたり計画するのに最適です。始めが肝心です。",
                "zh": "非常适合开始新工作或计划。好的开始是成功的一半。"
            },
            {
                "mon": "3월", "star": "⭐⭐⭐⭐",
                "ko": "아랫사람이나 자녀에게 좋은 일이 생깁니다. 덕분에 나까지 웃게 됩니다.",
                "en": "Good news for subordinates or children. It makes you smile.",
                "fr": "Bonnes nouvelles pour les subordonnés ou les enfants. Cela vous fait sourire.",
                "es": "Buenas noticias para subordinados o hijos. Te hace sonreír.",
                "ja": "目下の人や子供に良いことが起こります。おかげであなたまで笑顔になります。",
                "zh": "下属或子女会有好事发生。你也因此喜笑颜开。"
            },
            {
                "mon": "4월", "star": "⭐⭐⭐⭐",
                "ko": "직장에서 승진하거나 중요한 책임을 맡습니다. 어깨가 무겁지만 기회입니다.",
                "en": "Promotion or heavy responsibility. A burden but an opportunity.",
                "fr": "Promotion ou lourde responsabilité. Un fardeau mais une opportunité.",
                "es": "Promoción o gran responsabilidad. Una carga pero una oportunidad.",
                "ja": "職場で昇進したり重要な責任を負います。肩は重いですがチャンスです。",
                "zh": "职场晋升或承担重要责任。虽重任在肩，却是良机。"
            },
            {
                "mon": "5월", "star": "⭐⭐",
                "ko": "일확천금의 유혹이 옵니다. 투기나 도박은 패가망신의 지름길이니 절대 금지.",
                "en": "Temptation of jackpot. Gambling leads to ruin.",
                "fr": "Tentation du jackpot. Le jeu mène à la ruine.",
                "es": "Tentación del premio mayor. El juego lleva a la ruina.",
                "ja": "一攫千金の誘惑が来ます。投機やギャンブルは身の破滅への近道なので絶対禁止。",
                "zh": "有一夜暴富的诱惑。投机或赌博是败家之路，绝对禁止。"
            },
            {
                "mon": "6월", "star": "⭐⭐⭐",
                "ko": "돈은 많이 들어오는데 나갈 구멍도 많습니다. 가계부를 꼼꼼히 써야 합니다.",
                "en": "Money comes in but leaks out. Keep a strict budget.",
                "fr": "L'argent rentre mais fuit. Gardez un budget strict.",
                "es": "El dinero entra pero se escapa. Mantén un presupuesto estricto.",
                "ja": "お金はたくさん入ってきますが出る穴も多いです。家計簿をしっかりつける必要があります。",
                "zh": "进账多，花销也多。要仔细记账。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐⭐",
                "ko": "명예가 올라가고 여기저기서 나를 찾습니다. 인기 관리를 잘해야 합니다.",
                "en": "Honor rises and people seek you. Manage popularity.",
                "fr": "L'honneur monte et les gens vous cherchent. Gérez votre popularité.",
                "es": "El honor sube y la gente te busca. Gestiona tu popularidad.",
                "ja": "名誉が上がり、あちこちから声がかかります。人気管理をしっかりすべきです。",
                "zh": "名誉提升，到处都有人找。要做好人气管理。"
            },
            {
                "mon": "8월", "star": "⭐⭐⭐⭐",
                "ko": "깊이 있는 공부나 연구에 몰두하면 큰 성과를 냅니다. 전문가로 인정받습니다.",
                "en": "Focus on study brings results. Recognized as an expert.",
                "fr": "Se concentrer sur l'étude apporte des résultats. Reconnu comme expert.",
                "es": "Enfocarse en el estudio trae resultados. Reconocido como experto.",
                "ja": "深い勉強や研究に没頭すれば大きな成果を出します。専門家として認められます。",
                "zh": "潜心深入学习或研究将取得巨大成果。获得专家认可。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐",
                "ko": "국가 자격증이나 학위 취득 등 문서와 관련된 경사가 있습니다.",
                "en": "Good news regarding certifications or degrees.",
                "fr": "Bonnes nouvelles concernant les certifications ou les diplômes.",
                "es": "Buenas noticias sobre certificaciones o títulos.",
                "ja": "国家資格や学位取得など、文書に関連した慶事があります。",
                "zh": "有考取国家资格证或学位等文书相关的喜事。"
            },
            {
                "mon": "10월", "star": "⭐⭐",
                "ko": "사사건건 방해하는 경쟁자가 나타나 스트레스를 줍니다. 무시하는 게 답입니다.",
                "en": "Annoying competitors cause stress. Ignore them.",
                "fr": "Des concurrents agaçants causent du stress. Ignorez-les.",
                "es": "Competidores molestos causan estrés. Ignóralos.",
                "ja": "事あるごとに妨害するライバルが現れストレスを与えます。無視するのが正解です。",
                "zh": "出现事事阻挠的竞争对手，令人压力倍增。无视为上。"
            },
            {
                "mon": "11월", "star": "⭐⭐",
                "ko": "친한 친구와 돈 문제로 의 상할 수 있습니다. 밥은 사되 돈은 빌려주지 마세요.",
                "en": "Money issues with friends. Don't lend cash.",
                "fr": "Problèmes d'argent avec des amis. Ne prêtez pas d'argent.",
                "es": "Problemas de dinero con amigos. No prestes efectivo.",
                "ja": "親しい友人と金銭問題で仲違いする恐れがあります。食事は奢ってもお金は貸さないでください。",
                "zh": "可能会因金钱问题与好朋友伤感情。请客吃饭可以，但别借钱。"
            },
            {
                "mon": "12월", "star": "⭐⭐",
                "ko": "자존심 때문에 사랑하는 사람과 다툴 수 있습니다. 이번 한 번만 져주세요.",
                "en": "Pride causes fights with loved ones. Just lose this time.",
                "fr": "L'orgueil cause des disputes avec les proches. Perdez juste cette fois.",
                "es": "El orgullo causa peleas con seres queridos. Pierde solo esta vez.",
                "ja": "プライドのせいで愛する人と喧嘩するかもしれません。今回一度だけ負けてあげてください。",
                "zh": "可能会因自尊心与爱人争吵。就这一次，让着点吧。"
            }
        ]
    }

    # 데이터 가져오기 (해당 오행)
    months = raw_data.get(element, raw_data["Wood"])
    result = []

    # 월 표시 언어 설정
    month_map = {
        "1월": {"en":"Jan", "fr":"Janv", "es":"Ene", "ja":"1月", "zh":"1月"},
        "2월": {"en":"Feb", "fr":"Févr", "es":"Feb", "ja":"2月", "zh":"2月"},
        "3월": {"en":"Mar", "fr":"Mars", "es":"Mar", "ja":"3月", "zh":"3月"},
        "4월": {"en":"Apr", "fr":"Avr", "es":"Abr", "ja":"4月", "zh":"4月"},
        "5월": {"en":"May", "fr":"Mai", "es":"May", "ja":"5月", "zh":"5月"},
        "6월": {"en":"Jun", "fr":"Juin", "es":"Jun", "ja":"6月", "zh":"6月"},
        "7월": {"en":"Jul", "fr":"Juil", "es":"Jul", "ja":"7月", "zh":"7月"},
        "8월": {"en":"Aug", "fr":"Août", "es":"Ago", "ja":"8月", "zh":"8月"},
        "9월": {"en":"Sep", "fr":"Sept", "es":"Sep", "ja":"9月", "zh":"9月"},
        "10월": {"en":"Oct", "fr":"Oct", "es":"Oct", "ja":"10月", "zh":"10月"},
        "11월": {"en":"Nov", "fr":"Nov", "es":"Nov", "ja":"11月", "zh":"11月"},
        "12월": {"en":"Dec", "fr":"Déc", "es":"Dic", "ja":"12月", "zh":"12月"}
    }

    for m_data in months:
        mon_ko = m_data["mon"]
        # 1. 월 이름 변환
        if lang == "ko":
            display_mon = mon_ko
        else:
            display_mon = month_map.get(mon_ko, {}).get(lang, month_map[mon_ko]['en'])
            
        # 2. 운세 텍스트 선택
        # 해당 언어가 있으면 그 언어, 없으면 영어(en) 반환
        advice_text = m_data.get(lang, m_data['en'])
        
        result.append({
            "Month": display_mon,
            "Luck": m_data["star"],
            "Advice": advice_text
        })
    
    return result
# ----------------------------------------------------------------
# 4. 사이드바 구성 (언어 변경 기능 추가!)
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    
    # 현재 언어 표시
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Current Mode: **{lang_map.get(lang, 'English')}**")
    
    # ⭐ [언어 변경 버튼] ⭐
    st.write("Change Language:")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        if st.button("🇺🇸 EN", use_container_width=True):
            st.session_state['lang'] = 'en'
            st.rerun()
    with col_l2:
        if st.button("🇰🇷 KO", use_container_width=True):
            st.session_state['lang'] = 'ko'
            st.rerun()
    with col_l3:
        if st.button("🇫🇷 FR", use_container_width=True):
            st.session_state['lang'] = 'fr'
            st.rerun()
            
    col_l4, col_l5, col_l6 = st.columns(3)
    with col_l4:
        if st.button("🇪🇸 ES", use_container_width=True):
            st.session_state['lang'] = 'es'
            st.rerun()
    with col_l5:
        if st.button("🇯🇵 JA", use_container_width=True):
            st.session_state['lang'] = 'ja'
            st.rerun()
    with col_l6:
        if st.button("🇨🇳 ZH", use_container_width=True):
            st.session_state['lang'] = 'zh'
            st.rerun()

    st.markdown("---")
    
    # 홈으로 가기 버튼 (다국어 지원)
    btn_labels = {
        "ko": "🏠 홈으로", "en": "🏠 Go Home", "fr": "🏠 Accueil", 
        "es": "🏠 Inicio", "ja": "🏠 ホーム", "zh": "🏠 首页"
    }
    if st.button(btn_labels.get(lang, "Go Home"), use_container_width=True):
        st.switch_page("Home.py")    
# ----------------------------------------------------------------
# 4. 메인 로직 시작 (UI 및 검증)
# ----------------------------------------------------------------

# 홈 화면을 거치지 않고 직접 접속했을 경우 차단
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first. (홈 화면에서 정보를 입력해주세요.)")
    st.stop()

# UI 텍스트 리소스 (6개 국어 확장)
ui = {
    "ko": {
        "title": "디 엘리먼트: 2026년 정밀 운세",
        "lock": "🔒 유료 서비스 (Premium)",
        "label": "이메일로 받은 라이센스 키 입력",
        "btn_unlock": "확인 (Unlock)",
        "lock_warn": "⚠️ 주의: 결과 확인 시 라이센스 횟수가 1회 차감됩니다.",
        "welcome": "환영합니다",
        "h_trait": "🔮 타고난 기질",
        "h_fore": "📅 2026년 운세 분석",
        "print_btn": "🖨️ 결과 인쇄하기",
        "btn_buy_sp": "💳 단품 구매 ($10 / 3회)",
        "btn_buy_all": "🎟️ 프리패스 구매 ($30 / 10회)",
        "pop_btn": "⚠️ 사용 제한 확인",
        "pop_agree": "네, 확인했습니다 (진행)",
        "msg_ok_master": "마스터 키가 확인되었습니다!",
        "msg_ok_license": "정품 인증 성공!",
        "err_limit": "🚫 사용 횟수를 초과했습니다.",
        "err_invalid": "🚫 유효하지 않은 라이센스 키입니다.",
        "err_conn": "서버 연결 오류."
    },
    "en": {
        "title": "The Element: 2026 Forecast",
        "lock": "🔒 Premium Service",
        "label": "Enter License Key from Email",
        "btn_unlock": "Unlock",
        "lock_warn": "⚠️ Warning: This will consume 1 usage credit.",
        "welcome": "Welcome",
        "h_trait": "🔮 Personality",
        "h_fore": "📅 2026 Forecast",
        "print_btn": "🖨️ Print Result",
        "btn_buy_sp": "💳 Buy Single ($10 / 3 Uses)",
        "btn_buy_all": "🎟️ Buy All-Access ($30 / 10 Uses)",
        "pop_btn": "⚠️ Check Limit Info",
        "pop_agree": "I Understand & Proceed",
        "msg_ok_master": "Master Key Accepted!",
        "msg_ok_license": "License Verified!",
        "err_limit": "🚫 Limit exceeded.",
        "err_invalid": "🚫 Invalid License Key.",
        "err_conn": "Connection Error."
    },
    "fr": {
        "title": "L'Élément : Prévisions 2026",
        "lock": "🔒 Service Premium",
        "label": "Entrez la clé de licence",
        "btn_unlock": "Déverrouiller",
        "lock_warn": "⚠️ Attention : Cela consommera 1 crédit.",
        "welcome": "Bienvenue",
        "h_trait": "🔮 Personnalité",
        "h_fore": "📅 Prévisions 2026",
        "print_btn": "🖨️ Imprimer",
        "btn_buy_sp": "💳 Achat Unique (10$ / 3 essais)",
        "btn_buy_all": "🎟️ Pass Tout Accès (30$ / 10 essais)",
        "pop_btn": "⚠️ Vérifier la limite",
        "pop_agree": "Je comprends et continue",
        "msg_ok_master": "Clé Maître acceptée !",
        "msg_ok_license": "Licence vérifiée !",
        "err_limit": "🚫 Limite dépassée.",
        "err_invalid": "🚫 Clé invalide.",
        "err_conn": "Erreur de connexion."
    },
    "es": {
        "title": "El Elemento: Pronóstico 2026",
        "lock": "🔒 Servicio Premium",
        "label": "Ingrese la clave de licencia",
        "btn_unlock": "Desbloquear",
        "lock_warn": "⚠️ Advertencia: Consumirá 1 crédito.",
        "welcome": "Bienvenido",
        "h_trait": "🔮 Personalidad",
        "h_fore": "📅 Pronóstico 2026",
        "print_btn": "🖨️ Imprimir",
        "btn_buy_sp": "💳 Compra Única ($10 / 3 usos)",
        "btn_buy_all": "🎟️ Pase Total ($30 / 10 usos)",
        "pop_btn": "⚠️ Verificar límite",
        "pop_agree": "Entiendo y procedo",
        "msg_ok_master": "¡Clave Maestra aceptada!",
        "msg_ok_license": "¡Licencia verificada!",
        "err_limit": "🚫 Límite excedido.",
        "err_invalid": "🚫 Clave inválida.",
        "err_conn": "Error de conexión."
    },
    "ja": {
        "title": "ジ・エレメント：2026年精密運勢",
        "lock": "🔒 プレミアムサービス",
        "label": "ライセンスキーを入力",
        "btn_unlock": "解除",
        "lock_warn": "⚠️ 注意：利用回数が1回分消費されます。",
        "welcome": "ようこそ",
        "h_trait": "🔮 生まれ持った気質",
        "h_fore": "📅 2026年の運勢",
        "print_btn": "🖨️ 結果を印刷",
        "btn_buy_sp": "💳 単品購入 ($10 / 3回)",
        "btn_buy_all": "🎟️ オールアクセス ($30 / 10回)",
        "pop_btn": "⚠️ 制限事項を確認",
        "pop_agree": "理解して進む",
        "msg_ok_master": "マスターキーを確認しました！",
        "msg_ok_license": "認証成功！",
        "err_limit": "🚫 回数制限を超えました。",
        "err_invalid": "🚫 無効なキーです。",
        "err_conn": "接続エラー。"
    },
    "zh": {
        "title": "元素：2026年精准运势",
        "lock": "🔒 高级服务",
        "label": "输入许可证密钥",
        "btn_unlock": "解锁",
        "lock_warn": "⚠️ 注意：将扣除1次使用次数。",
        "welcome": "欢迎",
        "h_trait": "🔮 天生气质",
        "h_fore": "📅 2026年运势",
        "print_btn": "🖨️ 打印结果",
        "btn_buy_sp": "💳 单次购买 ($10 / 3次)",
        "btn_buy_all": "🎟️ 全通票 ($30 / 10次)",
        "pop_btn": "⚠️ 查看限制",
        "pop_agree": "我明白并继续",
        "msg_ok_master": "万能钥匙已确认！",
        "msg_ok_license": "验证成功！",
        "err_limit": "🚫 超过使用限制。",
        "err_invalid": "🚫 无效的密钥。",
        "err_conn": "连接错误。"
    }
}

# 언어 fallback 설정
if lang not in ui: lang = "en"
t = ui[lang]

st.markdown(f"<div class='year-title'>{t['title']}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 5. 잠금 해제 (Gumroad + MasterKey)
# ----------------------------------------------------------------
if "unlocked_2026" not in st.session_state: st.session_state["unlocked_2026"] = False

# 🌟 팝업창(Dialog) 함수 - 경고문구 표시
@st.dialog("⚠️ Warning")
def show_limit_warning():
    st.warning(t['lock_warn'], icon="⚠️")
    if st.button(t['pop_agree'], type="primary"):
        st.rerun()

if not st.session_state["unlocked_2026"]:
    with st.container(border=True):
        st.write(f"### {t['lock']}")
        
        # 3회 제한 팝업 버튼
        if st.button(t['pop_btn'], type="secondary"):
            show_limit_warning()
            
        c1, c2 = st.columns(2)
        with c1: st.link_button(t['btn_buy_sp'], GUMROAD_LINK_SPECIFIC, use_container_width=True)
        with c2: st.link_button(t['btn_buy_all'], GUMROAD_LINK_ALL, use_container_width=True)
        
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock'], type="primary", use_container_width=True):
            # 1. 마스터 키 확인
            if key == UNLOCK_CODE:
                st.session_state["unlocked_2026"] = True
                st.success(t['msg_ok_master'])
                st.rerun()
            
            # 2. 검로드 라이센스 확인
            try:
                # (A) 단품 상품 확인
                response_specific = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={"product_permalink": "2026_forecast", "license_key": key} # 상품 ID 직접 입력 or 변수 사용
                )
                data_specific = response_specific.json()

                if data_specific.get("success"):
                    if data_specific.get("uses", 0) > 3:
                        st.error(t['err_limit'] + " (Max 3)")
                    else:
                        st.session_state["unlocked_2026"] = True
                        st.success(t['msg_ok_license'])
                        st.rerun()
                else:
                    # (B) All-Access 패스 확인
                    response_all = requests.post(
                        "https://api.gumroad.com/v2/licenses/verify",
                        data={"product_permalink": "all-access_pass", "license_key": key}
                    )
                    data_all = response_all.json()
                    
                    if data_all.get("success"):
                        if data_all.get("uses", 0) > 10:
                            st.error(t['err_limit'] + " (Max 10)")
                        else:
                            st.session_state["unlocked_2026"] = True
                            st.success(t['msg_ok_license'])
                            st.rerun()
                    else:
                        st.error(t['err_invalid'])
            
            except Exception as e:
                st.error(f"{t['err_conn']} ({str(e)})")
    st.stop() # 잠금 상태면 아래 내용 안 보여줌

# ----------------------------------------------------------------
# 6. 결과 화면 (잠금 해제 후)
# ----------------------------------------------------------------
st.divider()

# 사용자 일간 계산
day_info = calculate_day_gan(st.session_state["birth_date"])
my_elem = day_info['element']

# 한자 -> 영어 변환 (함수 재사용을 위해)
def map_gan_to_element(gan_hanja):
    mapping = {'甲':'Wood', '乙':'Wood', '丙':'Fire', '丁':'Fire', '戊':'Earth', '己':'Earth', '庚':'Metal', '辛':'Metal', '壬':'Water', '癸':'Water'}
    return mapping.get(gan_hanja, 'Wood')

final_element = my_elem
if my_elem in ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']:
    final_element = map_gan_to_element(my_elem)

# (1) 성격 및 (2) 2026 총운 데이터 가져오기
trait_text = get_interpretation(final_element, lang)
forecast = get_forecast_data(final_element)

# 일간 이름 표시 (번역)
elem_display_map = {
    'Wood': {'ko':'목(나무)', 'en':'Wood', 'fr':'Bois', 'es':'Madera', 'ja':'木', 'zh':'木'},
    'Fire': {'ko':'화(불)', 'en':'Fire', 'fr':'Feu', 'es':'Fuego', 'ja':'火', 'zh':'火'},
    'Earth': {'ko':'토(흙)', 'en':'Earth', 'fr':'Terre', 'es':'Tierra', 'ja':'土', 'zh':'土'},
    'Metal': {'ko':'금(쇠)', 'en':'Metal', 'fr':'Métal', 'es':'Metal', 'ja':'金', 'zh':'金'},
    'Water': {'ko':'수(물)', 'en':'Water', 'fr':'Eau', 'es':'Agua', 'ja':'水', 'zh':'水'}
}
elem_name = elem_display_map.get(final_element, {}).get(lang, final_element)


# === 화면 출력 ===

# 1. 성격 분석
st.subheader(f"{t['h_trait']}")
st.markdown(f"""
<div class='card'>
    <h3 style='color:#94a3b8'>👋 {t['welcome']}, {st.session_state['user_name']}</h3>
    <h1 style='color:#60a5fa'>{elem_name} ({final_element})</h1>
    <div style='margin-top:15px; font-size:1.1em; line-height:1.6;'>{trait_text}</div>
</div>
""", unsafe_allow_html=True)

# 2. 2026 운세 (총운)
st.subheader(f"{t['h_fore']}")
st.markdown(f"""
<div class='card' style='border:1px solid #fbbf24'>
    <h2 style='color:#fbbf24'>👑 {forecast['title']}</h2>
    <p style='font-size:1.1em; line-height:1.6;'>{forecast['gen']}</p>
    <div style='margin-top:20px; padding-top:10px; border-top:1px solid #475569'>
        <p><b>💰 Money:</b> {forecast['money']}</p>
        <p><b>❤️ Love:</b> {forecast['love']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. 월별 표
monthly_data = get_monthly_forecast_unique(final_element, lang)
df = pd.DataFrame(monthly_data)
# 인덱스 숨기기 위해 CSS 사용하거나, 그냥 표시
st.table(df)

# 4. 인쇄 버튼 (JS)
st.divider()
components.html(
    f"""
    <script>
        function printParent() {{
            window.parent.print();
        }}
    </script>
    <div style="display: flex; justify-content: center;">
        <button onclick="printParent()" style="
            background-color: #3b82f6; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            text-align: center; 
            font-size: 16px; 
            cursor: pointer;
            border-radius: 8px;
            font-family: sans-serif;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: background-color 0.3s;
        ">
            {t['print_btn']}
        </button>
    </div>
    """,
    height=100
)
