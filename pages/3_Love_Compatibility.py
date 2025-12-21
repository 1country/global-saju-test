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

    # 🌟 6개 국어 상세 데이터베이스 (영어 부분에 변수 적용)
    reports = {
        "Same": { 
            "score": 85,
            "ko": {
                "t": "🤝 거울 속의 연인: 운명적 동질감",
                "c": "마치 잃어버린 반쪽을 찾은 듯 대화 코드와 웃음 포인트가 똑같습니다. 가장 친한 친구이자 뜨거운 연인이 될 수 있는 완벽한 파트너입니다.",
                "f": "하지만 둘 다 고집이 세서 한 번 싸우면 '네가 먼저 사과해'라며 냉전을 벌일 수 있습니다. 서로의 단점이 거울처럼 보여 짜증이 날 수도 있습니다.",
                "i": "속궁합 90점. 친구처럼 장난치듯 시작해 열정적으로 변합니다. 서로 무엇을 원하는지 말하지 않아도 알 수 있습니다.",
                "a": "자존심을 죽이고 먼저 사과하세요. 이기려 들면 상처만 남습니다."
            },
            "en": {
                "t": "🤝 Mirror Couple: Twin Souls",
                "c": f"You feel an instant connection like finding a lost twin. You share the same humor and values. Best friends and passionate lovers.",
                "f": f"Both have strong egos. Arguments can turn into cold wars because neither wants to apologize first. You might dislike seeing your own flaws in {O}.",
                "i": "Intimacy Score: 90. Starts playful, ends passionate. You intuitively know each other's needs.",
                "a": "Drop the ego. Apologize first. Winning an argument only hurts the relationship."
            },
            "fr": {"t": "🤝 Couple Miroir", "c": "Âmes sœurs avec le même humour.", "f": "Conflits d'ego possibles.", "i": "Intimité : 90/100.", "a": "Mettez votre ego de côté."},
            "es": {"t": "🤝 Pareja Espejo", "c": "Almas gemelas con el mismo humor.", "f": "Posibles conflictos de ego.", "i": "Intimidad: 90/100.", "a": "Deja el ego a un lado."},
            "ja": {"t": "🤝 鏡のような恋人", "c": "双子のような魂。親友であり恋人。", "f": "自我のぶつかり合いに注意。", "i": "相性90点。阿吽の呼吸。", "a": "プライドを捨てて先に謝りましょう。"},
            "zh": {"t": "🤝 镜中恋人", "c": "灵魂伴侣，既是挚友又是恋人。", "f": "注意自尊心的冲突。", "i": "亲密度90分。", "a": "放下自尊，先道歉。"}
        },
        "Output": { 
            "score": 92,
            "ko": {
                "t": "💖 헌신적인 사랑: 아낌없이 주는 나무",
                "c": "당신이 상대방을 자식처럼 예뻐하고 챙겨주는 관계입니다. 상대방은 당신의 사랑 속에서 안정감을 느끼고 전적으로 의지합니다.",
                "f": "'내가 이만큼 해줬는데 넌 왜 안 해줘?'라는 보상 심리가 생기면 서운함이 폭발합니다. 과도한 관심은 잔소리로 느껴질 수 있습니다.",
                "i": "당신이 리드하고 봉사하는 형태입니다. 상대방의 만족을 위해 최선을 다하며 거기서 기쁨을 느낍니다.",
                "a": "바라지 말고 베푸세요. 그리고 사랑이라는 이름으로 통제하지 마세요."
            },
            "en": {
                "t": "💖 Devoted Love: The Giver & Receiver",
                "c": f"You care for {O} like a parent. You give unconditional love, and {s} feels secure and cherished.",
                "f": f"Resentment arises if you expect equal return. Also, your care might feel like nagging to {O}.",
                "i": "You lead and serve. You derive pleasure from satisfying your partner.",
                "a": "Give without strings attached. Don't try to control them."
            },
            "fr": {"t": "💖 Amour Dévoué", "c": "Vous donnez, ils reçoivent.", "f": "Ne devenez pas étouffant.", "i": "Vous aimez faire plaisir.", "a": "Donnez sans attendre de retour."},
            "es": {"t": "💖 Amor Devoto", "c": "Tú das, ellos reciben.", "f": "No seas asfixiante.", "i": "Te gusta complacer.", "a": "Da sin esperar nada a cambio."},
            "ja": {"t": "💖 献身的な愛", "c": "惜しみなく与える関係。", "f": "見返りを求めると辛くなります。", "i": "相手を満足させることに喜びを感じます。", "a": "愛という名で束縛しないでください。"},
            "zh": {"t": "💖 奉献之爱", "c": "无私给予的关系。", "f": "不要期待回报，否则会失望。", "i": "乐于取悦对方。", "a": "不要以爱之名进行控制。"}
        },
        "Wealth": {
            "score": 88,
            "ko": {
                "t": "🔥 치명적인 매력: 소유욕과 열정",
                "c": "강렬한 성적 매력을 느낍니다. '내 것으로 만들고 싶다'는 정복욕이 사랑의 원동력이 됩니다. 남자가 여자를 만난 경우 최고의 궁합 중 하나입니다.",
                "f": "핵심은 '통제'입니다. 상대를 내 뜻대로 조종하려 들면 숨 막혀 도망갈 수 있습니다. 집착과 의심을 주의하세요.",
                "i": "속궁합 200점! 낮에는 싸워도 밤에는 화해하는 뜨거운 커플입니다. 쉽게 질리지 않습니다.",
                "a": "집착하지 말고 상대를 있는 그대로 존중하세요. 돈 문제는 투명해야 합니다."
            },
            "en": {
                "t": "🔥 Fatal Attraction: Passion & Control",
                "c": f"Intense physical attraction. You want to conquer and possess {O}. Driven by desire.",
                "f": "Control is the issue. Manipulation leads to suffocation. Beware of jealousy.",
                "i": "Score: 200/100. Fight by day, make up by night. Extremely hot connection.",
                "a": f"Respect {P} privacy. Be transparent about money."
            },
            "fr": {"t": "🔥 Attraction Fatale", "c": "Passion intense.", "f": "Jalousie et contrôle.", "i": "Score 200/100 !", "a": "Respectez leur liberté."},
            "es": {"t": "🔥 Atracción Fatal", "c": "Pasión intensa.", "f": "Celos y control.", "i": "¡Puntuación 200/100!", "a": "Respeta su libertad."},
            "ja": {"t": "🔥 致命的な魅力", "c": "所有欲と情熱。", "f": "束縛は禁物。", "i": "相性200点！激しい関係。", "a": "相手を尊重し、執着を捨ててください。"},
            "zh": {"t": "🔥 致命吸引力", "c": "强烈的占有欲。", "f": "控制欲会导致窒息。", "i": "200分！白天吵架晚上和好。", "a": "尊重对方，不要执着。"}
        },
        "Power": {
            "score": 78,
            "ko": {
                "t": "⚖️ 존경과 긴장: 나를 성장시키는 연인",
                "c": "상대방이 나를 리드하고 통제합니다. 묘한 카리스마와 어른스러움에 존경심을 느낍니다. 서로 부족함을 채워주는 '스승과 제자' 같습니다.",
                "f": "상대가 너무 깐깐하거나 보수적일 수 있습니다. 조언이 '잔소리'나 '지적질'로 들리면 스트레스가 폭발합니다.",
                "i": "안정적이고 신뢰가 바탕이 된 관계입니다. 스릴보다는 깊은 정서적 교감이 특징입니다.",
                "a": "자존심 세우지 말고 조언을 들으세요. 서로 간섭하지 않을 선을 정하세요."
            },
            "en": {
                "t": "⚖️ Respect & Tension: The Mentor",
                "c": f"{S} leads you. You feel respect for {P} charisma. Like a 'Teacher-Student' bond where you grow.",
                "f": f"{S} might be too strict. {P} advice can feel like criticism or nagging.",
                "i": "Stable and trusting. Deep emotional security rather than wild thrill.",
                "a": f"Don't be defensive. Listen to {P} advice. Set boundaries."
            },
            "fr": {"t": "⚖️ Respect et Tension", "c": "Relation Mentor-Élève.", "f": "Critiques possibles.", "i": "Stable et profond.", "a": "Écoutez les conseils."},
            "es": {"t": "⚖️ Respeto y Tensión", "c": "Relación Mentor-Estudiante.", "f": "Posibles críticas.", "i": "Estable y profundo.", "a": "Escucha los consejos."},
            "ja": {"t": "⚖️ 尊敬と緊張", "c": "私を成長させる人。", "f": "相手が厳しすぎるかも。", "i": "安定した信頼関係。", "a": "アドバイスを素直に聞き入れましょう。"},
            "zh": {"t": "⚖️ 尊敬与紧张", "c": "让我成长的恋人。", "f": "对方可能太严厉。", "i": "稳定且信任。", "a": "虚心听取建议。"}
        },
        "Resource": { 
            "score": 96,
            "ko": {
                "t": "🍼 무한한 사랑: 힐링 소울메이트",
                "c": "상대방이 당신을 헌신적으로 뒷바라지해줍니다. 엄마 품처럼 편안하고, 나를 이해하고 용서해주는 안식처 같은 관계입니다.",
                "f": "너무 편안해서 권태기가 올 수 있습니다. 상대의 사랑을 당연하게 여기거나, 과잉보호로 느껴질 때 위기가 옵니다.",
                "i": "자극보다는 정서적인 포만감이 큽니다. 서로 안고만 있어도 좋은 따뜻한 관계입니다.",
                "a": "감사함을 표현하세요. 익숙함에 속아 소중함을 잃지 마세요."
            },
            "en": {
                "t": "🍼 Unconditional Love: Healing Soulmate",
                "c": f"{S} supports you devotedly. Safe, understanding, and forgiving like a mother's embrace.",
                "f": f"Comfort can lead to boredom. Don't take {P} love for granted or feel smothered.",
                "i": "Emotional satisfaction > Physical thrill. Warm and gentle connection.",
                "a": "Express gratitude. Don't be too dependent."
            },
            "fr": {"t": "🍼 Amour Inconditionnel", "c": "Âme sœur guérisseuse.", "f": "Risque d'ennui.", "i": "Chaleureux et tendre.", "a": "Soyez reconnaissant."},
            "es": {"t": "🍼 Amor Incondicional", "c": "Alma gemela sanadora.", "f": "Riesgo de aburrimiento.", "i": "Cálido y tierno.", "a": "Se agradecido."},
            "ja": {"t": "🍼 無限の愛", "c": "癒しのソウルメイト。", "f": "マンネリに注意。", "i": "温かく優しい関係。", "a": "感謝を忘れないでください。"},
            "zh": {"t": "🍼 无限的爱", "c": "治愈系灵魂伴侣。", "f": "小心倦怠期。", "i": "温暖而温柔。", "a": "表达感谢，不要视为理所当然。"}
        }
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
        "btn_buy": "전체 리포트 해제 ($10)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "analyze": "궁합 분석하기", "h_chem": "🔮 성격과 케미", "h_conf": "⚔️ 갈등 포인트", 
        "h_inti": "💋 속궁합 & 애정", "h_adv": "🚀 관계를 위한 조언"
    },
    "en": {
        "title": "💘 Love Compatibility", "sub": "Deep analysis of souls, chemistry, and future.",
        "p_info": "Partner Info", "p_name": "Name", "p_dob": "DOB", "p_gender": "Gender",
        "lock_title": "🔒 VIP Report Locked", "lock_msg": "Unlock intimacy, conflict points, and future advice.",
        "btn_buy": "Unlock Report ($10)", "btn_unlock": "Unlock", "key_label": "License Key",
        "analyze": "Analyze", "h_chem": "🔮 Chemistry", "h_conf": "⚔️ Conflict", 
        "h_inti": "💋 Intimacy", "h_adv": "🚀 Advice"
    },
    "fr": {
        "title": "💘 Compatibilité Amoureuse", "sub": "Analyse approfondie des âmes et de la chimie.",
        "p_info": "Info Partenaire", "p_name": "Nom", "p_dob": "Date de Naissance", "p_gender": "Genre",
        "lock_title": "🔒 Rapport VIP", "lock_msg": "Débloquez l'intimité et les conseils.",
        "btn_buy": "Débloquer ($10)", "btn_unlock": "Déverrouiller", "key_label": "Clé",
        "analyze": "Analyser", "h_chem": "🔮 Chimie", "h_conf": "⚔️ Conflits", 
        "h_inti": "💋 Intimité", "h_adv": "🚀 Conseils"
    },
    "es": {
        "title": "💘 Compatibilidad Amorosa", "sub": "Análisis profundo de almas y química.",
        "p_info": "Info Pareja", "p_name": "Nombre", "p_dob": "Fecha Nacimiento", "p_gender": "Género",
        "lock_title": "🔒 Reporte VIP", "lock_msg": "Desbloquea intimidad y consejos.",
        "btn_buy": "Desbloquear ($10)", "btn_unlock": "Desbloquear", "key_label": "Clave",
        "analyze": "Analizar", "h_chem": "🔮 Química", "h_conf": "⚔️ Conflictos", 
        "h_inti": "💋 Intimidad", "h_adv": "🚀 Consejos"
    },
    "ja": {
        "title": "💘 恋愛相性診断", "sub": "魂、相性、未来を深く分析。",
        "p_info": "相手の情報", "p_name": "名前", "p_dob": "生年月日", "p_gender": "性別",
        "lock_title": "🔒 VIPレポート", "lock_msg": "親密さ、葛藤、未来のアドバイスを解除。",
        "btn_buy": "解除 ($10)", "btn_unlock": "解除", "key_label": "キー",
        "analyze": "分析する", "h_chem": "🔮 相性", "h_conf": "⚔️ 葛藤", 
        "h_inti": "💋 親密さ", "h_adv": "🚀 アドバイス"
    },
    "zh": {
        "title": "💘 恋爱契合度", "sub": "深度分析灵魂、化学反应和未来。",
        "p_info": "伴侣信息", "p_name": "姓名", "p_dob": "出生日期", "p_gender": "性别",
        "lock_title": "🔒 VIP报告", "lock_msg": "解锁亲密度、冲突点和建议。",
        "btn_buy": "解锁 ($10)", "btn_unlock": "解锁", "key_label": "密钥",
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
                if st.button(t['btn_unlock']):
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_love"] = True
                        st.success("Unlocked!")
                        st.rerun()
                    else:
                        try:
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={"product_permalink": "love_compatibility", "license_key": k_in}).json()
                            if r.get("success"):
                                st.session_state["unlocked_love"] = True
                                st.rerun()
                            else:
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={"product_permalink": "all-access_pass", "license_key": k_in}).json()
                                if r2.get("success"):
                                    st.session_state["unlocked_love"] = True
                                    st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: st.error("Error")
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
