import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=43200)
def load_loans():
    return conn.read(worksheet="loans")

@st.cache_data(ttl=86400)
def load_users():
    return conn.read(worksheet="users")

loans_df = load_loans()
users_df = load_users()

st.title("🎴 Loans Management")

st.write("This is the Loans management tool. Here you can manage your loans.")

def insert_cards(loan_data):
    # Implementation for inserting cards into google sheet
    new_loan_df = pd.DataFrame([loan_data])
    updated_df = pd.concat([loans_df, new_loan_df], ignore_index=True)
    conn.update(worksheet="loans", data=updated_df)
    st.success("Loan added successfully!")

with st.form("add_loan_form"):
    DateSold = st.date_input("Date Sold")
    Staff_name = st.selectbox("Staff Name", options=users_df["Staff_name"].tolist())
    CustomerName = st.text_input("Customer Name")
    CustomerPhone = st.text_input("Customer Phone Number")
    Location = st.text_input("Location")
    BusinessName = st.text_input("Business Name")
    LoanAmount = st.text_input("Amount of the loan")

    submitted = st.form_submit_button("Add Loan")

if submitted:
    loan_data = {
    "DateSold": DateSold,
    "Staff_name": Staff_name,
    "CustomerName": CustomerName,
    "CustomerPhone": CustomerPhone,
    "Location": Location,
    "BusinessName": BusinessName,
    "LoanAmount": LoanAmount
}
    insert_cards(loan_data)
    

