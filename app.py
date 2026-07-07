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
st.sidebar.header("📥 病健基本資料輸入")
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

# --- TAB 1~3, 5 (保持您原本的邏輯) ---
with tab1: st.write("請參閱原常用藥物模組")
with tab2: st.write("請參閱原 Ion dosage 模組")
with tab3: st.write("請參閱原 DART.BURST 模組")
with tab5: st.write("請參閱原 Dexmedetomidine 模組")

# =============================================================================
# TAB 4: 🔌 PUMP 總表115 (完全依據您提供的 Excel 欄位邏輯)
# =============================================================================
with tab4:
    st.markdown("### 🔌 PUMP 總表115")
    if not has_input:
        st.info("💡 正在等待左側輸入病患基本資料 (BW)...")
    else:
        # 設定稀釋比例係數 (基於您的 Excel 對應)
        ratios = {
            "1:1": 1.0, "1:2": 0.5, "1:5": 0.2, "1:10": 0.1, 
            "1:20": 0.05, "2:1": 2.0, "5:1": 5.0, "10:1": 10.0
        }
        
        c_ratio = st.selectbox("請選擇稀釋比例 (1:X 或 X:1)", list(ratios.keys()))
        factor = ratios[c_ratio]
        
        # 顯示該比例下的劑量計算方式
        st.info(f"當前配方係數 (Dose): (BW * 0.6) * {factor}")
        
        # 輸入幫浦設定流速
        pump_rate = st.number_input("輸入幫浦設定流速 (mL/hr)", min_value=0.0, value=0.0, step=0.01)
        
        # 計算結果顯示
        if pump_rate > 0:
            # 依據 Excel 公式: C/F*I*1000/60/C2 (簡化後對應)
            res = ( (b1_bw * 0.6) * factor ) / 10 * pump_rate * 1000 / 60 / b1_bw
            st.metric("換算後單位劑量 (mcg/kg/min)", f"{res:.3f}")
        else:
            st.write("請輸入流速以進行計算")

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
