import streamlit as st
from data.loader import load_data, load_businesses_users, get_ta_task

users = load_businesses_users()["users"]
business_df = load_businesses_users()["business"]
agg_data = load_data()["agg_data"]

st.title("Terminal Activity")
st.write("Businesses with cummulative payment less than weekly target")

merged_df = get_ta_task(users, business_df, agg_data)

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
