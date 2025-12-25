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

# 🔑 [마스터 키 & 구매 링크 설정]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/2026_forecast"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

st.set_page_config(page_title="2026 Forecast | The Element", page_icon="🔮", layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = os.environ.get("LANGUAGE", "en")
lang = st.session_state["lang"]

# ✅ 공통 CSS 먼저
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

.stApp {
    background-color: #7f1d1d;
    color: #fefefe;
    font-family: 'Gowun Batang', serif;
}

section[data-testid="stSidebar"] {
    background-color: #991b1b;
    border-right: 1px solid #7f1d1d;
}

section[data-testid="stSidebar"] * {
    color: #fefefe !important;
}

.page-title {
    font-size: 3.0em;
    font-weight: 800;
    margin-bottom: 12px;
    color: #fefefe;
}

.page-subtitle {
    font-size: 1.25em;
    color: #f3dcdc;
    margin-bottom: 35px;
}
</style>
""", unsafe_allow_html=True)

# ✅ 로고는 components.html
components.html("""
<style>
@keyframes subtleShake {
  0% { transform: translate(0, 0); }
  50% { transform: translate(1px, -1px) rotate(-0.5deg); }
  100% { transform: translate(0, 0); }
}
.animated-logo {
  width: 360px;
  max-width: 90%;
  margin: auto;
  display: block;
  animation: subtleShake 0.3s ease-in-out infinite;
  animation-delay: 5s;
  border-radius: 20px;
  box-shadow: 0 0 40px rgba(0,0,0,0.4);
}
.logo-wrapper {
  text-align: center;
  margin-top: -5px;
  margin-bottom: 30px;
  background: linear-gradient(#D41515, #7f1d1d, #ED0505);
  padding: 15px 20px;
  border-radius: 30px;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
}
</style>

<div class="logo-wrapper">
  <img src="https://raw.githubusercontent.com/1country/global-saju-test/main/images/Sign1.jpg"
       alt="FutureNara.com"
       class="animated-logo" />
</div>
""", height=220)

# ✅ 타이틀
st.markdown("""
<div class="page-title">The Element: 2026 Forecast</div>
<div class="page-subtitle">Discover your destiny for the year ahead</div>
""", unsafe_allow_html=True)
/* 기본 텍스트 */
.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stText {
    color: #fefefe !important;
}

/* 테이블 */
div[data-testid="stTable"] td {
    color: #fefefe !important;
}

div[data-testid="stTable"] th {
    color: #fde68a !important;
    font-weight: 700;
}

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #f8fafc !important;
        }

        [data-testid="stSidebarNav"] span {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #fefefe !important;
            padding-top: 5px;
            padding-bottom: 5px;
        }

        .main-title {
            font-size: 3.0em;
            color: #fefefe;
            font-weight: 800;
            margin-bottom: 10px;
            font-family: 'Gowun Batang', serif;
        }

        .sub-desc {
            font-size: 1.3em;
            color: #e2e8f0;
            margin-bottom: 40px;
            font-weight: 500;
        }

        .stTextInput label p,
        .stDateInput label p,
        .stTimeInput label p,
        .stRadio label p,
        .stCheckbox label p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #fefefe !important;
        }

        .card {
            background: #991b1b;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #b91c1c;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
            font-family: 'Gowun Batang', serif;
            color: #fefefe;
        }

        .stButton button {
            width: 100%;
            height: 50px;
            font-weight: bold;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s;
            background-color: #b91c1c;
            color: white;
            border: none;
        }

        .stButton button:hover {
            background-color: #7f1d1d;
        }

        .stLinkButton a {
            width: 100%;
            height: 50px;
            font-weight: bold;
            border-radius: 8px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            background-color: #be123c;
            color: white;
        }

        h1, h2, h3, h4, p {
            color: #fefefe;
        }
    </style>
""", unsafe_allow_html=True)

# FutureNara 로고 사이드바 상단 고정
# 🟡 FutureNara.com 간판을 사이드바 가장 위에 고정 배치
st.markdown("""
    <style>
        /* 사이드바 가장 위에 고정될 영역 */
        div[data-testid="stSidebar"]::before {
            content: "🌟 FutureNara.com";
            display: block;
            text-align: center;
            font-size: 1.4rem;
            text-shadow: 1px 1px 3px #00000055;
            font-weight: 800;
            color: gold;
            margin-bottom: 1rem;
            margin-top: 0.5rem;
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
            "ko": "당신은 만물의 시작과 성장을 상징하는 '나무(Wood)'의 기운을 타고났습니다. 하늘을 향해 뻗어 나가는 나무처럼 강한 추진력과 향상심을 가지고 있으며, 새로운 일을 기획하고 창조하는 데 탁월한 재능이 있습니다. 성품이 인자하고 측은지심이 있어 주변 사람들을 따뜻하게 보살피는 리더십을 발휘합니다. 다만, 굽히기보다 부러지기를 택하는 강직함 때문에 때로는 융통성이 부족하다는 평을 듣기도 하지만, 이는 당신이 가진 올곧은 신념의 증거이기도 합니다.",
            "en": "You embody the essence of 'Wood,' symbolizing the beginning of all life and upward growth. Much like a tree reaching for the sky, you possess powerful drive and a constant desire for self-improvement. You have an exceptional talent for planning and creating new ventures. Your benevolent nature and deep empathy allow you to lead others with warmth and compassion. While your steadfast integrity—choosing to break rather than bend—can sometimes be perceived as stubbornness, it is a testament to your unwavering principles and honesty.",
            "fr": "Vous incarnez l'essence du 'Bois', symbolisant le renouveau et la croissance ascendante. Tel un arbre s'élançant vers le ciel, vous possédez un dynamisme puissant et un désir constant de dépassement. Vous avez un talent exceptionnel pour planifier et créer de nouveaux projets. Votre nature bienveillante et votre profonde empathie vous permettent de diriger les autres avec chaleur. Bien que votre intégrité rigide — préférant rompre que de plier — puisse parfois passer pour de l'inflexibilité, c'est la preuve de vos principes inébranlables.",
            "es": "Encarnas la esencia de la 'Madera', que simboliza el comienzo de la vida y el crecimiento hacia arriba. Como un árbol que busca el cielo, posees un impulso poderoso y un deseo constante de superación. Tienes un talento excepcional para planificar y crear nuevos proyectos. Tu naturaleza benevolente y profunda empatía te permiten liderar a otros con calidez. Aunque tu integridad inquebrantable —prefiriendo romperse antes que doblarse— a veces puede verse como falta de flexibilidad, es testimonio de tus firmes principios.",
            "ja": "あなたは万物の始まりと成長を象徴する「木（Wood）」の気運を持って生まれました。空に向かって伸びる木のように強い推進力と向上心を持ち、新しいことを企画し創造することに卓越した才能を発揮します。慈悲深く、他人を思いやる心があるため、周囲を温かく見守るリーダーシップを持っています。曲がるよりは折れることを選ぶ潔さゆえに、時に融통性に欠けると評価されることもありますが、それはあなたが持つ真っ直ぐな信念の証でもあります。",
            "zh": "你命中带有‘木’的基因，象征着万物的起源与勃勃生机。正如向天空伸展的树木，你拥有强大的推动力和进取心，在策划与创新方面天赋异禀。你天性仁慈，富有同情心，能够以温暖的领导力关怀身边的人。虽然你刚正不阿、宁折不弯的性格有时会被认为缺乏灵活性，但这正证明了你那如青松般坚定的信念与正直的品格。"
        },
        "Fire": {
            "ko": "당신은 세상을 밝히고 따뜻하게 만드는 '불(Fire)'의 기운을 타고났습니다. 타오르는 불꽃처럼 뜨거운 열정과 예술적 감각을 지녔으며, 자신의 감정과 생각을 대중 앞에 표현하는 능력이 매우 뛰어납니다. 예의를 중시하고 매사에 명확하고 정직한 태도를 보이며, 특유의 명랑함으로 주변 분위기를 환하게 환기시키는 리더입니다. 다만, 순간적으로 달아올랐다 식는 급한 성미나 감정 기복을 다스리는 지혜가 필요하지만, 당신의 그 폭발적인 에너지는 불가능해 보이는 일도 가능하게 만드는 기적의 원동력입니다.",
            "en": "You embody the spirit of 'Fire,' bringing light and warmth to the world. Much like a flickering flame, you possess burning passion and keen artistic intuition, with an exceptional ability to express your thoughts and emotions to the public. You value etiquette and maintain a clear, honest attitude in all dealings, acting as a leader who brightens the atmosphere with your natural cheerfulness. While you may need the wisdom to manage an impulsive temper or emotional fluctuations, your explosive energy is the miraculous driving force that makes the impossible possible.",
            "fr": "Vous incarnez l'esprit du 'Feu', apportant lumière et chaleur au monde. Telle une flamme vacillante, vous possédez une passion ardente et une intuition artistique aiguisée, avec une capacité exceptionnelle à exprimer vos pensées et émotions. Vous valorisez l'étiquette et maintenez une attitude claire et honnête, agissant comme un leader qui illumine l'atmosphère par sa gaieté naturelle. Bien que vous puissiez avoir besoin de sagesse pour gérer un tempérament impulsif, votre énergie explosive est la force motrice miraculeuse qui rend possible l'impossible.",
            "es": "Encarnas el espíritu del 'Fuego', aportando luz y calidez al mundo. Como una llama ardiente, posees una pasión vibrante y una aguda intuición artística, con una capacidad excepcional para expresar tus pensamientos y emociones ante los demás. Valoras la etiqueta y mantienes una actitud clara y honesta, actuando como un líder que ilumina el ambiente con su alegría natural. Aunque necesites sabiduría para manejar un temperamento impulsivo o cambios emocionales, tu energía explosiva es la fuerza milagrosa que hace que lo imposible sea posible.",
            "ja": "あなたは世界を照らし、温める「火（Fire）」の気運を持って生まれました。燃え上がる炎のように熱い情熱と芸術的なセンスを持ち、自分の感情や考えを表現する能力に非常に長けています。礼儀を重んじ、何事にも明確で正直な態度を見せ、特有の明るさで周囲の雰囲気を一変させるリーダーです。瞬時に熱くなり冷めやすい短気な面や感情の起伏をコントロールする知恵が必要ですが、その爆発的なエネルギーは不可能に見えることも可能にする奇跡の原動力です。",
            "zh": "你命中带有‘火’的基因，象征着照亮世界的万丈光芒。正如熊熊燃烧的火焰，你拥有炽热的热情和敏锐 compaction 的艺术直觉，在公开表达情感与思想方面具有卓越的天赋。你极其重视礼仪，为人处事光明磊落，以特有的开朗性格带动周围的气氛。虽然有时需要智慧来克制瞬间爆发的急躁情绪或情感波动，但你那爆发性能量正是化腐朽为神奇、变不可能为可能的强大驱动力。"
        },
        "Earth": {
            "ko": "당신은 만물을 품고 길러내는 어머니 같은 '흙(Earth)'의 기운을 타고났습니다. 광활한 대지처럼 넓은 포용력과 중후한 매력을 지니고 있으며, 신용을 목숨처럼 중시하여 주변 사람들로부터 깊은 신뢰를 받는 '중재자'입니다. 매사에 서두르지 않고 묵직하게 자리를 지키는 안정감을 바탕으로 조직의 중심을 잡는 역할을 탁월하게 수행합니다. 다만, 생각이 너무 깊어 때로는 결단이 늦어지거나 변화를 두려워하는 보수적인 면도 있지만, 한 번 결심한 일은 끝까지 밀고 나가는 끈기는 누구도 따라올 수 없는 당신만의 강력한 무기입니다.",
            "en": "You embody the essence of 'Earth,' the nurturing force that embraces and fosters all life. Much like the vast and steady ground, you possess immense inclusivity and a dignified presence. You value trust above all else, acting as a reliable 'mediator' who earns deep respect from those around you. With your calm and grounded nature, you excel at being the stabilizing force in any organization. While your deep contemplation may sometimes lead to slow decision-making or a resistance to change, your unparalleled perseverance in following through on your commitments is a powerful weapon that no one else can match.",
            "fr": "Vous incarnez l'essence de la 'Terre', la force nourricière qui embrasse et favorise toute vie. Tout comme le sol vaste et stable, vous possédez une immense inclusivité et une présence digne. Vous valorisez la confiance avant tout, agissant comme un 'médiateur' fiable qui gagne le respect profond de son entourage. Grâce à votre nature calme et ancrée, vous excellez à être la force stabilisatrice de toute organisation. Bien que votre profonde réflexion puisse parfois mener à une prise de décision lente, votre persévérance inégalée à respecter vos engagements est une arme puissante que nul autre ne peut égaler.",
            "es": "Encarnas la esencia de la 'Tierra', la fuerza nutritiva que abraza y fomenta toda la vida. Al igual que el suelo vasto y estable, posees una inmensa inclusividad y una presencia digna. Valoras la confianza por encima de todo, actuando como un 'mediador' confiable que se gana el respeto profundo de quienes lo rodean. Con tu naturaleza tranquila y centrada, destacas por ser la fuerza estabilizadora en cualquier organización. Aunque tu profunda reflexión a veces puede llevarte a tomar decisiones lentas, tu perseverancia inigualable para cumplir tus compromisos es un arma poderosa que nadie más puede igualar.",
            "ja": "あなたは万物を包み込み、育てる母なる「土（Earth）」の気運を持って生まれました。広大な大地のように広い包容力と重厚な魅力を持ち、信用を何よりも重んじるため、周囲から深い信頼を得る「仲裁者」です。何事にも急がず、どっしりと構える安定感を活かし、組織の中心を守る役割を卓越して果たします。考えが深すぎて時に決단이 늦어지거나、変化を恐れる保守的な面もありますが、一度決心したことを最後までやり遂げる忍耐強さは、誰にも真似できないあなただけの強力な武器です。",
            "zh": "你命中带有‘土’的基因，象征着孕育万物、厚德载物的母性力量。正如广袤无垠的大地，你拥有极强的包容力和稳重的魅力。你视信用如生命，是深受周围人信赖的‘协调者’。凭借不急不躁、处变不惊的定力，你在团队中始终扮演着中流砥柱的角色。虽然深思熟虑有时会导致决策稍慢，或表现出畏惧改变的保守倾向，但那种一旦下定决心便绝不言弃的韧性，是你通往成功最强大的武器。"
        },
        "Metal": {
            "ko": "당신은 예리한 칼날과 단단한 바위를 상징하는 '쇠(Metal)'의 기운을 타고났습니다. 흐트러짐 없는 결단력과 강한 의지를 지니고 있으며, 한 번 맺은 인연과 약속을 끝까지 지켜내는 의리파입니다. 매사에 완벽을 기하며 공과 사를 명확히 구분하는 냉철한 이성을 바탕으로 조직의 기강을 잡고 문제를 해결하는 '해결사' 역할을 수행합니다. 다만, 자신과 타인에게 엄격한 잣대를 대는 완벽주의 성향 때문에 차갑다는 오해를 사기도 하지만, 그 내면에는 누구보다 정의롭고 속이 깊은 따뜻한 진심이 숨겨져 있습니다.",
            "en": "You embody the essence of 'Metal,' symbolizing sharp blades and solid rock. You possess unwavering decisiveness and a powerful will, acting as a person of great integrity who honors commitments and relationships to the end. With a commitment to perfection and a rational mind that clearly distinguishes between public and private matters, you excel as a 'troubleshooter' who maintains discipline and solves complex problems. While your perfectionist nature and strict standards for yourself and others may lead to being misunderstood as cold, beneath that exterior lies a profoundly just and deeply warm heart.",
            "fr": "Vous incarnez l'essence du 'Métal', symbolisant les lames acérées et le roc solide. Vous possédez une détermination inébranlable et une volonté puissante, agissant comme une personne d'une grande intégrité qui honore ses engagements jusqu'au bout. Avec un souci de perfection et un esprit rationnel qui distingue clairement les affaires publiques et privées, vous excellez en tant que 'dépanneur' qui maintient la discipline. Bien que votre nature perfectionniste et vos normes strictes puissent être perçues comme de la froideur, sous cette apparence se cache un cœur profondément juste et chaleureux.",
            "es": "Encarnas la esencia del 'Metal', que simboliza las hojas afiladas y la roca sólida. Posees una determinación inquebrantable y una voluntad poderosa, actuando como una persona de gran integridad que honra sus compromisos hasta el final. Con un compromiso con la perfección y una mente racional que distingue claramente entre asuntos públicos y privados, destacas como un 'solucionador de problemas' que mantiene la disciplina. Aunque tu naturaleza perfeccionista y tus estrictos estándares puedan ser malinterpretados como frialdad, bajo ese exterior se esconde un corazón profundamente justo y cálido.",
            "ja": "あなたは鋭い刃や硬い岩を象徴する「金（Metal）」の気運を持って生まれました。乱れのない決断力と強い意志を持ち、一度結んだ縁や約束を最後まで守り抜く義理堅い人です。何事にも完璧を期し、公私を明確に区별する冷静な理性を基に、組織の規律を守り問題を解決する「解決師」の役割を果たします。自分や他人に厳しい完璧主義な面から冷たいと誤解されることもありますが、その内面には誰よりも正義感が強く、思慮深い温かな真心が秘められています。",
            "zh": "你命中带有‘金’的基因，象征着锋利的宝剑与坚固的磐石。你拥有果 敢的决断力和顽强的意志，是极重义气、言出必行的诚信之辈。凭借追求完美的严谨态度和公私分明的冷峻理性，你在团队中扮演着整肃纪律、攻坚克难的‘终结者’角色。虽然因对自己和他人的严苛要求有时会被误解为冷酷，但实际上你外冷内热，内心深处藏着一颗比任何人都更正直、更深沉的赤子之心。"
        },
        "Water": {
            "ko": "당신은 만물의 생명을 유지시키고 어디로든 흐르는 '물(Water)'의 기운을 타고났습니다. 흐르는 강물처럼 유연한 사고와 뛰어난 적응력을 지니고 있으며, 보이지 않는 곳까지 살피는 깊은 통찰력과 지혜를 겸비한 '전략가'입니다. 대인관계에서 상대를 편안하게 만드는 포용력이 뛰어나며, 지식에 대한 탐구심이 강해 학문이나 예술 분야에서 두각을 나타냅니다. 다만, 생각이 너무 많아 때로는 내면의 우울감이나 고민에 빠지기도 하지만, 어떤 그릇에 담겨도 그 모양에 맞춰 변화하는 당신의 유연함은 변화무쌍한 현대 사회에서 살아남는 가장 강력한 생존 전략입니다.",
            "en": "You embody the essence of 'Water,' the life-giving force that flows and adapts to any environment. Much like a river, you possess a flexible mindset and exceptional adaptability, acting as a 'strategist' with profound insight and wisdom that looks beneath the surface. You have a natural ability to make others feel at ease and a strong intellectual curiosity that often leads to excellence in academia or the arts. While your deep contemplation can sometimes lead to inner melancholy or overthinking, your ability to adapt to any situation—like water taking the shape of its container—is your greatest strength in a rapidly changing world.",
            "fr": "Vous incarnez l'essence de l' 'Eau', la force vitale qui coule et s'adapte à tout environnement. Tel un fleuve, vous possédez un esprit flexible et une adaptabilité exceptionnelle, agissant comme un 'stratège' doté d'une perspicacité profonde et d'une sagesse qui voit au-delà des apparences. Vous avez une capacité naturelle à mettre les autres à l'aise et une forte curiosité intellectuelle. Bien que votre profonde réflexion puisse parfois mener à la mélancolie, votre capacité à vous adapter à toute situation — comme l'eau prenant la forme de son contenant — est votre plus grande force dans un monde en mutation.",
            "es": "Encarnas la esencia del 'Agua', la fuerza vital que fluye y se adapta a cualquier entorno. Como un río, posees una mente flexible y una adaptabilidad excepcional, actuando como un 'estratega' con una visión profunda y una sabiduría que mira más allá de la superficie. Tienes una capacidad natural para hacer que los demás se sientan cómodos y una fuerte curiosidad intelectual. Aunque tu profunda reflexión a veces puede llevarte a la melancolía o a pensar demasiado, tu capacidad para adaptarte a cualquier situación —como el agua tomando la forma de su recipiente— es tu mayor fortaleza en un mundo en constante cambio.",
            "ja": "あなたは万物の生命を維持し、どこへでも流れる「水（Water）」の気運を持って生まれました。流れる川のように柔軟な思考と優れた適応力を持ち、見えないところまで見通す深い洞察力と知恵を兼ね備えた「戦略家」です。対人関係で相手をリラックスさせる包容力に優れ、知識に対する探求心が強いため、学問や芸術分野で頭角を現します。考えすぎて時に内面的な憂鬱や悩みに陥ることもありますが、どんな器に入れてもその形に合わせて変化するあなたの柔軟性は、変化の激しい現代社会を生き抜く最も強力な生存戦略です。",
            "zh": "你命中带有‘水’的基因，象征着滋養万物、无孔不入的生命源泉。正如奔流不息的江河，你拥有极强的适应能力和灵活的思维，是一位极具洞察力与智慧的‘策划大师’。你擅长营造轻松的人际氛围，求知欲极强，常在学术或艺术领域展现非凡才华。虽然深邃的思想有时会带来内心的忧郁或过度思虑，但那种如水般随方就圆、顺势而为的变通能力，正是你在瞬息万变的现代社会中立于不败之地的最强生存武器。"
        },
    }

    # 해당 오행(element)의 데이터를 가져옴 (없으면 기본값 Wood)
    e_data = data.get(element, data["Wood"])
    
    # 선택된 언어(lang)의 텍스트를 반환 (해당 언어가 없으면 영어 반환)
    return e_data.get(lang, e_data['en'])

# (2) 2026년 운세 데이터 (6개 국어)
def get_forecast_data(element):
    data = {
        "Wood": {
            "ko": {
                "title": "🔥 재능이 불타오르는 '표현과 결실'의 해", 
                "gen": "2026년은 당신의 내면에 잠자고 있던 천재적인 잠재력이 화산처럼 폭발하는 시기입니다. 창의적인 아이디어가 끊임없이 샘솟으며, 당신의 말과 행동이 대중의 마음을 움직이는 강력한 힘을 갖게 됩니다. 새로운 도전이나 프로젝트를 시작하기에 최적의 해이며, 스스로의 가치를 증명할 기회가 도처에 널려 있습니다.", 
                "money": "활동 범위가 넓어지는 만큼 통장의 잔고도 함께 불어나는 운세입니다. 당신의 아이디어가 곧바로 수익 창출이나 사업 확장으로 연결되며, 특히 예체능이나 기획 분야에서 예상치 못한 큰 성과급이나 보너스를 기대해 볼 수 있습니다.", 
                "love": "거부할 수 없는 매력이 넘쳐나 주변에 사람이 끊이지 않는 해입니다. 싱글이라면 당신의 당당한 모습에 반한 이성의 적극적인 대시를 받게 되며, 커플은 서로의 꿈을 응원하며 관계가 한층 더 깊고 뜨거워지는 경험을 할 것입니다."
            },
            "en": {
                "title": "🔥 Year of Radiant Expression & Tangible Success", 
                "gen": "2026 is a monumental year where your dormant potential erupts like a volcano. Creative ideas will flow endlessly, and your words and actions will hold a magnetic power to influence the public. It is the ultimate time to launch new ventures, as opportunities to prove your worth are everywhere.", 
                "money": "Your wealth grows in direct proportion to your increased activity. Your innovative ideas will directly translate into revenue or business expansion. Expect significant windfalls, especially in creative, planning, or artistic fields.", 
                "love": "Your irresistible charm will make you the center of attention. If single, expect passionate advances from those captivated by your confidence. For couples, supporting each other's ambitions will lead to a deeper and more passionate bond."
            },
            "fr": {
                "title": "🔥 Année d'Expression Éclatante et de Succès", 
                "gen": "2026 est une année monumentale où votre potentiel dormant éclate. Les idées créatives fusionnent et vos paroles captivent le public. C'est le moment idéal pour lancer de nouveaux projets.", 
                "money": "Vos revenus augmentent avec votre activité. Vos idées se transforment en profit. Attendez-vous à des gains importants dans les domaines créatifs.", 
                "love": "Votre charme irrésistible attire tous les regards. Les célibataires recevront des avances passionnées. Les couples verront leur lien se renforcer par un soutien mutuel."
            },
            "es": {
                "title": "🔥 Año de Expresión Radiante y Éxito Tangible", 
                "gen": "2026 es un año monumental donde tu potencial dormido estalla. Las ideas creativas fluyen sin cesar y tus palabras cautivan al público. Es el momento perfecto para nuevos emprendimientos.", 
                "money": "Tu riqueza crece con tu actividad. Tus ideas se traducen en ganancias. Espera beneficios significativos, especialmente en campos creativos.", 
                "love": "Tu encanto irresistible te convertirá en el centro de atención. Si estás soltero, espera avances apasionados. Las parejas fortalecerán su vínculo mediante el apoyo mutuo."
            },
            "ja": {
                "title": "🔥 才能が燃え上がる「表現と結実」の年", 
                "gen": "2026年は、内面に眠っていた天才的な潜在能力が火山のように爆発する時期です。創造的なアイデアが絶えず湧き出、あなたの言葉と行動が人々の心を動かす強力な力を持つようになります。", 
                "money": "活動範囲が広がる分、収入も比例して増える運勢です。あなたのアイデアが収益創出や事業拡大に直결し、特にクリエイティブな分野で予期せぬ大きな報酬が期待できます。", 
                "love": "抗いがたい魅力が溢れ、周囲に人が絶えない一年です。シングルの人はあなたの堂々とした姿に惹かれた異性から積極的なアプローチを受け、カップルは互いの夢を応援し合うことで絆がより深まります。"
            },
            "zh": {
                "title": "🔥 才华横溢之“表现与收获”年", 
                "gen": "2026年是你内在潜能如火山般爆发的一年。创意灵感源源不断，你的言行将展现出影响大众的强大魅力。这是开启新挑战或项目的最佳时机，证明自身价值的机会无处不在。", 
                "money": "财运随活动量的增加而水涨船高。你的创意将直接转化为收益或事业扩张。特别是在策划、艺术或创意领域，有望获得意想不到的丰厚奖金或回报。", 
                "love": "魅力四射的一年，异性缘极佳。单身者会因自信大方的表现而收获热烈的追求；有伴侣的人则会通过互相扶持梦想，使感情进入更加深厚且甜蜜的新阶段。"
            }
        },
        "Fire": {
            "ko": {
                "title": "🤝 경쟁을 뚫고 우뚝 서는 '자립과 도약'의 해", 
                "gen": "2026년은 당신의 자신감과 주체성이 절정에 달하는 시기입니다. 주변의 시선에 흔들리지 않고 오직 자신의 신념에 따라 행동하게 되며, 이는 강력한 독립심으로 이어져 창업이나 새로운 사업 기틀을 마련하는 데 최적의 환경을 제공합니다. 동료들과의 건전한 경쟁 속에서 당신의 진가가 더욱 빛나게 될 것입니다.", 
                "money": "재물 흐름이 매우 역동적인 해입니다. 사업 확장이나 공격적인 투자로 인해 큰 수익이 발생하기도 하지만, 그만큼 재투자와 활동비 지출도 늘어나는 형국입니다. 들어오는 돈을 지키기보다는 더 큰 가치를 위해 '투자'하는 관점으로 접근할 때 장기적으로 큰 자산을 형성하게 됩니다.", 
                "love": "서로의 독립성을 존중하는 성숙한 연애운이 따릅니다. 싱글이라면 가치관이 비슷한 동료나 친구 사이에서 자연스럽게 연인으로 발전할 가능성이 크며, 커플은 서로의 성장을 돕는 가장 든든한 파트너로서 함께 미래를 설계하는 건설적인 한 해를 보낼 것입니다."
            },
            "en": {
                "title": "🤝 Year of Bold Self-Reliance & Competitive Growth", 
                "gen": "2026 is a year where your self-confidence reaches its peak. You will act solely on your convictions, unswayed by others, providing the perfect environment to establish a startup or a new business foundation. Your true value will shine through healthy competition with peers.", 
                "money": "A year of dynamic financial flow. While aggressive investments or business expansions will lead to significant gains, reinvestment and operational expenses will also rise. Focus on strategic 'investment' for long-term growth rather than just saving cash.", 
                "love": "A year for mature relationships that respect individuality. If single, a friend or colleague with similar values may naturally become a lover. Couples will find themselves acting as supportive partners, building a future together based on mutual growth."
            },
            "fr": {
                "title": "🤝 Année d'Autonomie et de Croissance Compétitive", 
                "gen": "2026 est l'année où votre confiance atteint son paroxysme. Vous agirez selon vos convictions, créant l'environnement idéal pour lancer une startup. Votre valeur s'imposera face à la concurrence.", 
                "money": "Flux financiers dynamiques. Les gains seront importants mais les réinvestissements aussi. Privilégiez l'investissement stratégique pour bâtir un patrimoine durable.", 
                "love": "Relations matures basées sur le respect de l'indépendance. Les célibataires pourraient trouver l'amour parmi leurs amis. Les couples se soutiendront mutuellement pour bâtir leur avenir."
            },
            "es": {
                "title": "🤝 Año de Autosuficiencia y Crecimiento Competitivo", 
                "gen": "2026 es un año donde tu confianza alcanza su punto máximo. Actuarás según tus convicciones, creando el entorno perfecto para emprender. Tu valor brillará en la competencia sana.", 
                "money": "Flujo financiero dinámico. Grandes ganancias se verán compensadas por reinversiones. Enfócate en la inversión estratégica para el crecimiento a largo plazo.", 
                "love": "Relaciones maduras que respetan la independencia. Los solteros podrían encontrar el amor entre amigos o colegas. Las parejas construirán un futuro basado en el apoyo mutuo."
            },
            "ja": {
                "title": "🤝 競争を勝ち抜き自립する「自立と飛躍」の年", 
                "gen": "2026年は、あなたの自信と主体性が絶頂に達する時期です。周囲に惑わされず自身の信念に従って行動でき、起業や新規事業の基盤を築くのに最適な環境が整います。", 
                "money": "財運の流れが非常にダイナミックな一年です。積極的な投資で大きな収益を得る反면、活動費や再投資も増える傾向にあります。目先の貯蓄より、将来の価値のための「投資」に重点を置くことで大きな資産を築けます。", 
                "love": "互いの独立性を尊重し合える成熟した恋愛運です。シングルの人は価値観の似た友人や同僚から恋人に発展する可能性が高く、カップルは互いの成長を支え合う最高のパートナーとして未来を共に設計するでしょう。"
            },
            "zh": {
                "title": "🤝 竞争中脱颖而出的“自立与飞跃”年", 
                "gen": "2026年是你的自信心与自主意识达到顶峰的一年。你将不受外界干扰，坚定地执行个人信念，这为创业或开辟事业新版图提供了绝佳时机。在与同行的良性竞争中，你的真正实力将得到充分认可。", 
                "money": "财运呈现出大进大出的动态特征。事业扩张和果断投资将带来显著收益，但相应的再投资与活动开销也会增加。与其死守现金，不如以“战略性投资”的眼光布局，方能成就长远的大宗资产。", 
                "love": "今年盛行尊重彼此独立空间的成熟恋爱观。单身者极易在志趣相投的朋友或同事中找到真爱；有伴侣的人则会成为彼此成长道路上最坚实的后盾，共同规划极具建设性的未来蓝图。"
            }
        },
        "Earth": {
            "ko": {
                "title": "💎 내실을 다져 황금기를 여는 '결실'의 해", 
                "gen": "2026년은 그동안 묵묵히 뿌려온 노력의 씨앗들이 마침내 단단한 결실을 맺는 시기입니다. 당신의 성실함이 대내외적으로 인정받으며, 조직 내에서 대체 불가능한 위치에 서게 됩니다. 주거 환경의 변화나 문서상의 이득이 따르는 등 삶의 기반이 더욱 공고해지는 한 해입니다.", 
                "money": "안정적인 자산 증식이 기대되는 해입니다. 큰 모험보다는 적금, 부동산, 장기 투자 등 검증된 방식에서 큰 이득이 발생합니다. 생각지도 못한 상속이나 증여, 혹은 과거에 묶여있던 자금이 풀리는 기분 좋은 소식도 기대해 볼 수 있습니다.", 
                "love": "신뢰를 바탕으로 한 깊은 유대감이 형성됩니다. 싱글이라면 가볍기보다는 결혼을 전제로 한 진지한 만남이 성사될 운이며, 커플은 양가 어른들께 인사를 드리거나 동거, 결혼 등 구체적인 가정을 꾸리는 단계로 진입하기에 매우 길한 운세입니다."
            },
            "en": {
                "title": "💎 Year of Harvesting Fruit & Solidifying Foundations", 
                "gen": "2026 is the year when the seeds of effort you've silently sown finally bear solid fruit. Your sincerity will be recognized, placing you in an irreplaceable position. It's a year where your life's foundation becomes even firmer through gains in contracts or favorable housing changes.", 
                "money": "Expect stable asset growth. Significant gains will come from verified methods like real estate or long-term investments rather than risky ventures. Good news regarding inheritance or the release of previously tied-up funds may also arrive.", 
                "love": "Deep bonds based on trust will flourish. If single, a serious relationship with marriage in mind is likely. For couples, it's a highly auspicious year to take concrete steps toward building a home, such as meeting parents or getting married."
            },
            "fr": {
                "title": "💎 Année de Récolte et de Consolidation", 
                "gen": "2026 est l'année où les graines d'efforts semées patiemment portent enfin leurs fruits. Votre sincérité sera reconnue, vous plaçant à un poste irremplaçable. C'est une année où les fondations de votre vie se renforcent grâce à des gains contractuels ou des changements de logement favorables.", 
                "money": "Une croissance stable des actifs est attendue. Des gains importants proviendront de méthodes vérifiées comme l'immobilier ou les investissements à long terme. Des nouvelles concernant un héritage ou le déblocage de fonds sont possibles.", 
                "love": "Des liens profonds basés sur la confiance s'épanouiront. Les célibataires pourraient envisager une relation sérieuse menant au mariage. Pour les couples, c'est une année propice pour bâtir un foyer ou rencontrer la belle-famille."
            },
            "es": {
                "title": "💎 Año de Cosecha y Consolidación de Bases", 
                "gen": "2026 es el año en que las semillas de esfuerzo que has sembrado en silencio finalmente dan sus frutos. Tu sinceridad será reconocida, colocándote en una posición irremplazable. Es un año donde las bases de tu vida se vuelven más firmes mediante ganancias en contratos o cambios de vivienda favorables.", 
                "money": "Se espera un crecimiento estable de activos. Las ganancias provendrán de métodos verificados como bienes raíces o inversiones a largo plazo. También pueden llegar noticias sobre herencias o la liberación de fondos retenidos.", 
                "love": "Florecerán vínculos profundos basados en la confianza. Si estás soltero, es probable una relación seria con miras al matrimonio. Para las parejas, es un año muy propicio para dar pasos concretos como conocer a los padres o casarse."
            },
            "ja": {
                "title": "💎 内実を固め黄金期を開く「結実」の年", 
                "gen": "2026年は、これまで黙々と蒔いてきた努力の種がついに強固な結実を結ぶ時期です. あなたの誠実さが認められ、組織内でかけがえのない地位を築くことになります. 住環境の変化や文書上の利益が伴うなど、生活の基盤がより強固になる一年です.", 
                "money": "安定的な資産形成が期待できる年です. 大きな冒険よりは、不動産や長期投資など検証された方法から大きな利益が発生します. 思いがけない相続や、過去に滞っていた資金が動くといった嬉しいニュースも期待できます.", 
                "love": "信頼に基づいた深い絆が形成されます. シングルの人は結婚を前提とした真剣な出会いがある運勢で、カップルは両親への挨拶や結婚など、具体的な家庭を築く段階に進むのに非常に良い時期です."
            },
            "zh": {
                "title": "💎 夯实基础、迎来黄金时刻的“收获”年", 
                "gen": "2026年是你过去默默付出的汗水终获丰硕果实的一年. 你的诚实可靠将获得内外一致认可，在组织中处于无可替代的地位. 通过合同获利或住房环境的改善，你的人生地基将变得更加稳固.", 
                "money": "财运稳步增长. 比起投机冒险，从房地产或长期投资等稳健渠道中获利更多. 可能会有关于遗产继承或之前被套牢资金回笼的好消息.", 
                "love": "基于信任的深层情感纽带正在形成. 单身者有望遇到以结婚为前提的认真对象；有伴侣的人则非常适合步入谈婚论嫁、组建家庭的实质性阶段."
            }
        },
        "Metal": {
            "ko": {
                "title": "🏢 권위와 명예가 드높아지는 '명예'의 해", 
                "gen": "2026년은 당신의 카리스마와 리더십이 만개하는 해입니다. 직장 내 승진이나 사회적 지위가 상승하는 운세가 매우 강하며, 국가 기관이나 대기업을 상대로 한 계약에서 유리한 고지를 점하게 됩니다. 당신의 원칙주의가 마침내 빛을 발하며 많은 이들의 귀감이 되는 해가 될 것입니다.", 
                "money": "명예가 오르면 재물은 자연스럽게 따라오는 법입니다. 고정적인 수입의 수준이 한 단계 업그레이드되며, 관급 공사나 공공 프로젝트 등을 통해 큰 규모의 자금을 만질 기회가 생깁니다. 다만, 체면 유지비나 품위 유지에 따른 지출이 늘어날 수 있으니 주의가 필요합니다.", 
                "love": "존경할 수 있는 상대를 만나거나, 본인이 상대에게 존경받는 관계가 형성됩니다. 싱글이라면 전문직 종사자나 사회적 지위가 높은 이성과 인연이 닿을 가능성이 높습니다. 커플은 서로의 사회적 성공을 축하하며 품격 있는 데이트와 여행을 즐기는 화려한 한 해가 될 것입니다."
            },
            "en": {
                "title": "🏢 Year of Rising Authority & Social Honor", 
                "gen": "2026 is the year your charisma and leadership fully bloom. There's a strong trend toward promotion or a rise in social status. Your principled nature will shine, making you a role model for many. It's an excellent time for contracts involving large institutions.", 
                "money": "As your honor rises, wealth naturally follows. Your base income will level up, and opportunities to handle large-scale funds through public projects may arise. However, be cautious of increased spending on maintaining your professional image.", 
                "love": "A relationship built on mutual respect will form. If single, you're likely to connect with someone of high social status or professional standing. Couples will enjoy a sophisticated year, celebrating each other's career successes."
            },
            "fr": {
                "title": "🏢 Année d'Autorité Croissante et d'Honneur", 
                "gen": "2026 est l'année où votre charisme et votre leadership s'épanouissent pleinement. Il existe une forte tendance à la promotion ou à une ascension sociale. Votre nature intègre fera de vous un modèle pour beaucoup.", 
                "money": "Avec l'honneur, la richesse suit naturellement. Vos revenus de base augmenteront et des opportunités de gérer des fonds importants via des projets publics pourraient se présenter. Attention toutefois aux dépenses de prestige.", 
                "love": "Une relation basée sur le respect mutuel s'installera. Les célibataires pourraient rencontrer une personne de statut social élevé. Les couples célébreront leurs succès professionnels respectifs par des voyages élégants."
            },
            "es": {
                "title": "🏢 Año de Autoridad Ascendente y Honor Social", 
                "gen": "2026 es el año en que tu carisma y liderazgo florecen por completo. Hay una fuerte tendencia hacia el ascenso o una mejora en tu estatus social. Tu naturaleza íntegra brillará, convirtiéndote en un modelo a seguir.", 
                "money": "A medida que sube tu honor, la riqueza te sigue naturalmente. Tus ingresos base subirán de nivel y surgirán oportunidades para manejar fondos a gran escala. Ten cuidado con los gastos excesivos en imagen profesional.", 
                "love": "Se formará una relación basada en el respeto mutuo. Si estás soltero, es probable que conectes con alguien de alto estatus. Las parejas disfrutarán de un año sofisticado, celebrando los éxitos laborales mutuos."
            },
            "ja": {
                "title": "🏢 権威と名誉が高まる「名誉」の年", 
                "gen": "2026年は、あなたのカリスマ性とリーダーシップが満開になる年です. 職場での昇進や社会的地位の上昇運が非常に強く、あなたの原則主義がついに光を放ち、多くの人々の模範となる一年になるでしょう.", 
                "money": "名誉が上がれば、財は自然とついてくるものです. 固定収入の水準が一段階上がり、公共プロジェクトなどを通じて大規模な資金を扱う機会に恵まれます. ただし、管理が必要です.", 
                "love": "尊敬できる相手に出会うか、自分が相手から尊敬される関係が築かれます. シングルの人は専門職や社会的地位の高い異性と縁がある可能性が高いです. カップルは品格のあるデートを楽しむ華やかな一年になるでしょう."
            },
            "zh": {
                "title": "🏢 威望与名誉双丰收的“显赫”年", 
                "gen": "2026年是你的魅力与领导力全面绽放的一年. 职场晋升或社会地位提升的运势极强，你的坚持原则终将获得认可，成为众人的楷模. 在合同谈判中，你将占据绝对优势.", 
                "money": "名利双收，财随名来. 你的固定收入将迈上新台阶. 但需注意，因维护个人形象或社交品位而产生的额外开销也会随之增加.", 
                "love": "一段建立在互相钦佩基础上的关系正在萌芽. 单身者易与专业人士结缘；有伴侣者则会共同庆祝事业上的成功，享受充满质感的高端情感生活."
            }
        },
        "Water": {
            "ko": {
                "title": "🧘 지혜가 깊어지고 귀인을 만나는 '조력'의 해", 
                "gen": "2026년은 당신의 깊은 통찰력이 빛을 발하고, 생각지도 못한 귀인의 도움을 받아 어려움을 해결하는 해입니다. 무리하게 앞으로 나가기보다는 공부, 연구, 혹은 내면의 평화를 찾는 활동에서 큰 성취감을 느낄 수 있습니다. 당신을 지지해 주는 강력한 후원자가 나타나 정신적, 물질적 안정을 돕는 시기입니다.", 
                "money": "직접적인 근로 소득 외에 자산 가치 상승이나 후원금 등 '가만히 있어도 들어오는' 간접적 이득이 강한 해입니다. 문서 운이 좋아 자격증 취득이나 학위 이수를 통한 장기적인 몸값 상승을 꾀하기에 최적입니다. 재물에 대해 지나치게 욕심내지 않아도 필요할 때 적절히 채워지는 운세입니다.", 
                "love": "정신적인 소통이 잘 통하는 소울메이트를 만나게 됩니다. 싱글이라면 대화가 잘 통하고 배울 점이 많은 이성에게 끌리게 되며, 커플은 함께 명상, 여행, 혹은 새로운 취미를 배우며 정서적인 유대감을 극대화하는 평온하고 행복한 한 해를 보낼 것입니다."
            },
            "en": {
                "title": "🧘 Year of Deep Wisdom & Meeting Mentors", 
                "gen": "2026 is a year where your insight shines and unexpected mentors help resolve long-standing issues. Focus on study, research, or inner peace rather than rushing forward. Powerful supporters will emerge to help you achieve both spiritual and material stability.", 
                "money": "Strong potential for passive income or asset appreciation rather than just labor income. It’s an ideal time for long-term value growth through certifications or degrees. Wealth will flow in naturally when needed, so avoid excessive greed.", 
                "love": "You will meet a soulmate with whom you share a deep spiritual connection. If single, you'll be drawn to someone intellectual and inspiring. Couples will maximize their emotional bond through shared hobbies or travel, enjoying a peaceful year."
            },
            "fr": {
                "title": "🧘 Année de Sagesse Profonde et de Mentors", 
                "gen": "2026 est une année où votre perspicacité brille et où des mentors inattendus aident à résoudre des problèmes anciens. Privilégiez l'étude ou la paix intérieure. Des soutiens puissants apparaîtront pour stabiliser vos finances et votre moral.", 
                "money": "Fort potentiel de revenus passifs ou de plus-value d'actifs. C'est le moment idéal pour valoriser votre profil par des diplômes. La richesse viendra naturellement selon vos besoins, évitez l'avidité excessive.", 
                "love": "Vous rencontrerez une âme sœur avec qui vous partagerez une connexion spirituelle. Les célibataires seront attirés par des intellectuels. Les couples renforceront leur lien par des loisirs partagés ou des voyages apaisants."
            },
            "es": {
                "title": "🧘 Año de Sabiduría Profunda y Encuentro con Mentores", 
                "gen": "2026 es un año donde tu visión brilla y mentores inesperados ayudan a resolver problemas de larga data. Enfócate en el estudio o la paz interior. Surgirán protectores poderosos que te ayudarán a lograr estabilidad espiritual y material.", 
                "money": "Gran potencial para ingresos pasivos o revalorización de activos. Es un momento ideal para el crecimiento de valor a largo plazo mediante certificaciones. La riqueza fluirá naturalmente, así que evita la codicia excesiva.", 
                "love": "Conocerás a un alma gemela con quien compartirás una profunda conexión espiritual. Los solteros se sentirán atraídos por alguien intelectual. Las parejas maximizarán su vínculo emocional mediante viajes o pasatiempos compartidos."
            },
            "ja": {
                "title": "🧘 知恵が深まり貴人に出会う「助力」の年", 
                "gen": "2026年は、あなたの深い洞察力が光を放ち、思いがけない貴人の助けを借りて困難を解決する年です. 勉強や研究、内面の平和を探る活動で大きな成就感を得られます. あなたを支持する強力な後援者が現れる時期です.", 
                "money": "資産価値の上昇や支援金など、間接적인利益に恵まれる年です. 文書運が良く、資格取得や学位取得を通じて長期的な価値を高めるのに最適です. 財物に対して欲張らなくても、適切に満たされる運勢です.", 
                "love": "精神的なコミュニケーションが深まるソウルメイトに出会います. シングルの人は尊敬できる異性に惹かれるでしょう. カップルは情緒的な絆を深める穏やかで幸せな一年を過ごします."
            },
            "zh": {
                "title": "🧘 智慧深造、贵人相助的“印绶”年", 
                "gen": "2026年是你洞察力大爆发的一年，困扰已久的难题将在意想不到的贵人指点下迎刃而解. 通过学习或寻求内心平静，你将获得更大的成就感. 强大的支持者将为你提供精神与物质的双重保障.", 
                "money": "偏财运旺盛，资产增值或获得赞助等收益显著. 今年非常利于考取证书，以此实现长期身价的飞跃. 财运自然随缘，无需过度强求即可满足生活所需.", 
                "love": "有望遇到心灵契合的灵魂伴侣. 单身者会被学识渊博的对象吸引；有伴侣的人则会通过共同学习，提升情感层次，度过静谧而幸福的一年."
            }
        },
    }
    e_data = data.get(element, data["Wood"]) 
    return e_data.get(lang, e_data["en"])

def get_monthly_forecast_unique(element, lang):
    # 5개 오행 x 12개월 x 6개 국어 데이터 베이스
    raw_data = {
        "Wood": [
            {
                "mon": "1월", "star": "⭐⭐",
                "ko": "새해 벽두부터 지인이나 가까운 친구가 곤란한 표정으로 금전적인 부탁을 해올 수 있습니다. 정에 이끌려 확답을 주거나 보증을 서는 행위는 절대 금물입니다. 냉정하게 거절하지 않으면 소중한 재산은 물론, 오랜 시간 쌓아온 인간관계까지 한꺼번에 잃을 수 있으니 공과 사를 명확히 구분하세요.",
                "en": "At the start of the year, an acquaintance or close friend may approach you with a difficult financial request. Avoid giving a definite answer or acting as a guarantor based on emotion. If you don't refuse firmly, you risk losing both your precious assets and long-standing relationships. Keep business and personal life strictly separate.",
                "fr": "En ce début d'année, une connaissance ou un ami proche pourrait vous solliciter pour une aide financière. Évitez de donner une réponse définitive ou de vous porter garant par émotion. Un refus ferme est nécessaire pour protéger votre patrimoine et vos relations de longue date.",
                "es": "A principios de año, un conocido o amigo cercano podría acercarse a ti con una petición financiera difícil. Evita dar una respuesta definitiva o actuar como avalista por emoción. Un rechazo firme es necesario para proteger tanto tus activos como tus amistades.",
                "ja": "年明け早々、知人や親한友人が困った様子で金銭的な頼み事をしてくるかもしれません。情に流されて安請け合いしたり、保証人になったりするのは絶対に禁物です。冷静に断らなければ、大切な財産はもちろん、長年築いてきた人間関係まで失う恐레가 있으니公私を明確に区別しましょう。",
                "zh": "新年伊始，熟人或好友可能会面露难色地向你提出金钱方面的请求。切记不可因感情用事而给出肯定的答复或作担保。若不果断拒绝，恐将面临人财两失的境地，请务必公私分明。"
            },
            {
                "mon": "2월", "star": "⭐⭐⭐",
                "ko": "사회생활에서 강력한 라이벌이 등장하여 당신의 성과를 가로채려 하거나 영역을 침범할 수 있습니다. 상대의 도발에 감정적으로 대응하기보다는, 당신만의 전문성과 실력으로 승부하는 것이 현명합니다. 겉으로 드러나는 기 싸움보다는 실질적인 이득과 내실을 챙기는 데 집중하며 조용히 실력을 갈고닦으세요.",
                "en": "A powerful rival appears in your professional life, attempting to take credit for your achievements or encroach on your territory. Rather than reacting emotionally to provocations, prove your worth through your expertise. Focus on securing practical benefits and inner strength rather than outward confrontations.",
                "fr": "Un rival puissant apparaît dans votre vie professionnelle. Ne réagissez pas émotionnellement aux provocations. Prouvez votre valeur par votre expertise. Concentrez-vous sur les bénéfices pratiques plutôt que sur les confrontations inutiles.",
                "es": "Aparece un rival poderoso en tu vida profesional. No reacciones emocionalmente a las provocaciones. Demuestra tu valía a través de tu experiencia. Concéntrate en asegurar beneficios prácticos en lugar de confrontaciones externas.",
                "ja": "社会生活において強力なライバルが登場し、あなたの成果を横取りしようとしたり、領域を侵犯したりする可能性があります。相手の挑発に感情的に反応するより、あなただけの専門性と実力で勝負するのが賢明です。見栄を張るよりも、実利を取ることに集中しましょう。",
                "zh": "职场上会出现强劲的对手，企图窃取你的成果或侵犯你的利益范围。面对挑衅，与其感情用事，不如凭借专业实力说话。比起表面的争执，专注于获取实利和巩固自身基础更为重要。"
            },
            {
                "mon": "3월", "star": "⭐⭐",
                "ko": "사람들이 많이 모이는 회식이나 미팅 자리에서 무심코 던진 한마디가 화근이 될 수 있습니다. 특히 타인의 험담이나 확인되지 않은 소문을 옮기는 것은 매우 위험합니다. '낮말은 새가 듣고 밤말은 쥐가 듣는다'는 격언을 가슴에 새기고, 가급적 남의 일에 참견하기보다 자신의 업무에만 몰입하는 것이 평안을 유지하는 길입니다.",
                "en": "Inadvertent remarks at social gatherings or business meetings could lead to major trouble. Avoid gossiping or spreading unverified rumors. Remember that 'walls have ears.' The best way to maintain peace is to immerse yourself in your own work rather than interfering in others' business.",
                "fr": "Des remarques imprudentes lors de réunions sociales pourraient causer des ennuis. Évitez les commérages. Gardez à l'esprit que 'les murs ont des oreilles'. Concentrez-vous sur votre propre travail pour préserver votre tranquillité.",
                "es": "Comentarios descuidados en reuniones sociales podrían causar problemas. Evita los chismes. Recuerda que 'las paredes oyen'. Concéntrate en tu propio trabajo para mantener la paz.",
                "ja": "人が集まる飲み会や会議の席で、何気なく発した一言が災いの元になるかもしれません。特に他人の悪口や不確かな噂を広めるのは非常に危険です。他人の事に首を突っ込むより、自分の業務に没頭することが平穏を保つ道です。",
                "zh": "在聚会或会议等场合，无心的一句话可能会引发事端。特别是传播他人是非或未经证实的传闻非常危险。切记“隔墙有耳”，与其干涉他人事务，不如潜心于自己的工作，方能保平安。"
            },
            {
                "mon": "4월", "star": "⭐⭐⭐⭐⭐",
                "ko": "운수대통의 기운이 가득한 달입니다. 복권 당첨과 같은 깜짝 행운은 물론, 과거에 잊고 있었던 투자금이나 빌려준 돈이 이자가 붙어 돌아오는 등 뜻밖의 횡재수가 있습니다. 생각지도 못한 성과급이나 보너스 덕분에 가계에 큰 보탬이 되는 시기이니, 이 기운을 몰아 새로운 수익 파이프라인을 구상해 보는 것도 좋습니다.",
                "en": "A month filled with immense good fortune. Beyond small wins like lotteries, expect unexpected windfalls such as the return of forgotten investments or debts with interest. This unexpected income will significantly boost your finances. It's a great time to brainstorm new revenue streams.",
                "fr": "Un mois rempli d'une immense fortune. Attendez-vous à des rentrées d'argent inattendues, comme le retour d'investissements oubliés. Ces revenus boosteront vos finances. C'est le moment idéal pour envisager de nouvelles sources de revenus.",
                "es": "Un mes lleno de inmensa fortuna. Espera ganancias inesperadas, como el retorno de inversiones olvidadas. Estos ingresos impulsarán tus finanzas. Es un gran momento para idear nuevas fuentes de ingresos.",
                "ja": "運気が大好転する月です。宝くじのようなラッキーはもちろん、過去に忘れていた投資金や貸したお金が戻ってくるなど、思いがけない横財数があります。予想外のボーナスのおかげで家計が潤う時期なので、この運気に乗って新しい収益源を考えてみるのも良いでしょう。",
                "zh": "本月好运连连。除了抽奖中奖之类的惊喜，还可能有遗忘已久的投资回笼或欠款归还等意外之财。意想不到的奖金将极大地改善财务状况，建议趁此好运筹划新的致富之路。"
            },
            {
                "mon": "5월", "star": "⭐⭐⭐⭐⭐",
                "ko": "지적 능력이 최고조에 달하며 반짝이는 아이디어가 봇물 터지듯 쏟아집니다. 기획안 작성, 창작 활동, 혹은 새로운 사업 전략을 짜기에 이보다 더 좋은 시기는 없습니다. 당신이 내놓은 독창적인 결과물이 주변의 찬사를 받으며 최고의 성과를 거두게 될 것입니다. 망설이지 말고 당신의 천재성을 세상에 드러내세요.",
                "en": "Your intellectual capacity reaches its peak, and brilliant ideas will flow endlessly. There is no better time for writing proposals, creative work, or devloping new business strategies. Your original outputs will receive widespread acclaim. Don't hesitate to show your genius to the world.",
                "fr": "Votre capacité intellectuelle est à son comble. C'est le meilleur moment pour des propositions, de la création ou des stratégies commerciales. Vos résultats originaux seront acclamés. N'hésitez pas à montrer votre génie.",
                "es": "Tu capacidad intelectual alcanza su punto máximo. No hay mejor momento para propuestas, trabajo creativo o estrategias comerciales. Tus resultados originales serán aclamados. No dudes en mostrar tu genio al mundo.",
                "ja": "知的能力が最高潮に達し、輝くアイデアが溢れ出します。企画書の作成、創作活動、あるいは新しい事業戦略を立てるのにこれ以上の時期はありません。あなたの独創的な成果が周囲から絶賛され、最高の成果を収めることになるでしょう。迷わずその才能を世に示してください。",
                "zh": "头脑极度灵活，灵感如泉涌。现在是撰写企划、进行创作或制定商业战略的最佳时机。你独具匠心的成果将赢得广泛赞誉并取得卓越成效。不要犹豫，向世界展示你的才华吧。"
            },
            {
                "mon": "6월", "star": "⭐⭐",
                "ko": "의욕이 앞서 여러 가지 일을 동시에 벌이다 보니 몸이 열 개라도 부족할 만큼 바쁜 일정을 보내게 됩니다. 성취욕도 좋지만 과도한 업무량으로 인해 면역력이 떨어지고 번아웃이 올 수 있습니다. 비타민이나 영양제를 챙겨 먹으며 체력을 보충하고, 일의 우선순위를 정해 에너지를 효율적으로 분배하는 지혜가 필요합니다.",
                "en": "Driven by ambition, you might take on too much at once, leading to an incredibly hectic schedule. While achievement is good, excessive workload may weaken your immunity or lead to burnout. Take supplements to boost your stamina and prioritize tasks to distribute your energy effectively.",
                "fr": "Porté par l'ambition, vous pourriez en faire trop, menant à un emploi du temps épuisant. Un surmenage pourrait affaiblir votre immunité. Prenez des vitamines et priorisez vos tâches pour gérer votre énergie.",
                "es": "Impulsado por la ambición, podrías abarcar demasiado, lo que resultaría en una agenda agotadora. El exceso de trabajo podría debilitar tu inmunidad. Toma suplementos y prioriza tus tareas para gestionar tu energía.",
                "ja": "意欲が空回りして多くの仕事を同時に抱え込み、体がいくつあっても足りないほど忙しい日々を過ごすことになります。過度な業務量によって免疫力が落ち、燃え尽き症候群になる恐れがあります。栄養を摂って体力をつけ、仕事の優先順位を決める知恵が必要です。",
                "zh": "因事业心过强，同时揽下多项任务，导致忙得不可开交。虽有成就欲是好事，但繁重的工作量可能会导致免疫力下降或产生倦怠感。请注意补充营养，学会分清轻重缓急，合理分配精力。"
            },
            {
                "mon": "7월", "star": "⭐⭐⭐⭐",
                "ko": "재물 흐름이 비단결처럼 매끄럽고 안정적인 달입니다. 수입과 지출이 균형을 이루며, 여유 자금이 생겨 저축하기에 아주 좋은 타이밍입니다. 충동적인 소비 욕구만 잘 억제한다면 통장의 숫자가 늘어나는 즐거움을 만끽할 수 있습니다. 장기적인 재테크 계획을 세우거나 안전 자산에 투자해 보는 것을 추천합니다.",
                "en": "Financial flow is as smooth and stable as silk this month. Income and expenses are well-balanced, making it a perfect time to save surplus funds. If you control impulsive spending, you'll enjoy watching your bank balance grow. Consider making long-term financial plans or investing in safe assets.",
                "fr": "Le flux financier est fluide et stable ce mois-ci. Les revenus et les dépenses sont équilibrés, idéal pour épargner. Si vous contrôlez vos impulsions d'achat, vous verrez votre solde augmenter. Envisagez des investissements sûrs.",
                "es": "El flujo financiero es fluido y estable este mes. Los ingresos y gastos están equilibrados, ideal para ahorrar. Si controlas tus impulsos de compra, verás crecer tu saldo. Considera inversiones seguras.",
                "ja": "財運の流れが非常にスムーズで安定した月です。収入と支出のバランスが取れ、余剰資金ができて貯蓄するのに絶好のタイミングです。衝動買いを抑えれば、通帳の数字が増えていく喜びを満喫できるでしょう。長期的な資産運用の計画を立てるのもお勧めです。",
                "zh": "本月财运如丝般顺滑稳定。收支平衡，是储备余钱的绝佳时机。只要克制住冲动消费，就能体会到存款增加的喜悦。建议制定长期的理财计划或投资稳健型资产。"
            },
            {
                "mon": "8월", "star": "⭐⭐",
                "ko": "조직 내 갈등이나 과중한 업무로 인해 스트레스가 정점에 달하는 시기입니다. 순간적인 감정을 이기지 못해 사표를 던지거나 극단적인 선택을 하고 싶은 유혹이 들 수 있지만, 지금은 인내해야 하는 때입니다. 비바람이 지나가면 땅이 굳어지듯, 이 고비를 잘 넘기면 연말에 예상치 못한 큰 보상이 기다리고 있을 것입니다.",
                "en": "Stress reaches its peak due to internal conflicts or heavy workloads. You may be tempted to quit impulsively, but now is the time for patience. Just as rain firms the ground, enduring this crisis will lead to unexpected rewards toward the end of the year.",
                "fr": "Le stress culmine en raison de conflits internes ou d'une charge de travail lourde. Vous pourriez être tenté de démissionner sur un coup de tête, mais c'est le moment d'être patient. Cette crise passée, de grandes récompenses vous attendront.",
                "es": "El estrés alcanza su punto máximo debido a conflictos internos o carga de trabajo. Podrías sentir la tentación de renunciar impulsivamente, pero es momento de tener paciencia. Superada esta crisis, te esperan grandes recompensas.",
                "ja": "組織内の葛藤や過重な業務により、ストレスが頂点に達する時期です。感情に任せて辞表を出したくなる誘惑に駆られるかもしれませんが、今は忍耐の時です。この峠を越えれば、年末に予想外の大きな報酬が待っているはずです。",
                "zh": "受职场纠纷或任务繁重的影响，压力达到顶峰。可能会有冲动辞职或采取消极态度的诱惑，但此时务必忍耐。风雨过后见彩虹，只要挺过这段时期，年末将有意想不到的厚报在等着你。"
            },
            {
                "mon": "9월", "star": "⭐⭐⭐⭐",
                "ko": "당신의 헌신과 성과가 마침내 윗사람들의 눈에 띄기 시작합니다. 책임이 막중해져 어깨는 무거워지겠지만, 그만큼 조직 내에서의 입지와 명예가 올라가는 보람찬 달입니다. 승진 제안을 받거나 중요한 프로젝트의 리더 자리를 맡게 될 수 있으니, 당당하게 당신의 역량을 발휘하여 리더십을 증명하세요.",
                "en": "Your dedication and achievements finally catch the eye of your superiors. Although your responsibilities will grow, your standing and reputation within the organization will rise. You may receive a promotion offer or be appointed leader of an important project. Demonstrate your capabilities with confidence.",
                "fr": "Votre dévouement et vos succès attirent enfin l'attention de vos supérieurs. Bien que vos responsabilités augmentent, votre statut s'améliore. Vous pourriez recevoir une promotion ou diriger un projet important. Montrez vos capacités.",
                "es": "Tu dedicación y logros finalmente atraen la atención de tus superiores. Aunque tus responsabilidades crezcan, tu estatus mejorará. Podrías recibir un ascenso o dirigir un proyecto importante. Demuestra tus capacidades con confianza.",
                "ja": "あなたの献身と成果がついに目上の人々の目に留まり始めます。責任が重くなり肩の荷は増えますが、その分組織内での地位と名誉が上がるやりがいのある月です。昇進の提案を受けたり、重要なプロジェクトのリーダーを任されたりする可能性があるので、堂々とリーダーシップを発揮してください。",
                "zh": "你的奉献与成果终于得到了上司的青睐。虽然责任加重会感到压力，但这也是你在组织中地位与名誉提升的收获之月。有望获得晋升或被委以重任，请自信地展示你的领导才能。"
            },
            {
                "mon": "10월", "star": "⭐⭐⭐⭐⭐",
                "ko": "부동산 매매, 임대차 계약, 혹은 중요한 비즈니스 파트너십 체결 등 문서와 관련된 모든 일에서 최고의 행운이 따릅니다. 중요한 도장을 찍어야 할 일이 있다면 이번 달로 일정을 잡으세요. 나중에 큰 자산 가치가 될 귀중한 문서를 손에 쥐게 될 운세이니 꼼꼼하게 검토하되 과감하게 결정하십시오.",
                "en": "Immense luck follows all matters related to documents, such as real estate deals, lease agreements, or major business partnerships. If you need to sign a contract, schedule it for this month. You are destined to hold a valuable document that will appreciate in the future. Review carefully but decide boldly.",
                "fr": "Une immense chance accompagne tout ce qui touche aux documents (immobilier, contrats d'affaires). Si vous devez signer un contrat, faites-le ce mois-ci. Vous obtiendrez un document précieux pour votre avenir financier.",
                "es": "Una inmensa suerte acompaña todo lo relacionado con documentos (bienes raíces, contratos). Si debes firmar un contrato, hazlo este mes. Obtendrás un documento valioso para tu futuro financiero. Revisa con cuidado pero decide con audacia.",
                "ja": "不動産の売買、賃貸借契約、あるいは重要なビジネスパートナーシップの締結など、文書に関連するすべての事柄で最高の幸運が伴います。重要な判子を押す予定があるなら、今月に設定しましょう。将来的に大きな資産価値となる貴重な文書を手にすることになる運勢です。",
                "zh": "本月在房地产交易、合同签署或重要商业合作等文书事务方面运势极佳。若有签约或盖章的需求，请安排在本月。你将获得未来具有巨大升值空间的珍贵文件，请在细致审查后果断抉择。"
            },
            {
                "mon": "11월", "star": "⭐⭐⭐⭐",
                "ko": "혼자 힘으로는 도저히 풀리지 않던 난제가 예상치 못한 조력자나 윗사람의 조언 한마디로 시원하게 해결됩니다. 주변에 도움을 요청하는 것을 부끄러워하지 마세요. 당신을 아끼는 귀인이 나타나 길을 인도해 주는 형국이니, 겸손한 자세로 조언을 구한다면 큰 성취를 맛보게 될 것입니다.",
                "en": "A problem that seemed impossible to solve on your own will be cleared up with a single piece of advice from a mentor or unexpected supporter. Don't be afraid to ask for help. A noble person who cares for you will emerge to guide the way. Great success awaits if you seek wisdom with humility.",
                "fr": "Un problème insoluble sera résolu grâce au conseil d'un mentor ou d'un soutien inattendu. N'ayez pas peur de demander de l'aide. Une personne bienveillante vous guidera. Le succès vous attend si vous restez humble.",
                "es": "Un problema insoluble se resolverá gracias al consejo de un mentor o un apoyo inesperado. No temas pedir ayuda. Una persona benévola te guiará. El éxito te espera si te mantienes humilde.",
                "ja": "一人の力ではどうしても解けなかった難題が、予想外の協力者や目上の人の助言一つでスッキリ解決します。周囲に助けを求めることを恥ずかしがらないでください。あなたを大切に思う貴人が現れて導いてくれる時期なので、謙虚な姿勢でアドバイスを求めれば大きな成果を得られます。",
                "zh": "单凭个人力量难以解决的难题，将在意想不到的贵人或长辈的点拨下迎刃而解。不要羞于向他人求助。此时会有赏识你的贵人指引方向，只要保持谦虚的态度虚心求教，定能取得巨大成就。"
            },
            {
                "mon": "12월", "star": "⭐⭐⭐⭐",
                "ko": "새로운 분야의 공부를 시작하거나 자격증 취득에 도전하기에 가장 완벽한 연말입니다. 학업적 성취도가 높아 시험운이 따르며, 지금 배우는 기술이나 지식이 내년 당신의 몸값을 결정짓는 핵심 자산이 될 것입니다. 한 해를 차분하게 마무리하며 지적 성장에 투자하는 시간을 가지세요.",
                "en": "The perfect end to the year for starting new studies or challenging yourself to earn a certification. Academic achievement is high, and the skills or knowledge you gain now will be key assets for your success next year. Invest time in intellectual growth as you close out the year calmly.",
                "fr": "Une fin d'année parfaite pour commencer de nouvelles études ou passer une certification. Votre réussite académique est favorisée. Les connaissances acquises seront des atouts clés pour l'année prochaine. Investissez dans votre croissance intellectuelle.",
                "es": "Un fin de año perfecto para comenzar nuevos estudios o certificaciones. Tu éxito académico está favorecido. Los conocimientos adquiridos serán activos clave para el próximo año. Invierte en tu crecimiento intelectual.",
                "ja": "新しい分野の勉強を始めたり、資格取得に挑戦したりするのに完璧な年末です。学業の成就度が高く試験運も良いため、今学ぶ技術や知識が来年のあなたの価値を決める核心的な資産になります。知的な成長に投資する時間を持ち、一年を穏やかに締めくくりましょう。",
                "zh": "这是开启新领域学习或挑战考证的完美岁末。学业运势强劲，此时掌握的技能或知识将成为明年提升个人身价的核心资产。建议在平静总结全年的同时，将时间投入到自我成长的智力投资中。"
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
        "btn_buy_sp": "💳 단품 구매 ($3 / 3회)",
        "btn_buy_all": "🎟️ 프리패스 구매 ($10 / 10회)",
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
        "btn_buy_sp": "💳 Buy Single ($3 / 3 Uses)",
        "btn_buy_all": "🎟️ Buy All-Access ($10 / 10 Uses)",
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
        "btn_buy_sp": "💳 Achat Unique (3$ / 3 essais)",
        "btn_buy_all": "🎟️ Pass Tout Accès (10$ / 10 essais)",
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
        "btn_buy_sp": "💳 Compra Única ($3 / 3 usos)",
        "btn_buy_all": "🎟️ Pase Total ($10 / 10 usos)",
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
        "btn_buy_sp": "💳 単品購入 ($3 / 3回)",
        "btn_buy_all": "🎟️ オールアクセス ($10 / 10回)",
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
        "btn_buy_sp": "💳 单次购买 ($3 / 3次)",
        "btn_buy_all": "🎟️ 全通票 ($10 / 10次)",
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
