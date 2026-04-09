import streamlit as st
import pandas as pd
from data.loader import load_products, load_businesses_users, load_data, get_loan_tasks
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

users = load_businesses_users()["users"]
business_df = load_businesses_users()["business"]
df_transc = load_data()["df_transc_today"]

st.title("Loans Target")
st.write("Businesses targeted for loans")

merged_df = get_loan_tasks(users, business_df, df_transc_today)

staff_dfs = {
    staff: df.reset_index(drop=True)
    for staff, df in merged_df.groupby("Assigned_staff")
}

selected_staff = st.selectbox("Select Staff", staff_dfs.keys())

st.dataframe(
    staff_dfs[selected_staff],
    hide_index=True,
    use_container_width=True
)
