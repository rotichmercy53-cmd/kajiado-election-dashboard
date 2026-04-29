import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kajiado Election Dashboard", layout="wide")

st.title("🗳️ Kajiado County 2022 Presidential Election Dashboard")
st.markdown("DCS 808 Interactive Dashboard Project")

@st.cache_data
def load_data():
    return pd.read_csv("kajiado_election_2022.csv")

df = load_data()

cands = ["Ruto","Raila","Wajackoyah","Mwaure"]
df["Winner"] = df[cands].idxmax(axis=1)

selected = st.sidebar.multiselect(
    "Select Constituency",
    options=df["Constituency"],
    default=list(df["Constituency"])
)

filtered = df[df["Constituency"].isin(selected)]

col1,col2,col3 = st.columns(3)
col1.metric("Total Votes", int(filtered[cands].sum().sum()))
col2.metric("Ruto Votes", int(filtered["Ruto"].sum()))
col3.metric("Raila Votes", int(filtered["Raila"].sum()))

fig = px.bar(filtered, x="Constituency", y=cands, barmode="group", title="Votes by Constituency")
st.plotly_chart(fig, use_container_width=True)

winner_counts = filtered["Winner"].value_counts().reset_index()
winner_counts.columns = ["Candidate","Wins"]

fig2 = px.pie(winner_counts, names="Candidate", values="Wins", title="Constituency Wins")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Detailed Results")
st.dataframe(filtered)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "kajiado_results.csv", "text/csv")
