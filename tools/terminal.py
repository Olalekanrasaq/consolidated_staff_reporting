import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from data.loader import load_products, load_businesses_users

conn = st.connection("gsheets", type=GSheetsConnection)

terminals_df = load_products()["terminals"]
users_df = load_businesses_users()["users"]
current_staff = st.session_state.get("staff_name")

st.title("🎴 Terminal Management")

st.write("This is the Terminal management tool. Here you can manage your terminals.")

def insert_terminals(terminal_data):
    # Implementation for inserting terminals into google sheet
    new_terminal_df = pd.DataFrame([terminal_data])
    updated_df = pd.concat([terminals_df, new_terminal_df], ignore_index=True)
    conn.update(worksheet="terminals", data=updated_df)
    st.success("Terminal added successfully!")

with st.form("add_terminal_form"):
    DateSold = st.date_input("Date Sold")
    st.text_input("Staff Name", value=current_staff, disabled=True)
    CustomerName = st.text_input("Customer Name")
    CustomerDOB = st.date_input("Date of Birth")
    CustomerPhone = st.text_input("Customer Phone Number")
    BusinessName = st.text_input("Business Name")
    BusinessAddress = st.text_input("Business Address")
    TerminalSerialNumber = st.text_input("Terminal Serial Number")


    submitted = st.form_submit_button("Add Terminal")


if submitted:
    terminal_data = {
        "DateSold": DateSold,
        "Staff_name": current_staff,
        "CustomerName": CustomerName,
        "Date_of_Birth": CustomerDOB,
        "PhoneNumber": CustomerPhone,
        "BusinessName": BusinessName,
        "BusinessAddress": BusinessAddress,
        "TerminalSerialNumber": TerminalSerialNumber
    }
    insert_terminals(terminal_data)


