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
    "Wealth": { # 재성 (재물과 수확의 에너지)
        "ko": "💰 <b>황금빛 풍요의 기운이 가득한 날입니다!</b><br>재물운이 정점에 달해 있으니 중요한 투자 결정을 내리거나 복권을 구매하기에 최적입니다. 평소 망설였던 큰 규모의 쇼핑이나 자산 운용을 시작해 보세요. 당신의 선택이 곧 수익으로 돌아올 것입니다.",
        "en": "💰 <b>A golden day of financial abundance!</b><br>Your financial energy is peaking, making it the ultimate timing for major investment decisions or purchasing a lottery ticket. Don't hesitate to proceed with significant purchases or wealth management plans today; your intuition will lead to tangible rewards.",
        "fr": "💰 <b>Une journée dorée d'abondance financière !</b><br>Votre énergie de richesse est à son apogée. C'est le moment idéal pour prendre des décisions d'investissement majeures ou tenter votre chance à la loterie. Ne tardez pas à concrétiser vos projets d'achat ou de gestion de patrimoine.",
        "es": "💰 <b>¡Un día dorado de abundancia financiera!</b><br>Tu energía de riqueza está en su punto máximo, lo que lo convierte en el momento ideal para decisiones de inversión importantes o comprar lotería. No dudes en realizar compras significativas; tu intuición te guiará hacia el éxito.",
        "ja": "💰 <b>黄金の輝きに満ちた金運最高の日です！</b><br>財운が絶頂に達しており、重要な投資判断や宝くじの購入にこれ以上ないタイミングです。欲しかった高額商品の購入や資産運用の開始も吉。今日の選択が将来の大きな利益に繋がるでしょう。",
        "zh": "💰 <b>黄金般的财富丰收之日！</b><br>您的财运正处于巅峰状态，是非常适合进行重大投资决策或购买彩票的绝佳时机。对于一直犹豫的大宗购物或资产管理计划，今天可以果断行动，您的眼光将转化为实际收益。"
    },
    "Output": { # 식상 (표현과 창의성의 에너지)
        "ko": "💘 <b>당신의 숨겨진 매력과 끼가 폭발하는 날입니다!</b><br>상대방의 마음을 사로잡는 화술과 센스가 돋보이니 설레는 데이트나 진심 어린 고백을 계획해 보세요. 창의적인 영감이 필요한 프로젝트나 예술 활동에서도 눈부신 성과를 거둘 수 있는 주인공의 날입니다.",
        "en": "💘 <b>A day where your hidden charm and talent explode!</b><br>Your wit and communication skills are exceptionally captivating, making it perfect for a romantic date or a heartfelt confession. In creative projects or artistic endeavors, you will shine as the main character, achieving brilliant results.",
        "fr": "💘 <b>Une journée où votre charme et votre talent éclatent !</b><br>Votre esprit et votre éloquence sont captivants. Idéal pour un rendez-vous romantique ou une déclaration sincère. Vous brillerez également dans tout projet créatif ou artistique, tel un véritable protagoniste.",
        "es": "💘 <b>¡Un día donde tu encanto y talento estallan!</b><br>Tu ingenio y habilidades de comunicación son excepcionalmente cautivadores, lo que lo hace perfecto para una cita romántica. En proyectos creativos, brillarás como el protagonista principal, logrando resultados brillantes.",
        "ja": "💘 <b>あなたの隠れた魅力と才能が溢れ出す日です！</b><br>相手の心を掴む話術とセンスが冴え渡るので、気になる人への告白や特別なデートに最適です。創造的なインスピレーションも湧きやすく、クリエイティブな活動やプレゼンでも主役として輝けるでしょう。",
        "zh": "💘 <b>您的魅力与才华全面爆发的一天！</b><br>今天您的谈吐和洞察力极具感染力，非常适合浪漫约会或真情告白。在需要创意的项目或艺术活动中，您将如同主角般闪耀，取得令人瞩目的成就。"
    },
    "Resource": { # 인성 (안정과 지혜의 에너지)
        "ko": "📝 <b>우주의 안정적인 기운이 당신을 보호하고 돕습니다.</b><br>중요한 계약서에 도장을 찍거나 결혼, 이사 등 삶의 기반을 다지는 일에 더없이 길한 날입니다. 새로운 지식을 습득하거나 깊이 있는 공부를 시작해 보세요. 당신의 지혜가 단단한 뿌리를 내리는 시기입니다.",
        "en": "📝 <b>The universe's stable energy protects and guides you.</b><br>It is an auspicious day for foundational life events like signing contracts, weddings, or moving. It's also the perfect time to acquire new knowledge or start deep studies; your wisdom will take firm root today.",
        "fr": "📝 <b>L'énergie stable de l'univers vous protège et vous guide.</b><br>C'est un jour faste pour les événements fondateurs comme la signature de contrats, les mariages ou les déménagements. Profitez-en pour acquérir de nouvelles connaissances ; votre sagesse s'enracinera durablement.",
        "es": "📝 <b>La energía estable del universo te protege y te guía.</b><br>Es un día propicio para eventos fundamentales como firmar contratos, bodas o mudanzas. También es el momento perfecto para adquirir nuevos conocimientos; tu sabiduría echará raíces firmes hoy.",
        "ja": "📝 <b>宇宙の安定したエネルギーがあなたを優しく守る日です。</b><br>重要な契約や結婚、引越しなど、人生の基盤を固める決断に最適な吉日です。新しいスキルの習得や深い学びに時間を費やしてみましょう。あなたの知恵が確かな実りをもたらす礎となります。",
        "zh": "📝 <b>宇宙稳定的气场正默默地守护并指引着您。</b><br>今天是签约、结婚、搬家等奠定人生基础事务的大吉之日。也非常适合汲取新知识或开启深度学习，您的智慧将在今天像大树一样扎下深根。"
    },
    "Power": { # 관성 (명예와 책임의 에너지)
        "ko": "🏆 <b>세상이 당신의 가치를 인정하는 명예로운 날입니다!</b><br>승진 기회를 잡거나 중요한 면접, 시험에서 최고의 실력을 발휘할 수 있는 강한 합격운이 따릅니다. 리더십을 발휘하여 조직 내 입지를 다지고, 당신의 명성을 널리 알릴 기회를 놓치지 마세요.",
        "en": "🏆 <b>A day of honor where the world recognizes your value!</b><br>Strong luck for success follows you in interviews, exams, or career advancements. Seize the opportunity to solidify your position within your organization through leadership and let your reputation flourish.",
        "fr": "🏆 <b>Un jour d'honneur où le monde reconnaît votre valeur !</b><br>Une forte chance de réussite vous accompagne pour les entretiens ou les promotions. Saisissez l'occasion d'affirmer votre leadership et de renforcer votre position au sein de votre organisation.",
        "es": "🏆 <b>¡Un día de honor donde el mundo reconoce tu valor!</b><br>La suerte te acompaña en entrevistas, exámenes o ascensos. Aprovecha la oportunidad para consolidar tu posición dentro de tu organización a través del liderazgo y deja que tu reputación florezca.",
        "ja": "🏆 <b>世界があなたの価値を認める、名誉ある一日です！</b><br>昇進のチャンスや重要な面接、試験において実力を最大限に発揮できる強い成功運が伴います。リーダーシップを発揮して組織内での地位を確立し、あなたの名を広める好機を逃さないでください。",
        "zh": "🏆 <b>全世界都认可您价值的光荣之日！</b><br>今天有极强的成功运，非常适合面试、考试或争取晋升机会。请尽情发挥领导力以巩固在团队中的地位，不要错过任何一个提升名望和影响力的好时机。"
    },
    "Same": { # 비견 (관계와 유대감의 에너지)
        "ko": "🤝 <b>사람 사이의 연결고리가 단단해지고 깊어지는 날입니다.</b><br>새로운 인맥을 넓히거나 소중한 친구들과 파티를 열어 즐거운 시간을 보내세요. 주변 동료들과의 협력을 통해 혼자서는 해결하지 못했던 난제를 시원하게 풀어나갈 수 있는 귀중한 조력자를 만날 운입니다.",
        "en": "🤝 <b>A day where social connections strengthen and deepen.</b><br>Expand your network, host a party, or enjoy quality time with cherished friends. Through collaboration, you will meet valuable supporters who can help you solve complex problems that seemed impossible alone.",
        "fr": "🤝 <b>Une journée où les liens sociaux se renforcent et s'approfondissent.</b><br>Élargissez votre réseau, organisez une fête ou passez du temps avec des amis chers. La collaboration vous permettra de rencontrer des alliés précieux pour résoudre des problèmes complexes.",
        "es": "🤝 <b>Un día donde las conexiones sociales se fortalecen y profundizan.</b><br>Amplía tu red, organiza una fiesta o disfruta con amigos. A través de la colaboración, conocerás a aliados valiosos que te ayudarán a resolver problemas que parecían imposibles solo.",
        "ja": "🤝 <b>人との絆がより強く、より深くなる日です。</b><br>新しい人脈を広げたり、親しい友人たちとパーティーを開いて楽しい時間を共有しましょう。周囲との協調を大切にすることで、一人では解決できなかった難題を共に乗り越えてくれる強力な助っ人が現れる予感です。",
        "zh": "🤝 <b>人际纽带变得更加紧密且深厚的一天。</b><br>非常适合拓展人脉、举办聚会或与好友共度时光。通过团队协作，您将有望遇到能助您一臂之力的贵人，共同解决那些单打独斗难以攻克的难题。"
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
                if st.button("Unlock", type="primary", use_container_width=True):
                    # 1. 마스터 키 (무제한) 확인
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_date_2"] = True
                        st.success("Master Unlocked!")
                        st.rerun()
                    else:
                        try:
                            # 2. 단품(Date Selection) 키 확인 (3회 제한)
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={
                                                  "product_permalink": "date_selection", 
                                                  "license_key": k_in,
                                                  "increment_uses_count": "true" # 👈 횟수 차감 활성화
                                              }).json()
                            
                            if r.get("success"):
                                if r.get("uses", 0) > 3: # 🚨 3회 제한 로직
                                    st.error("🚫 Usage limit exceeded (Max 3)")
                                else:
                                    st.session_state["unlocked_date_2"] = True
                                    st.rerun()
                            else:
                                # 3. 올패스(All-Access) 키 확인 (합산 10회 제한)
                                # 주의: 이 페이지에는 GUMROAD_LINK_ALL 변수가 누락되어 있을 수 있으니 확인 필요
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={
                                                       "product_permalink": "all-access_pass", 
                                                       "license_key": k_in,
                                                       "increment_uses_count": "true" # 👈 횟수 차감 활성화
                                                   }).json()
                                
                                if r2.get("success"):
                                    if r2.get("uses", 0) > 10: # 🚨 합산 10회 제한 로직
                                        st.error("🚫 Usage limit exceeded (Max 10)")
                                    else:
                                        st.session_state["unlocked_date_2"] = True
                                        st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: 
                            st.error("Connection Error")
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
