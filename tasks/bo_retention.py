import streamlit as st
from data.loader import load_businesses_users, load_data, get_retention_task

users = load_businesses_users()["users"]
business_df = load_businesses_users()["business"]
bo_retention_today = load_data()["bo_retention_today"]

st.title("BO Retention Today")
st.write("Declined Top Businesses Today")


merged_df = get_retention_task(users, business_df, bo_retention_today)

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