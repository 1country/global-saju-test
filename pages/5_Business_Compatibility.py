import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import date
import os
# utils.py 파일이 같은 폴더에 있어야 합니다.
from utils import calculate_day_gan

# ----------------------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------------------
st.set_page_config(page_title="Business Compatibility | The Element", page_icon="💼", layout="wide")

if 'lang' not in st.session_state:
    st.session_state['lang'] = os.environ.get('LANGUAGE', 'en')
lang = st.session_state['lang']

# 🔑 [키 설정]
UNLOCK_CODE = "MASTER2026"
PRODUCT_PERMALINK_SPECIFIC = "business_compatibility" 
PRODUCT_PERMALINK_ALL = "all-access_pass" 
GUMROAD_LINK_SPECIFIC = "https://5codes.gumroad.com/l/business_compatibility"
GUMROAD_LINK_ALL = "https://5codes.gumroad.com/l/all-access_pass"

# ----------------------------------------------------------------
# 2. 스타일 설정 (박스 제거 및 글자 가독성 강화)
# ----------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
        
        /* ✨ 배경: 밝은 고층 빌딩 뷰 */
        .stApp {
            background-image: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.6)),
            url("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop");
            background-size: cover; background-attachment: fixed; background-position: center;
            color: #1e293b; 
        }
        
        /* 사이드바 */
        section[data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid #cbd5e1; }
        section[data-testid="stSidebar"] * { color: #334155 !important; }

        /* 메인 타이틀 */
        .main-header {
            font-size: 3em; font-weight: 800; color: #1e40af; margin-bottom: 10px; text-align: center;
            font-family: 'Gowun Batang', serif; 
            text-shadow: 2px 2px 0 #fff, -1px -1px 0 #fff; /* 타이틀 흰색 테두리 */
        }
        
        /* 🚨 [핵심 수정] 라벨(질문) 글씨 스타일 (박스 없이 글자만 선명하게) */
        .stTextInput label, .stDateInput label, .stSelectbox label, div[data-testid="stWidgetLabel"] p {
            color: #1e3a8a !important;          /* 진한 파란색 글씨 */
            font-size: 1.5rem !important;       /* 글자 크기 키움 */
            font-weight: 900 !important;        /* 두께 두껍게 */
            text-shadow: 
                -1px -1px 0 #fff,  
                 1px -1px 0 #fff,
                -1px  1px 0 #fff,
                 1px  1px 0 #fff,
                 2px  2px 4px rgba(0,0,0,0.2) !important; /* 흰색 테두리로 배경 분리 */
            margin-bottom: 8px !important;
        }
        
        /* 입력창 내부 스타일 */
        div[data-baseweb="input"], div[data-baseweb="select"] > div { 
            background-color: rgba(255, 255, 255, 0.9) !important; 
            border: 2px solid #3b82f6 !important; /* 파란색 테두리 */
            color: #000 !important; 
            border-radius: 10px !important;
        }

        /* 리포트 컨테이너 */
        .report-container {
            background-color: #ffffff; padding: 40px; border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); border: 1px solid #bfdbfe;
            color: #334155;
        }
        
        .score-display {
            text-align: center; font-size: 3.5em; font-weight: bold; color: #2563eb; margin: 20px 0;
        }

        .section-box {
            margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px dashed #cbd5e1;
        }
        .section-box:last-child { border-bottom: none; }
        
        .section-title {
            font-size: 1.4em; font-weight: bold; color: #1e40af; margin-bottom: 15px; 
            display: flex; align-items: center; border-left: 5px solid #3b82f6; padding-left: 15px;
        }
        .content-text { font-size: 1.1em; line-height: 1.8; color: #475569; text-align: justify; }
        
        /* 사용자 카드 */
        .user-card {
            background: linear-gradient(135deg, #eff6ff, #ffffff); 
            padding: 20px; border-radius: 12px; border: 1px solid #dbeafe;
            text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .user-role { color: #64748b; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; font-weight:bold;}
        .user-name { font-size: 1.6em; font-weight: bold; color: #1e293b; margin: 5px 0; }
        .user-elem { font-size: 1.2em; color: #2563eb; font-weight: bold; }

        .vs-badge {
            display: flex; justify-content: center; align-items: center; 
            font-size: 2.5em; font-weight: bold; color: #3b82f6; height: 100%;
        }
        
        /* 잠금 화면 스타일 */
        .lock-container {
            text-align:center; background-color: rgba(255,255,255,0.95); padding:30px; border-radius:15px;
            border: 1px solid #cbd5e1; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. 사이드바 (언어 설정)
# ----------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    lang_map = {"ko": "한국어", "en": "English", "fr": "Français", "es": "Español", "ja": "日本語", "zh": "中文"}
    st.info(f"Language: **{lang_map.get(lang, 'English')}**")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("🇺🇸 EN"): st.session_state['lang']='en'; st.rerun()
    if c2.button("🇰🇷 KO"): st.session_state['lang']='ko'; st.rerun()
    if c3.button("🇫🇷 FR"): st.session_state['lang']='fr'; st.rerun()
    c4, c5, c6 = st.columns(3)
    if c4.button("🇪🇸 ES"): st.session_state['lang']='es'; st.rerun()
    if c5.button("🇯🇵 JA"): st.session_state['lang']='ja'; st.rerun()
    if c6.button("🇨🇳 ZH"): st.session_state['lang']='zh'; st.rerun()

    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

# ----------------------------------------------------------------
# 4. 데이터 및 리포트 (6개 국어)
# ----------------------------------------------------------------
def get_biz_report(u_elem, p_elem, lang):
    relations = {
        "Wood": {"Wood": "Same", "Fire": "Output", "Earth": "Wealth", "Metal": "Power", "Water": "Resource"},
        "Fire": {"Fire": "Same", "Earth": "Output", "Metal": "Wealth", "Water": "Power", "Wood": "Resource"},
        "Earth": {"Earth": "Same", "Metal": "Output", "Water": "Wealth", "Wood": "Power", "Fire": "Resource"},
        "Metal": {"Metal": "Same", "Water": "Output", "Wood": "Wealth", "Fire": "Power", "Earth": "Resource"},
        "Water": {"Water": "Same", "Wood": "Output", "Fire": "Wealth", "Earth": "Power", "Metal": "Resource"}
    }
    rel = relations.get(u_elem, {}).get(p_elem, "Same")
    
    reports = {
        "Same": { 
            "score": 80,
            "ko": {
                "title": "🤝 어깨를 나란히 하는 '공동 대표' (Friends & Rivals)",
                "synergy": "두 사람은 비즈니스 파트너로서 아주 대등한 관계입니다. 서로의 야망과 추진력이 비슷하여 창업 초기 폭발적인 시너지를 냅니다. 마치 형제처럼 서로를 밀어주는 강력한 '원팀'이 될 수 있습니다.",
                "finance": "수익 배분(Share)이 가장 중요합니다. 둘 다 계산이 빠르기 때문에 배분이 불투명하면 즉시 갈등이 생깁니다. 모든 것을 문서화하세요.",
                "role": "공동 대표 (Co-CEO) 또는 영업(CEO) vs 운영(COO) 분리",
                "advice": "1. 계약서에 지분율을 명확히 하세요.\n2. 서로의 영역을 침범하지 마세요.\n3. 선의의 경쟁을 즐기세요."
            },
            "en": {
                "title": "🤝 Equal Partners: Co-Founders",
                "synergy": "You are equals. Your ambition aligns perfectly, creating explosive synergy in early stages. You act like brothers in arms, pushing each other forward.",
                "finance": "Profit sharing is critical. Ambiguity leads to conflict. Document equity and distribution clearly.",
                "role": "Co-CEO or Split Roles (Sales vs Ops)",
                "advice": "1. Clarify equity in contracts.\n2. Define distinct responsibilities.\n3. Use rivalry to fuel growth."
            },
            "fr": {
                "title": "🤝 Partenaires Égaux : Cofondateurs",
                "synergy": "Vous êtes des égaux. Votre ambition s'aligne parfaitement. Vous agissez comme des frères d'armes.",
                "finance": "Le partage des profits est critique. L'ambiguïté mène au conflit. Documentez tout.",
                "role": "Co-PDG ou Rôles séparés",
                "advice": "1. Clarifiez l'équité par contrat.\n2. Définissez les responsabilités.\n3. Utilisez la rivalité positivement."
            },
            "es": {
                "title": "🤝 Socios Iguales: Cofundadores",
                "synergy": "Son iguales. Su ambición se alinea perfectamente. Actúan como hermanos de armas.",
                "finance": "El reparto de beneficios es crítico. La ambigüedad lleva al conflicto. Documenten todo.",
                "role": "Co-CEO o Roles separados",
                "advice": "1. Aclare la equidad en contratos.\n2. Defina responsabilidades.\n3. Use la rivalidad para crecer."
            },
            "ja": {
                "title": "🤝 肩を並べる「共同代表」タイプ",
                "synergy": "二人は対等な関係です。野心と推進力が似ており、創業初期に爆発的なシナジーを生み出します。",
                "finance": "利益配分が最も重要です。曖昧さは対立を招きます。全てを文書化してください。",
                "role": "共同代表 (Co-CEO) または役割分担",
                "advice": "1. 契約書で持分を明確にする。\n2. 互いの領域を侵さない。\n3. 善意の競争を楽しむ。"
            },
            "zh": {
                "title": "🤝 旗鼓相当的“联合创始人”",
                "synergy": "你们是平等的商业伙伴。野心和动力完美契合，在创业初期能产生爆发性的协同效应。",
                "finance": "利益分配至关重要。模糊不清会导致冲突。请务必白纸黑字写清楚。",
                "role": "联席CEO 或 职责分离",
                "advice": "1. 在合同中明确股权。\n2. 划清各自的责任领域。\n3. 良性竞争促进成长。"
            }
        },
        "Output": { 
            "score": 90,
            "ko": {
                "title": "💡 기획자와 실행가: 창조적 파트너십",
                "synergy": "당신(기획자)이 아이디어를 내면 파트너(실행가)가 그것을 현실로 만듭니다. R&D나 디자인 등 창의적인 분야에서 최고의 궁합입니다.",
                "finance": "당신이 투자하고 파트너가 기술을 대는 형태입니다. 당장의 수익보다 미래 가치를 보고 투자해야 합니다.",
                "role": "당신: 회장/기획 (Visionary) | 파트너: 사장/개발 (Executor)",
                "advice": "1. 실무에 너무 깊게 관여하지 마세요.\n2. 파트너에게 충분한 인센티브를 주세요.\n3. 성과가 나올 때까지 기다려주세요."
            },
            "en": {
                "title": "💡 Visionary & Executor: Creative Duo",
                "synergy": "You provide the vision; your partner turns it into reality. Excellent for R&D, design, or marketing.",
                "finance": "You invest capital; they invest skill. Look for future value rather than immediate profit.",
                "role": "You: Visionary/Chairman | Partner: Executor/CEO",
                "advice": "1. Don't micromanage execution.\n2. Incentivize them well.\n3. Be patient for results."
            },
            "fr": {
                "title": "💡 Visionnaire & Exécutant",
                "synergy": "Vous apportez la vision, votre partenaire la réalise. Excellent pour la R&D ou le design.",
                "finance": "Vous investissez le capital, eux la compétence. Visez la valeur future.",
                "role": "Vous: Visionnaire | Partenaire: Exécutant",
                "advice": "1. Ne microgérez pas.\n2. Donnez des incitations.\n3. Soyez patient."
            },
            "es": {
                "title": "💡 Visionario & Ejecutor",
                "synergy": "Tú aportas la visión; tu socio la hace realidad. Excelente para I+D o diseño.",
                "finance": "Tú inviertes capital; ellos habilidad. Busca valor futuro.",
                "role": "Tú: Visionario | Socio: Ejecutor",
                "advice": "1. No microgestiones.\n2. Incentiva bien.\n3. Ten paciencia."
            },
            "ja": {
                "title": "💡 企画者と実行者：創造的パートナー",
                "synergy": "あなたがビジョンを提示し、パートナーがそれを現実にします。R&Dやデザイン分野で最高です。",
                "finance": "あなたが資金を、パートナーが技術を提供する形です。目先の利益より未来の価値を見てください。",
                "role": "あなた：会長/企画 | パートナー：社長/開発",
                "advice": "1. 実務に干渉しすぎない。\n2. 十分なインセンティブを与える。\n3. 結果が出るまで待つ。"
            },
            "zh": {
                "title": "💡 策划者与执行者：创意搭档",
                "synergy": "你提供愿景，伙伴将其变为现实。非常适合研发、设计或营销领域。",
                "finance": "你出资，对方出力。看重未来价值而非眼前利益。",
                "role": "你：董事长/策划 | 伙伴：CEO/执行",
                "advice": "1. 不要微观管理。\n2. 给予充分的激励。\n3. 耐心等待结果。"
            }
        },
        "Wealth": {
            "score": 85,
            "ko": {
                "title": "💰 오너와 전문경영인: 이익 추구형",
                "synergy": "당신이 주도권을 쥐고 파트너를 관리합니다. 파트너는 실질적인 돈을 벌어옵니다. 이윤 추구가 목적이라면 가장 이상적입니다.",
                "finance": "재물운 최상. 파트너가 번 돈을 당신이 관리합니다. 자금 흐름을 꽉 쥐고 있어야 합니다.",
                "role": "당신: 오너 (Owner) | 파트너: 영업/실무 (Manager)",
                "advice": "1. 성과에 대해 확실히 보상하세요.\n2. 파트너를 인격적으로 존중하세요.\n3. 믿을 수 있는 범위 내에서 권한을 위임하세요."
            },
            "en": {
                "title": "💰 Owner & Manager: Profit Driven",
                "synergy": "You hold the reins. The partner brings in the profit. Ideal for profit-maximization businesses.",
                "finance": "Best financial luck. You manage the money they earn. Keep a grip on cash flow.",
                "role": "You: Owner | Partner: Manager/Sales",
                "advice": "1. Pay well for results.\n2. Treat them with respect.\n3. Delegate authority wisely."
            },
            "fr": {
                "title": "💰 Propriétaire & Gestionnaire",
                "synergy": "Vous tenez les rênes. Le partenaire apporte le profit. Idéal pour maximiser les gains.",
                "finance": "Meilleure chance financière. Vous gérez l'argent qu'ils gagnent.",
                "role": "Vous: Propriétaire | Partenaire: Gestionnaire",
                "advice": "1. Payez bien pour les résultats.\n2. Traitez-les avec respect.\n3. Déléguez sagement."
            },
            "es": {
                "title": "💰 Dueño & Gerente",
                "synergy": "Tú tienes el control. El socio trae las ganancias. Ideal para maximizar beneficios.",
                "finance": "Mejor suerte financiera. Tú gestionas el dinero que ganan.",
                "role": "Tú: Dueño | Socio: Gerente",
                "advice": "1. Paga bien por resultados.\n2. Trátalos con respeto.\n3. Delega sabiamente."
            },
            "ja": {
                "title": "💰 オーナーと専門経営者：利益追求型",
                "synergy": "あなたが主導権を握り、パートナーが利益をもたらします。利益追求において最も理想的です。",
                "finance": "金運最高。パートナーが稼いだお金をあなたが管理します。",
                "role": "あなた：オーナー | パートナー：営業/実務",
                "advice": "1. 成果に対して確実に報酬を出す。\n2. パートナーを尊重する。\n3. 賢く権限を委譲する。"
            },
            "zh": {
                "title": "💰 老板与职业经理人：利益驱动",
                "synergy": "你掌握控制权，伙伴带来利润。最适合追求利润最大化的企业。",
                "finance": "财运最佳。你管理他们赚来的钱。需紧抓现金流。",
                "role": "你：老板 | 伙伴：经理/销售",
                "advice": "1. 按结果给予丰厚回报。\n2. 尊重对方。\n3. 明智地放权。"
            }
        },
        "Power": {
            "score": 75,
            "ko": {
                "title": "⚖️ 시스템과 규율: 안정적 성장",
                "synergy": "파트너가 주도권을 쥐거나 엄격한 원칙을 요구합니다. 답답할 수 있지만 리스크 관리에 탁월합니다. 프랜차이즈 본사(파트너)와 점주(본인) 관계와 비슷합니다.",
                "finance": "대박보다는 안정을 추구합니다. 파트너가 재무 결재권을 가질 때 회사가 탄탄해집니다.",
                "role": "당신: 홍보/영업 (Face) | 파트너: CEO/관리 (Controller)",
                "advice": "1. 파트너의 규칙을 따르는 것이 이득입니다.\n2. 쓴소리를 귀담아 들으세요.\n3. 2인자가 되는 것을 두려워 마세요."
            },
            "en": {
                "title": "⚖️ Structured Growth: Discipline",
                "synergy": "Your partner sets strict rules. It feels restrictive but reduces risk. Like a Franchisee (You) vs HQ (Partner).",
                "finance": "Stability over jackpots. Financial health improves when the partner manages funds.",
                "role": "You: Face/PR | Partner: Controller/CEO",
                "advice": "1. Following their rules pays off.\n2. Listen to their advice.\n3. Accept being number two."
            },
            "fr": {
                "title": "⚖️ Croissance Structurée",
                "synergy": "Votre partenaire fixe des règles strictes. Cela réduit les risques.",
                "finance": "Stabilité avant tout. La santé financière s'améliore quand ils gèrent.",
                "role": "Vous: Image/RP | Partenaire: Contrôleur/PDG",
                "advice": "1. Suivre leurs règles paie.\n2. Écoutez leurs conseils.\n3. Acceptez d'être numéro deux."
            },
            "es": {
                "title": "⚖️ Crecimiento Estructurado",
                "synergy": "Tu socio establece reglas estrictas. Reduce riesgos. Como Franquiciado (Tú) vs Central (Socio).",
                "finance": "Estabilidad sobre premios. La salud financiera mejora cuando ellos gestionan.",
                "role": "Tú: Imagen/RP | Socio: Controlador/CEO",
                "advice": "1. Seguir sus reglas vale la pena.\n2. Escucha sus consejos.\n3. Acepta ser el número dos."
            },
            "ja": {
                "title": "⚖️ 規律とシステム：安定的成長",
                "synergy": "パートナーが主導権や厳格な原則を求めます。リスク管理に優れています。",
                "finance": "一攫千金より安定。パートナーが財務を管理すると会社が強くなります。",
                "role": "あなた：広報/営業 | パートナー：CEO/管理",
                "advice": "1. 相手のルールに従うが得。\n2. 苦言に耳を傾ける。\n3. No.2になることを恐れない。"
            },
            "zh": {
                "title": "⚖️ 制度与规范：稳健成长",
                "synergy": "伙伴制定严格规则。虽受限制但能降低风险。类似加盟商（你）与总部（伙伴）的关系。",
                "finance": "求稳不求快。伙伴管理资金时财务更健康。",
                "role": "你：门面/公关 | 伙伴：控制者/CEO",
                "advice": "1. 遵守规则会有回报。\n2. 听取逆耳忠言。\n3. 接受做二把手。"
            }
        },
        "Resource": {
            "score": 95,
            "ko": {
                "title": "🍼 멘토와 후원자: 최고의 서포터",
                "synergy": "파트너가 당신을 전적으로 믿고 지지해줍니다. 부족한 점을 채워주고 심리적 안정을 줍니다. 투자자(파트너)와 스타트업 대표(본인)로서 훌륭합니다.",
                "finance": "계약운과 문서운이 좋습니다. 파트너 덕분에 자산을 늘릴 수 있습니다.",
                "role": "당신: CEO (Operator) | 파트너: 회장/고문 (Mentor)",
                "advice": "1. 후원을 당연하게 여기지 마세요.\n2. 최종 결정은 당신이 내려야 합니다.\n3. 비전을 자주 공유하세요."
            },
            "en": {
                "title": "🍼 Mentor & Protege: Full Support",
                "synergy": "Your partner fully trusts and supports you. Ideal for an Investor (Partner) and CEO (You) relationship.",
                "finance": "Great luck with contracts and assets. Brand value grows with their help.",
                "role": "You: CEO | Partner: Mentor/Chairman",
                "advice": "1. Don't take support for granted.\n2. Make final decisions yourself.\n3. Share your vision regularly."
            },
            "fr": {
                "title": "🍼 Mentor & Protégé",
                "synergy": "Votre partenaire vous soutient totalement. Idéal pour Investisseur (Eux) et PDG (Vous).",
                "finance": "Grande chance avec les contrats. La valeur de la marque augmente.",
                "role": "Vous: PDG | Partenaire: Mentor",
                "advice": "1. Ne prenez pas le soutien pour acquis.\n2. Décidez vous-même.\n3. Partagez votre vision."
            },
            "es": {
                "title": "🍼 Mentor & Protegido",
                "synergy": "Tu socio te apoya totalmente. Ideal para Inversor (Ellos) y CEO (Tú).",
                "finance": "Gran suerte con contratos. El valor de marca crece.",
                "role": "Tú: CEO | Socio: Mentor",
                "advice": "1. No des el apoyo por sentado.\n2. Toma decisiones tú mismo.\n3. Comparte tu visión."
            },
            "ja": {
                "title": "🍼 メンターと後援者：最高のサポーター",
                "synergy": "パートナーがあなたを全面的に支持します。投資家（パートナー）と代表（あなた）として素晴らしい相性です。",
                "finance": "契約運と資産運が良いです。パートナーのおかげで資産が増えます。",
                "role": "あなた：CEO | パートナー：会長/顧問",
                "advice": "1. 支援を当たり前と思わない。\n2. 最終決定は自分でする。\n3. ビジョンを頻繁に共有する。"
            },
            "zh": {
                "title": "🍼 导师与被辅佐者：全力支持",
                "synergy": "伙伴完全信任并支持你。非常适合投资人（伙伴）与CEO（你）的关系。",
                "finance": "合同运和资产运极佳。在他们的帮助下品牌价值提升。",
                "role": "你：CEO | 伙伴：导师/董事长",
                "advice": "1. 不要把支持视为理所当然。\n2. 自己做最终决定。\n3. 定期分享愿景。"
            }
        }
    }
    
    base_data = reports[rel]
    data = base_data.get(lang, base_data['en'])
    
    return {
        "score": base_data["score"],
        "title": data['title'],
        "synergy": data['synergy'],
        "finance": data['finance'],
        "role": data['role'],
        "advice": data['advice']
    }

# ----------------------------------------------------------------
# 5. UI 텍스트 (6개 국어)
# ----------------------------------------------------------------
ui_text = {
    "ko": {
        "title": "💼 비즈니스 파트너 궁합", "sub": "동업 성공 전략 및 역할 분담 분석",
        "p_info_title": "파트너 정보 입력", "p_name": "파트너 이름", "p_dob": "파트너 생년월일", "p_gender": "성별",
        "lock_title": "🔒 리포트 잠금", "lock_desc": "결제 후 발급받은 키를 입력하세요.", "lock_warn": "⚠️ 사용 횟수가 1회 차감됩니다.",
        "btn_buy_sp": "💳 단품 구매 ($3)", "btn_buy_all": "🎟️ All-Access ($10)", "btn_unlock": "결과 확인", "btn_print": "🖨️ 인쇄하기",
        "lbl_syn": "🚀 시너지 (Synergy)", "lbl_fin": "💰 재무 (Finance)", "lbl_rol": "👔 역할 (Role)", "lbl_adv": "💡 조언 (Advice)", "lbl_score": "궁합 점수"
    },
    "en": {
        "title": "💼 Business Compatibility", "sub": "Co-founding Strategy & Role Analysis",
        "p_info_title": "Partner Info", "p_name": "Partner Name", "p_dob": "Partner DOB", "p_gender": "Gender",
        "lock_title": "🔒 Report Locked", "lock_desc": "Enter license key to unlock.", "lock_warn": "⚠️ Deducts 1 credit.",
        "btn_buy_sp": "💳 Single ($3)", "btn_buy_all": "🎟️ All-Access ($10)", "btn_unlock": "Unlock", "btn_print": "🖨️ Print",
        "lbl_syn": "🚀 Synergy", "lbl_fin": "💰 Finance", "lbl_rol": "👔 Role", "lbl_adv": "💡 Advice", "lbl_score": "Score"
    },
    "fr": {
        "title": "💼 Compatibilité Affaires", "sub": "Stratégie de partenariat",
        "p_info_title": "Info Partenaire", "p_name": "Nom", "p_dob": "Date de naissance", "p_gender": "Genre",
        "lock_title": "🔒 Verrouillé", "lock_desc": "Entrez la clé de licence.", "lock_warn": "⚠️ Déduit 1 crédit.",
        "btn_buy_sp": "💳 Unique ($3)", "btn_buy_all": "🎟️ Tout ($10)", "btn_unlock": "Débloquer", "btn_print": "🖨️ Imprimer",
        "lbl_syn": "🚀 Synergie", "lbl_fin": "💰 Finance", "lbl_rol": "👔 Rôle", "lbl_adv": "💡 Conseil", "lbl_score": "Score"
    },
    "es": {
        "title": "💼 Compatibilidad de Negocios", "sub": "Estrategia de asociación",
        "p_info_title": "Info Socio", "p_name": "Nombre", "p_dob": "Fecha nacimiento", "p_gender": "Género",
        "lock_title": "🔒 Bloqueado", "lock_desc": "Ingrese la clave.", "lock_warn": "⚠️ Deduce 1 crédito.",
        "btn_buy_sp": "💳 Único ($3)", "btn_buy_all": "🎟️ Todo ($10)", "btn_unlock": "Desbloquear", "btn_print": "🖨️ Imprimir",
        "lbl_syn": "🚀 Sinergia", "lbl_fin": "💰 Finanzas", "lbl_rol": "👔 Rol", "lbl_adv": "💡 Consejo", "lbl_score": "Puntuación"
    },
    "ja": {
        "title": "💼 ビジネス相性診断", "sub": "共同創業と役割分担の分析",
        "p_info_title": "パートナー情報", "p_name": "名前", "p_dob": "生年月日", "p_gender": "性別",
        "lock_title": "🔒 ロック中", "lock_desc": "ライセンスキーを入力。", "lock_warn": "⚠️ 1回分消費します。",
        "btn_buy_sp": "💳 単品 ($3)", "btn_buy_all": "🎟️ 全て ($10)", "btn_unlock": "解除", "btn_print": "🖨️ 印刷",
        "lbl_syn": "🚀 シナジー", "lbl_fin": "💰 財務", "lbl_rol": "👔 役割", "lbl_adv": "💡 アドバイス", "lbl_score": "スコア"
    },
    "zh": {
        "title": "💼 商业伙伴合盘", "sub": "合伙策略与角色分配",
        "p_info_title": "伙伴信息", "p_name": "姓名", "p_dob": "出生日期", "p_gender": "性别",
        "lock_title": "🔒 已锁定", "lock_desc": "输入许可密钥。", "lock_warn": "⚠️ 扣除1次额度。",
        "btn_buy_sp": "💳 单次 ($3)", "btn_buy_all": "🎟️ 通行证 ($10)", "btn_unlock": "解锁", "btn_print": "🖨️ 打印",
        "lbl_syn": "🚀 协同效应", "lbl_fin": "💰 财务", "lbl_rol": "👔 角色", "lbl_adv": "💡 建议", "lbl_score": "分数"
    }
}
t = ui_text.get(lang, ui_text['en'])

# ----------------------------------------------------------------
# 6. 메인 로직
# ----------------------------------------------------------------
if "user_name" not in st.session_state or "birth_date" not in st.session_state:
    st.warning("Please enter your info at Home first.")
    if st.button("Go Home"): st.switch_page("Home.py")
    st.stop()

u_name = st.session_state["user_name"]
u_dob = st.session_state["birth_date"]
u_gender = st.session_state.get("gender", "Male")

st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#64748b; margin-bottom:30px; font-weight:bold;'>{t['sub']}</div>", unsafe_allow_html=True)

# 6-1. 입력 컨테이너 (밝은 테마)
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1e3a8a;'>{t['p_info_title']}</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        p_name = st.text_input(t['p_name'])
    with c2:
        p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1990,1,1))
    with c3:
        p_gender = st.selectbox(t['p_gender'], ["Male", "Female"])
    st.markdown('</div>', unsafe_allow_html=True)

# 6-2. 잠금 및 결제
if "unlocked_biz" not in st.session_state: st.session_state["unlocked_biz"] = False

if not st.session_state["unlocked_biz"]:
    st.divider()
    with st.container():
        st.markdown('<div class="lock-container">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ec4899;'>{t['lock_title']}</h3>", unsafe_allow_html=True)
        st.write(f"<p style='color:#475569;'>{t['lock_desc']}</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: st.link_button(t['btn_buy_sp'], GUMROAD_LINK_SPECIFIC)
        with c2: st.link_button(t['btn_buy_all'], GUMROAD_LINK_ALL)
        
        st.markdown("---")
        key = st.text_input("License Key", type="password")
        
        if st.button(t['btn_unlock'], type="primary"):
            if not p_name:
                st.error("Please enter partner name.")
            else:
                if key == UNLOCK_CODE:
                    st.session_state["unlocked_biz"] = True
                    st.rerun()
                
                try:
                    r1 = requests.post("https://api.gumroad.com/v2/licenses/verify",
                                      data={"product_permalink": PRODUCT_PERMALINK_SPECIFIC, "license_key": key}).json()
                    if r1.get("success"):
                         st.session_state["unlocked_biz"] = True
                         st.rerun()
                    else:
                        r2 = requests.post("https://api.gumroad.com/v2/licenses/verify",
                                          data={"product_permalink": PRODUCT_PERMALINK_ALL, "license_key": key}).json()
                        if r2.get("success"):
                            st.session_state["unlocked_biz"] = True
                            st.rerun()
                        else:
                            st.error("Invalid License Key")
                except:
                    st.error("Connection Error")

        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 6-3. 결과 리포트
if st.session_state["unlocked_biz"]:
    st.divider()
    u_info = calculate_day_gan(u_dob)
    p_info = calculate_day_gan(p_dob)
    
    def map_elem(e):
        m = {'甲':'Wood','乙':'Wood','丙':'Fire','丁':'Fire','戊':'Earth','己':'Earth','庚':'Metal','辛':'Metal','壬':'Water','癸':'Water'}
        return m.get(e, e)

    u_elem_en = map_elem(u_info['element'])
    p_elem_en = map_elem(p_info['element'])

    report = get_biz_report(u_elem_en, p_elem_en, lang)
    
    # (A) 대결 구도 카드
    c1, c2, c3 = st.columns([1, 0.2, 1])
    with c1:
        st.markdown(f"""
        <div class='user-card'>
            <div class='user-role'>ME ({u_gender})</div>
            <div class='user-name'>{u_name}</div>
            <div class='user-elem'>{u_info['element']} ({u_elem_en})</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='vs-badge'>🤝</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='user-card'>
            <div class='user-role'>PARTNER ({p_gender})</div>
            <div class='user-name'>{p_name}</div>
            <div class='user-elem'>{p_info['element']} ({p_elem_en})</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # (B) 메인 리포트
    # 중요: 아래 문자열에서 HTML 태그 앞의 들여쓰기를 제거했습니다.
    html_content = f"""<div class='report-container'>
<div class='score-display'>{t['lbl_score']}: {report['score']}</div>
<h2 style='text-align:center; color:#1e40af; margin-bottom:40px; border-bottom:1px solid #e2e8f0; padding-bottom:20px;'>{report['title']}</h2>

<div class='section-box'>
<div class='section-title'>{t['lbl_syn']}</div>
<div class='content-text'>{report['synergy']}</div>
</div>

<div class='section-box'>
<div class='section-title'>{t['lbl_fin']}</div>
<div class='content-text'>{report['finance']}</div>
</div>

<div class='section-box' style='background-color:#f1f5f9; padding:20px; border-radius:10px; border:1px solid #e2e8f0;'>
<div class='section-title' style='color:#ec4899; border-left-color:#ec4899;'>{t['lbl_rol']}</div>
<div class='content-text' style='font-weight:bold; color:#334155; text-align:center;'>{report['role']}</div>
</div>

<div style='margin-top:30px;'>
<div class='section-title' style='color:#d97706; border-left-color:#d97706;'>{t['lbl_adv']}</div>
<div class='content-text' style='white-space: pre-line; color:#1e293b; font-weight:500;'>{report['advice']}</div>
</div>
</div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.write("")
    components.html(
        f"""<script>function printParent() {{ window.parent.print(); }}</script>
        <div style="text-align:center;">
            <button onclick="printParent()" style="background-color:#2563eb; color:white; border:none; padding:15px 30px; border-radius:30px; cursor:pointer; font-weight:bold; font-size:16px; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);">
            {t['btn_print']}
            </button>
        </div>""", height=100
    )
