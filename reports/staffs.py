import streamlit as st
import pandas as pd
from data.loader import load_data, load_businesses_users, load_assigned_tasks, load_products
from functools import reduce
from streamlit_gsheets import GSheetsConnection

assigned_ta_tasks = load_assigned_tasks()["assigned_ta_tasks"]
assigned_retention_tasks = load_assigned_tasks()["assigned_retention_tasks"]
assigned_ntt_tasks = load_assigned_tasks()["assigned_ntt_tasks"]
users_df = load_businesses_users()["users"]
loans = load_products()["loans"]
moniebooks = load_products()["moniebook"]
terminals = load_products()["terminals"]
cards = load_products()["cards"]
df_transc_today = load_data()["df_transc_today"]
df_ntt_today = load_data()["df_ntt_today"]
bo_retention_today = load_data()["bo_retention_today"]
cr_metrics_df = load_data()["cr_metrics"]



st.title("📊 Staff Performance Dashboard")

def count_by_staff(df, staff_col="Staff_name", count_col_name="count"):
    return (
        df
        .groupby(staff_col)
        .size()
        .reset_index(name=count_col_name)
    )

# determine if a task assigned per staff is no more in today not meeting target data
def get_completed_ta_tasks(assigned_tasks, df_transc_today):
    not_meeting_target = df_transc_today[df_transc_today["target_met"] == False]
    assigned_tasks["business_key"] = assigned_tasks["Business Name"].str.lower().str.strip()
    not_meeting_target["business_key"] = not_meeting_target["Business Name"].str.lower().str.strip()
    merged_df = assigned_tasks.merge(
        not_meeting_target[["business_key"]],
        on="business_key",
        how="inner"
    ).drop(columns=["business_key", "days_last_transact", "Phone"]
           ).drop_duplicates(subset=['Business Name']).rename(columns={"Assigned_staff": "Staff_name"})
    return merged_df

# determine if a task assigned per staff is no more in today not meeting target data
def get_completed_ntt_tasks(assigned_tasks, df):
    assigned_tasks["business_key"] = assigned_tasks["Business Name"].str.lower().str.strip()
    df["business_key"] = df["Business Name"].str.lower().str.strip()
    merged_df = assigned_tasks.merge(
        df[["business_key"]],
        on="business_key",
        how="inner"
    ).drop(columns=["business_key", "days_last_transact", "Phone"]
           ).drop_duplicates(subset=['Business Name']).rename(columns={"Assigned_staff": "Staff_name"})
    return merged_df

def get_completed_ret_tasks(assigned_tasks, df):
    assigned_tasks["business_key"] = assigned_tasks["Business Name"].str.lower().str.strip()
    df["business_key"] = df["Business Name"].str.lower().str.strip()
    merged_df = assigned_tasks.merge(
        df[["business_key"]],
        on="business_key",
        how="inner"
    ).drop(columns=["business_key", "Phone"]
           ).drop_duplicates(subset=['Business Name']).rename(columns={"Assigned_staff": "Staff_name"})
    return merged_df

completed_ta_tasks = get_completed_ta_tasks(assigned_ta_tasks, df_transc_today)
completed_retention_tasks = get_completed_ret_tasks(assigned_retention_tasks, bo_retention_today)
completed_ntt_tasks = get_completed_ntt_tasks(assigned_ntt_tasks, df_ntt_today)
    

loans_count = count_by_staff(loans, count_col_name="Loans")
moniebooks_count = count_by_staff(moniebooks, count_col_name="Moniebooks")
terminals_count = count_by_staff(terminals, count_col_name="Terminals")
cards_count = count_by_staff(cards, count_col_name="Cards")
comp_ta_tasks_count = count_by_staff(completed_ta_tasks, count_col_name="Completed_TA_Tasks")
comp_ret_tasks_count = count_by_staff(completed_retention_tasks, count_col_name="Completed_Retention_Tasks")
comp_ntt_tasks_count = count_by_staff(completed_ntt_tasks, count_col_name="Completed_NTT_Tasks")
ta_tasks_count = count_by_staff(assigned_ta_tasks, staff_col="Assigned_staff", count_col_name="Assigned_Tasks")
ta_tasks_count.rename(columns={"Assigned_staff": "Staff_name"}, inplace=True)
ret_tasks_count = count_by_staff(assigned_retention_tasks, staff_col="Assigned_staff", count_col_name="Assigned_Retention_Tasks")
ret_tasks_count.rename(columns={"Assigned_staff": "Staff_name"}, inplace=True)
ntt_tasks_count = count_by_staff(assigned_ntt_tasks, staff_col="Assigned_staff", count_col_name="Assigned_NTT_Tasks")
ntt_tasks_count.rename(columns={"Assigned_staff": "Staff_name"}, inplace=True)

