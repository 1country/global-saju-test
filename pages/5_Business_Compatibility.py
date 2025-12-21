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
        "Same": { # 비견 (비즈니스 형제/공동 창업자)
    "score": 80,
    "ko": {
        "title": "🤝 어깨를 나란히 하는 '공동 대표': 비즈니스 형제이자 강력한 경쟁자",
        "synergy": "두 사람은 비즈니스 파트너로서 완벽하게 대등한 기운을 가졌습니다. 서로의 야망, 추진력, 그리고 가치관이 흡사하여 창업 초기나 위기 상황에서 전우애에 가까운 폭발적인 시너지를 냅니다. 마치 거울을 보듯 서로의 장단점을 잘 이해하며, 서로를 밀어주고 끌어주는 강력한 '원팀(One-Team)'의 표본이 될 수 있습니다.",
        "finance": "수익 배분과 지분 구조가 이 관계의 생사 확인서입니다. 둘 다 주체성이 강하고 계산이 철저하기 때문에, 보상 체계가 0.1%라도 불투명하면 즉시 자존심 싸움과 신뢰 균열이 발생합니다. 모든 자금 흐름과 이익 공유 비율을 공증 수준으로 문서화하여 감정이 개입할 틈을 없애야 합니다.",
        "role": "공동 대표(Co-CEO) 체제 또는 대외 영업(CEO) vs 내부 운영(COO)의 엄격한 직무 분리",
        "advice": "1. 창업 전 계약서에 지분율과 의사결정 우선권을 명확히 하세요.\n2. 상대의 전문 영역을 존중하고 절대 '지시'하려 들지 마세요.\n3. 서로를 자극하는 선의의 라이벌 의식을 기업 성장의 연료로 쓰세요."
    },
    "en": {
        "title": "🤝 Strategic Equals: Co-Founders and Brothers-in-Arms",
        "synergy": "You are strategic equals in every sense. Your ambitions and drive align perfectly, creating an explosive momentum in the early stages of a venture. Like looking into a mirror, you understand each other's vision, acting as a formidable 'One-Team' that pushes boundaries through shared grit.",
        "finance": "Equity and profit-sharing are the lifelines of this partnership. Since both are independent and meticulous, any ambiguity in compensation triggers instant ego clashes. Every financial transaction and distribution must be documented with legal precision to prevent emotional fallout.",
        "role": "Co-CEO structure or a strict divide: CEO (Vision & Sales) vs. COO (Operations & Systems).",
        "advice": "1. Clarify equity and tie-breaking authority in a formal contract.\n2. Respect individual domains; never 'overstep' into the other's territory.\n3. Leverage your natural rivalry as a catalyst for professional excellence."
    },
    "fr": {
        "title": "🤝 Partenaires Stratégiques : Cofondateurs et Frères d'Armes",
        "synergy": "Vous êtes des égaux stratégiques. Vos ambitions s'alignent parfaitement, créant un élan explosif. Vous agissez comme une équipe soudée, repoussant les limites ensemble.",
        "finance": "L'équité et le partage des bénéfices sont vitaux. L'ambiguïté mène à des chocs d'ego. Documentez tout avec une précision juridique pour éviter les conflits émotionnels.",
        "role": "Structure Co-PDG ou séparation stricte : Ventes vs Opérations.",
        "advice": "1. Clarifiez l'équité par un contrat formel.\n2. Respectez les domaines de chacun ; ne dépassez jamais vos limites.\n3. Utilisez la rivalité comme un moteur de croissance."
    },
    "es": {
        "title": "🤝 Socios Estratégicos: Cofundadores y Hermanos de Armas",
        "synergy": "Son iguales estratégicos. Su ambición se alinea perfectamente, creando un impulso explosivo. Actúan como un 'Equipo Único' formidable que supera fronteras.",
        "finance": "La equidad y el reparto de utilidades son fundamentales. La ambigüedad provoca choques de ego. Todo debe estar documentado para evitar conflictos.",
        "role": "Estructura Co-CEO o división estricta: Ventas vs Operaciones.",
        "advice": "1. Aclare la equidad y la autoridad en un contrato.\n2. Respete los dominios individuales; no invada el territorio del otro.\n3. Use la rivalidad natural para impulsar la excelencia."
    },
    "ja": {
        "title": "🤝 肩を並べる「共同代表」：最強の戦友であり宿命のライバル",
        "synergy": "ビジネスパートナーとして完全に対等なエネルギーを持っています。野心と推進力が似ており、創業期や危機的な状況で爆発的なシナジーを発揮します。鏡を見るようにお互いのビジョンを理解し、高め合う「最強のチーム」を構築できます。",
        "finance": "利益配分と持分比率がこの関係の要です。双方が強い主体性を持つため、報酬体系が少しでも曖昧だと信頼関係が崩壊します。すべての資金の流れを公証レベルで文書化し、感情が入り込む余地をなくすべきです。",
        "role": "共同代表 (Co-CEO) 体制、あるいは営業(CEO)対運営(COO)の厳格な役割分離。",
        "advice": "1. 契約書で持分と最終意思決定権を明確にすること。\n2. 相手の専門領域を尊重し、決して「干渉」しないこと。\n3. お互いを刺激し合うライバル意識を事業成長の燃料に変えること。"
    },
    "zh": {
        "title": "🤝 旗鼓相当的“联合创始人”：事业兄弟与最强竞争者",
        "synergy": "你们是完全平等的商业合伙人。野心、动力和价值观高度契合，在创业初期或处理危机时能产生爆发性的协同效应。你们互为镜像，深知对方的优劣，是那种可以互相托付、共同冲锋的“梦之队”原型。",
        "finance": "利益分配和股权结构是这段关系的生命线。由于双方都极具主见且精于计算，奖励机制哪怕只有0.1%的模糊，也会引发自尊心的对决。必须以公证级的标准将财务细节白纸黑字化，绝不能留有情感干预的余地。",
        "role": "联席CEO（Co-CEO）体制，或严格划分：CEO（外拓营销）vs COO（内部运营）。",
        "advice": "1. 在正式合同中锁定股权比例和最终裁决权。\n2. 尊重对方的专业领地，严禁指手画脚或越权干涉。\n3. 将天然的竞争意识转化为推动企业超越巅峰的动力。"
    }
},
        "Output": { # 식상 (비전 제시자와 기술 실현자)
    "score": 90,
    "ko": {
        "title": "💡 아이디어의 현실화: '비전 제시자'와 '기술 실현자'의 만남",
        "synergy": "당신이 미래의 청사진과 창의적인 기획안을 제시하면, 파트너는 탁월한 기술력과 실행력으로 그것을 시장에 내놓습니다. R&D, 콘텐츠 제작, 디자인, 브랜딩 등 무(無)에서 유(有)를 창조하는 분야에서 최상의 시너지를 발휘하는 궁합입니다.",
        "finance": "당신이 자본과 인프라를 투자하고 파트너가 전문 기술과 노동력을 제공하는 구조가 이상적입니다. 당장의 단기 순익에 연연하기보다, 파트너의 재능이 꽃피워 만들어낼 '미래 자산 가치'에 장기적으로 투자하는 안목이 필요합니다.",
        "role": "당신: 회장 또는 전략 기획(Visionary) | 파트너: 대표이사 또는 기술 총괄(Executor/CTO)",
        "advice": "1. 세부 실무는 전문가인 파트너에게 전적으로 일임하고 마이크로매니징을 지양하세요.\n2. 파트너의 성취감이 수익으로 직결되도록 성과에 따른 파격적인 인센티브를 약속하세요.\n3. 창의적인 결과물이 시장에 안착하기까지 충분한 시간적 여유와 인내심을 가져주세요."
    },
    "en": {
        "title": "💡 Visionary & Executor: A High-Performance Creative Duo",
        "synergy": "You provide the architectural blueprint and creative vision, while your partner employs technical mastery and relentless execution to bring it to life. This is the ultimate partnership for R&D, content creation, and branding where innovation is the core asset.",
        "finance": "A structure where you invest capital and infrastructure, and they invest expertise and sweat equity, works best. Focus on the long-term appreciation of the 'Future Value' created by their talent rather than immediate, short-term quarterly profits.",
        "role": "You: Chairman / Chief Visionary | Partner: CEO / Chief Technology Officer (CTO)",
        "advice": "1. Delegate execution to the expert and avoid micromanagement at all costs.\n2. Ensure high motivation by offering bold, performance-based incentives and equity.\n3. Exercise patience, as high-value creative outputs require time to mature and penetrate the market."
    },
    "fr": {
        "title": "💡 Visionnaire & Exécutant : Le Duo de la Création Pure",
        "synergy": "Vous apportez la vision stratégique, votre partenaire la transforme en réalité tangible. Idéal pour l'innovation, la R&D et le design de luxe. Ensemble, vous transformez les idées en or.",
        "finance": "Vous fournissez le capital, ils apportent le savoir-faire. Misez sur la valorisation à long terme du projet plutôt que sur un profit immédiat.",
        "role": "Vous : Visionnaire / Président | Partenaire : Exécutant / Directeur Technique",
        "advice": "1. Évitez la microgestion et faites confiance à leur expertise technique.\n2. Proposez des incitations généreuses liées aux résultats.\n3. Soyez patient : l'innovation demande du temps pour porter ses fruits."
    },
    "es": {
        "title": "💡 Visionario & Ejecutor: Sinergia Creativa de Alto Nivel",
        "synergy": "Tú aportas la visión y el concepto; tu socio emplea su habilidad técnica para materializarlo. Es la combinación perfecta para sectores de I+D, diseño y marketing digital donde la creatividad es ley.",
        "finance": "Tú inviertes el capital y la infraestructura; ellos su talento y esfuerzo. Valora el crecimiento a largo plazo y la creación de activos futuros sobre la rentabilidad inmediata.",
        "role": "Tú: Visionario / Presidente | Socio: Ejecutor / Director de Tecnología",
        "advice": "1. No interfieras en los detalles de ejecución; deja que el experto trabaje.\n2. Motiva con incentivos audaces basados en el éxito del proyecto.\n3. Mantén la calma y espera a que los resultados creativos maduren en el mercado."
    },
    "ja": {
        "title": "💡 企画者と実行者：創造的インスピレーションの具現化",
        "synergy": "あなたが未来のビジョンと企画を提示し、パートナーがその卓越した技術力で形にします。R&D、コンテンツ制作、デザインなど、ゼロから一を生み出す分野で最高のシナジーを発揮します。",
        "finance": "あなたが資金とインフラを、パートナーが技術と労働力を提供する形が理想的です。目先の利益よりも、パートナーの才能が生み出す「将来の資産価値」に投資する姿勢が成功の鍵です。",
        "role": "あなた：会長 / 戦略企画 (Visionary) | パートナー：社長 / 技術統括 (CTO)",
        "advice": "1. 実務は専門家であるパートナーに一任し、細かな干渉（マイクロマネジ먼ト）は避けましょう。\n2. 成果に応じた魅力的なインセンティブを約束し、モチベーションを維持してください。\n3. 独創的な成果が市場に浸透するまで、十分な忍耐と時間を惜しまないでください。"
    },
    "zh": {
        "title": "💡 愿景领袖与硬核执行者：将创意点石成金",
        "synergy": "你提供战略蓝图和创意愿景，伙伴凭借卓越的技术能力和执行力将其转化为现实。在研发、内容创作、品牌设计等需要“无中生有”的领域，你们是无可替代的黄金搭档。",
        "finance": "理想模式是你提供资金和资源平台，对方投入专业技能与精力。应着眼于对方才华所创造的“长期股权价值”，而非仅仅关注眼前的短期营收。",
        "role": "你：董事长 / 首席愿景官 | 伙伴：CEO / 首席技术官 (CTO)",
        "advice": "1. 将具体执行完全交给专业的伙伴，切忌事无巨细的微观管理。\n2. 通过与成果挂钩的激励机制或股权，确保伙伴的创造力得到充分释放。\n3. 给创意产品留出成长期，耐心等待市场对高价值作品的反馈。"
    }
},
        "Wealth": { # 재성 (자본가와 자산 운용가)
    "score": 85,
    "ko": {
        "title": "💰 오너와 전문경영인: 현실적 이익을 극대화하는 '황금 파트너십'",
        "synergy": "당신이 전략적 의사결정과 전체적인 주도권을 쥐고 시스템을 관리하며, 파트너는 현장의 최전선에서 실질적인 매출과 이익을 창출해옵니다. 비즈니스의 목적이 명확한 이윤 추구라면 더할 나위 없이 가장 이상적인 '자본과 노동'의 결합입니다.",
        "finance": "재물운이 비약적으로 상승하는 궁합입니다. 파트너가 벌어오는 자금을 당신이 투명하고 견고하게 관리할 때 시너지가 완성됩니다. 자금의 유입과 유출, 즉 캐시플로우(Cash Flow)를 당신이 완벽하게 통제하고 있어야 리스크를 방지할 수 있습니다.",
        "role": "당신: 오너 및 이사회 의장 (Owner/Investor) | 파트너: 영업 총괄 및 실무 대표 (CEO/Sales Director)",
        "advice": "1. 성과에 따른 확실하고 투명한 보상(Incentive) 체계를 구축하세요.\n2. 파트너를 단순한 직원이 아닌, 비즈니스를 함께 키우는 인격적 동반자로 예우하세요.\n3. 핵심 실무 역량에 대해서는 믿을 수 있는 범위 내에서 과감하게 권한을 위임하여 효율을 높이세요."
    },
    "en": {
        "title": "💰 Owner & Professional Manager: The 'Gold Standard' Profit Partnership",
        "synergy": "You hold the reins of strategic governance while your partner drives frontline revenue. It is the most efficient 'Capital and Labor' synergy for businesses solely focused on profit maximization and market expansion.",
        "finance": "Peak financial energy. Synergy is completed when you manage the capital your partner earns with transparency and rigor. You must maintain a firm grip on the cash flow to safeguard the enterprise's sustainability.",
        "role": "You: Owner & Chairman (Investor) | Partner: CEO & Sales Director (Operations Head)",
        "advice": "1. Build a robust and transparent performance-based incentive system.\n2. Treat your partner as a professional peer, not just a subordinate.\n3. Delegate operational authority boldly within trusted limits to maximize agility."
    },
    "fr": {
        "title": "💰 Propriétaire & Gestionnaire : Le Partenariat pour le Profit Maximal",
        "synergy": "Vous dirigez la stratégie tandis que votre partenaire génère les revenus. C'est la synergie idéale entre le capital et l'exécution pour maximiser les gains.",
        "finance": "Excellente chance financière. Vous gérez avec rigueur les capitaux rapportés par votre partenaire. Le contrôle du flux de trésorerie est votre priorité absolue.",
        "role": "Vous : Propriétaire (Investisseur) | Partenaire : Gestionnaire (Direction des Ventes)",
        "advice": "1. Mettez en place des primes de performance claires.\n2. Traitez votre partenaire comme un allié de valeur, avec respect.\n3. Déléguez le pouvoir décisionnel sur le terrain pour plus d'efficacité."
    },
    "es": {
        "title": "💰 Dueño & Gerente Profesional: Alianza Orientada a Beneficios",
        "synergy": "Tú lideras la estrategia y el sistema, mientras tu socio genera ingresos en primera línea. Es la combinación perfecta de capital y ejecución para empresas enfocadas en el lucro.",
        "finance": "Máxima suerte financiera. Tú gestionas el capital que tu socio produce. Mantener el control total del flujo de caja es esencial para evitar riesgos.",
        "role": "Tú: Dueño (Inversionista) | Socio: Gerente General (Director Comercial)",
        "advice": "1. Establece un sistema de incentivos basado en resultados tangibles.\n2. Trata a tu socio como un compañero profesional estratégico.\n3. Delega autoridad operativa sabiamente para fomentar el crecimiento rápido."
    },
    "ja": {
        "title": "💰 オーナーと専門経営者：実利を極大化する「黄金の相性」",
        "synergy": "あなたが戦略的意思決定と主導権を握り、パートナーが最前線で実質的な利益を稼ぎ出します。利益追求を目的とするビジネスにおいて、これ以上ない理想的な「資本と労働」の結合です。",
        "finance": "金運が飛躍的に上昇します。パートナーが稼いできた資金を、あなたが透明性を持って堅実に管理することで相乗効果が完成します。キャッシュフローをあなたが完全に掌握することが不可欠です。",
        "role": "あなた：オーナー・会長 (投資家) | パートナー：営業総括・実務代表 (CEO)",
        "advice": "1. 成果に応じた明確で透明なインセンティブ体系を構築してください。\n2. パート너を単なる部下ではなく、ビジネスを共に育てる対等なパートナーとして礼遇してください。\n3. 信頼できる範囲内で大胆に権限を委譲し、現場の効率を高めてください。"
    },
    "zh": {
        "title": "💰 资本持有人与职业经理人：利益最大化的“黄金拍档”",
        "synergy": "你掌握战略决策权和系统主导权，伙伴则在市场一线创造实际利润。如果企业的核心目标是盈利，这便是最理想的“资本与执行”的结合模式。",
        "finance": "财运呈指数级增长。当伙伴赚取利润，由你进行稳健且透明的资金管理时，协同效应达到最强。你必须牢牢掌控现金流，以规避潜在财务风险。",
        "role": "你：老板/董事长 (投资方) | 伙伴：总经理/销售总监 (执行方)",
        "advice": "1. 建立一套基于结果的、明确且透明的激励机制。\n2. 将伙伴视为共同成长的商业人格化同伴，给予应有的尊重。\n3. 在可控范围内大胆放权，让专业的人做专业的事，提升经营效率。"
    }
},
        "Power": { # 관성 (리스크 관리자와 대외 협력가)
    "score": 75,
    "ko": {
        "title": "⚖️ 시스템과 규율: 위기에 강한 '안정적 성장'의 정석",
        "synergy": "파트너가 조직의 주도권을 쥐고 엄격한 원칙과 규율을 요구하는 구조입니다. 때로는 통제받는 기분에 답답할 수 있으나, 위기 상황에서 파트너의 리스크 관리 능력은 타의 추종을 불허합니다. 이는 마치 프랜차이즈 본사(파트너)의 매뉴얼에 따라 운영하는 점주(본인)의 관계처럼, 검증된 시스템 안에서 안전하게 성장하는 모델입니다.",
        "finance": "일확천금의 대박보다는 지속 가능한 '우상향 곡선'을 지향합니다. 파트너가 재무 결재권과 예산 통제권을 가질 때 기업의 현금 흐름이 가장 탄탄해집니다. 보수적인 자금 운용이 장기적으로는 더 큰 자산을 지켜내는 열쇠가 됩니다.",
        "role": "당신: 대외 홍보 및 전략 영업 (Face/Brand Ambassador) | 파트너: 최고 경영자 및 시스템 관리 (CEO/System Controller)",
        "advice": "1. 파트너가 구축한 가이드라인과 규칙을 충실히 따르는 것이 결과적으로 이득입니다.\n2. 파트너의 냉철한 비판과 쓴소리를 조직을 건강하게 만드는 보약으로 여기세요.\n3. 화려한 주인공보다 실속 있는 2인자(2인체제)로서의 역할을 즐길 때 성공이 다가옵니다."
    },
    "en": {
        "title": "⚖️ Structured Growth: The Power of Discipline and Risk Mitigation",
        "synergy": "Your partner exercises strategic control, demanding adherence to strict principles. While it may feel restrictive, their ability to mitigate risk is unparalleled. This mirrors the relationship between a Franchise HQ (Partner) and a Franchisee (You), where following a proven manual leads to predictable success.",
        "finance": "Prioritizes long-term stability over risky windfalls. Financial health is optimized when your partner manages the budget and approvals. Their conservative financial oversight is the key to preserving wealth during market volatility.",
        "role": "You: Public Relations & Strategic Sales (The Face) | Partner: CEO & Operations Management (The Controller)",
        "advice": "1. Adhering to the partner's established systems will yield the best results.\n2. Treat their blunt feedback as essential for organizational health.\n3. Embrace your role as a strategic Number Two to find collective prosperity."
    },
    "fr": {
        "title": "⚖️ Croissance Structurée : La Force de la Discipline",
        "synergy": "Votre partenaire impose des règles strictes. Bien que cela puisse sembler restrictif, leur gestion des risques est exceptionnelle. C'est une croissance sécurisée au sein d'un système éprouvé.",
        "finance": "La stabilité avant tout. La santé financière de l'entreprise est au plus haut lorsqu'ils contrôlent les flux de trésorerie. Une gestion prudente est la clé de votre pérennité.",
        "role": "Vous : Relations Publiques (L'Image) | Partenaire : Contrôleur / PDG",
        "advice": "1. Suivre leurs règles est votre meilleur atout.\n2. Écoutez leurs critiques constructives.\n3. Acceptez d'être le bras droit stratégique pour réussir."
    },
    "es": {
        "title": "⚖️ Crecimiento Estructurado: Disciplina y Mitigación de Riesgos",
        "synergy": "Tu socio establece principios rigurosos. Aunque te sientas limitado, su capacidad para evitar riesgos es infalible. Es un modelo de éxito basado en seguir un manual probado.",
        "finance": "Estabilidad sobre apuestas arriesgadas. La solvencia mejora cuando el socio gestiona el presupuesto. Su visión conservadora protege el capital a largo plazo.",
        "role": "Tú: Relaciones Públicas (La Cara) | Socio: Controlador / CEO",
        "advice": "1. Seguir sus sistemas te traerá los mejores beneficios.\n2. Valora sus consejos críticos como medicina para el negocio.\n3. Acepta tu papel como el número dos estratégico."
    },
    "ja": {
        "title": "⚖️ 規律とシステム：危機に強い「安定的成長」のモデル",
        "synergy": "パートナーが主導権を握り、厳格な原則と規律を求める構造です。拘束感を感じることもありますが、そのリスク管理能力は卓越しています。本部のマニュアルに従う加盟店のように、検証されたシステムの中で安全に成長できる相性です。",
        "finance": "一攫千金よりも持続可能な成長を志向します。パートナーが財務権限を持つことで、企業のキャッシュフローは最も強固になります。保守的な資金運用が、長期的には大きな資産を守る鍵となります。",
        "role": "あなた：対外広報および戦略営業 (Face) | パートナー：最高経営責任者および管理 (Controller)",
        "advice": "1. 相手が構築したガイドラインに忠実に従うことが、結果的に利益に繋がります。\n2. 相手の冷徹な苦言を、組織を健康にする良薬として受け入れてください。\n3. 主役の座にこだわらず、実利を取るNo.2としての役割を全うしてください。"
    },
    "zh": {
        "title": "⚖️ 制度与规范：稳打稳扎的“稳健成长”范본",
        "synergy": "伙伴掌握主导权并要求遵守严格的原则。虽然可能感到束缚，但对方的风险管控能力极其出色。这类似于总部（伙伴）与加盟商（你）的关系，在经过验证的系统内安全扩张。",
        "finance": "求稳不求快，追求可持续的增长曲线。当伙伴掌握财务审批权时，公司的现金流最为稳健。保守的财务管理是长期守护资产的关键。",
        "role": "你：公关与战略销售 (门面) | 伙伴：首席执行官与系统控制 (管理者)",
        "advice": "1. 忠实执行伙伴制定的规则和流程将使你获益最丰。\n2. 将对方的逆耳忠言视为增强组织免疫力的良药。\n3. 享受身为“实力派二把手”的角色，这才是通往成功的捷径。"
    }
},
        "Resource": { # 인성 (지적 자산과 무조건적 지원의 에너지)
    "score": 95,
    "ko": {
        "title": "🍼 멘토와 후원자: 무한 신뢰를 바탕으로 한 '최고의 조력 관계'",
        "synergy": "파트너가 당신의 역량과 비전을 전적으로 믿고 전폭적인 지지를 보내주는 관계입니다. 당신이 현장에서 겪는 심리적 압박을 파트너가 완벽하게 방어해주며, 부족한 경험을 지혜로 채워줍니다. 엔젤 투자자(파트너)와 혁신적인 스타트업 대표(본인)로서 만났을 때 세상에 없던 폭발적인 가치를 만들어냅니다.",
        "finance": "직접적인 매출 발생만큼이나 중요한 '문서 운'과 '자산 운'이 대길합니다. 파트너의 강력한 네트워킹과 신용을 담보로 유리한 계약을 따내거나, 브랜드 가치를 단숨에 끌어올릴 수 있습니다. 파트너의 존재 자체가 당신 비즈니스의 가장 강력한 자본금이 됩니다.",
        "role": "당신: 실무 총괄 및 의사결정권자 (CEO/Operator) | 파트너: 명예 회장 및 시니어 고문 (Mentor/Advisor)",
        "advice": "1. 파트너의 헌신적인 지원을 결코 당연한 권리로 여기지 말고 늘 감사를 표하세요.\n2. 파트너의 조언을 경청하되, 비즈니스의 최종 책임과 결정은 반드시 본인이 직접 내려야 합니다.\n3. 파트너가 당신의 성장을 지켜보는 기쁨을 누릴 수 있도록 사업 비전을 수시로 투명하게 공유하세요."
    },
    "en": {
        "title": "🍼 Mentor & Protege: The Ultimate Strategic Alliance of Faith",
        "synergy": "Your partner trusts your potential and vision unconditionally, providing unwavering spiritual and material support. They act as a psychological shield, filling your gaps with wisdom. This is the gold standard for an Angel Investor (Partner) and an innovative Tech Founder (You) seeking to change the world.",
        "finance": "Extraordinary luck with intellectual property, contracts, and asset acquisition. Your brand value escalates rapidly through their credibility and network. Their very involvement serves as your most significant capital and market trust factor.",
        "role": "You: Chief Executive & Decision Maker (CEO) | Partner: Chairman & Senior Advisor (The Mentor)",
        "advice": "1. Never take their devoted support for granted; gratitude is the currency of this bond.\n2. Listen deeply to their wisdom, but ensure you take ultimate ownership of final decisions.\n3. Maintain transparency by sharing your growth milestones and long-term vision frequently."
    },
    "fr": {
        "title": "🍼 Mentor & Protégé : L'Alliance Sacrée du Soutien Inconditionnel",
        "synergy": "Votre partenaire croit totalement en votre vision. Ils agissent comme un bouclier contre la pression extérieure. C'est la relation idéale entre un investisseur providentiel et un entrepreneur visionnaire.",
        "finance": "Grande chance avec les contrats et la propriété intellectuelle. Votre valeur de marque explose grâce à leur réseau. Leur soutien est votre plus grand capital confiance.",
        "role": "Vous : PDG et Décisionnaire | Partenaire : Mentor / Conseiller Stratégique",
        "advice": "1. Ne prenez jamais leur soutien pour acquis ; la reconnaissance est essentielle.\n2. Écoutez leurs conseils, mais assumez la responsabilité finale de chaque décision.\n3. Partagez régulièrement vos succès et vos doutes pour maintenir la confiance."
    },
    "es": {
        "title": "🍼 Mentor & Protegido: La Alianza Estratégica de Confianza Total",
        "synergy": "Tu socio confía plenamente en tu visión y te brinda un apoyo incondicional. Actúan como tu base sólida, cubriendo tus debilidades con su experiencia. Es la relación perfecta entre un inversor ángel y un fundador innovador.",
        "finance": "Excelente suerte en contratos y adquisición de activos. El valor de tu marca crece rápidamente gracias a su prestigio. Su respaldo es el pilar de tu solvencia ante el mercado.",
        "role": "Tú: CEO y Líder de Decisiones | Socio: Mentor / Consejero Senior",
        "advice": "1. No des su apoyo por sentado; la gratitud fortalece este vínculo comercial.\n2. Valora su sabiduría, pero toma la propiedad total de las decisiones finales.\n3. Comparte tu visión y los hitos de crecimiento para que se sientan parte del éxito."
    },
    "ja": {
        "title": "🍼 メンターと後援者：無限の信頼が築く「最高のパートナーシップ」",
        "synergy": "パートナーがあなたの能力とビジョンを全面的に信じ、物心両面で強力にバックアップしてくれる関係です。あなたが現場で感じる重圧を和らげ、経験不足を知恵で補ってくれます。投資家（パートナー）とスタートアップ代表（あなた）として、革新的な価値を創出するのに理想的な組み合わせです。",
        "finance": "契約運や文書運、そして資産運が非常に好調です。パートナーの強力なネットワークや社会的信用を背景に、有利な条件での契約やブランド価値の向上を実現できます。パートナーの存在自体が、あなたの事業における最大の無形資産となります。",
        "role": "あなた：実務統括・意思決定者 (CEO) | パートナー：会長・シニア顧問 (Mentor)",
        "advice": "1. 献身的な支援を当然の権利と思わず、常に感謝の意を伝えてください。\n2. 相手の助言を大切にしながらも、最終的な決断と責任は自らが負う姿勢を貫いてください。\n3. 事業のビジョンや進捗をこまめに共有し、共に成長を喜べる関係を維持しましょう。"
    },
    "zh": {
        "title": "🍼 导师与被辅佐者：基于绝对信任的“顶级背书”",
        "synergy": "伙伴对你的潜力和愿景有着无条件的信任，并提供全方位的精神与物质支持。TA是你事业上的避风港，用智慧弥补你的短板。这是天使投资人（伙伴）与创新创业家（你）共同改变世界的完美模式。",
        "finance": "在知识产权、合同签署及资产获取方面运势极佳。凭借伙伴的社会信誉和资源网络，你的品牌价值将迅速跃升。伙伴的参与本身就是你最核心的无形资本和市场信任状。",
        "role": "你：首席执行官/实务决策者 (CEO) | 伙伴：董事长/高级顾问 (导师)",
        "advice": "1. 绝不要把对方的无私支持视为理所当然，感恩是维持这种关系的基础。\n2. 深度倾听对方的智慧，但必须确保自己拥有最终决策的自主权。\n3. 定期分享你的成长里程碑和长远愿景，让伙伴见证并参与你的成功。"
    }
},
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
# 6. 메인 로직 (🚨 수정된 부분: 흰색 박스 제거)
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

