import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Kajiado Election Dashboard",
    page_icon="🗳️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM STYLE
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
h1, h2, h3 {
    color: #0d1b2a;
}
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e6e6e6;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🗳️ Kajiado County 2022 Presidential Election Dashboard")
st.markdown("### DCS 808 Mercy Rotich Interactive Dashboard Project")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("kajiado_election_2022.csv")

df = load_data()

cands = ["Ruto", "Raila", "Wajackoyah", "Mwaure"]

# Winner Column
df["Winner"] = df[cands].idxmax(axis=1)

# Total Votes Column
df["Total Votes"] = df[cands].sum(axis=1)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")

selected = st.sidebar.multiselect(
    "Select Constituencies",
    options=df["Constituency"],
    default=list(df["Constituency"])
)

candidate_view = st.sidebar.selectbox(
    "Focus Candidate",
    ["All Candidates"] + cands
)

# ✅ Scatter plot configuration
st.sidebar.subheader("Scatter Plot Settings")

x_axis = st.sidebar.selectbox("Select X-axis", cands, index=0)
y_axis = st.sidebar.selectbox("Select Y-axis", cands, index=1)

filtered = df[df["Constituency"].isin(selected)]

# ---------------------------------------------------
# GLOBAL CALCULATIONS (FIXED)
# ---------------------------------------------------
total_votes = filtered[cands].sum().sum()

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("📌 Highest votes summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Votes", f"{int(total_votes):,}")
col2.metric("Leading Candidate", filtered[cands].sum().idxmax())
col3.metric("Highest Turnout",
            filtered.loc[filtered["Total Votes"].idxmax(), "Constituency"])
col4.metric("Constituencies", len(filtered))

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Analysis", "📄 Raw Data"])

# ---------------------------------------------------
# TAB 1 OVERVIEW
# ---------------------------------------------------
with tab1:

    colA, colB = st.columns(2)

    with colA:
        fig = px.bar(
            filtered,
            x="Constituency",
            y=cands,
            barmode="group",
            title="Votes by Constituency",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        totals = filtered[cands].sum().reset_index()
        totals.columns = ["Candidate", "Votes"]

        fig2 = px.pie(
            totals,
            names="Candidate",
            values="Votes",
            hole=0.45,
            title="County Vote Share"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# TAB 2 ANALYSIS
# ---------------------------------------------------
with tab2:

    colC, colD = st.columns(2)

    with colC:
        heat = px.imshow(
            filtered[cands],
            labels=dict(x="Candidate", y="Constituency", color="Votes"),
            x=cands,
            y=filtered["Constituency"],
            title="Vote Heatmap"
        )
        st.plotly_chart(heat, use_container_width=True)

    with colD:
        win_counts = filtered["Winner"].value_counts().reset_index()
        win_counts.columns = ["Candidate", "Wins"]

        fig3 = px.bar(
            win_counts,
            x="Candidate",
            y="Wins",
            color="Candidate",
            title="Constituency Wins"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ✅ Scatter Plot (NEW)
    st.subheader("📍 Candidate Vote Relationship")

    scatter = px.scatter(
        filtered,
        x=x_axis,
        y=y_axis,
        size="Total Votes",
        color="Winner",
        hover_name="Constituency",
        title=f"{x_axis} vs {y_axis} Votes",
        size_max=40
    )

    st.plotly_chart(scatter, use_container_width=True)

    # Gauge Chart
    st.subheader("Leading Candidate Performance")

    lead_votes = filtered[cands].sum().max()
    percent = (lead_votes / total_votes) * 100

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percent,
        title={'text': "Lead Vote Share %"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(gauge, use_container_width=True)

# ---------------------------------------------------
# TAB 3 DATA
# ---------------------------------------------------
with tab3:

    st.subheader("Detailed Election Results")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV",
        csv,
        "kajiado_results.csv",
        "text/csv"
    )

# ---------------------------------------------------
# INSIGHTS SECTION
# ---------------------------------------------------
st.subheader("🔍 Insights")

leader = filtered[cands].sum().idxmax()
highest = filtered.loc[filtered["Total Votes"].idxmax(), "Constituency"]

st.write(f"✅ **{leader}** is currently leading in selected constituencies.")
st.write(f"✅ **{highest}** recorded the highest voter turnout.")
st.write(f"✅ Total valid votes counted: **{int(total_votes):,}**")


   
