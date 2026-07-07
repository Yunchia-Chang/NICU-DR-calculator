import streamlit as st

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
st.sidebar.header("📥 病患基本資料輸入")
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

# 側邊欄：常用藥物大項
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
    ]
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

# 核心功能頁籤
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💊 常用藥物計算機", "⚡ Ion dosage", "🫁 DART.BURST", "🔌 PUMP 總表115", "💤 Dexmedetomidine"
])

# =============================================================================
# TAB 1: 常用藥物計算機 (分類 1 ~ 9)
# =============================================================================
with tab1:
    st.markdown(f"<h3 style='margin:0px 0px 10px 0px;'>📂 當前分類：{category}</h3>", unsafe_allow_html=True)
    
    if category == "1. Antimicrobial agents":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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

    elif category == "2. Diuretics":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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

    elif category == "3. PDA":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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

    elif category == "4. 肺高壓":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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

    elif category == "5. Apnea/RDS Surfactant":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            ap_col1, ap_col2, ap_col3 = st.columns(3)
            with ap_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Aminophylline**")
                    st.markdown("---")
                    ap_load = 5.0 * b1_bw; ap_maint = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ap_load:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ap_maint:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with ap_col2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Theophylline**")
                    st.markdown("---")
                    theo_load_mg = 5.0 * b1_bw; theo_load_ml = theo_load_mg / 5.34
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{theo_load_mg:.2f} <span style='font-size:12px; color:#fff; font-weight:normal;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{theo_load_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    theo_maint_mg = 1.0 * b1_bw; theo_maint_ml = theo_maint_mg / 5.34
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose:</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{theo_maint_mg:.2f} <span style='font-size:12px; font-weight:normal;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{theo_maint_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose frequency:</p><p style='margin:0 0 2px 0; font-size: 16px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            with ap_col3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Caffeine citrate**")
                    st.markdown("---")
                    caf_load = 20.0 * b1_bw; caf_maint = 10.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Loading dose(20 mg/kg):</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{caf_load:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Maintain dose(10 mg/kg):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{caf_maint:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            ap_col4, _, _ = st.columns(3)
            with ap_col4:
                with st.container(border=True):
                    st.markdown("## 🫁 **Poractant alfa: ET**")
                    st.markdown("---")
                    pnt_mg = 200.0 * b1_bw; pnt_ml = 2.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose / 換算後mL數:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pnt_mg:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{pnt_ml:.1f} mL/dose</span></p>", unsafe_allow_html=True)

    elif category == "6. Seizure control":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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

    elif category == "7. Sedation":
        if not has_input: st.info("💡 正在等待左側輸入病健基本資料...")
        else:
            sd_col1, _, _ = st.columns(3)
            with sd_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Chloral hydrate 10%**")
                    sd_dose_mg = 25.0 * b1_bw; sd_dose_ml = sd_dose_mg / 100.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose / 換算後mL數:</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sd_dose_mg:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; <span style='color:#4CAF50;'>{sd_dose_ml:.2f} mL/dose</span></p>", unsafe_allow_html=True)

    elif category == "8. Miscellaneous.GCSF":
        if not has_input: st.info("💡 正在等待左側輸入病健基本資料...")
        else:
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

    elif category == "9. 胃腸類藥品/營養補充品/維他命/其它":
        if not has_input: st.info("💡 正在等待左側輸入病患基本資料...")
        else:
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
                    st.markdown("## 🪵 **Dioctahedral Smectite**")
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
                    st.markdown("## 🦋 **Levothyroxine**")
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
# TAB 3: DART.BURST
# =============================================================================
with tab3:
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」，系統將即時啟動 BPD 類固醇療程減量面板。")
    else:
        st.markdown("<p style='color:#ffb300; font-weight:bold; font-size:14px; margin-bottom:10px;'>📊 系統核對模式：全功能已依據病盤體重同步演算，單行直槓並排以極致壓縮視覺空間。</p>", unsafe_allow_html=True)
        
        bpd_col1, bpd_col2, bpd_col3 = st.columns(3)
        with bpd_col1:
            with st.container(border=True):
                st.markdown("## 🟥 **Burst (BPD burst) — Prednisolone**")
                st.markdown("---")
                burst_dose = 1.0 * b1_bw
                st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage I</b> (1mg/kg/dose Q6H 2 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q6H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>2 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage II</b> (1mg/kg/dose Q12H 2 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>2 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage III</b> (1mg/kg/dose QD 2 days):</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{burst_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>QD</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>2 days</span>
                </p>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height:44px;'></div>", unsafe_allow_html=True)
        with bpd_col2:
            with st.container(border=True):
                st.markdown("## 🟦 **Dart (Dexamethasone)**")
                st.markdown("---")
                dart_s1 = 0.075 * b1_bw; dart_s2 = 0.05 * b1_bw; dart_s3 = 0.025 * b1_bw; dart_s4 = 0.01 * b1_bw
                st.markdown(f"""
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage I</b> (0.15mg/kg/day 3 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>
                    {dart_s1:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>3 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage II</b> (0.1mg/kg/day 3 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>
                    {dart_s2:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>3 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage III</b> (0.05mg/kg/day 2 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>
                    {dart_s3:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>2 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage IV</b> (0.02mg/kg/day 2 days):</p><p style='margin:0; font-size: 20px; font-weight: bold; color: #1E88E5;'>
                    {dart_s4:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>2 days</span>
                </p>
                """, unsafe_allow_html=True)
        with bpd_col3:
            with st.container(border=True):
                st.markdown("## 🟩 **STOP-BPD protocol (Hydrocortisone)**")
                st.markdown("---")
                hydro_dose = 0.5 * b1_bw
                st.markdown(f"""
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage I</b> (1 mg/kg/day Q12h 7 days):</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{hydro_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>Q12H</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>7 days</span>
                </p>
                <p style='margin:1px 0; font-size:14px; color:#888;'>• <b>Stage II</b> (0.5mg/kg/day QD for 3 days):</p><p style='margin:0 0 10px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{hydro_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#F4511E; font-size:16px;'>QD</span> &nbsp;<span style='color:#555; font-weight:normal;'>|</span>&nbsp; 
                    <span style='color:#4CAF50; font-size:16px;'>3 days</span>
                </p>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height:144px;'></div>", unsafe_allow_html=True)

# =============================================================================
# TAB 4: PUMP 總表115
# =============================================================================
with tab4: 
    st.info("⏳ PUMP 總表115 微流速調配模組建構中...")

# =============================================================================
# 🎯 TAB 5: Dexmedetomidine (⚡ 新增：設定流速超限自動變紅防呆警示功能)
# =============================================================================
with tab5:
    if not has_input:
        st.warning("⚠️ 請先於左側輸入「BW 體重」，系統將即時啟動 Dexmedetomidine 稀釋流速核算面板。")
    else:
        st.markdown("<h3 style='margin:0px 0px 10px 0px;'>💤 Dexmedetomidine 四種配方濃度流速與劑量換算器</h3>", unsafe_allow_html=True)
        
        # --- 4種配方獨立流速與超限背景變紅判定邏輯 ---
        dex_r1_c1, dex_r1_c2 = st.columns(2)
        
        # 配方一：20 mcg/mL
        with dex_r1_c1:
            d1_min = b1_bw * 0.01
            d1_max = b1_bw * 0.07
            
            # 先行宣告互動輸入框取得數值
            j2_val = st.number_input("請輸入配方一設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d1_min, 3)) if d1_min > 0 else 0.0, step=0.01, key="j2_flow")
            l2_dose = (100.0 / 5.0 * j2_val) / b1_bw if b1_bw > 0 else 0.0
            
            # ⚡ 防呆判斷：若超出區間，將注入深紅背景樣式
            is_d1_out = (j2_val < d1_min or j2_val > d1_max) if has_input else False
            bg_color_d1 = "#3c1414; border: 1px solid #ff4444;" if is_d1_out else "#1a1a1a; border: 1px solid #333;"
            
            st.markdown(f"""
            <div style='background-color: {bg_color_d1} padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <h3 style='color:#fff; margin:0;'>🧪 配方一：5 mL <span style='font-size:14px; color:#888;'>(20 mcg/mL)</span></h3>
                <p style='margin:4px 0; font-size:13px; color:#aaa;'>安全範圍: {d1_min:.3f} ~ {d1_max:.3f} mL/hr</p>
                <p style='margin:2px 0; font-size:16px; font-weight:bold;'>
                    當前換算劑量: <span style='color:#64B5F6;'>{l2_dose:.3f} mcg/kg/hr</span>
                </p>
                {"<p style='color:#ff4444; font-size:12px; margin:2px 0 0 0; font-weight:bold;'>⚠️ 警告：流速已超出安全建議範圍！</p>" if is_d1_out else ""}
            </div>
            """, unsafe_allow_html=True)

        # 配方二：12 mcg/mL
        with dex_r1_c2:
            d2_min = b1_bw * 0.0166
            d2_max = b1_bw * 0.116
            
            j3_val = st.number_input("請輸入配方二設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d2_min, 3)) if d2_min > 0 else 0.0, step=0.01, key="j3_flow")
            l3_dose = (100.0 / 8.333 * j3_val) / b1_bw if b1_bw > 0 else 0.0
            
            is_d2_out = (j3_val < d2_min or j3_val > d2_max) if has_input else False
            bg_color_d2 = "#3c1414; border: 1px solid #ff4444;" if is_d2_out else "#1a1a1a; border: 1px solid #333;"
            
            st.markdown(f"""
            <div style='background-color: {bg_color_d2} padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <h3 style='color:#fff; margin:0;'>🧪 配方二：8.333 mL <span style='font-size:14px; color:#888;'>(12 mcg/mL)</span></h3>
                <p style='margin:4px 0; font-size:13px; color:#aaa;'>安全範圍: {d2_min:.3f} ~ {d2_max:.3f} mL/hr</p>
                <p style='margin:2px 0; font-size:16px; font-weight:bold;'>
                    當前換算劑量: <span style='color:#64B5F6;'>{l3_dose:.3f} mcg/kg/hr</span>
                </p>
                {"<p style='color:#ff4444; font-size:12px; margin:2px 0 0 0; font-weight:bold;'>⚠️ 警告：流速已超出安全建議範圍！</p>" if is_d2_out else ""}
            </div>
            """, unsafe_allow_html=True)

        st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
        dex_r2_c1, dex_r2_c2 = st.columns(2)
        
        # 配方三：8 mcg/mL
        with dex_r2_c1:
            d3_min = b1_bw * 0.025
            d3_max = b1_bw * 0.175
            
            j4_val = st.number_input("請輸入配方三設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d3_min, 3)) if d3_min > 0 else 0.0, step=0.01, key="j4_flow")
            l4_dose = (100.0 / 12.5 * j4_val) / b1_bw if b1_bw > 0 else 0.0
            
            is_d3_out = (j4_val < d3_min or j4_val > d3_max) if has_input else False
            bg_color_d3 = "#3c1414; border: 1px solid #ff4444;" if is_d3_out else "#1a1a1a; border: 1px solid #333;"
            
            st.markdown(f"""
            <div style='background-color: {bg_color_d3} padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <h3 style='color:#fff; margin:0;'>🧪 配方三：12.5 mL <span style='font-size:14px; color:#888;'>(8 mcg/mL)</span></h3>
                <p style='margin:4px 0; font-size:13px; color:#aaa;'>安全範圍: {d3_min:.3f} ~ {d3_max:.3f} mL/hr</p>
                <p style='margin:2px 0; font-size:16px; font-weight:bold;'>
                    當前換算劑量: <span style='color:#64B5F6;'>{l4_dose:.3f} mcg/kg/hr</span>
                </p>
                {"<p style='color:#ff4444; font-size:12px; margin:2px 0 0 0; font-weight:bold;'>⚠️ 警告：流速已超出安全建議範圍！</p>" if is_d3_out else ""}
            </div>
            """, unsafe_allow_html=True)

        # 🌟 配方四：4 mcg/mL (最推薦配方，同樣加入超限紅色熔斷機制)
        with dex_r2_c2:
            d4_min = b1_bw * 0.05
            d4_max = b1_bw * 0.35
            
            j5_val = st.number_input("請輸入配方四設定流速 (mL/hr)", min_value=0.0, max_value=5.0, value=float(round(d4_min, 3)) if d4_min > 0 else 0.0, step=0.01, key="j5_flow")
            l5_dose = (100.0 / 25.0 * j5_val) / b1_bw if b1_bw > 0 else 0.0
            
            is_d4_out = (j5_val < d4_min or j5_val > d4_max) if has_input else False
            # 觸發警告時變成紅色卡片，正常時保持原本的推薦黃黑對比卡片
            bg_color_d4 = "#3c1414; border: 1px solid #ff4444;" if is_d4_out else "#2b2214; border: 1px solid #ffb300;"
            text_color_d4 = "#ff4444" if is_d4_out else "#ffb300"
            
            st.markdown(f"""
            <div style='background-color: {bg_color_d4} padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <h3 style='color:{text_color_d4}; margin:0;'>🌟 配方四：25 mL <span style='font-size:14px; color:#aaa;'>(4 mcg/mL)</span></h3>
                <p style='margin:4px 0; font-size:13px; color:#aaa;'>安全範圍: {d4_min:.3f} ~ {d4_max:.3f} mL/hr (操作空間最大)</p>
                <p style='margin:2px 0; font-size:16px; font-weight:bold;'>
                    當前換算劑量: <span style='color:{text_color_d4}; text-decoration:underline;'>{l5_dose:.3f} mcg/kg/hr</span>
                </p>
                {"<p style='color:#ff4444; font-size:12px; margin:2px 0 0 0; font-weight:bold;'>⚠️ 警告：流速已超出安全建議範圍！</p>" if is_d4_out else "<p style='color:#4CAF50; font-size:12px; margin:2px 0 0 0; font-weight:bold;'>✓ 臨床最推薦調配配方</p>"}
            </div>
            """, unsafe_allow_html=True)

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
