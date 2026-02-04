import streamlit as st
from data.loader import load_data

data = load_data()
df_transc_today = data["df_transc_today"]
df_ntt_today = data["df_ntt_today"]
df_transc_yest = data["df_transc_yest"]
df_ntt_yest = data["df_ntt_yest"]
bo_retention_today = data["bo_retention_today"]
bo_retention_yest = data["bo_retention_yest"]

st.title("📊 Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        target_not_met_today = df_transc_today[df_transc_today["target_met"] == False]
        target_not_met_yest = df_transc_yest[df_transc_yest["target_met"] == False]
        st.metric(":material/south: Businesses without Target Met", value=len(target_not_met_today), 
                  delta=len(target_not_met_today) - len(target_not_met_yest), delta_color="inverse")

with col2:
    with st.container(border=True):
        st.metric(":material/thumb_down_alt: Non-Transacting Terminals", value=len(df_ntt_today), 
                  delta=len(df_ntt_today) - len(df_ntt_yest), delta_color="inverse")

with col3:
    with st.container(border=True):
        st.metric(":material/thumb_down_alt: Declined Top Businesses", value=len(bo_retention_today), 
                  delta=len(bo_retention_today) - len(bo_retention_yest), delta_color="inverse")

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