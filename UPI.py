import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(layout='wide')

data=pd.read_csv('data.csv')
data_2=pd.read_csv('data_2.csv')

st.sidebar.title('UPI Payment Visualization')
print(data.info())

UPI_banks=list(data['UPI Banks'].unique())
UPI_banks.insert(0,'Overall Payments')
years=['2020','2021']
selected_bank = st.sidebar.selectbox('Select a Payment Gateway',UPI_banks)
select_year=st.sidebar.selectbox('Year',years)
plot = st.sidebar.button('Plot Graph')

if plot and select_year=='2021':
    if selected_bank=='Overall Payments':
        st.title('Overall Payments')
        temp_df=data.groupby('Month')['Volume in Million'].sum()
        fig=px.line(temp_df,x=temp_df.index,y='Volume in Million',title='Transactions in Millions')
        st.plotly_chart(fig,use_container_width=True)

        temp_df=data.groupby('UPI Banks')['Value (Cr)'].sum()
        fig2=px.bar(temp_df,x=temp_df.index,y='Value (Cr)',title='Value (Cr) by Costumers')
        st.plotly_chart(fig2,use_container_width=True)
        temp_df=data.groupby('Month')['Volume of Costumers(in Millions)'].sum()
        fig3=px.line(temp_df,x=temp_df.index,y='Volume of Costumers(in Millions)',title='Volume of Costumers(in Millions)')
        st.plotly_chart(fig3,use_container_width=True)
        temp_df = data.groupby('UPI Banks')['Volume in Million'].sum().sort_values(ascending=False)
        fig4 = px.pie(temp_df, values='Volume in Million', names=temp_df.index, title='Market Share by Transaction Volume')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        df=data[data['UPI Banks']==selected_bank]
        st.title('Overall Payments')
        temp_df=df.groupby('Month')['Volume in Million'].sum()
        fig=px.line(temp_df,x=temp_df.index,y='Volume in Million',title='Transactions in Millions')
        st.plotly_chart(fig,use_container_width=True)

        temp_df=df.groupby('UPI Banks')['Value (Cr)'].sum()
        fig2=px.bar(temp_df,x=temp_df.index,y='Value (Cr)',title='Value (Cr) by Costumers')
        st.plotly_chart(fig2,use_container_width=True)
        temp_df=df.groupby('Month')['Volume of Costumers(in Millions)'].sum()
        fig3=px.line(temp_df,x=temp_df.index,y='Volume of Costumers(in Millions)',title='Volume of Costumers(in Millions)')
        st.plotly_chart(fig3,use_container_width=True)
        
        


elif plot and select_year=='2020':
    
    if selected_bank=='Overall Payments':
        st.title('Overall Payments')
        temp_df=data_2.groupby('Month')['Volume in Million'].sum()
        fig=px.line(temp_df,x=temp_df.index,y='Volume in Million',title='Number of Transactions in Millions')
        st.plotly_chart(fig,use_container_width=True)

        temp_df=data_2.groupby('UPI Banks')['Value (Cr)'].sum()
        fig2=px.bar(temp_df,x=temp_df.index,y='Value (Cr)',title='Value (Cr) by Costumers')
        st.plotly_chart(fig2,use_container_width=True)
        temp_df=data_2.groupby('Month')['Volume of Costumers(in Millions)'].sum()
        fig3=px.line(temp_df,x=temp_df.index,y='Volume of Costumers(in Millions)',title='Volume of Costumers(in Millions)')
        st.plotly_chart(fig3,use_container_width=True)
        temp_df = data_2.groupby('UPI Banks')['Volume in Million'].sum().sort_values(ascending=False)
        fig4 = px.pie(temp_df, values='Volume in Million', names=temp_df.index, title='Market Share by Transaction Volume')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        df=data_2[data_2['UPI Banks']==selected_bank]
        st.title('Overall Payments')
        temp_df=df.groupby('Month')['Volume in Million'].sum()
        fig=px.line(temp_df,x=temp_df.index,y='Volume in Million',title='Number of Transactions in Millions')
        st.plotly_chart(fig,use_container_width=True)

        temp_df=df.groupby('UPI Banks')['Value (Cr)'].sum()
        fig2=px.bar(temp_df,x=temp_df.index,y='Value (Cr)',title='Value (Cr) by Costumers')
        st.plotly_chart(fig2,use_container_width=True)
        temp_df=df.groupby('Month')['Volume of Costumers(in Millions)'].sum()
        fig3=px.line(temp_df,x=temp_df.index,y='Volume of Costumers(in Millions)',title='Volume of Costumers(in Millions)')
        st.plotly_chart(fig3,use_container_width=True)