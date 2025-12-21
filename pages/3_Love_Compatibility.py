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
st.set_page_config(page_title="Love Compatibility | The Element", page_icon="💘", layout="wide")

# 언어 설정 (세션 상태 우선)
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

# 🔑 [마스터 키 & 구매 링크]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/love_compatibility" 
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정 (다크 테마 + 핑크 포인트)
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
        [data-testid="stSidebarNav"] span { font-size: 1.1rem !important; font-weight: 600 !important; color: #e2e8f0 !important; }
        
        .main-title {
            font-size: 2.5em; font-weight: 800; color: #f472b6; text-align: center; margin-bottom: 10px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);
        }
        .card {
            background: rgba(30, 41, 59, 0.9); border: 1px solid #f472b6; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; color: #e2e8f0; line-height: 1.6;
        }
        .vs-box {
            background: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; text-align: center;
            border: 1px solid #475569; margin-bottom: 20px;
        }
        .section-title {
            font-size: 1.3em; font-weight: bold; color: #f9a8d4; margin-top: 20px; margin-bottom: 10px;
            border-left: 4px solid #f472b6; padding-left: 10px;
        }
        
        /* 잠금 오버레이 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #f472b6;
            box-shadow: 0 0 20px rgba(244, 114, 182, 0.3);
        }
        /* 입력 필드 레이블 및 라디오 버튼 텍스트 색상 변경 */
        .stTextInput label, .stDateInput label, .stRadio label p {
            color: #e2e8f0 !important; /* 밝은 회색으로 설정하여 가독성 확보 */
            font-weight: 600 !important;
        }
        /* 라디오 버튼 옵션 텍스트 (Male, Female) 색상 */
        .stRadio div[role='radiogroup'] label div {
            color: #e2e8f0 !important;
        }
        /* 🖨️ 프린트 전용 스타일 (사이드바 숨김) */
        @media print {
            section[data-testid="stSidebar"], header, footer {
                display: none !important;
            }
            .stApp {
                background: white !important; /* 잉크 절약을 위해 흰 배경 */
                color: black !important; /* 글자는 검은색 */
            }
            .main .block-container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            .card, .vs-box {
                border: 1px solid #ccc !important;
                background: white !important;
                color: black !important;
                box-shadow: none !important;
            }
            h1, h2, h3, h4, p, div, span {
                color: black !important;
                text-shadow: none !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 함수 (He/She 성별 적용 완료)
# ----------------------------------------------------------------
# ⭐ [수정] 인자에 p_gender 추가
def get_love_report(u_elem, p_elem, lang, p_gender):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Wood": "Resource", "Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power"},
        "Earth": {"Wood": "Power", "Fire": "Resource", "Earth": "Same", "Metal": "Output", "Water": "Wealth"},
        "Metal": {"Wood": "Wealth", "Fire": "Power", "Earth": "Resource", "Metal": "Same", "Water": "Output"},
        "Water": {"Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource", "Water": "Same"},
    }
    rel_key = relations.get(u_elem, {}).get(p_elem, "Same")
    
    # ⭐ [수정] 성별에 따른 대명사 설정
    if p_gender == "Male":
        S, s, O, P = "He", "he", "him", "his" # 주어(대), 주어(소), 목적어, 소유격
    else:
        S, s, O, P = "She", "she", "her", "her"

    # 🌟 6개 국어 프리미엄 궁합 데이터 (풍성한 버전)
    reports = {
        "Same": { # 비견 (거울/친구)
    "score": 85,
    "ko": {
        "t": "🤝 거울 속의 연인: 운명적 동질감과 자존심의 이중주",
        "c": "마치 평행우주에서 온 또 다른 나를 만난 듯한 충격을 줍니다. 대화의 리듬, 유머의 결, 심지어 삶을 바라보는 가치관까지 놀라울 정도로 일치합니다. 굳이 설명하지 않아도 서로의 마음을 읽어내는 '소울메이트'이자, 세상에서 가장 든든한 내 편이 되어주는 친구 같은 연인입니다.",
        "f": "하지만 '서로 너무 닮았다'는 점이 때로는 가장 큰 장애물이 됩니다. 둘 다 자기주장과 고집이 강해 의견이 충돌하면 누구 하나 먼저 굽히려 하지 않는 팽팽한 대립이 이어집니다. 상대방에게서 자신의 단점을 발견할 때 거부감을 느끼기도 하며, 사소한 자존심 싸움이 차가운 냉전으로 번지기 쉽습니다.",
        "i": "속궁합 90점. 친구처럼 장난스럽고 편안하게 시작되지만, 일단 불이 붙으면 그 어떤 관계보다 뜨겁고 격정적입니다. 서로의 신체적 리듬과 원하는 포인트를 본능적으로 꿰뚫고 있어 말 한마디 없이도 최고의 만족감을 공유하는 파워풀한 소통을 보여줍니다.",
        "a": "1. 자존심은 잠시 접어두기: 사랑 싸움에서 이겨봤자 남는 것은 상처뿐입니다.\n2. 사과의 선제공격: '미안해'라는 짧은 한마디가 모든 갈등을 녹이는 마법의 주문이 됩니다.\n3. 함께 성장하는 데이트: 스포츠나 활동적인 취미를 함께 공유하며 에너지를 건강하게 분출하세요."
    },
    "en": {
        "t": "🤝 Mirror Lovers: A Duet of Twin Souls and Ego Battles",
        "c": "Connecting with {O} feels like discovering your long-lost reflection from a parallel universe. Your conversational rhythm, sense of humor, and core values are strikingly aligned. You are true 'Soulmates' who can read each other's minds without words, serving as both best friends and fiercely loyal partners.",
        "f": "The trap lies in being 'too similar.' With both possessing strong wills and ironclad egos, conflicts can lead to intense standoffs where neither is willing to back down. You may feel frustrated when seeing your own flaws reflected in your partner, turning petty pride into a lingering cold war.",
        "i": "Intimacy Score: 90. It begins playfully and comfortably like a friendship, but once the spark ignites, it becomes more passionate and intense than any other. You instinctively grasp each other's physical rhythms and desires, achieving a powerful connection without needing to speak.",
        "a": "1. Put the Ego Aside: Winning an argument in love only results in deep emotional scars.\n2. Preemptive Apology: A simple 'I’m sorry' acts as a magic spell that melts all tension.\n3. Dynamic Dates: Discharge your combined energy healthily through shared active hobbies and sports."
    },
    "fr": {
        "t": "🤝 Amants Miroirs : Duo d'Âmes Sœurs et de Chocs d'Egos",
        "c": "Rencontrer {O}, c'est comme trouver son double venu d'un univers parallèle. Votre rythme de conversation et vos valeurs sont en parfaite harmonie. Vous êtes de véritables 'Âmes Sœurs' qui se comprennent sans mots, à la fois meilleurs amis et partenaires dévoués.",
        "f": "Le piège est d'être 'trop semblables'. Avec deux personnalités fortes, les conflits deviennent des duels où personne ne veut céder. Voir vos propres défauts chez l'autre peut être irritant, transformant une simple dispute en une guerre froide de fierté.",
        "i": "Intimité : 90/100. Cela commence par des jeux complices, mais se transforme en une passion dévorante. Vous devinez instinctivement les désirs de l'autre, partageant une satisfaction profonde sans besoin de longs discours.",
        "a": "1. Mettez l'ego de côté : Gagner une dispute ne sert à rien si vous blessez l'autre.\n2. L'excuse préventive : Un simple 'Je suis désolé' est une formule magique contre les conflits.\n3. Activités dynamiques : Partagez des loisirs actifs pour canaliser votre énergie commune."
    },
    "es": {
        "t": "🤝 Amantes Espejo: Un Dúo de Almas Gemelas y Choques de Ego",
        "c": "Conocer a {O} es como encontrar a tu otro yo de un universo paralelo. Su ritmo de conversación y valores fundamentales están increíblemente alineados. Son verdaderas 'Almas Gemelas' que se leen la mente, siendo mejores amigos y compañeros leales al mismo tiempo.",
        "f": "La trampa está en ser 'demasiado iguales'. Al tener ambos un carácter fuerte, los conflictos pueden llevar a enfrentamientos donde ninguno quiere ceder. Puede resultar frustrante ver tus propios defectos reflejados en el otro, convirtiendo el orgullo en una guerra fría.",
        "i": "Intimidad: 90/100. Comienza de forma juguetona y relajada, pero una vez encendida la chispa, es más intensa que cualquier otra. Saben instintivamente lo que el otro desea, logrando una conexión poderosa sin palabras.",
        "a": "1. Deja el ego de lado: Ganar una discusión en el amor solo deja cicatrices emocionales.\n2. Disculpa proactiva: Un simple 'lo siento' funciona como un hechizo que derrite toda tensión.\n3. Citas activas: Canalicen su energía compartida a través de deportes y pasatiempos dinámicos."
    },
    "ja": {
        "t": "🤝 鏡の中の恋人：運命的な同質性と自我の共鳴",
        "c": "まるでパラレルワールドから来た「もう一人の自分」に出会ったような衝撃を与えます。会話のリズム、笑いのツボ、人生観まで驚くほど一致しています。説明しなくても通じ合う「ソウルメイト」であり、世界で一番の味方である親友のような恋人です。",
        "f": "しかし「似すぎている」ことが最大の障壁になることも。二人とも自我が強く頑固なため、一度意見が対立すると譲歩を知らない平行線が続きます。相手の中に自分の欠点を見つけて嫌悪感を感じたり、些細なプライドが原因で冷戦状態に陥りやすい傾向があります。",
        "i": "相性90点。友達のようにふざけ合うリラックスした関係から始まりますが、火がつくと誰よりも情熱的。相手の身体的リズムや欲求を本能的に察知しており、言葉がなくても最高の満足感を共有できるパワフルな相性です。",
        "a": "1. プライドを脇に置く：愛の喧嘩で勝っても残るのは心の傷だけです。\n2. 攻めの謝罪：短く「ごめん」と言うだけで、すべての葛등が解消する魔法になります。\n3. アクティブな趣味：スポーツや活動的な趣味を共有し、エネルギーを健康的に発散しましょう。"
    },
    "zh": {
        "t": "🤝 镜中恋人：命运般的同质感与自尊心的二重奏",
        "c": "遇见 {O} 就像是遇到了平行时空的另一个自己。谈话的节奏、幽默的共鸣点、甚至是价值观都惊人地一致。你们是不需要言语就能读懂对方的“灵魂伴侣”，也是彼此生命中最可靠、最像亲友的伴侣。",
        "f": "但“太像了”有时也是最大的障碍。两人的主观意识和固执程度不相上下，一旦产生冲突，谁都不愿先低头。在对方身上看到自己的缺点时会感到烦躁，微小的自尊心之争极易演变成漫长的冷战。",
        "i": "亲密度90分。像朋友般调皮和放松地开始，但一旦点燃激情，会比任何关系都更炽热。你们本能地了解对方的身体律动和渴望，不需要多言就能共享最高契合度的交流。",
        "a": "1. 收起自尊心：在感情争吵中赢了对方，只会留下满心伤痕。\n2. 先发制人的道歉：一句简单的“对不起”是融化所有紧张局势的魔法咒语。\n3. 充满活力的约会：一起参加体育运动或户外爱好，以健康的方式释放共同的能量。"
    }
},
        "Output": { # 식상 (헌신/표현)
    "score": 92,
    "ko": {
        "t": "💖 헌신적인 사랑: 아낌없이 주는 나무와 화사하게 피어난 꽃",
        "c": "당신이 상대방을 마치 자식처럼 금지옥엽 아끼고 보살피는 형국입니다. 당신의 무한한 지지와 헌신 속에서 상대방은 세상 어디에서도 느껴보지 못한 깊은 안정감을 느끼며 당신을 전적으로 신뢰하고 의지하게 됩니다. 당신은 주는 기쁨에서, 상대방은 받는 행복에서 삶의 의미를 찾는 조화로운 결합입니다.",
        "f": "하지만 사람의 마음인지라 '내가 이만큼 헌신했는데 너는 왜 그만큼 표현하지 않니?'라는 보상 심리가 고개를 드는 순간, 억눌렸던 서운함이 둑이 터지듯 폭발할 수 있습니다. 또한 당신의 세심한 관심이 때로는 상대의 성장을 방해하는 '간섭'이나 '통제'로 변질되어 관계를 질식시킬 위험이 있습니다.",
        "i": "정서적 교감이 육체적 결합으로 이어지는 로맨틱함의 정석입니다. 당신이 상대방을 리드하며 세심하게 봉사하는 형태를 띠며, 상대가 만족해하는 모습에서 극상의 성취감과 쾌락을 얻습니다. 분위기와 배려가 지배하는 아주 부드럽고 따뜻한 교감을 나눕니다.",
        "a": "1. 대가 없는 사랑의 연습: 베푸는 행위 자체에서 만족을 찾고 기대치를 낮추세요.\n2. 건강한 거리두기: 사랑이라는 이름의 포장지로 상대의 자유를 구속하지 마세요.\n3. 긍정적 피드백 요청: 참지 말고 상대에게 '고맙다'는 따뜻한 한마디를 주기적으로 요구하세요."
    },
    "en": {
        "t": "💖 Devoted Love: The Nurturing Giving Tree and The Blooming Flower",
        "c": "You cherish and nurture {O} with the depth of a parent's heart. Wrapped in your boundless support and devotion, {s} feels a profound sense of security found nowhere else, leading to total trust and reliance on you. It is a beautiful harmony where you find purpose in giving, and your partner finds joy in being cherished.",
        "f": "The shadow of this devotion is the 'Compensation Trap.' The moment you ask, 'I’ve given so much, why don't you do the same?', suppressed resentment can erupt. Moreover, your meticulous care may inadvertently turn into 'nagging' or 'control,' potentially suffocating {O}'s independence.",
        "i": "This is the epitome of romanticism, where emotional intimacy flows into physical connection. You take the lead with a servant's heart, deriving immense pleasure from satisfying your partner. It is a soft, warm, and deeply considerate communion.",
        "a": "1. Practice Altruism: Find joy in the act of giving itself and lower your expectations for return.\n2. Respect Boundaries: Do not let your care become a cage that stifles {O}'s growth.\n3. Vocalize Your Needs: Don't wait in silence; gently ask {O} to express their gratitude with a warm 'Thank you' regularly."
    },
    "fr": {
        "t": "💖 Amour Dévoué : L'Arbre Généreux et la Fleur Épanouie",
        "c": "Vous chérissez {O} avec la tendresse d'un parent. Grâce à votre soutien indéfectible, votre partenaire ressent une sécurité profonde et une confiance totale en vous. Un équilibre précieux où donner devient votre mission et recevoir devient son bonheur.",
        "f": "Le risque réside dans l'attente d'un retour. Si vous commencez à compter vos efforts, la déception sera amère. De plus, votre protection peut parfois se transformer en un contrôle étouffant qui freine l'autonomie de l'autre.",
        "i": "Une connexion hautement romantique. Vous menez avec douceur et dévouement, trouvant votre plaisir dans la satisfaction de l'autre. C'est un échange tendre, chaud et empreint d'une grande délicatesse.",
        "a": "1. Donnez sans compter : Appréciez l'acte de donner sans attendre de réciprocité.\n2. Laissez de l'espace : L'amour ne doit pas devenir une prison dorée.\n3. Communiquez vos besoins : Encouragez {O} à exprimer sa gratitude par des mots simples."
    },
    "es": {
        "t": "💖 Amor Devoto: El Árbol Generoso y la Flor en Crecimiento",
        "c": "Cuidas a {O} con la devoción de quien protege un tesoro. Bajo tu apoyo incondicional, tu pareja encuentra una paz y seguridad inigualables, confiando plenamente en ti. Es una armonía donde tú te realizas dando y {s} florece recibiendo.",
        "f": "El peligro aparece cuando surge el deseo de reciprocidad forzada. Si sientes que das demasiado sin recibir nada, el resentimiento estallará. Además, tu atención constante puede ser percibida como control o falta de espacio personal.",
        "i": "Es el romance puro convertido en intimidad. Tú guías y sirves, encontrando placer en la felicidad de tu pareja. La conexión es suave, cálida y profundamente emocional.",
        "a": "1. Ama sin condiciones: Encuentra la paz en el acto de dar sin llevar la cuenta.\n2. Respeta la autonomía: Tu cuidado debe ser un ala, no una cadena.\n3. Pide reconocimiento: Recuérdale a {O} lo importante que es para ti escuchar un 'gracias'."
    },
    "ja": {
        "t": "💖 献身的な愛：惜しみなく与える大樹と美しく咲く花",
        "c": "あなたが相手をまるで宝物のように慈しみ、育てる関係です。あなたの無限の支えと献身の中で、相手はこれまでにない深い安心感を得て、あなたを全面的に信頼し、頼るようになります。与える喜びと受ける幸せが完璧に調和した結びつきです。",
        "f": "しかし、「これだけしてあげたのに」という見返りを求める心が芽生えた瞬間、抑えていた不満が爆発する危険があります。また、あなたの細やかな配慮が、時として相手の成長を妨げる「干渉」や「束縛」になり、相手を息苦しくさせてしまうこともあります。",
        "i": "情緒的なつながりが肉体的な結びつきへと昇華する、究極のロマンチシズムです。あなたがリードし、奉仕する形をとり、相手が満足する姿に最高の喜びを感じます。非常に優しく、温かい共感の時間となります。",
        "a": "1. 見返りを求めない練習：与えること自体に価値を見出し、期待を抑えましょう。\n2. 健康的な距離感：愛という名の下に、相手の自由を奪わないでください。\n3. 感謝の要求：我慢せず、相手に「ありがとう」という言葉を定期的にねだりましょう。"
    },
    "zh": {
        "t": "💖 奉献之爱：无私给予的大树与灿烂绽放的花朵",
        "c": "你像呵护至宝一样守护着对方。在你无限的支持与奉献中，对方感受到了前所未有的安全感，并对你产生绝对的信任与依赖。这是一种你在给予中找到意义，而对方在接受中获得幸福的和谐结合。",
        "f": "但这种关系的隐患在于“补偿心理”。一旦你开始计较“我付出了这么多，你为什么没有回应”，积压的委屈就会爆发。此外，你无微不至的关怀有时会演变成“唠叨”或“控制”，甚至让对方感到窒息，丧失独立空间。",
        "i": "这是极致浪漫的体现，情感的交融引导着身体的契合。你在关系中主导并全心服务，从满足对方的过程中获得巨大的成就感与快感。这是一种温柔、细腻且充满关怀的亲密交流。",
        "a": "1. 练习无私：在付出的行为本身中寻找满足，降低对他人的预期。\n2. 保持健康距离：不要以爱的名义束缚对方的自由与成长。\n3. 引导对方表达：不要默默承受，试着要求对方经常说出那句温情的“谢谢”。"
    }
},
        "Wealth": { # 재성 (소유/열정)
    "score": 88,
    "ko": {
        "t": "🔥 치명적인 매력: 타오르는 소유욕과 주도권의 뜨거운 줄다리기",
        "c": "두 사람 사이에는 거부할 수 없는 강렬한 성적 인력과 자석 같은 이끌림이 존재합니다. '서로를 온전히 정복하고 소유하고 싶다'는 갈망이 사랑의 강력한 엔진이 됩니다. 첫 만남에서 전율을 느꼈거나, 이성적인 판단보다 본능적인 스파크가 먼저 튀었을 확률이 매우 높습니다.",
        "f": "관계의 핵심 키워드는 '통제'입니다. 상대를 내 방식대로 조종하거나 바꾸려 드는 순간, 상대방은 질식할 것 같은 압박감을 느끼며 탈출을 꿈꾸게 됩니다. 깊은 사랑이 집착과 근거 없는 의심으로 변질되기 쉬우며, 때로는 정서적 교감보다 물질이나 돈을 매개로 한 계산적인 관계로 흐를 위험이 있습니다.",
        "i": "속궁합 200점! 육체적 화학 반응이 정점에 달해 있습니다. 낮에 격렬하게 다투더라도 밤의 뜨거운 화해로 모든 갈등을 덮어버리는 커플입니다. 서로의 신체에 대한 탐닉과 호기심이 워낙 강해, 오랜 시간이 지나도 권태기가 쉽게 침범하지 못하는 독보적인 궁합입니다.",
        "a": "1. 소유와 구속은 별개: 사랑할수록 상대의 독립적인 사생활을 철저히 존중하세요.\n2. 금전적 투명성 확보: 현실적인 재물운이 엮인 관계이므로, 돈 문제에서 신뢰를 잃으면 관계가 뿌리째 흔들립니다.\n3. 수평적 관계 유지: 명령조의 말투나 상대를 하대하는 태도를 버리고 인격적으로 존중하세요."
    },
    "en": {
        "t": "🔥 Fatal Attraction: A High-Stakes Tug-of-War Between Passion and Possession",
        "c": f"There is an irresistible, magnetic physical pull between you and {O}. The desire to 'conquer' and completely possess one another serves as the powerful engine of your romance. It is highly likely that sparks flew instantly, with instinct prevailing over logic from your very first encounter.",
        "f": "The central challenge is 'Control.' If you attempt to manipulate or mold {O} to fit your ideals, {s} will feel suffocated and yearn for escape. Intense passion can easily degrade into obsession and groundless jealousy. Beware of letting the relationship become too transactional or focused on material gain.",
        "i": "Intimacy Score: 200/100. Your physical chemistry is off the charts. You are the classic couple that fights bitterly by day but reconciles passionately by night. Because your mutual physical infatuation is so strong, your relationship is uniquely resistant to the usual boredom of long-term unions.",
        "a": f"1. Love is Not Ownership: The more you love {P}, the more you must respect {P} private boundaries.\n2. Financial Integrity: Since this bond is tied to 'Wealth,' even minor money issues can shatter your foundation. Be transparent.\n3. Equality is Key: Drop the bossy, commanding tone and treat your partner with genuine human respect."
    },
    "fr": {
        "t": "🔥 Attraction Fatale : Un Bras de Fer entre Passion et Possession",
        "c": "Il existe entre vous une force d'attraction magnétique et charnelle irrésistible. L'envie de 'conquérir' l'autre est le moteur de votre histoire. Il est fort probable que l'étincelle ait été instantanée dès le premier regard.",
        "f": "Le 'Contrôle' est le défi majeur. Si vous tentez de manipuler l'autre, il ou elle se sentira étouffé. La passion peut vite virer à l'obsession et à la jalousie. Évitez que votre relation ne devienne une simple transaction matérielle.",
        "i": "Alchimie : 200/100 ! Une chimie physique au sommet. Vous êtes le couple qui se dispute le jour pour mieux se réconcilier passionnément la nuit. Votre fascination mutuelle vous protège durablement de la routine.",
        "a": "1. L'amour n'est pas une cage : Respectez strictement son jardin secret.\n2. Transparence totale : Les non-dits financiers sont mortels pour votre lien.\n3. Respect mutuel : Abandonnez les tons autoritaires et privilégiez l'égalité."
    },
    "es": {
        "t": "🔥 Atracción Fatal: Un Pulso entre la Pasión y la Posesión",
        "c": "Existe una atracción física magnética e irresistible entre ambos. El deseo de 'conquistar' y poseer al otro es el motor de su romance. Es muy probable que las chispas saltaran desde el primer momento, antes que cualquier lógica.",
        "f": "La clave es el 'Control'. Si intentas manipular al otro, se sentirá asfixiado y querrá huir. La pasión puede transformarse fácilmente en obsesión y celos. Eviten que la relación se vuelva puramente transaccional o basada en el dinero.",
        "i": "¡Puntuación: 200/100! Química física en su apogeo. Son la pareja que pelea intensamente de día pero se reconcilia con pasión de noche. La fascinación corporal mutua los mantiene a salvo de la monotonía.",
        "a": "1. Amar no es poseer: Respeta profundamente su privacidad y espacio personal.\n2. Honestidad financiera: Al ser una unión ligada a la 'Riqueza', los problemas de dinero son fatales. Sean claros.\n3. Respeto absoluto: Olvida los modales mandones y trata a tu pareja como a un igual."
    },
    "ja": {
        "t": "🔥 致命的な魅力：燃え上がる所有欲と主導権争い",
        "c": "二人の間には、抗いがたい磁석のような強烈な肉体的引力が存在します。「相手を完全に征服し、自分のものにしたい」という渇望が愛のエンジンです。出会った瞬間に理屈を超えた火花が散った可能性が極めて高いです。",
        "f": "核心的な課題は「コントロール」です。相手を思い通りに操ろうとすると、相手は息苦しさを感じ、逃げ出したくなります。深い愛が執着や根拠のない疑いに変質しやすく、情緒的な交流よりも金銭的な利害関係に陥る危険もあります。",
        "i": "相性200点！肉体的な化学反応が頂点に達しています。昼間に激しく衝突しても、夜の情熱的な仲直りで全てを流せるカップルです。お互いへの飽くなき探求心が強いため、マンネリ化とは無縁の独創的な相性です。",
        "a": "1. 所有と拘束は別物：愛するほどに相手のプライバシーを徹底的に尊重しましょう。\n2. 金銭的な透明性：財運が絡む相性ゆえに、お金の信頼を失うと関係が根底から崩れます。\n3. 対等な関係：命令口調や相手を見下す態度を捨て、人格的に尊重しましょう。"
    },
    "zh": {
        "t": "🔥 致命吸引力：炽热占有欲与主导权的巅峰拉锯",
        "c": "你们之间存在着无法抗拒的、磁铁般的肉体吸引力。“想要彻底征服并占有对方”的渴望是这段感情的强力引擎。极有可能在相遇的瞬间就擦出了本能的火花，甚至让理智退居其次。",
        "f": "核心挑战在于“控制”。一旦你试图操纵或改造对方，对方会感到极度窒息并产生逃离的念头。浓烈的爱意极易演变成执着与猜忌。要警惕感情变得过于物质化或陷入金钱算计之中。",
        "i": "亲密度200分！身体化学反应处于巅峰状态。你们是典型的“床头吵架床尾和”的情侣。由于对彼此身体的迷恋极深，这段关系具有天然的免疫力，很难被倦怠期入侵。",
        "a": "1. 爱不是束缚：越是深爱，越要彻底尊重对方的私人空间。\n2. 财务透明：由于这段关系与“财”相关，任何金钱上的不诚实都会动摇感情根基。\n3. 保持平等：抛弃命令式的语气和居高临下的态度，给予对方人格上的尊重。"
    }
},
        "Power": { # 관성 (존경/긴장)
    "score": 78,
    "ko": {
        "t": "⚖️ 존경과 긴장 사이: 나를 담금질하여 성장시키는 완숙한 연인",
        "c": "상대방이 당신의 삶에 올바른 이정표를 제시하고 리드하는 형태의 관계입니다. 당신은 상대에게서 느껴지는 묵직한 카리스마와 어른스러운 포용력에 깊은 신뢰와 존경심을 갖게 됩니다. 서로의 부족함을 일깨우며 더 나은 사람이 되도록 이끌어주는 '스승과 제자' 혹은 '멘토와 멘티' 같은 성숙한 커플입니다.",
        "f": "때때로 상대방의 태도가 지나치게 원칙주의적이거나 보수적으로 느껴져 숨이 막힐 수 있습니다. 상대의 진심 어린 조언이 어느 순간 날카로운 '지적'이나 따분한 '잔소리'로 들리기 시작하면 감정적 스트레스가 한계치에 도달합니다. '왜 나를 있는 그대로 봐주지 않고 가르치려고만 들까?'라는 반발심이 관계의 가장 큰 고비가 됩니다.",
        "i": "자극적이거나 화려하지는 않지만, 서로를 지켜준다는 굳건한 신뢰를 바탕으로 한 은근하고 깊은 매력이 있습니다. 찰나의 스릴보다는 정서적 '안정감'과 보호받는다는 느낌이 돋보이는 품격 있는 교감을 나눕니다.",
        "a": "1. 수용의 미학: 상대의 조언을 당신을 강하게 만드는 '입에 쓴 보약'으로 받아들여 보세요.\n2. 화법의 개선 요청: 결과만큼 과정도 중요하므로, 조금 더 부드럽고 따뜻하게 말해달라고 솔직하게 요청하세요.\n3. 사적 영역의 보호: 사랑하기 때문에 모든 것을 간섭할 수는 없습니다. 서로의 독립성을 침해하지 않을 명확한 선을 정하세요."
    },
    "en": {
        "t": "⚖️ Respect & Tension: The Mature Couple Forging Personal Growth",
        "c": f"{S} acts as a steady compass, guiding and leading your life with effective direction. You are naturally drawn to {P} heavy charisma and mature embrace, fostering a deep sense of respect. It is a high-level union where you evolve together, much like a 'Mentor-Mentee' relationship.",
        "f": f"{S} may sometimes appear overly rigid, strict, or conservative, which can feel suffocating. If {P} sincere advice starts to sound like constant judging or condescending lectures, your stress will peak. You may feel a growing resentment, wondering why you are being 'managed' rather than simply loved.",
        "i": "Instead of being wild or impulsive, the connection is built on profound emotional security and trust. It provides a deep sense of being protected and stable, which is its most alluring quality.",
        "a": "1. Practice Receptivity: Try to view advice as 'bitter medicine' that ultimately makes you stronger.\n2. Request Gentleness: Ask {O} to communicate in a softer tone to protect your feelings.\n3. Establish Boundaries: Set a clear line where interference ends and personal autonomy begins."
    },
    "fr": {
        "t": "⚖️ Respect et Tension : Un Couple de Mentorat et d'Élévation",
        "c": "Votre partenaire vous dirige avec sagesse. Vous respectez son charisme et sa maturité. Une relation 'Maître-Élève' où chaque défi devient une opportunité de grandir ensemble.",
        "f": "Il/Elle peut se montrer trop strict ou conservateur. Ses conseils peuvent ressembler à des critiques constantes, créant une pression psychologique et un sentiment d'être jugé.",
        "i": "Une relation stable et confiante plutôt que sauvage. Elle offre une sécurité émotionnelle profonde et le sentiment d'être protégé.",
        "a": "1. Écoutez sans vous braquer, comme on accepte un remède efficace mais amer.\n2. Demandez une communication plus douce pour ne pas blesser votre ego.\n3. Fixez des limites claires pour préserver votre jardin secret."
    },
    "es": {
        "t": "⚖️ Respeto y Tensión: La Pareja que Inspira Crecimiento Real",
        "c": "Tu pareja te dirige y establece el rumbo. Sientes una profunda admiración por su carisma y madurez. Es una relación de 'Maestro-Estudiante' donde ambos se elevan mutuamente.",
        "f": "Puede ser demasiado estricto o conservador. Si sus consejos empiezan a sonar como mandatos o críticas, el estrés y el resentimiento florecerán rápidamente.",
        "i": "Es una unión estable y de confianza absoluta más que de pasión desenfrenada. Ofrece una paz emocional muy profunda.",
        "a": "1. Escucha con apertura; considera sus palabras como un consejo valioso para tu futuro.\n2. Pide una comunicación más suave para que el mensaje llegue sin dolor.\n3. Establece límites de privacidad para evitar sentirte controlado."
    },
    "ja": {
        "t": "⚖️ 尊敬と緊張：私を鍛え、成長させてくれる熟成した関係",
        "c": "相手があなたの人生に正しい道標を示し、リードしてくれる関係です. 相手の持つ重厚なカリスマ性と大人っぽい包容力に、深い信頼と尊敬の念を抱きます. お互いを高め合う「メンターとメンティー」のような成熟したカップルです.",
        "f": "時として相手の態度が厳格すぎたり、保守的に感じられたりして息苦しくなることがあります. 助言が「小言」や「批判」に聞こえ始めると、心理的ストレスが爆発し、「なぜありのままの私を認めてくれないのか」という不満が生じます.",
        "i": "刺激的ではありませんが、守られているという確かな実感を伴う深い魅力があります. スリルよりも「安定感」と信頼関係が際立つ大人の相性です.",
        "a": "1. 素直に受け入れる：良薬口に苦しだと思い、耳を傾けてみましょう.\n2. 伝え方のリクエスト：もっと優しく、温かい言葉で話してほしいと素直に伝えて.\n3. 境界線を引く：お互いの独立性を尊重し、干渉しすぎないルールを作りましょう."
    },
    "zh": {
        "t": "⚖️ 尊敬与紧张：磨砺自我、共同成长的深厚羁绊",
        "c": "对方为你的生活指明方向并引导着你。你对TA展现出的强大魅力和成熟包容心深感敬佩. 这是一个像“导师与学生”一样互补成长、共同进步的成熟关系.",
        "f": "对方有时表现得过于原则化或保守，让你感到窒息. 当TA的真心建议演变为尖锐的“指责”或枯燥的“唠叨”时，压力会达到顶点. 你会怀疑对方是在爱人还是在教训人.",
        "i": "虽然并不追求感官刺激，但基于绝对信任的亲密感非常稳固. 这种相性强调的是“安全感”和被守护的幸福感.",
        "a": "1. 放下防御心理：将建议视为苦口良药.\n2. 温柔沟通：明确要求对方在给予建议时使用更委婉、更温暖的措辞.\n3. 设定个人界限：划定互不干涉的底线，保护彼此的独立空间."
    }
},
        "Resource": { # 인성 (수용/치유)
    "score": 96,
    "ko": {
        "t": "🍼 무한한 사랑의 안식처: 어머니의 품 같은 힐링 소울메이트",
        "c": "상대방이 당신의 존재 자체를 긍정하며 헌신적으로 뒷바라지해주는 관계입니다. 당신이 굳이 애써 증명하지 않아도 상대는 당신의 모든 허물을 이해하고 용서하며 감싸 안아줍니다. 세상의 거친 풍파 속에서 언제든 돌아가 쉴 수 있는 가장 편안한 요새이자, 지친 영혼을 달래주는 완벽한 '힐링 파트너'입니다.",
        "f": "하지만 관계가 너무 안온하고 편안하다 보니 긴장감이 사라져 권태기가 소리 없이 찾아올 수 있습니다. 당신이 상대의 헌신적인 사랑을 '당연한 권리'로 여기며 나태해지는 순간, 상대방은 깊은 회의감에 빠질 것입니다. 때로는 상사의 보살핌이 '과잉보호'로 변질되어 당신의 성장을 가로막거나 사생활을 간섭한다는 느낌을 주어 답답함을 유발할 수 있습니다.",
        "i": "강렬한 육체적 자극보다는 영혼이 꽉 차는 듯한 정서적인 포만감이 관계의 핵심입니다. 서로의 심장 소리를 들으며 가만히 안고만 있어도 세상 부러울 것 없는 행복을 느낍니다. 부드럽고 따뜻하며, 서로를 어루만지는 세심한 스킨십을 통해 깊은 안도감을 공유합니다.",
        "a": "1. '당연한 것'은 없습니다: 매 순간 상대의 배려에 진심 어린 감사를 표현하세요.\n2. 건강한 긴장감 조성: 가끔은 익숙한 일상에서 벗어나 낯선 장소에서 설레는 데이트를 즐기세요.\n3. 정서적 홀로서기: 상대에게 모든 결정을 맡기기보다 스스로 판단하고 행동하는 독립적인 매력을 보여주세요."
    },
    "en": {
        "t": "🍼 A Sanctuary of Infinite Love: The Healing Soulmate Like a Mother's Embrace",
        "c": f"{S} affirms your very existence and supports you with unwavering devotion. You don’t have to prove anything; {s} understands your flaws and forgives you before you even ask. It is a fortress where you can always find peace amidst the world's chaos—a perfect 'Healing Partner' who soothes your tired soul.",
        "f": f"However, such profound comfort can lead to a loss of spark, allowing boredom to creep in unnoticed. If you start taking {P} devotion for granted and become lazy in the relationship, a crisis will inevitably follow. At times, {P} care may cross the line into 'over-protection,' making you feel smothered or hindered in your personal growth.",
        "i": "Emotional fulfillment takes precedence over physical thrill. Simply holding each other and listening to the rhythm of your hearts brings a supreme sense of happiness. Your intimacy is characterized by gentle, warm, and deeply considerate touches that reinforce a powerful sense of security.",
        "a": "1. Nothing is Guaranteed: Express heartfelt gratitude for {P} small acts of kindness every single day.\n2. Reignite the Spark: Break the routine by planning exciting dates in unfamiliar settings.\n3. Cultivate Independence: Show your attractive, self-reliant side rather than delegating every decision to {O}."
    },
    "fr": {
        "t": "🍼 Un Sanctuaire d'Amour Infini : L'Âme Sœur Guérisseuse",
        "c": "Votre partenaire affirme votre existence et vous soutient avec un dévouement total. C'est une forteresse où vous trouvez la paix, un véritable 'Partenaire de Guérison' qui apaise votre âme fatiguée, comme dans les bras d'une mère.",
        "f": "Le confort absolu peut éteindre la flamme. Si vous considérez son amour comme un dû, la relation s'essoufflera. Attention à ce que sa protection ne devienne pas une cage dorée qui freine votre épanouissement personnel.",
        "i": "La plénitude émotionnelle l'emporte sur l'excitation physique. Le simple fait de rester l'un contre l'autre apporte un bonheur immense. Une connexion douce, chaude et protectrice.",
        "a": "1. Pratiquez la gratitude : Ne tenez jamais son soutien pour acquis.\n2. Créez la surprise : Sortez de la routine pour maintenir le désir.\n3. Restez autonome : Ne reposez pas toutes vos décisions sur ses épaules."
    },
    "es": {
        "t": "🍼 Un Santuario de Amor Infinito: El Alma Gemela que Sana",
        "c": "Tu pareja valora tu esencia y te apoya con una devoción incondicional. Es un refugio donde siempre puedes descansar; un 'Compañero de Sanación' que calma tu espíritu, tal como el abrazo de una madre protege a su hijo.",
        "f": "La comodidad extrema puede llevar a la apatía. Si dejas de esforzarte porque te sientes 'seguro', la pasión morirá. A veces, su cuidado puede sentirse como sobreprotección, limitando tu independencia.",
        "i": "La satisfacción emocional es la clave. El simple contacto físico lleno de ternura es suficiente para sentir felicidad plena. Una intimidad suave, cálida y profundamente reconfortante.",
        "a": "1. Nada es obvio: Agradece cada detalle y gesto de amor que recibas.\n2. Rompe la rutina: Planifica citas diferentes para mantener viva la emoción.\n3. Sé independiente: Mantén tu propia identidad y toma tus propias decisiones."
    },
    "ja": {
        "t": "🍼 無限の愛の安식処：母の懐のような癒しのソウルメイト",
        "c": "相手があなたの存在そのものを肯定し、献身的に支えてくれる関係です。あなたが無理に自分を証明しなくても、相手はすべての欠点を理解し、包み込んでくれます。荒波の中でもいつでも戻って休める心の要塞であり、疲れた魂を癒してくれる最高のパートナーです。",
        "f": "しかし、あまりに居心地が良すぎると緊張感が失われ、マンネリ化が進む恐れがあります。相手の献身を「当然の権利」だと思い始めると、関係に亀裂が入ります。時として、相手の愛が「過保護」になり、あなたの成長を妨げているように感じて息苦しくなることもあります。",
        "i": "肉体的な刺激よりも、心が満たされるような精神的な満足感が大きいです。ただ抱きしめ合っているだけで、この上ない幸せを感じます。優しく温かい、お互いをいたわる繊細なスキン십を通じて深い安らぎを共有します。",
        "a": "1. 「当たり前」を捨てる：毎日の小さな配慮に対して、心からの感謝を言葉にしましょう。\n2. 緊張感の演出：たまには日常を離れ、新鮮な場所でドキドキするデートを楽しんで。\n3. 自立心を見せる：すべてを相手に委ねるのではなく、自分の足で立つ強さを見せることで魅力が増します。"
    },
    "zh": {
        "t": "🍼 无限爱意的避风港：如同母爱般的治愈系灵魂伴侣",
        "c": "对方无条件地肯定你的存在，并全心全意地为你付出。你无需刻意证明自己，TA也能包容并接纳你的一切。这是你在纷扰世界中随时可以停靠的港湾，是抚慰疲惫心灵的完美“治愈合伙人”。",
        "f": "然而，过于安逸的环境容易让关系丧失活力，导致倦怠期悄然而至。当你把对方的付出视为“理所当然”而变得懒散时，危机便会降临。有时这种呵护会演变成“过度保护”，让你感到被束缚，甚至阻碍了你的个人成长。",
        "i": "情感上的饱满远胜于感官上的刺激。仅仅是相拥而眠、倾听彼此的心跳，就能感到无比的幸福。你们的亲密关系充满了温柔、细腻和关怀，通过温暖的肢体接触共享那份深层的安全感。",
        "a": "1. 拒绝理所当然：请时刻对对方的体贴表达真诚的谢意。\n2. 制造新鲜感：偶尔跳出舒适圈，去陌生的地方进行一场令人心跳加速的约会。\n3. 保持独立人格：不要事事依赖对方，展现出你独立决断、富有主见的一面，这会让你更有魅力。"
    }
},
    }
    
    base_data = reports.get(rel_key, reports["Same"])
    data = base_data.get(lang, base_data["en"])
    
    return {
        "score": base_data["score"],
        "title": data['t'],
        "chemistry": data['c'],
        "conflict": data['f'],
        "intimacy": data['i'],
        "advice": data['a']
    }
    
# ----------------------------------------------------------------
# 4. 사이드바 (언어 설정 - 통일 완료!)
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

# UI 텍스트 (6개 국어)
ui = {
    "ko": {
        "title": "💘 사랑 궁합 분석", "sub": "두 사람의 영혼, 케미, 미래를 꿰뚫어보는 심층 리포트",
        "p_info": "상대방 정보 입력", "p_name": "상대방 이름", "p_dob": "생년월일", "p_gender": "성별",
        "lock_title": "🔒 궁합 리포트 잠금 (VIP)", "lock_msg": "두 사람의 속궁합, 갈등 원인, 미래 조언을 확인하세요.",
        "btn_buy": "전체 리포트 해제 ($3)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "analyze": "궁합 분석하기", "h_chem": "🔮 성격과 케미", "h_conf": "⚔️ 갈등 포인트", 
        "h_inti": "💋 속궁합 & 애정", "h_adv": "🚀 관계를 위한 조언"
    },
    "en": {
        "title": "💘 Love Compatibility", "sub": "Deep analysis of souls, chemistry, and future.",
        "p_info": "Partner Info", "p_name": "Name", "p_dob": "DOB", "p_gender": "Gender",
        "lock_title": "🔒 VIP Report Locked", "lock_msg": "Unlock intimacy, conflict points, and future advice.",
        "btn_buy": "Unlock Report ($3)", "btn_unlock": "Unlock", "key_label": "License Key",
        "analyze": "Analyze", "h_chem": "🔮 Chemistry", "h_conf": "⚔️ Conflict", 
        "h_inti": "💋 Intimacy", "h_adv": "🚀 Advice"
    },
    "fr": {
        "title": "💘 Compatibilité Amoureuse", "sub": "Analyse approfondie des âmes et de la chimie.",
        "p_info": "Info Partenaire", "p_name": "Nom", "p_dob": "Date de Naissance", "p_gender": "Genre",
        "lock_title": "🔒 Rapport VIP", "lock_msg": "Débloquez l'intimité et les conseils.",
        "btn_buy": "Débloquer ($3)", "btn_unlock": "Déverrouiller", "key_label": "Clé",
        "analyze": "Analyser", "h_chem": "🔮 Chimie", "h_conf": "⚔️ Conflits", 
        "h_inti": "💋 Intimité", "h_adv": "🚀 Conseils"
    },
    "es": {
        "title": "💘 Compatibilidad Amorosa", "sub": "Análisis profundo de almas y química.",
        "p_info": "Info Pareja", "p_name": "Nombre", "p_dob": "Fecha Nacimiento", "p_gender": "Género",
        "lock_title": "🔒 Reporte VIP", "lock_msg": "Desbloquea intimidad y consejos.",
        "btn_buy": "Desbloquear ($3)", "btn_unlock": "Desbloquear", "key_label": "Clave",
        "analyze": "Analizar", "h_chem": "🔮 Química", "h_conf": "⚔️ Conflictos", 
        "h_inti": "💋 Intimidad", "h_adv": "🚀 Consejos"
    },
    "ja": {
        "title": "💘 恋愛相性診断", "sub": "魂、相性、未来を深く分析。",
        "p_info": "相手の情報", "p_name": "名前", "p_dob": "生年月日", "p_gender": "性別",
        "lock_title": "🔒 VIPレポート", "lock_msg": "親密さ、葛藤、未来のアドバイスを解除。",
        "btn_buy": "解除 ($3)", "btn_unlock": "解除", "key_label": "キー",
        "analyze": "分析する", "h_chem": "🔮 相性", "h_conf": "⚔️ 葛藤", 
        "h_inti": "💋 親密さ", "h_adv": "🚀 アドバイス"
    },
    "zh": {
        "title": "💘 恋爱契合度", "sub": "深度分析灵魂、化学反应和未来。",
        "p_info": "伴侣信息", "p_name": "姓名", "p_dob": "出生日期", "p_gender": "性别",
        "lock_title": "🔒 VIP报告", "lock_msg": "解锁亲密度、冲突点和建议。",
        "btn_buy": "解锁 ($3)", "btn_unlock": "解锁", "key_label": "密钥",
        "analyze": "分析", "h_chem": "🔮 化学反应", "h_conf": "⚔️ 冲突点", 
        "h_inti": "💋 亲密度", "h_adv": "🚀 建议"
    }
}
if lang not in ui: t = ui['en']
else: t = ui[lang]

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#cbd5e1; margin-bottom:30px;'>{t['sub']}</div>", unsafe_allow_html=True)

# 1. 상대방 정보 입력
with st.container(border=True):
    st.subheader(t['p_info'])
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input(t['p_name'])
        p_dob = st.date_input(t['p_dob'], min_value=date(1950,1,1), value=date(1995,1,1))
    with c2:
        p_gender = st.radio(t['p_gender'], ["Male", "Female"], horizontal=True)
    
    analyze_btn = st.button(t['analyze'], type="primary", use_container_width=True)

# 2. 분석 및 결과
if analyze_btn or st.session_state.get('love_analyzed'):
    if not p_name:
        st.warning("Please enter partner's name.")
        st.stop()
        
    st.session_state['love_analyzed'] = True
    
    # 사주 계산
    my_info = calculate_day_gan(st.session_state["birth_date"])
    pt_info = calculate_day_gan(p_dob)
    
    # ⭐ [수정] 한자와 영어를 모두 처리하는 안전한 변환 함수
    def map_elem(input_val):
        # 1. 이미 영어라면 그대로 반환
        valid_english = ["Wood", "Fire", "Earth", "Metal", "Water"]
        if input_val in valid_english:
            return input_val
        # 2. 한자라면 영어로 변환
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(input_val, 'Wood') # 기본값 설정

    my_elem = map_elem(my_info['element'])
    pt_elem = map_elem(pt_info['element'])
    
    # 결과 가져오기
    # ⭐ [수정] 성별 정보(p_gender)를 함수에 전달해야 He/She가 적용됩니다!
    res = get_love_report(my_elem, pt_elem, lang, p_gender)
    
    st.divider()
    
    # VS 박스 (나 vs 상대)
    c1, c2, c3 = st.columns([1, 0.2, 1])
    with c1:
        st.markdown(f"<div class='vs-box'><b>ME</b><br>{st.session_state['user_name']}<br><span style='color:#f472b6'>{my_elem}</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='text-align:center; padding-top:25px; font-size:1.5em;'>❤️</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='vs-box'><b>PARTNER</b><br>{p_name}<br><span style='color:#f472b6'>{pt_elem}</span></div>", unsafe_allow_html=True)

    if "unlocked_love" not in st.session_state: st.session_state["unlocked_love"] = False
    
    # 🔒 잠금 상태
    if not st.session_state["unlocked_love"]:
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(12px); opacity: 0.5; pointer-events: none;'>
                <div class='card'>
                    <h2 style='color:#f472b6;'>Score: 95/100</h2>
                    <h3>🔮 Chemistry</h3>
                    <p>You two are destined to be together. The sparks fly immediately...</p>
                    <h3>💋 Intimacy</h3>
                    <p>Passion is high and satisfaction is guaranteed...</p>
                </div>
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
                if st.button(t['btn_unlock'], type="primary", use_container_width=True):
                    # 1. 마스터 키 (무제한) 확인
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_love"] = True
                        st.success("Master Unlocked!")
                        st.rerun()
                    else:
                        try:
                            # 2. 단품(Love Compatibility) 키 확인 (3회 제한)
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={
                                                  "product_permalink": "love_compatibility", 
                                                  "license_key": k_in, 
                                                  "increment_uses_count": "true" # 👈 카운트 증가
                                              }).json()
                            
                            if r.get("success"):
                                if r.get("uses", 0) > 3: # 🚨 3회 제한 로직
                                    st.error("🚫 Usage limit exceeded (Max 3)")
                                else:
                                    st.session_state["unlocked_love"] = True
                                    st.rerun()
                            else:
                                # 3. 올패스(All-Access) 키 확인 (합산 10회 제한)
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={
                                                       "product_permalink": "all-access_pass", 
                                                       "license_key": k_in, 
                                                       "increment_uses_count": "true" # 👈 카운트 증가
                                                   }).json()
                                
                                if r2.get("success"):
                                    if r2.get("uses", 0) > 10: # 🚨 합산 10회 제한 로직
                                        st.error("🚫 Usage limit exceeded (Max 10)")
                                    else:
                                        st.session_state["unlocked_love"] = True
                                        st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: 
                            st.error("Connection Error")
    else:
        # 🔓 해제 상태
        st.success("🔓 VIP Report Unlocked!")
        
        # 점수 표시
        st.markdown(f"""
            <div style='text-align:center; margin-bottom:30px;'>
                <h1 style='font-size:4em; color:#f472b6; margin:0;'>{res['score']} / 100</h1>
                <h2 style='margin-top:10px;'>{res['title']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # 상세 내용 (카드 스타일)
        st.markdown(f"<div class='section-title'>{t['h_chem']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>{res['chemistry']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='section-title'>{t['h_conf']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>{res['conflict']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='section-title'>{t['h_inti']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>{res['intimacy']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='section-title'>{t['h_adv']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card' style='border-color:#fbbf24;'>{res['advice']}</div>", unsafe_allow_html=True)
        
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:30px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;'>🖨️ Save Report</button></div>""", height=80)
