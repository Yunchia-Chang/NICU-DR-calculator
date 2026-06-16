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

# --- 側邊欄：統一輸入基本資料 (對應您的 Excel 儲存格位置) ---
st.sidebar.header("📥 病患基本資料輸入")

# B1: 體重
st.sidebar.markdown("**BW 體重 (B1)**")
b1_bw = st.sidebar.number_input("請輸入體重 (kg)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)

st.sidebar.write("---")
st.sidebar.markdown("**GA 胎齡 (F1 + H1)**")
# F1: GA週 (預設改為 36 週，避免小於 min_value 報錯)
f1_ga_wk = st.sidebar.number_input("GA 週數 (F1)", min_value=20, max_value=45, value=36, step=1)
# H1: GA天
h1_ga_day = st.sidebar.number_input("GA 天數 (H1)", min_value=0, max_value=6, value=0, step=1)

st.sidebar.write("---")
# L1: PNA出生天數
st.sidebar.markdown("**PNA 出生天數 (L1)**")
l1_pna = st.sidebar.number_input("請輸入出生天數 (days)", min_value=0, max_value=365, value=1, step=1)


# --- 後台邏輯計算：PMA 自動換算 (對應 Excel Q1, S1) ---
ga_total_days = (f1_ga_wk * 7) + h1_ga_day
pma_total_days = ga_total_days + l1_pna
q1_pma_wk = pma_total_days // 7
s1_pma_day = pma_total_days % 7


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


# --- 核心功能頁籤 (對應圖片的五大工作表) ---
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
    st.header("分類大項：第一類 - Antimicrobial agents")
    
    # 建立藥物區塊：Ampicillin
    st.markdown("### 🧬 Ampicillin")
    st.markdown("#### 📌 Normal 療程建議")
    
    # 安全防錯檢查：檢查體重是否為 0
    if b1_bw <= 0:
        st.warning("⚠️ 請先於左側欄位輸入大於 0 的「體重 (BW)」，系統將自動計算建議劑量。")
    else:
        # 1. 轉化您的 Excel 劑量公式 (B4)
        if ga_total_days <= 244:  # GA ≦ 34+6wk (244天)
            if l1_pna <= 7:
                b4_dose = b1_bw * 50
                is_valid = True
            else:
                b4_dose = b1_bw * 75
                is_valid = True
        else:  # GA ≧ 35+0wk
            if l1_pna <= 28:
                b4_dose = b1_bw * 50
                is_valid = True
            else:
                b4_dose = "超過28天(請手動確認)"
                is_valid = False
                
        # 2. 轉化您的 Excel 頻次公式 (D4)
        if ga_total_days <= 244:
            d4_freq = "Q12H"
        else:
            d4_freq = "Q8H"
            
        # 3. 前端呈現結果
        col_dose, col_freq = st.columns(2)
        with col_dose:
            if is_valid:
                st.metric(label="💰 建議單次劑量 (B4)", value=f"{b4_dose:.1f} mg/dose")
            else:
                st.error(f"❌ 劑量警示 (B4)：{b4_dose}")
                
        with col_freq:
            if is_valid or l1_pna > 28:
                st.metric(label="⏱️ 給藥頻次 (D4)", value=d4_freq)

# =========================================================================
# 其餘分頁暫時保留作為骨架
# =========================================================================
with tab2:
    st.info("⏳ Ion dosage 模組建構中，等待輸入下一批公式...")
with tab3:
    st.info("⏳ DART.BURST 模組建構中，等待輸入下一批公式...")
with tab4:
    st.info("⏳ PUMP 總表115 模組建構中，等待輸入下一批公式...")
with tab5:
    st.info("⏳ Dexmedetomidine 模組建構中，等待輸入下一批公式...")

# --- 頁尾 ---
st.write("---")
st.caption("🔒 NICU智慧計算機 | 臨床決策支援系統 (CDSS) 安全防護中")
