import streamlit as st
from data.loader import load_businesses_users, load_data, get_ntt_task

users = load_businesses_users()["users"]
business_df = load_businesses_users()["business"]
df_ntt_today = load_data()["df_ntt_today"]

st.title("Non-Transacting Terminals Today")
st.write("Businesses with Non-Transacting Terminals Today")

merged_df = get_ntt_task(users, business_df, df_ntt_today)

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