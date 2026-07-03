import streamlit as st

# --- 網頁外觀設定 ---
st.set_page_config(
    page_title="NICU智慧計算機", 
    page_icon="👶", 
    layout="wide"  # 寬螢幕佈局
)

# --- APP 標題 ---
st.title("👶 NICU智慧計算機")
st.caption("🔒 兒科/新生兒加護病房專用 | 臨床決策支援系統 (CDSS)")
st.write("---")

# --- 側邊欄：統一輸入基本資料 (對應 Excel 儲存格位置) ---
st.sidebar.header("📥 病患基本資料輸入")

# B1: 體重
b1_bw = st.sidebar.number_input("BW 體重 (B1) (kg)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)

st.sidebar.write("---")
st.sidebar.markdown("**GA 胎齡 (F1 + H1)**")
# F1: GA週
f1_ga_wk = st.sidebar.number_input("GA 週數 (F1)", min_value=20, max_value=45, value=36, step=1)
# H1: GA天
h1_ga_day = st.sidebar.number_input("GA 天數 (H1)", min_value=0, max_value=6, value=0, step=1)

st.sidebar.write("---")
# L1: PNA出生天數
l1_pna = st.sidebar.number_input("PNA 出生天數 (L1) (days)", min_value=0, max_value=365, value=1, step=1)


# --- 後台邏輯計算：PMA 自動換算 (對應 Excel Q1, S1) ---
ga_total_days = (f1_ga_wk * 7) + h1_ga_day
pma_total_days = ga_total_days + l1_pna
q1_pma_wk = pma_total_days // 7
s1_pma_day = pma_total_days % 7


# --- 📌 側邊欄：常用藥物類別選單 (全展開點選清單) ---
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


# --- 頂部發育指標看板 ---
st.subheader("📊 當前病患生理指標核對")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="👶 病患體重 (BW)", value=f"{b1_bw:.2f} kg" if b1_bw > 0 else "未輸入")
with col2:
    st.metric(label="⏳ 胎齡 (GA)", value=f"{f1_ga_wk} 週 + {h1_ga_day} 天")
with col3:
    st.success(f"🧮 **PMA (受孕齡) [Q1+S1]**：\n### {q1_pma_wk} 週 + {s1_pma_day} 天")

st.write("---")


# --- 核心功能頁籤 ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💊 常用藥物計算機", 
    "⚡ Ion dosage", 
    "🫁 DART.BURST", 
    "🔌 PUMP 總表115", 
    "💤 Dexmedetomidine"
])


