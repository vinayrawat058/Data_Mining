import streamlit as st
import pandas as pd
import numpy as np
from utils import calculate_new_price_and_units,adjust_price,CITY_LIST,LOC_LIST
st.set_page_config(layout="wide")
st.title("Price Optimization 📈")

with st.form('Price Optimization'):
    # Input for dataset upload
    level = st.radio('Select the level at which you want price recommendation',['Overall','Store','City','Location'])
    store_id = st.selectbox('Store_ID (Only if needed at store level*)',[x for x in range(1,51)])
    city = st.selectbox('City (Only if needed at City level*)',CITY_LIST)
    location = st.selectbox('Location in City (Only if needed at Location level*)',LOC_LIST)

    if level == 'Overall':
        product_elasticity = pd.read_csv('clean_data/elasticities/product_elasticities.csv')
        sales_data = pd.read_csv('clean_data/month_yr_product_rollup_data.csv')
        sales_data = sales_data.loc[(sales_data['Year']==2023) & (sales_data['Month'] >=3)]
        sales_data = sales_data.groupby(['Product_ID','Product_Name','Product_Category']).agg({'Product_Cost':'max','Units':'sum','Actual_Product_Price':'mean','Product_Price':'max','Revenue':'sum','xRevenue':'sum','Profit':'sum'}).reset_index()
        final_data = sales_data.merge(product_elasticity,how='left',on='Product_ID')
    
    if level == 'Store':
        product_elasticity = pd.read_csv('clean_data/elasticities/store_elasticities.csv')
        sales_data = pd.read_csv('clean_data/month_yr_store_product_rollup_data.csv')
        sales_data = sales_data.loc[(sales_data['Year']==2023) & (sales_data['Month'] >=3) & (sales_data['Store_ID']==store_id)]
        sales_data = sales_data.groupby(['Store_ID','Product_ID','Product_Name','Product_Category']).agg({'Product_Cost':'max','Units':'sum','Actual_Product_Price':'mean','Product_Price':'max','Revenue':'sum','xRevenue':'sum','Profit':'sum'}).reset_index()
        final_data = sales_data.merge(product_elasticity,how='left',on=['Product_ID','Store_ID'])
        
    if level == 'City':
        product_elasticity = pd.read_csv('clean_data/elasticities/store_city_elasticities.csv')
        sales_data = pd.read_csv('clean_data/month_yr_store_city_product_rollup_data.csv')
        sales_data = sales_data.loc[(sales_data['Year']==2023) & (sales_data['Month'] >=3) & (sales_data['Store_City']==city)]
        sales_data = sales_data.groupby(['Store_City','Product_ID','Product_Name','Product_Category']).agg({'Product_Cost':'max','Units':'sum','Actual_Product_Price':'mean','Product_Price':'max','Revenue':'sum','xRevenue':'sum','Profit':'sum'}).reset_index()
        final_data = sales_data.merge(product_elasticity,how='left',on=['Store_City','Product_ID'])
        
    if level == 'Location':
        product_elasticity = pd.read_csv('clean_data/elasticities/store_loc_elasticities.csv')
        sales_data = pd.read_csv('clean_data/month_yr_loc_product_rollup_data.csv')
        sales_data = sales_data.loc[(sales_data['Year']==2023) & (sales_data['Month'] >=3) & (sales_data['Store_Location'] ==location)]
        sales_data = sales_data.groupby(['Store_Location','Product_ID','Product_Name','Product_Category']).agg({'Product_Cost':'max','Units':'sum','Actual_Product_Price':'mean','Product_Price':'max','Revenue':'sum','xRevenue':'sum','Profit':'sum'}).reset_index()
        final_data = sales_data.merge(product_elasticity,how='left',on=['Store_Location','Product_ID'])
        
    clicked = st.form_submit_button('Find new prices')


if clicked:
    final_data[["New_Product_Price", "New_Units"]] = final_data.apply(calculate_new_price_and_units, axis=1)
    final_data['New_Product_Price'] = (final_data["New_Product_Price"].apply(lambda x: x + 0.01 if str(round(x, 2))[-1] == '4' else x))
    # final_data['New_Product_Price'] = final_data['New_Product_Price'].apply(adjust_price)
    final_data['New_Revenue'] = round(final_data["New_Product_Price"]*final_data["New_Units"],2)
    final_data['Delta_Revenue'] = final_data['New_Revenue'] -final_data['xRevenue']
    final_data['Delta_Change'] = final_data['New_Product_Price'] -final_data['Product_Price']
    predicted_revenue_increase = round(final_data['Delta_Revenue'].sum(),2)
    st.success(f"The revenue with new prices are expected to increase in the range of \${round(predicted_revenue_increase*0.8,2)} to \$ {round(predicted_revenue_increase*1.2,2)}")
    
    st.dataframe(final_data[['Product_ID','Product_Price','New_Product_Price','Delta_Change','xRevenue','New_Revenue','Delta_Revenue']])
    csv_data = final_data.to_csv(index=False, sep="|")
    st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="price_opt.csv",
    mime="text/csv",)
