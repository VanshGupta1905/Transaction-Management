import streamlit as st
import UpiUser
import qrcode
from io import BytesIO
from Database import users
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

choose=st.sidebar.selectbox("Choose",['UPI','Payment Services Analyis','My Payment Analysis'])
if choose=='UPI':
    st.sidebar.title("UPI Application")

    activity = st.sidebar.radio("Choose an activity",
        ["Add Account", "Request Money", "Pending Requests", "Approve/Reject Request", "Check Balance", "View All Users", "Transaction History", "Profile Management", "Generate QR Code"])

    st.title(f"UPI Application - {activity}")

    if activity == "Add Account":
        with st.form("create_user_form"):
            Name = st.text_input("Enter Name")
            new_upi_id = st.text_input("Enter UPI ID")
            Phone_No = st.text_input("Enter Phone Number")

            submit_button = st.form_submit_button("Create User")
            if submit_button and new_upi_id not in users:
                result = UpiUser.UPIUser(Name, Phone_No, new_upi_id)
                users[new_upi_id] = result
                print(users)
                st.success(f"User created: {result.name, result.phone_number, result.upi_id}")
            elif submit_button and new_upi_id in users:
                st.error("User Already Exists")

    elif activity == "Request Money":
        with st.form("request_money_form"):
            requester_upi_id = st.text_input("Requester UPI ID")
            from_upi_id = st.text_input("From UPI ID")
            amount = st.number_input("Amount", min_value=0, step=1000)
            description = st.text_input("Description")
            submit_button = st.form_submit_button("Request Money")

            if submit_button:
                if from_upi_id in users:
                    user = users[from_upi_id]
                    try:
                        result = user.request_money(from_upi_id, amount, description)
                        st.success(f"Money requested: {result}")
                    except Exception as e:
                        st.error(f"Error requesting money: {e}")
                else:
                    st.error(f"User with UPI ID {from_upi_id} not found.")


    elif activity == "Pending Requests":
        with st.form("pending_requests_form"):
            upi_id = st.text_input("UPI ID for Pending Requests")
            submit_button = st.form_submit_button("Get Pending Requests")
            if submit_button:
                if upi_id in users:
                    user = users[upi_id]
                    pending_requests = user.get_pending_requests()
                    if pending_requests:
                        st.markdown("### Your Pending Requests")
                        st.table(pending_requests)
                    else:
                        st.info("No pending requests found.")
                else:
                    st.error(f"User with UPI ID {upi_id} not found.")

    elif activity == "Approve/Reject Request":
        with st.form("approve_reject_form"):
            action_upi_id = st.text_input("UPI ID")
            request_id = st.text_input("Request ID")
            col1, col2 = st.columns(2)
            with col1:
                approve_button = st.form_submit_button("Approve")
            with col2:
                reject_button = st.form_submit_button("Reject")

            if approve_button:
                result = UpiUser.approve_request(action_upi_id, request_id)
                st.success(f"Request approved: {result}")
            elif reject_button:
                result = UpiUser.reject_request(action_upi_id, request_id)
                st.error(f"Request rejected: {result}")

    elif activity == "Check Balance":
        with st.form("check_balance_form"):
            upi_id = st.text_input("UPI ID for Balance Check")
            submit_button = st.form_submit_button("Check Balance")
            if submit_button:
                print(users)
                print(upi_id)
                if upi_id in users:
                    user = users[str(upi_id)]
                    result = user.check_balance()
                    st.info(f"Current balance: {result}")
                else:
                    st.error(f"User with UPI ID {upi_id} not found.")

    elif activity == "View All Users":
        st.header("All Users")
        if users:
            for upi_id, user in users.items():
                with st.expander(f"User: {user.name}"):
                    st.markdown(f"""
                        <div style="background-color: #0000; padding: 10px; border-radius: 5px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <h4>{user.name}</h4>
                            <p><strong>UPI ID:</strong> {user.upi_id}</p>
                            <p><strong>Phone Number:</strong> {user.phone_number}</p>
                            <p><strong>Balance:</strong> {user.check_balance()}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No users found.")

    elif activity == "Transaction History":
        st.header("Transaction History")
        upi_id = st.text_input("Enter UPI ID to view transaction history")
        if st.button("Get History"):
            # Simulate fetching transaction history
            user = users[str(upi_id)]
            history = user.view_transaction_history()
            st.table(history)

    elif activity == "Profile Management":
        st.header("Profile Management")
        upi_id = st.text_input("Enter UPI ID to manage profile")
        if st.button("Get Profile"):
            if upi_id in users:
                user = users[upi_id]
                with st.form("update_profile_form"):
                    new_name = st.text_input("Update Name", value=user.name)
                    new_phone = st.text_input("Update Phone Number", value=user.phone_number)
                    submit_button = st.form_submit_button("Update Profile")
                    if submit_button:
                        user.name = new_name
                        user.phone_number = new_phone
                        st.success("Profile updated successfully")
            else:
                st.error("User not found")

    elif activity == "Generate QR Code":
        st.header("Generate QR Code")
        upi_id = st.text_input("Enter UPI ID to generate QR code")
        if st.button("Generate"):
            if upi_id in users:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(upi_id)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                buf = BytesIO()
                img.save(buf)
                byte_im = buf.getvalue()
                st.image(byte_im, caption=f"QR Code for {upi_id}")
            else:
                st.error("User not found")

    st.sidebar.markdown("---")
    st.sidebar.info("This is a UPI application demo.")
    st.sidebar.markdown(" In Order to make a real transaction this app needs to be connected to IMPS API"
                "The permission for IMPS API is only availaible to Rejistered FinTech Companies")


if choose=='Payment Services Analyis':

    data = pd.read_csv('data.csv')
    data_2 = pd.read_csv('data_2.csv')

    st.sidebar.title('UPI Payment Visualization')
    print(data.info())

    UPI_banks = list(data['UPI Banks'].unique())
    UPI_banks.insert(0, 'Overall Payments')
    years = ['2020', '2021']
    selected_bank = st.sidebar.selectbox('Select a Payment Gateway', UPI_banks)
    select_year = st.sidebar.selectbox('Year', years)
    plot = st.sidebar.button('Plot Graph')

    if plot and select_year == '2021':
        if selected_bank == 'Overall Payments':
            st.title('Overall Payments')
            temp_df = data.groupby('Month')['Volume in Million'].sum()
            fig = px.line(temp_df, x=temp_df.index, y='Volume in Million', title='Transactions in Millions')
            st.plotly_chart(fig, use_container_width=True)

            temp_df = data.groupby('UPI Banks')['Value (Cr)'].sum()
            fig2 = px.bar(temp_df, x=temp_df.index, y='Value (Cr)', title='Value (Cr) by Costumers')
            st.plotly_chart(fig2, use_container_width=True)
            temp_df = data.groupby('Month')['Volume of Costumers(in Millions)'].sum()
            fig3 = px.line(temp_df, x=temp_df.index, y='Volume of Costumers(in Millions)',
                           title='Volume of Costumers(in Millions)')
            st.plotly_chart(fig3, use_container_width=True)
            temp_df = data.groupby('UPI Banks')['Volume in Million'].sum().sort_values(ascending=False)
            fig4 = px.pie(temp_df, values='Volume in Million', names=temp_df.index,
                          title='Market Share by Transaction Volume')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            df = data[data['UPI Banks'] == selected_bank]
            st.title('Overall Payments')
            temp_df = df.groupby('Month')['Volume in Million'].sum()
            fig = px.line(temp_df, x=temp_df.index, y='Volume in Million', title='Transactions in Millions')
            st.plotly_chart(fig, use_container_width=True)

            temp_df = df.groupby('UPI Banks')['Value (Cr)'].sum()
            fig2 = px.bar(temp_df, x=temp_df.index, y='Value (Cr)', title='Value (Cr) by Costumers')
            st.plotly_chart(fig2, use_container_width=True)
            temp_df = df.groupby('Month')['Volume of Costumers(in Millions)'].sum()
            fig3 = px.line(temp_df, x=temp_df.index, y='Volume of Costumers(in Millions)',
                           title='Volume of Costumers(in Millions)')
            st.plotly_chart(fig3, use_container_width=True)




    elif plot and select_year == '2020':

        if selected_bank == 'Overall Payments':
            st.title('Overall Payments')
            temp_df = data_2.groupby('Month')['Volume in Million'].sum()
            fig = px.line(temp_df, x=temp_df.index, y='Volume in Million', title='Number of Transactions in Millions')
            st.plotly_chart(fig, use_container_width=True)

            temp_df = data_2.groupby('UPI Banks')['Value (Cr)'].sum()
            fig2 = px.bar(temp_df, x=temp_df.index, y='Value (Cr)', title='Value (Cr) by Costumers')
            st.plotly_chart(fig2, use_container_width=True)
            temp_df = data_2.groupby('Month')['Volume of Costumers(in Millions)'].sum()
            fig3 = px.line(temp_df, x=temp_df.index, y='Volume of Costumers(in Millions)',
                           title='Volume of Costumers(in Millions)')
            st.plotly_chart(fig3, use_container_width=True)
            temp_df = data_2.groupby('UPI Banks')['Volume in Million'].sum().sort_values(ascending=False)
            fig4 = px.pie(temp_df, values='Volume in Million', names=temp_df.index,
                          title='Market Share by Transaction Volume')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            df = data_2[data_2['UPI Banks'] == selected_bank]
            st.title('Overall Payments')
            temp_df = df.groupby('Month')['Volume in Million'].sum()
            fig = px.line(temp_df, x=temp_df.index, y='Volume in Million', title='Number of Transactions in Millions')
            st.plotly_chart(fig, use_container_width=True)

            temp_df = df.groupby('UPI Banks')['Value (Cr)'].sum()
            fig2 = px.bar(temp_df, x=temp_df.index, y='Value (Cr)', title='Value (Cr) by Costumers')
            st.plotly_chart(fig2, use_container_width=True)
            temp_df = df.groupby('Month')['Volume of Costumers(in Millions)'].sum()
            fig3 = px.line(temp_df, x=temp_df.index, y='Volume of Costumers(in Millions)',
                           title='Volume of Costumers(in Millions)')
            st.plotly_chart(fig3, use_container_width=True)
if choose=='My Payment Analysis':

    data = pd.read_csv('personal_data.csv')
    st.sidebar.title('Personal Transactions')
    years = ['2023']
    select_year = st.sidebar.selectbox('Year', years)

    months = ['Overall', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    select_month = st.sidebar.selectbox('Month', months)
    plot = st.sidebar.button('Plot Graph')
    if plot and select_month == 'Overall':
        data['Category'].value_counts()
        fig5 = px.bar(data['Category'].value_counts(), title='Number of Transactions vs Categories')
        st.plotly_chart(fig5, use_container_width=True)

        category_trends = data.pivot_table(values='Withdrawal', index='Month', columns='Category',
                                           aggfunc='sum').fillna(0)
        fig8 = px.area(category_trends, title='Category-wise Spending Trends')
        st.plotly_chart(fig8, use_container_width=True)

        monthly_summary = data.groupby('Month').agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
        fig7 = px.bar(monthly_summary, x='Month', y=['Deposit', 'Withdrawal'],
                      title='Monthly Income vs Expenses', barmode='group')
        st.plotly_chart(fig7, use_container_width=True)

        fig4 = px.scatter(data, x='Withdrawal', y='Balance', title='Withdrawal vs Balance')
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.line(data, x=data.index, y='Balance', title='Balance of Entire Year')
        st.plotly_chart(fig5, use_container_width=True)

        temp_df = data.groupby(['day'])['Withdrawal'].mean()
        fig = px.bar(temp_df, x=temp_df.index, y='Withdrawal', title='Average Money Withdrawal Everyday ',
                     color_discrete_sequence=['#F63366'])
        st.plotly_chart(fig, use_container_width=True)

        temp_df = data.groupby(['Month'])['Deposit'].sum()
        fig2 = px.line(temp_df, x=temp_df.index, y='Deposit', title='Money Deposited Every Month')
        st.plotly_chart(fig2, use_container_width=True)

        temp_df = data.groupby(['Month'])['Balance'].mean()
        fig3 = px.bar(temp_df, x=temp_df.index, y='Balance', title='Balance Every Month in Account',
                      color_discrete_sequence=['#16ffdf'])
        st.plotly_chart(fig3, use_container_width=True)

        temp_df = data.groupby(['Category'])['Withdrawal'].sum()
        fig6 = px.pie(temp_df, values='Withdrawal', names=temp_df.index)
        st.plotly_chart(fig6, use_container_width=True)

    if plot and select_month != 'Overall':
        df = data[data['Month'] == select_month]

        fig10 = make_subplots(specs=[[{"secondary_y": True}]])
        fig10.add_trace(go.Bar(x=df['Date'], y=df['Deposit'], name='Income', marker_color='green'), secondary_y=False)
        fig10.add_trace(go.Bar(x=df['Date'], y=df['Withdrawal'], name='Expenses', marker_color='red'),
                        secondary_y=False)
        fig10.add_trace(go.Scatter(x=df['Date'], y=df['Balance'], name='Balance', mode='lines+markers'),
                        secondary_y=True)
        fig10.update_layout(title_text='Daily Income, Expenses, and Balance')
        fig10.update_yaxes(title_text="Amount", secondary_y=False)
        fig10.update_yaxes(title_text="Balance", secondary_y=True)
        st.plotly_chart(fig10, use_container_width=True)

        fig5 = px.bar(df['Category'].value_counts(), title='Number of Transactions vs Categories')
        st.plotly_chart(fig5, use_container_width=True)

        fig4 = px.scatter(df, x='Withdrawal', y='Balance', title='Withdrawal vs Balance')
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.line(df, x=df.index, y='Balance', title='Balance of Entire Month')
        st.plotly_chart(fig5, use_container_width=True)

        temp_df = df.groupby(['day'])['Withdrawal'].mean()
        fig = px.bar(temp_df, x=temp_df.index, y='Withdrawal', title='Average Money Withdrawal Everyday ',
                     color_discrete_sequence=['#F63366'])
        st.plotly_chart(fig, use_container_width=True)

        temp_df = df.groupby(['Category'])['Withdrawal'].sum()
        fig6 = px.pie(temp_df, values='Withdrawal', names=temp_df.index)
        st.plotly_chart(fig6, use_container_width=True)