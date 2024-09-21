import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


data=pd.read_csv('personal_data.csv')
st.sidebar.title('Personal Transactions')
years=['2023']
select_year=st.sidebar.selectbox('Year',years)

months=['Overall','January', 'February', 'March', 'April', 'May', 'June', 
'July', 'August', 'September', 'October', 'November', 'December']
select_month=st.sidebar.selectbox('Month',months)
plot = st.sidebar.button('Plot Graph')
if plot and select_month=='Overall':


    data['Category'].value_counts()
    fig5=px.bar(data['Category'].value_counts(),title='Number of Transactions vs Categories')
    st.plotly_chart(fig5,use_container_width=True)

    category_trends = data.pivot_table(values='Withdrawal', index='Month', columns='Category', aggfunc='sum').fillna(0)
    fig8 = px.area(category_trends, title='Category-wise Spending Trends')
    st.plotly_chart(fig8, use_container_width=True)


    monthly_summary = data.groupby('Month').agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
    fig7 = px.bar(monthly_summary, x='Month', y=['Deposit', 'Withdrawal'], 
                  title='Monthly Income vs Expenses', barmode='group')
    st.plotly_chart(fig7, use_container_width=True)


    fig4=px.scatter(data,x='Withdrawal',y='Balance',title='Withdrawal vs Balance')
    st.plotly_chart(fig4,use_container_width=True)
    
    fig5=px.line(data,x=data.index,y='Balance',title='Balance of Entire Year')
    st.plotly_chart(fig5,use_container_width=True)

    temp_df=data.groupby(['day'])['Withdrawal'].mean()
    fig=px.bar(temp_df,x=temp_df.index,y='Withdrawal',title='Average Money Withdrawal Everyday ',color_discrete_sequence=['#F63366'])
    st.plotly_chart(fig,use_container_width=True)
    


    temp_df=data.groupby(['Month'])['Deposit'].sum()
    fig2=px.line(temp_df,x=temp_df.index,y='Deposit',title='Money Deposited Every Month')
    st.plotly_chart(fig2,use_container_width=True)



    

    
    temp_df=data.groupby(['Month'])['Balance'].mean()
    fig3=px.bar(temp_df,x=temp_df.index,y='Balance',title='Balance Every Month in Account',color_discrete_sequence=['#16ffdf'])
    st.plotly_chart(fig3,use_container_width=True)
    

    temp_df=data.groupby(['Category'])['Withdrawal'].sum()
    fig6=px.pie(temp_df,values='Withdrawal',names=temp_df.index)
    st.plotly_chart(fig6,use_container_width=True)



if plot and select_month!='Overall':
    df=data[data['Month']==select_month]

    fig10 = make_subplots(specs=[[{"secondary_y": True}]])
    fig10.add_trace(go.Bar(x=df['Date'], y=df['Deposit'], name='Income', marker_color='green'), secondary_y=False)
    fig10.add_trace(go.Bar(x=df['Date'], y=df['Withdrawal'], name='Expenses', marker_color='red'), secondary_y=False)
    fig10.add_trace(go.Scatter(x=df['Date'], y=df['Balance'], name='Balance', mode='lines+markers'), secondary_y=True)
    fig10.update_layout(title_text='Daily Income, Expenses, and Balance')
    fig10.update_yaxes(title_text="Amount", secondary_y=False)
    fig10.update_yaxes(title_text="Balance", secondary_y=True)
    st.plotly_chart(fig10, use_container_width=True)






    fig5=px.bar(df['Category'].value_counts(),title='Number of Transactions vs Categories')
    st.plotly_chart(fig5,use_container_width=True)


    fig4=px.scatter(df,x='Withdrawal',y='Balance',title='Withdrawal vs Balance')
    st.plotly_chart(fig4,use_container_width=True)

    fig5=px.line(df,x=df.index,y='Balance',title='Balance of Entire Month')
    st.plotly_chart(fig5,use_container_width=True)

    temp_df=df.groupby(['day'])['Withdrawal'].mean()
    fig=px.bar(temp_df,x=temp_df.index,y='Withdrawal',title='Average Money Withdrawal Everyday ',color_discrete_sequence=['#F63366'])
    st.plotly_chart(fig,use_container_width=True)
       
    

    temp_df=df.groupby(['Category'])['Withdrawal'].sum()
    fig6=px.pie(temp_df,values='Withdrawal',names=temp_df.index)
    st.plotly_chart(fig6,use_container_width=True)


    


