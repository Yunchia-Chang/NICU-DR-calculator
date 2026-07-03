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
        /* 緊湊網頁頂部間距 */
        .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
        /* 縮減所有標題與文字的上下 margin 間距 */
        h2, h3, h4 {margin-top: 0px !important; margin-bottom: 4px !important; padding-top: 0px !important;}
        div[data-testid="stForm"] {padding: 5px;}
        hr {margin-top: 5px !important; margin-bottom: 8px !important;}
        /* 側邊欄間距精簡 */
        section[data-testid="stSidebar"] .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# 頂部標題列極致精簡並行化
col_title, col_sub = st.columns([2, 3])
with col_title:
    st.markdown("<h2 style='font-size:24px; margin:0;'>👶 NICU智慧計算機</h2>", unsafe_allow_html=True)
with col_sub:
    st.markdown("<p style='margin:6px 0 0 0; color:#888; font-size:13px;'>🔒 兒科/新生兒加護病房專用 | 臨床決策支援系統 (CDSS)</p>", unsafe_allow_html=True)

st.write("---")

# --- 側邊欄：基本資料輸入 (預設全部歸 0，防呆不預載) ---
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

# 側邊欄：全展開點選清單
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

# --- 📊 當前病患生理指標核對 (超級精簡一行式排版，對齊 image_cefbdf.png 的優化) ---
# 判斷是否已輸入必要的基本資料
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
    if category == "1. Antimicrobial agents":
        # 如果未輸入基本資料，下方處方箋區塊保持空白防錯
        if not has_input:
            st.info("💡 正在等待左側輸入病患基本資料...")
        else:
            # -------------------------------------------------------------
            # 【第 1 排藥物：Ampicillin / Cefotaxime / Gentamicin】
            # -------------------------------------------------------------
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            
            with r1_c1:
                with st.container(border=True):
                    st.markdown("### 🟥 **Ampicillin**")
                    
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
                            amp_ok = False
                    
                    if norm_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b4:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d4}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {amp_b4}</p>", unsafe_allow_html=True)
                    
                    amp_b5 = b1_bw * 100 if l1_pna <= 7 else b1_bw * 75
                    amp_d5 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b5:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amp_d5}</span></p>", unsafe_allow_html=True)
                    
                    amp_b6 = b1_bw * 50
                    amp_d6 = "60 mins prior"
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Surgical prophylaxis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amp_b6:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>{amp_d6}</span></p>", unsafe_allow_html=True)
            
            with r1_c2:
                with st.container(border=True):
                    st.markdown("### 🟦 **Cefotaxime**")
                    
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
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b8:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d8}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {ctx_b8}</p>", unsafe_allow_html=True)
                    
                    ctx_b9 = b1_bw * 50
                    ctx_d9 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{ctx_b9:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{ctx_d9}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
            
            with r1_c3:
                with st.container(border=True):
                    st.markdown("### 🟩 **Gentamicin**")
                    
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
                            
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{gen_b11:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{gen_d11}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 2 排藥物：Cefazolin / Piperacillin... / Amoxicillin(IV)】
            # -------------------------------------------------------------
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r2_c1, r2_c2, r2_c3 = st.columns(3)
            
            with r2_c1:
                with st.container(border=True):
                    st.markdown("### 🟧 **Cefazolin**")
                    
                    if l1_pna <= 28:
                        cfz_b13 = b1_bw * 25 if b1_bw <= 2 else b1_bw * 50
                        cfz_b13_ok = True
                    else:
                        cfz_b13 = b1_bw * 150 / 4 if l1_pna <= 60 else "超過60天(請手動確認)"
                        cfz_b13_ok = False if l1_pna > 60 else True
                    cfz_d13 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    
                    if cfz_b13_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{cfz_b13:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d13}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {cfz_b13}</p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Perioperative dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 14px; color: #F4511E; margin-left: 8px;'>30-60 mins prior</span></p>", unsafe_allow_html=True)
                    
                    cfz_d15 = "Q12H" if l1_pna <= 7 else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Postoperative dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{cfz_d15}</span></p>", unsafe_allow_html=True)
            
            with r2_c2:
                with st.container(border=True):
                    # 💡 已修正：完整名稱對齊 image_cefc07.png
                    st.markdown("### 🟪 **Piperacillin 2g + Tazobactam 0.25g**")
                    
                    if b1_bw <= 2:
                        pt_b17 = b1_bw * 112.5 if l1_pna <= 7 else (b1_bw * 112.5 if q1_pma_wk <= 30 else b1_bw * 90)
                        pt_d17 = "Q8H" if l1_pna <= 7 else ("Q8H" if q1_pma_wk <= 30 else "Q6H")
                    else:
                        pt_b17 = b1_bw * 90
                        pt_d17 = "Q6H"
                        
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{pt_b17:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{pt_d17}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)
            
            with r2_c3:
                with st.container(border=True):
                    # 💡 已修正：完整名稱對齊 image_cefc07.png
                    st.markdown("### 🟫 **Amoxicillin 1g + Clavulanate 0.2g 5:1(IV)**")
                    
                    amx_iv_b19 = min(1200.0, b1_bw * 30)
                    amx_iv_d19 = "Q8H" if (ga_total_days >= 90 and l1_pna >= 4) else "Q12H"
                    
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_iv_b19:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{amx_iv_d19}</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:114px;'></div>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 3 排藥物：Amoxicillin(PO) / Meropenem / Vancomycin】
            # -------------------------------------------------------------
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r3_c1, r3_c2, r3_c3 = st.columns(3)
            
            with r3_c1:
                with st.container(border=True):
                    # 💡 已修正：完整名稱對齊 image_cefeb0.png
                    st.markdown("### 🧪 **液粉(複方)(4:1)Amoxicillin 50 mg + Clavulanic acid 12.5 mg/mL : PO**")
                    
                    amx_po_b21 = b1_bw * 0.3
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{amx_po_b21:.2f} <span style='font-size:12px; color:#fff;'>mL/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Q12H</span></p>", unsafe_allow_html=True)
                    st.markdown("<div style='height:94px;'></div>", unsafe_allow_html=True)
            
            with r3_c2:
                with st.container(border=True):
                    st.markdown("### 🛸 **Meropenem**")
                    
                    mrp_b23 = b1_bw * 20 if ga_total_days <= 223 else (b1_bw * 20 if l1_pna < 14 else b1_bw * 30)
                    mrp_d23 = "Q12H" if (ga_total_days <= 223 and l1_pna < 14) else "Q8H"
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Normal dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b23:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d23}</span></p>", unsafe_allow_html=True)
                    
                    mrp_b24_ok = True
                    if l1_pna <= 60:
                        mrp_b24 = b1_bw * 40
                    else:
                        mrp_b24 = "超過60天(請手動確認)"
                        mrp_b24_ok = False
                    mrp_d24 = ("Q12H" if l1_pna < 14 else "Q8H") if b1_bw <= 2 else "Q8H"
                    
                    if mrp_b24_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{mrp_b24:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{mrp_d24}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {mrp_b24}</p>", unsafe_allow_html=True)
            
            with r3_c3:
                with st.container(border=True):
                    st.markdown("### 🥊 **Vancomycin (Initial)**")
                    
                    vnc_b26 = b1_bw * 15
                    vnc_d26 = "Q24H" if (ga_total_days + l1_pna) < 203 else ("Q12H" if (ga_total_days + l1_pna) < 252 else "Q8H")
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Initial dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b26:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d26}</span></p>", unsafe_allow_html=True)
                    
                    if b1_bw < 2:
                        vnc_b27 = "體重<2kg(請手動確認)"
                        vnc_b27_ok = False
                    else:
                        vnc_b27 = b1_bw * 10 if l1_pna <= 7 else b1_bw * 11.25
                        vnc_d27 = "Q8H" if l1_pna <= 7 else "Q6H"
                        vnc_b27_ok = True
                        
                    if vnc_b27_ok:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{vnc_b27:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>{vnc_d27}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Meningitis dose:</p><p style='margin:0 0 2px 0; font-size: 14px; font-weight: bold; color: #D32F2F;'>❌ {vnc_b27}</p>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 4 排藥物：Teicoplanin / Fluconazole】
            # -------------------------------------------------------------
            st.write("<div style='height:4px;'></div>", unsafe_allow_html=True)
            r4_c1, r4_c2, r4_c3 = st.columns(3)
            
            with r4_c1:
                with st.container(border=True):
                    st.markdown("### 🛡️ **Teicoplanin**")
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Loading dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{16 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>Day 1</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Maintenance dose:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{8 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)
            
            with r4_c2:
                with st.container(border=True):
                    st.markdown("### 🍄 **Fluconazole**")
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Prophylaxis dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{3 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 15px; color: #F4511E; margin-left: 8px;'>Q3D/QOD</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Treatment DAY 1 dose:</p><p style='margin:0 0 6px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{25 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:1px 0; font-size:13px; color:#888;'>• Treatment DAY2~ frequency:</p><p style='margin:0 0 2px 0; font-size: 20px; font-weight: bold; color: #1E88E5;'>{12 * b1_bw:.1f} <span style='font-size:12px; color:#fff;'>mg/dose</span> <span style='font-size: 16px; color: #F4511E; margin-left: 8px;'>QD</span></p>", unsafe_allow_html=True)

            with r4_c3:
                st.write("")

    # 其餘大項暫留
    elif category == "2. Diuretics": st.info("💡 利尿劑模組建構中...")
    elif category == "3. PDA": st.info("💡 PDA 治療藥物公式建構中...")
    elif category == "4. 肺高壓": st.info("💡 肺高壓藥物公式建構中...")
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
