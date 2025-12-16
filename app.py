import streamlit as st
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Global Destiny", page_icon="🌏", layout="wide")

# 스타일 (CSS) - 폰트 및 여백 조정
st.markdown("""
<style>
    .main-title {font-size: 2.5em; color: #2C3E50; text-align: center; font-weight: bold; margin-bottom: 5px;}
    .sub-title {font-size: 1.1em; color: #7F8C8D; text-align: center; margin-bottom: 30px;}
    .result-box {background-color: #ffffff; padding: 30px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-top: 20px;}
    .premium-box {background-color: #fff8e1; padding: 25px; border-radius: 15px; border: 2px solid #f1c40f; margin-top: 20px;}
    .desc-text {font-size: 1.05em; line-height: 1.8; color: #444; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# --- 2. 다국어 UI 팩 ---
ui_languages = {
    "English 🇺🇸": {
        "code": "en", "title": "The Element: Discover Your True Self", "subtitle": "Ancient Asian Wisdom Decoded for the Modern Soul",
        "name": "Name", "date": "Birth Date", "time": "Birth Time (Optional)",
        "btn": "🔮 Analyze My Energy", "tab1": "Basic Profile", "tab2": "2026 Forecast",
        "msg": "Hello", "born": "Born in"
    },
    "한국어 🇰🇷": {
        "code": "ko", "title": "디 엘리먼트: 진정한 나를 찾는 여행", "subtitle": "현대인을 위한 고대 동양 철학의 지혜",
        "name": "이름", "date": "생년월일", "time": "태어난 시간 (선택)",
        "btn": "🔮 나의 에너지 분석하기", "tab1": "기본 성격", "tab2": "2026년 운세",
        "msg": "반갑습니다", "born": "출생년도"
    },
    "中文 (Chinese) 🇨🇳": { "code": "cn", "title": "The Element: 发现真实的自己", "subtitle": "Ancient Wisdom Decoded", "name": "姓名", "date": "出生日期", "time": "时间", "btn": "🔮 分析", "tab1": "基本性格", "tab2": "2026年 运势", "msg": "你好", "born": "年份" },
    "Español (Spanish) 🇪🇸": { "code": "es", "title": "The Element: Descubre tu verdadero ser", "subtitle": "Sabiduría antigua para el alma moderna", "name": "Nombre", "date": "Fecha", "time": "Hora", "btn": "🔮 Analizar", "tab1": "Perfil", "tab2": "Pronóstico 2026", "msg": "Hola", "born": "Nacido en" },
    "Français (French) 🇫🇷": { "code": "fr", "title": "The Element: Découvrez votre vrai moi", "subtitle": "Sagesse ancienne décodée", "name": "Nom", "date": "Date", "time": "Heure", "btn": "🔮 Analyser", "tab1": "Profil", "tab2": "Prévisions 2026", "msg": "Bonjour", "born": "Né en" },
    "Deutsch (German) 🇩🇪": { "code": "de", "title": "The Element: Entdecke dein wahres Ich", "subtitle": "Alte Weisheit entschlüsselt", "name": "Name", "date": "Datum", "time": "Zeit", "btn": "🔮 Analysieren", "tab1": "Profil", "tab2": "Prognose 2026", "msg": "Hallo", "born": "Geboren in" },
    "日本語 (Japanese) 🇯🇵": { "code": "jp", "title": "The Element: 本当の自分を発見する", "subtitle": "現代人のための古代の知恵", "name": "名前", "date": "生年月日", "time": "時間", "btn": "🔮 診断する", "tab1": "基本性格", "tab2": "2026年の運勢", "msg": "こんにちは", "born": "生まれ" },
    "Pусский (Russian) 🇷🇺": { "code": "ru", "title": "The Element: Открой свое истинное Я", "subtitle": "Древняя мудрость для современной души", "name": "Имя", "date": "Дата", "time": "Время", "btn": "🔮 Анализировать", "tab1": "Профиль", "tab2": "Прогноз 2026", "msg": "Привет", "born": "Год" },
    "Português (Portuguese) 🇧🇷": { "code": "pt", "title": "The Element: Descubra seu verdadeiro eu", "subtitle": "Sabedoria antiga decodificada", "name": "Nome", "date": "Data", "time": "Hora", "btn": "🔮 Analisar", "tab1": "Perfil", "tab2": "Previsão 2026", "msg": "Olá", "born": "Nascido em" },
    "العربية (Arabic) 🇸🇦": { "code": "ar", "title": "The Element: اكتشف ذاتك الحقيقية", "subtitle": "الحكمة القديمة", "name": "الاسم", "date": "تاريخ الميلاد", "time": "الوقت", "btn": "🔮 تحليل", "tab1": "الملف الشخصي", "tab2": "توقعات 2026", "msg": "مرحباً", "born": "مواليد" },
    "Bahasa Indonesia 🇮🇩": { "code": "id", "title": "The Element: Temukan Jati Dirimu", "subtitle": "Kebijaksanaan Kuno", "name": "Nama", "date": "Tanggal", "time": "Waktu", "btn": "🔮 Analisis", "tab1": "Profil", "tab2": "Ramalan 2026", "msg": "Halo", "born": "Lahir" },
    "हिन्दी (Hindi) 🇮🇳": { "code": "hi", "title": "The Element: अपनी सच्ची पहचान खोजें", "subtitle": "प्राचीन ज्ञान", "name": "नाम", "date": "तिथि", "time": "समय", "btn": "🔮 विश्लेषण", "tab1": "प्रोफ़ाइल", "tab2": "2026 राशिफल", "msg": "नमस्ते", "born": "वर्ष" }
}

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("Language 🌐")
    lang_choice = st.selectbox("Select Language", list(ui_languages.keys()))
    ui = ui_languages[lang_choice]
    st.write("---")
    st.info("💡 Tip: Try entering the birth year of your friends or family.")

# --- 4. 데이터 로직 (3문단 상세 풀이) ---
def get_content(year, lang_code):
    last_digit = int(str(year)[-1])
    is_korean = (lang_code == "ko")
    
    # [영어] 상세 데이터 (3문단)
    en_data = {
        4: {"type": "Wood (Gap) 🌲", "arch": "The Pioneer", 
            "desc": """You possess the energy of a giant pine tree stretching straight towards the sky. You are honest, benevolent, and have a strong drive for growth. Once you set a goal, you move forward without looking back. Your leadership is natural, and people rely on your unwavering strength.
            
            In work and relationships, you prefer to lead rather than follow. You might seem rigid at times, but that is simply because you have strong principles. You are not the type to use tricks or manipulation; you win by being better and stronger.
            
            **Advice:** Because you are so straight, you can sometimes break if you refuse to bend. Learning a little flexibility will make you truly unstoppable."""},
            
        5: {"type": "Wood (Eul) 🌿", "arch": "The Survivor", 
            "desc": """You are like a resilient vine or a beautiful flower that blooms even in harsh conditions. Unlike the rigid tree, you are incredibly flexible and adaptable. You know how to survive anywhere, using your social skills and networking abilities to climb higher.
            
            People might underestimate you because you look gentle on the outside, but you have a hidden tenacity that is scary. You are a realist who values substance over appearance. You are good at managing people and situations to your advantage.
            
            **Advice:** You sometimes rely too much on others or the environment. Trust in your own independent strength a bit more."""},
            
        6: {"type": "Fire (Byeong) ☀️", "arch": "The Visionary", 
            "desc": """You are the burning sun in the midday sky. You are passionate, open-hearted, and full of explosive energy. You cannot hide your emotions; everything shows on your face. You love being the center of attention and have a natural charisma that draws people in.
            
            You are fair and dislike secrets. You are quick to get angry but also quick to forgive, holding no grudges. You are a visionary who sees the big picture rather than the small details.
            
            **Advice:** You start things with great passion but sometimes struggle to finish them. Consistency is the only key missing from your success."""},
            
        7: {"type": "Fire (Jeong) 🔥", "arch": "The Mentor", 
            "desc": """You are like a candle flame, a lighthouse, or starlight. Unlike the sun, your fire is focused, delicate, and intense. You are sensitive and have a warm heart that cares deeply for others. You often sacrifice yourself to guide people in the dark.
            
            You have incredible intuition and artistic talent. You notice things that others miss. While you appear calm, you have a very strong inner will and can be quite sharp when provoked.
            
            **Advice:** You can be overly sensitive and get hurt easily by small words. Protect your emotional energy and don't take everything personally."""},
            
        8: {"type": "Earth (Mu) ⛰️", "arch": "The Guardian", 
            "desc": """You stand tall like a majestic, heavy mountain range. You are trustworthy, steady, and stubborn. You do not move easily, but once you make a decision, your persistence is overwhelming. People naturally trust you with their secrets and money.
            
            You have a huge scale of thinking. You are not interested in petty tricks. However, you can be slow to express your feelings, which might frustrate others. You are a pillar of support for your family and organization.
            
            **Advice:** Your strength is stability, but your weakness is lack of adaptability. Be open to new changes and try to express your feelings more often."""},
            
        9: {"type": "Earth (Gi) 🪴", "arch": "The Nurturer", 
            "desc": """You are the fertile soil of a garden. You are practical, nurturing, and multifaceted. Unlike the mountain, you are productive and can grow anything. You are very realistic and have a talent for education and nurturing others' talents.
            
            You are adaptable and know how to fit into any group. You are smart with numbers and assets. You may look soft, but you have a very clear calculation of what is beneficial and what is not.
            
            **Advice:** You can sometimes be too calculating or worry too much. Sometimes, just trusting your gut feeling is better than over-analyzing."""},
            
        0: {"type": "Metal (Gyeong) ⚔️", "arch": "The Warrior", 
            "desc": """You are like raw iron or a powerful sword. You value loyalty, justice, and friendship above all else. You are decisive and have strong executive power. You hate ambiguity—for you, it's either yes or no, friend or foe.
            
            You are a reformer who wants to change the world. You are not afraid of conflict if it is for a just cause. Your blunt honesty can sometimes hurt others, but your intentions are pure.
            
            **Advice:** You are very strong, but sometimes too rigid. Learning to soften your speech and approach will gain you more allies."""},
            
        1: {"type": "Metal (Sin) 💎", "arch": "The Perfectionist", 
            "desc": """You are a polished gemstone or a sharp needle. You shine brightly and have a delicate aesthetic sense. You aim for perfection in everything you do. You are sharp, sensitive, and have high standards for yourself and others.
            
            You value your dignity and self-respect. You are very precise and logical. Because you are like a jewel, you want to be treated with care and respect. You can be critical, but your analysis is usually correct.
            
            **Advice:** You can be too sharp and cold. Try to embrace the imperfections in yourself and others. Warmth will make you shine even brighter."""},
            
        2: {"type": "Water (Im) 🌊", "arch": "The Strategist", 
            "desc": """You are the vast, deep ocean. You are incredibly wise, adaptable, and have a big heart. Like the ocean, your depth is hard to measure. You flow around obstacles rather than fighting them, but your power can be overwhelming when unleashed.
            
            You are a natural strategist with a lot of ideas. You can be very social, but you also have a secret side that you don't show to anyone. You have a great capacity to absorb knowledge and wealth.
            
            **Advice:** You think too much and sometimes fall into laziness. Action is the only way to manifest your brilliant ideas into reality."""},
            
        3: {"type": "Water (Gye) 🌧️", "arch": "The Thinker", 
            "desc": """You are the gentle spring rain or morning dew. You are quiet, intelligent, and very logical. You prefer planning behind the scenes rather than standing in front. You are sensitive to others' feelings and have a kind, introverted nature.
            
            You are very creative and have a unique way of seeing the world. You can change your shape to fit any container. You are not loud, but your influence slowly soaks into everything around you.
            
            **Advice:** You can be prone to mood swings or negative thinking. Surround yourself with warm, positive people (Fire energy) to balance your nature."""}
    }
    
    # [한국어] 상세 데이터 (3문단)
    ko_data = {
        4: {"type": "큰 나무 (갑목) 🌲", "arch": "개척자", 
            "desc": """당신은 하늘을 향해 곧게 뻗어 올라가는 거대한 소나무의 기운을 타고났습니다. 성격이 대쪽 같고 솔직하며, 성장하고자 하는 욕구가 매우 강합니다. 한번 목표를 정하면 뒤를 돌아보지 않고 앞으로 나아가는 추진력이 있습니다.
            
            남의 밑에 있기보다는 우두머리가 되기를 좋아합니다. 굽히기를 싫어해서 자존심이 세다는 말을 듣기도 하지만, 그만큼 책임감이 강하고 의지할 수 있는 리더입니다. 편법을 쓰기보다는 정면승부를 선호합니다.
            
            **조언:** 너무 강하면 부러질 수 있습니다. 가끔은 주변의 의견을 수용하고 굽힐 줄 아는 유연함을 갖춘다면 당신은 누구도 막을 수 없는 거목이 될 것입니다."""},
            
        5: {"type": "꽃과 넝쿨 (을목) 🌿", "arch": "생존자", 
            "desc": """당신은 척박한 환경에서도 꽃을 피워내는 끈질긴 생명력을 지녔습니다. 거목(갑목)처럼 뻣뻣하지 않고, 바람이 불면 흔들리는 유연함과 적응력을 가지고 있습니다. 어떤 환경에 던져져도 살아남는 생활력 강한 실속파입니다.
            
            겉모습은 부드럽고 여려 보일 수 있지만, 내면에는 무서운 고집과 인내심이 숨어 있습니다. 사람들과 어울리는 능력이 탁월하며, 인맥을 통해 자신을 성장시키는 지혜를 가지고 있습니다.
            
            **조언:** 때로는 혼자서 해결하기보다 주변 환경이나 타인에게 너무 의지하려는 경향이 있을 수 있습니다. 자신의 독립적인 힘을 믿으세요."""},
            
        6: {"type": "태양 (병화) ☀️", "arch": "비전가", 
            "desc": """당신은 세상을 환하게 비추는 태양입니다. 매사에 열정적이고 공명정대하며, 에너지가 넘쳐흐릅니다. 자신의 감정을 숨기지 못하고 얼굴에 다 드러나는 투명한 사람입니다. 언제나 주목받기를 좋아하고, 실제로 어디서든 주인공 역할을 합니다.
            
            뒤끝이 없고 시원시원한 성격이라 사람들이 많이 따릅니다. 작은 디테일보다는 큰 그림을 보는 비전가 스타일입니다. 예의를 중시하고 불의를 보면 참지 못하는 정의감도 있습니다.
            
            **조언:** 시작은 화려하고 열정적이지만, 끈기가 부족해 마무리가 약할 수 있습니다. 꾸준함만 갖춘다면 당신은 큰 성공을 거둘 수 있습니다."""},
            
        7: {"type": "촛불 (정화) 🔥", "arch": "멘토", 
            "desc": """당신은 어둠을 밝히는 은은한 촛불이나 별빛과 같습니다. 태양처럼 강렬하지는 않지만, 집중력이 뛰어나고 섬세하며 따뜻한 온기를 지녔습니다. 타인을 위해 자신을 태워 희생하고 봉사하는 정신이 강해 '멘토'의 자질이 있습니다.
            
            예술적인 감각과 직관력이 매우 발달해 있습니다. 겉으로는 조용하고 차분해 보이지만, 속으로는 폭발적인 열정과 예리함을 감추고 있습니다. 한 번 화가 나면 걷잡을 수 없이 무서운 면도 있습니다.
            
            **조언:** 감수성이 풍부하여 사소한 말에도 쉽게 상처받을 수 있습니다. 타인의 감정에 너무 휩쓸리지 말고 자신의 멘탈을 지키는 연습이 필요합니다."""},
            
        8: {"type": "큰 산 (무토) ⛰️", "arch": "수호자", 
            "desc": """당신은 웅장하고 묵직한 산맥과 같습니다. 가볍게 움직이지 않으며, 믿음과 신용을 목숨처럼 중요하게 생각합니다. 포용력이 넓어 많은 사람들이 당신에게 의지하려 합니다. 한번 마음먹은 일은 끝까지 밀고 나가는 뚝심이 있습니다.
            
            자신의 속마음을 잘 드러내지 않아 무슨 생각을 하는지 알기 어렵다는 말을 듣기도 합니다. 중간자적 입장에서 중재하는 능력이 탁월하며, 묵묵히 자신의 자리를 지키는 기둥 같은 존재입니다.
            
            **조언:** 지나치게 신중하여 기회를 놓칠 수 있습니다. 때로는 과감한 변화와 표현이 필요합니다. 고집을 조금만 내려놓으세요."""},
            
        9: {"type": "비옥한 땅 (기토) 🪴", "arch": "양육자", 
            "desc": """당신은 만물을 길러내는 정원의 비옥한 흙입니다. 거대한 산(무토)보다는 규모가 작지만, 훨씬 실속 있고 현실적입니다. 무엇이 이득이고 손해인지 빠르게 파악하며, 다재다능하여 어떤 환경에서도 자신의 몫을 챙깁니다.
            
            어머니와 같은 자애로움으로 타인을 교육하고 기르는 데 소질이 있습니다. 적응력이 뛰어나고 모나지 않게 처세합니다. 겉으로는 부드러워 보이지만 속은 아주 야무진 외유내강형입니다.
            
            **조언:** 생각이 너무 많아 의심이 많아지거나 걱정을 사서 할 수 있습니다. 너무 계산하기보다는 때로는 단순하게 믿고 행동하는 것이 도움이 됩니다."""},
            
        0: {"type": "무쇠 칼 (경금) ⚔️", "arch": "전사", 
            "desc": """당신은 제련되지 않은 원석이나 강력한 무쇠 칼입니다. 의리와 정의를 가장 중요하게 생각합니다. 결단력이 빠르고 실행력이 강해, 한번 결정하면 뒤를 돌아보지 않고 밀어붙입니다. 흐지부지한 것을 싫어하고 맺고 끊음이 확실합니다.
            
            세상을 바꾸고자 하는 개혁가적인 기질이 있습니다. 투박하지만 거짓이 없고 순수합니다. 아군에게는 든든한 방패가 되지만, 적에게는 무자비한 칼이 됩니다.
            
            **조언:** 지나친 강함은 부러지거나 타인에게 상처를 줄 수 있습니다. 말과 행동을 조금 더 부드럽게 다듬는다면 더 많은 사람들이 당신을 따를 것입니다."""},
            
        1: {"type": "보석 (신금) 💎", "arch": "완벽주의자", 
            "desc": """당신은 이미 예리하게 세공된 보석이나 날카로운 칼날입니다. 반짝이는 외모나 센스 있는 감각을 가진 경우가 많습니다. 자존심이 매우 강하고, 자신이 보석처럼 대우받기를 원합니다. 매사에 깔끔하고 정확하며 완벽을 추구합니다.
            
            예민하고 섬세하여 남들이 보지 못하는 것까지 캐치해냅니다. 냉철한 비판 능력이 있어 말 한마디로 핵심을 찌릅니다. 고고하고 품위 있는 삶을 지향합니다.
            
            **조언:** 너무 예민하고 날카로워 주변 사람들을 긴장시킬 수 있습니다. 조금 더 너그러운 마음을 갖고, 자신의 결점까지도 사랑하는 법을 배워보세요."""},
            
        2: {"type": "바다 (임수) 🌊", "arch": "전략가", 
            "desc": """당신은 끝을 알 수 없는 깊고 넓은 바다입니다. 지혜가 뛰어나고 임기응변에 능하며, 어떤 그릇에도 담길 수 있는 유연함을 가졌습니다. 포용력이 커서 많은 것을 받아들이지만, 그 속을 알기는 어렵습니다.
            
            스케일이 크고 흐름을 읽는 눈이 탁월해 전략가나 기획자가 많습니다. 평소에는 잔잔하지만 화가 나면 쓰나미처럼 모든 것을 쓸어버리는 무서운 폭발력도 가지고 있습니다.
            
            **조언:** 생각이 너무 많아 실행하지 않고 머릿속으로만 계획하다 끝날 수 있습니다. 또한 비밀이 너무 많으면 고립될 수 있으니 마음을 표현하세요."""},
            
        3: {"type": "봄비 (계수) 🌧️", "arch": "사색가", 
            "desc": """당신은 대지를 촉촉하게 적시는 봄비나 옹달샘입니다. 조용하고 차분하며, 지능이 높고 논리적입니다. 앞에 나서기보다는 뒤에서 조용히 상황을 컨트롤하는 참모 역할을 선호합니다. 감수성이 풍부하고 타인의 감정을 잘 읽어냅니다.
            
            작은 물줄기처럼 어디든 스며들어 환경을 변화시킵니다. 끈기가 있고 치밀하여 계획을 세우는 데 능합니다. 겉으로는 약해 보이지만 끈질긴 면이 있습니다.
            
            **조언:** 생각이 꼬리에 꼬리를 물어 부정적인 생각에 빠지기 쉽습니다. 밝고 긍정적인 에너지(화의 기운)를 가진 사람들과 어울려 균형을 맞추는 것이 좋습니다."""}
    }

    # 2026 운세 
    forecast_en = {
        "Wood": "🔥 Very Busy & Passionate Year (Output)",
        "Fire": "🤝 Competition & Partnership (Same Energy)",
        "Earth": "📜 Support & Documents (Best Luck)",
        "Metal": "🔨 Pressure & Transformation (Power)",
        "Water": "💰 Wealth Opportunities (Money)"
    }
    forecast_ko = {
        "Wood": "🔥 매우 바쁘고 열정적인 한 해 (식상운)",
        "Fire": "🤝 경쟁자와 협력자가 동시에 나타남 (비겁운)",
        "Earth": "📜 문서운과 귀인의 도움 (인성운 - 최고)",
        "Metal": "🔨 압박감 속에서 성장하는 시기 (관성운)",
        "Water": "💰 재물운이 따르지만 관리가 필요 (재성운)"
    }

    groups = ["Metal", "Metal", "Water", "Water", "Wood", "Wood", "Fire", "Fire", "Earth", "Earth"]
    my_group = groups[last_digit]

    # 영어/한국어 외의 언어는 영어를 기본으로 보여줍니다.
    if is_korean:
        return {"basic": ko_data[last_digit], "forecast": forecast_ko[my_group]}
    else:
        return {"basic": en_data[last_digit], "forecast": forecast_en[my_group]}

