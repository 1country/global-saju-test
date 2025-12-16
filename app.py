import streamlit as st
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="The Element: Global Destiny", page_icon="🌏", layout="wide")

# 스타일 (CSS)
st.markdown("""
<style>
    .main-title {font-size: 2.5em; color: #2C3E50; text-align: center; font-weight: bold; margin-bottom: 10px;}
    .sub-title {font-size: 1.2em; color: #7F8C8D; text-align: center; margin-bottom: 30px;}
    .result-box {background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;}
    .premium-box {background-color: #fff8e1; padding: 25px; border-radius: 15px; border: 2px solid #f1c40f; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 2. 다국어 UI 팩 (Top 12 Languages) ---
# 이곳에 언어를 계속 추가하면 됩니다.
ui_languages = {
    "English 🇺🇸": {
        "code": "en", "title": "The Element", "subtitle": "Discover Your True Self",
        "name": "Name", "date": "Birth Date", "time": "Birth Time (Optional)",
        "btn": "🔮 Analyze Energy", "tab1": "Basic Profile", "tab2": "2026 Forecast",
        "msg": "Hello", "born": "Born in"
    },
    "한국어 🇰🇷": {
        "code": "ko", "title": "디 엘리먼트", "subtitle": "나를 찾는 여행",
        "name": "이름", "date": "생년월일", "time": "태어난 시간 (선택)",
        "btn": "🔮 분석하기", "tab1": "기본 성격", "tab2": "2026년 운세",
        "msg": "반갑습니다", "born": "출생년도"
    },
    "中文 (Chinese) 🇨🇳": {
        "code": "cn", "title": "五行 (The Element)", "subtitle": "发现真实的自己",
        "name": "姓名", "date": "出生日期", "time": "出生时间 (可选)",
        "btn": "🔮 分析能量", "tab1": "基本性格", "tab2": "2026年 运势",
        "msg": "你好", "born": "出生年份"
    },
    "Español (Spanish) 🇪🇸": {
        "code": "es", "title": "El Elemento", "subtitle": "Descubre tu verdadero ser",
        "name": "Nombre", "date": "Fecha de nacimiento", "time": "Hora (Opcional)",
        "btn": "🔮 Analizar Energía", "tab1": "Perfil Básico", "tab2": "Pronóstico 2026",
        "msg": "Hola", "born": "Nacido en"
    },
    "Français (French) 🇫🇷": {
        "code": "fr", "title": "L'Élément", "subtitle": "Découvrez votre vrai moi",
        "name": "Nom", "date": "Date de naissance", "time": "Heure (Facultatif)",
        "btn": "🔮 Analyser", "tab1": "Profil de base", "tab2": "Prévisions 2026",
        "msg": "Bonjour", "born": "Né en"
    },
    "Deutsch (German) 🇩🇪": {
        "code": "de", "title": "Das Element", "subtitle": "Entdecke dein wahres Ich",
        "name": "Name", "date": "Geburtsdatum", "time": "Zeit (Optional)",
        "btn": "🔮 Analysieren", "tab1": "Basisprofil", "tab2": "Prognose 2026",
        "msg": "Hallo", "born": "Geboren in"
    },
    "日本語 (Japanese) 🇯🇵": {
        "code": "jp", "title": "エレメント", "subtitle": "本当の自分を発見する",
        "name": "名前", "date": "生年月日", "time": "出生時間 (任意)",
        "btn": "🔮 診断する", "tab1": "基本性格", "tab2": "2026年の運勢",
        "msg": "こんにちは", "born": "生まれ"
    },
    "Pусский (Russian) 🇷🇺": {
        "code": "ru", "title": "Элемент", "subtitle": "Открой свое истинное Я",
        "name": "Имя", "date": "Дата рождения", "time": "Время (Необязательно)",
        "btn": "🔮 Анализировать", "tab1": "Профиль", "tab2": "Прогноз 2026",
        "msg": "Привет", "born": "Год рождения"
    },
    "Português (Portuguese) 🇧🇷": {
        "code": "pt", "title": "O Elemento", "subtitle": "Descubra seu verdadeiro eu",
        "name": "Nome", "date": "Data de nascimento", "time": "Hora (Opcional)",
        "btn": "🔮 Analisar", "tab1": "Perfil Básico", "tab2": "Previsão 2026",
        "msg": "Olá", "born": "Nascido em"
    },
    "العربية (Arabic) 🇸🇦": {
        "code": "ar", "title": "العنصر", "subtitle": "اكتشف ذاتك الحقيقية",
        "name": "الاسم", "date": "تاريخ الميلاد", "time": "وقت الميلاد (اختياري)",
        "btn": "🔮 تحليل الطاقة", "tab1": "الملف الشخصي", "tab2": "توقعات 2026",
        "msg": "مرحباً", "born": "مواليد"
    },
    "Bahasa Indonesia 🇮🇩": {
        "code": "id", "title": "Elemen", "subtitle": "Temukan Jati Dirimu",
        "name": "Nama", "date": "Tanggal Lahir", "time": "Waktu (Opsional)",
        "btn": "🔮 Analisis", "tab1": "Profil Dasar", "tab2": "Ramalan 2026",
        "msg": "Halo", "born": "Lahir tahun"
    },
    "हिन्दी (Hindi) 🇮🇳": {
        "code": "hi", "title": "तत्व (The Element)", "subtitle": "अपनी सच्ची पहचान खोजें",
        "name": "नाम", "date": "जन्म तिथि", "time": "समय (वैकल्पिक)",
        "btn": "🔮 विश्लेषण करें", "tab1": "मूल प्रोफ़ाइल", "tab2": "2026 का पूर्वानुमान",
        "msg": "नमस्ते", "born": "जन्म वर्ष"
    }
}

# --- 3. 사이드바: 언어 선택 ---
with st.sidebar:
    st.header("Language 🌐")
    # 드롭다운 메뉴로 변경 (Selectbox)
    lang_choice = st.selectbox("Select your language", list(ui_languages.keys()))
    ui = ui_languages[lang_choice] # 선택된 언어팩 로드
    
    st.write("---")
    st.caption("Developed by The Element Lab")

# --- 4. 데이터 로직 (내용) ---
def get_content(year, lang_code):
    last_digit = int(str(year)[-1])
    
    # 한국어만 특별 처리, 나머지는 영어(Global)로 표시
    is_korean = (lang_code == "ko")
    
    # 영어 데이터 (기본값)
    en_data = {
        4: {"type": "Wood (Gap) 🌲", "arch": "The Pioneer", "desc": "Straight, honest, and upward-growing giant tree."}, 
        5: {"type": "Wood (Eul) 🌿", "arch": "The Survivor", "desc": "Flexible and resilient flower or vine."}, 
        6: {"type": "Fire (Byeong) ☀️", "arch": "The Visionary", "desc": "Passionate sun that shines on everyone."}, 
        7: {"type": "Fire (Jeong) 🔥", "arch": "The Mentor", "desc": "Warm candle light, sensitive and artistic."}, 
        8: {"type": "Earth (Mu) ⛰️", "arch": "The Guardian", "desc": "Huge mountain, trustworthy and steady."}, 
        9: {"type": "Earth (Gi) 🪴", "arch": "The Nurturer", "desc": "Fertile soil, practical and nurturing."}, 
        0: {"type": "Metal (Gyeong) ⚔️", "arch": "The Warrior", "desc": "Strong iron sword, decisive and loyal."}, 
        1: {"type": "Metal (Sin) 💎", "arch": "The Perfectionist", "desc": "Polished gem, sharp and delicate."}, 
        2: {"type": "Water (Im) 🌊", "arch": "The Strategist", "desc": "Vast ocean, wise and adaptable."}, 
        3: {"type": "Water (Gye) 🌧️", "arch": "The Thinker", "desc": "Gentle rain, intelligent and logical."}
    }
    
    # 한국어 데이터
    ko_data = {
        4: {"type": "큰 나무 (갑목) 🌲", "arch": "개척자", "desc": "하늘을 향해 곧게 뻗은 소나무입니다. 정직하고 리더십이 강합니다."},
        5: {"type": "꽃과 넝쿨 (을목) 🌿", "arch": "생존자", "desc": "유연하고 적응력이 뛰어난 꽃입니다. 끈기가 대단합니다."},
        6: {"type": "태양 (병화) ☀️", "arch": "비전가", "desc": "세상을 비추는 태양입니다. 열정적이고 숨김이 없습니다."},
        7: {"type": "촛불 (정화) 🔥", "arch": "멘토", "desc": "어둠을 밝히는 촛불입니다. 섬세하고 예술적인 감각이 있습니다."},
        8: {"type": "큰 산 (무토) ⛰️", "arch": "수호자", "desc": "믿음직한 거대한 산입니다. 신용을 중시하며 묵직합니다."},
        9: {"type": "비옥한 땅 (기토) 🪴", "arch": "양육자", "desc": "실속 있고 현실적인 텃밭입니다. 남을 잘 기르고 포용합니다."},
        0: {"type": "무쇠 칼 (경금) ⚔️", "arch": "전사", "desc": "단단한 원석이나 칼입니다. 결단력이 있고 의리가 강합니다."},
        1: {"type": "보석 (신금) 💎", "arch": "완벽주의자", "desc": "반짝이는 보석입니다. 예리하고 섬세하며 깔끔합니다."},
        2: {"type": "바다 (임수) 🌊", "arch": "전략가", "desc": "깊고 넓은 바다입니다. 지혜롭고 포용력이 큽니다."},
        3: {"type": "봄비 (계수) 🌧️", "arch": "사색가", "desc": "만물을 적시는 비입니다. 조용하지만 머리가 비상합니다."}
    }

    # 2026 운세 (한국어 vs 영어)
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

    if is_korean:
        return {"basic": ko_data[last_digit], "forecast": forecast_ko[my_group]}
    else:
        return {"basic": en_data[last_digit], "forecast": forecast_en[my_group]}


# --- 5. 화면 구성 (UI Rendering) ---
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
                <h1 style="color: #4A90E2; margin: 10px 0;">{content['basic']['type']}</h1>
                <p><b>Archetype:</b> {content['basic']['arch']}</p>
                <hr>
                <p style="font-size: 1.1em; line-height: 1.6;">{content['basic']['desc']}</p>
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
