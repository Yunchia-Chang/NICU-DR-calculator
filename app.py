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
b1_bw = st.sidebar.number_input("BW 體重 (B1) (kg)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

st.sidebar.write("---")
st.sidebar.markdown("**GA 胎齡 (F1 + H1)**")
f1_ga_wk = st.sidebar.number_input("GA 週數 (F1)", min_value=0, max_value=45, value=0, step=1)
h1_ga_day = st.sidebar.number_input("GA 天數 (H1)", min_value=0, max_value=6, value=0, step=1)

st.sidebar.write("---")
l1_pna = st.sidebar.number_input("PNA 出生天數 (L1) (days)", min_value=0, max_value=365, value=0, step=1)

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
        "5. Apnea",
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
            <span style='font-size:14px; color:#fff;'>| &nbsp;🧮 <b>PMA [Q1+S1]:</b> <span style='color:#4CAF50; font-weight:bold;'>{q1_pma_wk} 週 + {s1_pma_day} 天</span></span>
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

with tab1:
    st.markdown(f"<h3 style='margin:0px 0px 10px 0px;'>📂 當前分類：{category}</h3>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 大項 1: Antimicrobial agents
    # -------------------------------------------------------------
    if category == "1. Antimicrobial agents":
        if not has_input:
            st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            with r1_c1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Ampicillin**")
                    if ga_total_days <= 244:
                        amp_b4 = b1_bw * 50 if l1_pna <= 7 else b1_bw * 75
                        amp_d4 = "Q12H"
                        norm_ok = True
                    else:
                        if l1_pna <= 28:
                            amp_b4 = b1_bw * 50
                            amp_d4 = "Q8H"
                            norm_ok = True
                        else:
                            amp_b4 = "超過28天(請手動確認)"
                            norm_ok = False
                    if norm_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b4:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d4}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {amp_b4}</p>", unsafe_allow_html=True)
                    amp_b5 = b1_bw * 100 if l1_pna <= 7 else b1_bw * 75
                    amp_d5 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b5:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d5}</span></p>", unsafe_allow_html=True)
                    amp_b6 = b1_bw * 50
                    amp_d6 = "60 mins prior"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Surgical prophylaxis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b6:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>{amp_d6}</span></p>", unsafe_allow_html=True)
            
            with r1_c2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Cefotaxime**")
                    if b1_bw <= 2:
                        ctx_b8 = b1_bw * 50 if l1_pna <= 28 else "超過28天(請手動確認)"
                        ctx_b8_ok = False if l1_pna > 28 else True
                    else:
                        if l1_pna <= 7:
                            ctx_b8 = b1_bw * 50
                            ctx_b8_ok = True
                        elif l1_pna <= 28:
                            ctx_b8 = b1_bw * 37.5
                            ctx_b8_ok = True
                        else:
                            ctx_b8 = b1_bw * 50 if l1_pna <= 60 else "超過60天(請手動確認)"
                            ctx_b8_ok = False if l1_pna > 60 else True
                    if b1_bw <= 2:
                        ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else "確認醫囑")
                    else:
                        ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    if ctx_b8_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b8:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d8}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {ctx_b8}</p>", unsafe_allow_html=True)
                    ctx_b9 = b1_bw * 50
                    ctx_d9 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b9:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d9}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
            
            with r1_c3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Gentamicin**")
                    if ga_total_days <= 209:
                        gen_b11 = b1_bw * 5
                    else:
                        gen_b11 = b1_bw * 4 if l1_pna <= 7 else b1_bw * 5
                    if ga_total_days <= 209:
                        gen_d11 = "Q36H" if l1_pna <= 14 else "Q24H"
                    else:
                        if ga_total_days <= 244:
                            gen_d11 = "Q36H" if l1_pna <= 10 else "QD"
                        else:
                            gen_d11 = "QD"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{gen_b11:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{gen_d11}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r2_c1, r2_c2, r2_c3 = st.columns(3)
            with r2_c1:
                with st.container(border=True):
                    st.markdown("## 🟧 **Cefazolin**")
                    if l1_pna <= 28:
                        cfz_b13 = b1_bw * 25 if b1_bw <= 2 else b1_bw * 50
                        cfz_b13_ok = True
                    else:
                        cfz_b13 = b1_bw * 150 / 4 if l1_pna <= 60 else "超過60天(請手動確認)"
                        cfz_b13_ok = False if l1_pna > 60 else True
                    cfz_d13 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    if cfz_b13_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{cfz_b13:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d13}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {cfz_b13}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Perioperative dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>30-60 mins prior</span></p>", unsafe_allow_html=True)
                    cfz_d15 = "Q12H" if l1_pna <= 7 else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Postoperative dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d15}</span></p>", unsafe_allow_html=True)
            
            with r2_c2:
                with st.container(border=True):
                    st.markdown("### 🟪 **Piperacillin 2g + Tazobactam 0.25g**")
                    if b1_bw <= 2:
                        pt_b17 = b1_bw * 112.5 if l1_pna <= 7 else (b1_bw * 112.5 if q1_pma_wk <= 30 else b1_bw * 90)
                        pt_d17 = "Q8H" if l1_pna <= 7 else ("Q8H" if q1_pma_wk <= 30 else "Q6H")
                    else:
                        pt_b17 = b1_bw * 90
                        pt_d17 = "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pt_b17:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{pt_d17}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)
            
            with r2_c3:
                with st.container(border=True):
                    st.markdown("### 🟫 **Amoxicillin 1g + Clavulanate 0.2g 5:1(IV)**")
                    amx_iv_b19 = min(1200.0, b1_bw * 30)
                    amx_iv_d19 = "Q8H" if (ga_total_days >= 90 and l1_pna >= 4) else "Q12H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_iv_b19:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amx_iv_d19}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r3_c1, r3_c2, r3_c3 = st.columns(3)
            with r3_c1:
                with st.container(border=True):
                    st.markdown("### 🧪 **液粉(複方)(4:1)Amoxicillin 50 mg + Clavulanic acid 12.5 mg/mL : PO**")
                    amx_po_b21 = b1_bw * 0.3
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_po_b21:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span> <span style='font-size: 17px; color: #F4511E; margin-left: 8px;'>Q12H</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:94px;'></div>", unsafe_allow_html=True)
            
            with r3_c2:
                with st.container(border=True):
                    st.markdown("### 🛸 **Meropenem**")
                    mrp_b23 = b1_bw * 20 if ga_total_days <= 223 else (b1_bw * 20 if l1_pna < 14 else b1_bw * 30)
                    mrp_d23 = "Q12H" if (ga_total_days <= 223 and l1_pna < 14) else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b23:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d23}</span></p>", unsafe_allow_html=True)
                    mrp_b24_ok = True
                    if l1_pna <= 60:
                        mrp_b24 = b1_bw * 40
                    else:
                        mrp_b24 = "超過60天(請手動確認)"
                        mrp_b24_ok = False
                    mrp_d24 = ("Q12H" if l1_pna < 14 else "Q8H") if b1_bw <= 2 else "Q8H"
                    if mrp_b24_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b24:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d24}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {mrp_b24}</p>", unsafe_allow_html=True)
            
            with r3_c3:
                with st.container(border=True):
                    st.markdown("### 🥊 **Vancomycin (Initial)**")
                    vnc_b26 = b1_bw * 15
                    vnc_d26 = "Q24H" if (ga_total_days + l1_pna) < 203 else ("Q12H" if (ga_total_days + l1_pna) < 252 else "Q8H")
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Initial dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b26:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d26}</span></p>", unsafe_allow_html=True)
                    if b1_bw < 2:
                        vnc_b27 = "體重<2kg(請手動確認)"
                        vnc_b27_ok = False
                    else:
                        vnc_b27 = b1_bw * 10 if l1_pna <= 7 else b1_bw * 11.25
                        vnc_d27 = "Q8H" if l1_pna <= 7 else "Q6H"
                        vnc_b27_ok = True
                    if vnc_b27_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b27:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d27}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {vnc_b27}</p>", unsafe_allow_html=True)

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
            with r4_c3:
                st.write("")

    # -------------------------------------------------------------
    # 大項 2: Diuretics
    # -------------------------------------------------------------
    elif category == "2. Diuretics":
        if not has_input:
            st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            d_r1_c1, d_r1_c2, d_r1_c3 = st.columns(3)
            with d_r1_c1:
                with st.container(border=True):
                    st.markdown("## 💧 **Furosemide**")
                    furo_po = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• PO dose (I4):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{furo_po:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-48h</span></p>", unsafe_allow_html=True)
                    furo_oral_ml = furo_po / 10.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• oral dosage(1mg/mL) (N4):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{furo_oral_ml:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span></p>", unsafe_allow_html=True)
                    furo_iv = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• IM, intermittent IV (I5):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{furo_iv:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD-QOD</span></p>", unsafe_allow_html=True)
            
            with d_r1_c2:
                with st.container(border=True):
                    st.markdown("## 🧪 **Bumetanide**")
                    st.caption("Dose Range: 0.01-0.06 mg/kg")
                    bt_preterm = 0.01 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Preterm dosage(0.01mg/kg) (I7):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{bt_preterm:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-48H</span></p>", unsafe_allow_html=True)
                    bt_term = 0.01 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Term dosage(0.01mg/kg) (I8):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{bt_term:.3f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12-24h</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:36px;'></div>", unsafe_allow_html=True)
            
            with d_r1_c3:
                with st.container(border=True):
                    st.markdown("## 💊 **Spironolactone**")
                    sp_bpd = 1.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• BPD dose (I10):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sp_bpd:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12H</span></p>", unsafe_allow_html=True)
                    sp_edema = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Edema dose(Range:1-3mg/kg) (I11):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{sp_edema:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD-Q12H</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:1px 0; font-size:13px; font-weight:bold; color:#64B5F6;'>🧪 泡製後劑量動態計算 (M12/M13)：</p>", unsafe_allow_html=True)
                    m12_input = st.number_input("請輸入自訂泡製後劑量 (mg/dose) [M12]", min_value=0.0, max_value=50.0, value=float(round(sp_bpd, 2)), step=0.1, key="m12_sp")
                    m13_ml = m12_input / 5.0
                    st.markdown(f"<p style='margin:3px 0 0 0; font-size:13px; color:#ffb300;'>泡製1# in DW 5ml (5mg/mL) 稀釋後冷藏14天 (M13):</p><p style='margin:0; font-size: 21px; font-weight: bold; color: #4CAF50;'>{m13_ml:.2f} mL/dose</p>", unsafe_allow_html=True)

            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            d_r2_c1, d_r2_c2, d_r2_c3 = st.columns(3)
            with d_r2_c1:
                with st.container(border=True):
                    st.markdown("## 🪵 **Trichlormethiazide**")
                    tcm_dose = 0.04 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Initial dose(Range:0.04-1.6mg/kg/day) (I14):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{tcm_dose:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD-Q12H</span></p>", unsafe_allow_html=True)
            
            with d_r2_c2:
                with st.container(border=True):
                    st.markdown("## 🧊 **Mannitol 20%**")
                    mnt_icp_mg = 0.25 * b1_bw
                    mnt_icp_ml = (0.25 * b1_bw) / 200.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• ICP(0.25mg/kg) (I16/L16):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mnt_icp_mg:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;|&nbsp; <span style='color:#4CAF50;'>{mnt_icp_ml:.4f} mL/dose</span></p>", unsafe_allow_html=True)
                    mnt_iop_mg = 1.5 * b1_bw
                    mnt_iop_ml = (1.5 * b1_bw) / 200.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• IOP(1.5mg/kg) (I17/L17):</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mnt_iop_mg:.2f} <span style='font-size:12px; color:#fff;'>mg/dose</span> &nbsp;|&nbsp; <span style='color:#4CAF50;'>{mnt_iop_ml:.4f} mL/dose</span></p>", unsafe_allow_html=True)
            with d_r2_c3:
                st.write("")

    # -------------------------------------------------------------
    # 大項 3: PDA
    # -------------------------------------------------------------
    elif category == "3. PDA":
        if not has_input:
            st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            pda_col1, pda_col2, pda_col3 = st.columns(3)
            with pda_col1:
                with st.container(border=True):
                    st.markdown("## 🧬 **Ibuprofen (Standard)**")
                    st.markdown("---")
                    ibu_1st = 10 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard dose(10mg/kg) 1st dose (I19):</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ibu_1st:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    ibu_follow = 5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard following dose(5mg/kg)2nd ,3rd doses (L19):</p><p style='margin:0 0 8px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ibu_follow:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown("<p style='margin:4px 0 2px 0; font-size:13px; font-weight:bold; color:#64B5F6;'>🧪 口服劑型換算後體積 (ORAL):</p>", unsafe_allow_html=True)
                    ibu_1st_oral_ml = (10 * b1_bw) / 20.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• 1st dose ORAL 換算後mL數 (O19):</p><p style='margin:0 0 6px 0; font-size: 19px; font-weight: bold; color: #4CAF50;'>{ibu_1st_oral_ml:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span></p>", unsafe_allow_html=True)
                    ibu_follow_oral_ml = (5 * b1_bw) / 20.0
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• 2nd ,3rd doses ORAL 換算後mL數 (P19):</p><p style='margin:0; font-size: 19px; font-weight: bold; color: #4CAF50;'>{ibu_follow_oral_ml:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span></p>", unsafe_allow_html=True)
            
            with pda_col2:
                with st.container(border=True):
                    st.markdown("## 💊 **Propacetamol**")
                    st.markdown("---")
                    prop_dose = 30 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard dose(30mg/kg) (I20):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{prop_dose:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency (K20):</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)
            
            with pda_col3:
                with st.container(border=True):
                    st.markdown("## 🧫 **Acetaminophen**")
                    st.markdown("---")
                    ace_mg = 15 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Standard dose(15mg/kg) (I21):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{ace_mg:.1f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    ace_ml = ace_mg / 24.0
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• 換算後mL數 (N21 = I21/24):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #4CAF50;'>{ace_ml:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency (K21):</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 🎯 大項 4: 肺高壓 (全面激活並對齊新視覺，對應 image_da466a.png)
    # -------------------------------------------------------------
    elif category == "4. 肺高壓":
        if not has_input:
            st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            ph_col1, ph_col2, ph_col3 = st.columns(3)
            
            # 1. Sildenafil
            with ph_col1:
                with st.container(border=True):
                    st.markdown("## 🟥 **Sildenafil**")
                    st.markdown("---")
                    
                    sil_dose = 0.5 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose(Range:0.5-2mg/kg) (0.5mg/kg) (I24):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{sil_dose:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency (K24):</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q6H</p>", unsafe_allow_html=True)
            
            # 2. Bosentan
            with ph_col2:
                with st.container(border=True):
                    st.markdown("## 🟦 **Bosentan**")
                    st.markdown("---")
                    
                    bos_dose = 1.0 * b1_bw
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose (I25):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #1E88E5;'>{bos_dose:.2f} <span style='font-size:13px; color:#fff;'>mg/dose</span></p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency (K25):</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q12H</p>", unsafe_allow_html=True)
            
            # 3. Iloprost
            with ph_col3:
                with st.container(border=True):
                    st.markdown("## 🟩 **Iloprost**")
                    st.markdown("---")
                    
                    ilo_dose = 0.5 * b1_bw
                    # 💡 依照 image_da466a.png 精準切換單位為 mcg/dose
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Dose(Range:0.5-2mcg/kg) (0.5mcg/kg) (I26):</p><p style='margin:0 0 10px 0; font-size: 21px; font-weight: bold; color: #64B5F6;'>{ilo_dose:.2f} <span style='font-size:13px; color:#ff8a80; font-weight:bold;'>mcg/dose</span></p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='margin:1px 0; font-size:14px; color:#888;'>• Frequency (K26):</p><p style='margin:0 0 2px 0; font-size: 18px; font-weight: bold; color: #F4511E;'>Q4H</p>", unsafe_allow_html=True)

    # 其餘大項暫留
    elif category == "5. Apnea": st.info("💡 呼吸暫停/咖啡因模組建構中...")
    elif category == "6. Seizure control": st.info("💡 抗癲癇藥物公式建構中...")
    elif category == "7. Sedation": st.info("💡 鎮靜止痛藥物模組建構中...")
    elif category == "8. Miscellaneous.GCSF": st.info("💡 GCSF 特殊藥物公式建構中...")
    elif category == "9. 胃腸類藥品/營養補充品/維他命/其它": st.info("💡 胃腸營養模組建構中...")

# --- 其餘分頁 Tab 暫留 ---
with tab2: st.info("⏳ Ion dosage 模組建構中...")
with tab3: st.info("⏳ DART.BURST 模組建構中...")
with tab4: st.info("⏳ PUMP 總表115 模組建構中...")
with tab5: st.info("⏳ Dexmedetomidine 模組建構中...")

# --- 底部專業版權宣告 ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: #888888; font-size: 12px; line-height: 1.6;'>
        🔒 <b>臨床決策支援系統 (CDSS) 免責宣告</b>：本工具計算結果僅供醫療專業人員參考核對，處方開立仍應以臨床實際病情與主治醫師之最終判斷為準。<br>
        <b>版權為中國醫藥大學附設醫院藥劑部 臨床藥學科 臨床服務組 張運佳藥師 所有</b>
    </div>
    """, 
    unsafe_allow_html=True
)