# 6-1. 파트너 정보 입력 (박스 제거됨)
st.markdown(f"<h3 style='color:#1e3a8a; text-shadow:1px 1px 0 #fff; margin-bottom:15px;'>{t['p_info_title']}</h3>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    p_name = st.text_input(t['p_name'])
with c2:
    p_dob = st.date_input(t['p_dob'], min_value=date(1900,1,1), value=date(1990,1,1))
with c3:
    p_gender = st.selectbox(t['p_gender'], ["Male", "Female"])

st.write("") # 간격

# 6-2. 잠금 및 결제 (흰 박스 완벽 제거 버전)
if "unlocked_biz" not in st.session_state: 
    st.session_state["unlocked_biz"] = False

if not st.session_state["unlocked_biz"]:
    st.divider()
    
    # 🚨 [수정] 박스를 만드는 모든 div와 border 옵션을 제거했습니다.
    st.markdown(f"<h3 style='color:#ec4899; text-align:center; text-shadow: 1px 1px 2px white;'>{t['lock_title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#475569; text-align:center; font-weight:bold;'>{t['lock_desc']}</p>", unsafe_allow_html=True)
    
    # 구매 버튼 섹션
    c1, c2 = st.columns(2)
    with c1: 
        st.link_button(t['btn_buy_sp'], GUMROAD_LINK_SPECIFIC, use_container_width=True)
    with c2: 
        st.link_button(t['btn_buy_all'], GUMROAD_LINK_ALL, use_container_width=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True) # 미세 간격 조정
    
    # 라이선스 키 입력창 (중앙 정렬 효과를 위해 빈 컬럼 활용 가능)
    key = st.text_input("🔑 License Key (결제 후 받은 키를 입력하세요)", type="password")
    
    # 분석하기 버튼
    if st.button(t['btn_unlock'], type="primary", use_container_width=True):
        if not p_name:
            st.error("Please enter partner name.")
        else:
            # 1. 마스터 키 (무제한) 확인
            if key == UNLOCK_CODE:
                st.session_state["unlocked_biz"] = True
                st.success("Master Unlocked!")
                st.rerun()
            
            # 2. 검로드 라이센스 확인
            try:
                # (A) 단품(Business Compatibility) 키 확인 (3회 제한)
                r1 = requests.post("https://api.gumroad.com/v2/licenses/verify",
                                  data={
                                      "product_permalink": PRODUCT_PERMALINK_SPECIFIC, 
                                      "license_key": key,
                                      "increment_uses_count": "true" 
                                  }).json()
                
                if r1.get("success"):
                    if r1.get("uses", 0) > 3: 
                        st.error(f"🚫 Usage limit exceeded (Max 3)")
                    else:
                        st.session_state["unlocked_biz"] = True
                        st.rerun()
                else:
                    # (B) 올패스(All-Access) 키 확인 (합산 10회 제한)
                    r2 = requests.post("https://api.gumroad.com/v2/licenses/verify",
                                      data={
                                          "product_permalink": PRODUCT_PERMALINK_ALL, 
                                          "license_key": key,
                                          "increment_uses_count": "true"
                                      }).json()
                    
                    if r2.get("success"):
                        if r2.get("uses", 0) > 10: 
                            st.error(f"🚫 Usage limit exceeded (Max 10)")
                        else:
                            st.session_state["unlocked_biz"] = True
                            st.rerun()
                    else:
                        st.error("Invalid License Key")
            except:
                st.error("Connection Error")

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
