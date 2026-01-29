import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=43200)
def load_cards():
    return conn.read(worksheet="cards")

@st.cache_data(ttl=86400)
def load_users():
    return conn.read(worksheet="users")

cards_df = load_cards()
users_df = load_users()
current_staff = st.session_state.get("staff_name")

st.title("🎴 Cards Management")

st.write("This is the Cards management tool. Here you can manage your cards.")

def insert_cards(card_data):
    # Implementation for inserting cards into google sheet
    new_card_df = pd.DataFrame([card_data])
    updated_df = pd.concat([cards_df, new_card_df], ignore_index=True)
    conn.update(worksheet="cards", data=updated_df)
    st.success("Card added successfully!")

with st.form("add_card_form"):
    DateSold = st.date_input("Date Sold")
    st.text_input("Staff Name", value=current_staff, disabled=True)
    CustomerName = st.text_input("Customer Name")
    CustomerPhone = st.text_input("Customer Phone Number")
    CustomerAccount = st.text_input("Customer Account Number")
    CardNumber = st.text_input("Card Number")

    submitted = st.form_submit_button("Add Card")


if submitted:
    card_data = {
        "DateSold": DateSold,
        "Staff_name": current_staff,
        "CustomerName": CustomerName,
        "CustomerPhone": CustomerPhone,
        "CustomerAccount": CustomerAccount,
        "CardNumber": CardNumber,
    }
    insert_cards(card_data)