# --- 5. UI 구성 ---
st.markdown(f"<h1 class='main-title'>{ui['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-title'>{ui['subtitle']}</p>", unsafe_allow_html=True)

st.write("---")

col1, col2, col3 = st.columns([1.2, 1, 1]) 
with col1:
    name = st.text_input(ui['name'])
with col2:
    birth_date = st.date_input(ui['date'], min_value=datetime(1920, 1, 1), value=datetime(1990, 1, 1))
with col3:
    birth_time = st.time_input(ui['time'], value=None)

# 탭 생성
tab1, tab2 = st.tabs([ui['tab1'], ui['tab2']])

if st.button(ui['btn'], use_container_width=True):
    if name:
        year = birth_date.year
        content = get_content(year, ui['code'])
        time_str = birth_time.strftime("%H:%M") if birth_time else ""

        # [탭 1] 무료 결과
        with tab1:
            st.markdown(f"""
            <div class="result-box">
                <h3 style="color: #555;">{ui['msg']}, {name}.</h3>
                <p>{ui['born']}: <b>{year}</b> {time_str}</p>
                <h1 style="color: #4A90E2; margin: 15px 0;">{content['basic']['type']}</h1>
                <p style="font-size: 1.2em;"><b>Archetype:</b> {content['basic']['arch']}</p>
                <hr style="border-top: 1px solid #eee; margin: 20px 0;">
                <div class="desc-text">
                    {content['basic']['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # [탭 2] 유료 결과 (데모)
        with tab2:
            st.markdown(f"""
            <div class="premium-box">
                <h3 style="color: #d35400;">👑 Premium 2026</h3>
                <div style="background: white; padding: 15px; border-radius: 10px; margin-top: 10px;">
                    <h2 style="text-align: center; margin: 0;">{content['forecast']}</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"Please enter your {ui['name']}")

st.write("---")
st.caption("© 2025 The Element Lab (Global)")
