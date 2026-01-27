import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df_transc_today = conn.read(worksheet="weekly_transc_today", ttl=43200)
df_ntt_today = conn.read(worksheet="ntt_today", ttl=43200)
df_transc_yest = conn.read(worksheet="weekly_transc_yest", ttl=43200)
df_ntt_yest = conn.read(worksheet="ntt_yesterday", ttl=43200)

st.title("📊 Dashboard")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.metric(":material/list_alt: Total Businesses", value=len(df_transc_today), 
                  delta=len(df_transc_today) - len(df_transc_yest))

with col2:
    with st.container(border=True):
        st.metric(":material/thumb_down_alt: Non-Transacting Terminals", value=len(df_ntt_today), 
                  delta=len(df_ntt_today) - len(df_ntt_yest))

_col1, _col2 = st.columns(2)
with _col1:
    with st.container(border=True):
        target_met_today = df_transc_today[df_transc_today["target_met"] == True]
        target_met_yest = df_transc_yest[df_transc_yest["target_met"] == True]
        st.metric(":material/upgrade: Businesses with Target Met", value=len(target_met_today), 
                  delta=len(target_met_today) - len(target_met_yest))

with _col2:
    with st.container(border=True):
        target_not_met_today = df_transc_today[df_transc_today["target_met"] == False]
        target_not_met_yest = df_transc_yest[df_transc_yest["target_met"] == False]
        st.metric(":material/south: Businesses without Target Met", value=len(target_not_met_today), 
                  delta=len(target_not_met_today) - len(target_not_met_yest))

tab_1, tab_2 = st.columns(2)
with tab_1:
    with st.container(border=True):
        st.caption("Top 5 Businesses by Weekly Payment Volume")
        top_5 = df_transc_today.nlargest(5, "payment_vol")
        st.dataframe(top_5[["Business Name", "payment_vol"]], hide_index=True)

with tab_2:
    with st.container(border=True):
        st.caption("Top 5 Businesses by Weekly Payment Value")
        top_5_value = df_transc_today.nlargest(5, "payment_value")
        st.dataframe(top_5_value[["Business Name", "payment_value"]], hide_index=True)