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
st.set_page_config(page_title="Specific Day Forecast | The Element", page_icon="📅", layout="wide")

# 언어 설정
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

# 🔑 [마스터 키 & 구매 링크]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/specific_day"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정 (CSS)
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        /* 탭 스타일 변경 */
        button[data-baseweb="tab"] {
            color: #cbd5e1 !important; /* 기본 탭 글자색 (밝은 회색) */
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #f472b6 !important; /* 선택된 탭 글자색 (핑크) */
            background-color: rgba(244, 114, 182, 0.1) !important; /* 선택된 탭 배경 */
        }
        .stApp {
            background-image: linear-gradient(rgba(20, 30, 48, 0.9), rgba(36, 59, 85, 0.9)),
            url("https://img.freepik.com/free-photo/abstract-paint-texture-background-blue-sumi-e-style_53876-129316.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        [data-testid="stSidebarNav"] span { font-size: 1.1rem !important; font-weight: 600 !important; color: #e2e8f0 !important; }
        
        .day-header {
            font-size: 2.2em; font-weight: 800; color: #f472b6; text-align: center; margin-bottom: 20px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);
        }
        .card {
            background: rgba(30, 41, 59, 0.9); border: 1px solid #475569; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; color: #e2e8f0; line-height: 1.6;
        }
        .premium-box {
            border: 1px solid #f472b6; background: rgba(83, 24, 59, 0.3); padding: 20px; border-radius: 10px; margin-top: 10px;
        }
        h3, h4 { font-family: 'Gowun Batang', serif; }
        
        /* 잠금 오버레이 스타일 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #f472b6;
            box-shadow: 0 0 20px rgba(244, 114, 182, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 함수 (6개 국어 - 키값 통일 완료)
# ----------------------------------------------------------------
def get_relationship_data(user_elem, target_elem, language):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Wood": "Resource", "Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power"},
        "Earth": {"Wood": "Power", "Fire": "Resource", "Earth": "Same", "Metal": "Output", "Water": "Wealth"},
        "Metal": {"Wood": "Wealth", "Fire": "Power", "Earth": "Resource", "Metal": "Same", "Water": "Output"},
        "Water": {"Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource", "Water": "Same"},
    }
    rel_key = relations.get(user_elem, {}).get(target_elem, "Same")
    
    # 데이터베이스 (6개 국어)
    db = {
        "Same": { # 비견/겁재
            "ko": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 거울 속의 나를 만나는 날 (자아/경쟁)",
                "d": "오늘은 당신과 똑같은 에너지가 우주에서 쏟아지는 날입니다. 독립심과 주체성이 폭발하여 누구의 도움 없이도 혼자서 일을 처리해내는 능력이 탁월해집니다. 하지만 '내가 맞고 네가 틀리다'는 고집이 생기기 쉬우니 주의하세요.",
                "money": "재물운에서는 '탈재(奪財)', 즉 재물을 뺏길 수 있습니다. 친구가 돈을 빌려달라고 하거나 예상치 못한 지출이 생깁니다. 이를 방지하는 최고의 방법은 **먼저 베푸는 것**입니다.",
                "love": "연애 전선에 '경쟁자'의 그림자가 보입니다. 연인이 있다면 자존심 싸움을 하다가 냉전이 될 수 있습니다. 오늘 당신이 해야 할 일은 딱 하나, **'무조건 져주는 척하기'**입니다.",
                "health": "에너지가 차고 넘쳐서 문제입니다. 가만히 있으면 몸살이 날 수 있으니 헬스장이나 등산을 가서 에너지를 쏟아내세요.",
                "action": "1. 주문: '그래, 그럴 수도 있지.' (고집 내려놓기)\n2. 행동: 친구에게 밥 사주기\n3. 주의: 동업 제안이나 돈 거래 금지.",
                "lucky": "🕶️ 선글라스/거울, 👫 모임 장소"
            },
            "en": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 Day of the Mirror: Strong Self & Competition",
                "d": "Energy identical to yours flows today. Independence creates great ability to work alone, but avoid the stubborn 'I am right, you are wrong' attitude.",
                "money": "Risk of wealth loss. Prevent this by spending on others first (charity or treating friends). Avoid high-risk investments.",
                "love": "Rivals may appear. In relationships, avoid ego battles. Your mission today is to 'pretend to lose' to keep the peace.",
                "health": "Excess energy needs release. Work out vigorously to avoid feeling restless or sick.",
                "action": "1. Mantra: 'It is what it is.'\n2. Action: Treat a friend to a meal.\n3. Warning: No lending money.",
                "lucky": "🕶️ Sunglasses/Mirror, 👫 Social Gatherings"
            },
            "fr": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 Jour du Miroir : Soi Fort & Compétition",
                "d": "Une énergie identique à la vôtre circule aujourd'hui. Grande indépendance, mais évitez l'attitude obstinée du 'J'ai raison, tu as tort'.",
                "money": "Risque de perte financière. Prévenez cela en dépensant d'abord pour les autres (charité ou resto entre amis). Évitez les investissements risqués.",
                "love": "Des rivaux peuvent apparaître. Évitez les batailles d'ego. Votre mission : 'faire semblant de perdre' pour garder la paix.",
                "health": "Trop d'énergie. Faites du sport intensément pour ne pas vous sentir agité.",
                "action": "1. Mantra : 'C'est comme ça.'\n2. Action : Offrir un repas à un ami.\n3. Attention : Ne prêtez pas d'argent.",
                "lucky": "🕶️ Lunettes de soleil/Miroir, 👫 Rassemblements"
            },
            "es": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 Día del Espejo: Yo Fuerte y Competencia",
                "d": "Hoy fluye energía idéntica a la tuya. Gran independencia, pero evita la actitud terca de 'Yo tengo razón y tú no'.",
                "money": "Riesgo de perder dinero. Evítalo gastando en otros primero (caridad o invitar a amigos). Evita inversiones de alto riesgo.",
                "love": "Pueden aparecer rivales. Evita luchas de ego. Tu misión hoy es 'fingir perder' para mantener la paz.",
                "health": "Exceso de energía. Haz ejercicio vigoroso para liberar la tensión.",
                "action": "1. Mantra: 'Es lo que es.'\n2. Acción: Invita a comer a un amigo.\n3. Advertencia: No prestes dinero.",
                "lucky": "🕶️ Gafas de sol/Espejo, 👫 Reuniones sociales"
            },
            "ja": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 鏡の日：強い自我と競争",
                "d": "自分と同じエネルギーが流れる日。独立心が高まりますが、「自分が正しい」という頑固な態度は避けましょう。",
                "money": "お金が出ていく運気です。寄付や友人に奢るなど、先に人のために使うことで不運を防げます。投資は控えて。",
                "love": "ライバル現る。恋人とは意地の張り合いを避けて。平和のために「負けるが勝ち」を演じましょう。",
                "health": "エネルギーが余っています。激しい運動をして発散しないと体調を崩します。",
                "action": "1. 呪文：「まあ、いいか」\n2. 行動：友人に食事をご馳走する\n3. 注意：お金の貸し借りは禁止。",
                "lucky": "🕶️ サングラス/鏡, 👫 集まり"
            },
            "zh": {
                "score": 3, "star": "⭐⭐⭐",
                "t": "🤝 镜面之日：自我与竞争",
                "d": "今天流动着与你相同的能量。独立能力虽强，但要避免“我是对的，你是错的”这种固执态度。",
                "money": "有破财风险。建议通过先花钱（慈善或请客）来化解。避免高风险投资。",
                "love": "可能出现情敌。避免自尊心的争斗。今天的任务是为了和平而“假装输掉”。",
                "health": "精力过剩。做些剧烈运动来发泄，以免感到焦躁。",
                "action": "1. 咒语：“就这样吧”\n2. 行动：请朋友吃饭\n3. 注意：禁止借钱给别人。",
                "lucky": "🕶️ 墨镜/镜子, 👫 聚会"
            }
        },
        
        "Output": { # 식상 (Output)
            "ko": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 억눌린 끼가 폭발하는 '표현'의 날",
                "d": "가슴 속 아이디어가 화산처럼 분출됩니다. 머리 회전이 빨라져 창의적인 기획에 탁월합니다. 당신이 주인공이 되어 무대를 휘어잡는 날이니 자신감 있게 드러내세요.",
                "money": "당신의 재주와 말솜씨가 곧바로 수익으로 연결됩니다. 프리랜서나 영업직에게 대박의 날입니다. 단, 기분이 들떠서 하는 '충동구매'만 조심하세요.",
                "love": "유머 감각과 센스가 폭발하여 이성의 마음을 사로잡습니다. 썸 타는 사람에게 고백하기 좋은 날입니다. 여성은 남편에게 잔소리 대신 칭찬을 해주세요.",
                "health": "에너지 소모가 극심해 저녁엔 방전될 수 있습니다. 달콤한 디저트로 당을 충전하고 목을 보호하세요.",
                "action": "1. 주문: '나는 아티스트다.'\n2. 행동: 노래방, 일기 쓰기, SNS 포스팅\n3. 주의: 말실수 조심 (세 번 생각하고 말하기).",
                "lucky": "🎤 마이크/노트, 🍰 디저트, 🎨 미술관"
            },
            "en": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 Day of Expression (Talent)",
                "d": "Ideas erupt. Perfect for creativity. You are the main character today; show off.",
                "money": "Talent brings cash. Beware of impulse buying.",
                "love": "Humor captivates. Great for confessions.",
                "health": "High energy consumption. Recharge with sweets.",
                "action": "1. Mantra: 'I am an Artist.'\n2. Action: Karaoke, Social Media.\n3. Warning: Watch your tongue.",
                "lucky": "🎤 Microphone, 🍰 Dessert"
            },
            "fr": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 Jour d'Expression (Talent)",
                "d": "Les idées fusent. Parfait pour la créativité. Vous êtes le personnage principal aujourd'hui ; montrez-vous.",
                "money": "Le talent rapporte de l'argent. Attention aux achats impulsifs.",
                "love": "L'humour captive. Idéal pour faire une déclaration.",
                "health": "Grande consommation d'énergie. Rechargez-vous avec des sucreries.",
                "action": "1. Mantra : 'Je suis un Artiste.'\n2. Action : Karaoké, Réseaux sociaux.\n3. Attention : Surveillez vos paroles.",
                "lucky": "🎤 Micro, 🍰 Dessert"
            },
            "es": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 Día de Expresión (Talento)",
                "d": "Las ideas brotan. Perfecto para la creatividad. Eres el protagonista hoy; lúcete.",
                "money": "El talento trae dinero. Cuidado con las compras impulsivas.",
                "love": "El humor cautiva. Genial para confesiones.",
                "health": "Alto consumo de energía. Recárgate con dulces.",
                "action": "1. Mantra: 'Soy un Artista.'\n2. Acción: Karaoke, Redes sociales.\n3. Advertencia: Cuida tu lengua.",
                "lucky": "🎤 Micrófono, 🍰 Postre"
            },
            "ja": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 表現の日（才能）",
                "d": "アイデアが爆発します。創造性を発揮するのに最適。今日の主役はあなたです。アピールしましょう。",
                "money": "才能がお金になります。衝動買いには注意してください。",
                "love": "ユーモアが心を掴みます。告白するのに絶好の日です。",
                "health": "エネルギー消費が激しいです。甘いもので充電してください。",
                "action": "1. 呪文：「私はアーティストだ」\n2. 行動：カラオケ、SNS\n3. 注意：失言に注意。",
                "lucky": "🎤 マイク, 🍰 デザート"
            },
            "zh": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 表现之日（才华）",
                "d": "灵感迸发。最适合发挥创意。今天你是主角，尽情展示吧。",
                "money": "才华变现。提防冲动购物。",
                "love": "幽默感迷人。非常适合表白。",
                "health": "能量消耗大。吃点甜食补充。",
                "action": "1. 咒语：“我是艺术家”\n2. 行动：卡拉OK、社交媒体\n3. 注意：小心口舌。",
                "lucky": "🎤 麦克风, 🍰 甜点"
            }
        },
        "Wealth": { # 재성 (Wealth)
            "ko": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 결실을 맺는 '수확'의 날 (재물/결과)",
                "d": "뜬구름 잡는 소리는 그만! 오늘은 철저하게 현실적이고 계산적인 하루입니다. 무엇이 나에게 이득인지 본능적으로 알게 됩니다. 노력에 대한 확실한 보상이 주어지며, 과정보다는 '결과'가 당신을 증명해 줄 것입니다.",
                "money": "금전운 최상(Best)! 하늘에서 돈비가 내리는 형국입니다. 예상치 못한 보너스, 밀린 돈을 받거나 투자 수익이 발생합니다. 사고 싶었던 물건을 싸게 사는 등 돈을 '잘 쓰는' 운도 좋습니다.",
                "love": "남자는 여자가 따르고, 여자는 능력 있는 남자를 만납니다. 감성보다는 현실적인 조건이 중요해지는 날입니다. 맛집 투어나 쇼핑 등 오감을 만족시키는 데이트가 행운을 부릅니다.",
                "health": "컨디션은 좋으나, 결과에 집착하여 신경성 두통이 올 수 있습니다. '돈 세다가 밤새는 줄 모른다'는 말처럼 과로하기 쉬우니 휴식을 챙기세요. 하체 운동이 재물운을 지켜줍니다.",
                "action": "1. 주문: '나는 부자다.' (풍요의 마인드)\n2. 행동: 지갑 정리, 복권 구매, 가계부 정리\n3. 주의: 돈 자랑 하지 말기. 조용히 챙길 것.",
                "lucky": "💳 지갑/현금, 🏦 은행/백화점, 🍗 고기/맛집"
            },
            "en": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 Day of Harvest: Results Are in Sight",
                "d": "No more daydreaming! Today is strictly realistic and calculated. You instinctively know what benefits you. Tangible rewards for your efforts await. Today, the 'Result' proves your worth more than the process.",
                "money": "Best Financial Luck! It's raining money. Unexpected bonuses, overdue payments, or investment returns are likely. It's also a good day for smart spending, like finding great deals on items you wanted.",
                "love": "Men will be popular with women, and women will be drawn to capable partners. Realistic conditions matter more than emotions today. Sensory dates like gourmet tours or shopping bring good luck.",
                "health": "Body feels light, but obsessing over results can cause tension headaches. Beware of overworking from excitement. Lower body exercises will strengthen your capacity to hold wealth.",
                "action": "1. Mantra: 'I am Abundant.'\n2. Action: Organize wallet, Buy a lottery ticket.\n3. Warning: Don't show off your money.",
                "lucky": "💳 Wallet/Cash, 🏦 Bank/Mall, 🍗 Fine Dining"
            },
            "fr": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 Jour de Récolte : Résultats en Vue",
                "d": "Fini de rêvasser ! Aujourd'hui est une journée strictement réaliste et calculée. Vous savez instinctivement ce qui est profitable. Des récompenses tangibles vous attendent. Le 'Résultat' compte plus que le processus.",
                "money": "Chance Financière au Top ! Il pleut de l'argent. Bonus inattendus ou retours sur investissement sont probables. C'est aussi un bon jour pour dépenser intelligemment et faire de bonnes affaires.",
                "love": "Les hommes auront du succès, les femmes chercheront des partenaires capables. Le réalisme l'emporte sur l'émotion. Les rendez-vous gourmands ou le shopping portent chance.",
                "health": "Bonne forme, mais l'obsession des résultats peut causer des maux de tête. Attention au surmenage. Les exercices des jambes renforcent votre chance financière.",
                "action": "1. Mantra : 'Je suis Abondant.'\n2. Action : Organiser son portefeuille, Acheter un billet de loterie.\n3. Attention : Ne montrez pas votre argent.",
                "lucky": "💳 Portefeuille, 🏦 Banque, 🍗 Restaurant"
            },
            "es": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 Día de Cosecha: Resultados a la Vista",
                "d": "¡No más soñar despierto! Hoy es un día estrictamente realista y calculado. Sabes instintivamente qué te beneficia. Recompensas tangibles te esperan. El 'Resultado' importa más que el proceso hoy.",
                "money": "¡La Mejor Suerte Financiera! Llueve dinero. Bonos inesperados o retornos de inversión son probables. También es un buen día para gastar sabiamente y encontrar grandes ofertas.",
                "love": "Los hombres serán populares y las mujeres buscarán parejas capaces. El realismo supera a la emoción. Citas sensoriales como tours gastronómicos o compras traen suerte.",
                "health": "El cuerpo se siente ligero, pero obsesionarse con los resultados puede causar dolores de cabeza. Cuidado con el exceso de trabajo. Ejercicios de piernas fortalecen tu suerte.",
                "action": "1. Mantra: 'Soy Abundante.'\n2. Acción: Organizar la billetera, Comprar lotería.\n3. Advertencia: No presumas tu dinero.",
                "lucky": "💳 Billetera, 🏦 Banco, 🍗 Cena Fina"
            },
            "ja": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 収穫の日：結果が目の前に",
                "d": "夢を見るのはやめて、徹底的に現実的で計算高い一日になりましょう。何が利益になるか本能的にわかります。努力に対する確実な報酬が待っており、過程より「結果」があなたを証明します。",
                "money": "金運最高！空からお金の雨が降るようです。予期せぬボーナスや投資収益が期待できます。欲しかった物を安く買うなど、お金を「うまく使う」運も良いです。",
                "love": "男性はモテ期、女性は能力のある男性に惹かれます。感情より現実的な条件が重要になる日。グルメツアーやショッピングなどのデートが幸運を呼びます。",
                "health": "体調は良いですが、結果に執着して緊張性頭痛が起きるかも。興奮して働きすぎないように。下半身の運動が財運を支える器を丈夫にします。",
                "action": "1. 呪文：「私は豊かだ」\n2. 行動：財布の整理、宝くじ購入\n3. 注意：お金を自慢しないこと。",
                "lucky": "💳 財布/現金, 🏦 銀行/デパート, 🍗 グルメ"
            },
            "zh": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 收获之日：结果近在眼前",
                "d": "别做白日梦了！今天是非常现实和精打细算的一天。你会本能地知道什么对自己有益。切实的努力回报在等着你，今天“结果”比过程更能证明你的价值。",
                "money": "财运最佳！简直是天上掉钱。可能会有意外的奖金或投资回报。也是聪明消费的好日子，能以低价买到心仪的东西。",
                "love": "男性的异性缘极佳，女性则会被有能力的伴侣吸引。今天是现实条件重于情感的日子。美食之旅或购物等满足感官的约会能招来好运。",
                "health": "身体轻盈，但过度执着于结果可能会导致紧张性头痛。小心因兴奋而过劳。下肢运动能巩固你的财运。",
                "action": "1. 咒语：“我很富足”\n2. 行动：整理钱包，买彩票\n3. 注意：财不外露，不要炫富。",
                "lucky": "💳 钱包/现金, 🏦 银行/商场, 🍗 美食"
            }
        },
        "Power": { # 관성 (Power)
            "ko": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ 왕관의 무게를 견디는 '명예'의 날",
                "d": "책임감, 의무, 규칙이 당신을 둘러쌉니다. 상사의 압박이나 마감이 힘들게 느껴질 수 있습니다. 하지만 다이아몬드가 압력을 받아 만들어지듯, 이 스트레스를 견뎌내면 '리더'로서의 명예와 인정을 받게 됩니다.",
                "money": "현금보다는 '명예'가 올라갑니다. 승진운이 있습니다. 돈은 오히려 세금, 공과금, 범칙금 등 의무적인 지출로 나갈 수 있으니 주의하세요.",
                "love": "일에 치여 연인에게 소홀해지기 쉽습니다. 밖에서 받은 스트레스를 연인에게 풀지 않도록 각별히 조심하세요. 여성은 카리스마 있는 강한 남자를 만날 운입니다.",
                "health": "스트레스 지수가 최고조에 달합니다. 어깨 결림이나 편두통을 조심하세요. 오늘은 격렬한 운동보다는 요가나 명상, 반신욕으로 긴장을 풀어야 합니다.",
                "action": "1. 주문: '이 또한 지나가리라.' (인내)\n2. 행동: 정장/시계 착용, 규칙 준수\n3. 주의: 신호 위반, 지각 절대 금지.",
                "lucky": "👔 시계/정장, 🏛️ 관공서, 🧘 명상"
            },
            "en": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ Day of Honor: Bearing the Weight of the Crown",
                "d": "Responsibility and rules surround you. External pressure is high, but like a diamond formed under pressure, this stress forges you into a leader. Enduring it brings honor and recognition.",
                "money": "Reputation rises rather than cash. Promotion luck is strong. Money might leave your pocket for mandatory expenses like taxes or bills.",
                "love": "You might neglect your partner due to work. Be careful not to vent your stress on them. Women are likely to meet a powerful, charismatic man.",
                "health": "Stress levels peak. Watch out for stiff shoulders or migraines. Choose yoga or meditation over intense exercise today.",
                "action": "1. Mantra: 'This too shall pass.'\n2. Action: Wear a suit/watch, Follow rules.\n3. Warning: No lateness or violations.",
                "lucky": "👔 Suit/Watch, 🏛️ Government Office, 🧘 Meditation"
            },
            "fr": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ Jour d'Honneur : Porter le Poids de la Couronne",
                "d": "Responsabilités et règles vous entourent. La pression est forte, mais comme un diamant, ce stress vous forge en leader. L'endurance apporte la reconnaissance.",
                "money": "C'est la réputation qui monte, pas le cash. Chance de promotion. L'argent risque de sortir pour des dépenses obligatoires (taxes, factures).",
                "love": "Ne négligez pas votre partenaire à cause du travail. Ne déchargez pas votre stress sur l'autre. Les femmes pourraient rencontrer un homme charismatique.",
                "health": "Stress au maximum. Attention aux raideurs de la nuque et migraines. Préférez le yoga ou la méditation au sport intense.",
                "action": "1. Mantra : 'Cela aussi passera.'\n2. Action : Portez un costume/montre.\n3. Attention : Pas de retard ni d'infraction.",
                "lucky": "👔 Costume/Montre, 🏛️ Bureau, 🧘 Méditation"
            },
            "es": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ Día de Honor: Soportando el Peso de la Corona",
                "d": "La responsabilidad y las reglas te rodean. La presión es alta, pero como un diamante, este estrés te forja como líder. Aguantar trae reconocimiento.",
                "money": "Sube la reputación, no el efectivo. Suerte de ascenso. El dinero podría salir para gastos obligatorios como impuestos o facturas.",
                "love": "No descuides a tu pareja por el trabajo. No descargues tu estrés en ella. Las mujeres podrían conocer a un hombre poderoso.",
                "health": "Estrés al máximo. Cuidado con la rigidez de cuello y migrañas. Mejor yoga o meditación que ejercicio intenso.",
                "action": "1. Mantra: 'Esto también pasará.'\n2. Acción: Usa traje/reloj.\n3. Advertencia: Prohibido llegar tarde.",
                "lucky": "👔 Traje/Reloj, 🏛️ Oficina, 🧘 Meditación"
            },
            "ja": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ 名誉の日：王冠の重さに耐える",
                "d": "責任とルールがあなたを取り囲みます。圧力は高いですが、ダイヤモンドのように、今日のストレスはあなたをリーダーに育てます。耐えれば名誉が得られます。",
                "money": "現金より「名声」が上がる日。昇進の可能性があります。むしろ税金や請求書などでお金が出ていくかもしれません。",
                "love": "仕事で恋人を疎かにしがちです。ストレスを恋人にぶつけないよう注意。女性はカリスマ性のある男性に出会う運気です。",
                "health": "ストレスがピークに。肩こりや片頭痛に注意。激しい運動より、ヨガや瞑想でリラックスしてください。",
                "action": "1. 呪文：「これもまた過ぎ去る」\n2. 行動：スーツ/時計の着用\n3. 注意：遅刻・違反厳禁。",
                "lucky": "👔 スーツ/時計, 🏛️ 役所, 🧘 瞑想"
            },
            "zh": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ 名誉之日：欲戴王冠，必承其重",
                "d": "责任和规则包围着你。压力很大，但这正是将你锻造成领导者的过程。坚持下去会带来认可和名誉。",
                "money": "旺名声不旺财。有晋升运。钱财反而可能因税金或账单等义务性支出而流出。",
                "love": "容易因工作忽略伴侣。千万别把压力发泄在爱人身上。女性可能会遇到充满魅力的强势男性。",
                "health": "压力达到顶峰。注意肩膀僵硬或偏头痛。与其剧烈运动，不如做瑜伽或冥想。",
                "action": "1. 咒语：“这一切终将过去”\n2. 行动：穿西装/戴手表\n3. 注意：严禁迟到或违规。",
                "lucky": "👔 西装/手表, 🏛️ 政府机关, 🧘 冥想"
            }
        },
        "Resource": { # 인성 (Resource)
            "ko": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 사랑과 지혜가 충전되는 '힐링'의 날",
                "d": "마치 엄마 품에 안긴 듯 편안하고 안정적인 하루입니다. 굳이 애쓰지 않아도 주변에서 알아서 챙겨주고 도와주는 '인복'이 터집니다. 활동하기보다는 기존의 것을 점검하고, 공부하고, 계획을 세우기에 최적입니다. 오늘은 '속도'보다는 '방향'을 고민하는 시간입니다.",
                "money": "당장 현금이 도는 운은 아니지만, '문서운'이 대길합니다. 부동산 계약, 결재, 자격증 취득 등 서류상의 이득이 따릅니다. 훗날 큰 자산이 될 문서를 잡는 날이니, 나를 위한 공부에 돈을 아끼지 마세요. 윗사람에게 용돈을 받을 수도 있습니다.",
                "love": "사랑받는 날입니다. 연인에게 위로받고 싶어지며, 상대방이 나를 공주/왕자님처럼 세심하게 챙겨줍니다. 소개팅을 한다면 예의 바르고 학식이 깊어 배울 점이 많은 사람을 만나게 됩니다.",
                "health": "몸이 물 먹은 솜처럼 처지고 나른해질 수 있는데, 이는 병이 아니라 '쉬어가라'는 신호입니다. 억지로 운동하지 말고, 낮잠을 자거나 마사지를 받으며 푹 쉬는 것이 최고의 보약입니다. 소화가 느리니 과식은 피하세요.",
                "action": "1. 주문: '나는 사랑받기 위해 태어났다.'\n2. 행동: 독서, 명상, 부모님께 안부 전화\n3. 주의: 게으름 (생각만 하고 실행 안 함).",
                "lucky": "📚 책/도서관, ☕ 따뜻한 차, 🛌 침대/휴식"
            },
            "en": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 Day of Healing: Recharge with Love & Wisdom",
                "d": "A day as comfortable as a mother's embrace. You have great 'People Luck'—others help you without you even trying. Static energy dominates, making it perfect for studying, planning, and reviewing rather than starting new actions. Focus on 'Direction' rather than 'Speed' today.",
                "money": "Cash flow might be slow, but 'Document Luck' is excellent. Great for signing contracts, approvals, or acquiring licenses. Invest in self-improvement. You might receive gifts or allowance from elders.",
                "love": "You will be loved and cared for. Your partner will treat you like royalty and look after your feelings. If single, expect to meet someone polite, educated, and worthy of respect.",
                "health": "Feeling lethargic is a sign to rest, not sickness. Don't force intense exercise; a nap or massage is the best medicine today. Avoid overeating as digestion might be slow.",
                "action": "1. Mantra: 'I am born to be loved.'\n2. Action: Reading, Meditation, Call parents.\n3. Warning: Laziness (Thinking without acting).",
                "lucky": "📚 Book/Library, ☕ Warm Tea, 🛌 Bed/Rest"
            },
            "fr": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 Jour de Guérison : Recharger avec Amour et Sagesse",
                "d": "Une journée confortable comme les bras d'une mère. La chance avec les gens est excellente ; on vous aide spontanément. L'énergie est statique, idéale pour étudier et planifier plutôt que d'agir. Concentrez-vous sur la 'Direction' plutôt que la 'Vitesse'.",
                "money": "Pas de cash immédiat, mais excellente chance avec les 'Documents' (contrats, licences). C'est le moment d'investir en vous. Vous pourriez recevoir des cadeaux ou de l'argent de vos aînés.",
                "love": "Vous serez aimé et choyé. Votre partenaire prendra soin de vous comme d'un roi/une reine. Pour les célibataires, attendez-vous à rencontrer quelqu'un de poli et cultivé.",
                "health": "La léthargie est un signal pour se reposer. Ne forcez pas le sport ; une sieste ou un massage est le meilleur remède. Évitez les excès de table.",
                "action": "1. Mantra : 'Je suis né pour être aimé.'\n2. Action : Lecture, Méditation, Appeler les parents.\n3. Attention : Paresse.",
                "lucky": "📚 Livre, ☕ Thé chaud, 🛌 Repos"
            },
            "es": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 Día de Curación: Recarga con Amor y Sabiduría",
                "d": "Un día tan cómodo como el abrazo de una madre. Tienes gran 'Suerte con la Gente'; te ayudan sin pedirlo. La energía estática domina, ideal para estudiar y planificar. Enfócate en la 'Dirección' más que en la 'Velocidad'.",
                "money": "Poco flujo de efectivo, pero excelente 'Suerte de Documentos' (contratos, licencias). Invierte en ti mismo. Podrías recibir regalos de personas mayores.",
                "love": "Serás amado y cuidado. Tu pareja te tratará como a la realeza. Si estás soltero, conocerás a alguien educado y digno de admiración.",
                "health": "Sentirse letárgico es señal de descansar. No fuerces el ejercicio; una siesta o un masaje es la mejor medicina. Evita comer en exceso.",
                "action": "1. Mantra: 'Nací para ser amado.'\n2. Acción: Leer, Meditar, Llamar a los padres.\n3. Advertencia: Pereza.",
                "lucky": "📚 Libro, ☕ Té caliente, 🛌 Descanso"
            },
            "ja": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 癒しの日：愛と知恵の充電",
                "d": "母の胸のように安らかな日です。周りが自然と助けてくれる「人徳」があります。動くよりは、勉強や計画、点検に最適な静的な一日。「速度」より「方向」を考える時です。",
                "money": "現金より「文書運」が大吉。契約、決済、資格取得に良いです。自己投資にお金を使いましょう。目上の人からお小遣いをもらえるかも。",
                "love": "愛される日です。恋人はあなたを王族のように大切に扱ってくれます。シングルなら、礼儀正しく学識のある、尊敬できる人との出会いがあります。",
                "health": "体がだるいのは「休め」のサインです。無理な運動は避け、昼寝やマッサージが最高の薬です。消化機能が落ちるので過食は禁物。",
                "action": "1. 呪文：「私は愛されるために生まれた」\n2. 行動：読書、瞑想、親への連絡\n3. 注意：怠け心（考えすぎて動かない）。",
                "lucky": "📚 本, ☕ 温かいお茶, 🛌 休息"
            },
            "zh": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 治愈之日：爱与智慧的充电",
                "d": "像母亲怀抱一样舒适安稳的一天。贵人运极佳，周围人会主动帮忙。静态能量为主，适合学习、规划而非开展新行动。今天请关注“方向”而非“速度”。",
                "money": "虽然现金流一般，但“文书运”大吉（合同、审批、考证）。请投资自己。可能会收到长辈的红包或礼物。",
                "love": "是被爱的日子。伴侣会把你当王子/公主般细心照顾。单身者会遇到彬彬有礼、博学多才的对象。",
                "health": "身体沉重乏力是休息的信号。别强迫运动，午睡或按摩是最好的良药。注意消化不良，避免暴饮暴食。",
                "action": "1. 咒语：“我为被爱而生”\n2. 行动：读书、冥想、联系父母\n3. 注意：懒惰（只想不做）。",
                "lucky": "📚 书籍, ☕ 热茶, 🛌 休息"
            }
        }
    }
    data = db.get(rel_key, db["Same"])
    return data.get(language, data["en"])

# ----------------------------------------------------------------
# 4. 사이드바
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Current Mode: **{lang_map.get(lang, 'English')}**")
    
    st.write("Change Language:")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        if st.button("🇺🇸 EN", key="en"): st.session_state['lang']='en'; st.rerun()
    with col_l2:
        if st.button("🇰🇷 KO", key="ko"): st.session_state['lang']='ko'; st.rerun()
    with col_l3:
        if st.button("🇫🇷 FR", key="fr"): st.session_state['lang']='fr'; st.rerun()
    
    col_l4, col_l5, col_l6 = st.columns(3)
    with col_l4:
        if st.button("🇪🇸 ES", key="es"): st.session_state['lang']='es'; st.rerun()
    with col_l5:
        if st.button("🇯🇵 JA", key="ja"): st.session_state['lang']='ja'; st.rerun()
    with col_l6:
        if st.button("🇨🇳 ZH", key="zh"): st.session_state['lang']='zh'; st.rerun()

    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 5. 메인 로직
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    st.stop()

# ⭐ [수정] UI 텍스트 업데이트 (6개 국어 완벽 지원)
ui = {
    "ko": {
        "title": "📅 그날의 운세", 
        "sub": "선택한 날짜의 기운을 미리 확인하세요.",
        "date_label": "날짜 선택", 
        "btn_anal": "분석하기",
        "res_header": "🔒 오늘의 운세 분석 결과 (Premium)", 
        "lock_msg": "이 날의 기운, 재물, 연애, 행동 지침 등 모든 상세 분석은 유료 리포트에서 제공됩니다.",
        "btn_buy": "전체 리포트 열람 ($3)", 
        "btn_unlock": "잠금 해제", 
        "key_label": "라이센스 키",
        "h_money": "💰 재물운 가이드", "h_love": "❤️ 연애운 가이드", "h_health": "💪 건강 관리", 
        "h_action": "🚀 오늘의 행동 지침", "h_lucky": "🍀 행운의 아이템"
    },
    "en": {
        "title": "📅 Specific Day Forecast", 
        "sub": "Check the energy of any important day.",
        "date_label": "Select Date", 
        "btn_anal": "Analyze",
        "res_header": "🔒 Daily Forecast Analysis (Premium)", 
        "lock_msg": "Unlock the full report including Day Energy, Wealth, Love, and Action Guides.",
        "btn_buy": "Unlock Full Report ($3)", 
        "btn_unlock": "Unlock", 
        "key_label": "License Key",
        "h_money": "💰 Wealth Guide", "h_love": "❤️ Love Guide", "h_health": "💪 Health", 
        "h_action": "🚀 Action Plan", "h_lucky": "🍀 Lucky Items"
    },
    "fr": {
        "title": "📅 Prévisions du Jour", 
        "sub": "Vérifiez l'énergie d'un jour important.",
        "date_label": "Sélectionner une date", 
        "btn_anal": "Analyser",
        "res_header": "🔒 Analyse des Prévisions (Premium)", 
        "lock_msg": "Débloquez le rapport complet incluant l'énergie du jour, la richesse, l'amour et les conseils.",
        "btn_buy": "Rapport Complet ($3)", 
        "btn_unlock": "Déverrouiller", 
        "key_label": "Clé de Licence",
        "h_money": "💰 Guide Financier", "h_love": "❤️ Guide Amoureux", "h_health": "💪 Santé", 
        "h_action": "🚀 Plan d'Action", "h_lucky": "🍀 Porte-bonheur"
    },
    "es": {
        "title": "📅 Pronóstico del Día", 
        "sub": "Revisa la energía de cualquier día importante.",
        "date_label": "Seleccionar Fecha", 
        "btn_anal": "Analizar",
        "res_header": "🔒 Análisis del Pronóstico Diario (Premium)", 
        "lock_msg": "Desbloquea el informe completo incluyendo energía del día, riqueza, amor y guías de acción.",
        "btn_buy": "Informe Completo ($3)", 
        "btn_unlock": "Desbloquear", 
        "key_label": "Clave de Licencia",
        "h_money": "💰 Guía de Riqueza", "h_love": "❤️ Guía de Amor", "h_health": "💪 Salud", 
        "h_action": "🚀 Plan de Acción", "h_lucky": "🍀 Ítems de la Suerte"
    },
    "ja": {
        "title": "📅 その日の運勢", 
        "sub": "大切な日の運気を事前にチェックしましょう。",
        "date_label": "日付を選択", 
        "btn_anal": "分析する",
        "res_header": "🔒 今日の運勢分析結果 (Premium)", 
        "lock_msg": "その日の運気、財運、恋愛、行動指針など、すべての詳細分析は有料レポートで提供されます。",
        "btn_buy": "完全版レポート解除 ($3)", 
        "btn_unlock": "ロック解除", 
        "key_label": "ライセンスキー",
        "h_money": "💰 財運ガイド", "h_love": "❤️ 恋愛ガイド", "h_health": "💪 健康管理", 
        "h_action": "🚀 行動指針", "h_lucky": "🍀 ラッキーアイテム"
    },
    "zh": {
        "title": "📅 特定日运势", 
        "sub": "提前查看重要日子的气场。",
        "date_label": "选择日期", 
        "btn_anal": "开始分析",
        "res_header": "🔒 今日运势分析结果 (Premium)", 
        "lock_msg": "解锁完整报告，包括当日气场、财运、爱情及行动指南。",
        "btn_buy": "解锁完整报告 ($3)", 
        "btn_unlock": "解锁", 
        "key_label": "许可证密钥",
        "h_money": "💰 财运指南", "h_love": "❤️ 恋爱指南", "h_health": "💪 健康管理", 
        "h_action": "🚀 行动指南", "h_lucky": "🍀 幸运物"
    }
}
if lang not in ui: t = ui['en']
else: t = ui[lang]

st.markdown(f"<div class='day-header'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color:#cbd5e1; margin-bottom:30px;'>{t['sub']}</div>", unsafe_allow_html=True)

# 1. 입력
with st.container(border=True):
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        target_date = st.date_input(t['date_label'], min_value=date.today())
    with col_d2:
        st.write("")
        st.write("")
        check_clicked = st.button(t['btn_anal'], type="primary", use_container_width=True)

# 2. 분석
if check_clicked or st.session_state.get('day_analyzed'):
    st.session_state['day_analyzed'] = True
    
    # 일간 계산
    my_info = calculate_day_gan(st.session_state["birth_date"])
    target_info = calculate_day_gan(target_date)
    
    def map_elem(input_val):
        # 1. 이미 영어(Fire, Water 등)라면 그대로 반환 (이게 빠져서 오류가 났었습니다)
        valid_english = ["Wood", "Fire", "Earth", "Metal", "Water"]
        if input_val in valid_english:
            return input_val
            
        # 2. 한자(甲, 乙...)라면 영어로 변환
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(input_val, 'Wood') # 한자도, 영어도 아니면 기본값 Wood
    
    my_elem = map_elem(my_info['element'])
    tgt_elem = map_elem(target_info['element'])
    
    # 데이터 로드 (결과는 res에 담기지만, 잠금 해제 전까진 안 보여줌)
    res = get_relationship_data(my_elem, tgt_elem, lang)
    
    st.divider()
    st.subheader(t['res_header'])
    
    if "unlocked_day" not in st.session_state: st.session_state["unlocked_day"] = False
    
    # 🌟 [전체 잠금 로직] 🌟
    if not st.session_state["unlocked_day"]:
        # 블러 처리된 가짜 콘텐츠 (총운 + 상세 모두 블러)
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(12px); opacity: 0.5; pointer-events: none; user-select: none;'>
                <div class='card'>
                    <h2 style='color:#f472b6;'>Analysis Complete!</h2>
                    <h1>⭐⭐⭐⭐⭐</h1>
                    <p>This day brings amazing opportunities for you...</p>
                    <hr>
                    <h3>💰 Money Guide</h3>
                    <p>Today is the best day for investment...</p>
                    <h3>❤️ Love Guide</h3>
                    <p>You will meet someone special...</p>
                </div>
            </div>
            <div class='lock-overlay'>
                <h3 style='color: #f472b6;'>🔒 Premium Report</h3>
                <p style='color: #e2e8f0; margin-bottom: 20px; font-size: 1.1em;'>{t['lock_msg']}</p>
                <a href="{GUMROAD_LINK_SPECIFIC}" target="_blank" 
                   style="background-color: #ec4899; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; display: inline-block;">
                   {t['btn_buy']}
                </a>
            </div>
        </div>
        """
        st.markdown(blur_html, unsafe_allow_html=True)
        
        # 키 입력
        with st.expander(f"{t['key_label']} Input"):
            c1, c2 = st.columns([3, 1])
            with c1: k_in = st.text_input(t['key_label'], type="password", label_visibility="collapsed")
            with c2: 
                if st.button(t['btn_unlock']):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_day"] = True
                        st.success("Unlocked!")
                        st.rerun()
                    else:
                        try:
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={"product_permalink": "specific_day", "license_key": k_in}).json()
                            if r.get("success"):
                                st.session_state["unlocked_day"] = True
                                st.rerun()
                            else:
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={"product_permalink": "all-access_pass", "license_key": k_in}).json()
                                if r2.get("success"):
                                    st.session_state["unlocked_day"] = True
                                    st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: st.error("Error")
    else:
        # 🔓 [잠금 해제됨] 진짜 결과 전체 표시
        st.success("🔓 VIP Content Unlocked!")
        
        # 1. 총운 표시
        st.markdown(f"""
            <div class='card' style='border:1px solid #f472b6; text-align:center;'>
                <h2 style='color:#f472b6; margin-top:0;'>{res['t']}</h2>
                <h1 style='font-size:3.5em;'>{res['star']}</h1>
                <p style='font-size:1.3em; line-height:1.6;'>{res['d']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. 상세 정보 (탭 제거 -> 한꺼번에 나열)
        st.write("")
        
        # [재물 & 연애]
        st.markdown(f"""
            <div class='premium-box'>
                <h3 style='color:#fbbf24;'>{t['h_money']}</h3>
                <p>{res['money']}</p>
            </div>
            <div class='premium-box'>
                <h3 style='color:#f472b6;'>{t['h_love']}</h3>
                <p>{res.get('love', res.get('love_m', ''))}</p> 
            </div>
        """, unsafe_allow_html=True)
        
        # [건강 & 행동 지침]
        st.markdown(f"""
            <div class='premium-box'>
                <h3 style='color:#34d399;'>{t['h_health']}</h3>
                <p>{res['health']}</p>
            </div>
            <div class='premium-box'>
                <h3 style='color:#60a5fa;'>{t['h_action']}</h3>
                <p style='white-space: pre-line;'>{res['action']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # [행운의 아이템]
        st.markdown(f"""
            <div class='card' style='text-align:center; margin-top: 20px;'>
                <h3 style='color:#cbd5e1; margin-bottom:10px;'>{t['h_lucky']}</h3>
                <h1 style='font-size:2.5em;'>{res['lucky']}</h1>
            </div>
        """, unsafe_allow_html=True)
            
        # 인쇄 버튼
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:20px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;'>🖨️ Save Report</button></div>""", height=80)
