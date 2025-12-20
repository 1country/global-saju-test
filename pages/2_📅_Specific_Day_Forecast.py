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
            # (다른 언어 생략 - 영어 사용)
        },
        "Output": { # 식상
            "ko": {
                "score": 4, "star": "⭐⭐⭐⭐⭐",
                "t": "🎨 끼가 폭발하는 '표현'의 날",
                "d": "아이디어가 화산처럼 분출됩니다. 창의적인 기획에 탁월합니다. 당신이 주인공이 되어 무대를 휘어잡는 날입니다.",
                "money": "당신의 재주가 수익으로 연결됩니다. 단, 기분이 들떠서 하는 '충동구매'만 조심하세요.",
                "love": "유머 감각이 폭발하여 이성을 사로잡습니다. 고백하기 좋은 날입니다.",
                "health": "에너지 소모가 극심해 저녁엔 방전될 수 있습니다. 달콤한 디저트를 드세요.",
                "action": "1. 주문: '나는 아티스트다.'\n2. 행동: 노래방, SNS 포스팅\n3. 주의: 말실수 조심.",
                "lucky": "🎤 마이크, 🍰 디저트"
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
            }
        },
        "Wealth": { # 재성
            "ko": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 결실을 맺는 '수확'의 날",
                "d": "현실적이고 계산적인 날입니다. 노력에 대한 확실한 보상이 주어지며, 결과가 당신을 증명합니다.",
                "money": "금전운 최상! 예상치 못한 보너스나 수익이 생깁니다. 쇼핑하기에도 좋습니다.",
                "love": "남자는 여자가 따르고, 여자는 능력 있는 남자를 만납니다. 맛집 데이트가 좋습니다.",
                "health": "컨디션 좋음. 하체 운동이 운을 더해줍니다.",
                "action": "1. 주문: '나는 부자다.'\n2. 행동: 지갑 정리, 복권 구매\n3. 주의: 돈 자랑 금지.",
                "lucky": "💳 지갑, 🍗 맛집"
            },
            "en": {
                "score": 5, "star": "⭐⭐⭐⭐⭐",
                "t": "💰 Day of Harvest (Wealth)",
                "d": "Be realistic. Tangible rewards await. Results matter today.",
                "money": "Best Financial Luck! Bonuses likely. Good for shopping.",
                "love": "Great romance luck. Gourmet dates bring luck.",
                "health": "Good condition. Leg exercises boost luck.",
                "action": "1. Mantra: 'I am Abundant.'\n2. Action: Organize wallet.\n3. Warning: Don't show off money.",
                "lucky": "💳 Wallet, 🍗 Fine Dining"
            }
        },
        "Power": { # 관성
            "ko": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ 왕관의 무게를 견디는 '명예'의 날",
                "d": "책임감과 의무가 당신을 둘러쌉니다. 압박감이 있지만 견뎌내면 리더로서 인정받습니다.",
                "money": "돈보다는 명예가 올라갑니다. 승진운이 있습니다. 돈은 오히려 나갈 수 있습니다.",
                "love": "일에 치여 연인에게 소홀하기 쉽습니다. 스트레스를 연인에게 풀지 마세요.",
                "health": "스트레스 주의. 격렬한 운동보다 명상이나 반신욕을 하세요.",
                "action": "1. 주문: '이 또한 지나가리라.'\n2. 행동: 정장 착용, 규칙 준수\n3. 주의: 지각 금지.",
                "lucky": "👔 정장, 🧘 명상"
            },
            "en": {
                "score": 2, "star": "⭐⭐",
                "t": "⚖️ Day of Honor (Pressure)",
                "d": "Responsibility surrounds you. Enduring pressure brings recognition.",
                "money": "Reputation rises, not cash. Promotion luck.",
                "love": "Don't vent stress on your partner.",
                "health": "High stress. Try yoga or meditation.",
                "action": "1. Mantra: 'This too shall pass.'\n2. Action: Wear a suit.\n3. Warning: No lateness.",
                "lucky": "👔 Suit, 🧘 Meditation"
            }
        },
        "Resource": { # 인성
            "ko": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 에너지를 충전하는 '힐링'의 날",
                "d": "엄마 품처럼 편안합니다. 주변에서 도와줍니다. 공부하거나 휴식을 취하기 최적입니다.",
                "money": "현금보다 문서운(계약)이 좋습니다. 나를 위한 공부에 투자하세요.",
                "love": "사랑받는 날입니다. 대접받습니다. 예의 바른 사람을 만납니다.",
                "health": "몸이 나른한 건 쉬라는 신호입니다. 낮잠이나 마사지를 즐기세요.",
                "action": "1. 주문: '나는 사랑받는 사람이다.'\n2. 행동: 독서, 부모님께 전화\n3. 주의: 게으름.",
                "lucky": "📚 책, 🛌 휴식"
            },
            "en": {
                "score": 4, "star": "⭐⭐⭐⭐",
                "t": "📚 Day of Healing (Support)",
                "d": "Comfortable like a mother's embrace. People help you. Best for study and rest.",
                "money": "Good document luck. Invest in yourself.",
                "love": "You are loved and treated well.",
                "health": "Rest if you feel lethargic. Massage helps.",
                "action": "1. Mantra: 'I am loved.'\n2. Action: Reading.\n3. Warning: Laziness.",
                "lucky": "📚 Book, 🛌 Rest"
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

# ⭐ [수정] UI 텍스트 업데이트 (Free 문구 제거, All Premium 강조)
ui = {
    "ko": {
        "title": "📅 그날의 운세", "sub": "선택한 날짜의 기운을 미리 확인하세요.",
        "date_label": "날짜 선택", "btn_anal": "분석하기",
        "res_header": "🔒 오늘의 운세 분석 결과 (Premium)", # Free 제거
        "lock_msg": "이 날의 기운, 재물, 연애, 행동 지침 등 모든 상세 분석은 유료 리포트에서 제공됩니다.",
        "btn_buy": "전체 리포트 열람 ($5)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "h_money": "💰 재물운 가이드", "h_love": "❤️ 연애운 가이드", "h_health": "💪 건강 관리", 
        "h_action": "🚀 오늘의 행동 지침", "h_lucky": "🍀 행운의 아이템"
    },
    "en": {
        "title": "📅 Specific Day Forecast", "sub": "Check the energy of any important day.",
        "date_label": "Select Date", "btn_anal": "Analyze",
        "res_header": "🔒 Daily Forecast Analysis (Premium)", # Free 제거
        "lock_msg": "Unlock the full report including Day Energy, Wealth, Love, and Action Guides.",
        "btn_buy": "Unlock Full Report ($5)", "btn_unlock": "Unlock", "key_label": "License Key",
        "h_money": "💰 Wealth Guide", "h_love": "❤️ Love Guide", "h_health": "💪 Health", 
        "h_action": "🚀 Action Plan", "h_lucky": "🍀 Lucky Items"
    },
    # (다른 언어는 영어 fallback)
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
    
    def map_elem(hanja):
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(hanja, 'Wood')
    
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
        
        # 1. 총운 (원래 Free였던 것)
        st.markdown(f"""
            <div class='card' style='border:1px solid #f472b6; text-align:center;'>
                <h2 style='color:#f472b6; margin-top:0;'>{res['t']}</h2>
                <h1 style='font-size:3.5em;'>{res['star']}</h1>
                <p style='font-size:1.3em; line-height:1.6;'>{res['d']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. 상세 (탭)
        st.write("")
        tab1, tab2, tab3 = st.tabs([t['h_money'] + " & " + t['h_love'], t['h_health'] + " & " + t['h_action'], t['h_lucky']])
        
        with tab1:
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
            
        with tab2:
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
            
        with tab3:
            st.markdown(f"""
                <div class='card' style='text-align:center;'>
                    <h1 style='font-size:3em;'>{res['lucky']}</h1>
                    <p style='color:#cbd5e1;'>{t['h_lucky']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        components.html("""<script>function p(){window.parent.print();}</script><div style='display:flex;justify-content:center;margin-top:20px;'><button onclick='p()' style='background:#ec4899;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;'>🖨️ Save Report</button></div>""", height=80)
