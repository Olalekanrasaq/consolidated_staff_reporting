import streamlit as st
from streamlit_gsheets import GSheetsConnection
from data.loader import load_assigned_tasks, load_businesses_users, load_data, load_products
from data.loader import get_ntt_task, get_retention_task, get_ta_task

business_df = load_businesses_users()["business"]
users_df = load_businesses_users()["users"]

@st.cache_data
def update_ta_tasks():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_transc_today = load_data()["df_transc_today"]
    ntt_today = load_data()["df_ntt_today"]
    ta_tasks_df = get_ta_task(users_df, business_df, df_transc_today, ntt_today)
    conn.update(worksheet="assigned_ta_task", data=ta_tasks_df)

@st.cache_data
def update_retention_tasks():
    conn = st.connection("gsheets", type=GSheetsConnection)
    bo_retention_today = load_data()["bo_retention_today"]
    retention_tasks_df = get_retention_task(users_df, business_df, bo_retention_today)
    conn.update(worksheet="assigned_retention_task", data=retention_tasks_df)

@st.cache_data
def update_ntt_tasks():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_ntt_today = load_data()["df_ntt_today"]
    ntt_tasks_df = get_ntt_task(users_df, business_df, df_ntt_today)
    conn.update(worksheet="assigned_ntt_task", data=ntt_tasks_df)

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

secret_code = st.text_input("Enter admin secret code:", type="password")

if st.button("Submit"):
    if secret_code != "123@4":
        st.error("Unauthorized access.")
    else:
        st.session_state.is_admin = True
        st.rerun()

if st.session_state.is_admin:
    st.title("🛠️ Admin Panel")

    if st.button("Refresh Data from Google Sheets"):
        st.cache_data.clear()
        st.toast("Cache cleared! Reloading data 🔄", icon="✅")
        st.rerun()

    if st.button("Load google sheets data into cache"):
        load_data()
        load_businesses_users()
        load_assigned_tasks()
        load_products()
        st.success("Data loaded into cache successfully!")

    if st.button("Update TA Tasks"):
        update_ta_tasks()
        st.success("TA Tasks updated successfully!")

    if st.button("Update Retention Tasks"):
        update_retention_tasks()
        st.success("Retention Tasks updated successfully!")

    if st.button("Update NTT Tasks"):
        update_ntt_tasks()
        st.success("NTT Tasks updated successfully!")

