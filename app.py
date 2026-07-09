import streamlit as st
import math  

# --- 網頁外觀設定 ---
st.set_page_config(
    page_title="NICU智慧計算機", 
    page_icon="👶", 
    layout="wide"
)

# --- 🎨 頁面空間物理大瘦身 CSS 注入 ---
st.markdown("""
    <style>
        .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
        h2, h3, h4 {margin-top: 0px !important; margin-bottom: 4px !important; padding-top: 0px !important;}
        div[data-testid="stForm"] {padding: 5px;}
        hr {margin-top: 5px !important; margin-bottom: 8px !important;}
        section[data-testid="stSidebar"] .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# 頂部標題列
col_title, col_sub = st.columns([2, 3])
with col_title:
    st.markdown("<h2 style='font-size:24px; margin:0;'>👶 NICU智慧計算機</h2>", unsafe_allow_html=True)
with col_sub:
    st.markdown("<p style='margin:6px 0 0 0; color:#888; font-size:13px;'>🔒 兒科/新生兒加護病房專用 | 臨床決策支援系統 (CDSS)</p>", unsafe_allow_html=True)

st.write("---")

# --- 側邊欄：基本資料輸入 ---
st.sidebar.header("📥 病童基本資料輸入")
b1_bw = st.sidebar.number_input("BW 體重 (kg)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

st.sidebar.write("---")
st.sidebar.markdown("**GA 胎齡**")
f1_ga_wk = st.sidebar.number_input("GA 週數", min_value=0, max_value=45, value=0, step=1)
h1_ga_day = st.sidebar.number_input("GA 天數", min_value=0, max_value=6, value=0, step=1)

st.sidebar.write("---")
l1_pna = st.sidebar.number_input("PNA 出生天數 (days)", min_value=0, max_value=365, value=0, step=1)

# 後台核心數據計算
ga_total_days = (f1_ga_wk * 7) + h1_ga_day
pma_total_days = ga_total_days + l1_pna
q1_pma_wk = pma_total_days // 7
s1_pma_day = pma_total_days % 7

# =============================================================================
# 🛠️ 全局分頁大開關 —— 擴充 8 大核心面板版
# =============================================================================
st.sidebar.write("---")
st.sidebar.header("🎯 核心功能導航")
main_page = st.sidebar.radio(
    "請選擇主要調配面板：",
    [
        "💊 常用藥物計算機", 
        "⚡ Ion dosage", 
        "🫁 DART.BURST", 
        "🔌 升壓劑.止痛鎮靜pump", 
        "🩸 Vasopressin pump", 
        "🧬 Prostaglandin E1與利尿劑pump", 
        "💉 Insulin pump", 
        "💤 Dexmedetomidine"
    ],
    key="main_page_navigator"
)

# 只有在「常用藥物計算機」被選中時，側邊欄才秀出那九大分類，視覺超乾淨！
category = "1. Antimicrobial agents"
if main_page == "💊 常用藥物計算機":
    st.sidebar.write("---")
    st.sidebar.header("📁 藥物類別選擇")
    category = st.sidebar.radio(
        "請直接點選常用藥物大項：",
        [
            "1. Antimicrobial agents",
            "2. Diuretics",
            "3. PDA",
            "4. 肺高壓",
            "5. Apnea/RDS Surfactant",
            "6. Seizure control",
            "7. Sedation",
            "8. Miscellaneous.GCSF",
            "9. 胃腸類藥品/營養補充品/維他命/其它"
        ],
        key="nicu_main_category"
    )

# --- 📊 當前病患生理指標核對 ---
has_input = (b1_bw > 0 and f1_ga_wk > 0)

if has_input:
    st.markdown(
        f"""
        <div style='display: flex; gap: 15px; align-items: center; background-color: #1a1a1a; padding: 6px 12px; border-radius: 4px; border-left: 4px solid #1E88E5;'>
            <span style='font-size:14px; font-weight:bold; color:#ccc;'>📊 生理指標核對：</span>
            <span style='font-size:14px; color:#fff;'>👶 <b>BW:</b> <span style='color:#1E88E5; font-weight:bold;'>{b1_bw:.2f} kg</span></span>
            <span style='font-size:14px; color:#fff;'>| &nbsp;⏳ <b>GA:</b> <b>{f1_ga_wk} 週 + {h1_ga_day} 天</b></span>
            <span style='font-size:14px; color:#fff;'>| &nbsp;🧮 <b>PMA:</b> <span style='color:#4CAF50; font-weight:bold;'>{q1_pma_wk} 週 + {s1_pma_day} 天</span></span>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style='padding: 6px 12px; background-color: #2b2214; border-left: 4px solid #ffb300; border-radius: 4px; font-size:13px; color:#ffe082;'>
            ⚠️ <b>系統提示</b>：請先於左側輸入「BW 體重」及「GA 週數」，系統將即時啟動臨床核對與劑量計算。
        </div>
        """, 
        unsafe_allow_html=True
    )

st.write("---")

# =============================================================================
# 💊 區塊 1: 常用藥物計算機
# =============================================================================
if main_page == "💊 常用藥物計算機":
    if not has_input:
        st.info("💡 正在等待左側輸入病患基本資料...")
    else:
        st.markdown(f"<h3 style='margin:0px 0px 10px 0px;'>📂 當前分類：{category}</h3>", unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # 分類 1: Antimicrobial agents
        # ---------------------------------------------------------------------
        if category == "1. Antimicrobial agents":
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            with r1_c1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Ampicillin**")
                    if ga_total_days <= 244:
                        amp_b4 = b1_bw * 50 if l1_pna <= 7 else b1_bw * 75; amp_d4 = "Q12H"; norm_ok = True
                    else:
                        if l1_pna <= 28: amp_b4 = b1_bw * 50; amp_d4 = "Q8H"; norm_ok = True
                        else: amp_b4 = "超過28天(請手動確認)"; norm_ok = False
                    if norm_ok: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b4:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d4}</span></p>", unsafe_allow_html=True)
                    else: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {amp_b4}</p>", unsafe_allow_html=True)
                    amp_b5 = b1_bw * 100 if l1_pna <= 7 else b1_bw * 75; amp_d5 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b5:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d5}</span></p>", unsafe_allow_html=True)
                    amp_b6 = b1_bw * 50; amp_d6 = "60 mins prior"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Surgical prophylaxis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>{amp_d6}</span></p>", unsafe_allow_html=True)
            with r1_c2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Cefotaxime**")
                    if b1_bw <= 2: ctx_b8 = b1_bw * 50 if l1_pna <= 28 else "超過28天(請手動確認)"; ctx_b8_ok = False if l1_pna > 28 else True
                    else:
                        if l1_pna <= 7: ctx_b8 = b1_bw * 50; ctx_b8_ok = True
                        elif l1_pna <= 28: ctx_b8 = b1_bw * 37.5; ctx_b8_ok = True
                        else: ctx_b8 = b1_bw * 50 if l1_pna <= 60 else "超過60天(請手動確認)"; ctx_b8_ok = False if l1_pna > 60 else True
                    if b1_bw <= 2: ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else "確認醫囑")
                    else: ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    if ctx_b8_ok: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b8:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d8}</span></p>", unsafe_allow_html=True)
                    else: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {ctx_b8}</p>", unsafe_allow_html=True)
                    ctx_b9 = b1_bw * 50; ctx_d9 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b9:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d9}</span></p>", unsafe_allow_html=True)
            with r1_c3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Gentamicin**")
                    if ga_total_days <= 209: gen_b11 = b1_bw * 5
                    else: gen_b11 = b1_bw * 4 if l1_pna <= 7 else b1_bw * 5
                    if ga_total_days <= 209: gen_d11 = "Q36H" if l1_pna <= 14 else "Q24H"
                    else: gen_d11 = "Q36H" if l1_pna <= 10 else "QD"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{gen_b11:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{gen_d11}</span></p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r2_c1, r2_c2, r2_c3 = st.columns(3)
            with r2_c1:
                with st.container(border=True):
                    st.markdown("## 🟧 **Cefazolin**")
                    if l1_pna <= 28: cfz_b13 = b1_bw * 25 if b1_bw <= 2 else b1_bw * 50; cfz_b13_ok = True
                    else: cfz_b13 = b1_bw * 150 / 4 if l1_pna <= 60 else "超過60天(請手動確認)"; cfz_b13_ok = False if l1_pna > 60 else True
                    cfz_d13 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    if cfz_b13_ok: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{cfz_b13:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d13}</span></p>", unsafe_allow_html=True)
                    else: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {cfz_b13}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Perioperative dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>30-60 mins prior</span></p>", unsafe_allow_html=True)
                    cfz_d15 = "Q12H" if l1_pna <= 7 else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Postoperative dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d15}</span></p>", unsafe_allow_html=True)
            with r2_c2:
                with st.container(border=True):
                    st.markdown("### 🟪 **Piperacillin + Tazobactam**")
                    if b1_bw <= 2: pt_b17 = b1_bw * 112.5 if l1_pna <= 7 else (b1_bw * 112.5 if q1_pma_wk <= 30 else b1_bw * 90); pt_d17 = "Q8H" if l1_pna <= 7 else ("Q8H" if q1_pma_wk <= 30 else "Q6H")
                    else: pt_b17 = b1_bw * 90; pt_d17 = "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pt_b17:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{pt_d17}</span></p>", unsafe_allow_html=True)
            with r2_c3:
                with st.container(border=True):
                    st.markdown("### 🟫 **Amoxicillin + Clavulanate (IV)**")
                    amx_iv_b19 = min(1200.0, b1_bw * 30); amx_iv_d19 = "Q8H" if (ga_total_days >= 90 and l1_pna >= 4) else "Q12H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_iv_b19:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amx_iv_d19}</span></p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r3_c1, r3_c2, r3_c3 = st.columns(3)
            with r3_c1:
                with st.container(border=True):
                    st.markdown("### 🧪 **Amoxicillin + Clavulanate (PO)**")
                    amx_po_b21 = b1_bw * 0.3
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_po_b21:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span> <span style='font-size: 17px; color: #F4511E; margin-left: 8px;'>Q12H</span></p>", unsafe_allow_html=True)
            with r3_c2:
                with st.container(border=True):
                    st.markdown("## 🛸 **Meropenem**")
                    mrp_b23 = b1_bw * 20 if ga_total_days <= 223 else (b1_bw * 20 if l1_pna < 14 else b1_bw * 30)
                    mrp_d23 = "Q12H" if (ga_total_days <= 223 and l1_pna < 14) else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b23:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d23}</span></p>", unsafe_allow_html=True)
                    mrp_b24_ok = True if l1_pna <= 60 else False; mrp_b24 = b1_bw * 40 if mrp_b24_ok else "超過60天(請手動確認)"
                    mrp_d24 = ("Q12H" if l1_pna < 14 else "Q8H") if b1_bw <= 2 else "Q8H"
                    if mrp_b24_ok: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b24:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d24}</span></p>", unsafe_allow_html=True)
                    else: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {mrp_b24}</p>", unsafe_allow_html=True)
            with r3_c3:
                with st.container(border=True):
                    st.markdown("### 🥊 **Vancomycin (Initial)**")
                    vnc_b26 = b1_bw * 15; vnc_d26 = "Q24H" if (ga_total_days + l1_pna) < 203 else ("Q12H" if (ga_total_days + l1_pna) < 252 else "Q8H")
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Initial dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b26:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d26}</span></p>", unsafe_allow_html=True)
                    vnc_b27_ok = False if b1_bw < 2 else True; vnc_b27 = (b1_bw * 10 if l1_pna <= 7 else b1_bw * 11.25) if vnc_b27_ok else "體重<2kg(請手動確認)"
                    vnc_d27 = "Q8H" if l1_pna <= 7 else "Q6H"
                    if vnc_b27_ok: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b27:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d27}</span></p>", unsafe_allow_html=True)
                    else: st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {vnc_b27}</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r4_c1, r4_c2, r4_c3 = st.columns(3)
            with r4_c1:
                with st.container(border=True):
                    st.markdown("### 🛡️ **Teicoplanin**")
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{16 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Day 1</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintenance dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{8 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)
            with r4_c2:
                with st.container(border=True):
                    st.markdown("### 🍄 **Fluconazole**")
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Prophylaxis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{3 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 15px; color: #F4511E; margin-left: 8px;'>Q3D/QOD</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Treatment DAY 1 dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{25 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Treatment DAY2~ frequency:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{12 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 17px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 2: Diuretics
        # ---------------------------------------------------------------------
        if category == "2. Diuretics":
            d_r1_c1, d_r1_c2, d_r1_c3 = st.columns(3)
            with d_r1_c1:
                with st.container(border=True):
                    st.markdown("## 💧 **Furosemide**")
                    furo_po = 1.0 * b1_bw; furo_oral_ml = furo_po / 10.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• PO dose / oral dosage(1mg/mL):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{furo_po:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{furo_oral_ml:.2f} mL/dose</span> &nbsp;<span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-48h</span></p>", unsafe_allow_html=True)
                    furo_iv = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• IM, intermittent IV:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{furo_iv:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD-QOD</span></p>", unsafe_allow_html=True)
            with d_r1_c2:
                with st.container(border=True):
                    st.markdown("## 🧪 **Bumetanide**")
                    st.caption("Dose Range: 0.01-0.06 mg/kg")
                    bt_preterm = 0.01 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Preterm dosage(0.01mg/kg):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{bt_preterm:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-48H</span></p>", unsafe_allow_html=True)
                    bt_term = 0.01 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Term dosage(0.01mg/kg):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{bt_term:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-24h</span></p>", unsafe_allow_html=True)
            with d_r1_c3:
                with st.container(border=True):
                    st.markdown("## 💊 **Spironolactone**")
                    sp_bpd = 1.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• BPD dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sp_bpd:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12H</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; font-weight:bold; color:#64B5F6;'>🧪 泡製後劑量動態計算：</p>", unsafe_allow_html=True)
                    m12_input = st.number_input("自訂劑量 (mg/dose)", min_value=0.0, max_value=50.0, value=float(round(sp_bpd, 2)), step=0.1, key="m12_sp", label_visibility="collapsed")
                    m13_ml = m12_input / 5.0
                    st.markdown(f"<p style='margin:2px 0 0 0; font-size:12px; color:#ffb300;'>泡製1# in DW 5ml (5mg/mL) 稀釋後冷藏14天：</p><p style='margin:0; font-size: 18px; font-weight: bold; color: #1E88E5;'>{m12_input:.1f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{m13_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            d_r2_c1, d_r2_c2, _ = st.columns(3)
            with d_r2_c1:
                with st.container(border=True):
                    st.markdown("## 🪵 **Trichlormethiazide**")
                    tcm_dose = 0.04 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Initial dose(Range:0.04-1.6mg/kg/day):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{tcm_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD-Q12H</span></p>", unsafe_allow_html=True)
            with d_r2_c2:
                with st.container(border=True):
                    st.markdown("## 🧊 **Mannitol 20%**")
                    mnt_icp_g = 0.25 * b1_bw; mnt_icp_ml = mnt_icp_g / 0.2
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• ICP(0.25g/kg) / 換算後mL數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mnt_icp_g:.2f} <span style='font-size:12px; color:#fff;'>g/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{mnt_icp_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    mnt_iop_g = 1.5 * b1_bw; mnt_iop_ml = mnt_iop_g / 0.2
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• IOP(1.5g/kg) / 換算後mL數:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mnt_iop_g:.2f} <span style='font-size:12px; color:#fff;'>g/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{mnt_iop_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 3: PDA
        # ---------------------------------------------------------------------
        if category == "3. PDA":
            pda_col1, pda_col2, pda_col3 = st.columns(3)
            with pda_col1:
                with st.container(border=True):
                    st.markdown("## 🧬 **Ibuprofen (Standard)**")
                    st.markdown("---")
                    ibu_1st = 10 * b1_bw; ibu_1st_oral_ml = ibu_1st / 20.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 1st dose (IV / ORAL mL數):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ibu_1st:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{ibu_1st_oral_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    ibu_follow = 5 * b1_bw; ibu_follow_oral_ml = ibu_follow / 20.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 2nd, 3rd doses (IV / ORAL mL數):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ibu_follow:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{ibu_follow_oral_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
            with pda_col2:
                with st.container(border=True):
                    st.markdown("## 💊 **Propacetamol**")
                    st.markdown("---")
                    prop_dose = 30 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard dose(30mg/kg):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{prop_dose:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)
            with pda_col3:
                with st.container(border=True):
                    st.markdown("## 🧫 **Acetaminophen**")
                    st.markdown("---")
                    ace_mg = 15 * b1_bw; ace_ml = ace_mg / 24.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard dose / 換算後mL數:</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ace_mg:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{ace_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 4: 肺高壓
        # ---------------------------------------------------------------------
        if category == "4. 肺高壓":
            ph_col1, ph_col2, ph_col3 = st.columns(3)
            with ph_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Sildenafil**")
                    st.markdown("---")
                    sil_dose = 0.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose(Range:0.5-2mg/kg) (0.5mg/kg):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{sil_dose:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)
            with ph_col2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Bosentan**")
                    st.markdown("---")
                    bos_dose = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose:</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{bos_dose:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with ph_col3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Iloprost**")
                    st.markdown("---")
                    ilo_dose = 0.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose(Range:0.5-2mcg/kg) (0.5mcg/kg):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #64B5F6;'>{ilo_dose:.2f} <span style='font-size:13px; color:#ff8a80; font-weight:bold;'>mcg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q4H</p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 5: Apnea/RDS Surfactant —— 🛠️ 專屬變數完全隔離，徹底修正！
        # ---------------------------------------------------------------------
        if category == "5. Apnea/RDS Surfactant":
            ap_c1, ap_c2, ap_c3 = st.columns(3)
            with ap_c1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Aminophylline**")
                    st.markdown("---")
                    ap_load = 5.0 * b1_bw; ap_maint = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ap_load:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ap_maint:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with ap_c2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Theophylline**")
                    st.markdown("---")
                    theo_load_mg = 5.0 * b1_bw; theo_load_ml = theo_load_mg / 5.34
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{theo_load_mg:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{theo_load_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    theo_maint_mg = 1.0 * b1_bw; theo_maint_ml = theo_maint_mg / 5.34
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{theo_maint_mg:.2f} <span style='font-size:12px; font-weight:normal;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{theo_maint_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with ap_c3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Caffeine citrate**")
                    st.markdown("---")
                    caf_load = 20.0 * b1_bw; caf_maint = 10.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose(20 mg/kg):</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{caf_load:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose(10 mg/kg):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{caf_maint:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
            
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            ap_c4, _, _ = st.columns(3)
            with ap_c4:
                with st.container(border=True):
                    st.markdown("## 🫁 **Poractant alfa: ET**")
                    st.markdown("---")
                    pnt_mg = 200.0 * b1_bw; pnt_ml = 2.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose / 換算後mL數:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pnt_mg:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{pnt_ml:.1f} mL/dose</span></p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 6: Seizure control
        # ---------------------------------------------------------------------
        if category == "6. Seizure control":
            sz_col1, sz_col2, _ = st.columns(3)
            with sz_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Phenobarbital**")
                    st.markdown("---")
                    pb_load = 15.0 * b1_bw; pb_maint = 3.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose(IV) (15mg/kg/day):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{pb_load:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintenance (PO.IV):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{pb_maint:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with sz_col2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Levetiracetam**")
                    st.markdown("---")
                    sz_load = 20.0 * b1_bw; sz_maint = 10.0 * b1_bw; sz_ml = sz_maint / 100.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{sz_load:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintenance (PO.IV) / 換算後mL數:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sz_maint:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{sz_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 7: Sedation
        # ---------------------------------------------------------------------
        if category == "7. Sedation":
            sd_col1, _, _ = st.columns(3)
            with sd_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Chloral hydrate 10%**")
                    sd_dose_mg = 25.0 * b1_bw; sd_dose_ml = sd_dose_mg / 100.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose / 換算後mL數:</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sd_dose_mg:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{sd_dose_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 8: Miscellaneous.GCSF
        # ---------------------------------------------------------------------
        if category == "8. Miscellaneous.GCSF":
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Albumin**")
                    alb_dose = b1_bw * 1.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose (1g/kg):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #64B5F6;'>{alb_dose:.2f} <span style='font-size:13px; color:#ff8a80; font-weight:bold;'>g/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with m_col2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Eptacog alfa(Factor 7)**")
                    ept_dose = b1_bw * 50.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Preterm pulmonary hemorrhage (50mcg/kg/dose):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{ept_dose:.1f} <span style='font-size:13px; color:#fff;'>mcg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q2-6H</p>", unsafe_allow_html=True)
            with m_col3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Beriplex P/N**")
                    ber_dose = b1_bw * 30.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Initial dosage(30 IU/kg):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{ber_dose:.1f} <span style='font-size:13px; color:#fff;'>IU</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q4H</p>", unsafe_allow_html=True)
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            m_col4, _, _ = st.columns(3)
            with m_col4:
                with st.container(border=True):
                    st.markdown("## 🧪 **Filgrastim**")
                    fil_dose = b1_bw * 10.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Neutropenia with sepsis(10mcg/kg/dose):</p><p style='margin:0 0 8px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{fil_dose:.1f} <span style='font-size:13px; color:#fff;'>mcg</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 分類 9: 胃腸類藥品/營養補充品/維他命/其它
        # ---------------------------------------------------------------------
        if category == "9. 胃腸類藥品/營養補充品/維他命/其它":
            g_r1_c1, g_r1_c2, g_r1_c3 = st.columns(3)
            with g_r1_c1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Famotidine(PO.IV)**")
                    famo = 0.25 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(0.25mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{famo:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD-Q12H</p>", unsafe_allow_html=True)
            with g_r1_c2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Pantoprazole(IV)**")
                    panto = 0.6 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Initail dose (Range 0.6-1.2mg/kg/day):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{panto:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with g_r1_c3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Esomeprazole(PO)**")
                    eso = 0.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage (0.5mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{eso:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            g_r2_c1, g_r2_c2, g_r2_c3 = st.columns(3)
            with g_r2_c1:
                with st.container(border=True):
                    st.markdown("## 🟧 **Lansoprazole(PO)**")
                    lanso = 0.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Initail dose (Range 0.5-1.5mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{lanso:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with g_r2_c2:
                with st.container(border=True):
                    st.markdown("## 🟪 **Domperidone (PO)**")
                    domp_mg = 0.25 * b1_bw; domp_ml = domp_mg / 1.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage / 換算後mL數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{domp_mg:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{domp_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8H</p>", unsafe_allow_html=True)
            with g_r2_c3:
                with st.container(border=True):
                    st.markdown("## 🟫 **Mosapride(PO)**")
                    mosa = 0.1 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(0.3mg/kg/day):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mosa:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8H</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            g_r3_c1, g_r3_c2, g_r3_c3 = st.columns(3)
            with g_r3_c1:
                with st.container(border=True):
                    st.markdown("## 🧪 **Metoclopramide**")
                    meto = 0.1 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(0.1 mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{meto:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with g_r3_c2:
                with st.container(border=True):
                    st.markdown("## ## 🔍 **Dioctahedral Smectite**")
                    smec_g = 1.5; smec_pac = smec_g / 3.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage / 換算後包數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #64B5F6;'>{smec_g:.1f} <span style='font-size:12px; color:#ff8a80; font-weight:bold;'>g/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{smec_pac:.2f} pac/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with g_r3_c3:
                with st.container(border=True):
                    st.markdown("## 🟶 **Racecadotril**")
                    race = 1.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(1.5 mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{race:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8H</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            g_r4_c1, g_r4_c2, g_r4_c3 = st.columns(3)
            with g_r4_c1:
                with st.container(border=True):
                    st.markdown("## ☀️ **Calcitriol**")
                    calc_mcg = 0.1 * b1_bw; calc_ml = (calc_mcg * 0.32) / 0.5
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage / 換算後mL數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #64B5F6;'>{calc_mcg:.2f} <span style='font-size:12px; color:#ff8a80; font-weight:bold;'>mcg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{calc_ml:.3f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with g_r4_c2:
                with st.container(border=True):
                    st.markdown("## 🛡️ **Sideral GOCCE P**")
                    sid_ml = b1_bw * 0.2; sid_mg = sid_ml * 7.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage / 換算後mg數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sid_ml:.2f} <span style='font-size:12px; color:#fff;'>mL/day</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{sid_mg:.2f} mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with g_r4_c3:
                with st.container(border=True):
                    st.markdown("## 🐻 **Ursodeoxycholic acid**")
                    urso = 10 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{urso:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8H</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            g_r5_c1, g_r5_c2, g_r5_c3 = st.columns(3)
            with g_r5_c1:
                with st.container(border=True):
                    st.markdown("## 🌿 **Silymarin**")
                    sily = 3.75 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sily:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with g_r5_c2:
                with st.container(border=True):
                    st.markdown("## 🩸 **Tranexamic Acid(IV)**")
                    tran = 10 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(10 mg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{tran:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8H</p>", unsafe_allow_html=True)
            with g_r5_c3:
                with st.container(border=True):
                    st.markdown("## 💊 **Diazoxide(PO)**")
                    diaz = 5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dosage(10 mg/kg/day):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{diaz:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            g_r6_c1, g_r6_c2, g_r6_c3 = st.columns(3)
            with g_r6_c1:
                with st.container(border=True):
                    st.markdown("## ## 🦋 **Levothyroxine**")
                    levo = 10 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dosage(10 - 15 mcg/kg/dose):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #64B5F6;'>{levo:.1f} <span style='font-size:12px; color:#ff8a80; font-weight:bold;'>mcg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>QD</p>", unsafe_allow_html=True)
            with g_r6_c2:
                with st.container(border=True):
                    st.markdown("## 🍓 **Propranolol**")
                    prop_hem = 0.25 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Infantile Hemangiomas(0.5 mg/kg/day):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{prop_hem:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with g_r6_c3:
                with st.container(border=True):
                    st.markdown("## 🧠 **Piracetam**")
                    pira_mg = 20 * b1_bw; pira_ml = pira_mg / 200.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Breath holding spell / 換算後mL數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pira_mg:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{pira_ml:.3f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; color:#888;'>• Frequency:</p><p style='margin:0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)

# =============================================================================
# ⚡ 區塊 2: Ion dosage —— 全局隔離，絕對不跳
# =============================================================================
if main_page == "⚡ Ion dosage":
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」，系統將即時啟動電解質與元素換算面板。")
    else:
        st.markdown("<p style='color:#ff8a80; font-weight:bold; font-size:14px; margin-bottom:10px;'>⚠️ 臨床警訊：離子藥物微量滴注風險高，建議醫護同仁雙重確認！僅可更改藍色互動區域。</p>", unsafe_allow_html=True)
        
        ion_r1_c1, ion_r1_c2, _ = st.columns(3)
        with ion_r1_c1:
            with st.container(border=True):
                st.markdown("## 🟥 **Magnesium Sulfate 10% (MgSO4)**")
                st.caption("濃度規格: 100 mg/mL (IV) | 臨床範圍: 25 - 50 mg/kg/dose")
                mgso4_base = 50.0 * b1_bw; mgso4_ml = mgso4_base / 100.0
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議劑量 / 換算後mL數:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mgso4_base:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>{mgso4_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q8-Q12H</p>", unsafe_allow_html=True)
        with ion_r1_c2:
            with st.container(border=True):
                st.markdown("## 🟦 **Magnesium Oxide**")
                st.caption("臨床範圍: 16.5 - 33.1 mg/kg/dose")
                mg_oxide = 25.0 * b1_bw
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議劑量:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mg_oxide:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>QID</p>", unsafe_allow_html=True)

        st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
        ion_r2_c1, _ = st.columns([2, 1])
        with ion_r2_c1:
            with st.container(border=True):
                st.markdown("## 🥛 **Calcium Gluconate 10% (PO.IV)**")
                ca_glu_po = 1.34 * b1_bw
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 口服PO 建議劑量 (1.34*BW):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ca_glu_po:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E;'>Q6H</span> &nbsp;<span style='font-size:12px; color:#888; font-weight:normal;'>(範圍: 5.37-8.06 mL/kg/day)</span></p>", unsafe_allow_html=True)
                ca_glu_iv = b1_bw * 1.0
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 輸注IV 建議劑量 (BW*1):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ca_glu_iv:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E;'>Q6H</span> &nbsp;<span style='font-size:12px; color:#888; font-weight:normal;'>(範圍: 1-2 mL/kg/dose)</span></p>", unsafe_allow_html=True)

        st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
        ion_r3_c1, ion_r3_c2 = st.columns(2)
        with ion_r3_c1:
            with st.container(border=True):
                st.markdown("## 🟨 **Calcium gluconated (PO)**")
                st.caption("每粒常數基礎：含鈣 103.86 mg、磷 66.51 mg (鈣磷比 1.5:1)、Vit D2 330 IU")
                c_gl_init_tab = 0.20 * b1_bw; c_gl_max_tab = 0.75 * b1_bw
                init_ca = (c_gl_init_tab * 103.86) / b1_bw if b1_bw > 0 else 0.0; init_p = (c_gl_init_tab * 66.51) / b1_bw if b1_bw > 0 else 0.0; init_d2 = c_gl_init_tab * 330.0
                max_ca = (c_gl_max_tab * 103.86) / b1_bw if b1_bw > 0 else 0.0; max_p = (c_gl_max_tab * 66.51) / b1_bw if b1_bw > 0 else 0.0; max_d2 = c_gl_max_tab * 330.0
                st.markdown(f"""
                <p style='margin:1px 0 3px 0; font-size:14px; color:#888;'>• <b>Initial Dose</b> 建議: <span style='color:#1E88E5; font-weight:bold;'>{c_gl_init_tab:.2f} tab/day</span></p>
                <p style='margin:0 0 8px 0; font-size:13px; color:#4CAF50; padding-left: 10px;'>
                    元素Ca: {init_ca:.2f} mg/kg/day &nbsp;|&nbsp; 元素P: {init_p:.2f} mg/kg/day &nbsp;|&nbsp; Vit D2: {init_d2:.1f} IU
                </p>
                <p style='margin:1px 0 3px 0; font-size:14px; color:#888;'>• <b>Max Dose</b> 建議: <span style='color:#F4511E; font-weight:bold;'>{c_gl_max_tab:.2f} tab/day</span></p>
                <p style='margin:0 0 2px 0; font-size:13px; color:#ff8a80; padding-left: 10px;'>
                    元素Ca: {max_ca:.2f} mg/kg/day &nbsp;|&nbsp; 元素P: {max_p:.2f} mg/kg/day &nbsp;|&nbsp; Vit D2: {max_d2:.1f} IU
                </p>
                """, unsafe_allow_html=True)
        with ion_r3_c2:
            with st.container(border=True):
                st.markdown("## 🟩 **Bio-cal Plus chewable Tab.**")
                st.caption("每粒常數基礎：含鈣 450 mg、磷 230 mg (鈣磷比 2:1)、Cholecalciferol 330 IU")
                bcal_init_tab = 0.045 * b1_bw; bcal_max_tab = 0.17 * b1_bw
                bc_init_ca = (bcal_init_tab * 450.0) / b1_bw if b1_bw > 0 else 0.0; bc_init_p = (bcal_init_tab * 230.0) / b1_bw if b1_bw > 0 else 0.0; bc_init_d3 = bcal_init_tab * 330.0
                bc_max_ca = (bcal_max_tab * 450.0) / b1_bw if b1_bw > 0 else 0.0; bc_max_p = (bcal_max_tab * 230.0) / b1_bw if b1_bw > 0 else 0.0; bc_max_d3 = bcal_max_tab * 330.0
                st.markdown(f"""
                <p style='margin:1px 0 3px 0; font-size:14px; color:#888;'>• <b>Initial Dose</b> 建議: <span style='color:#1E88E5; font-weight:bold;'>{bcal_init_tab:.2f} tab/day</span></p>
                <p style='margin:0 0 8px 0; font-size:13px; color:#4CAF50; padding-left: 10px;'>
                    元素Ca: {bc_init_ca:.2f} mg/kg/day &nbsp;|&nbsp; 元素P: {bc_init_p:.2f} mg/kg/day &nbsp;|&nbsp; Vit D3: {bc_init_d3:.1f} IU
                </p>
                <p style='margin:1px 0 3px 0; font-size:14px; color:#888;'>• <b>Max Dose</b> 建議: <span style='color:#F4511E; font-weight:bold;'>{bcal_max_tab:.2f} tab/day</span></p>
                <p style='margin:0 0 2px 0; font-size:13px; color:#ff8a80; padding-left: 10px;'>
                    元素Ca: {bc_max_ca:.2f} mg/kg/day &nbsp;|&nbsp; 元素P: {bc_max_p:.2f} mg/kg/day &nbsp;|&nbsp; Vit D3: {bc_max_d3:.1f} IU
                </p>
                """, unsafe_allow_html=True)

        st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
        ion_r4_c1, _ = st.columns([2, 1])
        with ion_r4_c1:
            with st.container(border=True):
                st.markdown("## ## 🧴 **All-right calcium suspension**")
                st.caption("每 mL 常數基礎：含鈣 39.92 mg、磷 20.57 mg (鈣磷比 2:1) | 建議劑量: 2.5 mL/dose (QD)")
                st.markdown("<p style='color:#64B5F6; font-size:12px; margin:0;'>🟦 劑量換算器：請輸入預開立之使用劑量 (mL/dose)</p>", unsafe_allow_html=True)
                c16_input = st.number_input("輸入使用劑量 (mL/dose)", min_value=0.0, max_value=50.0, value=2.5, step=0.5, key="c16_calc", label_visibility="collapsed")
                f16_ca = (c16_input * 39.92) / b1_bw if b1_bw > 0 else 0.0; i16_p = (20.57 * c16_input) / b1_bw if b1_bw > 0 else 0.0; m16_d3 = 160.0 * c16_input; p16_vitA = (1600.0 * c16_input) / b1_bw if b1_bw > 0 else 0.0
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:13px; color:#ccc;'>🧮 換算後各元素暴露總量解析：</p><p style='margin:0; font-size:15px; font-weight:bold;'>Ca含量: <span style='color:#1E88E5;'>{f16_ca:.2f} mg/kg/day</span> &nbsp;<span style='color:#555;'>|</span>&nbsp; P含量: <span style='color:#1E88E5;'>{i16_p:.2f} mg/kg/day</span> &nbsp;<span style='color:#555;'>|</span>&nbsp; Vit D3: <span style='color:#4CAF50;'>{m16_d3:.1f} IU</span> &nbsp;<span style='color:#555;'>|</span>&nbsp; Vit A: <span style='color:#ffb300;'>{p16_vitA:.1f} IU/kg/dose</span></p>", unsafe_allow_html=True)

# =============================================================================
# 🫁 區塊 3: DART.BURST —— 全局隔離，絕對不跳
# =============================================================================
if main_page == "🫁 DART.BURST":
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」，系統將即時啟動 BPD 類固醇療慢減量面板。")
    else:
        st.markdown("<p style='color:#ffb300; font-weight:bold; font-size:14px; margin-bottom:12px;'>📊 臨床指引核對模式：已依據病患體重自動換算完整療程劑量。</p>", unsafe_allow_html=True)
        
        bpd_col1, bpd_col2, bpd_col3 = st.columns(3)
        with bpd_col1:
            with st.container(border=True):
                st.markdown("## 🟥 **Burst (BPD burst) — Prednisolone**")
                st.markdown("---")
                burst_dose = 1.0 * b1_bw
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage I</b> (1mg/kg/dose Q6H 2 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q6H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>2 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage II</b> (1mg/kg/dose Q12H 2 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>2 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage III</b> (1mg/kg/dose QD 2 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 4px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>QD</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>2 days</span></p>", unsafe_allow_html=True)
        with bpd_col2:
            with st.container(border=True):
                st.markdown("## 🟦 **Dart (Dexamethasone)**")
                st.markdown("---")
                dart_s1 = 0.075 * b1_bw; dart_s2 = 0.05 * b1_bw; dart_s3 = 0.025 * b1_bw; dart_s4 = 0.01 * b1_bw
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage I</b> (0.15mg/kg/day 3 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{dart_s1:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>3 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage II</b> (0.1mg/kg/day 3 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{dart_s2:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>3 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage III</b> (0.05mg/kg/day 2 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{dart_s3:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>2 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage IV</b> (0.02mg/kg/day 2 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 4px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{dart_s4:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>2 days</span></p>", unsafe_allow_html=True)
        with bpd_col3:
            with st.container(border=True):
                st.markdown("## 🟩 **STOP-BPD (Hydrocortisone)**")
                st.markdown("---")
                hydro_dose = 0.5 * b1_bw
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage I</b> (1 mg/kg/day Q12h 7 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 12px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{hydro_dose:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>7 days</span></p>", unsafe_allow_html=True)
                st.markdown("<p style='margin:8px 0 2px 0; font-size:13px; color:#888;'>• <b>Stage II</b> (0.5mg/kg/day QD for 3 days):</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0 0 4px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{hydro_dose:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #4CAF50;'>QD</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color: #F4511E; font-size:16px;'>3 days</span></p>", unsafe_allow_html=True)

# =============================================================================
# 🔌 區塊 4: 升壓劑.止痛鎮靜pump (原 PUMP 總表 10 品項完美保留)
# =============================================================================
if main_page == "🔌 升壓劑.止痛鎮靜pump":
    st.markdown("### 🔌 升壓劑.止痛鎮靜幫浦 - 多配方動態演算面板")
    
    if "fixed_drug_p4" not in st.session_state:
        st.session_state["fixed_drug_p4"] = "Dopamine"
    if "fixed_flow_p4" not in st.session_state:
        st.session_state["fixed_flow_p4"] = 0.5
        
    with st.container(border=True):
        st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#64B5F6;'>📋 臨床常用重症藥物劑量參考範圍 (Range)</p>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.markdown("<div>• <b>Dopamine</b>: 3 - 10 mcg/kg/min<br>• <b>Dobutamine</b>: 2 - 20 mcg/kg/min<br>• <b>Epinephrine</b>: 0.05 - 0.5 mcg/kg/min</div>", unsafe_allow_html=True)
        with rc2:
            st.markdown("<div>• <b>Norepinephrine</b>: 0.02 - 0.1 mcg/kg/min (⚠️最濃 2:1)<br>• <b>Milrinone</b>: 0.25 - 0.75 mcg/kg/min<br>• <b>Fentanyl</b>: 0.008 - 0.05 mcg/kg/min</div>", unsafe_allow_html=True)
        with rc3:
            st.markdown("<div>• <b>Morphine</b>: 0.16 - 0.83 mcg/kg/min<br>• <b>Midazolam</b>: 0.5 - 6.66 mcg/kg/min<br>• <b>Cisatracurium</b>: 0.75 - 11.5 mcg/kg/min<br>• <b>Rocuronium</b>: 8 - 17 mcg/kg/min</div>", unsafe_allow_html=True)

    st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if has_input:
        p4_c1, p4_c2 = st.columns([2, 2])
        drug_list = ["Dopamine", "Dobutamine", "Epinephrine", "Norepinephrine", "Milrinone", "Fentanyl", "Morphine", "Midazolam", "Cisatracurium", "Rocuronium"]
        try:
            default_index = drug_list.index(st.session_state["fixed_drug_p4"])
        except ValueError:
            default_index = 0
            
        with p4_c1:
            s_drug_p4 = st.selectbox("💉 選擇計算藥物品項：", drug_list, index=default_index, key="p4_drug_selectbox_widget")
            st.session_state["fixed_drug_p4"] = s_drug_p4
        with p4_c2:
            i_flow_p4 = st.number_input("🔌 請輸入目前幫浦設定流速 (mL/hr):", min_value=0.0, value=st.session_state["fixed_flow_p4"], step=0.1, key="p4_flow_input_widget")
            st.session_state["fixed_flow_p4"] = i_flow_p4
            
        st.write("---")
        st.markdown(f"#### 🎯 當前藥物：<span style='color:#1E88E5;'>{s_drug_p4}</span> | 設定流速：<span style='color:#4CAF50;'>{i_flow_p4:.1f} mL/hr</span>", unsafe_allow_html=True)
        
        if i_flow_p4 > 0:
            f_1 = float(max(10.0, math.ceil((i_flow_p4 * 24) / 10.0) * 10.0))
            c_1 = (b1_bw * 0.6) * (f_1 / 10.0); k_1 = (c_1 / f_1) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:1)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_1:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_1:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_1:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_1:.2f} mg 加入 D5W 至 {f_1:.0f} mL", language="text")

            f_2 = float(max(5.0, math.ceil((i_flow_p4 * 24) / 5.0) * 5.0))
            c_2 = (b1_bw * 0.6) * (f_2 / 5.0); k_2 = (c_2 / f_2) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:2)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_2:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_2:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_2:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_2:.2f} mg 加入 D5W 至 {f_2:.0f} mL", language="text")

            f_3 = float(max(20.0, math.ceil((i_flow_p4 * 24) / 20.0) * 20.0))
            c_3 = (b1_bw * 6.0) * (f_3 / 20.0); k_3 = (c_3 / f_3) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:5)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_3:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_3:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_3:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_3:.2f} mg 加入 D5W 至 {f_3:.0f} mL", language="text")

            f_4 = float(max(10.0, math.ceil((i_flow_p4 * 24) / 10.0) * 10.0))
            c_4 = (b1_bw * 6.0) * (f_4 / 10.0); k_4 = (c_4 / f_4) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:10)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_4:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_4:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_4:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_4:.2f} mg 加入 D5W 至 {f_4:.0f} mL", language="text")

            f_5 = float(max(5.0, math.ceil((i_flow_p4 * 24) / 5.0) * 5.0))
            c_5 = (b1_bw * 6.0) * (f_5 / 5.0); k_5 = (c_5 / f_5) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:20)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_5:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_5:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_5:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_5:.2f} mg 加入 D5W 至 {f_5:.0f} mL", language="text")

            f_6 = float(max(20.0, math.ceil((i_flow_p4 * 24) / 20.0) * 20.0))
            c_6 = (b1_bw * 0.6) * (f_6 / 20.0); k_6 = (c_6 / f_6) * i_flow_p4 * 1000 / 60 / b1_bw
            st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (2:1)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_6:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_6:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_6:.3f} mcg/kg/min</span></p></div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_6:.2f} mg 加入 D5W 至 {f_6:.0f} mL", language="text")

            f_7 = float(max(50.0, math.ceil((i_flow_p4 * 24) / 50.0) * 50.0))
            c_7 = (b1_bw * 0.6) * (f_7 / 50.0); k_7 = (c_7 / f_7) * i_flow_p4 * 1000 / 60 / b1_bw
            is_n_danger_7 = (s_drug_p4 == "Norepinephrine")
            bg_7 = "#3c1414" if is_n_danger_7 else "#13171a"; bd_7 = "#ff4444" if is_n_danger_7 else "#1E88E5"
            st.markdown(f"<div style='background-color:{bg_7}; padding:10px 14px; border-radius:4px; border-left:4px solid {bd_7}; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (5:1)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_7:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_7:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_7:.3f} mcg/kg/min</span></p>{' <p style=margin:4px_0_0_0; _color:#ff4444; _font-size:12px; _font-weight:bold;>⚠️ 臨床警告：Norepinephrine 建議最濃為 2:1！此配置已高於安全極限濃度！</p>' if is_n_danger_7 else ''}</div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_7:.2f} mg 加入 D5W 至 {f_7:.0f} mL", language="text")

            f_8 = float(max(100.0, math.ceil((i_flow_p4 * 24) / 100.0) * 100.0))
            c_8 = (b1_bw * 0.6) * (f_8 / 100.0); k_8 = (c_8 / f_8) * i_flow_p4 * 1000 / 60 / b1_bw
            is_n_danger_8 = (s_drug_p4 == "Norepinephrine")
            bg_8 = "#3c1414" if is_n_danger_8 else "#13171a"; bd_8 = "#ff4444" if is_n_danger_8 else "#1E88E5"
            st.markdown(f"<div style='background-color:{bg_8}; padding:10px 14px; border-radius:4px; border-left:4px solid {bd_8}; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (10:1)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_8:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_8:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_8:.3f} mcg/kg/min</span></p>{' <p style=margin:4px_0_0_0; _color:#ff4444; _font-size:12px; _font-weight:bold;>⚠️ 臨床警告：Norepinephrine 建議最濃為 2:1！此配置已高於安全極限濃度！</p>' if is_n_danger_8 else ''}</div>", unsafe_allow_html=True)
            st.code(f"抽取 {s_drug_p4} {c_8:.2f} mg 加入 D5W 至 {f_8:.0f} mL", language="text")
        else:
            st.info("💡 請輸入大於 0 的幫浦流速開始即時演算。")
    else:
        st.warning("⚠️ 請先於左側輸入「BW 體重」及「GA 週數」，系統將自動解鎖組套演算列表。")

# =============================================================================
# 🩸 區塊 4-2: Vasopressin pump —— 🧪 修正標題對齊、加粗顯眼、可複製字眼版
# =============================================================================
if main_page == "🩸 Vasopressin pump":
    st.markdown("<h3 style='color: #FF7043;'>🩸 Vasopressin pump - 獨立演算面板</h3>", unsafe_allow_html=True)
    
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」及「GA 週數」，系統將自動啟動 Vasopressin 演算列表。")
    else:
        # 🌟 選擇區視覺強化：加上背景大黑盒與醒目標題，讓點選的地方極度明顯！
        st.markdown("""
            <div style='background-color: #263238; padding: 10px 14px; border-radius: 4px; border-left: 5px solid #FF7043; margin-bottom: 12px; box-shadow: 0px 2px 4px rgba(0,0,0,0.3);'>
                <span style='color: #FFF; font-weight: bold; font-size: 16px;'>🎯 請點選下方的「適應症計算機分類」來切換面板：</span>
            </div>
        """, unsafe_allow_html=True)
        
        vaso_mode = st.sidebar.radio(
            "🗂️ 當前計算機切換（亦可於此點選）：",
            ["1. Vasopressin - shock / PPHN (多組套流速回推劑量)", "2. Vasopressin - Diabetes insipidus (尿崩症調配面板)"],
            key="vaso_sidebar_sync_key"
        )
        
        # 主畫面同步點選器（改為縱向大字體，排版更顯眼，完全消滅橫向被吃字的問題）
        vaso_mode = st.radio(
            "請直接勾選：",
            ["1. Vasopressin - shock / PPHN (多組套流速回推劑量)", "2. Vasopressin - Diabetes insipidus (尿崩症調配面板)"],
            horizontal=False,
            label_visibility="collapsed",
            key="vaso_mode_selector"
        )
        st.write("---")

        # ---------------------------------------------------------------------
        # 適應症 1: Vasopressin-shock.PPHN
        # ---------------------------------------------------------------------
        if vaso_mode == "1. Vasopressin - shock / PPHN (多組套流速回推劑量)":
            with st.container(border=True):
                st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#64B5F6;'>📋 Vasopressin 臨床指引參考範圍 ( mU/kg/min )</p>", unsafe_allow_html=True)
                v_rc1, vaso_rc2 = st.columns(2)
                with v_rc1:
                    st.markdown("<div>• <b>Shock 建議劑量</b>: 0.17 - 0.67 milliunits/kg/min</div>", unsafe_allow_html=True)
                with vaso_rc2:
                    st.markdown("<div>• <b>PPHN 建議劑量</b>: 0.1 - 1.2 milliunits/kg/min</div>", unsafe_allow_html=True)

            st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)
            
            if "v_shock_flow" not in st.session_state:
                st.session_state["v_shock_flow"] = 0.5
            
            v_flow = st.number_input("🔌 請輸入目前幫浦設定流速 (mL/hr):", min_value=0.0, value=st.session_state["v_shock_flow"], step=0.1, key="v_shock_flow_input")
            st.session_state["v_shock_flow"] = v_flow
            
            st.write("---")
            
            if v_flow > 0:
                # --- 1:1 組套 ---
                f_1_1 = float(max(10.0, math.ceil((v_flow * 24) / 10.0) * 10.0))
                c_1_1 = (b1_bw * 0.6) * (f_1_1 / 10.0)
                k_1_1 = (c_1_1 / f_1_1) * v_flow * 1000 / 60 / b1_bw
                st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:1)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_1_1:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>IU</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_1_1:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_1_1:.3f} milliunits/kg/min</span></p></div>", unsafe_allow_html=True)
                st.code(f"抽取 Vasopressin {c_1_1:.2f} IU 加入 D5W 至 {f_1_1:.0f} mL", language="text")

                # --- 1:2 組套 ---
                f_1_2 = float(max(5.0, math.ceil((v_flow * 24) / 5.0) * 5.0))
                c_1_2 = (b1_bw * 0.6) * (f_1_2 / 5.0)
                k_1_2 = (c_1_2 / f_1_2) * v_flow * 1000 / 60 / b1_bw
                st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:2)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_1_2:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>IU</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_1_2:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_1_2:.3f} milliunits/kg/min</span></p></div>", unsafe_allow_html=True)
                st.code(f"抽取 Vasopressin {c_1_2:.2f} IU 加入 D5W 至 {f_1_2:.0f} mL", language="text")

                # --- 1:5 組套 ---
                f_1_5 = float(max(20.0, math.ceil((v_flow * 24) / 20.0) * 20.0))
                c_1_5 = (b1_bw * 6.0) * (f_1_5 / 20.0)
                k_1_5 = (c_1_5 / f_1_5) * v_flow * 1000 / 60 / b1_bw
                st.markdown(f"<div style='background-color:#13171a; padding:10px 14px; border-radius:4px; border-left:4px solid #1E88E5; margin-bottom:6px;'><span style='font-size:14px; font-weight:bold; color:#64B5F6;'>組套 (1:5)</span><p style='margin:4px 0 0 0; font-size:20px; font-weight:bold; color:#1E88E5;'>{c_1_5:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>IU</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; D5W 至 {f_1_5:.0f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{k_1_5:.3f} milliunits/kg/min</span></p></div>", unsafe_allow_html=True)
                st.code(f"抽取 Vasopressin {c_1_5:.2f} IU 加入 D5W 至 {f_1_5:.0f} mL", language="text")
            else:
                st.info("💡 請輸入大於 0 的幫浦流速開始即時演算。")

        # ---------------------------------------------------------------------
        # 適應症 2: Vasopressin-Diabetes insipidus (尿崩症) —— 🛠️ 完美對齊開門字眼！
        # ---------------------------------------------------------------------
        elif vaso_mode == "2. Vasopressin - Diabetes insipidus (尿崩症調配面板)":
            with st.container(border=True):
                st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#4CAF50;'>📋 Vasopressin - Diabetes insipidus 臨床指引範圍</p>", unsafe_allow_html=True)
                st.markdown("<div>• <b>建議劑量範圍</b>: 0.008 - 0.033 milliunits/kg/min</div>", unsafe_allow_html=True)

            st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)
            
            di_col1, di_col2 = st.columns(2)
            
            # 計算機 (1)：固定 10:1 比例
            with di_col1:
                with st.container(border=True):
                    st.markdown("### 🧮 **(1) 固定 10:1 泡製法**")
                    if "v_di_flow_1" not in st.session_state:
                        st.session_state["v_di_flow_1"] = 0.5
                    
                    v_di_flow_1 = st.number_input("請輸入設定流速 (mL/hr)", min_value=0.0, value=st.session_state["v_di_flow_1"], step=0.1, key="v_di_flow_1_input")
                    st.session_state["v_di_flow_1"] = v_di_flow_1
                    
                    if v_di_flow_1 > 0:
                        f_31 = float(max(100.0, math.ceil((v_di_flow_1 * 24) / 100.0) * 100.0))
                        c_31 = (b1_bw * 0.6) * (f_31 / 100.0)
                        k_31 = (c_31 / f_31) * v_di_flow_1 * 1000 / 60 / b1_bw
                        st.markdown(f"<p style='margin:6px 0 2px 0; font-size:13px; color:#ccc;'>🧪 換算劑量結果：</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #4CAF50;'>{k_31:.4f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mU/kg/min</span></p>", unsafe_allow_html=True)
                        st.code(f"抽取 Vasopressin {c_31:.3f} IU 加入 D10W 至 {f_31:.0f} mL", language="text")
                    else:
                        st.caption("請輸入流速以啟動計算。")

            # 計算機 (2)：固定調流速 0.04 IU/mL 規格
            with di_col2:
                with st.container(border=True):
                    st.markdown("### 🔌 **(2) 固定濃度 0.04 IU/mL 法**")
                    st.markdown("<p style='margin:0; font-size:12px; color:#ffb300; font-weight:bold;'>固定調配規格：20 IU 加入 D10W 至 500 mL</p>", unsafe_allow_html=True)
                    
                    d33_suggest_min = 0.0125 * b1_bw
                    d34_suggest_max = 0.05 * b1_bw
                    st.markdown(f"<p style='margin:4px 0 4px 0; font-size:13px; color:#888;'>• 臨床最低-最高流速參考區間：<br><span style='color:#64B5F6; font-weight:bold;'>{d33_suggest_min:.4f} ~ {d34_suggest_max:.4f} mL/hr</span></p>", unsafe_allow_html=True)
                    
                    if "v_di_flow_2" not in st.session_state:
                        st.session_state["v_di_flow_2"] = float(round(d33_suggest_min, 4)) if d33_suggest_min > 0 else 0.0
                        
                    v_di_flow_2 = st.number_input("請輸入當前幫浦流速 (mL/hr)", min_value=0.0, value=st.session_state["v_di_flow_2"], step=0.01, format="%.4f", key="v_di_flow_2_input")
                    st.session_state["v_di_flow_2"] = v_di_flow_2
                    
                    if v_di_flow_2 > 0:
                        k_35 = (20.0 / 500.0 * v_di_flow_2 / b1_bw) * 1000 / 60
                        st.markdown(f"<p style='margin:6px 0 2px 0; font-size:14px; color:#ccc;'>🧮 換算劑量結果：</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #4CAF50;'>{k_35:.4f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mU/kg/min</span></p>", unsafe_allow_html=True)
                        st.code(f"抽取 Vasopressin 20.000 IU 加入 D10W 至 500 mL", language="text")
                    else:
                        st.caption("請輸入流速以啟動計算。")
                        
# =============================================================================
# 🧬 區塊 4-3: Prostaglandin E1與利尿劑pump —— 🧪 動態基數配方演算面板
# =============================================================================
if main_page == "🧬 Prostaglandin E1與利尿劑pump":
    st.markdown("<h3 style='color: #4DB6AC;'>🧬 Prostaglandin E1 與利尿劑幫浦面板</h3>", unsafe_allow_html=True)
    
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」及「GA 週數」，系統將自動啟動演算面板。")
    else:
        # 1. 臨床建議劑量指引公告藍圖
        with st.container(border=True):
            st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#4DB6AC;'>📋 臨床建議劑量指引參考範圍</p>", unsafe_allow_html=True)
            pge_rc1, pge_rc2, pge_rc3 = st.columns(3)
            with pge_rc1:
                st.markdown("<div>• <b>Prostaglandin E1</b>: 10 - 400 ng/kg/min</div>", unsafe_allow_html=True)
            with pge_rc2:
                st.markdown("<div>• <b>Furosemide pump</b>: 0.1 - 0.4 mg/kg/hr</div>", unsafe_allow_html=True)
            with pge_rc3:
                st.markdown("<div>• <b>Bumetanide pump</b>: 1 - 10 mcg/kg/hr</div>", unsafe_allow_html=True)

        st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)
        
        # 建立三欄並排橫向版面，讓選擇和輸入極度明顯
        pge_col1, pge_col2, pge_col3 = st.columns(3)
        
        # ---------------------------------------------------------------------
        # 藥物 (1): Prostaglandin E1
        # ---------------------------------------------------------------------
        with pge_col1:
            with st.container(border=True):
                st.markdown("### 🧪 **Prostaglandin E1**")
                
                if "p4_pge_flow" not in st.session_state:
                    st.session_state["p4_pge_flow"] = 0.5
                    
                pge_flow = st.number_input("輸入 PGE1 流速 (mL/hr)", min_value=0.0, value=st.session_state["p4_pge_flow"], step=0.1, key="pge_flow_input")
                st.session_state["p4_pge_flow"] = pge_flow
                
                if pge_flow > 0:
                    # Excel 核心邏輯: 基數 = 200 / 體重 / 6
                    pge_base = 200.0 / b1_bw / 6.0
                    # in D10W = MAX(基數, CEILING(流速*24, 基數))
                    f_28 = float(max(pge_base, math.ceil((pge_flow * 24) / pge_base) * pge_base))
                    # Dose = 20 * (in D10W / 基數)
                    c_28 = 20.0 * (f_28 / pge_base)
                    # 換算後單位劑量 = C28 / F28 * 流速 * 1000 / 60 / 體重
                    k_28 = (c_28 / f_28) * pge_flow * 1000.0 / 60.0 / b1_bw
                    
                    st.markdown(f"<p style='margin:6px 0 2px 0; font-size:13px; color:#ccc;'>🧮 換算暴露劑量：</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #4CAF50;'>{k_28:.3f} <span style='font-size:12px; color:#fff; font-weight:normal;'>ng/kg/min</span></p>", unsafe_allow_html=True)
                    st.code(f"抽取 PGE1 {c_28:.2f} mcg 加入 D10W 至 {f_28:.1f} mL", language="text")
                else:
                    st.caption("請輸入流速以啟動計算。")

        # ---------------------------------------------------------------------
        # 藥物 (2): Furosemide (1:1)
        # ---------------------------------------------------------------------
        with pge_col2:
            with st.container(border=True):
                st.markdown("### 💧 **Furosemide (1:1)**")
                
                if "p4_furo_flow" not in st.session_state:
                    st.session_state["p4_furo_flow"] = 0.5
                    
                furo_flow = st.number_input("輸入 Furosemide 流速 (mL/hr)", min_value=0.0, value=st.session_state["p4_furo_flow"], step=0.1, key="furo_flow_input")
                st.session_state["p4_furo_flow"] = furo_flow
                
                if furo_flow > 0:
                    # Excel 核心邏輯: 基數 = 20 / 體重 / 1
                    furo_base = 20.0 / b1_bw / 1.0
                    # in D10W = MAX(基數, CEILING(流速*24, 基數))
                    f_29 = float(max(furo_base, math.ceil((furo_flow * 24) / furo_base) * furo_base))
                    # Dose = 20 * (in D10W / 基數)
                    c_29 = 20.0 * (f_29 / furo_base)
                    # 換算後單位劑量 = C29 / F29 * 流速 / 體重
                    k_29 = (c_29 / f_29) * furo_flow / b1_bw
                    
                    st.markdown(f"<p style='margin:6px 0 2px 0; font-size:13px; color:#ccc;'>🧮 換算暴露劑量：</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #4CAF50;'>{k_29:.3f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg/kg/hr</span></p>", unsafe_allow_html=True)
                    st.code(f"抽取 Furosemide {c_29:.2f} mg 加入 D10W 至 {f_29:.1f} mL", language="text")
                else:
                    st.caption("請輸入流速以啟動計算。")

        # ---------------------------------------------------------------------
        # 藥物 (3): Bumetanide 0.02mg/mL
        # ---------------------------------------------------------------------
        with pge_col3:
            with st.container(border=True):
                st.markdown("### 🧪 **Bumetanide 0.02mg/mL**")
                st.markdown("<p style='margin:0; font-size:12px; color:#ffb300; font-weight:bold;'>固定調配規格：1 mg 加入 D10W 至 500 mL</p>", unsafe_allow_html=True) # 0.02mg/mL 等於 1mg in 50mL 或是 10mg in 500mL，依據圖片規格寫 1 mg in 50 mL
                
                if "p4_bume_flow" not in st.session_state:
                    st.session_state["p4_bume_flow"] = 0.5
                    
                bume_flow = st.number_input("輸入 Bumetanide 流速 (mL/hr)", min_value=0.0, value=st.session_state["p4_bume_flow"], step=0.1, key="bume_flow_input")
                st.session_state["p4_bume_flow"] = bume_flow
                
                if bume_flow > 0:
                    # Excel 固定值: C30 = 1 mg, F30 = 50 mL
                    # 換算後單位劑量 = C30 / F30 * 流速 / 體重 * 1000
                    k_30 = (1.0 / 50.0 * bume_flow / b1_bw) * 1000.0
                    
                    st.markdown(f"<p style='margin:6px 0 2px 0; font-size:13px; color:#ccc;'>🧮 換算暴露劑量：</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #4CAF50;'>{k_30:.3f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mcg/kg/hr</span></p>", unsafe_allow_html=True)
                    st.code(f"抽取 Bumetanide 1.00 mg 加入 D10W 至 50.0 mL", language="text")
                else:
                    st.caption("請輸入流速以啟動計算。")

# =============================================================================
# 💉 區塊 4-4: Insulin pump —— 🧪 完美對齊 Excel 初始流速校正版
# =============================================================================
if main_page == "💉 Insulin pump":
    st.markdown("<h3 style='color: #4954bc;'>💉 Insulin aspart (速效胰島素) 幫浦面板</h3>", unsafe_allow_html=True)
    
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」及「GA 週數」，系統將自動啟動 Insulin 演算列表。")
    else:
        # 子功能雙適應症導航
        ins_mode = st.radio(
            "請選擇 Insulin aspart 臨床適應症計算機：",
            ["1. 控制血糖初始 PUMP (Continuous IV infusion)", "2. Hyperkalemia PUMP (高血鉀緊急處置)"],
            horizontal=True,
            key="ins_mode_selector"
        )
        st.write("---")

        # ---------------------------------------------------------------------
        # 模式 1: 控制血糖初始 PUMP
        # ---------------------------------------------------------------------
        if ins_mode == "1. 控制血糖初始 PUMP (Continuous IV infusion)":
            # 完整臨床指引與規則劑量區塊
            with st.container(border=True):
                st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#64B5F6;'>📋 控制血糖初始 PUMP 臨床規則與建議劑量</p>", unsafe_allow_html=True)
                st.markdown("""
                    <div style='font-size:12px; color:#ccc; line-height:1.6;'>
                    • <b>Continuous IV infusion</b>: 0.05 IU/kg/hr，建議以 0.01 IU/kg/hr 的增量進行滴定調整 (titrate)。<br>
                    • <b>&lt; 2 kg</b>: 25 IU/kg in HS 50 mL → 初始流速 0.1 mL/hr，增量調整 0.02 mL/hr (範圍: 0.02 - 0.2 mL/hr)。<br>
                    • <b>2 - 4 kg</b>: 12.5 IU/kg in HS 50 mL → 初始流速 0.2 mL/hr，增量調整 0.04 mL/hr (範圍: 0.04 - 0.4 mL/hr)。<br>
                    • <b>4 - 8 kg</b>: 6.25 IU/kg in HS 50 mL → 初始流速 0.4 mL/hr，增量調整 0.08 mL/hr (範圍: 0.08 - 0.8 mL/hr)。
                    </div>
                """, unsafe_allow_html=True)

            st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)
            
            # 1. 根據體重決定級距常數與「最新校正之 Excel 固定初始流速 (I27)」
            if b1_bw < 2.0:
                ins_weight_factor = 25.0
                i_27_suggest_flow = 0.10   # 👈 完美對齊 Excel: 固定 0.1 mL/hr
            elif b1_bw < 4.0:
                ins_weight_factor = 12.5
                i_27_suggest_flow = 0.20   # 👈 完美對齊 Excel: 固定 0.2 mL/hr
            elif b1_bw <= 8.0:
                ins_weight_factor = 6.25
                i_27_suggest_flow = 0.40   # 👈 完美對齊 Excel: 固定 0.4 mL/hr
            else:
                ins_weight_factor = 6.25
                i_27_suggest_flow = 0.40
                
            f_27 = 50.0  # 恆定 HS 50 mL
            
            # C27: Dose = 體重 * 級距常數 * (F27/50)
            c_27 = (b1_bw * ins_weight_factor) * (f_27 / 50.0)
            
            # K27: 初始流速換算後的單位劑量 = C27 / F27 * I27 / 體重 (算出來每級距都會是完美的 0.0500 IU/kg/hr)
            k_27 = (c_27 / f_27) * i_27_suggest_flow / b1_bw if b1_bw > 0 else 0.0
            
            # 2. 呈現並排互動區塊：左邊看「系統自動推薦」，右邊「供護理手動微調輸入」
            ins1_c1, ins1_c2 = st.columns(2)
            
            with ins1_c1:
                st.markdown("""
                    <div style='background-color: #1a2432; padding: 10px 14px; border-radius: 4px; border-left: 4px solid #1E88E5;'>
                        <span style='font-size:13px; font-weight:bold; color:#64B5F6;'>💡 系統初始建議流速狀態 (目標 0.05 IU/kg/hr)</span>
                    </div>
                """, unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Excel 同步初始建議流速:</p><p style='margin:0 0 6px 0; font-size: 22px; font-weight: bold; color: #1E88E5;'>{i_27_suggest_flow:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mL/hr</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 換算後建議初始劑量:</p><p style='margin:0 0 2px 0; font-size: 22px; font-weight: bold; color: #4CAF50;'>{k_27:.4f} <span style='font-size:12px; color:#fff; font-weight:normal;'>IU/kg/hr</span></p>", unsafe_allow_html=True)
            
            with ins1_c2:
                st.markdown("""
                    <div style='background-color: #1e3a1e; padding: 10px 14px; border-radius: 4px; border-left: 4px solid #4CAF50;'>
                        <span style='font-size:13px; font-weight:bold; color:#81C784;'>🔌 目前幫浦手動調速計算區</span>
                    </div>
                """, unsafe_allow_html=True)
                with st.container(border=True):
                    if "p4_ins_user_flow" not in st.session_state:
                        st.session_state["p4_ins_user_flow"] = float(round(i_27_suggest_flow, 2))
                    
                    o_27_user_flow = st.number_input("請輸入設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=st.session_state["p4_ins_user_flow"], step=0.01, format="%.4f", key="ins_user_flow_input")
                    st.session_state["p4_ins_user_flow"] = o_27_user_flow
                    
                    if o_27_user_flow > 0:
                        # Q27: 手動流速換算後單位劑量 = C27 / F27 * O27 / 體重
                        q_27 = (c_27 / f_27) * o_27_user_flow / b1_bw
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 目前實際給予劑量 :</p><p style='margin:0 0 2px 0; font-size: 24px; font-weight: bold; color: #ffb300;'>{q_27:.4f} <span style='font-size:12px; color:#fff; font-weight:normal;'>IU/kg/hr</span></p>", unsafe_allow_html=True)
                    else:
                        st.caption("請輸入流速以啟動暴露劑量換算。")

            st.write("---")
            st.markdown("<p style='margin:0; font-size:13px; color:#ccc; font-weight:bold;'>📋 複製以下完整調配字眼至醫囑或護理交班：</p>", unsafe_allow_html=True)
            st.code(f"抽取 Insulin aspart {c_27:.3f} IU 加入 HS 至 50 mL", language="text")

        # ---------------------------------------------------------------------
        # 模式 2: Hyperkalemia PUMP
        # ---------------------------------------------------------------------
        elif ins_mode == "2. Hyperkalemia PUMP (高血鉀緊急處置)":
            with st.container(border=True):
                st.markdown("<p style='margin:0; font-size:14px; font-weight:bold; color:#e53935;'>📋 Hyperkalemia 臨床處置指引安全規則</p>", unsafe_allow_html=True)
                st.markdown("""
                    <div style='font-size:12px; color:#ccc; line-height:1.6;'>
                    • <b>Insulin 劑量</b>: 0.1 IU/kg ( 單次最大極限 Max: 10 IU )，需於 30 分鐘內微量點滴滴注完成。<br>
                    • <b>IV Glucose 同步糖防線</b>: 0.5 g/kg over 30 mins。<br>
                    • <b>&lt; 5 歲兒童 D10W 規格</b>: 建議使用 D10W 5 mL/kg ( D10W 最大極限 250 mL；若使用 D25W 則最大極限 100 mL )。
                    </div>
                """, unsafe_allow_html=True)

            st.write("<div style='height:8px;'></div>", unsafe_allow_html=True)
            
            # Excel 核心公式演算 (C36 = 0.1 * 體重, F36 = 5 * 體重)
            c_36_raw = 0.1 * b1_bw
            c_36_insulin_dose = min(10.0, c_36_raw) # 鎖死最大 10 IU 安全極限
            
            f_36_glucose_ml = 5.0 * b1_bw
            f_36_glucose_ml = min(250.0, f_36_glucose_ml) # 鎖死最大 250 mL 安全極限
            
            # 計算同步葡萄糖公克數 (0.5g/kg)
            glucose_grams = 0.5 * b1_bw

            ins2_col1, ins2_col2 = st.columns(2)
            
            with ins2_col1:
                st.markdown("""
                    <div style='background-color: #2c1616; padding: 10px 14px; border-radius: 4px; border-left: 4px solid #e53935;'>
                        <span style='font-size:13px; font-weight:bold; color:#ef5350;'>🟥 胰島素計算劑量 (C36, Over 30 mins)</span>
                    </div>
                """, unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 應抽取 Insulin 總量:</p><p style='margin:0 0 2px 0; font-size: 24px; font-weight: bold; color: #ef5350;'>{c_36_insulin_dose:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>IU</span></p>", unsafe_allow_html=True)
            
            with ins2_col2:
                st.markdown("""
                    <div style='background-color: #2b2214; padding: 10px 14px; border-radius: 4px; border-left: 4px solid #ffb300;'>
                        <span style='font-size:13px; font-weight:bold; color:#ffb300;'>🟨 同步葡萄糖防線 (F36, Over 30 mins)</span>
                    </div>
                """, unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 應給予 D10W 總量:</p><p style='margin:0 0 2px 0; font-size: 24px; font-weight: bold; color: #ffb300;'>{f_36_glucose_ml:.2f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mL</span> <span style='font-size:13px; color:#9ea7ad; font-weight:normal;'>(={glucose_grams:.2f} g)</span></p>", unsafe_allow_html=True)

            st.write("---")
            st.markdown("<p style='margin:0; font-size:13px; color:#ccc; font-weight:bold;'>📋 複製以下完整高血鉀處置調配字眼：</p>", unsafe_allow_html=True)
            st.code(f"【高血鉀緊急處置】抽取 Insulin aspart {c_36_insulin_dose:.3f} IU 混合於 D10W {f_36_glucose_ml:.2f} mL 中，於 30 分鐘內點滴滴注完畢。", language="text")
            
# =============================================================================
# 💤 區塊 5: Dexmedetomidine —— 全局隔離，絕對不跳
# =============================================================================
if main_page == "💤 Dexmedetomidine":
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」，系統將即時啟動 Dexmedetomidine 稀釋流速核算面板。")
    else:
        st.markdown("<h3 style='margin:0px 0px 10px 0px;'>💤 Dexmedetomidine 四種配方濃度流速與劑量換算器</h3>", unsafe_allow_html=True)
        
        dex_r1_c1, dex_r1_c2 = st.columns(2)
        with dex_r1_c1:
            with st.container(border=True):
                st.markdown("### 🧪 **配方一：1 mL in NS 5 mL** &nbsp;&nbsp;`(20 mcg/mL)`")
                d1_min = b1_bw * 0.01; d1_max = b1_bw * 0.07
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議流速區間 (0.2-1.4 mcg/kg/hr):</p><p style='margin:0 0 10px 0; font-size: 18px; font-weight: bold; color: #1E88E5;'>{d1_min:.3f} mL/hr &nbsp;<span style='color:#555; font-weight:normal;'>~</span>&nbsp; {d1_max:.3f} mL/hr</p>", unsafe_allow_html=True)
                j2_val = st.number_input("請輸入配方一設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d1_min, 3)) if d1_min > 0 else 0.0, step=0.01, key="j2_flow")
                l2_dose = (100.0 / 5.0 * j2_val) / b1_bw if b1_bw > 0 else 0.0
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:14px; color:#ccc;'>🧮 換算後流速劑量：</p><p style='margin:0; font-size: 22px; font-weight: bold; color: #4CAF50;'>{l2_dose:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mcg/kg/hr</span></p>", unsafe_allow_html=True)
        with dex_r1_c2:
            with st.container(border=True):
                st.markdown("### 🧪 **配方二：1 mL in NS 8.333 mL** &nbsp;&nbsp;`(12 mcg/mL)`")
                d2_min = b1_bw * 0.0166; d2_max = b1_bw * 0.116
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議流速區間:</p><p style='margin:0 0 10px 0; font-size: 18px; font-weight: bold; color: #1E88E5;'>{d2_min:.3f} mL/hr &nbsp;<span style='color:#555; font-weight:normal;'>~</span>&nbsp; {d2_max:.3f} mL/hr</p>", unsafe_allow_html=True)
                j3_val = st.number_input("請輸入配方二設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d2_min, 3)) if d2_min > 0 else 0.0, step=0.01, key="j3_flow")
                l3_dose = (100.0 / 8.333 * j3_val) / b1_bw if b1_bw > 0 else 0.0
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:14px; color:#ccc;'>🧮 換算後流速劑量：</p><p style='margin:0; font-size: 22px; font-weight: bold; color: #4CAF50;'>{l3_dose:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mcg/kg/hr</span></p>", unsafe_allow_html=True)

        st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
        dex_r2_c1, dex_r2_c2 = st.columns(2)
        with dex_r2_c1:
            with st.container(border=True):
                st.markdown("### 🧪 **配方三：1 mL in NS 12.5 mL** &nbsp;&nbsp;`(8 mcg/mL)`")
                d3_min = b1_bw * 0.025; d3_max = b1_bw * 0.175
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議流速區間:</p><p style='margin:0 0 10px 0; font-size: 18px; font-weight: bold; color: #1E88E5;'>{d3_min:.3f} mL/hr &nbsp;<span style='color:#555; font-weight:normal;'>~</span>&nbsp; {d3_max:.3f} mL/hr</p>", unsafe_allow_html=True)
                j4_val = st.number_input("請輸入配方三設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d3_min, 3)) if d3_min > 0 else 0.0, step=0.01, key="j4_flow")
                l4_dose = (100.0 / 12.5 * j4_val) / b1_bw if b1_bw > 0 else 0.0
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:14px; color:#ccc;'>🧮 換算後流速劑量：</p><p style='margin:0; font-size: 22px; font-weight: bold; color: #4CAF50;'>{l4_dose:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mcg/kg/hr</span></p>", unsafe_allow_html=True)
        with dex_r2_c2:
            st.markdown("<div style='background-color:#2b2214; padding:2px 10px; border-radius:4px 4px 0 0; border-left:4px solid #ffb300; border-top:1px solid #ffb300; border-right:1px solid #ffb300;'><span style='color:#ffb300; font-weight:bold; font-size:13px;'>🌟 臨床最推薦調配配方 (流速操作範圍最安全)</span></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("### 🌟 **配方四：1 mL in NS 25 mL** &nbsp;&nbsp;`(4 mcg/mL)`")
                d4_min = b1_bw * 0.05; d4_max = b1_bw * 0.35
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 建議流速區間 (安全操作空間大):</p><p style='margin:0 0 10px 0; font-size: 19px; font-weight: bold; color: #ffb300;'>{d4_min:.3f} mL/hr &nbsp;<span style='color:#555; font-weight:normal;'>~</span>&nbsp; {d4_max:.3f} mL/hr</p>", unsafe_allow_html=True)
                j5_val = st.number_input("請輸入配方四設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d4_min, 3)) if d4_min > 0 else 0.0, step=0.01, key="j5_flow")
                l5_dose = (100.0 / 25.0 * j5_val) / b1_bw if b1_bw > 0 else 0.0
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:14px; color:#ccc;'>🧮 換算後流速劑量：</p><p style='margin:0; font-size: 24px; font-weight: bold; color: #ffb300;'>{l5_dose:.3f} <span style='font-size:13px; color:#fff; font-weight:normal;'>mcg/kg/hr</span></p>", unsafe_allow_html=True)

# --- 底部專業版權宣告 ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: #888888; font-size: 12px; line-height: 1.6;'>
        🔒 <b>臨床決策支援系統 (CDSS) 免責宣告</b>：本工具計算結果僅供醫療專業人員參考核對，處方開立仍應以臨床實際病情與主治醫師之最終判斷為準。<br>
        <b>版權為中國醫藥大學附設醫院藥劑部 臨床藥學科 臨床服務組 張運佳藥師 所有 <span style='color: #ff8a80; font-weight: bold;'>請勿隨意轉傳</span></b>
    </div>
    """, 
    unsafe_allow_html=True
)
