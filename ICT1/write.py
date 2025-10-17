import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Placement Dashboard", layout="wide")
st.title("🎓 Placement Data Analytics Dashboard")

# --- Load Data ---
df = pd.read_csv("data/NNRG_Placement_2018_2025.csv")
# --- Sidebar Filter ---
st.sidebar.header("📅 Filter by Year")
selected_year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df['Year'].unique().tolist()))

# --- Filter Data Based on Selection ---
if selected_year == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df['Year'] == selected_year]
    

# --- Summary Metrics ---
total_students = len(df)
total_branches = df['Branch'].nunique()
total_recruiters = df['Name of the Employer'].nunique()
total_placements = len(filtered_df)  # changes when year is selected

col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("🏫 Unique Branches", total_branches)
col3.metric("🏢 Total Recruiters", total_recruiters)
col4.metric("🎯 Total Placements", total_placements)

st.markdown("---")

# --- Top Branch of the Year ---
if selected_year != "All":
    st.subheader(f"🏆 Top Branch in {selected_year}")
    if not filtered_df.empty:
        top_branch = filtered_df['Branch'].value_counts().idxmax()
        top_branch_count = filtered_df['Branch'].value_counts().max()
        st.success(f"🎓 *{top_branch}* achieved the highest placements in {selected_year} with *{top_branch_count} students*.")
    else:
        st.warning("No data available for the selected year.")
    st.markdown("---")

# --- Side-by-side Graphs ---
col1, col2 = st.columns(2)

# 1️⃣ Year-wise placement bar chart (always from full data)
year_counts = df['Year'].value_counts().sort_index()
fig_bar = px.bar(
    x=year_counts.index,
    y=year_counts.values,
    color=year_counts.index,
    labels={'x': 'Year', 'y': 'Number of Placements'},
    title="📊 Year-wise Placement Count"
)
col1.plotly_chart(fig_bar, use_container_width=True)

# 2️⃣ Pie chart: Branch-wise distribution for selected year/all
branch_counts = filtered_df['Branch'].value_counts()
fig_pie = px.pie(
    names=branch_counts.index,
    values=branch_counts.values,
    title=f"🧭 Branch-wise Distribution ({'All Years' if selected_year == 'All' else selected_year})"
)
col2.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- Treemap: Branch-wise placement ---
if not filtered_df.empty:
    branch_counts_df = filtered_df['Branch'].value_counts().reset_index()
    branch_counts_df.columns = ['Branch', 'Count']
    fig_treemap = px.treemap(
        branch_counts_df,
        path=['Branch'],
        values='Count',
        title=f"🌳 Branch-wise Placement Treemap ({'All Years' if selected_year == 'All' else selected_year})"
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
else:
    st.info("No treemap available for the selected year.")

st.markdown("---")

# --- Recruiter-wise Placement Count ---
st.subheader(f"🏢 Top Recruiters ({'All Years' if selected_year == 'All' else selected_year})")
if not filtered_df.empty:
    recruiter_counts = filtered_df['Name of the Employer'].value_counts().reset_index()
    recruiter_counts.columns = ['Recruiter', 'Placements']
    fig_recruiters = px.bar(
        recruiter_counts.head(10),
        x='Recruiter',
        y='Placements',
        color='Placements',
        title=f"Top 10 Recruiters ({'All Years' if selected_year == 'All' else selected_year})"
    )
    st.plotly_chart(fig_recruiters, use_container_width=True)
else:
    st.info("No recruiter data available for the selected year.")

st.markdown("---")

# --- Full Data Table ---
st.subheader("📋 Full Placement Data")
st.dataframe(filtered_df, use_container_width=True)
