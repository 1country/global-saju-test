import streamlit as st
from datetime import date, time
import time as tm
import os 
from utils import calculate_day_gan, get_interpretation 

# 1. 페이지 설정
st.set_page_config(page_title="The Element: Destiny Map", page_icon="🧭", layout="wide")

# ----------------------------------------------------------------
# ⭐ [핵심] 언어 설정 로직 (Session State 사용)
# ----------------------------------------------------------------
# 1. 처음 접속했다면(세션에 lang이 없으면) -> 서버 환경변수 or 기본값 'en' 사용
# 2. 언어를 바꾼 적이 있다면 -> 그 값을 유지
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')

lang = st.session_state['lang'] # 이제 이 변수가 전체 언어를 결정합니다.

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

        /* 전체 배경 스타일 - 진한 붉은색 */
        .stApp {
    background-image: 
        linear-gradient(rgba(127, 29, 29, 0.9), rgba(127, 29, 29, 0.9)),
        url("https://github.com/1country/global-saju-test/main/images/sign1.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #fefefe;
},
st.markdown("""
    <div style="text-align: center; margin-top: -20px; margin-bottom: 20px;">
        <img src="https://github.com/1country/global-saju-test/tree/main/images#:~:text=..-,Sign1.jpg,-Add%20files%20via.jpg" 
             alt="FutureNara.com"
             style="width: 250px; max-width: 80%; margin: auto;">
    </div>
""", unsafe_allow_html=True)


        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {
            background-color: #991b1b;  /* 진한 레드 */
            border-right: 1px solid #7f1d1d;
        }

        /* 사이드바 텍스트 색상 */
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #f8fafc !important;  /* 밝은 텍스트 */
        }

        /* 사이드바 메뉴 링크 */
        [data-testid="stSidebarNav"] span {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #fefefe !important;
            padding-top: 5px;
            padding-bottom: 5px;
        }

        /* 메인 타이틀 */
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

        /* 입력창 라벨 텍스트 */
        .stTextInput label p,
        .stDateInput label p,
        .stTimeInput label p,
        .stRadio label p,
        .stCheckbox label p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #fefefe !important;
        }

        /* 카드 스타일 */
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

        /* 버튼 스타일 */
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

        /* 링크 버튼 스타일 */
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

        /* 전체 텍스트 컬러 */
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
# 3. 사이드바 설정 (디자인 통일)
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <h1 style="color: gold; font-weight: 800; text-align: center; margin-bottom: 20px;">
            FutureNara.com
        </h1>
    """, unsafe_allow_html=True)

    st.header("Settings")
    
    # 현재 언어 표시
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Current Mode: **{lang_map.get(lang, 'English')}**")
    
    # ⭐ 6개 국어 변경 버튼
    st.write("Change Language:")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        if st.button("🇺🇸 EN", key="home_en"): st.session_state['lang'] = 'en'; st.rerun()
    with col_l2:
        if st.button("🇰🇷 KO", key="home_ko"): st.session_state['lang'] = 'ko'; st.rerun()
    with col_l3:
        if st.button("🇫🇷 FR", key="home_fr"): st.session_state['lang'] = 'fr'; st.rerun()
            
    col_l4, col_l5, col_l6 = st.columns(3)
    with col_l4:
        if st.button("🇪🇸 ES", key="home_es"): st.session_state['lang'] = 'es'; st.rerun()
    with col_l5:
        if st.button("🇯🇵 JA", key="home_ja"): st.session_state['lang'] = 'ja'; st.rerun()
    with col_l6:
        if st.button("🇨🇳 ZH", key="home_zh"): st.session_state['lang'] = 'zh'; st.rerun()
    
    st.markdown("---")
    
    # 커피 문구 번역
    coffee_msg_dict = {
        "ko": "운명의 코드를 응원해 주세요!", "en": "Support the developer!",
        "fr": "Soutenez le développeur !", "es": "¡Apoya al desarrollador!",
        "ja": "開発者を応援してください！", "zh": "支持开发者！"
    }
    coffee_text = coffee_msg_dict.get(lang, "Support the developer!")
    
    coffee_title = "☕ 개발자 응원하기" if lang == "ko" else "☕ Buy me a coffee"
    coffee_html = f"<span style='color: #cbd5e1; font-weight: bold;'>{coffee_text}</span>"
    
    st.header(coffee_title)
    st.markdown(f"""
        <div style="text-align: center;">
            <a href="https://buymeacoffee.com/5codes" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                    style="width: 180px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 5px;">
            </a>
            <p style="font-size: 14px; margin-top: 10px; color: #94a3b8;">{coffee_html}</p>
        </div>
    """, unsafe_allow_html=True)

# 4. 텍스트 데이터 (6개 국어)
txt = {
    "ko": {
        "title": "🧭 운명의 나침반", "sub": "당신의 태어난 순간이 말해주는 운명의 지도를 펼쳐보세요.", "input_h": "👤 사주 정보 입력 (필수)",
        "name": "이름", "birth": "생년월일", "gender": "성별", "time": "태어난 시간", "unknown": "시간 모름", "btn": "✨ 내 운명 확인하기 (Free)", "warn_name": "이름을 입력해주세요.",
        "res_hello": "반갑습니다,", "res_msg": "당신은 <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>의 기운을 타고났습니다.",
        "menu_h": "💎 프리미엄 운세 스토어", "btn_check": "확인하기 ($3)", "btn_buy": "구매하기 ($10)", "loading": "운명의 지도를 펼치는 중입니다...",
        "s1_t": "🔮 2026 신년 운세", "s1_d": "2026년의 재물, 연애, 직장운을 미리 봅니다.", "s2_t": "📅 그날의 운세", "s2_d": "면접, 데이트 등 중요한 날의 기운을 확인하세요.",
        "s3_t": "❤️ 사랑 궁합", "s3_d": "그 사람과 나는 천생연분일까?", "s4_t": "📆 택일 (좋은 날짜)", "s4_d": "결혼, 이사, 개업 최고의 날짜.", "s5_t": "🤝 비즈니스 궁합", "s5_d": "성공적인 파트너십을 위한 분석.", "s6_t": "👑 프리패스 (VIP)", "s6_d": "모든 유료 서비스를 한 번에 소장하세요!",
        "icon1_t": "Ancient Wisdom", "icon1_d": "동양의 깊은 명리학적 지혜", "icon2_t": "Modern Insight", "icon2_d": "AI 기술을 결합한 정밀 분석", "icon3_t": "Premium Keys", "icon3_d": "인생의 해답을 여는 마스터 키", "coffee_bottom": "이 서비스가 도움이 되셨나요? 따뜻한 커피 한 잔은 개발자에게 큰 힘이 됩니다! ☕"
    },
    "en": {
        "title": "🧭 The Element: Destiny Map", "sub": "Discover the map of destiny hidden in your birth moment.", "input_h": "👤 Enter Your Details",
        "name": "Name", "birth": "Date of Birth", "gender": "Gender", "time": "Birth Time", "unknown": "Unknown Time", "btn": "✨ Analyze My Destiny (Free)", "warn_name": "Please enter your name.",
        "res_hello": "Hello,", "res_msg": "You are born with the energy of <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>.",
        "menu_h": "💎 Premium Store", "btn_check": "Check ($3)", "btn_buy": "Buy Pass ($10)", "loading": "Unfolding your destiny map...",
        "s1_t": "🔮 2026 Forecast", "s1_d": "Prepare for 2026. Wealth, Love, and Career.", "s2_t": "📅 Specific Day Forecast", "s2_d": "Check your luck for any specific day.",
        "s3_t": "❤️ Love Compatibility", "s3_d": "Are we a match? Romantic chemistry analysis.", "s4_t": "📆 Date Selection", "s4_d": "Find the most auspicious dates.", "s5_t": "🤝 Business Compatibility", "s5_d": "Analyze professional synergy.", "s6_t": "👑 All-Access Pass", "s6_d": "Unlock EVERYTHING at once.",
        "icon1_t": "Ancient Wisdom", "icon1_d": "Deep Ancient Asian Wisdom", "icon2_t": "Modern Insight", "icon2_d": "Precise Analysis with AI", "icon3_t": "Premium Keys", "icon3_d": "Master Keys to Unlock Destiny", "coffee_bottom": "Did you enjoy the service? A coffee would be a great support! ☕"
    },
    "fr": {
        "title": "🧭 La Carte du Destin", "sub": "Découvrez la carte du destin cachée dans votre moment de naissance.", "input_h": "👤 Entrez vos détails",
        "name": "Nom", "birth": "Date de naissance", "gender": "Genre", "time": "Heure de naissance", "unknown": "Heure inconnue", "btn": "✨ Analyser mon destin (Gratuit)", "warn_name": "Veuillez entrer votre nom.",
        "res_hello": "Bonjour,", "res_msg": "Vous êtes né avec l'énergie de <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>.",
        "menu_h": "💎 Boutique Premium", "btn_check": "Vérifier (3$)", "btn_buy": "Acheter (10$)", "loading": "Déploiement de votre carte du destin...",
        "s1_t": "🔮 Prévisions 2026", "s1_d": "Préparez-vous pour 2026. Richesse, Amour, Carrière.", "s2_t": "📅 Prévisions Quotidiennes", "s2_d": "Vérifiez votre chance pour un jour précis.",
        "s3_t": "❤️ Compatibilité Amoureuse", "s3_d": "Sommes-nous compatibles ?", "s4_t": "📆 Sélection de Date", "s4_d": "Trouvez les dates les plus propices.", "s5_t": "🤝 Compatibilité Professionnelle", "s5_d": "Analysez la synergie professionnelle.", "s6_t": "👑 Pass Tout Accès", "s6_d": "Débloquez TOUT en une fois.",
        "icon1_t": "Sagesse Ancienne", "icon1_d": "Sagesse asiatique profonde", "icon2_t": "Vision Moderne", "icon2_d": "Analyse précise avec l'IA", "icon3_t": "Clés Premium", "icon3_d": "Clés maîtresses pour le destin", "coffee_bottom": "Vous avez aimé le service ? Un café serait un grand soutien ! ☕"
    },
    "es": {
        "title": "🧭 El Mapa del Destino", "sub": "Descubre el mapa del destino oculto en tu momento de nacimiento.", "input_h": "👤 Ingresa tus datos",
        "name": "Nombre", "birth": "Fecha de nacimiento", "gender": "Género", "time": "Hora de nacimiento", "unknown": "Hora desconocida", "btn": "✨ Analizar mi destino (Gratis)", "warn_name": "Por favor ingresa tu nombre.",
        "res_hello": "Hola,", "res_msg": "Naciste con la energía de <span style='color:#93c5fd; font-weight:bold;'>'{e_name}'</span>.",
        "menu_h": "💎 Tienda Premium", "btn_check": "Ver ($3)", "btn_buy": "Comprar ($10)", "loading": "Desplegando tu mapa del destino...",
        "s1_t": "🔮 Pronóstico 2026", "s1_d": "Prepárate para 2026. Riqueza, Amor, Carrera.", "s2_t": "📅 Pronóstico Diario", "s2_d": "Revisa tu suerte para cualquier día.",
        "s3_t": "❤️ Compatibilidad Amorosa", "s3_d": "¿Somos compatibles?", "s4_t": "📆 Selección de Fechas", "s4_d": "Encuentra las fechas más auspiciosas.", "s5_t": "🤝 Compatibilidad de Negocios", "s5_d": "Analiza la sinergia profesional.", "s6_t": "👑 Pase de Acceso Total", "s6_d": "Desbloquea TODO a la vez.",
        "icon1_t": "Sabiduría Antigua", "icon1_d": "Profunda sabiduría asiática", "icon2_t": "Visión Moderna", "icon2_d": "Análisis preciso con IA", "icon3_t": "Llaves Premium", "icon3_d": "Llaves maestras para el destino", "coffee_bottom": "¿Te gustó el servicio? ¡Un café sería un gran apoyo! ☕"
    },
    "ja": {
        "title": "🧭 運命の羅針盤", "sub": "生まれた瞬間に隠された運命の地図を広げましょう。", "input_h": "👤 情報を入力 (必須)",
        "name": "名前", "birth": "生年月日", "gender": "性別", "time": "出生時間", "unknown": "時間不明", "btn": "✨ 運命を分析する (無料)", "warn_name": "名前を入力してください。",
        "res_hello": "こんにちは、", "res_msg": "あなたは<span style='color:#93c5fd; font-weight:bold;'>「{e_name}」</span>のエネルギーを持って生まれました。",
        "menu_h": "💎 プレミアムストア", "btn_check": "確認 ($3)", "btn_buy": "購入 ($10)", "loading": "運命の地図を展開中...",
        "s1_t": "🔮 2026年の運勢", "s1_d": "2026年の財運、恋愛、仕事運を詳しく分析。", "s2_t": "📅 その日の運勢", "s2_d": "面接やデートなど、特定の日の運気をチェック。",
        "s3_t": "❤️ 恋愛相性", "s3_d": "あの人との相性は？ロマンチックな相性分析。", "s4_t": "📆 択日 (吉日選び)", "s4_d": "結婚、引っ越し、開業に最適な日を見つけます。", "s5_t": "🤝 ビジネス相性", "s5_d": "上司やパートナーとの仕事の相性を分析。", "s6_t": "👑 オールアクセスパス", "s6_d": "すべての有料サービスを一度にアンロック。",
        "icon1_t": "古代の叡智", "icon1_d": "東洋の深い命理学的知恵", "icon2_t": "現代の洞察", "icon2_d": "AI技術を組み合わせた精密分析", "icon3_t": "プレミアムキー", "icon3_d": "人生の答えを開くマスターキー", "coffee_bottom": "サービスは役に立ちましたか？コーヒー一杯の応援をお願いします！☕"
    },
    "zh": {
        "title": "🧭 命运指南针", "sub": "探索隐藏在出生时刻的命运地图。", "input_h": "👤 输入您的信息",
        "name": "姓名", "birth": "出生日期", "gender": "性别", "time": "出生时间", "unknown": "时间未知", "btn": "✨ 分析我的命运 (免费)", "warn_name": "请输入您的名字。",
        "res_hello": "你好，", "res_msg": "你生来就带有<span style='color:#93c5fd; font-weight:bold;'>“{e_name}”</span>的能量。",
        "menu_h": "💎 高级商店", "btn_check": "查看 ($3)", "btn_buy": "购买 ($10)", "loading": "正在展开命运地图...",
        "s1_t": "🔮 2026年运势", "s1_d": "为2026年做准备。财富、爱情、事业详细分析。", "s2_t": "📅 特定日运势", "s2_d": "查询面试、约会等特定日期的运势。",
        "s3_t": "❤️ 恋爱契合度", "s3_d": "我们合适吗？浪漫化学反应分析。", "s4_t": "📆 择吉日", "s4_d": "寻找结婚、搬家、开业的最佳吉日。", "s5_t": "🤝 商业契合度", "s5_d": "分析职业协同效应和团队合作。", "s6_t": "👑 全通票 (VIP)", "s6_d": "一次性解锁所有服务。",
        "icon1_t": "古老智慧", "icon1_d": "深奥的东方命理智慧", "icon2_t": "现代洞察", "icon2_d": "结合AI技术的精准分析", "icon3_t": "高级钥匙", "icon3_d": "开启命运答案的万能钥匙", "coffee_bottom": "喜欢这项服务吗？一杯咖啡将是巨大的支持！☕"
    }
}

if lang not in txt: lang = "en"
t = txt[lang]

# 깃허브 기본 주소
base_url = "https://raw.githubusercontent.com/1country/global-saju-test/main/images"

imgs = {
    "s1": f"{base_url}/s1.png", "s2": f"{base_url}/s2.png", "s3": f"{base_url}/s3.png", 
    "s4": f"{base_url}/s4.png", "s5": f"{base_url}/s5.png", "s6": f"{base_url}/s6.png" 
}

# 5. 메인 화면 구성
with st.container():
    col1, col2 = st.columns([1, 2.5]) 
    
    with col1:
        # ⭐ [수정] 이미지를 클릭하면 Gumroad 구매 링크로 이동하도록 변경 ⭐
        # (마우스를 올리면 살짝 커지는 애니메이션 효과 포함)
        gumroad_link = "https://5codes.gumroad.com/l/all-access_pass"
        
        st.markdown(f"""
            <a href="{gumroad_link}" target="_blank">
                <img src="{imgs['s6']}" 
                     style="width: 100%; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); 
                            transition: transform 0.3s ease-in-out; cursor: pointer;"
                     onmouseover="this.style.transform='scale(1.03)'" 
                     onmouseout="this.style.transform='scale(1)'">
            </a>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<div style='text-align: left; margin-top: 20px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='main-title' style='text-align: left;'>{t['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sub-desc' style='text-align: left; margin-bottom: 20px;'>{t['sub']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='display: flex; gap: 15px;'>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>✨ AI Based Analysis</span>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>📜 Asian Wisdom</span>
                <span style='background:rgba(255,255,255,0.1); padding:5px 10px; border-radius:15px; font-size:0.85em; color:#cbd5e1;'>🔒 Privacy Protected</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") 