# =========================================================================
# TAB 1: 常用藥物計算機
# =========================================================================
with tab1:
    st.header(f"📂 當前分類：{category}")
    st.write("---")

    # -------------------------------------------------------------
    # 大項 1: Antimicrobial agents (每行顯示 3 種藥物，高度極致壓縮版)
    # -------------------------------------------------------------
    if category == "1. Antimicrobial agents":
        
        if b1_bw <= 0:
            st.warning("⚠️ 請先於左側欄位輸入大於 0 的「體重 (BW)」，系統將自動計算建議劑量。")
        else:
            
            # -------------------------------------------------------------
            # 【第 1 排藥物：Ampicillin / Cefotaxime / Gentamicin】
            # -------------------------------------------------------------
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            
            # 1. Ampicillin
            with r1_c1:
                with st.container(border=True):
                    st.markdown("### 🟥 **Ampicillin**")
                    
                    # Normal
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
                            amp_b4 = "超過28天(手動確認)"
                            norm_ok = False
                    
                    if norm_ok:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{amp_b4:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{amp_d4}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 16px; font-weight: bold; color: #D32F2F;'>❌ {amp_b4}</p>", unsafe_allow_html=True)
                    
                    # Meningitis
                    amp_b5 = b1_bw * 100 if l1_pna <= 7 else b1_bw * 75
                    amp_d5 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{amp_b5:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{amp_d5}</span></p>", unsafe_allow_html=True)
                    
                    # Surgical
                    amp_b6 = b1_bw * 50
                    amp_d6 = "60m prior"
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Surgical:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{amp_b6:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 16px; color: #F4511E; margin-left: 10px;'>{amp_d6}</span></p>", unsafe_allow_html=True)
            
            # 2. Cefotaxime
            with r1_c2:
                with st.container(border=True):
                    st.markdown("### 🟦 **Cefotaxime**")
                    
                    # Normal
                    if b1_bw <= 2:
                        ctx_b8 = b1_bw * 50 if l1_pna <= 28 else "超過28天(手動確認)"
                        ctx_b8_ok = False if l1_pna > 28 else True
                    else:
                        if l1_pna <= 7:
                            ctx_b8 = b1_bw * 50
                            ctx_b8_ok = True
                        elif l1_pna <= 28:
                            ctx_b8 = b1_bw * 37.5
                            ctx_b8_ok = True
                        else:
                            ctx_b8 = b1_bw * 50 if l1_pna <= 60 else "超過60天(手動確認)"
                            ctx_b8_ok = False if l1_pna > 60 else True
                            
                    if b1_bw <= 2:
                        ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else "確認醫囑")
                    else:
                        ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                        
                    if ctx_b8_ok:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{ctx_b8:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{ctx_d8}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 16px; font-weight: bold; color: #D32F2F;'>❌ {ctx_b8}</p>", unsafe_allow_html=True)
                    
                    # Meningitis
                    ctx_b9 = b1_bw * 50
                    ctx_d9 = "Q8H" if l1_pna <= 7 else "Q6H"
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{ctx_b9:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{ctx_d9}</span></p>", unsafe_allow_html=True)
                    
                    # 墊高排版對齊 Ampicillin 高度
                    st.markdown("<div style='height:62px;'></div>", unsafe_allow_html=True)
            
            # 3. Gentamicin
            with r1_c3:
                with st.container(border=True):
                    st.markdown("### 🟩 **Gentamicin**")
                    
                    # Normal
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
                            
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{gen_b11:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{gen_d11}</span></p>", unsafe_allow_html=True)
                    
                    # 墊高排版對齊 Ampicillin 高度
                    st.markdown("<div style='height:136px;'></div>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 2 排藥物：Cefazolin / Piperacillin+Tazobactam / Amoxicillin(IV)】
            # -------------------------------------------------------------
            r2_c1, r2_c2, r2_c3 = st.columns(3)
            
            # 4. Cefazolin
            with r2_c1:
                with st.container(border=True):
                    st.markdown("### 🟧 **Cefazolin**")
                    
                    # Normal
                    if l1_pna <= 28:
                        cfz_b13 = b1_bw * 25 if b1_bw <= 2 else b1_bw * 50
                        cfz_b13_ok = True
                    else:
                        cfz_b13 = b1_bw * 150 / 4 if l1_pna <= 60 else "超過60天(手動確認)"
                        cfz_b13_ok = False if l1_pna > 60 else True
                    cfz_d13 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                    
                    if cfz_b13_ok:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{cfz_b13:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{cfz_d13}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 16px; font-weight: bold; color: #D32F2F;'>❌ {cfz_b13}</p>", unsafe_allow_html=True)
                    
                    # Perioperative
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Perioperative:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 15px; color: #F4511E; margin-left: 10px;'>30-60m prior</span></p>", unsafe_allow_html=True)
                    
                    # Postoperative
                    cfz_d15 = "Q12H" if l1_pna <= 7 else "Q8H"
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Postoperative:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{b1_bw * 30:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{cfz_d15}</span></p>", unsafe_allow_html=True)
            
            # 5. Piperacillin + Tazobactam
            with r2_c2:
                with st.container(border=True):
                    st.markdown("### 🟪 **Pip/Tazo (0.25g)**")
                    
                    # Normal
                    if b1_bw <= 2:
                        pt_b17 = b1_bw * 112.5 if l1_pna <= 7 else (b1_bw * 112.5 if q1_pma_wk <= 30 else b1_bw * 90)
                        pt_d17 = "Q8H" if l1_pna <= 7 else ("Q8H" if q1_pma_wk <= 30 else "Q6H")
                    else:
                        pt_b17 = b1_bw * 90
                        pt_d17 = "Q6H"
                        
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{pt_b17:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{pt_d17}</span></p>", unsafe_allow_html=True)
                    
                    # 墊高排版對齊 Cefazolin 高度
                    st.markdown("<div style='height:136px;'></div>", unsafe_allow_html=True)
            
            # 6. Amoxicillin + Clavulanate (IV)
            with r2_c3:
                with st.container(border=True):
                    st.markdown("### 🟫 **Amoxicillin (IV)**")
                    
                    # Normal
                    amx_iv_b19 = min(1200.0, b1_bw * 30)
                    amx_iv_d19 = "Q8H" if (ga_total_days >= 90 and l1_pna >= 4) else "Q12H"
                    
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{amx_iv_b19:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{amx_iv_d19}</span></p>", unsafe_allow_html=True)
                    
                    # 墊高排版對齊 Cefazolin 高度
                    st.markdown("<div style='height:136px;'></div>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 3 排藥物：Amoxicillin(PO) / Meropenem / Vancomycin】
            # -------------------------------------------------------------
            r3_c1, r3_c2, r3_c3 = st.columns(3)
            
            # 7. Amoxicillin (PO) 水劑
            with r3_c1:
                with st.container(border=True):
                    st.markdown("### 🧪 **Amoxicillin (PO)**")
                    st.caption("液粉(複方) 50+12.5 mg/ml")
                    
                    # Normal
                    amx_po_b21 = b1_bw * 0.3
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{amx_po_b21:.2f} <span style='font-size:14px;'>mL/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>Q12H</span></p>", unsafe_allow_html=True)
                    
                    # 墊高排版對齊 Meropenem 高度
                    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
            
            # 8. Meropenem
            with r3_c2:
                with st.container(border=True):
                    st.markdown("### 🛸 **Meropenem**")
                    
                    # Normal
                    mrp_b23 = b1_bw * 20 if ga_total_days <= 223 else (b1_bw * 20 if l1_pna < 14 else b1_bw * 30)
                    mrp_d23 = "Q12H" if (ga_total_days <= 223 and l1_pna < 14) else "Q8H"
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Normal dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{mrp_b23:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{mrp_d23}</span></p>", unsafe_allow_html=True)
                    
                    # Meningitis
                    mrp_b24_ok = True
                    if l1_pna <= 60:
                        mrp_b24 = b1_bw * 40
                    else:
                        mrp_b24 = "超過60天(手動確認)"
                        mrp_b24_ok = False
                    mrp_d24 = ("Q12H" if l1_pna < 14 else "Q8H") if b1_bw <= 2 else "Q8H"
                    
                    if mrp_b24_ok:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{mrp_b24:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{mrp_d24}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 2px 0px; font-size: 16px; font-weight: bold; color: #D32F2F;'>❌ {mrp_b24}</p>", unsafe_allow_html=True)
            
            # 9. Vancomycin (Initial)
            with r3_c3:
                with st.container(border=True):
                    st.markdown("### 🥊 **Vancomycin**")
                    
                    # Initial
                    vnc_b26 = b1_bw * 15
                    vnc_d26 = "Q24H" if (ga_total_days + l1_pna) < 203 else ("Q12H" if (ga_total_days + l1_pna) < 252 else "Q8H")
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Initial dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{vnc_b26:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{vnc_d26}</span></p>", unsafe_allow_html=True)
                    
                    # Meningitis
                    if b1_bw < 2:
                        vnc_b27 = "體重<2kg(手動確認)"
                        vnc_b27_ok = False
                    else:
                        vnc_b27 = b1_bw * 10 if l1_pna <= 7 else b1_bw * 11.25
                        vnc_d27 = "Q8H" if l1_pna <= 7 else "Q6H"
                        vnc_b27_ok = True
                        
                    if vnc_b27_ok:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{vnc_b27:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>{vnc_d27}</span></p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Meningitis:</p><p style='margin:0px 0px 2px 0px; font-size: 16px; font-weight: bold; color: #D32F2F;'>❌ {vnc_b27}</p>", unsafe_allow_html=True)

            # -------------------------------------------------------------
            # 【第 4 排藥物：Teicoplanin / Fluconazole / 剩餘空間】
            # -------------------------------------------------------------
            r4_c1, r4_c2, r4_c3 = st.columns(3)
            
            # 10. Teicoplanin
            with r4_c1:
                with st.container(border=True):
                    st.markdown("### 🛡️ **Teicoplanin**")
                    
                    # Loading
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Loading dose:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{16 * b1_bw:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>Day 1</span></p>", unsafe_allow_html=True)
                    
                    # Maintenance
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Maintenance:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{8 * b1_bw:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>QD</span></p>", unsafe_allow_html=True)
            
            # 11. Fluconazole
            with r4_c2:
                with st.container(border=True):
                    st.markdown("### 🍄 **Fluconazole**")
                    
                    # Prophylaxis
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Prophylaxis:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{3 * b1_bw:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 17px; color: #F4511E; margin-left: 10px;'>Q3D/QOD</span></p>", unsafe_allow_html=True)
                    
                    # Treatment D1
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Treatment D1:</p><p style='margin:0px 0px 8px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{25 * b1_bw:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>QD</span></p>", unsafe_allow_html=True)
                    
                    # Treatment D2~
                    st.markdown(f"<p style='margin:2px 0px; font-size:15px; color:#888;'>• Treatment D2~:</p><p style='margin:0px 0px 2px 0px; font-size: 23px; font-weight: bold; color: #1E88E5;'>{12 * b1_bw:.1f} <span style='font-size:14px;'>mg/d</span> <span style='font-size: 18px; color: #F4511E; margin-left: 10px;'>QD</span></p>", unsafe_allow_html=True)

            with r4_c3:
                st.write("")

    # -------------------------------------------------------------
    # 大項 2 ~ 9 預留區塊
    # -------------------------------------------------------------
    elif category == "2. Diuretics":
        st.info("💡 這裡即將放入 Diuretics (利尿劑) 類藥物公式。")
    elif category == "3. PDA":
        st.info("💡 這裡即將放入 PDA 治療藥物公式。")
    elif category == "4. 肺高壓":
        st.info("💡 這裡即將放入 肺高壓 相關藥物公式。")
    elif category == "5. Apnea":
        st.info("💡 這裡即將放入 Apnea 藥物公式。")
    elif category == "6. Seizure control":
        st.info("💡 這裡即將放入 Seizure control 公式。")
    elif category == "7. Sedation":
        st.info("💡 這裡即將放入 Sedation 公式。")
    elif category == "8. Miscellaneous.GCSF":
        st.info("💡 這裡即將放入 GCSF 等其它各類特殊藥物公式。")
    elif category == "9. 胃腸類藥品/營養補充品/維他命/其它":
        st.info("💡 這裡即將放入 胃腸類藥品、營養補充品、維他命與其它藥品公式。")


# =========================================================================
# 其餘大 Tab 分頁暫時保留
# =========================================================================
with tab2:
    st.info("⏳ Ion dosage 模組建構中...")
with tab3:
    st.info("⏳ DART.BURST 模組建構中...")
with tab4:
    st.info("⏳ PUMP 總表115 模組建構中...")
with tab5:
    st.info("⏳ Dexmedetomidine 模組建構中...")


# --- 底部專業版權宣告與免責聲明 ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: #888888; font-size: 13px; line-height: 1.8;'>
        🔒 <b>臨床決策支援系統 (CDSS) 免責宣告</b>：本工具計算結果僅供醫療專業人員參考核對，處方開立仍應以臨床實際病情與主治醫師之最終判斷為準。<br>
        © 2026 版權所有．智慧財產保護中<br>
        <b>版權為中國醫藥大學附設醫院藥劑部 臨床藥學科 臨床服務組 張運佳藥師 所有</b>
    </div>
    """, 
    unsafe_allow_html=True
)
