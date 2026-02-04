import streamlit as st
from streamlit_gsheets import GSheetsConnection
# from tasks.bo_retention import get_retention_task
# from tasks.ntt import get_ntt_task
# from tasks.terminal_activity import get_ta_task

@st.cache_data(ttl=86400)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return {
        "df_transc_today": conn.read(worksheet="weekly_transc_today"),
        "df_ntt_today": conn.read(worksheet="ntt_today"),
        "df_transc_yest": conn.read(worksheet="weekly_transc_yest"),
        "df_ntt_yest": conn.read(worksheet="ntt_yesterday"),
        "bo_retention_today": conn.read(worksheet="bo_retention_today"),
        "bo_retention_yest": conn.read(worksheet="bo_retention_yest")
    }

@st.cache_data(ttl=86400)
def load_products():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return {
        "loans": conn.read(worksheet="loans"),
        "moniebook": conn.read(worksheet="moniebook"),
        "terminals": conn.read(worksheet="terminals"),
        "cards": conn.read(worksheet="cards")
    }

@st.cache_data(ttl=86400)
def load_assigned_tasks():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return {
        "assigned_ta_tasks": conn.read(worksheet="assigned_ta_task"),
        "assigned_retention_tasks": conn.read(worksheet="assigned_retention_task"),
        "assigned_ntt_tasks": conn.read(worksheet="assigned_ntt_task")
    }

@st.cache_data
def load_businesses_users():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return {
        "business": conn.read(worksheet="businesses"),
        "users": conn.read(worksheet="users")
    }

@st.cache_data
def assign_staffs(df, staffs):
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df["Assigned_staff"] = [
        staffs[i % len(staffs)]
        for i in range(len(df))
    ]
    return df

@st.cache_data
def get_ta_task(users, business_df, df_transc_today):
    ta_data = df_transc_today[df_transc_today["target_met"] == False]
    target_not_met = ta_data[["Business Name", "days_last_transact"]]

    business_df["business_key"] = business_df["Business"].str.lower().str.strip()
    target_not_met["business_key"] = target_not_met["Business Name"].str.lower().str.strip()

    merged_df = target_not_met.merge(
        business_df[["business_key", "Phone"]],
        on="business_key",
        how="left"
    ).drop(columns="business_key").drop_duplicates(subset=['Business Name'])
    merged_df["Phone"] = merged_df["Phone"].astype("Int64").astype(str).str.zfill(11)
    staffs = users["Staff_name"].to_list()
    ta_tasks_df = assign_staffs(merged_df, staffs)
    return ta_tasks_df


@st.cache_data
def get_retention_task(users, business_df, bo_retention_today):
    business_df["business_key"] = business_df["Business"].str.lower().str.strip()
    bo_retention_today["business_key"] = bo_retention_today["Business Name"].str.lower().str.strip()

    merged_df = bo_retention_today.merge(
        business_df[["business_key", "Phone"]],
        on="business_key",
        how="left"
    ).drop(columns="business_key").drop_duplicates(subset=['Business Name'])
    merged_df["Phone"] = merged_df["Phone"].astype("Int64").astype(str).str.zfill(11)
    staffs = users["Staff_name"].to_list()
    ret_tasks_df = assign_staffs(merged_df, staffs)
    return ret_tasks_df

@st.cache_data
def get_ntt_task(users, business_df, df_ntt_today):
    business_df["business_key"] = business_df["Business"].str.lower().str.strip()
    df_ntt_today["business_key"] = df_ntt_today["Business Name"].str.lower().str.strip()

    merged_df = df_ntt_today.merge(
        business_df[["business_key", "Phone"]],
        on="business_key",
        how="left"
    ).drop(columns="business_key").drop_duplicates(subset=['Business Name'])
    merged_df["Phone"] = merged_df["Phone"].astype("Int64").astype(str).str.zfill(11)
    staffs = users["Staff_name"].to_list()
    ntt_tasks_df = assign_staffs(merged_df, staffs)
    return ntt_tasks_df