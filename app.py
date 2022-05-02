
import pandas as pd  
import plotly.express as px 
import streamlit as st  
import numpy as np



st.set_page_config(
    page_title="Org. Sales Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide")


# read the data
df = pd.read_csv("./sales.csv")



st.sidebar.header("Select Your Options: ")

city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()[0]
)

customer_type = st.sidebar.multiselect(
    "Choose the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()[0],
)

gender = st.sidebar.multiselect(
    "Choose the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()[0]
)

prod_line = st.sidebar.multiselect(
    "Choose Product line type",
    options = df['Productline'].unique(),
    default = df['Productline'].unique()[0]
)

# & Productline == @prod_line
df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender "
)


# define the page look
st.title("Sales Dashboard")



total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)


col1, col2, col3= st.columns(3)
with col1:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")
with col2:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with col3:
    st.subheader("Avg Sales Per Trans:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# a barchart by productline
sales_by_product_line = (
    df_selection.groupby(by=["Productline"]).sum()[["Total"]].sort_values(by="Total")
)


fig_product_sales = px.bar(
    sales_by_product_line,
    y="Total",
    x=sales_by_product_line.index,
    orientation="v",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#2223B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)



# sales bar
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    orientation ='v',
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#1183B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(showgrid=False),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
