import streamlit as st
import pandas as pd

# 页面配置：初次加载即为宽屏模式（适配手机屏幕）
st.set_page_config(
    page_title="ZEN ZEN POT 运费助手", 
    page_icon="📦",
    layout="centered"
)

# 使用 CSS 强制优化手机端显示：加大输入框高度和字体
st.markdown("""
    <style>
    .stNumberInput input {
        font-size: 20px !important;
        height: 50px !important;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 运费计算助手")

# --- 1. 用户输入区 ---
st.subheader("第一步：输入货物重量")
# 使用 number_input，在手机上会自动弹出数字键盘
weight = st.number_input(
    "货物实际重量 (KG)", 
    min_value=0.0, 
    max_value=30.0, 
    value=0, 
    step=0.01,
    format="%.2f"
)

# --- 2. 核心逻辑计算 ---
# 判定箱子
if weight <= 0.346:
    box_name = "12号"
elif 0.346 < weight <= 0.598:
    box_name = "9号"
else:
    box_name = "7号"

# 费率逻辑
rates = [
    (0.1, 145, 23), (0.2, 145, 21), (0.3, 143, 19),
    (0.45, 142, 19), (0.7, 141, 19), (2.0, 140, 12), (30.0, 133, 12)
]

billing_w = max(weight, 0.03)
cost, price, fee = 0, 0, 0

for limit, p, f in rates:
    if billing_w <= limit:
        cost = (billing_w * p) + f
        price, fee = p, f
        break

# --- 3. 结果展示区 ---
st.subheader("第二步：计算结果")

# 在手机上，columns 会自动堆叠，看起来非常自然
c1, c2 = st.columns(2)
c1.metric("建议箱子", f"{box_name}号")
c2.metric("预计运费", f"¥{round(cost, 2)}")

# 详细明细：使用 st.expander 节省空间，点击可查看
with st.expander("查看计费详情"):
    details_df = pd.DataFrame({
        "项": ["实际/计费重", "单价", "挂号费"],
        "值": [f"{billing_w} KG", f"{price} RMB", f"{fee} RMB"]
    })
    st.table(details_df)

# --- 4. 参考表（放在底部，不遮挡操作） ---
st.markdown("---")
st.caption("🔍 箱子选择参考范围：")
reference_data = {
    "箱子": ["12号", "9号", "7号"],
    "适用重量": ["<= 0.346kg", "0.346 ~ 0.598kg", "> 0.598kg"]
}
st.dataframe(pd.DataFrame(reference_data), use_container_width=True, hide_index=True)
