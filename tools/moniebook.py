import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from data.loader import load_products, load_businesses_users

conn = st.connection("gsheets", type=GSheetsConnection)

moniebook_df = load_products()["moniebook"]
users_df = load_businesses_users()["users"]
current_staff = st.session_state.get("staff_name")

st.title("🎴 Moniebook Management")

st.write("This is the Moniebook management tool. Here you can manage your moniebooks.")

def insert_moniebook(mb_data):
    # Implementation for inserting moniebooks into google sheet
    new_mb_df = pd.DataFrame([mb_data])
    updated_df = pd.concat([moniebook_df, new_mb_df], ignore_index=True)
    conn.update(worksheet="moniebook", data=updated_df)
    st.success("Moniebook added successfully!")

with st.form("add_moniebook_form"):
    DateSold = st.date_input("Date Sold")
    st.text_input("Staff Name", value=current_staff, disabled=True)
    CustomerName = st.text_input("Customer Name")
    CustomerPhone = st.text_input("Customer Phone Number")
    Location = st.text_input("Location")
    BusinessName = st.text_input("Business Name")
    BusinessType = st.text_input("Business Type")

    submitted = st.form_submit_button("Add Moniebook")

if submitted:
    mb_data = {
    "DateSold": DateSold,
    "Staff_name": current_staff,
    "CustomerName": CustomerName,
    "CustomerPhone": CustomerPhone,
    "Location": Location,
    "BusinessName": BusinessName,
    "BusinessType": BusinessType
}
    insert_moniebook(mb_data)



