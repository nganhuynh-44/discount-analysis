import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Discount & Business KPI - E-commerce", layout="wide")
st.title("Phân tích mối quan hệ giữa Discount và Hiệu quả kinh doanh trong thương mại điện tử ")
st.caption("Học viên thực hiện: Huỳnh Trúc Ngân")
st.caption("Mã số học viên: C25611251")

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

# ---- 1. Phân bố Discount ----
st.markdown("<h4 style='font-size:22px;'>1. Tổng quan KPI theo nhóm Discount</h4>", unsafe_allow_html=True)
fig = px.bar(discount_kpi, x="Order_Discount_Group", y="Orders",
             title="Số lượng đơn hàng theo nhóm Discount")
fig.update_layout(title_font_size=13, height=380,
                   xaxis_title="Nhóm Discount", yaxis_title="Số đơn hàng")
st.plotly_chart(fig, use_container_width=True)

# ---- 2. KPI tổng quan ----
st.header("2. Tổng quan KPI theo nhóm Discount")
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

# ---- 3. Profit Margin Trend ----
st.header("3. Xu hướng Profit Margin theo nhóm Discount")
fig = px.line(discount_kpi, x="Order_Discount_Group", y="Profit_Margin", markers=True,
              title="Xu hướng Profit Margin theo nhóm Discount")
fig.add_hline(y=0, line_color="red")
fig.update_layout(title_font_size=15, height=400,
                   xaxis_title="Nhóm Discount", yaxis_title="Profit Margin (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 4. AOV theo nhóm Discount ----
st.header("4. Giá trị đơn hàng trung bình (AOV) theo nhóm Discount")
fig = px.bar(discount_kpi, x="Order_Discount_Group", y="Sales_per_Order",
             title="AOV - Doanh thu trung bình mỗi đơn theo nhóm Discount")
fig.update_layout(title_font_size=15, height=400,
                   xaxis_title="Nhóm Discount", yaxis_title="AOV ($)")
st.plotly_chart(fig, use_container_width=True)

# ---- 5. Boxplot phân phối Profit Margin ----
st.header("5. Phân phối Profit Margin theo nhóm Discount")
fig = px.box(order_margin, x="Order_Discount_Group", y="Order_Profit_Margin",
             title="Phân phối Profit Margin theo nhóm Discount")
fig.add_hline(y=0, line_color="red")
fig.update_layout(title_font_size=15, height=450,
                   xaxis_title="Nhóm Discount", yaxis_title="Profit Margin của đơn hàng (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 6. Profit Margin theo Category ----
st.header("6. Xu hướng Profit Margin theo Category và nhóm Discount")
category_discount["Discount_Group"] = pd.Categorical(
    category_discount["Discount_Group"], categories=group_order, ordered=True
)
category_discount = category_discount.sort_values("Discount_Group")

fig = px.line(category_discount, x="Discount_Group", y="Profit_Margin", color="Category",
              markers=True, title="Xu hướng Profit Margin theo Category và nhóm Discount")
fig.add_hline(y=0, line_color="black")
fig.update_layout(title_font_size=15, height=450,
                   xaxis_title="Nhóm Discount", yaxis_title="Profit Margin (%)")
st.plotly_chart(fig, use_container_width=True)

# ---- 7. Correlation matrix ----
st.header("7. Ma trận tương quan")
fig = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r",
                 zmin=-1, zmax=1, title="Ma trận tương quan (Spark MLlib)")
fig.update_layout(title_font_size=15, height=450)
st.plotly_chart(fig, use_container_width=True)

