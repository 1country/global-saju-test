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

# 언어 설정 (세션 상태 우선, 없으면 환경변수)
if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

# 🔑 [마스터 키 & 구매 링크]
UNLOCK_CODE = "MASTER2026"
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/specific_day"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정 (CSS - 가독성 및 테마 적용)
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
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
        section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
        [data-testid="stSidebarNav"] span { font-size: 1.1rem !important; font-weight: 600 !important; color: #e2e8f0 !important; }
        
        /* 헤더 스타일 */
        .day-header {
            font-size: 2.2em; font-weight: 800; color: #f472b6; text-align: center; margin-bottom: 20px;
            font-family: 'Gowun Batang', serif; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);
        }
        .card {
            background: rgba(30, 41, 59, 0.8); border: 1px solid #475569; padding: 25px;
            border-radius: 15px; margin-bottom: 20px; color: #e2e8f0;
        }
        
        /* 잠금 오버레이 */
        .lock-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.85); padding: 30px; border-radius: 15px; 
            text-align: center; width: 90%; z-index: 99; border: 1px solid #f472b6;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 데이터 함수 (6개 국어 완벽 지원)
# ----------------------------------------------------------------

# (1) 관계 계산 및 운세 데이터 반환
def get_relationship_data(user_elem, target_elem, language):
    # 오행 상생상극 로직 (Wood -> Fire -> Earth -> Metal -> Water)
    relations = {
        "Wood": {"Wood": "Friend", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Support"},
        "Fire": {"Wood": "Support", "Fire": "Friend", "Earth": "Output", "Metal": "Wealth", "Water": "Power"},
        "Earth": {"Wood": "Power", "Fire": "Support", "Earth": "Friend", "Metal": "Output", "Water": "Wealth"},
        "Metal": {"Wood": "Wealth", "Fire": "Power", "Earth": "Support", "Metal": "Friend", "Water": "Output"},
        "Water": {"Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Support", "Water": "Friend"},
    }
    # 기본값은 Friend
    rel_key = relations.get(user_elem, {}).get(target_elem, "Friend")
    
    # 6개 국어 데이터베이스
    db = {
        "Friend": { # 비견/겁재
            "ko": {"t": "🤝 나와 같은 기운의 날 (경쟁/협력)", "d": "자신감이 넘치고 의욕이 생깁니다. 동료와 함께하면 좋지만 고집은 금물.", "star": "⭐⭐⭐"},
            "en": {"t": "🤝 Day of Peers (Competition)", "d": "High confidence. Good for teamwork, but avoid stubbornness.", "star": "⭐⭐⭐"},
            "fr": {"t": "🤝 Jour des Pairs", "d": "Grande confiance. Bon pour l'équipe, évitez l'entêtement.", "star": "⭐⭐⭐"},
            "es": {"t": "🤝 Día de Pares", "d": "Alta confianza. Bueno para equipo, evita la terquedad.", "star": "⭐⭐⭐"},
            "ja": {"t": "🤝 同僚の日 (競争/協力)", "d": "自信が溢れます。チームワークには良いですが頑固は禁物。", "star": "⭐⭐⭐"},
            "zh": {"t": "🤝 比肩之日 (竞争/合作)", "d": "自信满满。适合团队合作，切忌固执。", "star": "⭐⭐⭐"}
        },
        "Output": { # 식신/상관
            "ko": {"t": "🔥 능력을 발휘하는 날 (표현/창작)", "d": "아이디어가 샘솟습니다. 발표, 미팅, 데이트 등 나를 드러내세요.", "star": "⭐⭐⭐⭐⭐"},
            "en": {"t": "🔥 Day of Expression", "d": "Ideas flow. Perfect for presentations and dates. Show yourself.", "star": "⭐⭐⭐⭐⭐"},
            "fr": {"t": "🔥 Jour d'Expression", "d": "Les idées fusent. Parfait pour présentations et rendez-vous.", "star": "⭐⭐⭐⭐⭐"},
            "es": {"t": "🔥 Día de Expresión", "d": "Las ideas fluyen. Perfecto para presentaciones y citas.", "star": "⭐⭐⭐⭐⭐"},
            "ja": {"t": "🔥 表現の日 (創造)", "d": "アイデアが湧きます。発表やデートに最適です。", "star": "⭐⭐⭐⭐⭐"},
            "zh": {"t": "🔥 表现之日 (创意)", "d": "灵感涌现。适合演讲、会议和约会。", "star": "⭐⭐⭐⭐⭐"}
        },
        "Wealth": { # 편재/정재
            "ko": {"t": "💰 이득을 얻는 날 (재물/결실)", "d": "노력한 만큼 결과가 나옵니다. 금전운이 좋고 판단력이 뛰어납니다.", "star": "⭐⭐⭐⭐"},
            "en": {"t": "💰 Day of Wealth", "d": "Efforts pay off. Good financial luck and judgment.", "star": "⭐⭐⭐⭐"},
            "fr": {"t": "💰 Jour de Richesse", "d": "Les efforts paient. Bonne chance financière.", "star": "⭐⭐⭐⭐"},
            "es": {"t": "💰 Día de Riqueza", "d": "Esfuerzos valen la pena. Buena suerte financiera.", "star": "⭐⭐⭐⭐"},
            "ja": {"t": "💰 財の日 (結果)", "d": "努力が報われます。金運が良い日です。", "star": "⭐⭐⭐⭐"},
            "zh": {"t": "💰 财运之日 (结果)", "d": "付出有回报。财运佳，判断力强。", "star": "⭐⭐⭐⭐"}
        },
        "Power": { # 편관/정관
            "ko": {"t": "⚖️ 책임과 명예의 날 (직장/압박)", "d": "부담스럽지만 잘 해내면 인정받습니다. 규칙과 예의를 지키세요.", "star": "⭐⭐"},
            "en": {"t": "⚖️ Day of Power", "d": "Pressured but rewarding. Follow rules and be polite.", "star": "⭐⭐"},
            "fr": {"t": "⚖️ Jour de Pouvoir", "d": "Sous pression mais gratifiant. Suivez les règles.", "star": "⭐⭐"},
            "es": {"t": "⚖️ Día de Poder", "d": "Presionado pero gratificante. Sigue las reglas.", "star": "⭐⭐"},
            "ja": {"t": "⚖️ 権力の日 (仕事)", "d": "プレッシャーがありますが、認められます。礼儀正しく。", "star": "⭐⭐"},
            "zh": {"t": "⚖️ 官运之日 (事业)", "d": "虽有压力但能获认可。请遵规守礼。", "star": "⭐⭐"}
        },
        "Support": { # 편인/정인
            "ko": {"t": "📚 배움과 도움의 날 (계약/휴식)", "d": "윗사람의 도움이나 좋은 문서 운이 있습니다. 공부나 계획에 좋습니다.", "star": "⭐⭐⭐⭐"},
            "en": {"t": "📚 Day of Support", "d": "Help from superiors or document luck. Good for study.", "star": "⭐⭐⭐⭐"},
            "fr": {"t": "📚 Jour de Soutien", "d": "Aide des supérieurs. Bon pour étudier ou planifier.", "star": "⭐⭐⭐⭐"},
            "es": {"t": "📚 Día de Apoyo", "d": "Ayuda de superiores. Bueno para estudiar.", "star": "⭐⭐⭐⭐"},
            "ja": {"t": "📚 支援の日 (学び)", "d": "目上の人の助けがあります。勉強や計画に良いです。", "star": "⭐⭐⭐⭐"},
            "zh": {"t": "📚 印星之日 (贵人)", "d": "有长辈相助。适合学习或制定计划。", "star": "⭐⭐⭐⭐"}
        }
    }
    
    # 해당 관계의 데이터를 가져오고, 언어에 맞는 텍스트 반환
    data = db.get(rel_key, db["Friend"])
    return data.get(language, data["en"]) # 없으면 영어 기본값

# ----------------------------------------------------------------
# 4. 사이드바 구성 (언어 변경 기능)
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    
    # 현재 모드 표시
    lang_map_display = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Current Mode: **{lang_map_display.get(lang, 'English')}**")
    
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
    
    # 홈 버튼 번역
    home_labels = {
        "ko": "🏠 홈으로", "en": "🏠 Go Home", "fr": "🏠 Accueil", 
        "es": "🏠 Inicio", "ja": "🏠 ホーム", "zh": "🏠 首页"
    }
    if st.button(home_labels.get(lang, "Go Home"), use_container_width=True):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 5. 메인 로직 (UI 텍스트 & 흐름)
# ----------------------------------------------------------------
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please go Home first.")
    st.stop()

# ⭐ UI 텍스트 (6개 국어 완벽 지원) ⭐
ui = {
    "ko": {
        "title": "📅 그날의 운세", "sub": "중요한 날의 기운을 미리 확인하세요.",
        "date_label": "날짜를 선택하세요", "analyze_btn": "운세 분석하기",
        "res_h": "당신의 운세 분석 결과", "lock_title": "🔒 프리미엄 상세 분석",
        "lock_msg": "시간대별 행운, 행운의 색상, 구체적인 행동 지침은 유료 리포트에서 확인하세요.",
        "btn_buy": "상세 분석 해제 ($5)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "detail_h": "🕒 상세 가이드 (Premium)", "warn_lock": "⚠️ 라이센스 횟수가 1회 차감됩니다.", "pop_ok": "확인"
    },
    "en": {
        "title": "📅 Specific Day Forecast", "sub": "Check the energy of any important day.",
        "date_label": "Select a Date", "analyze_btn": "Analyze",
        "res_h": "Analysis Result", "lock_title": "🔒 Premium Detail",
        "lock_msg": "Unlock hourly luck, lucky colors, and specific action guides.",
        "btn_buy": "Unlock Details ($5)", "btn_unlock": "Unlock", "key_label": "License Key",
        "detail_h": "🕒 Detailed Guide (Premium)", "warn_lock": "⚠️ This will consume 1 credit.", "pop_ok": "Proceed"
    },
    "fr": {
        "title": "📅 Prévisions du Jour", "sub": "Vérifiez l'énergie d'un jour important.",
        "date_label": "Sélectionnez une date", "analyze_btn": "Analyser",
        "res_h": "Résultat de l'analyse", "lock_title": "🔒 Détails Premium",
        "lock_msg": "Débloquez la chance horaire, les couleurs et les conseils.",
        "btn_buy": "Débloquer (5$)", "btn_unlock": "Déverrouiller", "key_label": "Clé de licence",
        "detail_h": "🕒 Guide Détaillé", "warn_lock": "⚠️ Cela consommera 1 crédit.", "pop_ok": "Continuer"
    },
    "es": {
        "title": "📅 Pronóstico del Día", "sub": "Revisa la energía de un día importante.",
        "date_label": "Selecciona una fecha", "analyze_btn": "Analizar",
        "res_h": "Resultado del Análisis", "lock_title": "🔒 Detalle Premium",
        "lock_msg": "Desbloquea la suerte por hora, colores y guías.",
        "btn_buy": "Desbloquear (5$)", "btn_unlock": "Desbloquear", "key_label": "Clave de licencia",
        "detail_h": "🕒 Guía Detallada", "warn_lock": "⚠️ Esto consumirá 1 crédito.", "pop_ok": "Proceder"
    },
    "ja": {
        "title": "📅 その日の運勢", "sub": "大切な日の運気を事前にチェックしましょう。",
        "date_label": "日付を選択", "analyze_btn": "分析する",
        "res_h": "分析結果", "lock_title": "🔒 プレミアム詳細",
        "lock_msg": "時間別の運勢、ラッキーカラー、行動指針を確認できます。",
        "btn_buy": "詳細を解除 ($5)", "btn_unlock": "解除", "key_label": "ライセンスキー",
        "detail_h": "🕒 詳細ガイド", "warn_lock": "⚠️ 1回分消費されます。", "pop_ok": "確認"
    },
    "zh": {
        "title": "📅 特定日运势", "sub": "提前查看重要日子的气场。",
        "date_label": "选择日期", "analyze_btn": "开始分析",
        "res_h": "分析结果", "lock_title": "🔒 高级详情",
        "lock_msg": "解锁每小时运势、幸运色和行动指南。",
        "btn_buy": "解锁详情 ($5)", "btn_unlock": "解锁", "key_label": "许可证密钥",
        "detail_h": "🕒 详细指南", "warn_lock": "⚠️ 将扣除1次使用次数。", "pop_ok": "继续"
    }
}

if lang not in ui: t = ui['en']
else: t = ui[lang]

# 화면 표시
st.markdown(f"<div class='day-header'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color:#cbd5e1; margin-bottom:30px;'>{t['sub']}</div>", unsafe_allow_html=True)

# 1. 날짜 입력 섹션
with st.container(border=True):
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        target_date = st.date_input(t['date_label'], min_value=date.today())
    with col_d2:
        st.write("")
        st.write("")
        check_clicked = st.button(t['analyze_btn'], type="primary", use_container_width=True)

# 2. 분석 결과 표시
if check_clicked or st.session_state.get('day_analyzed'):
    st.session_state['day_analyzed'] = True
    
    # 내 일간 vs 타겟 일간 계산
    my_info = calculate_day_gan(st.session_state["birth_date"])
    target_info = calculate_day_gan(target_date)
    
    # 한자 -> 영어 매핑
    def map_elem(hanja):
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(hanja, 'Wood')
        
    my_elem = map_elem(my_info['element'])
    tgt_elem = map_elem(target_info['element'])
    
    # 데이터 가져오기
    res = get_relationship_data(my_elem, tgt_elem, lang)
    
    st.divider()
    
    # [무료] 총운 표시
    st.subheader(t['res_h'])
    st.markdown(f"""
        <div class='card' style='border:1px solid #f472b6;'>
            <h2 style='color:#f472b6; margin-top:0;'>{res['t']}</h2>
            <h1 style='text-align:center; font-size:3em;'>{res['star']}</h1>
            <p style='font-size:1.2em; line-height:1.6; text-align:center;'>{res['d']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # [유료] 상세 가이드 (잠금/해제)
    st.subheader(t['detail_h'])
    
    if "unlocked_day" not in st.session_state: st.session_state["unlocked_day"] = False
    
    # 잠금 상태일 때
    if not st.session_state["unlocked_day"]:
        # 블러 처리된 가짜 콘텐츠
        blur_html = f"""
        <div style='position: relative; overflow: hidden; border-radius: 15px;'>
            <div style='filter: blur(8px); opacity: 0.6; pointer-events: none;'>
                <div class='card'>
                    <h4>🍀 Lucky Time</h4>
                    <p>09:00 ~ 11:00 (Best for meetings)</p>
                    <hr>
                    <h4>🎨 Lucky Color & Direction</h4>
                    <p>Blue, North-East</p>
                    <hr>
                    <h4>🚀 Action Plan</h4>
                    <p>Wear bright clothes and speak loudly. Avoid contracts in the afternoon.</p>
                </div>
            </div>
            <div class='lock-overlay'>
                <h3 style='color: #f472b6;'>{t['lock_title']}</h3>
                <p style='color: #e2e8f0; margin-bottom: 20px;'>{t['lock_msg']}</p>
                <a href="{GUMROAD_LINK_SPECIFIC}" target="_blank" 
                   style="background-color: #ec4899; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                   {t['btn_buy']}
                </a>
            </div>
        </div>
        """
        st.markdown(blur_html, unsafe_allow_html=True)
        
        # 키 입력창
        with st.expander(f"{t['key_label']} Input"):
            c_k1, c_k2 = st.columns([3, 1])
            with c_k1: k_in = st.text_input(t['key_label'], type="password")
            with c_k2: 
                st.write("")
                st.write("")
                if st.button(t['btn_unlock']):
                    # 1. 마스터 키 확인
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_day"] = True
                        st.success("Unlocked!")
                        st.rerun()
                    
                    # 2. 검로드 확인
                    try:
                        # 단품
                        r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                          data={"product_permalink": "specific_day", "license_key": k_in}).json()
                        if r.get("success"):
                            st.session_state["unlocked_day"] = True
                            st.success("Verified!")
                            st.rerun()
                        else:
                            # 프리패스
                            r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                               data={"product_permalink": "all-access_pass", "license_key": k_in}).json()
                            if r2.get("success"):
                                st.session_state["unlocked_day"] = True
                                st.success("Verified!")
                                st.rerun()
                            else:
                                st.error("Invalid Key")
                    except:
                        st.error("Connection Error")
                        
    else:
        # 해제된 실제 데이터
        st.success("🔓 Premium Content Unlocked!")
        
        # 행운 데이터 (간단 로직 예시)
        lucky_time = "09:00 ~ 13:00"
        lucky_color = "Red, Purple" if tgt_elem == "Fire" else "Blue, Black"
        action_tip = "Be proactive! (적극적으로 행동하세요)"
        
        st.markdown(f"""
            <div class='card'>
                <div style='display:flex; justify-content:space-around; text-align:center;'>
                    <div>
                        <h4 style='color:#f472b6;'>⏰ Lucky Time</h4>
                        <p style='font-size:1.2em;'>{lucky_time}</p>
                    </div>
                    <div>
                        <h4 style='color:#f472b6;'>🎨 Lucky Color</h4>
                        <p style='font-size:1.2em;'>{lucky_color}</p>
                    </div>
                </div>
                <hr style='border-color:#475569;'>
                <h4 style='color:#f472b6;'>🚀 Action Guide</h4>
                <p style='font-size:1.1em;'>{action_tip}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 인쇄 버튼
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;'>🖨️ Save Result</button></div>""", height=80)
