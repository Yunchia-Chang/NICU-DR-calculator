import streamlit as st

# --- 網頁外觀設定 ---
st.set_page_config(
    page_title="NICU智慧計算機", 
    page_icon="👶", 
    layout="wide"  # 寬螢幕佈局
)

# --- APP 標題與簡介 (精簡一行化) ---
title_col, cap_col = st.columns([1, 2])
with title_col:
    st.markdown("<h2 style='margin:0px;'>👶 NICU智慧計算機</h2>", unsafe_allow_html=True)
with cap_col:
    st.markdown("<p style='margin-top:10px; color:#888;'>🔒 兒科/新生兒加護病房專用 | 臨床決策支援系統 (CDSS)</p>", unsafe_allow_html=True)
st.write("---")

# --- 側邊欄：統一輸入基本資料 (對應 Excel 儲存格位置) ---
st.sidebar.header("📥 📊 病患基本資料")

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


# --- 後台邏輯計算：PMA 自動換算 ---
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


# --- 頂部發育指標看板 (極度精簡高度) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="👶 病患體重 (BW)", value=f"{b1_bw:.2f} kg" if b1_bw > 0 else "未輸入")
with col2:
    st.metric(label="⏳ 胎齡 (GA)", value=f"{f1_ga_wk} 週 + {h1_ga_day} 天")
