import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Discount & Business KPI - E-commerce", layout="wide")
st.title("Phân tích mối quan hệ giữa Discount và hiệu quả kinh doanh (E-commerce)")
st.caption("Case study PySpark trên dataset Sample Superstore (Kaggle)")

discount_kpi = pd.read_csv("discount_kpi.csv")
category_discount = pd.read_csv("category_discount.csv")
order_margin = pd.read_csv("order_profit_margin.csv")
corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

group_order = ["0%", ">0-10%", ">10-20%", ">20-30%", ">30%"]

st.header("1. Tổng quan KPI theo nhóm Discount")
st.dataframe(discount_kpi)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    ax.bar(discount_kpi["Order_Discount_Group"], discount_kpi["Sales"])
    ax.set_title("Total Sales by Discount Group")
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots()
    ax.bar(discount_kpi["Order_Discount_Group"], discount_kpi["Quantity"])
    ax.set_title("Total Quantity by Discount Group")
    st.pyplot(fig)

st.header("2. Profit Margin Trend by Discount Group")
fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(discount_kpi["Order_Discount_Group"], discount_kpi["Profit_Margin"], marker="o")
ax.axhline(0, color="red")
st.pyplot(fig)

st.header("3. Distribution of Order Profit Margin (Boxplot)")
data_by_group = [order_margin[order_margin["Order_Discount_Group"] == g]["Order_Profit_Margin"] for g in group_order]
fig, ax = plt.subplots()
bp = ax.boxplot(data_by_group, showfliers=False)
ax.set_xticks(range(1, len(group_order) + 1))
ax.set_xticklabels(group_order)
ax.axhline(0, color="red")
st.pyplot(fig)

st.header("4. Profit Margin Trend by Category and Discount Group")
pivot = category_discount.pivot(index="Category", columns="Discount_Group", values="Profit_Margin")
fig, ax = plt.subplots()
for cat in pivot.index:
    ax.plot(pivot.columns, pivot.loc[cat], marker="o", label=cat)
ax.axhline(0, color="black", linewidth=1)
ax.legend()
st.pyplot(fig)

st.header("5. Correlation Matrix")
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, ax=ax)
st.pyplot(fig)

st.info("Lưu ý: Dữ liệu là dữ liệu quan sát (observational). Các mối quan hệ trình bày ở đây không thể diễn giải là quan hệ nhân quả.")
