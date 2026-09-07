import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Discount & Business KPI - E-commerce", layout="wide")
st.title("Phân tích mối quan hệ giữa Discount và Hiệu quả kinh doanh trong thương mại điện tử ")
st.caption("Học viên thực hiện: Huỳnh Trúc Ngân")

# ---- Đọc dữ liệu ----
discount_kpi = pd.read_csv("discount_kpi.csv")
category_discount = pd.read_csv("category_discount.csv")
order_margin = pd.read_csv("order_profit_margin.csv")
corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

group_order = ["0%", ">0-10%", ">10-20%", ">20-30%", ">30%"]

# Ép thứ tự nhóm Discount đúng thứ tự logic thay vì alphabet
discount_kpi["Order_Discount_Group"] = pd.Categorical(
    discount_kpi["Order_Discount_Group"], categories=group_order, ordered=True
)
discount_kpi = discount_kpi.sort_values("Order_Discount_Group")

order_margin["Order_Discount_Group"] = pd.Categorical(
    order_margin["Order_Discount_Group"], categories=group_order, ordered=True
)

# ---- 1. KPI tổng quan ----
st.header("1. Tổng quan KPI theo nhóm Discount")
st.dataframe(discount_kpi, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(discount_kpi, x="Order_Discount_Group", y="Sales",
                 title="Total Sales by Discount Group")
    fig.update_layout(title_font_size=15, height=380)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.bar(discount_kpi, x="Order_Discount_Group", y="Quantity",
                 title="Total Quantity by Discount Group")
    fig.update_layout(title_font_size=15, height=380)
    st.plotly_chart(fig, use_container_width=True)

# ---- 2. Profit Margin Trend ----
st.header("2. Profit Margin Trend by Discount Group")
fig = px.line(discount_kpi, x="Order_Discount_Group", y="Profit_Margin", markers=True,
              title="Profit Margin Trend by Discount Group")
fig.add_hline(y=0, line_color="red")
fig.update_layout(title_font_size=15, height=400,
                   xaxis_title="Discount Group", yaxis_title="Profit Margin (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 3. AOV theo nhóm Discount ----
st.header("3. Average Order Value (AOV) by Discount Group")
fig = px.bar(discount_kpi, x="Order_Discount_Group", y="Sales_per_Order",
             title="AOV - Sales per Order by Discount Group")
fig.update_layout(title_font_size=15, height=400,
                   xaxis_title="Discount Group", yaxis_title="AOV ($)")
st.plotly_chart(fig, use_container_width=True)

# ---- 4. Boxplot phân phối Profit Margin ----
st.header("4. Distribution of Order Profit Margin by Discount Group")
fig = px.box(order_margin, x="Order_Discount_Group", y="Order_Profit_Margin",
             title="Distribution of Order Profit Margin by Discount Group")
fig.add_hline(y=0, line_color="red")
fig.update_layout(title_font_size=15, height=450,
                   xaxis_title="Discount Group", yaxis_title="Order Profit Margin (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 5. Profit Margin theo Category ----
st.header("5. Profit Margin Trend by Category and Discount Group")
category_discount["Discount_Group"] = pd.Categorical(
    category_discount["Discount_Group"], categories=group_order, ordered=True
)
category_discount = category_discount.sort_values("Discount_Group")

fig = px.line(category_discount, x="Discount_Group", y="Profit_Margin", color="Category",
              markers=True, title="Profit Margin Trend by Category and Discount Group")
fig.add_hline(y=0, line_color="black")
fig.update_layout(title_font_size=15, height=450,
                   xaxis_title="Discount Group", yaxis_title="Profit Margin (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 6. Correlation matrix ----
st.header("6. Correlation Matrix")
fig = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r",
                 zmin=-1, zmax=1, title="Correlation Matrix (Spark MLlib)")
fig.update_layout(title_font_size=15, height=450)
st.plotly_chart(fig, use_container_width=True)

st.info("Lưu ý: Dữ liệu là dữ liệu quan sát (observational). Các mối quan hệ trình bày ở đây không thể diễn giải là quan hệ nhân quả.")