dfs_to_merge = [loans_count, moniebooks_count, terminals_count, cards_count, comp_ta_tasks_count, 
                comp_ret_tasks_count, comp_ntt_tasks_count, ta_tasks_count, ret_tasks_count, ntt_tasks_count]

summarized_df = reduce(
    lambda left, right: pd.merge(left, right, on="Staff_name", how="outer"),
    dfs_to_merge
).fillna(0)

summarized_df["TA_CR"] = (
    (summarized_df["Assigned_Tasks"] - summarized_df["Completed_TA_Tasks"])/summarized_df["Assigned_Tasks"]) * 100
summarized_df["Retention_CR"] = (
    (summarized_df["Assigned_Retention_Tasks"]- summarized_df["Completed_Retention_Tasks"]) / summarized_df["Assigned_Retention_Tasks"]) * 100
summarized_df["NTT_CR"] = (
    (summarized_df["Assigned_NTT_Tasks"] - summarized_df["Completed_NTT_Tasks"]) /summarized_df["Assigned_NTT_Tasks"]) * 100

# remove okunlola francis from summarized df
summarized_df = summarized_df[summarized_df["Staff_name"] != "Okunlola Francis"]

cols = ["Staff_name", "Loans", "Moniebooks", "Terminals", "Cards", "TA_CR", "Retention_CR", "NTT_CR"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.metric(":material/sell: Total Loans", f"{len(loans)}")
with col2:
    with st.container(border=True):
        st.metric(":material/computer: Total Moniebooks", f"{len(moniebooks)}")
with col3:
    with st.container(border=True):
        st.metric(":material/sell: Total Terminals", f"{len(terminals)}")
with col4:
    with st.container(border=True):
        st.metric(":material/card_giftcard: Total Cards", f"{len(cards)}")

st.caption(":material/addchart: :green[Staff Performance Summary]")
st.dataframe(summarized_df[cols], 
             column_config={
                     "TA_CR": st.column_config.NumberColumn(
                         "TA_CR (%)",
                         format="%.0f"
                     ),
                     "Retention_CR": st.column_config.NumberColumn(
                         "Ret_CR (%)",
                         format="%.0f"
                     ),
                     "NTT_CR": st.column_config.NumberColumn(
                         "NTT_CR (%)",
                         format="%.0f"
                     )
                 },
             hide_index=True, use_container_width=True)

# get staffs scores based on summarized df
count_metrics = ["Loans", "Moniebooks", "Terminals", "Cards"]
count_metrics_data = ["Staff_name", "Loans", "Moniebooks", "Terminals", "Cards"]

df_pct = summarized_df.copy()

for col in count_metrics:
    total = summarized_df[col].sum()
    if total > 0:
        df_pct[col] = (summarized_df[col] / total) * 100
    else:
        df_pct[col] = 0

cr_metrics = ["TA_CR", "Retention_CR", "NTT_CR"]
cr_metrics_data = ["Staff_name", "TA_CR", "Retention_CR", "NTT_CR"]

@st.cache_data
def update_cr_metrics():
    conn = st.connection("gsheets", type=GSheetsConnection)
    new_df = summarized_df[cr_metrics_data]
    combined_metrics_df = pd.concat([cr_metrics_df, new_df], ignore_index=True)
    agg_metrics = combined_metrics_df.groupby('Staff_name', as_index=False).mean()
    conn.update(worksheet="cr_metrics", data=agg_metrics)
    return agg_metrics

agg_metrics = update_cr_metrics()

df_pct_merged = df_pct[count_metrics_data].merge(
    agg_metrics,
    on='Staff_name',
    how='inner'
)

score_columns = count_metrics + cr_metrics

df_pct_merged["Total_Score"] = df_pct_merged[score_columns].sum(axis=1)
# final_df = df_pct_merged[["Staff_name"] + score_columns + ["Total_Score"]]
final_df = df_pct_merged.sort_values(by="Total_Score", ascending=False).reset_index(drop=True)

with st.expander("Staff Performance Point Ranking (Percentage)"):
    st.dataframe(final_df, 
                 column_config={
                     "TA_CR": st.column_config.NumberColumn(
                         "TA_CR (%)",
                         format="%.0f"
                     ),
                     "Retention_CR": st.column_config.NumberColumn(
                         "Ret_CR (%)",
                         format="%.0f"
                     ),
                     "NTT_CR": st.column_config.NumberColumn(
                         "NTT_CR (%)",
                         format="%.0f"
                     ),
                     "Total_Score": st.column_config.NumberColumn(
                         "Total Score",
                         format="%.0f"
                     )
                 },
                 hide_index=True, use_container_width=True)
