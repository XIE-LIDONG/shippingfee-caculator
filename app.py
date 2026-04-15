import streamlit as st
import pandas as pd

# 页面配置：适配手机屏幕
st.set_page_config(
    page_title="ZEN ZEN POT 运费助手", 
    page_icon="📦",
    layout="centered"
)

# 使用 CSS 优化手机端触控体验
st.markdown("""
    <style>
    /* 加大数字输入框的字体和高度，方便手指点击 */
    .stNumberInput input {
        font-size: 20px !important;
        height: 50px !important;
    }
    /* 优化结果卡片的显示效果 */
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 ZEN ZEN POT 运费计算")

# --- 1. 用户输入区 ---
st.subheader("第一步：输入货物重量")
# 直接输入克 (g)，value=0.0 确保为浮点数，避免 Streamlit 类型报错
weight_g = st.number_input(
    "货物实际重量 (单位: 克/g)", 
    min_value=0.0, 
    max_value=30000.0, 
    value=0.0, 
    step=1.0,
    format="%.0f"
)

# 逻辑转换：将克转换为 KG 用于费率匹配
w_kg = weight_g / 1000.0

# --- 2. 箱子推荐逻辑 (按照你的要求，以克为单位判定) ---
if weight_g <= 346:
    box_name = "12号"
elif 346 < weight_g <= 598:
    box_name = "9号"
else:
    box_name = "7号"

# --- 3. 运费费率表 (上限KG, 单价RMB/KG, 挂号费) ---
rates = [
    (0.1, 145, 23), (0.2, 145, 21), (0.3, 143, 19),
    (0.45, 142, 19), (0.7, 141, 19), (2.0, 140, 12), (30.0, 133, 12)
]

# 计费重量不低于 0.03kg (即 30g)
billing_w_kg = max(w_kg, 0.03)
cost, price, fee = 0, 0, 0

for limit, p, f in rates:
    if billing_w_kg <= limit:
        cost = (billing_w_kg * p) + f
        price, fee = p, f
        break

# --- 4. 结果展示区 ---
st.subheader("第二步：计算结果")

# 手机端会上下堆叠展示，视觉清晰
c1, c2 = st.columns(2)
c1.metric("建议使用", f"{box_name}号箱")
c2.metric("预计运费", f"¥ {round(cost, 2)}")

# 计费详情折叠菜单
with st.expander("查看计费详情"):
    details_df = pd.DataFrame({
        "项": ["实际/计费重量", "运费单价", "挂号费"],
        "值": [f"{weight_g} g", f"{price} RMB/KG", f"{fee} RMB/票"]
    })
    st.table(details_df)

# --- 5. 固定对照表 (显示克单位) ---
st.markdown("---")
st.caption("🔍 箱子选择参考范围：")
reference_data = {
    "箱子型号": ["12号箱", "9号箱", "7号箱"],
    "质量区间": ["346g 及以下", "346g ~ 598g", "超过 598g"]
}
st.dataframe(pd.DataFrame(reference_data), use_container_width=True, hide_index=True)

st.info("💡 提示：输入重量后，系统会自动匹配最优箱号并按实时费率计算。")