st.write("") 

# 세션 초기화
if "user_name" not in st.session_state: st.session_state["user_name"] = ""
if "birth_date" not in st.session_state: st.session_state["birth_date"] = date(1990, 1, 1)
if "birth_time" not in st.session_state: st.session_state["birth_time"] = time(12, 00)
if "time_unknown" not in st.session_state: st.session_state["time_unknown"] = False
if "gender" not in st.session_state: st.session_state["gender"] = "Male"
if "analyzed" not in st.session_state: st.session_state["analyzed"] = False

# 입력창
st.markdown(f"### {t['input_h']}")
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input(t['name'], value=st.session_state["user_name"])
        g_opts = ["Male", "Female"]
        if lang == "ko": g_opts = ["남성", "여성"]
        elif lang == "fr": g_opts = ["Homme", "Femme"]
        elif lang == "es": g_opts = ["Hombre", "Mujer"]
        elif lang == "ja": g_opts = ["男性", "女性"]
        elif lang == "zh": g_opts = ["男性", "女性"]

        gender_val = st.radio(t['gender'], g_opts, horizontal=True)
        gender = "Male"
        if gender_val in ["여성", "Female", "Femme", "Mujer", "女性"]:
            gender = "Female"

    with c2:
        b_date = st.date_input(t['birth'], min_value=date(1920,1,1), value=st.session_state["birth_date"])
        tc1, tc2 = st.columns([2, 1])
        with tc2:
            st.write("")
            st.write("")
            is_unknown = st.checkbox(t['unknown'], value=st.session_state["time_unknown"])
        with tc1:
            b_time = st.time_input(t['time'], value=st.session_state["birth_time"], disabled=is_unknown)

    st.write("")
    if st.button(t['btn'], type="primary", use_container_width=True):
        if name:
            with st.spinner(t['loading']):
                tm.sleep(2.0) 
                
                st.session_state["user_name"] = name
                st.session_state["birth_date"] = b_date
                st.session_state["gender"] = gender
                st.session_state["time_unknown"] = is_unknown
                st.session_state["birth_time"] = None if is_unknown else b_time
                st.session_state["analyzed"] = True
                st.rerun()
        else:
            st.warning(t['warn_name'])

