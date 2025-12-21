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
        /* 🖨️ 프린트 전용 스타일 (사이드바 숨김) */
        @media print {
            section[data-testid="stSidebar"], header, footer {
                display: none !important;
            }
            .stApp {
                background: white !important; /* 잉크 절약을 위해 흰 배경 */
                color: black !important; /* 글자는 검은색 */
            }
            .main .block-container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            .card, .vs-box {
                border: 1px solid #ccc !important;
                background: white !important;
                color: black !important;
                box-shadow: none !important;
            }
            h1, h2, h3, h4, p, div, span {
                color: black !important;
                text-shadow: none !important;
            }
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

    # 🌟 6개 국어 프리미엄 궁합 데이터 (풍성한 버전)
    reports = {
        "Same": { # 비견 (거울/친구)
            "score": 85,
            "ko": {
                "t": "🤝 거울 속의 연인: 운명적 동질감과 자존심 대결",
                "c": "마치 잃어버린 반쪽을 찾은 듯 대화 코드, 웃음 포인트, 심지어 싫어하는 것까지 똑같습니다. 말하지 않아도 통하는 '텔레파시 커플'이자, 세상에서 가장 친한 친구 같은 연인입니다.",
                "f": "하지만 '너무 똑같다'는 게 함정입니다. 둘 다 고집이 세서 한 번 싸우면 '네가 먼저 사과해'라며 냉전을 벌입니다. 상대에게서 나의 단점을 발견할 때 짜증을 느끼기도 합니다.",
                "i": "속궁합 90점. 친구처럼 장난치듯 시작해 뜨거운 열정으로 변합니다. 서로의 몸과 마음 상태를 누구보다 잘 알기 때문에 만족도가 높습니다.",
                "a": "1. 자존심 죽이기: 이겨봤자 상처만 남습니다.\n2. 먼저 사과하기: '미안해' 한 마디면 해결됩니다.\n3. 친구 같은 데이트: 활동적인 취미를 함께 하세요."
            },
            "en": {
                "t": "🤝 Mirror Couple: Twin Souls with Ego Clashes",
                "c": f"You feel an instant connection like finding a lost twin. You share the same humor and values. A telepathic connection exists between you two. You are best friends and lovers.",
                "f": f"Being too similar is the trap. Both have strong egos and refuse to back down. You might hate seeing your own flaws reflected in {O}. Arguments often stem from trivial pride issues.",
                "i": "Intimacy Score: 90. Starts playful like friends and ends passionate. You intuitively know what the other wants without needing words.",
                "a": "1. Drop the Ego: Winning an argument hurts the relationship.\n2. Apologize First: A simple 'I'm sorry' works magic.\n3. Active Dates: Enjoy hobbies together."
            },
            "fr": {
                "t": "🤝 Couple Miroir : Âmes Sœurs et Choc des Egos",
                "c": "Une connexion instantanée, comme si vous retrouviez un jumeau perdu. Vous partagez le même humour et les mêmes valeurs. Vous êtes à la fois meilleurs amis et amants passionnés.",
                "f": "Le piège est d'être trop similaires. Vous avez tous deux un ego fort et refusez de céder. Les disputes peuvent se transformer en guerre froide car personne ne veut s'excuser en premier.",
                "i": "Intimité : 90/100. Cela commence de manière ludique et finit passionnément. Vous devinez intuitivement les désirs de l'autre.",
                "a": "1. Mettez l'ego de côté.\n2. Excusez-vous en premier.\n3. Partagez des activités ludiques."
            },
            "es": {
                "t": "🤝 Pareja Espejo: Almas Gemelas y Choque de Egos",
                "c": "Sientes una conexión instantánea, como encontrar a un gemelo perdido. Comparten el mismo humor y valores. Son mejores amigos y amantes apasionados al mismo tiempo.",
                "f": "Ser demasiado similares es la trampa. Ambos tienen egos fuertes y se niegan a ceder. Las discusiones pueden convertirse en guerras frías porque nadie quiere disculparse primero.",
                "i": "Intimidad: 90/100. Empieza como un juego y termina con pasión. Sabes intuitivamente lo que el otro quiere.",
                "a": "1. Deja el ego a un lado.\n2. Discúlpate primero.\n3. Disfruten de pasatiempos juntos."
            },
            "ja": {
                "t": "🤝 鏡の中の恋人：運命的なシンクロと自我の衝突",
                "c": "まるで失われた片割れを見つけたかのように、笑いのツボや価値観が同じです。言葉にしなくても通じ合うテレパシーのような関係で、親友であり恋人です。",
                "f": "しかし「似すぎている」のが罠です。お互いに頑固で、一度喧嘩になると「そっちが先に謝って」と冷戦状態になりがちです。相手に自分の欠点を見てイライラすることもあります。",
                "i": "相性90点。友達のようにふざけ合って始まり、情熱的に燃え上がります。相手が何を求めているか本能的にわかります。",
                "a": "1. プライドを捨てる：勝っても傷が残るだけです。\n2. 先に謝る：「ごめん」の一言が魔法です。\n3. アクティブなデート：趣味を共有しましょう。"
            },
            "zh": {
                "t": "🤝 镜中恋人：灵魂伴侣与自尊心的对决",
                "c": "就像找到了失散的另一半，笑点和价值观都惊人地相似。你们既是最好的朋友，也是热情的恋人，拥有不用言语也能相通的默契。",
                "f": "但“太像了”也是陷阱。两人的自尊心都很强，一旦吵架绝不退让。你可能会在对方身上看到自己的缺点而感到烦躁。",
                "i": "亲密度90分。像朋友一样嬉闹开始，以激情结束。本能地知道对方想要什么。",
                "a": "1. 放下自尊：赢了争吵输了感情。\n2. 先道歉：一句“对不起”能解决大问题。\n3. 共同爱好：一起享受活跃的约会。"
            }
        },
        "Output": { # 식상 (헌신/표현)
            "score": 92,
            "ko": {
                "t": "💖 헌신적인 사랑: 아낌없이 주는 나무와 꽃",
                "c": "당신이 상대방을 자식처럼 예뻐하고 챙겨주는 관계입니다. 상대방은 당신의 무한한 사랑 속에서 안정감을 느끼고, 당신을 전적으로 의지하게 됩니다. 주는 기쁨과 받는 행복이 조화를 이룹니다.",
                "f": "'내가 이만큼 해줬는데 너는 왜?'라는 보상 심리가 생기는 순간 서운함이 폭발합니다. 또한 당신의 과도한 관심이 상대에게는 '잔소리'나 '통제'로 느껴질 수 있습니다.",
                "i": "침대에서도 당신이 리드하고 봉사하는 형태입니다. 상대방의 만족을 위해 최선을 다하며, 거기서 기쁨을 느낍니다. 로맨틱한 분위기가 강합니다.",
                "a": "1. 기대하지 않기: 대가를 바라지 말고 베푸세요.\n2. 잔소리 줄이기: 사랑이라는 이름으로 통제하지 마세요.\n3. 표현 요구하기: 고맙다는 말을 자주 해달라고 하세요."
            },
            "en": {
                "t": "💖 Devoted Love: The Giver and The Receiver",
                "c": f"You care for {O} like a parent cares for a child. Unconditional love flows from you, and {s} feels secure and cherished. Ideally, the giver finds joy in giving, and the receiver feels deeply loved.",
                "f": f"Issues arise when you burn out. Expecting an equal return leads to resentment. Also, your care can turn into nagging, making {O} feel suffocated.",
                "i": "You lead and serve in bed. It is a highly emotional and romantic connection where you derive pleasure from satisfying your partner.",
                "a": "1. Don't Expect Return: Give without strings attached.\n2. Reduce Nagging: Care, don't control.\n3. Ask for Appreciation: Remind {O} to say 'Thank you'."
            },
            "fr": {
                "t": "💖 Amour Dévoué : L'Arbre qui Donne",
                "c": "Vous prenez soin de votre partenaire comme un parent. Vous offrez un amour inconditionnel et il/elle se sent en sécurité. L'équilibre idéal entre donner et recevoir.",
                "f": "La rancœur surgit si vous attendez un retour égal à vos efforts. De plus, vos soins peuvent être perçus comme des critiques étouffantes.",
                "i": "Vous dirigez et servez. C'est une connexion très émotionnelle où vous prenez plaisir à satisfaire l'autre.",
                "a": "1. Donnez sans attendre de retour.\n2. Moins de reproches, plus de soutien.\n3. Demandez de la reconnaissance."
            },
            "es": {
                "t": "💖 Amor Devoto: El Dador y el Receptor",
                "c": "Cuidas a tu pareja como un padre a un hijo. Das amor incondicional y él/ella se siente seguro/a. El equilibrio ideal entre dar y recibir.",
                "f": "El resentimiento surge si esperas una retribución igual. Además, tus cuidados pueden sentirse como regaños asfixiantes.",
                "i": "Tú diriges y sirves en la intimidad. Obtienes placer al satisfacer a tu pareja.",
                "a": "1. Da sin esperar nada a cambio.\n2. Cuida, no controles.\n3. Pide agradecimiento verbal."
            },
            "ja": {
                "t": "💖 献身的な愛：惜しみなく与える関係",
                "c": "あなたが相手を子供のように可愛がり、世話を焼く関係です。相手はあなたの無限の愛の中で安心感を感じ、全面的に頼るようになります。",
                "f": "「こんなにしてあげたのに」という見返りを求めると辛くなります。また、過度な関心は相手にとって「小言」や「束縛」に感じられることがあります。",
                "i": "あなたがリードし、奉仕する形です。相手を満足させることに喜びを感じます。ロマンチックな雰囲気が強いです。",
                "a": "1. 見返りを期待しない：無条件に愛しましょう。\n2. 小言を減らす：愛という名で支配しないでください。\n3. 感謝を求める：「ありがとう」と言ってもらいましょう。"
            },
            "zh": {
                "t": "💖 奉献之爱：无私给予的大树",
                "c": "你像照顾孩子一样照顾对方。对方在你的无限关爱中感到安全并完全依赖你。施与受的完美平衡。",
                "f": "如果你期待同等的回报，就会产生怨恨。此外，过度的关心可能会被对方视为“唠叨”或“控制”。",
                "i": "你在床上主导并服务对方。你从满足伴侣中获得快乐，浪漫氛围浓厚。",
                "a": "1. 不求回报：无条件地付出。\n2. 少唠叨：是关心而不是控制。\n3. 要求表达：让对方多说谢谢。"
            }
        },
        "Wealth": { # 재성 (소유/열정)
            "score": 88,
            "ko": {
                "t": "🔥 치명적인 매력: 소유욕과 주도권의 줄다리기",
                "c": "서로에게 강렬한 성적 매력을 느낍니다. '내 것으로 만들고 싶다'는 정복욕이 사랑의 원동력이 됩니다. 첫눈에 반했거나 만나는 순간 스파크가 튀었을 확률이 높습니다.",
                "f": "핵심은 '통제'입니다. 당신이 상대를 조종하려 들면 상대는 숨이 막혀 도망치고 싶어 합니다. 집착과 의심이 싹트기 쉬우며, 돈 문제로 계산적인 관계가 될 수도 있습니다.",
                "i": "속궁합 200점! 낮에는 싸워도 밤에는 화해하는 커플입니다. 서로에 대한 육체적 탐닉이 강해 권태기가 쉽게 오지 않습니다.",
                "a": "1. 집착 금지: 사생활을 존중해주세요.\n2. 돈 문제 투명하게: 금전적 신뢰가 중요합니다.\n3. 존중하기: 명령조의 말투를 버리세요."
            },
            "en": {
                "t": "🔥 Fatal Attraction: Passion and Control",
                "c": f"Intense physical attraction exists. You want to 'conquer' and possess {O}. Driven by a strong desire, sparks flew from the moment you met.",
                "f": "Control is the main issue. If you try to manipulate {O}, {s} will feel suffocated. Obsession and jealousy are major risks. Avoid becoming too transactional.",
                "i": "Score: 200/100. You might fight during the day but make up passionately at night. Physical satisfaction is extremely high.",
                "a": f"1. No Obsession: Respect {P} privacy.\n2. Financial Transparency: Money issues break this bond.\n3. Respect: Drop the bossy attitude."
            },
            "fr": {
                "t": "🔥 Attraction Fatale : Passion et Contrôle",
                "c": "Une attraction physique intense. Vous voulez 'conquérir' l'autre. Une relation motivée par un fort désir de possession.",
                "f": "Le contrôle est le problème majeur. La manipulation mène à l'étouffement. Attention à la jalousie et à l'obsession.",
                "i": "Score : 200/100 ! Des disputes le jour, des réconciliations passionnées la nuit. Une alchimie physique très forte.",
                "a": "1. Pas d'obsession : Respectez sa vie privée.\n2. Transparence financière.\n3. Respect mutuel."
            },
            "es": {
                "t": "🔥 Atracción Fatal: Pasión y Control",
                "c": "Existe una intensa atracción física. Quieres 'conquistar' al otro. Una relación impulsada por un fuerte deseo de posesión.",
                "f": "El control es el problema principal. La manipulación lleva a la asfixia. Cuidado con los celos y la obsesión.",
                "i": "¡Puntuación: 200/100! Pelean de día, se reconcilian apasionadamente de noche. Química física extremadamente alta.",
                "a": "1. Sin obsesiones: Respeta su privacidad.\n2. Transparencia financiera.\n3. Respeto mutuo."
            },
            "ja": {
                "t": "🔥 致命的な魅力：所有欲と情熱",
                "c": "強烈な性的魅力を感じます。「自分のものにしたい」という征服欲が愛の原動力です。出会った瞬間に火花が散った可能性が高いです。",
                "f": "核心は「コントロール」です。相手を操ろうとすると、相手は息が詰まって逃げ出したくなります。執着と嫉妬に注意が必要です。",
                "i": "相性200点！昼は喧嘩しても夜には仲直りするカップルです。肉体的な相性が抜群で、マンネリになりにくいです。",
                "a": "1. 執着しない：プライバシーを尊重しましょう。\n2. お金はクリアに：金銭トラブルは致命的です。\n3. 尊重する：命令口調はやめましょう。"
            },
            "zh": {
                "t": "🔥 致命吸引力：激情与控制的拉锯战",
                "c": "存在强烈的肉体吸引力。征服欲是爱情的原动力。很可能是一见钟情或相遇瞬间就擦出了火花。",
                "f": "核心问题是“控制”。如果你试图操纵对方，对方会感到窒息想逃跑。容易产生执着和猜疑。",
                "i": "200分！白天吵架晚上和好的情侣。对彼此的肉体迷恋很强，不容易倦怠。",
                "a": "1. 禁止执着：尊重对方隐私。\n2. 金钱透明：财务信任很重要。\n3. 互相尊重：抛弃命令的语气。"
            }
        },
        "Power": { # 관성 (존경/긴장)
            "score": 78,
            "ko": {
                "t": "⚖️ 존경과 긴장 사이: 나를 성장시키는 연인",
                "c": "상대방이 당신을 리드하고 통제하는 관계입니다. 당신은 상대에게서 묘한 카리스마와 어른스러움을 느끼고 존경심을 갖습니다. 서로 부족한 점을 채워주는 '스승과 제자' 같은 커플입니다.",
                "f": "상대가 너무 깐깐하거나 보수적일 수 있습니다. 상대의 조언이 '지적질'이나 '잔소리'로 들리기 시작하면 스트레스가 폭발합니다. '왜 맨날 가르치려 들어?'라는 불만이 생깁니다.",
                "i": "다소 보수적이지만 신뢰가 바탕이 된 관계라 깊고 은근한 매력이 있습니다. 스릴보다는 '안정감'이 돋보이는 속궁합입니다.",
                "a": "1. 자존심 세우지 않기: 쓴약이라고 생각하고 들으세요.\n2. 부드러운 대화: 상처받지 않게 말해달라고 요청하세요.\n3. 규칙 정하기: 서로 간섭하지 않을 선을 정하세요."
            },
            "en": {
                "t": "⚖️ Respect & Tension: The Growth Couple",
                "c": f"{S} leads and pressures you effectively. You feel respect for {P} charisma and maturity. Like a 'Teacher-Student' relationship where you grow together.",
                "f": f"{S} might seem too strict or conservative. If {P} advice starts sounding like criticism or lecturing, your stress will peak. You might feel constantly judged.",
                "i": "Stable and trusting rather than wild. It provides deep emotional security and a sense of being protected.",
                "a": "1. Don't be Defensive: Listen to the advice.\n2. Soft Communication: Ask {O} to speak gently.\n3. Set Boundaries: Limit interference."
            },
            "fr": {
                "t": "⚖️ Respect et Tension : Le Mentor",
                "c": "Votre partenaire vous dirige. Vous respectez son charisme. Une relation 'Maître-Élève' où vous grandissez ensemble.",
                "f": "Il/Elle peut être trop strict(e). Ses conseils peuvent ressembler à des critiques, créant du stress et de la rancœur.",
                "i": "Stable et confiant plutôt que sauvage. Offre une profonde sécurité émotionnelle.",
                "a": "1. Écoutez sans vous braquer.\n2. Communication douce.\n3. Fixez des limites."
            },
            "es": {
                "t": "⚖️ Respeto y Tensión: El Mentor",
                "c": "Tu pareja te dirige. Respetas su carisma. Una relación 'Maestro-Estudiante' donde crecen juntos.",
                "f": "Puede ser demasiado estricto/a. Sus consejos pueden sonar como críticas, creando estrés y resentimiento.",
                "i": "Estable y de confianza más que salvaje. Ofrece una profunda seguridad emocional.",
                "a": "1. Escucha sin ponerte a la defensiva.\n2. Comunicación suave.\n3. Establece límites."
            },
            "ja": {
                "t": "⚖️ 尊敬と緊張：私を成長させる恋人",
                "c": "相手があなたをリードし、コントロールします。相手のカリスマ性と大人っぽさに尊敬の念を抱きます。「先生と生徒」のようにお互いを高め合う関係です。",
                "f": "相手が厳しすぎたり保守的だったりします。アドバイスが「小言」や「批判」に聞こえ始めるとストレスが爆発します。",
                "i": "少し保守的ですが、信頼に基づいた深い魅力があります。スリルよりは「安定感」が際立つ相性です。",
                "a": "1. 素直になる：良薬だと思って聞きましょう。\n2. 優しく話す：傷つかない言い方をリクエストして。\n3. ルールを決める：干渉しすぎない線を決めましょう。"
            },
            "zh": {
                "t": "⚖️ 尊敬与紧张：让我成长的恋人",
                "c": "对方引导并控制着你。你对TA的魅力和成熟感到尊敬。就像“老师和学生”一样互补成长的关系。",
                "f": "对方可能太严厉或保守。当建议听起来像“指责”或“唠叨”时，压力会爆发。你会觉得总是在被说教。",
                "i": "虽然有些保守，但基于信任，有一种深沉的魅力。比起刺激，更强调“安全感”。",
                "a": "1. 放下自尊：良药苦口。\n2. 温柔沟通：要求对方说话委婉点。\n3. 设定界限：划定互不干涉的底线。"
            }
        },
        "Resource": { # 인성 (엄마/힐링)
            "score": 96,
            "ko": {
                "t": "🍼 무한한 사랑: 엄마 품 같은 힐링 커플",
                "c": "상대방이 당신을 헌신적으로 뒷바라지해줍니다. 가만히 있어도 알아서 챙겨주고, 이해하고, 용서해줍니다. 세상에서 가장 편안한 안식처 같은 '힐링 소울메이트'입니다.",
                "f": "너무 편안하다 보니 권태기가 빨리 올 수 있습니다. 당신이 게을러지거나 사랑을 당연하게 여기는 순간 위기가 옵니다. 때로는 상대의 사랑이 '과잉보호'로 느껴져 답답할 수 있습니다.",
                "i": "자극적인 쾌락보다는 정서적인 포만감이 큽니다. 서로 안고만 있어도 좋은, 부드럽고 따뜻한 스킨십이 주를 이룹니다.",
                "a": "1. 감사 표현하기: 받는 것에 익숙해지지 마세요.\n2. 긴장감 유지: 가끔은 색다른 데이트가 필요합니다.\n3. 독립심 키우기: 너무 의존하지 마세요."
            },
            "en": {
                "t": "🍼 Unconditional Love: Healing Soulmate",
                "c": f"{S} supports you devotedly. You feel safe, understood, and forgiven without even trying, as if in a mother's arms. It is a healing relationship with a strong emotional bond.",
                "f": f"Comfort can lead to boredom or laziness. You might take {P} love for granted. Also, {P} care might feel like smothering or over-protection at times.",
                "i": "Emotional satisfaction is higher than physical thrill. A gentle, warm connection where just holding each other feels enough.",
                "a": "1. Express Gratitude: Don't get used to receiving.\n2. Keep the Spark: Try new things together.\n3. Be Independent: Don't rely on {O} too much."
            },
            "fr": {
                "t": "🍼 Amour Inconditionnel : Âme Sœur Guérisseuse",
                "c": "Il/Elle vous soutient avec dévouement. Vous vous sentez en sécurité et compris(e), comme dans les bras d'une mère. Une relation apaisante.",
                "f": "Le confort peut mener à l'ennui. Ne prenez pas son amour pour acquis. Attention à ne pas vous sentir étouffé(e) par sa protection.",
                "i": "Satisfaction émotionnelle > Frisson physique. Une connexion douce et chaleureuse.",
                "a": "1. Exprimez votre gratitude.\n2. Maintenez la flamme.\n3. Gardez votre indépendance."
            },
            "es": {
                "t": "🍼 Amor Incondicional: Alma Gemela Sanadora",
                "c": "Te apoya con devoción. Te sientes seguro/a y comprendido/a, como en los brazos de una madre. Una relación sanadora.",
                "f": "La comodidad puede llevar al aburrimiento. No des su amor por sentado. Cuidado con sentirte asfixiado/a por su protección.",
                "i": "Satisfacción emocional > Emoción física. Una conexión suave y cálida.",
                "a": "1. Expresa gratitud.\n2. Mantén la chispa.\n3. Sé independiente."
            },
            "ja": {
                "t": "🍼 無限の愛：母のような癒しのカップル",
                "c": "相手があなたを献身的に支えてくれます。何もしなくても世話を焼き、理解し、許してくれます。世界で一番安らげる「癒しのソウルメイト」です。",
                "f": "居心地が良すぎてマンネリが早まるかも。愛を当たり前だと思ったり、怠けたりすると危機が訪れます。過保護に感じて息苦しくなることも。",
                "i": "刺激よりは精神的な満腹感が大きいです。抱きしめ合うだけで幸せな、温かいスキンシップが中心です。",
                "a": "1. 感謝を伝える：受け取ることに慣れすぎないで。\n2. 緊張感を維持：たまには新鮮なデートを。\n3. 自立心を持つ：依存しすぎないように。"
            },
            "zh": {
                "t": "🍼 无限的爱：治愈系灵魂伴侣",
                "c": "对方全心全意地照顾你。即使你什么都不做，TA也会理解和包容你。就像在母亲怀抱中一样，是最舒适的避风港。",
                "f": "太舒适会导致倦怠期早早到来。当你变得懒惰或把爱视为理所当然时，危机就会降临。有时过度的爱会让人觉得是“过分保护”而感到郁闷。",
                "i": "比起感官刺激，情感上的满足感更大。主要是温柔温暖的肢体接触，仅是拥抱也很美好。",
                "a": "1. 表达感谢：不要习惯于索取。\n2. 保持紧张感：偶尔需要特别的约会。\n3. 培养独立心：不要太依赖对方。"
            }
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
        "btn_buy": "전체 리포트 해제 ($3)", "btn_unlock": "잠금 해제", "key_label": "라이센스 키",
        "analyze": "궁합 분석하기", "h_chem": "🔮 성격과 케미", "h_conf": "⚔️ 갈등 포인트", 
        "h_inti": "💋 속궁합 & 애정", "h_adv": "🚀 관계를 위한 조언"
    },
    "en": {
        "title": "💘 Love Compatibility", "sub": "Deep analysis of souls, chemistry, and future.",
        "p_info": "Partner Info", "p_name": "Name", "p_dob": "DOB", "p_gender": "Gender",
        "lock_title": "🔒 VIP Report Locked", "lock_msg": "Unlock intimacy, conflict points, and future advice.",
        "btn_buy": "Unlock Report ($3)", "btn_unlock": "Unlock", "key_label": "License Key",
        "analyze": "Analyze", "h_chem": "🔮 Chemistry", "h_conf": "⚔️ Conflict", 
        "h_inti": "💋 Intimacy", "h_adv": "🚀 Advice"
    },
    "fr": {
        "title": "💘 Compatibilité Amoureuse", "sub": "Analyse approfondie des âmes et de la chimie.",
        "p_info": "Info Partenaire", "p_name": "Nom", "p_dob": "Date de Naissance", "p_gender": "Genre",
        "lock_title": "🔒 Rapport VIP", "lock_msg": "Débloquez l'intimité et les conseils.",
        "btn_buy": "Débloquer ($3)", "btn_unlock": "Déverrouiller", "key_label": "Clé",
        "analyze": "Analyser", "h_chem": "🔮 Chimie", "h_conf": "⚔️ Conflits", 
        "h_inti": "💋 Intimité", "h_adv": "🚀 Conseils"
    },
    "es": {
        "title": "💘 Compatibilidad Amorosa", "sub": "Análisis profundo de almas y química.",
        "p_info": "Info Pareja", "p_name": "Nombre", "p_dob": "Fecha Nacimiento", "p_gender": "Género",
        "lock_title": "🔒 Reporte VIP", "lock_msg": "Desbloquea intimidad y consejos.",
        "btn_buy": "Desbloquear ($3)", "btn_unlock": "Desbloquear", "key_label": "Clave",
        "analyze": "Analizar", "h_chem": "🔮 Química", "h_conf": "⚔️ Conflictos", 
        "h_inti": "💋 Intimidad", "h_adv": "🚀 Consejos"
    },
    "ja": {
        "title": "💘 恋愛相性診断", "sub": "魂、相性、未来を深く分析。",
        "p_info": "相手の情報", "p_name": "名前", "p_dob": "生年月日", "p_gender": "性別",
        "lock_title": "🔒 VIPレポート", "lock_msg": "親密さ、葛藤、未来のアドバイスを解除。",
        "btn_buy": "解除 ($3)", "btn_unlock": "解除", "key_label": "キー",
        "analyze": "分析する", "h_chem": "🔮 相性", "h_conf": "⚔️ 葛藤", 
        "h_inti": "💋 親密さ", "h_adv": "🚀 アドバイス"
    },
    "zh": {
        "title": "💘 恋爱契合度", "sub": "深度分析灵魂、化学反应和未来。",
        "p_info": "伴侣信息", "p_name": "姓名", "p_dob": "出生日期", "p_gender": "性别",
        "lock_title": "🔒 VIP报告", "lock_msg": "解锁亲密度、冲突点和建议。",
        "btn_buy": "解锁 ($3)", "btn_unlock": "解锁", "key_label": "密钥",
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
                if st.button(t['btn_unlock'], type="primary", use_container_width=True):
                    # 1. 마스터 키 (무제한) 확인
                    if k_in == UNLOCK_CODE:
                        st.session_state["unlocked_love"] = True
                        st.success("Master Unlocked!")
                        st.rerun()
                    else:
                        try:
                            # 2. 단품(Love Compatibility) 키 확인 (3회 제한)
                            r = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                              data={
                                                  "product_permalink": "love_compatibility", 
                                                  "license_key": k_in, 
                                                  "increment_uses_count": "true" # 👈 카운트 증가
                                              }).json()
                            
                            if r.get("success"):
                                if r.get("uses", 0) > 3: # 🚨 3회 제한 로직
                                    st.error("🚫 Usage limit exceeded (Max 3)")
                                else:
                                    st.session_state["unlocked_love"] = True
                                    st.rerun()
                            else:
                                # 3. 올패스(All-Access) 키 확인 (합산 10회 제한)
                                r2 = requests.post("https://api.gumroad.com/v2/licenses/verify", 
                                                   data={
                                                       "product_permalink": "all-access_pass", 
                                                       "license_key": k_in, 
                                                       "increment_uses_count": "true" # 👈 카운트 증가
                                                   }).json()
                                
                                if r2.get("success"):
                                    if r2.get("uses", 0) > 10: # 🚨 합산 10회 제한 로직
                                        st.error("🚫 Usage limit exceeded (Max 10)")
                                    else:
                                        st.session_state["unlocked_love"] = True
                                        st.rerun()
                                else:
                                    st.error("Invalid Key")
                        except: 
                            st.error("Connection Error")
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
