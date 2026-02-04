import streamlit as st
import pandas as pd
from data.loader import load_products, load_businesses_users
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

loans_df = load_products()["loans"]
users_df = load_businesses_users()["users"]
current_staff = st.session_state.get("staff_name")

st.title("🎴 Loans Management")

st.write("This is the Loans management tool. Here you can manage your loans.")

def insert_loan(loan_data):
    # Implementation for inserting loans into google sheet
    new_loan_df = pd.DataFrame([loan_data])
    updated_df = pd.concat([loans_df, new_loan_df], ignore_index=True)
    conn.update(worksheet="loans", data=updated_df)
    st.success("Loan added successfully!")

with st.form("add_loan_form"):
    DateSold = st.date_input("Date Sold")
    st.text_input("Staff Name", value=current_staff, disabled=True)
    CustomerName = st.text_input("Customer Name")
    CustomerPhone = st.text_input("Customer Phone Number")
    Location = st.text_input("Location")
    BusinessName = st.text_input("Business Name")
    LoanAmount = st.text_input("Amount of the loan")

    submitted = st.form_submit_button("Add Loan")

if submitted:
    loan_data = {
    "DateSold": DateSold,
    "Staff_name": current_staff,
    "CustomerName": CustomerName,
    "CustomerPhone": CustomerPhone,
    "Location": Location,
    "BusinessName": BusinessName,
    "LoanAmount": LoanAmount
}
    insert_loan(loan_data)
    