# [하단 아이콘 섹션]
if not st.session_state["analyzed"]:
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    icon_url_1 = f"{base_url}/icon1.png"
    icon_url_2 = f"{base_url}/icon2.png"
    icon_url_3 = f"{base_url}/icon3.png"
    
    icon_style = """
        width: 120px; height: 120px; object-fit: cover; border-radius: 50%; margin-bottom: 20px;
        -webkit-mask-image: radial-gradient(circle at center, black 30%, transparent 80%);
        mask-image: radial-gradient(circle at center, black 30%, transparent 80%);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); 
    """
    col_f1, col_f2, col_f3 = st.columns(3)
    text_style_h4 = "margin-top: 0; color: #f8fafc; font-size: 1.2em; font-weight: bold;"
    text_style_p = "color: #e2e8f0; font-size: 1.1em; line-height: 1.5;"

    with col_f1:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_1}" style="{icon_style}">
                <h4 style="{text_style_h4}">{t['icon1_t']}</h4>
                <p style="{text_style_p}">{t['icon1_d']}</p>
            </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_2}" style="{icon_style}">
                <h4 style="{text_style_h4}">{t['icon2_t']}</h4>
                <p style="{text_style_p}">{t['icon2_d']}</p>
            </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{icon_url_3}" style="{icon_style}">
                <h4 style="{text_style_h4}">{t['icon3_t']}</h4>
                <p style="{text_style_p}">{t['icon3_d']}</p>
            </div>
        """, unsafe_allow_html=True)

# --- 도우미 함수 (수정됨) ---
def draw_premium_card(title, desc, btn_text, img_url, click_page=None, link_url=None):
    with st.container(border=True):
        col_img, col_text, col_btn = st.columns([1.2, 3.3, 1.5], gap="medium")
        with col_img:
            st.write("") 
            st.markdown(f"""<img src="{img_url}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">""", unsafe_allow_html=True)
        with col_text:
            st.subheader(title)
            st.write(desc)
        with col_btn:
            st.write("") 
            st.write("") 
            # ⭐ [중요] 버튼 로직을 단순하고 명확하게 변경
            if link_url:
                # 외부 링크 (새 탭)
                st.link_button(btn_text, link_url, type="primary", use_container_width=True)
            elif click_page:
                # 내부 페이지 이동 (st.switch_page는 반드시 전체 경로를 포함해야 함)
                if st.button(btn_text, key=f"btn_{title}", use_container_width=True):
                    try:
                        st.switch_page(click_page)
                    except Exception as e:
                        st.error(f"Page not found: {click_page}")

# 6. 결과 및 프리미엄 스토어
if st.session_state["analyzed"]:
    st.divider()
    day_info = calculate_day_gan(st.session_state["birth_date"])
    
    description = day_info.get('desc_' + lang, day_info.get('desc_en', ''))
    if lang == 'ko': description = day_info['desc']
    
    detail_text = get_interpretation(day_info['element'], lang)
    element_name = day_info.get(lang, day_info['en'])

    st.markdown(f"""
    <div class='card'>
        <h3 style='color:#cbd5e1; margin:0;'>{t['res_hello']} <b>{st.session_state['user_name']}</b>!</h3>
        <p style='font-size:1.6em; margin-top:15px; color:#f8fafc; line-height: 1.6;'>
            {t['res_msg'].format(e_name=element_name)}
        </p>
        <p style='font-size:1em; color:#94a3b8; margin-top:5px;'>({description})</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(detail_text) 
        
    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader(t['menu_h'])

    # VIP 패스 (링크 연결)
    draw_premium_card(t['s6_t'], t['s6_d'], t['btn_buy'], imgs['s6'], link_url="https://5codes.gumroad.com/l/all-access_pass")
    
    # 1. 2026 운세 (페이지 이동)
    draw_premium_card(t['s1_t'], t['s1_d'], t['btn_check'], imgs['s1'], click_page="pages/1_2026_Forecast.py")
    
    # ⭐ 2. 그날의 운세 [수정됨] : 파일명 뒤에 _Forecast가 붙어야 에러가 안 납니다!
    draw_premium_card(t['s2_t'], t['s2_d'], t['btn_check'], imgs['s2'], click_page="pages/2_Specific_Day_Forecast.py")
    
    # ⭐ 3. 사랑 궁합 [수정됨] : 파일명 정확히 매칭
    draw_premium_card(t['s3_t'], t['s3_d'], t['btn_check'], imgs['s3'], click_page="pages/3_Love_Compatibility.py")
    draw_premium_card(t['s4_t'], t['s4_d'], t['btn_check'], imgs['s4'], click_page="pages/4_Date_Selection.py")
    draw_premium_card(t['s5_t'], t['s5_d'], t['btn_check'], imgs['s5'], click_page="pages/5_Business_Compatibility.py")

    st.divider()
    
    st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: rgba(30, 41, 59, 0.8); border-radius: 15px; margin-top: 20px; border: 1px solid #475569;">
            <p style="font-size: 1.1em; color: #cbd5e1; margin-bottom: 20px; font-weight: bold; font-family: 'Gowun Batang', serif;">
                {t['coffee_bottom']}
            </p>
            <a href="https://buymeacoffee.com/5codes" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                    style="width: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 5px; transition: transform 0.2s;">
            </a>
        </div>
    """, unsafe_allow_html=True)
