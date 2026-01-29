import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from functools import reduce

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=86400)
def load_users():
    return conn.read(worksheet="users")
@st.cache_data(ttl=43200)
def load_loans():
    return conn.read(worksheet="loans")
@st.cache_data(ttl=43200)
def load_moniebook():
    return conn.read(worksheet="moniebook")
@st.cache_data(ttl=43200)
def load_terminals():
    return conn.read(worksheet="terminals")
@st.cache_data(ttl=43200)
def load_cards():
    return conn.read(worksheet="cards")

st.title("📊 Staff Performance Dashboard")

users_df = load_users()
loans = load_loans()
moniebooks = load_moniebook()
terminals = load_terminals()
cards = load_cards()

def count_by_staff(df, staff_col="Staff_name", count_col_name="count"):
    return (
        df
        .groupby(staff_col)
        .size()
        .reset_index(name=count_col_name)
    )

loans_count = count_by_staff(loans, count_col_name="Loans")
moniebooks_count = count_by_staff(moniebooks, count_col_name="Moniebooks")
terminals_count = count_by_staff(terminals, count_col_name="Terminals")
cards_count = count_by_staff(cards, count_col_name="Cards")

dfs_to_merge = [loans_count, moniebooks_count, terminals_count, cards_count]
summarized_df = reduce(
    lambda left, right: pd.merge(left, right, on="Staff_name", how="outer"),
    dfs_to_merge
).fillna(0)

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
st.dataframe(summarized_df, hide_index=True)