with col3:
    st.success(f"🧮 **PMA (受孕齡) [Q1+S1]**：{q1_pma_wk} 週 + {s1_pma_day} 天")

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
    st.markdown(f"### 📂 當前分類：{category}")
    
    if category == "1. Antimicrobial agents":
        if b1_bw <= 0:
            st.warning("⚠️ 請先於左側欄位輸入大於 0 的「體重 (BW)」，系統將自動計算建議劑量。")
        else:
            
            # =========================================================================
            # 【第 1 大區：Ampicillin & Cefotaxime】(2大柱並排，內部橫向拆分療程)
            # =========================================================================
            top_col1, top_col2 = st.columns([1, 1])
            
            # 1. Ampicillin
            with top_col1:
                with st.container(border=True):
                    st.markdown("<h3 style='margin:0px; color:#E53935;'>🟥 Ampicillin</h3>", unsafe_allow_html=True)
                    st.write("---")
                    
                    # 內部療程橫向並排
                    amp_c1, amp_c2, amp_c3 = st.columns(3)
                    
                    with amp_c1:
                        st.markdown("**1. Normal**")
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
                                amp_b4 = "超過28天"
                                amp_d4 = "Q8H"
                                norm_ok = False
                        if norm_ok:
                            st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #1E88E5; margin:0px;'>{amp_b4:.1f} <span style='font-size:13px;'>mg/d</span></p><p style='font-size: 15px; color: #F4511E; font-weight:bold; margin:0px;'>{amp_d4}</p>", unsafe_allow_html=True)
                        else:
                            st.caption(f"❌ {amp_b4}")
                            
                    with amp_c2:
                        st.markdown("**2. Meningitis**")
                        amp_b5 = b1_bw * 100 if l1_pna <= 7 else b1_bw * 75
                        amp_d5 = "Q8H" if l1_pna <= 7 else "Q6H"
                        st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #1E88E5; margin:0px;'>{amp_b5:.1f} <span style='font-size:13px;'>mg/d</span></p><p style='font-size: 15px; color: #F4511E; font-weight:bold; margin:0px;'>{amp_d5}</p>", unsafe_allow_html=True)
                        
                    with amp_c3:
                        st.markdown("**3. Surgical**")
                        amp_b6 = b1_bw * 50
                        amp_d6 = "60m prior"
                        st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #1E88E5; margin:0px;'>{amp_b6:.1f} <span style='font-size:13px;'>mg/d</span></p><p style='font-size: 14px; color: #F4511E; font-weight:bold; margin:0px;'>{amp_d6}</p>", unsafe_allow_html=True)
            
            # 2. Cefotaxime
            with top_col2:
                with st.container(border=True):
                    st.markdown("<h3 style='margin:0px; color:#1E88E5;'>🟦 Cefotaxime</h3>", unsafe_allow_html=True)
                    st.write("---")
                    
                    ctx_c1, ctx_c2 = st.columns(2)
                    with ctx_c1:
                        st.markdown("**1. Normal**")
                        if b1_bw <= 2:
                            ctx_b8 = b1_bw * 50 if l1_pna <= 28 else "超過28天"
                            ctx_b8_ok = False if l1_pna > 28 else True
                            ctx_d8 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else "確認醫囑")
                        else:
                            if l1_pna <= 7:
                                ctx_b8 = b1_bw * 50
                                ctx_b8_ok = True
                                ctx_d8 = "Q12H"
                            elif l1_pna <= 28:
                                ctx_b8 = b1_bw * 37.5
                                ctx_b8_ok = True
                                ctx_d8 = "Q8H"
                            else:
                                ctx_b8 = b1_bw * 50 if l1_pna <= 60 else "超過60天"
                                ctx_b8_ok = False if l1_pna > 60 else True
                                ctx_d8 = "Q6H" if l1_pna <= 60 else "確認醫囑"
                        if ctx_b8_ok:
                            st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #1E88E5; margin:0px;'>{ctx_b8:.1f} <span style='font-size:13px;'>mg/d</span></p><p style='font-size: 15px; color: #F4511E; font-weight:bold; margin:0px;'>{ctx_d8}</p>", unsafe_allow_html=True)
                        else:
                            st.caption(f"❌ {ctx_b8}")
                            
                    with ctx_c2:
                        st.markdown("**2. Meningitis**")
                        ctx_b9 = b1_bw * 50
                        ctx_d9 = "Q8H" if l1_pna <= 7 else "Q6H"
                        st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #1E88E5; margin:0px;'>{ctx_b9:.1f} <span style='font-size:13px;'>mg/d</span></p><p style='font-size: 15px; color: #F4511E; font-weight:bold; margin:0px;'>{ctx_d9}</p>", unsafe_allow_html=True)

            # =========================================================================
            # 【第 2 大區：常規單療程藥物並排】(每行顯示 4 種藥物，大幅節省空間)
            # =========================================================================
            st.write("---")
            grid1_c1, grid1_c2, grid1_c3, grid1_c4 = st.columns(4)
            
            # 3. Gentamicin
            with grid1_c1:
                with st.container(border=True):
                    st.markdown("<b style='color:#2E7D32;'>🟩 Gentamicin</b>", unsafe_allow_html=True)
                    if ga_total_days <= 209:
                        gen_b11 = b1_bw * 5
                        gen_d11 = "Q36H" if l1_pna <= 14 else "Q24H"
                    else:
                        gen_b11 = b1_bw * 4 if l1_pna <= 7 else b1_bw * 5
                        if ga_total_days <= 244:
                            gen_d11 = "Q36H" if l1_pna <= 10 else "QD"
                        else:
                            gen_d11 = "QD"
                    st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #1E88E5; margin:0px;'>{gen_b11:.1f} <span style='font-size:12px;'>mg/d</span></p><p style='font-size: 14px; color: #F4511E; margin:0px; font-weight:bold;'>{gen_d11}</p>", unsafe_allow_html=True)

            # 5. Piperacillin + Tazobactam
            with grid1_c2:
                with st.container(border=True):
                    st.markdown("<b style='color:#6A1B9A;'>🟪 Pip/Tazo (0.25g)</b>", unsafe_allow_html=True)
                    if b1_bw <= 2:
                        pt_b17 = b1_bw * 112.5 if l1_pna <= 7 else (b1_bw * 112.5 if q1_pma_wk <= 30 else b1_bw * 90)
                        pt_d17 = "Q8H" if l1_pna <= 7 else ("Q8H" if q1_pma_wk <= 30 else "Q6H")
                    else:
                        pt_b17 = b1_bw * 90
                        pt_d17 = "Q6H"
                    st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #1E88E5; margin:0px;'>{pt_b17:.1f} <span style='font-size:12px;'>mg/d</span></p><p style='font-size: 14px; color: #F4511E; margin:0px; font-weight:bold;'>{pt_d17}</p>", unsafe_allow_html=True)

            # 6. Amoxicillin + Clavulanate (IV)
            with grid1_c3:
                with st.container(border=True):
                    st.markdown("<b style='color:#4E342E;'>🟫 Amoxicillin (IV)</b>", unsafe_allow_html=True)
                    amx_iv_b19 = min(1200.0, b1_bw * 30)
                    amx_iv_d19 = "Q8H" if (ga_total_days >= 90 and l1_pna >= 4) else "Q12H"
                    st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #1E88E5; margin:0px;'>{amx_iv_b19:.1f} <span style='font-size:12px;'>mg/d</span></p><p style='font-size: 14px; color: #F4511E; margin:0px; font-weight:bold;'>{amx_iv_d19}</p>", unsafe_allow_html=True)

            # 7. Amoxicillin (PO) 水劑
            with grid1_c4:
                with st.container(border=True):
                    st.markdown("<b style='color:#00838F;'>🧪 Amoxicillin (PO)</b>", unsafe_allow_html=True)
                    amx_po_b21 = b1_bw * 0.3
                    st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #1E88E5; margin:0px;'>{amx_po_b21:.2f} <span style='font-size:12px;'>mL/d</span></p><p style='font-size: 14px; color: #F4511E; margin:0px; font-weight:bold;'>Q12H</p>", unsafe_allow_html=True)

            # =========================================================================
            # 【第 3 大區：多療程複雜抗生素（Cefazolin & Meropenem & Vancomycin）】
            # =========================================================================
            grid2_c1, grid2_c2, grid2_c3 = st.columns([4, 4, 4])
            
            # 4. Cefazolin
            with grid2_c1:
                with st.container(border=True):
                    st.markdown("<b style='color:#EF6C00;'>🟧 Cefazolin</b>", unsafe_allow_html=True)
                    st.write("---")
                    cfz1, cfz2, cfz3 = st.columns(3)
                    with cfz1:
                        st.caption("Normal")
                        if l1_pna <= 28:
                            cfz_b13 = b1_bw * 25 if b1_bw <= 2 else b1_bw * 50
                            cfz_b13_ok = True
                        else:
                            cfz_b13 = b1_bw * 150 / 4 if l1_pna <= 60 else "超過60天"
                            cfz_b13_ok = False if l1_pna > 60 else True
                        cfz_d13 = "Q12H" if l1_pna <= 7 else ("Q8H" if l1_pna <= 28 else ("Q6H" if l1_pna <= 60 else "確認醫囑"))
                        if cfz_b13_ok:
                            st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{cfz_b13:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{cfz_d13}</span>", unsafe_allow_html=True)
                        else:
                            st.caption(cfz_b13)
                    with cfz2:
                        st.caption("Periop")
                        st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{b1_bw * 30:.1f}</span><br><span style='font-size:11px; color:#F4511E;'>60m prior</span>", unsafe_allow_html=True)
                    with cfz3:
                        st.caption("Postop")
                        cfz_d15 = "Q12H" if l1_pna <= 7 else "Q8H"
                        st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{b1_bw * 30:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{cfz_d15}</span>", unsafe_allow_html=True)

            # 8. Meropenem
            with grid2_c2:
                with st.container(border=True):
                    st.markdown("<b style='color:#558B2F;'>🛸 Meropenem</b>", unsafe_allow_html=True)
                    st.write("---")
                    mrp1, mrp2 = st.columns(2)
                    with mrp1:
                        st.caption("Normal")
                        mrp_b23 = b1_bw * 20 if ga_total_days <= 223 else (b1_bw * 20 if l1_pna < 14 else b1_bw * 30)
                        mrp_d23 = "Q12H" if (ga_total_days <= 223 and l1_pna < 14) else "Q8H"
                        st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{mrp_b23:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{mrp_d23}</span>", unsafe_allow_html=True)
                    with mrp2:
                        st.caption("Meningitis")
                        mrp_b24 = b1_bw * 40 if l1_pna <= 60 else "超過60天"
                        if b1_bw <= 2:
                            mrp_d24 = "Q12H" if l1_pna < 14 else ("Q8H" if l1_pna <= 60 else "確認醫囑")
                        else:
                            mrp_d24 = "Q8H" if l1_pna <= 60 else "確認醫囑"
                        if l1_pna <= 60:
                            st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{mrp_b24:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{mrp_d24}</span>", unsafe_allow_html=True)
                        else:
                            st.caption(mrp_b24)

            # 9. Vancomycin
            with grid2_c3:
                with st.container(border=True):
                    st.markdown("<b style='color:#C62828;'>🥊 Vancomycin</b>", unsafe_allow_html=True)
                    st.write("---")
                    vnc1, vnc2 = st.columns(2)
                    with vnc1:
                        st.caption("Initial")
                        vnc_b26 = b1_bw * 15
                        vnc_d26 = "Q24H" if (ga_total_days + l1_pna) < 203 else ("Q12H" if (ga_total_days + l1_pna) < 252 else "Q8H")
                        st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{vnc_b26:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{vnc_d26}</span>", unsafe_allow_html=True)
                    with vnc2:
                        st.caption("Meningitis")
                        if b1_bw < 2:
                            st.caption("體重<2kg")
                        else:
                            vnc_b27 = b1_bw * 10 if l1_pna <= 7 else b1_bw * 11.25
                            vnc_d27 = "Q8H" if l1_pna <= 7 else "Q6H"
                            st.markdown(f"<span style='font-size:15px; font-weight:bold; color:#1E88E5;'>{vnc_b27:.1f}</span><br><span style='font-size:12px; color:#F4511E;'>{vnc_d27}</span>", unsafe_allow_html=True)

            # =========================================================================
            # 【第 4 大區：雙療程精簡藥物（Teicoplanin & Fluconazole）】
            # =========================================================================
            grid3_c1, grid3_c2 = st.columns([1, 1])
            
            # 10. Teicoplanin
            with grid3_c1:
                with st.container(border=True):
                    st.markdown("<b style='color:#37474F;'>🛡️ Teicoplanin</b>", unsafe_allow_html=True)
                    tei1, tei2 = st.columns(2)
                    with tei1:
                        st.markdown(f"<span style='font-size:13px; color:#555;'>Loading:</span> <b style='color:#1E88E5;'>{16*b1_bw:.1f}</b> <span style='font-size:12px; color:#F4511E; font-weight:bold;'>Day1</span>", unsafe_allow_html=True)
                    with tei2:
                        st.markdown(f"<span style='font-size:13px; color:#555;'>Maint:</span> <b style='color:#1E88E5;'>{8*b1_bw:.1f}</b> <span style='font-size:12px; color:#F4511E; font-weight:bold;'>QD</span>", unsafe_allow_html=True)

            # 11. Fluconazole
            with grid3_c2:
                with st.container(border=True):
                    st.markdown("<b style='color:#AD1457;'>🍄 Fluconazole</b>", unsafe_allow_html=True)
                    flu1, flu2, flu3 = st.columns(3)
                    with flu1:
                        st.markdown(f"<span style='font-size:12px; color:#555;'>Prophy:</span> <b style='color:#1E88E5;'>{3*b1_bw:.1f}</b> <span style='font-size:11px; color:#F4511E; font-weight:bold;'>Q3D/QOD</span>", unsafe_allow_html=True)
                    with flu2:
                        st.markdown(f"<span style='font-size:12px; color:#555;'>Day1:</span> <b style='color:#1E88E5;'>{25*b1_bw:.1f}</b> <span style='font-size:11px; color:#F4511E; font-weight:bold;'>QD</span>", unsafe_allow_html=True)
                    with flu3:
                        st.markdown(f"<span style='font-size:12px; color:#555;'>Day2~:</span> <b style='color:#1E88E5;'>{12*b1_bw:.1f}</b> <span style='font-size:11px; color:#F4511E; font-weight:bold;'>QD</span>", unsafe_allow_html=True)

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

# 其餘大 Tab 暫留
with tab2: st.info("⏳ Ion dosage 模組建構中...")
with tab3: st.info("⏳ DART.BURST 模組建構中...")
with tab4: st.info("⏳ PUMP 總表115 模組建構中...")
with tab5: st.info("⏳ Dexmedetomidine 模組建構中...")

# --- 底部專業版權宣告與免責聲明 ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: #888888; font-size: 11px; line-height: 1.5;'>
        🔒 <b>CDSS 免責宣告</b>：計算結果僅供醫療專業人員核對參考，處方仍應以臨床實際病情與醫師最終判斷為準。<br>
        <b>版權為中國醫藥大學附設醫院藥劑部 臨床藥學科 臨床服務組 張運佳藥師 所有</b>
    </div>
    """, 
    unsafe_allow_html=True
)
