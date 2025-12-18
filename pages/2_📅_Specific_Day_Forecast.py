import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Specific Day Forecast", page_icon="📅", layout="wide")

# 🔑 [마스터 키 & 검로드 설정]
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK = "specific_day"
GUMROAD_LINK = "https://gumroad.com/l/선생님의_상품주소" 

st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
            url("https://img.freepik.com/free-vector/hand-drawn-korean-traditional-pattern-background_23-2149474585.jpg");
            background-size: cover; background-attachment: fixed; background-position: center;
        }
        .main-header {font-size: 2.2em; font-weight: bold; color: #1e293b; margin-bottom: 10px; text-align: center;}
        
        /* 리포트 스타일 고급화 */
        .report-container {
            background-color: white; padding: 40px; border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
        }
        .report-section {
            margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px dashed #cbd5e1;
        }
        .report-section:last-child { border-bottom: none; }
        
        .section-emoji { font-size: 1.5em; margin-right: 10px; vertical-align: middle; }
        .section-title { 
            font-size: 1.3em; font-weight: bold; color: #334155; 
            display: inline-block; margin-bottom: 10px; border-left: 5px solid #3b82f6; padding-left: 15px;
        }
        .content-text { 
            font-size: 1.05em; line-height: 1.8; color: #334155; text-align: justify; letter-spacing: -0.01em;
        }
        
        .user-info-box {
            background-color: #f8fafc; padding: 15px 20px; border-radius: 10px; border: 1px solid #e2e8f0;
            color: #475569; font-size: 0.95em; margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        
        .lucky-box {
            background-color: #f0f9ff; padding: 15px; border-radius: 10px; border: 1px solid #bae6fd;
            margin-top: 10px; font-weight: bold; color: #0284c7;
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
    if st.button("👈 Home" if lang=="en" else "👈 홈으로"):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 3. [초대형] 리포트 데이터
# ----------------------------------------------------------------
def get_long_report(user_elem, day_elem, lang, gender):
    
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    
    rel_type = relations.get(user_elem, {}).get(day_elem, "Same")
    
    # 🌟 긴 텍스트 데이터 (Ultra Premium)
    scenarios = {
        "Same": { # 비견/겁재
            "ko": {
                "score": 3,
                "title": "🤝 거울 속의 나를 만나는 날 (자아와 경쟁)",
                "general": "오늘은 당신과 똑같은 에너지가 우주에서 쏟아지는 날입니다. 마치 거울을 보는 것처럼 나와 비슷한 사람을 만나거나, 내 내면의 목소리가 확성기를 켠 듯 커지는 하루입니다. 평소에는 남의 의견을 잘 듣던 사람도 오늘만큼은 **'내 방식대로 할 거야!'**라는 고집이 생깁니다. 독립심과 주체성이 폭발하여 누구의 도움 없이도 혼자서 일을 처리해내는 능력이 탁월해집니다. 하지만 이 에너지가 과해지면 주변 사람들과 사소한 의견 차이로 부딪힐 수 있습니다. **'내가 맞고 네가 틀리다'**는 생각이 지배하기 쉬운 날이니, 의식적으로 한 발짝 물러서는 여유가 필요합니다.",
                "money": "재물운에서는 **'탈재(奪財)'**, 즉 재물을 빼앗길 수 있는 기운이 감돕니다. 하지만 겁먹지 마세요. 이는 '나눔'을 통해 액땜할 수 있습니다. 오늘은 혼자 이익을 독차지하려 하면 오히려 탈이 납니다. 친구가 돈을 빌려달라고 하거나, 예상치 못한 지출이 생길 수 있습니다. 이를 방지하는 최고의 방법은 **먼저 베푸는 것**입니다. 점심 식사 값을 먼저 계산하거나, 커피를 쏘세요. 내가 기분 좋게 쓴 돈은 나쁜 기운을 몰아내고 더 큰 복을 불러옵니다. 주식이나 투자는 경쟁이 치열하여 재미를 보기 힘드니 관망하는 것이 좋습니다.",
                "love_m": "**[남성의 경우]** 연애 전선에 '경쟁자'의 그림자가 보입니다. 짝사랑 중이라면 강력한 라이벌이 등장해 마음을 졸일 수 있습니다. 연인이 있다면 당신의 자존심이 세지는 날이라, 별것 아닌 일로 자존심 싸움을 하다가 냉전 상태가 될 수 있습니다. 오늘 당신이 해야 할 일은 딱 하나, **'무조건 져주는 척하기'**입니다. 이기려 들면 관계에 금이 갑니다.",
                "love_f": "**[여성의 경우]** 친구처럼 편안한 관계는 좋지만, 연인에게는 고집을 부리기 쉽습니다. 남자가 내 뜻대로 움직여주지 않으면 화가 치밀어 오를 수 있습니다. 싱글이라면 친구들과의 모임이나 동호회에서 나와 코드가 딱 맞는 사람을 만날 수 있습니다. 하지만 그 사람이 내 친구와도 썸이 있을 수 있으니 눈치 작전이 필요합니다.",
                "health": "에너지가 차고 넘쳐서 문제입니다. 가만히 앉아 있으면 좀이 쑤시고, 오히려 몸살이 날 수 있습니다. 오늘은 헬스장을 가거나 등산을 하는 등 **몸을 혹사시키다시피 움직여야** 컨디션이 좋아집니다. 다만, 경쟁심 때문에 무리하게 무게를 치거나 달리기를 하다가 근육이나 관절을 다칠 수 있으니 스트레칭은 필수입니다.",
                "action": "1. **오늘의 주문:** '그래, 그럴 수도 있지.' (고집 내려놓기)\n2. **개운 행동:** 친구나 동료에게 밥 사주기 (돈으로 액땜하기)\n3. **주의사항:** 동업 제안이나 돈 거래는 절대 금물입니다.",
                "lucky": "🕶️ 선글라스/거울, 👫 모임 장소"
            },
            "en": {
                "score": 3,
                "title": "🤝 Day of the Mirror: Strong Self & Competition",
                "general": "Today, the universe sends you energy identical to your own. It's like looking into a mirror; you may meet people very similar to you, or your inner voice will become amplified. Even if you are usually compliant, today you will feel a strong urge to do things **'My Way.'** Your independence and self-reliance are at their peak, allowing you to handle tasks without help. However, this strong ego can lead to friction. You might strongly feel **'I am right, and you are wrong.'** Consciously take a step back to avoid conflicts.",
                "money": "There is a risk of **'Wealth Loss'** today. But don't panic; you can prevent this by **'Sharing'** proactively. Trying to keep all profits to yourself will lead to trouble. Unexpected expenses may arise. The best strategy is to **spend money on others first.** Treat your colleagues to lunch or coffee. Money spent happily will ward off bad luck. Avoid high-risk investments as competition is too fierce.",
                "love_m": "**[For Men]** A shadow of a **'Rival'** looms. If you have a crush, a competitor might appear. If you are in a relationship, your heightened pride could lead to unnecessary ego battles. Your mission today is simple: **'Pretend to lose.'** Trying to win an argument today will damage the relationship.",
                "love_f": "**[For Women]** Friendly relationships are great, but you might be stubborn with your partner. You may get annoyed if he doesn't follow your lead. If single, you might meet someone who clicks with you perfectly at a social gathering. However, be aware that he might also be interested in your friend.",
                "health": "You have too much energy today. Sitting still might actually make you feel sick. You need to **move your body vigorously**—go to the gym or hike. However, be careful not to overexert yourself out of competitiveness, as this could lead to muscle injuries.",
                "action": "1. **Mantra:** 'It is what it is.' (Let go of ego)\n2. **Remedy:** Buy a meal for a friend (Spending prevents loss)\n3. **Warning:** No lending money or joint ventures today.",
                "lucky": "🕶️ Sunglasses/Mirror, 👫 Social Gatherings"
            }
        },
        "Output": { # 식상
            "ko": {
                "score": 4,
                "title": "🎨 억눌린 끼가 폭발하는 '표현'의 날",
                "general": "가슴 속에 담아두었던 말이나 아이디어가 화산처럼 분출되는 날입니다. **'표현하고 싶어 미치겠다'**는 감정이 들 수 있습니다. 머리 회전이 평소보다 2배는 빨라져서, 창의적인 기획이나 문제 해결 능력이 탁월해집니다. 평소에 답답했던 상황이 있었다면, 오늘 당신의 재치 있는 말 한마디로 상황을 역전시킬 수 있습니다. 하지만 말이 너무 많아지거나 직설적으로 나갈 수 있어, 본의 아니게 상대방에게 상처를 줄 수도 있습니다. 오늘은 당신이 주인공이 되어 무대를 휘어잡는 날이니, 자신감 있게 나를 드러내세요.",
                "money": "**'재주는 곰이 부리고 돈은 되놈이 번다'**는 속담이 있지만, 오늘은 **재주 부린 곰(=당신)이 돈까지 다 가져갑니다.** 당신의 기술, 말솜씨, 아이디어가 곧바로 수익으로 연결됩니다. 프리랜서, 영업직, 예체능 종사자에게는 대박의 기운이 있습니다. 다만, 기분이 너무 들뜨는 바람에 **'충동구매'**라는 함정에 빠질 수 있습니다. '이건 나를 위한 투자야!'라고 합리화하며 비싼 물건을 긁을 수 있으니 지갑 단속이 필요합니다.",
                "love_m": "**[남성의 경우]** 당신의 유머 감각과 센스가 폭발하여 여심을 사로잡습니다. 좋아하는 이성에게 적극적으로 대시하거나 이벤트를 해주기에 최고의 날입니다. 다만, 분위기에 취해 지키지 못할 약속을 하거나, 가벼운 언행으로 점수를 깎아먹지 않도록 주의하세요.",
                "love_f": "**[여성의 경우]** 모성애가 발동하는 날입니다. 남자친구나 남편을 아이 다루듯 챙겨주려 합니다. 하지만 이것이 지나치면 **'잔소리 폭격'**이 될 수 있습니다. 오늘은 남자를 가르치려 들거나 지적하지 말고, 칭찬으로 조련하는 것이 훨씬 효과적입니다. 자녀가 있다면 자녀와 관련된 기쁜 일이 생깁니다.",
                "health": "배터리 소모가 극심한 날입니다. 정신없이 에너지를 쏟아내다 보면 저녁에는 **방전(Burn-out)** 상태가 될 수 있습니다. 특히 소화기관이 예민해지거나, 말을 너무 많이 해서 목이 쉴 수 있습니다. 달콤한 디저트로 당을 충전하고, 저녁에는 따뜻한 차를 마시며 목을 보호하세요.",
                "action": "1. **오늘의 주문:** '나는 아티스트다.' (창의성 발휘)\n2. **개운 행동:** 노래방 가기, 일기 쓰기, 블로그 포스팅\n3. **주의사항:** 실언(말실수) 주의. 세 번 생각하고 말하기.",
                "lucky": "🎤 마이크/노트, 🍰 달콤한 디저트, 🎨 미술관"
            },
            "en": {
                "score": 4,
                "title": "🎨 Day of Expression: Unleash Your Talent",
                "general": "Ideas and words you've kept inside will erupt like a volcano today. You will feel an intense urge to **'Express Yourself.'** Your brain will work twice as fast, enhancing your creativity and problem-solving skills. If you've felt stuck, your wit can turn the situation around today. However, be careful not to talk too much or be too blunt, as you might unintentionally hurt others. Today, you are the main character on stage—show yourself off with confidence.",
                "money": "Usually, talent doesn't always equal money, but today **your talent brings cash immediately.** Your skills, speech, and ideas will translate directly into profit. This is a jackpot day for freelancers, sales, and creatives. However, beware of the **'Impulse Buying'** trap. You might rationalize buying expensive items by saying, 'This is an investment in myself.' Watch your wallet.",
                "love_m": "**[For Men]** Your humor and sense of style will captivate women. It's the best day to pursue a crush or plan a surprise event. Just be careful not to make promises you can't keep or appear too lighthearted, which could hurt your reputation.",
                "love_f": "**[For Women]** Your maternal instincts kick in. You might want to take care of your partner like a child. However, this can turn into **'Nagging.'** Avoid lecturing or correcting him today; instead, use praise to guide him. Good news related to children is likely.",
                "health": "High battery consumption day. You might face **'Burn-out'** in the evening after pouring out so much energy. Your digestion might be sensitive, or you might lose your voice from talking too much. Recharge with sweet desserts and protect your throat with warm tea.",
                "action": "1. **Mantra:** 'I am an Artist.'\n2. **Remedy:** Karaoke, Writing a diary, Posting on social media\n3. **Warning:** Watch your tongue. Think three times before speaking.",
                "lucky": "🎤 Microphone/Notebook, 🍰 Dessert, 🎨 Art Gallery"
            }
        },
        "Wealth": { # 재성
            "ko": {
                "score": 5,
                "title": "💰 결과가 눈앞에 보이는 '수확'의 날",
                "general": "뜬구름 잡는 소리는 그만! 오늘은 철저하게 **'현실적'**이고 **'계산적'**인 하루입니다. 무엇이 나에게 이득이 되고 손해가 되는지 본능적으로 계산기가 두들겨지는 날입니다. 그동안 노력했던 일들에 대한 **확실한 보상**이 주어집니다. 막연했던 목표가 구체적인 성과로 나타나며, 일의 마무리가 깔끔하게 됩니다. 감정보다는 이성이 앞서는 날이므로, 중요한 결정이나 협상을 하기에 더할 나위 없이 좋습니다. 오늘은 과정보다 '결과'가 당신을 증명해 줄 것입니다.",
                "money": "**금전운 최상(Best)!** 하늘에서 돈비가 내리는 형국입니다. 예상치 못한 보너스, 밀린 돈을 받거나, 투자 수익이 발생할 수 있습니다. 단순히 돈이 들어오는 것뿐만 아니라, 돈을 **'잘 쓰는'** 운도 좋습니다. 평소 사고 싶었던 물건을 최저가에 사거나, 가성비 좋은 투자를 할 수 있습니다. 사업가라면 오늘은 매출 기록을 경신할 수 있는 날이니 매장에 집중하세요. 복권을 한 장 사보는 것도 오늘의 재미있는 이벤트가 될 것입니다.",
                "love_m": "**[남성의 경우]** 명리학에서 재성(돈)은 곧 **'여자'**를 의미합니다. 즉, 돈과 여자가 함께 들어오는 날입니다. 평소보다 이성에게 인기가 많아지며, 소개팅을 하면 미모와 능력을 겸비한 여성을 만날 확률이 높습니다. 썸녀가 있다면 오늘이 바로 고백 타이밍입니다.",
                "love_f": "**[여성의 경우]** 남자를 볼 때 **'능력'**과 **'현실적인 조건'**을 따지게 됩니다. 감성에 호소하는 남자보다는, 비전이 확실하고 내 삶에 도움이 될 만한 남자에게 끌립니다. 오늘은 데이트할 때 맛집 투어나 쇼핑 등 오감을 만족시키는 코스가 행운을 불러옵니다.",
                "health": "몸이 가볍고 컨디션이 좋습니다. 하지만 지나치게 일이나 결과에 몰두하다 보면 **신경성 두통**이나 눈의 피로가 올 수 있습니다. '돈 세다가 밤새는 줄 모른다'는 말처럼, 과로하기 쉬우니 중간중간 휴식을 챙기세요. 하체 운동을 하면 재물운을 담는 그릇이 더 튼튼해집니다.",
                "action": "1. **오늘의 주문:** '나는 부자다.' (풍요의 마인드)\n2. **개운 행동:** 지갑 정리하기, 가계부 쓰기, 복권 구매\n3. **주의사항:** 돈 자랑 하지 말기. 조용히 챙길 것.",
                "lucky": "💳 지갑/현금, 🏦 은행/백화점, 🍗 고기/맛집"
            },
            "en": {
                "score": 5,
                "title": "💰 Day of Harvest: Results Are in Sight",
                "general": "No more daydreaming! Today is strictly **'Realistic'** and **'Calculated.'** You will instinctively know exactly what benefits you and what doesn't. **Tangible rewards** for your past efforts will appear. Vague goals turn into concrete achievements. Reason rules over emotion today, making it perfect for important decisions or negotiations. Today, the 'Result' proves your worth more than the process.",
                "money": "**Financial Luck: Best!** It's raining money. Unexpected bonuses, overdue payments, or investment returns are likely. It's not just about earning; you will also **spend wisely.** You might find a great deal on something you've wanted. Business owners should focus on sales as records could be broken today. Buying a lottery ticket could be a fun little event.",
                "love_m": "**[For Men]** In metaphysics, 'Wealth' also represents **'Women.'** Money and romance come together today. You will be more popular than usual. Blind dates are likely to introduce you to beautiful and capable women. If you have a crush, today is the day to confess.",
                "love_f": "**[For Women]** You will judge men based on **'Capability'** and **'Conditions.'** Instead of emotional types, you'll be drawn to men with clear visions who can help your life. For dates, sensory experiences like gourmet tours or shopping will bring good luck.",
                "health": "Your body feels light. However, obsessing over results can cause **Tension Headaches** or eye strain. Like the saying 'Working too hard to count money,' beware of overwork. Lower body exercises will strengthen your capacity to hold wealth.",
                "action": "1. **Mantra:** 'I am Abundant.'\n2. **Remedy:** Organize your wallet, Check finances, Buy lottery\n3. **Warning:** Don't show off your money. Keep it quiet.",
                "lucky": "💳 Wallet/Cash, 🏦 Bank/Mall, 🍗 Fine Dining"
            }
        },
        "Power": { # 관성
            "ko": {
                "score": 2,
                "title": "⚖️ 왕관의 무게를 견디는 '명예'의 날",
                "general": "오늘은 공기마저 무겁게 느껴질 수 있습니다. **책임감, 의무, 규칙**이라는 단어가 당신을 둘러쌉니다. 상사의 지시가 내려오거나, 마감 기한을 맞춰야 하는 등 외부의 압박이 들어옵니다. 하지만 이것은 나쁜 것이 아닙니다. 다이아몬드가 압력을 받아 만들어지듯, 오늘 당신이 겪는 스트레스는 당신을 **'리더'**로 만들어주는 과정입니다. 힘들어도 도망가지 않고 묵묵히 해냈을 때, 주변의 인정과 명예, 그리고 '감투'가 주어집니다. 오늘은 '나'를 죽이고 '조직'이나 '대의'를 따를 때 빛이 납니다.",
                "money": "현금이 들어오는 날이라기보다는, **'명함 값'**이 올라가는 날입니다. 승진을 하거나 좋은 부서로 이동하는 운입니다. 오히려 돈은 나갈 수 있습니다. 세금, 공과금, 범칙금, 회비 등 **의무적으로 내야 할 돈**이 생길 수 있습니다. 또한, 체면치레를 하느라 한턱 쏘는 일이 생길 수 있는데, 이는 미래를 위한 투자라고 생각하는 것이 마음 편합니다. 법적인 문제나 서류상의 실수가 없도록 꼼꼼히 체크하세요.",
                "love_m": "**[남성의 경우]** 일에 치여 연인에게 소홀해지기 쉽습니다. 혹은 자녀 문제로 골머리를 앓을 수 있습니다. 밖에서 받은 스트레스를 연인에게 풀지 않도록 각별히 조심해야 합니다. '나 힘드니까 건드리지 마'라는 태도는 싸움을 부릅니다.",
                "love_f": "**[여성의 경우]** **남자가 들어오는 날**입니다. 그것도 아주 강력하고 카리스마 있는 남자가 나타납니다. 나를 리드해주고 보호해주는 '상남자' 스타일일 확률이 높습니다. 하지만 연인이 있다면, 상대방이 나를 통제하거나 가르치려 들어 답답함을 느낄 수 있습니다. 오늘은 싸우면 백전백패니 져주는 게 낫습니다.",
                "health": "스트레스 지수가 최고조에 달합니다. 어깨와 뒷목이 뻣뻣하게 굳는 **근육통**이나 편두통을 조심하세요. 긴장감 때문에 소화가 잘 안 될 수 있습니다. 오늘은 격렬한 운동보다는 요가나 명상, 반신욕으로 몸의 긴장을 풀어주는 것이 생명입니다.",
                "action": "1. **오늘의 주문:** '이 또한 지나가리라.' (인내심)\n2. **개운 행동:** 넥타이/정장 착용, 시계 차기, 규칙 준수\n3. **주의사항:** 신호 위반, 지각 금지 (관재수 주의).",
                "lucky": "👔 시계/정장, 🏛️ 관공서/사무실, 🧘 명상"
            },
            "en": {
                "score": 2,
                "title": "⚖️ Day of Honor: Bearing the Weight of the Crown",
                "general": "The air might feel heavy today. Words like **Responsibility, Duty, and Rules** surround you. External pressures, such as boss's orders or deadlines, will weigh on you. But this isn't bad. Like a diamond formed under pressure, today's stress is forging you into a **Leader.** If you endure without running away, recognition and honor await. Today, shine by putting the 'Organization' or 'Greater Good' above 'Self.'",
                "money": "It's not a day for cash flow, but for raising your **'Reputation Value.'** Promotion or moving to a better position is likely. Money might actually leave your pocket. Mandatory expenses like taxes, bills, fines, or dues may arise. You might spend money to save face; treat it as an investment for the future. Check legal matters and documents carefully to avoid mistakes.",
                "love_m": "**[For Men]** You might neglect your partner due to work overload. Issues with children could also cause headaches. Be extremely careful not to vent your work stress on your partner. Saying 'I'm tired, leave me alone' will invite a fight.",
                "love_f": "**[For Women]** **Men are entering your life.** A powerful, charismatic man is likely to appear—someone who can protect and lead you. However, if you have a partner, he might try to control or lecture you, causing frustration. Fighting back today guarantees defeat; just let him win.",
                "health": "Stress levels peak. Beware of **stiff neck/shoulders** or migraines. Tension might cause indigestion. Instead of intense exercise, focus on relaxing your body with yoga, meditation, or a warm bath.",
                "action": "1. **Mantra:** 'This too shall pass.' (Patience)\n2. **Remedy:** Wear a watch/suit, Follow rules strictly\n3. **Warning:** No traffic violations or lateness (Avoid legal trouble).",
                "lucky": "👔 Watch/Suit, 🏛️ Government Office, 🧘 Meditation"
            }
        },
        "Resource": { # 인성
            "ko": {
                "score": 4,
                "title": "📚 사랑과 지혜가 충전되는 '힐링'의 날",
                "general": "마치 엄마 품에 안긴 듯 편안하고 안정적인 하루입니다. 내가 굳이 애쓰고 뛰어다니지 않아도, 가만히 있으면 주변에서 알아서 챙겨주고 도와줍니다. **'인복(人福)'**이 터지는 날입니다. 활동적인 에너지보다는 **정적인 에너지**가 강합니다. 새로운 일을 벌이기보다는 기존의 것을 점검하고, 공부하고, 계획을 세우기에 최적입니다. 직감과 영감이 발달하여 꿈자리가 사납거나 기막힌 아이디어가 떠오를 수도 있습니다. 오늘은 '속도'보다는 '방향'을 고민하는 시간입니다.",
                "money": "당장 현금이 도는 운은 아니지만, **'문서운'**이 대길합니다. 부동산 계약, 전세 계약, 중요한 결재, 라이센스 취득 등 서류상의 이득이 따릅니다. 지금 당장은 돈이 묶이는 것처럼 보여도, 훗날 큰 자산이 되어 돌아올 문서를 잡는 날입니다. 자기 계발을 위해 책을 사거나 강의를 듣는 비용은 아끼지 마세요. 부모님이나 윗사람으로부터 용돈이나 선물을 받을 수도 있습니다.",
                "love_m": "**[남성의 경우]** 연인에게 기대고 싶고 위로받고 싶은 마음이 커집니다. 모성애가 강한 여성을 만나거나, 연인이 나를 엄마처럼 살뜰히 챙겨줍니다. 오늘은 데이트 코스를 짜느라 머리 쓰지 말고, 상대방이 하자는 대로 따라가는 게 편합니다.",
                "love_f": "**[여성의 경우]** 사랑받는 날입니다. 공주님 대접을 받을 수 있습니다. 상대방이 나의 기분을 세심하게 살피고 배려해줍니다. 소개팅을 한다면 예의 바르고 학식이 깊은, 배울 점이 많은 남자가 나옵니다.",
                "health": "몸이 물 먹은 솜처럼 처지고 나른해질 수 있습니다. 이는 병이 아니라 **'쉬어가라'**는 신호입니다. 억지로 운동을 하려 하지 말고, 오늘은 낮잠을 자거나 마사지를 받으며 푹 쉬는 것이 최고의 보약입니다. 소화 기능이 느려질 수 있으니 과식은 피하세요.",
                "action": "1. **오늘의 주문:** '나는 사랑받기 위해 태어났다.'\n2. **개운 행동:** 독서, 명상, 부모님께 안부 전화\n3. **주의사항:** 게으름 주의. 생각만 하다가 실행 못 할 수 있음.",
                "lucky": "📚 책/도서관, ☕ 따뜻한 차, 🛌 침대/휴식"
            },
            "en": {
                "score": 4,
                "title": "📚 Day of Healing: Recharge with Love & Wisdom",
                "general": "A day as comfortable as being in a mother's arms. Even if you don't strive hard, people around you will take care of you. **'People Luck'** is at its best. **Static energy** dominates over active energy. It's optimal for reviewing, studying, and planning rather than starting new things. Your intuition is heightened; pay attention to your dreams or sudden inspirations. Focus on 'Direction' rather than 'Speed' today.",
                "money": "Cash might not flow immediately, but **'Document Luck'** is excellent. Great for real estate contracts, signing papers, or acquiring licenses. It's a day to grab documents that will become valuable assets later. Don't hesitate to spend on books or courses for self-improvement. You might also receive allowance or gifts from parents or elders.",
                "love_m": "**[For Men]** You'll want to lean on your partner for comfort. You might meet a nurturing woman, or your partner will take care of you like a mother. Don't stress over planning dates; just follow her lead today.",
                "love_f": "**[For Women]** You are loved. Expect to be treated like a princess. Your partner will be attentive to your feelings. If you have a blind date, expect a polite, educated man with much to offer.",
                "health": "Your body might feel heavy and lethargic. This isn't sickness but a signal to **'Rest.'** Don't force exercise; a nap or massage is the best medicine today. Avoid overeating as digestion might be slow.",
                "action": "1. **Mantra:** 'I am born to be loved.'\n2. **Remedy:** Reading, Meditation, Call parents\n3. **Warning:** Beware of laziness. Too much thinking, no action.",
                "lucky": "📚 Book/Library, ☕ Warm Tea, 🛌 Bed/Rest"
            }
        }
    }
    
    # 🌟 데이터 추출 및 매핑
    data = scenarios[rel_type][lang]
    final_love = data["love_m"] if gender == "Male" else data["love_f"]
    
    return {
        "title": data["title"],
        "score": data["score"],
        "general": data["general"],
        "money": data["money"],
        "love": final_love,
        "health": data["health"],
        "action": data["action"],
        "lucky": data["lucky"]
    }

# ----------------------------------------------------------------
# 4. 메인 화면 UI
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("⚠️ 홈 화면에서 먼저 정보를 입력해주세요.")
    if st.button("홈으로 이동"): st.switch_page("Home.py")
    st.stop()

user_name = st.session_state["user_name"]
birth_date = st.session_state["birth_date"]
user_gender = st.session_state.get("gender", "Male") 

ui = {
    "ko": {
        "title": "📅 특정일 운세 정밀 분석",
        "sub": "심리학과 명리학이 만난 프리미엄 심층 리포트 (A4 1장 분량)",
        "user_info": f"👤 **분석 대상:** {user_name}님 ({user_gender} / {birth_date})",
        "lock_msg": "🔒 프리미엄 리포트 잠금 ($10)",
        "label": "구매 후 받은 라이센스 키 입력",
        "btn_unlock": "리포트 잠금 해제",
        "btn_buy": "💳 프리미엄 리포트 구매 ($10)",
        "target_date": "분석하고 싶은 날짜 (D-Day)",
        "btn_analyze": "상세 운세 확인하기",
        "print": "🖨️ 리포트 인쇄하기"
    },
    "en": {
        "title": "📅 Specific Day: Deep Report",
        "sub": "Premium In-depth Report combining Psychology & Metaphysics.",
        "user_info": f"👤 **User:** {user_name} ({user_gender} / {birth_date})",
        "lock_msg": "🔒 Premium Report Locked ($10)",
        "label": "Enter License Key",
        "btn_unlock": "Unlock Report",
        "btn_buy": "💳 Buy Premium Report ($10)",
        "target_date": "Target Date (D-Day)",
        "btn_analyze": "Analyze Detail",
        "print": "🖨️ Print Report"
    }
}
t = ui[lang]

section_titles = {
    "ko": {
        "gen": "심리 & 총평 (Psychology & Flow)",
        "mon": "재물 & 커리어 (Money & Career)",
        "lov": "사랑 & 인간관계 (Love & Relationship)",
        "hea": "건강 & 컨디션 (Health & Condition)",
        "act": "행동 지침 & 개운법 (Action Plan)",
        "luc": "오늘의 행운 (Lucky Items)"
    },
    "en": {
        "gen": "Psychology & General Flow",
        "mon": "Wealth & Career",
        "lov": "Love & Relationships",
        "hea": "Health & Condition",
        "act": "Action Plan",
        "luc": "Lucky Items"
    }
}
st_t = section_titles[lang]

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)

# 🔒 [잠금 로직]
if "unlocked_specific" not in st.session_state: st.session_state["unlocked_specific"] = False

if not st.session_state["unlocked_specific"]:
    with st.container(border=True):
        st.info(t['sub'])
        st.markdown(f"<div class='user-info-box'>{t['user_info']}</div>", unsafe_allow_html=True)
        st.write(f"### {t['lock_msg']}")
        st.link_button(t['btn_buy'], GUMROAD_LINK)
        st.markdown("---")
        key = st.text_input(t['label'], type="password")
        
        if st.button(t['btn_unlock']):
            if key == UNLOCK_CODE:
                st.session_state["unlocked_specific"] = True
                st.success("Master Key Accepted!")
                st.rerun()
            try:
                response = requests.post(
                    "https://api.gumroad.com/v2/licenses/verify",
                    data={"product_permalink": PRODUCT_PERMALINK, "license_key": key}
                )
                data = response.json()
                if data.get("success"):
                    if data.get("uses", 0) > 3:
                        st.error("🚫 Limit exceeded (Max 3 uses).")
                    else:
                        st.session_state["unlocked_specific"] = True
                        st.success("Success!")
                        st.rerun()
                else:
                    st.error("🚫 Invalid Key.")
            except:
                st.error("Connection Error.")
    st.stop()

# 🔓 [메인 리포트 화면]
with st.container():
    st.markdown(f"<div class='user-info-box'>{t['user_info']}</div>", unsafe_allow_html=True)
    col_center, _ = st.columns([1, 2])
    with col_center:
        target_date = st.date_input(t['target_date'], value=date.today(), min_value=date.today())

    if st.button(t['btn_analyze'], type="primary"):
        user_info = calculate_day_gan(birth_date)
        target_info = calculate_day_gan(target_date)
        
        # 👇 거대해진 리포트 데이터 가져오기
        report = get_long_report(user_info['element'], target_info['element'], lang, user_gender)
        
        st.divider()
        st.markdown(f"<h2 style='text-align:center; color:#334155;'>📅 {target_date.strftime('%Y-%m-%d')} Analysis Report</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 0.5, 1])
        with c1: 
            st.markdown(f"<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:15px; border:1px solid #e2e8f0;'><b>ME</b><br><span style='font-size:1.8em;'>{user_info[lang]}</span><br>({user_info['element']})</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div style='text-align:center; font-size:2em; padding-top:25px; color:#cbd5e1;'>VS</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:15px; border:1px solid #e2e8f0;'><b>DAY</b><br><span style='font-size:1.8em;'>{target_info[lang]}</span><br>({target_info['element']})</div>", unsafe_allow_html=True)

        st.write("") 
        
        score = report['score']
        stars = "⭐" * score + "🌑" * (5 - score)
        
        # 👇 HTML 들여쓰기 완전 제거 (화면 깨짐 방지: 한 줄로 작성)
        html_content = f"""<div class='report-container'><div style='text-align:center; margin-bottom:40px;'><div style='font-size:2em; color:#f59e0b; letter-spacing: 5px;'>{stars}</div><h1 style='color:#1e293b; margin-top: 15px; font-size: 2em; line-height: 1.3;'>{report['title']}</h1></div><div class='report-section'><div class='section-title'><span class='section-emoji'>🔮</span>{st_t['gen']}</div><div class='content-text'>{report['general']}</div></div><div class='report-section'><div class='section-title'><span class='section-emoji'>💰</span>{st_t['mon']}</div><div class='content-text'>{report['money']}</div></div><div class='report-section'><div class='section-title'><span class='section-emoji'>❤️</span>{st_t['lov']}</div><div class='content-text'>{report['love']}</div></div><div class='report-section'><div class='section-title'><span class='section-emoji'>💪</span>{st_t['hea']}</div><div class='content-text'>{report['health']}</div></div><div class='report-section'><div class='section-title'><span class='section-emoji'>🚀</span>{st_t['act']}</div><div class='content-text' style='white-space: pre-line; font-weight:bold; color:#0f172a;'>{report['action']}</div><div class='lucky-box'><div class='section-title' style='font-size:1.1em; border:none; margin-bottom:5px;'>🍀 {st_t['luc']}</div><div class='content-text'>{report['lucky']}</div></div></div></div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)

        st.write("")
        components.html(
            f"""<script>function printParent() {{ window.parent.print(); }}</script>
            <div style="text-align:center;">
                <button onclick="printParent()" style="background-color:#475569; color:white; border:none; padding:15px 30px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                {t['print']}
                </button>
            </div>""", height=100
        )
