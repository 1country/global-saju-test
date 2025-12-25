import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import os
from datetime import date
from utils import calculate_day_gan

# ==================================================
# 1. Page Config
# ==================================================
st.set_page_config(
    page_title="Specific Day Forecast | The Element",
    page_icon="📅",
    layout="wide"
)

# ==================================================
# 2. Language Session
# ==================================================
if "lang" not in st.session_state:
    st.session_state["lang"] = os.environ.get("LANGUAGE", "en")

lang = st.session_state["lang"]
# 🔑 [마스터 키 & 구매 링크]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/specific_day"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ==================================================
# 3. Global CSS (Home / 2026 Forecast와 동일)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

.stApp {
    background-image:
        linear-gradient(rgba(89, 0, 10, 0.88), rgba(89, 0, 10, 0.88)),
        url("https://i.imgur.com/sSRRsW0.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #fefefe;
    font-family: 'Gowun Batang', serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #7f1d1d !important;
    border-right: 1px solid #991b1b;
}

section[data-testid="stSidebar"] * {
    color: #fefefe !important;
}

[data-testid="stSidebarNav"] span {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

/* Card */
.card {
    background: rgba(127, 29, 29, 0.85);
    border: 1px solid #dc2626;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: #fefefe;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# 🔴 여기! 접근 체크 위치 (가장 중요)
# --------------------------------------------------
if "birth_info" not in st.session_state:
    st.markdown("""
    <div class="card" style="text-align:center;">
        <h3>🚨 Step Required</h3>
        <p style="font-size:1.1em;">
            Please complete your basic information on the Home page first.
        </p>
        <br>
        <p>⬅️ Use the sidebar to return to Home</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
# ==================================================
# 4. Sidebar (🔥 모든 페이지 공통)
# ==================================================
with st.sidebar:
    st.header("Settings")

    lang_map = {
        "en": "English",
        "ko": "한국어",
        "fr": "Français",
        "es": "Español",
        "ja": "日本語",
        "zh": "中文"
    }

    st.info(f"Current Mode: **{lang_map.get(lang, 'English')}**")

    st.write("Change Language:")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🇺🇸 EN"): st.session_state["lang"] = "en"; st.rerun()
    with c2:
        if st.button("🇰🇷 KO"): st.session_state["lang"] = "ko"; st.rerun()
    with c3:
        if st.button("🇫🇷 FR"): st.session_state["lang"] = "fr"; st.rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🇪🇸 ES"): st.session_state["lang"] = "es"; st.rerun()
    with c5:
        if st.button("🇯🇵 JA"): st.session_state["lang"] = "ja"; st.rerun()
    with c6:
        if st.button("🇨🇳 ZH"): st.session_state["lang"] = "zh"; st.rerun()

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

# ==================================================
# 5. Page Content (페이지별 내용)
# ==================================================
st.markdown("""
<div class="card">
<h2>📅 Specific Day Forecast</h2>
<p>
Choose a date and discover the elemental energy of that specific moment.
</p>
</div>
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
        "Same": { # 비견/겁재 (자아와 경쟁의 에너지)
    "ko": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 거울 속의 나를 만나는 날: 강한 주체성과 보이지 않는 경쟁",
        "d": "우주가 당신과 똑같은 주파수의 에너지를 보내주는 날입니다. 평소보다 자아 존중감이 높아지고 독립심이 폭발하여, 누구의 도움 없이도 어려운 과업을 스스로 돌파해낼 수 있는 강력한 추진력이 생깁니다. 마치 거울 속의 나를 마주하듯 본인의 장단점이 극명하게 드러나는 시기이기도 합니다. 다만, '내가 최고'라는 자만심과 '나만 옳다'는 고집이 타인과의 불협화음을 만들 수 있으니, 자신의 강한 에너지를 조절하는 '중용'의 자세가 필요합니다.",
        "money": "재물운에서는 '탈재(奪財)'의 기운이 감돕니다. 이는 내 주머니의 돈을 노리는 경쟁자가 있거나, 주변 지인으로 인해 예상치 못한 지출이 생길 수 있음을 암시합니다. 친구가 투자 제안을 하거나 돈을 빌려달라고 할 수 있는데, 오늘 가장 현명한 대처법은 **'적극적인 베풂'**입니다. 차라리 먼저 기분 좋게 밥을 사거나 작은 기부를 함으로써 나갈 돈의 액운을 미리 액땜하는 것이 훨씬 유리합니다.",
        "love": "연애 전선에 묘한 긴장감이 흐릅니다. 연인이 있다면 사소한 의견 차이가 '누가 이기나 보자'는 식의 자존심 싸움으로 번져 냉전이 될 수 있습니다. 오늘은 상대방이 나의 경쟁자가 아닌, 보듬어줘야 할 동반자임을 잊지 마세요. 싱글이라면 마음에 드는 상대 주변에 경쟁자가 나타날 수 있습니다. 오늘 당신의 필살기는 카리스마가 아닌 **'무조건적인 포용과 져주기'**입니다.",
        "health": "내면의 에너지가 너무 차올라 가만히 있으면 오히려 몸살이 나거나 짜증이 늘 수 있습니다. 이 넘치는 에너지를 밖으로 분출해야 합니다. 땀이 흠뻑 날 정도의 고강도 운동, 등산, 혹은 활동량이 많은 취미 생활을 통해 에너지를 순환시키세요. 가벼운 명상은 들뜬 마음을 가라앉히는 데 큰 도움이 됩니다.",
        "action": "1. 마음 주문: '내 생각만 옳은 것은 아니다' (고집 내려놓기)\n2. 행운의 행동: 가까운 동료나 친구에게 따뜻한 차 한 잔 대접하기\n3. 주의사항: 새로운 동업 제안, 금전 거래, 보증은 오늘 절대 금물입니다.",
        "lucky": "🕶️ 선글라스(시선 분산), 🪞 거울(객관화), ☕ 커뮤니티 카페"
    },
    "en": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 Meeting Your Mirror: Strong Sovereignty & Subtle Competition",
        "d": "Today, the universe vibrates at the same frequency as your own soul. Your self-esteem and independence are at an all-time high, granting you the drive to conquer difficult tasks single-handedly. It’s a day where your strengths and weaknesses are magnified, as if staring into a cosmic mirror. However, beware of the 'I am always right' trap. Success today depends on your ability to channel your intense energy into constructive actions rather than stubborn arguments.",
        "money": "The energy of 'Wealth Depletion' is present. This indicates potential competition for your resources or unexpected social expenses. You might encounter friends seeking loans or questionable investment advice. The best remedy? **'Proactive Generosity.'** By choosing to treat a friend to a meal or making a small donation, you satisfy the energy of 'giving' on your own terms, preventing larger, involuntary losses.",
        "love": "A subtle tension exists in romantic relationships. Minor disagreements can easily escalate into ego battles if you aren't careful. Remember, your partner is your ally, not your rival. For singles, you may find yourself competing for someone's attention. Your winning strategy today is not to overpower others, but to **'graciously yield'** and show emotional maturity.",
        "health": "Excess energy can lead to restlessness or physical tension. You need a healthy outlet for this internal fire. High-intensity workouts, long hikes, or active social hobbies are highly recommended to keep your energy circulating. Practice grounding through meditation if you feel overly irritable.",
        "action": "1. Daily Mantra: 'I am open to other perspectives.'\n2. Luck Action: Treat a colleague to coffee to harmonize relations.\n3. Warning: Avoid new business partnerships or lending money today.",
        "lucky": "🕶️ Sunglasses, 🪞 Mirrors, 👫 Social Clubs or Lounges"
    },
    "fr": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 Rencontre avec votre Miroir : Souveraineté et Compétition",
        "d": "Aujourd'hui, l'univers vibre à la même fréquence que vous. Votre indépendance et votre confiance en vous explosent, vous donnant la force de réussir seul. C'est un jour de réflexion où vos qualités et défauts sont amplifiés. Attention toutefois à l'entêtement : l'idée que 'vous avez seul raison' pourrait créer des frictions.",
        "money": "Risque de 'dispersion des richesses'. Des proches pourraient solliciter votre aide financière ou des dépenses imprévues pourraient survenir. La meilleure stratégie est la **'Générosité Active'**. Offrir un repas ou faire un don permet de maîtriser ce flux sortant et d'éviter des pertes plus importantes.",
        "love": "Tension dans l'air. Ne laissez pas votre ego transformer une simple discussion en bataille. Pour les célibataires, la compétition est forte. Votre atout ? **'Laisser gagner l'autre'** avec élégance pour montrer votre maturité.",
        "health": "Trop d'énergie interne ! Bougez pour éviter l'irritabilité. Le sport intensif ou une longue marche sont vos meilleurs alliés. Méditez pour calmer votre esprit bouillonnant.",
        "action": "1. Mantra : 'Mon point de vue n'est pas le seul.'\n2. Action : Offrir un café à un ami.\n3. Attention : Pas de prêts d'argent ni de nouvelles associations.",
        "lucky": "🕶️ Lunettes de soleil, 🪞 Miroir, ☕ Café ou espaces sociaux"
    },
    "es": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 Encuentro con tu Espejo: Soberanía y Competencia",
        "d": "Hoy el universo vibra en tu misma frecuencia. Tu independencia y autoestima están en su punto máximo, dándote el impulso para resolver todo por ti mismo. Es un día de autodescubrimiento donde tus virtudes y defectos se reflejan claramente. Evita la terquedad; el creer que solo tú tienes la razón puede causar conflictos innecesarios.",
        "money": "Energía de 'pérdida de riqueza'. Esto sugiere gastos inesperados por compromisos sociales o amigos pidiendo préstamos. La solución es la **'Generosidad Proactiva'**. Al invitar a alguien o donar voluntariamente, armonizas la energía del dinero y evitas pérdidas mayores imprevistas.",
        "love": "Tensiones por el ego. No permitas que una diferencia de opinión se convierta en una guerra fría con tu pareja. Si estás soltero, podrías enfrentar rivales. Tu mejor jugada hoy es **'ceder con gracia'**, demostrando confianza y calma.",
        "health": "Exceso de energía que necesita ser liberada. El ejercicio intenso o el senderismo son ideales para evitar el estrés físico o la irritabilidad. La meditación te ayudará a centrarte.",
        "action": "1. Mantra: 'Acepto otras opiniones con humildad.'\n2. Acción: Invita a un colega a un café.\n3. Advertencia: No prestes dinero ni firmes contratos de sociedad hoy.",
        "lucky": "🕶️ Gafas de sol, 🪞 Espejo, 👫 Lugares de reunión social"
    },
    "ja": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 鏡の中の自分に出会う日：強い自律心と潜在的な競争",
        "d": "今日は宇宙があなたと同じ周波数のエネルギーを送ってくれる日です。自律心と独立心が高まり、誰の助けを借りずとも困難な課題を自力で突破できる強い推進力が生まれます。鏡を見るように自分の長所と短所が明確になる時期です。しかし、「自分が一番正しい」という固執が対人関係に摩擦を生む可能性があるため、エネルギーを調整する「中庸」の姿勢が求められます。",
        "money": "財運においては「奪財（だつざい）」、つまり財を奪われる気配があります。知人からの借金の申し込みや、予期せぬ交際費が発生しやすい時です。最も賢明な対処法は**「積極的な施し」**です。自分から進んで食事をご馳走したり、少額の寄付をしたりすることで、不運な出費を事前に「厄払い」することができます。",
        "love": "恋愛面では奇妙な緊張感が流れます。パートナーがいる場合、些細な意見の相違がプライドをかけた争いに発展し、冷戦状態になる恐れがあります。今日は相手を「競争相手」ではなく「支え合う存在」として接しましょう。シングルの人は恋のライバルが現れるかも。今日の秘策は、強がるのではなく**「潔く負けてあげる」**心の余裕です。",
        "health": "エネルギーが溢れすぎて、じっとしているとかえって体調を崩したり、イライラしたりします。この有り余るエネルギーを外に放出すべきです。激しい運動や登山などを通じて、心身の循環を促してください。軽い瞑想は高ぶった感情を鎮めるのに効果的です。",
        "action": "1. 呪文：「他人の意見にも一理ある」\n2. 幸運の行動：同僚や友人に温かいお茶を差し出す\n3. 注意事項：共同事業の提案やお金の貸し借り、保証人になることは厳禁です。",
        "lucky": "🕶️ サングラス、🪞 鏡、☕ カフェ・交流の場"
    },
    "zh": {
        "score": 3, "star": "⭐⭐⭐",
        "t": "🤝 与镜中之我相遇：强大的主观意识与隐形的竞争",
        "d": "今天宇宙的能量与你的个人频率完全同步。你的自尊心与独立意识爆发，拥有不依靠任何人也能独当一面的强大推动力。这像是一面镜子，让你看清自己的优缺点。但要警惕“唯我独尊”的傲慢和固执，以免与他人产生不和谐的摩擦，学会调控能量的“中庸之道”是今天的核心。",
        "money": "财运方面带有“比劫夺财”的意味。这意味着可能会有竞争者觊觎你的利益，或者因人际关系产生意料之外的支出。朋友可能会提出借钱或合作邀请。今天最聪明的化解方法是**“主动布施”**。主动请客或进行小额捐款，以此“破财消灾”，避免更严重的身不由己的损失。",
        "love": "恋爱关系中存在微妙的火药味。有伴侣的人容易因琐事陷入自尊心的较量，甚至演变成冷战。请记住，伴侣是你的爱人而非对手。单身者可能会遇到情敌。今天你的必杀技不是展现霸气，而是**“无条件地宽容与示弱”**，展现你的大度。",
        "health": "精力过剩，若无处发泄则容易导致身体酸痛或心情烦躁。必须将这股能量排出体外。建议进行大汗淋漓的高强度运动、登山或户外活动。冥想则能帮助你平复浮躁的心情。",
        "action": "1. 心灵咒语：“我的想法不一定全对” (放下固执)\n2. 开运行动：请同事或朋友喝杯热茶\n3. 注意事项：严禁任何形式的合伙提议、金钱借贷或担保。",
        "lucky": "🕶️ 墨镜, 🪞 镜子, ☕ 社交咖啡馆"
    }
},
        
        "Output": { # 식상 (예술적 감각과 생산적인 에너지)
    "ko": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 창조적 영감이 폭발하는 날: 세상이 당신의 무대입니다",
        "d": "내면에 억눌려 있던 예술적 끼와 아이디어가 화산처럼 분출되는 날입니다. 머리 회전이 평소보다 2배는 빨라지며, 복잡한 문제를 한 번에 해결할 기발한 기획력이 돋보입니다. 오늘은 관객이 아닌 주인공이 되어야 하는 날입니다. 당신의 능력을 숨기지 말고 당당하게 세상에 드러내세요. 당신의 말 한마디, 몸짓 하나가 주변 사람들에게 강력한 영감을 줄 것입니다.",
        "money": "당신의 독창적인 재주와 세련된 말솜씨가 곧바로 금전적 가치로 치환됩니다. 프리랜서, 영업직, 마케터라면 평소보다 높은 성과를 올릴 수 있는 '골든 데이'입니다. 다만, 에너지가 고조되어 기분에 취한 나머지 계획에 없던 과감한 '지름신'이 강림할 수 있으니 카드 결제 전 딱 세 번만 더 생각하세요.",
        "love": "유머 감각과 센스가 최고조에 달해 가만히 있어도 이성의 시선을 한몸에 받습니다. 평소 마음에 두었던 상대가 있다면 오늘이 바로 승부수를 던질 날입니다. 이미 연인이 있다면 재치 있는 이벤트로 상대방을 감동시켜 보세요. 여성이라면 배우자에게 지적이나 잔소리 대신 따뜻한 칭찬과 애교를 보여줄 때 관계가 비약적으로 발전합니다.",
        "health": "두뇌 회전과 외부 활동량이 많아 저녁에는 급격한 체력 방전이 올 수 있습니다. 목소리를 많이 쓰는 날이니 따뜻한 차로 목을 보호하고, 초콜릿이나 과일 같은 달콤한 간식으로 즉각적인 당 충전을 해주는 것이 좋습니다. 충분한 수면이 내일의 창의력을 보장합니다.",
        "action": "1. 자기 암시: '나는 세상을 아름답게 만드는 아티스트다.'\n2. 행운 행동: SNS에 당신의 작업물 공유하기, 노래방 가기, 전시회 관람\n3. 주의 사항: 감정에 치우친 말실수 주의 (말하기 전 1초만 멈추기).",
        "lucky": "🎤 블루투스 마이크, 🎨 파스텔 톤 아이템, 🍰 달콤한 마카롱"
    },
    "en": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 Explosion of Creative Inspiration: The World is Your Stage",
        "d": "Today, your suppressed artistic talents and ideas erupt like a volcano. Your brain processes information twice as fast as usual, granting you brilliant planning skills to solve complex problems effortlessly. Don't be an observer today; be the protagonist. Showcase your abilities boldly. Your every word and gesture will serve as a powerful inspiration to those around you.",
        "money": "Your unique talents and polished eloquence translate directly into monetary value. For freelancers, salespeople, or marketers, this is a 'Golden Day' for high performance. However, your elevated mood might trigger impulsive luxury purchases. Think three times before swiping your card.",
        "love": "Your peak sense of humor and wit will naturally draw people to you. If there is someone you like, today is the perfect day to express your feelings. For couples, a witty surprise will deepen your bond. Women can dramatically improve relationship harmony by replacing nagging with warm compliments and affection.",
        "health": "High mental and physical activity may lead to a sudden energy crash by evening. Since you'll likely be talking a lot, protect your throat with warm tea. Recharge instantly with sweet snacks like chocolate or fruit. Quality sleep is essential to sustain tomorrow's creativity.",
        "action": "1. Affirmation: 'I am an artist who makes the world beautiful.'\n2. Luck Action: Share your creative work on social media, visit a gallery, or go to karaoke.\n3. Warning: Watch for emotional slips of the tongue. Pause for one second before speaking.",
        "lucky": "🎤 Microphone, 🎨 Pastel-colored items, 🍰 Sweet Macarons"
    },
    "fr": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 Explosion d'Inspiration Créative : Le Monde est Votre Scène",
        "d": "Aujourd'hui, vos talents artistiques et vos idées fusent comme un volcan. Votre cerveau fonctionne à toute allure, vous offrant une capacité de planification géniale. Ne soyez pas un simple spectateur ; soyez le protagoniste. Montrez vos capacités avec assurance. Chaque parole et geste inspirera puissamment votre entourage.",
        "money": "Vos talents uniques et votre éloquence se transforment directement en gains financiers. Pour les freelances ou les commerciaux, c'est une 'Journée Dorée'. Attention toutefois aux achats compulsifs sous le coup de l'émotion. Réfléchissez bien avant de dépenser.",
        "love": "Votre humour et votre esprit captivent tout le monde. C'est le moment idéal pour déclarer votre flamme. En couple, une surprise pleine d'esprit ravira votre partenaire. Les femmes renforceront leur relation en remplaçant les reproches par des compliments sincères.",
        "health": "Une forte activité mentale peut épuiser vos réserves en fin de journée. Protégez votre gorge avec du thé chaud. Rechargez vos batteries avec des douceurs sucrées. Un bon sommeil est crucial pour la créativité de demain.",
        "action": "1. Affirmation : 'Je suis un artiste qui embellit le monde.'\n2. Action : Partager vos créations sur les réseaux, aller au musée ou au karaoké.\n3. Attention : Évitez les paroles impulsives. Marquez une pause avant de parler.",
        "lucky": "🎤 Micro, 🎨 Accessoires aux tons pastels, 🍰 Macarons"
    },
    "es": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 Explosión de Inspiración Creativa: El Mundo es tu Escenario",
        "d": "Hoy, tus talentos artísticos e ideas brotan como un volcán. Tu mente trabaja más rápido que nunca, dándote una capacidad de planificación brillante. No seas un observador; sé el protagonista. Muestra tus habilidades con confianza. Cada palabra y gesto será una gran inspiración para los demás.",
        "money": "Tus talentos únicos y elocuencia se traducen directamente en valor económico. Para freelancers y vendedores, es un 'Día Dorado'. Sin embargo, tu buen humor podría incitar compras impulsivas. Piénsalo tres veces antes de usar tu tarjeta.",
        "love": "Tu sentido del humor y agudeza atraerán todas las miradas. Es el día perfecto para confesar tus sentimientos. En pareja, una sorpresa ingeniosa fortalecerá el vínculo. Las mujeres verán mejoras en su relación al cambiar los regaños por elogios afectuosos.",
        "health": "La alta actividad mental puede causar un bajón de energía por la noche. Protege tu garganta con té caliente. Recárgate con dulces como chocolate o fruta. Dormir bien es vital para mantener la creatividad.",
        "action": "1. Afirmación: 'Soy un artista que embellece el mundo.'\n2. Acción: Comparte tu trabajo en redes sociales, visita una galería o ve al karaoke.\n3. Advertencia: Cuidado con las palabras impulsivas. Pausa un segundo antes de hablar.",
        "lucky": "🎤 Micrófono, 🎨 Objetos de tonos pastel, 🍰 Macarons dulces"
    },
    "ja": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 創造的インスピレーションの爆発：世界があなたの舞台です",
        "d": "内に秘めていた芸術的な才能とアイデアが火山のように噴出する日です。頭の回転がいつもの2倍速くなり、複雑な問題を解決する独創的な企画力が光ります。今日は観客ではなく、主人公になるべき日です。堂々と自分の能力を世に示してください。あなたの言葉一つ、仕草一つが周囲に強いインスピレーションを与えるでしょう。",
        "money": "あなたの独創的な才能と洗練された話術が、そのまま金銭的価値に変わります。フリーランスや営業職にとって、最高の成果を上げられる「ゴールデンデー」です。ただし、気分が高揚して予定外の衝動買いをしてしまう恐れがあるので、財布を開く前によく考えましょう。",
        "love": "ユーモアのセンスが最高潮に達し、何もしなくても異性の視線を独占します。意中の人がいるなら、今日が勝負の日です。パートナーがいる方は、気の利いたサプライズで相手を感動させてみて。女性は小言を封印し、褒め言葉と愛嬌を見せることで関係が飛躍的に良くなります。",
        "health": "脳の活動量が多く、夜には急激なエネルギー切れが起こるかもしれません。喉を酷使する日なので、温かいお茶で保護し、マカロンやフルーツなどの甘いもので糖分を補給してください。十分な睡眠が明日の創造力を支えます。",
        "action": "1. 自己暗示：『私は世界を美しくするアーティストだ』\n2. 幸運の行動：SNSで作品を共有する、美術館に行く、カラオケで歌う\n3. 注意事項：感情に任せた失言に注意（話す前に一呼吸置くこと）。",
        "lucky": "🎤 マイク、🎨 パステルカラーのアイテム、🍰 甘いマカロン"
    },
    "zh": {
        "score": 4, "star": "⭐⭐⭐⭐⭐",
        "t": "🎨 创意灵感大爆发：世界就是你的舞台",
        "d": "今天，你内心积压已久的艺术才华和创意将如火山般喷发。头脑运转速度比平时快两倍，卓越的策划能力让你能轻松解决复杂问题。今天不要做旁观者，要做主角。大胆展示你的才华吧，你的言谈举止将给周围人带来巨大的启发。",
        "money": "你独特的才华和圆滑的口才会直接转化为财富。对于自由职业者或销售人员来说，这是高绩效的“黄金日”。但由于情绪高涨，可能会引发冲动消费。刷卡前请三思。",
        "love": "幽默感和灵敏度达到顶峰，让你成为异性关注的焦点。如果有心仪的对象，今天就是表白的最佳时机。已有伴侣的人可以用别出心裁的惊喜打动对方。女性通过温柔的赞美代替唠叨，会让夫妻关系飞跃式提升。",
        "health": "由于脑力消耗和活动量巨大，傍晚可能会感到精疲力竭。今天是费嗓子的一天，请喝热茶保护喉咙，并吃点巧克力或水果等甜食补充能量。充足的睡眠是保持明天创造力的关键。",
        "action": "1. 自我暗示：“我是美化世界的艺术家。”\n2. 开运行动：在社交平台分享作品、看展览、去KTV唱歌\n3. 注意事项：谨防情绪化的失言（说话前先停顿一秒）。",
        "lucky": "🎤 麦克风, 🎨 柔和粉色系物品, 🍰 甜点/马卡龙"
    }
},
        "Wealth": { # 재성 (결과 중심적이며 현실적인 수확의 에너지)
    "ko": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 황금빛 결실을 맺는 날: 당신의 노력이 현금화되는 순간",
        "d": "막연한 기대나 뜬구름 잡는 소리는 이제 그만두세요. 오늘은 철저하게 현실의 법칙이 지배하는 날입니다. 당신의 뇌는 무엇이 나에게 이득이 되고 손해인지 본능적으로 계산해낼 것입니다. 그동안 공들여온 프로젝트나 계획들이 마침내 눈에 보이는 '결과물'로 나타나며, 과정보다는 확실한 '숫자'와 '실적'이 당신의 가치를 증명해 줄 것입니다.",
        "money": "금전운 최상(Best)! 하늘에서 풍요의 비가 내리는 형국입니다. 잊고 있던 미수금이 들어오거나, 보너스, 혹은 투자했던 자산의 가치가 급상승하는 경험을 할 수 있습니다. 오늘은 단순히 돈을 버는 것뿐만 아니라, 사고 싶었던 물건을 최적의 가격에 얻는 등 '돈을 잘 쓰는' 감각도 매우 날카롭습니다.",
        "love": "감성적인 밀당보다는 현실적인 조건과 신뢰가 사랑의 중심이 됩니다. 남성은 나를 믿고 따라주는 이성운이 강하며, 여성은 능력 있고 경제적 기반이 튼튼한 상대와 인연이 닿습니다. 맛집 투어나 쇼핑, 오감을 자극하는 화려한 데이트가 행운을 더욱 증폭시킵니다.",
        "health": "전반적인 컨디션은 활기차지만, 성과에 대한 과도한 집착이 신경성 두통이나 소화 불량을 유발할 수 있습니다. '돈을 세느라 밤새는 줄 모른다'는 말처럼 과로하기 쉬운 날이니 의식적인 휴식이 필요합니다. 특히 하체 운동이나 스쿼트가 재물을 담는 당신의 그릇을 튼튼하게 지켜줄 것입니다.",
        "action": "1. 풍요 주문: '나는 부를 끌어당기는 자석이다.' (확언)\n2. 행운 행동: 지갑 안 영수증 정리, 복권 구매, 가계부 앱 점검\n3. 주의 사항: 들어온 돈을 자랑하지 마세요. 조용히 챙겨야 내 것이 됩니다.",
        "lucky": "💳 가죽 지갑/현금 뭉치, 🏦 은행/백화점 라운지, 🥩 고기 요리/미슐랭 맛집"
    },
    "en": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 The Golden Harvest: The Moment Your Efforts Turn into Cash",
        "d": "Stop daydreaming. Today is governed by the laws of reality. Your mind will instinctively calculate gains and losses with cold precision. Long-term projects finally manifest into tangible results. Today, 'Numbers' and 'Metrics' will prove your worth more than any process or intention.",
        "money": "Best Financial Luck! It is raining abundance. You may experience unexpected bonuses, the settlement of overdue debts, or a surge in investment value. Beyond earning, your sense of 'smart spending' is sharp—it's the perfect day to secure a great deal on a high-value purchase.",
        "love": "Realistic conditions and trust take center stage over emotional games. Men will attract supportive partners, while women will connect with capable individuals with solid foundations. Indulgent dates, such as fine dining or luxury shopping, will amplify your luck.",
        "health": "General vitality is high, but obsessing over results may cause tension headaches or indigestion. You risk overworking from sheer excitement. Conscious rest is mandatory. Lower-body exercises like squats will strengthen your 'vessel' to hold this incoming wealth.",
        "action": "1. Wealth Mantra: 'I am a magnet for financial abundance.'\n2. Luck Action: Organize your wallet, buy a lottery ticket, or review your budget.\n3. Warning: Keep your gains private. Quietly securing your assets is the key to keeping them.",
        "lucky": "💳 Leather Wallet/Cash, 🏦 Bank/Mall Lounges, 🥩 Fine Steak/Gourmet Dining"
    },
    "fr": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 La Récolte Dorée : Quand vos efforts se transforment en profit",
        "d": "Fini les rêves vagues. Aujourd'hui est régi par la réalité brute. Votre esprit calculera instinctivement les profits. Les projets de longue date se concrétisent. Aujourd'hui, les 'Chiffres' et les 'Résultats' prouvent votre valeur plus que n'importe quel discours.",
        "money": "Excellente chance financière ! Il pleut de l'abondance. Bonus inattendus, retours sur investissements ou remboursements de dettes sont au rendez-vous. C'est aussi un jour idéal pour faire des achats intelligents et dénicher la perle rare au meilleur prix.",
        "love": "Le réalisme et la confiance l'emportent sur les jeux de séduction. Les hommes attirent des partenaires dévouées, et les femmes rencontrent des personnes aux bases solides. Les sorties luxueuses et le shopping portent chance.",
        "health": "Grande vitalité, mais attention au surmenage lié à l'excitation des gains. L'obsession des résultats peut causer des maux de tête. Les exercices des jambes renforcent votre capacité à stabiliser votre fortune.",
        "action": "1. Mantra d'abondance : 'Je suis un aimant pour la richesse.'\n2. Action chanceuse : Organiser son portefeuille, acheter un billet de loterie.\n3. Attention : Ne vous vantez pas de vos gains. La discrétion est la mère de la sûreté.",
        "lucky": "💳 Portefeuille en cuir, 🏦 Banque/Grands Magasins, 🥩 Dîner gastronomique"
    },
    "es": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 La Cosecha de Oro: El momento en que tu esfuerzo se vuelve efectivo",
        "d": "Basta de soñar despierto. Hoy mandan las leyes de la realidad. Tu mente calculará ganancias y pérdidas con precisión instintiva. Los proyectos largos finalmente dan frutos tangibles. Hoy, los 'Números' y el 'Éxito' hablan por ti.",
        "money": "¡La mejor suerte financiera! Llueve abundancia. Espera bonos inesperados o un aumento en tus inversiones. Tu instinto para las compras inteligentes está muy agudo; es el día ideal para conseguir ofertas en artículos de lujo.",
        "love": "Las condiciones realistas y la confianza superan a las emociones pasajeras. Los hombres atraerán parejas leales; las mujeres conectarán con personas de gran solvencia. Citas sensoriales como cenas gourmet o compras aumentarán tu suerte.",
        "health": "Vitalidad alta, pero la obsesión por el éxito puede causar migrañas por tensión. Cuidado con el exceso de trabajo por la emoción de ganar. Los ejercicios de piernas te ayudarán a 'sostener' esta riqueza entrante.",
        "action": "1. Mantra de riqueza: 'Soy un imán para la abundancia.'\n2. Acción: Organiza tu billetera, compra lotería o revisa tus finanzas.\n3. Advertencia: No presumas tus ganancias. El dinero prefiere el silencio.",
        "lucky": "💳 Billetera de cuero, 🏦 Banco/Centro Comercial, 🥩 Cena de gala/Cortes finos"
    },
    "ja": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 黄金の収穫：努力が現金に変わる瞬間",
        "d": "夢想は終わりです。今日は徹底的に現実的な法則が支配する日です。何が利益になり、何が損になるか、脳が本能的に計算します。これまで準備してきたことが「数字」や「実績」として現れ、過程よりも確かな結果があなたの価値を証明します。",
        "money": "金運最高（Best）！豊かさの雨が降る兆しです。未回収金の入金やボーナス、投資価値の急騰が期待できます。稼ぐだけでなく、欲しかった物を最安値で手に入れるような「賢い支出」のセンスも抜群です。",
        "love": "感情的な駆け引きよりも、現実的な条件と信頼が愛の柱となります。男性は献身的なパートナーに恵まれ、女性は経済力の安定した相手との縁があります。美食やショッピングなど、五感を満たす華やかなデートが幸運を呼びます。",
        "health": "全体的なコンディションは良いですが、結果への執着が神経性頭痛を招くかもしれません。稼ぐことに夢中で働きすぎないよう、意識的な休息が必要です。下半신を鍛える運動が、財運を逃さない器を強くしてくれます。",
        "action": "1. 豊かさの呪文：「私は富を引き寄せる磁石だ」\n2. 幸運の行動：財布の中の整理、宝くじ購入、家計簿のチェック\n3. 注意事項：得た利益を自慢しないでください。静かに守ることが肝心です。",
        "lucky": "💳 革の財布/現金, 🏦 銀行/ラウンジ, 🥩 肉料理/ミシュラン店"
    },
    "zh": {
        "score": 5, "star": "⭐⭐⭐⭐⭐",
        "t": "💰 黄金收获日：努力转化为财富的时刻",
        "d": "停止幻想。今天受现实法则主宰。你的大脑会本能地精准计算得失。长期积累的项目终于迎来显现成果的时刻。今天，“数字”和“业绩”比任何过程都能更好地证明你的价值。",
        "money": "财运顶峰！ abundance 盈门。可能会收到意外奖金、欠款回笼或投资升值。除了赚钱，你对“聪明消费”的感觉也很敏锐，非常适合以极佳的价格买入心仪已久的物品。",
        "love": "现实条件与信任感比情感博弈更重要。男性会有贤内助般的异性缘，女性则易结识经济基础雄厚的伴侣。美食之旅、购物等能刺激感官的华丽约会能进一步催旺运气。",
        "health": "精力充沛，但过度执着于结果可能导致神经性头痛或消化不良。小心因兴奋而过劳，需要有意识地休息。加强下肢锻炼（如深蹲）能稳固你承载财富的“容器”。",
        "action": "1. 财富咒语：“我是吸引财富的磁石。”\n2. 开运行动：整理钱包收据、买彩票、查看理财账单\n3. 注意事项：财不外露。闷声发大财才能真正留住财富。",
        "lucky": "💳 真皮钱包/现金, 🏦 银行/高端商场休息室, 🥩 顶级牛排/米其林餐厅"
    }
},
        "Power": { # 관성 (사회적 규율과 리더십을 단련하는 에너지)
    "ko": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ 왕관의 무게를 견디는 날: 인내가 만드는 고결한 명예",
        "d": "주변의 시선, 엄격한 규칙, 그리고 막중한 책임감이 당신의 어깨를 누르는 날입니다. 상사의 까다로운 지시나 촉박한 마감이 심리적 압박으로 다가올 수 있습니다. 하지만 기억하세요. 다이아몬드는 거대한 압력을 견뎌내었을 때 비로소 탄생합니다. 오늘 겪는 이 스트레스는 당신을 진정한 '리더'로 성장시키기 위한 우주의 시험이며, 이를 묵묵히 버텨낼 때 당신의 명예와 사회적 평판은 비약적으로 상승할 것입니다.",
        "money": "당장의 현금 흐름보다는 미래를 위한 '명예 지수'가 올라가는 날입니다. 승진이나 공공 프로젝트 참여 등 장기적인 수익 기반을 다지는 운세입니다. 재물적으로는 세금 체납, 과태료, 혹은 의무적인 부조금 등 피할 수 없는 지출이 생길 수 있으니 꼼꼼한 자금 관리가 필요합니다.",
        "love": "업무적인 긴장감이 연애 전선까지 영향을 줄 수 있습니다. 밖에서 받은 스트레스를 무의식중에 파트너에게 쏟아내지 않도록 각별히 주의하세요. 오늘은 로맨틱한 이벤트보다 서로의 고충을 들어주는 '신뢰의 대화'가 필요한 때입니다. 여성이라면 카리스마 있고 배울 점이 많은 듬직한 이성과의 인연이 닿는 날입니다.",
        "health": "스트레스 지수가 최고조에 달해 어깨 결림, 목통증, 혹은 신경성 편두통이 올 수 있습니다. 오늘은 자기 자신을 채찍질하기보다는 이완해 주어야 합니다. 격렬한 근력 운동보다는 요가, 명상, 혹은 반신욕을 통해 경직된 몸과 마음의 긴장을 풀어주는 것이 최고의 보약입니다.",
        "action": "1. 인내 주문: '이 또한 지나가리라, 나는 더 강해지고 있다.'\n2. 행운 행동: 격식을 차린 옷차림(정장), 시계 착용, 5분 일찍 도착하기\n3. 주의 사항: 신호 위반, 사소한 규칙 어기기, 지각은 명예에 치명타를 입힙니다.",
        "lucky": "👔 잘 다려진 셔츠/시계, 🏛️ 도서관/정부 청사, 🧘 숲속 명상 센터"
    },
    "en": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ Day of the Crown's Weight: Honor Forged in Patience",
        "d": "Social expectations, strict rules, and heavy responsibilities weigh on your shoulders today. Demanding instructions from superiors or tight deadlines may feel overwhelming. Remember, a diamond is only formed under immense pressure. The stress you face today is a cosmic test designed to forge you into a true leader. By enduring this with grace, your reputation and social standing will rise to new heights.",
        "money": "Your 'Honor Quotient' rises rather than immediate cash flow. This is a time to solidify your long-term income base through promotions or public projects. Financially, be prepared for mandatory expenses such as taxes, bills, or social obligations. Manage your funds with extra care.",
        "love": "Work-related tension may spill over into your romantic life. Be mindful not to vent your frustrations on your partner. Instead of romantic gestures, focus on 'trust-building conversations' where you listen to each other’s struggles. Women are likely to encounter a charismatic and reliable partner who offers great inspiration.",
        "health": "Stress levels peak, potentially causing stiff shoulders or migraines. Today, prioritize relaxation over self-discipline. Avoid high-intensity workouts; instead, choose yoga, meditation, or a warm bath to release the physical and mental tension accumulated throughout the day.",
        "action": "1. Resilience Mantra: 'This too shall pass, and I am becoming stronger.'\n2. Luck Action: Dress formally, wear a watch, and arrive 5 minutes early to all appointments.\n3. Warning: Traffic violations, breaking small rules, or lateness will severely damage your reputation today.",
        "lucky": "👔 Formal Suit/Watch, 🏛️ Government Building, 🧘 Meditation Center"
    },
    "fr": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ Le Poids de la Couronne : L'Honneur forgé par la Patience",
        "d": "Les attentes sociales et les responsabilités pèsent lourd aujourd'hui. Le stress que vous ressentez est un test pour faire de vous un véritable leader. En endurant cela avec calme, votre réputation s'élèvera. Comme le diamant, vous brillez sous la pression.",
        "money": "C'est votre prestige qui augmente, pas votre cash immédiat. Préparez-vous à des dépenses obligatoires (taxes, factures). Gérez vos finances avec une précision rigoureuse.",
        "love": "La tension du travail peut affecter votre couple. Ne déchargez pas votre stress sur l'autre. Privilégiez l'écoute et le soutien mutuel. Les femmes pourraient être attirées par un homme charismatique et protecteur.",
        "health": "Le stress est au maximum. Attention aux maux de tête. Évitez le sport intensif ; préférez le yoga ou un bain chaud pour relâcher la pression accumulée.",
        "action": "1. Mantra : 'Cela aussi passera, je deviens plus fort.'\n2. Action : Tenue formelle, ponctualité exemplaire.\n3. Attention : Les infractions aux règles nuiront gravement à votre image aujourd'hui.",
        "lucky": "👔 Costume/Montre, 🏛️ Administration, 🧘 Méditation"
    },
    "es": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ El Peso de la Corona: Honor forjado en la Paciencia",
        "d": "Las responsabilidades y las reglas te rodean hoy. La presión externa es alta, pero como un diamante, este estrés te convierte en un líder. Aguantar con dignidad traerá reconocimiento y elevará tu estatus social.",
        "money": "Sube tu reputación más que el efectivo. Es un momento para asegurar tu futuro profesional. Ten cuidado con gastos obligatorios como impuestos o facturas imprevistas. Controla bien tu presupuesto.",
        "love": "El estrés laboral puede filtrarse en tu relación. No te desquites con tu pareja. Hoy se necesita comprensión, no drama. Las mujeres podrían conocer a un hombre con gran carisma y liderazgo.",
        "health": "Niveles de estrés al límite. Cuidado con la tensión en hombros y cuello. No te exijas físicamente; mejor opta por yoga o meditación para calmar la mente y el cuerpo.",
        "action": "1. Mantra: 'Esto también pasará y me hará más fuerte.'\n2. Acción: Viste formal, usa reloj y sé muy puntual.\n3. Advertencia: Romper reglas o llegar tarde dañará seriamente tu prestigio hoy.",
        "lucky": "👔 Traje/Reloj, 🏛️ Edificio Gubernamental, 🧘 Meditación"
    },
    "ja": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ 王冠の重みに耐える日：忍耐が創る気高い名誉",
        "d": "周囲の視線、厳しい規則、そして重い責任が肩にのしかかる日です。上司の要求や締め切りがプレッシャーになるかもしれません。しかし、ダイヤモンドが圧力の中で磨かれるように、今日の試練はあなたを真のリーダーへと成長させます。耐え抜くことで、あなたの社会的評価は飛躍的に高まるでしょう。",
        "money": "現金の流入よりも「名誉指数」が上がる日です。昇進や大きなプロジェクトへの参加など、長期的な基盤を固める運気です。出費面では、税金や公共料金、義理の出費など避けられない支払いが発生しやすいので注意が必要です。",
        "love": "仕事の緊張感をプライベートに持ち込まないよう注意しましょう。外でのストレスをパートナーにぶつけるのは厳禁です。今日は情熱的なデートよりも、お互いの苦労を分かち合う「信頼の対話」を大切に。女性はカリスマ性のある頼もしい異性との縁があります。",
        "health": "ストレスがピークに達し、肩こりや頭痛が起きやすい時です。自分を追い込むのではなく、緩めることが必要です。激しい運動より、ヨガや瞑想、半身浴で心身の緊張を解きほぐしてください。",
        "action": "1. 忍耐の呪文：『これもまた過ぎ去る、私はより強くなっている』\n2. 幸運の行動：フォーマルな服装、時計の着用、5分前行動を徹底する\n3. 注意事項：信号無視や些細なルール違反、遅刻は名誉に致命傷を与えます。",
        "lucky": "👔 スーツ/腕時計, 🏛️ 役所/図書館, 🧘 瞑想センター"
    },
    "zh": {
        "score": 2, "star": "⭐⭐",
        "t": "⚖️ 欲戴王冠，必承其重：耐性铸就的高贵名誉",
        "d": "今天，社会的期待、严格的规则和沉重的责任感笼罩着你。上司的苛刻要求或紧迫的截止日期可能会让你感到窒息。但请记住，钻石是在压力下形成的。今天的压力是宇宙对你的考验，旨在将你锻造成真正的领导者。当你默默坚持下去时，你的社会地位和名誉将获得质的飞跃。",
        "money": "与其说是财运，不如说是“名誉运”上升的日子。这是通过晋升或参与重要项目来巩固长期收益基础的时机。财物方面，可能会有税款、罚单或人情往来等不可避免的开支，请务必精细化管理财务。",
        "love": "职场的紧张感极易蔓延到感情生活。请特别注意不要将外面的负能量发泄在伴侣身上。今天比起浪漫的惊喜，更需要一次坦诚相待、互相倾听的深度交流。女性有望结识有魄力、值得学习和依赖的高素质异性。",
        "health": "压力指数达到顶点，容易出现肩膀僵硬、颈椎酸痛或神经性头痛。今天不适合挑战体能，而应以放松为主。比起高强度健身，瑜伽、冥想或泡澡是缓解身心僵硬的最佳良药。",
        "action": "1. 忍耐咒语：“这一切终将过去，而我正变得愈发强大。”\n2. 开运行动：穿着得体西装、佩戴手表、任何约会提前5分钟到达\n3. 注意事项：违章、违反小规则或迟到都会对你今天的名誉造成致命打击。",
        "lucky": "👔 熨烫平整的衬衫/手表, 🏛️ 政府机关/图书馆, 🧘 冥想中心"
    }
},
        "Resource": { # 인성 (지혜와 사랑을 받아들이는 수용의 에너지)
    "ko": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 지혜와 사랑이 샘솟는 날: 영혼을 채우는 힐링의 시간",
        "d": "마치 따뜻한 어머니의 품에 안긴 듯 마음이 한없이 편안하고 안정적인 하루입니다. 굳이 당신이 애써 노력하지 않아도 주변 사람들이 먼저 당신의 필요를 채워주는 '인복'이 터지는 시기입니다. 오늘은 밖으로 나가 에너지를 발산하기보다 내면을 가꾸고, 미뤄왔던 공부를 하거나 계획을 재점검하기에 가장 완벽한 날입니다. 인생의 '속도'에 매몰되기보다 올바른 '방향'을 정립하는 귀중한 시간을 가지세요.",
        "money": "당장 눈앞에 현금이 오가는 운은 아니지만, 미래의 부를 보장하는 '문서운'이 대길합니다. 부동산 계약, 중요한 결재, 자격증 취득 등 서류와 관련된 일에서 큰 이득이 따를 것입니다. 훗날 큰 자산이 될 지식이나 자격을 갖추는 날이니, 자신을 위한 교육이나 책 구매에 돈을 아끼지 마세요. 윗사람이나 부모님으로부터 생각지도 못한 용돈이나 지원을 받을 수도 있습니다.",
        "love": "온 세상의 사랑을 듬뿍 받는 날입니다. 연인에게 정서적인 위로를 받고 싶어지며, 상대방 역시 당신을 왕자님/공주님처럼 세심하고 따뜻하게 챙겨줄 것입니다. 싱글이라면 대화가 깊이 있게 통하고 학식이 깊어 배울 점이 많은 이성과 인연이 닿을 운입니다. 화려한 곳보다는 조용한 카페나 서점에서의 데이트가 사랑의 깊이를 더해줍니다.",
        "health": "몸이 물에 젖은 솜처럼 처지고 나른해질 수 있는데, 이는 병이 아니라 당신의 몸이 '잠시 쉬어가라'고 보내는 강력한 신호입니다. 억지로 고강도 운동을 하기보다는 낮잠을 자거나 전문가의 마사지를 받으며 몸을 이완하는 것이 최고의 보약입니다. 소화 기관이 평소보다 천천히 움직이니 자극적인 음식이나 과식은 피하는 것이 좋습니다.",
        "action": "1. 긍정 주문: '나는 충분히 사랑받을 자격이 있는 소중한 존재다.'\n2. 행운 행동: 독서, 명상, 부모님이나 스승님께 안부 전화드리기\n3. 주의 사항: 게으름과 나태함 경계 (생각만 하다가 실천의 때를 놓칠 수 있음).",
        "lucky": "📚 고전 소설/인문학 서적, ☕ 따뜻한 대추차나 허브티, 🛌 포근한 호텔 침구"
    },
    "en": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 Day of Flowing Wisdom & Love: A Time for Soul Healing",
        "d": "Today feels as safe and stable as a mother's warm embrace. Even without conscious effort, your 'People Luck' is so strong that others will naturally step forward to support and care for you. It is the perfect day for introspection, studying, or reviewing long-term plans rather than outward expansion. Instead of obsessing over 'Speed,' use this precious time to re-evaluate your life's 'Direction.'",
        "money": "While immediate cash flow may be quiet, your 'Document Luck' is exceptionally auspicious. This is a great time for signing real estate contracts, obtaining professional certifications, or securing official approvals. Invest generously in your self-improvement or books, as they will turn into significant assets later. You might also receive unexpected gifts or financial support from elders or parents.",
        "love": "You are surrounded by deep affection today. You will find yourself seeking emotional comfort from your partner, who in turn will treat you with immense care and devotion. If single, you are likely to meet someone intellectual and well-mannered who inspires respect. Dates in quiet, thoughtful places like libraries or cozy cafes will deepen your connection.",
        "health": "Feeling unusually lethargic or heavy is not a sign of illness, but a signal from your body to slow down. Avoid forcing yourself into intense workouts. A long nap or a professional massage is the best medicine today. Your digestion may be slower than usual, so opt for light, warm meals over heavy feasts.",
        "action": "1. Affirmation: 'I am a precious being worthy of unconditional love.'\n2. Luck Action: Reading, meditation, or calling your parents/mentors.\n3. Warning: Beware of excessive procrastination. Don't let deep thinking turn into missed opportunities.",
        "lucky": "📚 Classic Literature, ☕ Warm Herbal Tea, 🛌 Soft Premium Bedding"
    },
    "fr": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 Jour de Sagesse et d'Amour : Temps pour la Guérison de l'Âme",
        "d": "Une journée aussi apaisante que les bras d'une mère. Votre 'Chance avec les gens' est excellente ; on vous aide spontanément. C'est le moment idéal pour étudier et planifier. Au lieu de viser la 'Vitesse', concentrez-vous sur la 'Direction' de votre vie.",
        "money": "Excellente chance avec les documents officiels (contrats, licences). Investissez dans votre savoir, cela deviendra un actif précieux. Des cadeaux inattendus de la part de vos aînés sont possibles.",
        "love": "Vous êtes choyé aujourd'hui. Votre partenaire prendra soin de vous comme d'une royauté. Pour les célibataires, attendez-vous à rencontrer une personne cultivée et inspirante. Privilégiez les rendez-vous calmes.",
        "health": "La léthargie est un signal pour se reposer. Évitez le sport intensif. Un massage ou une sieste est le meilleur remède. Mangez léger.",
        "action": "1. Mantra : 'Je mérite d'être aimé inconditionnellement.'\n2. Action : Lecture, méditation, appeler ses parents.\n3. Attention : Ne confondez pas repos et paresse totale.",
        "lucky": "📚 Beaux livres, ☕ Thé chaud, 🛌 Repos et confort"
    },
    "es": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 Día de Sabiduría y Amor: Tiempo para la Sanación del Alma",
        "d": "Un día tan seguro y estable como el abrazo de una madre. Tu 'Suerte con la Gente' es fuerte; los demás te ayudarán sin que lo pidas. Es el momento perfecto para el estudio y la introspección. Enfócate en la 'Dirección' de tu vida más que en la 'Velocidad'.",
        "money": "Excelente 'Suerte de Documentos' (contratos, licencias). Invierte en tu educación; los libros que compres hoy serán riqueza mañana. Podrías recibir apoyo financiero de tus padres o superiores.",
        "love": "Te sentirás muy amado. Tu pareja te tratará con una dedicación especial. Si estás soltero, podrías conocer a alguien intelectual y digno de admiración. Una cita en un lugar tranquilo será ideal.",
        "health": "Sentirse cansado es un aviso para descansar. No te fuerces físicamente. Una siesta o un masaje será tu mejor medicina hoy. Evita las comidas pesadas.",
        "action": "1. Afirmación: 'Soy un ser valioso digno de todo amor.'\n2. Acción: Leer, meditar o llamar a tus mentores.\n3. Advertencia: Cuidado con la procrastinación excesiva.",
        "lucky": "📚 Libros clásicos, ☕ Té de hierbas caliente, 🛌 Ropa de cama cómoda"
    },
    "ja": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 知恵と愛が溢れる日：魂を充たす癒やしの時間",
        "d": "母の懐に抱かれているような、安らぎに満ちた一日です。周囲の人々が自然とあなたの力になってくれる「人徳」に恵まれます。活動的に動くよりも、内面を磨き、勉強や計画の再確認に時間を割くのが最適です。「速度」よりも「方向」を見つめ直す貴重な時間にしてください。",
        "money": "目先の現金よりも、将来の富を約束する「文書運」が大吉です。不動産契約や資格取得、重要な決済などに利益があります。自己投資や書籍への支出は惜しまないでください。目上の人や両親から思いがけない援助を受ける可能性もあります。",
        "love": "愛に包まれる日です。パートナーに甘えたい気持ちが強まり、相手もあなたを大切に扱ってくれるでしょう。シングルなら、学識があり尊敬できる異性との出会いの予感。静かなカフェや図書館でのデートが二人の距離を縮めます。",
        "health": "体がだるく感じるのは「休め」というサインです。無理に運動せず、昼寝やマッサージで心身を解きほぐすのが最善の健康法です。消化機能が休止モードなので、暴飲暴食は避けてください。",
        "action": "1. 肯定の言葉：『私は愛されるに値する大切な存在だ』\n2. 幸운の行動：読書、瞑想、両親や恩師に連絡を入れる\n3. 注意事項：怠慢に注意（考えるだけで終わらないこと）。",
        "lucky": "📚 古典や専門書, ☕ 温かいお茶, 🛌 心地よい寝具"
    },
    "zh": {
        "score": 4, "star": "⭐⭐⭐⭐",
        "t": "📚 智慧与爱盈门：充实灵魂的治愈时刻",
        "d": "像在母亲怀抱中一样安稳舒适的一天。贵人运极佳，周围人会主动关怀并满足你的需求。比起外出的忙碌，今天更适合深造学习或复盘计划。不要执着于人生的“速度”，请利用这段时间确立正确的“方向”。",
        "money": "“文书运”大吉。虽然没有大笔现金流，但在房产合同、考证、审批等事务上会有长远获利。请大方地为知识和自我提升买单。此外，还可能收到长辈或父母的红包或资助。",
        "love": "是被爱包围的日子。伴侣会像对待王子/公主般细心呵护你。单身者易遇到谈吐不凡、学识渊博的对象。在书店或安静的茶室约会更能增进感情。",
        "health": "身体感到沉重乏力是休息的信号，而非生病。不要强迫自己剧烈运动，午睡或按摩是最好的良药。消化系统较弱，请避免油腻，饮食宜清淡。",
        "action": "1. 心灵咒语：“我是一个值得被无条件爱着的宝贵存在。”\n2. 开运行动：读书、冥想、给父母或老师打个问候电话\n3. 注意事项：警惕懒散（防止因思虑过多而错过行动时机）。",
        "lucky": "📚 经典著作, ☕ 热茶/草本茶, 🛌 舒适的床上用品"
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
                if st.button(t['btn_unlock'], type="primary", use_container_width=True):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_day"] = True
                        st.success("Master Unlocked!")
                        st.rerun()
                    else:
                        try:
                            # 1. 단품 키 확인 (3회 제한)
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={
                                                  "product_permalink": "specific_day", 
                                                  "license_key": k_in, 
                                                  "increment_uses_count": "true"
                                              }).json()
                            
                            if r.get("success"):
                                if r.get("uses", 0) > 3: # 🚨 3회 제한
                                    st.error("🚫 Usage limit exceeded (Max 3)")
                                else:
                                    st.session_state["unlocked_day"] = True
                                    st.rerun()
                            else:
                                # 2. 올패스 키 확인 (합산 10회 제한)
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={
                                                       "product_permalink": "all-access_pass", 
                                                       "license_key": k_in, 
                                                       "increment_uses_count": "true"
                                                   }).json()
                                
                                if r2.get("success"):
                                    if r2.get("uses", 0) > 10: # 🚨 10회 제한
                                        st.error("🚫 Usage limit exceeded (Max 10)")
                                    else:
                                        st.session_state["unlocked_day"] = True
                                        st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: 
                            st.error("Connection Error")
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
