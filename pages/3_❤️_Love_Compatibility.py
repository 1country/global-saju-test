import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Love Compatibility", page_icon="💘", layout="wide")

# 🔑 [키 설정]
UNLOCK_CODE = "MASTER2026"

# (1) 이 페이지 전용 상품 (3회 제한)
PRODUCT_PERMALINK_SPECIFIC = "love_compatibility"
# (2) 만능 패스 상품 (10회 제한)
PRODUCT_PERMALINK_ALL = "all-access_pass"

# 구매 링크
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/love_compatibility"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #be185d; margin-bottom: 10px; text-align: center;}
        
        /* 리포트 스타일 고급화 */
        .report-container {
            background-color: white; padding: 50px; border-radius: 20px;
            box-shadow: 0 10px 40px rgba(236, 72, 153, 0.15); border: 1px solid #fce7f3;
        }
        .section-box {
            margin-bottom: 35px; padding-bottom: 25px; border-bottom: 1px dashed #f9a8d4;
        }
        .section-box:last-child { border-bottom: none; }
        
        .section-title {
            font-size: 1.5em; font-weight: bold; color: #9d174d; margin-bottom: 20px; 
            display: flex; align-items: center; border-left: 5px solid #db2777; padding-left: 15px;
        }
        .content-text { font-size: 1.1em; line-height: 1.9; color: #374151; text-align: justify; letter-spacing: -0.02em; }
        .score-display { text-align: center; font-size: 3.5em; font-weight: bold; color: #be185d; margin: 30px 0; }
        
        .user-card {
            background: #fff1f2; padding: 20px; border-radius: 15px; border: 1px solid #fecdd3;
            text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .vs-badge {
            display: flex; justify-content: center; align-items: center; 
            font-size: 2em; font-weight: bold; color: #db2777; height: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 2. 사이드바
# ----------------------------------------------------------------
with st.sidebar:
    st.title("Settings")
    lang_opt = st.radio("Language", ["English", "한국어"])
    lang = "ko" if "한국어" in lang_opt else "en"
    st.markdown("---")
    if st.button("👈 Home"): st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. [초대형] 궁합 데이터 (꼬리표 제거 & 분량 확대)
# ----------------------------------------------------------------
def get_love_report(u_elem, p_elem, u_gender, p_gender, lang):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    rel = relations[u_elem][p_elem]
    
    # 🌟 호칭 설정 (언어별)
    if lang == "ko":
        me_str = "당신"
        pt_str = "상대방"
    else:
        me_str = "You"
        pt_str = "Your Partner"

    # 🌟 시나리오 데이터 (꼬리표 제거 & 내용 3배 증량)
    reports = {
        "Same": {
            "score": 85,
            "ko": {
                "title": "🤝 거울 속의 연인: 운명적 동질감과 자존심의 대결",
                "chemistry": f"두 사람은 처음 만나는 순간부터 **'이 사람, 나랑 진짜 비슷하다'**는 느낌을 강하게 받았을 것입니다. 마치 잃어버린 반쪽을 찾은 것처럼 대화 코드, 웃음 포인트, 심지어 싫어하는 것까지 똑같습니다. 말하지 않아도 서로의 기분을 알아채는 **텔레파시 커플**입니다. 서로가 서로에게 가장 친한 친구이자, 가장 뜨거운 연인이 될 수 있는 완벽한 파트너입니다. 함께 있으면 세상 무서울 것이 없는 든든한 동지가 되며, 데이트를 할 때도 친구처럼 편안하고 즐거운 분위기가 계속됩니다.",
                "conflict": f"하지만 **'너무 똑같다'**는 것이 치명적인 단점이 되기도 합니다. 두 사람 모두 자아와 고집이 강해서, 한 번 싸움이 붙으면 절대 물러서지 않습니다. 특히 상대방에게서 **'나의 단점'**을 발견했을 때 참을 수 없는 짜증을 느끼게 됩니다. 싸움의 원인은 대부분 사소한 자존심 문제입니다. '네가 먼저 사과해'라며 며칠씩 냉전을 벌이기도 합니다. 둘 다 불같은 성격이라면 끝장을 볼 수도 있으니, 화가 났을 때는 잠시 자리를 피하는 지혜가 필요합니다.",
                "intimacy": "속궁합은 **100점 만점에 90점**입니다. 친구처럼 장난치듯 시작해서 열정적으로 변하는 타입입니다. 서로의 몸과 마음 상태를 누구보다 잘 알기 때문에, 상대가 무엇을 원하는지 본능적으로 캐치합니다. 권태기가 와도 새로운 시도를 통해 금방 극복할 수 있는 에너지가 있습니다.",
                "future": "결혼을 한다면 **'맞벌이 부부'**나 **'동업자 부부'**가 될 확률이 높습니다. 서로 대등한 위치에서 가정을 꾸려나가며, 친구 같은 부모가 됩니다. 다만, 경제권 문제로 주도권 싸움을 할 수 있으니 통장은 각자 관리하거나 투명하게 공개하는 것이 좋습니다.",
                "advice": "1. **자존심 죽이기:** 상대방을 이기려 들지 마세요. 이겨봤자 남는 건 상처뿐입니다.\n2. **먼저 사과하기:** '미안해'라는 말이 관계를 구합니다.\n3. **친구 같은 데이트:** 로맨틱한 분위기보다 활동적인 데이트가 사랑을 키웁니다."
            },
            "en": {
                "title": "🤝 Mirror Couple: Twin Souls with Ego Clashes",
                "chemistry": f"You felt an instant connection with your partner, as if looking into a mirror. You share the same humor, values, and dislikes. A telepathic connection exists between you two. You are best friends and lovers, making the relationship incredibly comfortable and fun.",
                "conflict": f"Being too similar is the trap. Both have strong egos and refuse to back down in arguments. You might hate seeing your own flaws reflected in your partner. Arguments often stem from trivial pride issues rather than logical reasons.",
                "intimacy": "Physical chemistry is **90/100**. It starts playful like friends and ends passionate. You intuitively know what the other wants without needing words. Even if boredom strikes, you can overcome it with new adventures.",
                "future": "Likely to be a dual-income couple or business partners. You will be equal partners in marriage, like friends raising a family together. Be transparent about finances to avoid power struggles.",
                "advice": "1. **Drop the Ego:** Winning an argument only hurts the relationship.\n2. **Apologize First:** A simple 'I'm sorry' works magic.\n3. **Active Dates:** Choose fun activities over serious romantic dinners."
            }
        },
        "Output": {
            "score": 92,
            "ko": {
                "title": "💖 헌신적인 사랑: 아낌없이 주는 나무와 사랑받는 꽃",
                "chemistry": f"**{me_str}**이 **{pt_str}**를 자식처럼 예뻐하고 챙겨주는 관계입니다. 본인은 상대방을 보기만 해도 귀여워서 어쩔 줄 모르고, 맛있는 것이 있으면 하나라도 더 먹이고 싶어 합니다. 상대방 역시 당신의 무한한 사랑 속에서 안정감을 느끼고, 당신을 전적으로 의지하게 됩니다. 세상에서 가장 **이타적이고 희생적인 사랑**을 하는 커플입니다. 주는 사람은 주는 기쁨을, 받는 사람은 받는 행복을 누리니 이보다 더 평화로울 수 없습니다.",
                "conflict": f"문제는 **{me_str}**이 지칠 때 발생합니다. '나는 이만큼 해줬는데, 너는 왜 나한테 그만큼 안 해줘?'라는 보상 심리가 생기는 순간 서운함이 폭발합니다. 또한, 당신의 관심이 지나치면 상대방에게는 간섭과 잔소리(통제)로 느껴질 수 있습니다. 마치 엄마와 사춘기 자녀처럼 투닥거릴 수 있는 위험이 있습니다.",
                "intimacy": f"침대에서도 **{me_str}**이 분위기를 리드하고 봉사하는 형태입니다. 상대방의 만족을 위해 최선을 다하며, 거기서 기쁨을 느낍니다. 감정적인 교감이 매우 풍부하고 로맨틱한 관계입니다.",
                "future": f"결혼 인연으로 아주 강력합니다. 특히 자녀가 생기면 관계가 더욱 단단해집니다. **{me_str}**이 집안의 대소사를 주도하고, 상대방은 잘 따르는 안정적인 가정이 됩니다. 다만 당신이 혼자 모든 짐을 짊어지지 않도록 역할 분담이 필요합니다.",
                "advice": "1. **기대하지 않기:** 내가 해준 만큼 돌아오지 않아도 실망하지 마세요.\n2. **잔소리 줄이기:** 사랑이라는 이름으로 상대를 통제하지 마세요.\n3. **표현 요구하기:** 상대방에게 '고맙다'는 말을 자주 해달라고 요청하세요."
            },
            "en": {
                "title": "💖 Devoted Love: The Giver and The Receiver",
                "chemistry": f"You care for your partner like a parent cares for a child. Unconditional love flows from you, and your partner feels secure and cherished. It is an ideal balance where the giver finds joy in giving, and the receiver feels deeply loved.",
                "conflict": f"Issues arise when the Giver burns out. Expecting an equal return on your sacrifice leads to resentment. Also, your care can turn into nagging or controlling behavior, making your partner feel suffocated.",
                "intimacy": "You lead and serve in bed. It is a highly emotional and romantic connection where you derive pleasure from satisfying your partner.",
                "future": "Strong marriage potential. Children will strengthen the bond even further. You will likely lead the household decisions. Ensure responsibilities are shared to avoid burnout.",
                "advice": "1. **Don't Expect Return:** Give without strings attached.\n2. **Reduce Nagging:** Care, don't control.\n3. **Ask for Appreciation:** Remind your partner to say 'Thank you'."
            }
        },
        "Wealth": {
            "score": 88,
            "ko": {
                "title": "🔥 치명적인 매력: 소유욕과 주도권의 줄다리기",
                "chemistry": f"두 사람은 서로에게 **강렬한 성적 매력**을 느낍니다. 특히 **{me_str}**에게 **{pt_str}**는 '내 것으로 만들고 싶다'는 정복욕을 자극하는 대상입니다. 첫눈에 반했거나, 만나는 순간부터 스파크가 튀었을 확률이 높습니다. 서로를 소유하고 싶어 하는 욕망이 사랑의 원동력이 됩니다. (남자가 여자를 만난 경우라면 가장 이상적인 배치 중 하나입니다.)",
                "conflict": f"이 관계의 핵심은 **'통제'**입니다. **{me_str}**이 상대를 내 뜻대로 조종하려 들면 상대방은 숨이 막혀 도망치고 싶어집니다. 집착과 의심이 싹트기 쉬운 관계이기도 합니다. 또한, 현실적인 문제(돈, 직업)로 인해 계산적인 관계가 될 수도 있으니 순수한 마음을 잃지 않도록 주의해야 합니다.",
                "intimacy": "속궁합은 **100점 만점에 200점**입니다. 낮에는 싸우더라도 밤에는 화해하는 커플입니다. 서로에 대한 육체적인 탐닉이 강하며, 권태기가 쉽게 오지 않는 뜨거운 관계입니다.",
                "future": "결혼을 하면 **재산 증식**에 아주 유리한 커플입니다. 두 사람이 합심하면 부자가 될 수 있는 에너지가 있습니다. 다만, 상대방을 소유물로 생각하지 말고 인격체로 존중해주는 것이 결혼 생활 유지의 핵심입니다.",
                "advice": "1. **집착 금지:** 상대방의 사생활을 존중해주세요.\n2. **돈 문제 투명하게:** 금전적인 신뢰가 깨지면 관계도 끝납니다.\n3. **존중하기:** '내 말대로 해'라는 명령조의 말투를 버리세요."
            },
            "en": {
                "title": "🔥 Fatal Attraction: Passion and Control",
                "chemistry": f"Intense physical attraction exists between you. You find your partner irresistibly attractive and want to 'conquer' them. This relationship is driven by a strong desire to possess one another.",
                "conflict": f"Control is the main issue. If you try to manipulate your partner, they will feel suffocated and run away. Obsession and jealousy are major risks. Avoid becoming too transactional or calculating.",
                "intimacy": "Physical chemistry is **200/100**. You might fight during the day but make up passionately at night. Physical satisfaction is extremely high.",
                "future": "Great for building wealth together. Financial success is likely if you cooperate. The key to a lasting marriage is respecting each other as individuals, not possessions.",
                "advice": "1. **No Obsession:** Respect privacy.\n2. **Financial Transparency:** Money issues can break this bond.\n3. **Respect:** Drop the bossy attitude."
            }
        },
        "Power": {
            "score": 78,
            "ko": {
                "title": "⚖️ 존경과 긴장 사이: 나를 성장시키는 어려운 연인",
                "chemistry": f"**{pt_str}**가 **{me_str}**을 리드하고 통제하는 관계입니다. **{me_str}**은 상대방에게서 묘한 카리스마와 어른스러움을 느끼고 존경심을 갖게 됩니다. 다소 보수적이거나 격식이 있을 수 있지만, 서로의 부족한 점을 채워주며 성장하는 **'선생님과 제자'** 같은 커플입니다. (여자가 남자를 만난 경우라면 가장 전통적이고 안정적인 길연입니다.)",
                "conflict": f"**{me_str}**이 느끼기에 **{pt_str}**는 너무 깐깐하거나 보수적일 수 있습니다. 상대방의 조언이 **'지적질'**이나 **'잔소리'**로 들리기 시작하면 스트레스가 극에 달합니다. '너는 왜 맨날 나를 가르치려 들어?'라는 불만이 터져 나올 수 있습니다.",
                "intimacy": "다소 보수적이거나 일방적일 수 있습니다. 하지만 신뢰가 바탕이 된 관계라 깊고 은근한 매력이 있습니다. 스릴보다는 **안정감**이 돋보이는 속궁합입니다.",
                "future": "연애보다는 **결혼 상대로 더 좋은 궁합**입니다. 서로의 책임을 다하고 예의를 지키는 모범적인 부부가 됩니다. 다만, 너무 격식을 차리다가 정서적인 교감이 부족해질 수 있으니 가끔은 망가지는 모습도 보여주세요.",
                "advice": "1. **자존심 세우지 않기:** 상대방의 말이 쓴약이라고 생각하세요.\n2. **대화법 바꾸기:** 상대방은 부드럽게 말하고, 본인은 솔직하게 표현하세요.\n3. **규칙 정하기:** 서로 간섭하지 말아야 할 선을 정하세요."
            },
            "en": {
                "title": "⚖️ Respect & Tension: The Growth Couple",
                "chemistry": f"Your partner leads or pressures you. You feel respect and charisma from them. It's like a 'Teacher-Student' relationship where you grow together, though it might feel a bit traditional or strict.",
                "conflict": f"You might feel stressed by your partner's strictness. Their advice often sounds like criticism or lecturing to you. Resentment can build up if you feel constantly judged.",
                "intimacy": "Stable and trusting rather than wild. It provides deep emotional security and a sense of being protected.",
                "future": "Better for marriage than dating. You will be a model couple who fulfill responsibilities. Don't be too formal; allow some playfulness in the family.",
                "advice": "1. **Listen:** Their advice is for your good.\n2. **Soft Communication:** Ask them to speak gently.\n3. **Boundaries:** Set limits on how much you interfere with each other."
            }
        },
        "Resource": {
            "score": 96,
            "ko": {
                "title": "🍼 무한한 사랑: 엄마 품 같은 힐링 커플",
                "chemistry": f"**{pt_str}**가 **{me_str}**을 헌신적으로 뒷바라지해주는 관계입니다. **{me_str}**은 가만히 있어도 상대방이 알아서 챙겨주고, 이해해주고, 용서해줍니다. 마치 엄마 품에 있는 것처럼 세상에서 가장 편안한 안식처를 만난 셈입니다. 정서적인 결속력이 매우 강한 **'힐링 커플'**입니다.",
                "conflict": f"너무 편안하다 보니 **권태기**가 빨리 올 수 있습니다. **{me_str}**이 게을러지거나 상대방을 당연하게 여기는 순간 위기가 옵니다. 또한, 상대방의 사랑이 과해지면 **'집착'**이나 **'과잉보호'**로 느껴져 답답해질 수 있습니다. '나를 어린애 취급 하지 마'라고 반항할 수 있습니다.",
                "intimacy": "자극적인 쾌락보다는 **정서적인 포만감**이 큰 관계입니다. 서로를 안고만 있어도 좋은, 부드럽고 따뜻한 스킨십이 주를 이룹니다.",
                "future": "헤어지려야 헤어질 수 없는 **질긴 인연**입니다. 결혼을 하면 서로에게 없어서는 안 될 공기 같은 존재가 됩니다. 어려움이 닥쳐도 서로 의지하며 끝까지 함께할 동반자입니다.",
                "advice": "1. **감사 표현하기:** 받는 것에 익숙해지지 마세요.\n2. **긴장감 유지:** 가끔은 색다른 데이트로 설렘을 주세요.\n3. **독립심 키우기:** 상대방에게 너무 의존하지 마세요."
            },
            "en": {
                "title": "🍼 Unconditional Love: Healing Soulmates",
                "chemistry": f"Your partner supports you devotedly. You feel safe, understood, and forgiven, as if in a mother's arms. It is a healing relationship with a strong emotional bond.",
                "conflict": "Comfort can lead to boredom or laziness. You might take their love for granted. Also, their care might feel like smothering or over-protection at times.",
                "intimacy": "Emotional satisfaction is high. Gentle and warm connection.",
                "future": "Inseparable bond. Destiny partners who support each other through life.",
                "advice": "1. Express gratitude. 2. Keep the spark alive. 3. Don't be too dependent."
            }
        }
    }
    
    base_data = reports[rel]
    data = base_data[lang]
    
    return {
        "score": base_data["score"],
        "title": data['title'],
        "chemistry": data['chemistry'],
        "conflict": data['conflict'],
        "intimacy": data['intimacy'],
        "future": data['future'],
        "advice": data['advice']
    }

# ----------------------------------------------------------------
# 4. 메인 화면 UI
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("Please enter your info at Home first." if lang == "en" else "⚠️ 홈 화면에서 본인 정보를 먼저 입력해주세요.")
    if st.button("Go Home" if lang == "en" else "홈으로 이동"): st.switch_page("Home.py")
    st.stop()

u_name = st.session_state["user_name"]
u_dob = st.session_state["birth_date"]
u_gender = st.session_state.get("gender", "Male") 

ui = {
    "ko": {
        "title": "💘 프리미엄 궁합 분석",
        "sub": "두 사람의 영혼, 성격, 그리고 미래까지 꿰뚫어보는 심층 리포트 (A4 1장 분량)",
        "p_info_title": "상대방 정보 입력",
        "p_name": "상대방 이름",
        "p_dob": "상대방 생년월일",
        "p_gender": "상대방 성별",
        "lock_title": "🔒 궁합 리포트 잠금",
        "lock_desc": "결제 후 받은 라이센스 키를 입력하세요.",
        "lock_warn": "⚠️ 주의: 라이센스 키 사용 횟수가 차감됩니다.",
        "label": "구매 후 받은 라이센스 키 입력",
        "btn_unlock": "리포트 잠금 해제",
        "btn_buy_sp": "💳 단품 구매 ($10 / 3회)",
        "btn_buy_all": "🎟️ All-Access 패스 구매 ($30 / 10회)",
        "score_label": "궁합 점수",
        "btn_print": "🖨️ 리포트 인쇄하기",
        "sec_chem": "🔮 성격과 케미 (Chemistry)",
        "sec_conf": "⚔️ 갈등 포인트 (Conflict)",
        "sec_inti": "💋 속궁합 & 애정 (Intimacy)",
        "sec_fut": "💍 미래 & 결혼 (Future)",
        "sec_adv": "🚀 관계를 위한 조언 (Advice)"
    },
    "en": {
        "title": "💘 Premium Love Compatibility",
        "sub": "Deep analysis of souls, personalities, and future (Full Report).",
        "p_info_title": "Partner Information",
        "p_name": "Partner Name",
        "p_dob": "Partner DOB",
        "p_gender": "Partner Gender",
        "lock_title": "🔒 Report Locked",
        "lock_desc": "Enter the license key after purchase.",
        "lock_warn": "⚠️ Warning: This will consume 1 usage credit.",
        "label": "Enter License Key",
        "btn_unlock": "Unlock Report",
        "btn_buy_sp": "💳 Buy Single ($10 / 3 Uses)",
        "btn_buy_all": "🎟️ Buy All-Access ($30 / 10 Uses)",
        "score_label": "Compatibility Score",
        "btn_print": "🖨️ Print Report",
        "sec_chem": "🔮 Chemistry & Personality",
        "sec_conf": "⚔️ Conflict Points",
        "sec_inti": "💋 Intimacy & Love",
        "sec_fut": "💍 Future & Marriage",
        "sec_adv": "🚀 Advice for Relationship"
    }
}
t = ui[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.info(f"{t['sub']} (User: {u_name})")

# 5. 상대방 정보 입력
with st.container(border=True):
    st.subheader(t['p_info_title'])
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input(t['p_name'])
        p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1990,1,1))
    with c2:
        default_idx = 1 if u_gender == "Male" else 0
        p_gender = st.selectbox(t['p_gender'], ["Male", "Female"], index=default_idx)

# 6. 잠금 및 결제
if "unlocked_love" not in st.session_state: st.session_state["unlocked_love"] = False

# 🌟 팝업창(Dialog) 함수
@st.dialog("⚠️ Usage Limit Warning")
def show_limit_warning():
    st.warning(t['lock_warn'], icon="⚠️")
    st.write("Checking this result will deduct 1 credit from your license.")
    if st.button("I Understand & Proceed", type="primary"):
        st.rerun()

if not st.session_state["unlocked_love"]:
    with st.container(border=True):
        st.markdown(f"### {t['lock_title']}")
        st.write(t['lock_desc'])
        
        # 3회 제한 팝업 버튼
        if st.button("⚠️ Check Limit Info", type="secondary"):
            show_limit_warning()
            
        c1, c2 = st.columns(2)
        with c1: st.link_button(t['btn_buy_sp'], GUMROAD_LINK_SPECIFIC)
        with c2: st.link_button(t['btn_buy_all'], GUMROAD_LINK_ALL)
        
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock'], type="primary"):
            if not p_name:
                st.error("Please enter partner's name." if lang=="en" else "상대방 이름을 입력해주세요.")
            else:
                if key == UNLOCK_CODE:
                    st.session_state["unlocked_love"] = True
                    st.success("Developer Access Granted!")
                    st.rerun()
                try:
                    # (A) 단품 상품 확인
                    response_specific = requests.post(
                        "https://api.gumroad.com/v2/licenses/verify",
                        data={"product_permalink": PRODUCT_PERMALINK_SPECIFIC, "license_key": key}
                    )
                    data_specific = response_specific.json()

                    if data_specific.get("success"):
                        if data_specific.get("uses", 0) > 3:
                            st.error(f"🚫 Limit exceeded (Max 3 uses).")
                        else:
                            st.session_state["unlocked_love"] = True
                            st.success("Success!")
                            st.rerun()
                    else:
                        # (B) All-Access 패스 확인
                        response_all = requests.post(
                            "https://api.gumroad.com/v2/licenses/verify",
                            data={"product_permalink": PRODUCT_PERMALINK_ALL, "license_key": key}
                        )
                        data_all = response_all.json()
                        
                        if data_all.get("success"):
                            if data_all.get("uses", 0) > 10:
                                st.error(f"🚫 All-Access Pass Limit Exceeded ({data_all.get('uses')}/10)")
                            else:
                                st.session_state["unlocked_love"] = True
                                st.success("All-Access Pass Accepted!")
                                st.rerun()
                        else:
                            st.error("🚫 Invalid Key.")
                except:
                    st.error("Connection Error.")
    st.stop()

# 7. 결과 리포트
if st.session_state["unlocked_love"]:
    st.divider()
    u_info = calculate_day_gan(u_dob)
    p_info = calculate_day_gan(p_dob)
    report = get_love_report(u_info['element'], p_info['element'], u_gender, p_gender, lang)
    
    # 대결 구도
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.markdown(f"""<div class='user-card'><div style='color:#6b7280;'>ME ({u_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{u_name}</div><div style='font-size:1.2em; color:#db2777;'>{u_info[lang]} ({u_info['element']})</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-badge'>❤️</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='user-card'><div style='color:#6b7280;'>PARTNER ({p_gender})</div><div style='font-size:1.5em; font-weight:bold; color:#1f2937;'>{p_name}</div><div style='font-size:1.2em; color:#db2777;'>{p_info[lang]} ({p_info['element']})</div></div>""", unsafe_allow_html=True)

    # 메인 리포트
    html_content = f"""<div class='report-container'><div class='score-display'>{t['score_label']}: {report['score']}</div><h2 style='text-align:center; color:#831843; margin-bottom:40px;'>{report['title']}</h2><div class='section-box'><div class='section-title'>{t['sec_chem']}</div><div class='content-text'>{report['chemistry']}</div></div><div class='section-box'><div class='section-title'>{t['sec_conf']}</div><div class='content-text'>{report['conflict']}</div></div><div class='section-box'><div class='section-title'>{t['sec_inti']}</div><div class='content-text'>{report['intimacy']}</div></div><div class='section-box'><div class='section-title'>{t['sec_fut']}</div><div class='content-text'>{report['future']}</div></div><div class='section-box' style='background-color: #fdf2f8; border: 1px solid #fbcfe8;'><div class='section-title'>{t['sec_adv']}</div><div class='content-text' style='font-weight:bold; color:#be185d; white-space: pre-line;'>{report['advice']}</div></div></div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#be185d; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(190, 24, 93, 0.3);">
            {t['btn_print']}
            </button>
        </div>""", height=100
    )
