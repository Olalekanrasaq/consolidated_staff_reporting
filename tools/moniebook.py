import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=43200)
def load_moniebook():
    return conn.read(worksheet="moniebook")

@st.cache_data(ttl=86400)
def load_users():
    return conn.read(worksheet="users")

moniebook_df = load_moniebook()
users_df = load_users()

st.title("🎴 Moniebook Management")

st.write("This is the Moniebook management tool. Here you can manage your moniebooks.")

def insert_cards(mb_data):
    # Implementation for inserting cards into google sheet
    new_mb_df = pd.DataFrame([mb_data])
    updated_df = pd.concat([moniebook_df, new_mb_df], ignore_index=True)
    conn.update(worksheet="moniebook", data=updated_df)
    st.success("Moniebook added successfully!")

with st.form("add_moniebook_form"):
    DateSold = st.date_input("Date Sold")
    Staff_name = st.selectbox("Staff Name", options=users_df["Staff_name"].tolist())
    CustomerName = st.text_input("Customer Name")
    CustomerPhone = st.text_input("Customer Phone Number")
    Location = st.text_input("Location")
    BusinessName = st.text_input("Business Name")
    BusinessType = st.text_input("Business Type")

    submitted = st.form_submit_button("Add Moniebook")

if submitted:
    mb_data = {
    "DateSold": DateSold,
    "Staff_name": Staff_name,
    "CustomerName": CustomerName,
    "CustomerPhone": CustomerPhone,
    "Location": Location,
    "BusinessName": BusinessName,
    "BusinessType": BusinessType
}
    insert_cards(mb_data)



