import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# URL of the Flask API
API_URL = "http://127.0.0.1:5000"

# Function to fetch data from API
def get_total_sessions():
    response = requests.get(f"{API_URL}/total_sessions")
    if response.status_code == 200:
        return response.json().get("total_sessions", 0)
    else:
        return 0

def get_users():
    # Replace this with actual API call for users
    return 51790  # Placeholder for now

def get_bounce_rate():
    response = requests.get(f"{API_URL}/bounce_rate")
    if response.status_code == 200:
        return response.json().get("bounce_rate", 0)
    else:
        return 0

def get_goal_conversion_rate():
    response = requests.get(f"{API_URL}/goal_conversion_rate")
    if response.status_code == 200:
        return response.json().get("goal_conversion_rate", 0)
    else:
        return 0

def get_traffic_sources():
    response = requests.get(f"{API_URL}/traffic_sources")
    if response.status_code == 200:
        return response.json().get("traffic_sources", [])
    else:
        return []

def get_geographic_distribution():
    response = requests.get(f"{API_URL}/geographic_distribution")
    if response.status_code == 200:
        return response.json().get("geographic_distribution", [])
    else:
        return []

def get_goal_value():
    # Replace this with actual API call for goal value
    return 352  # Placeholder for now

def get_goal_completion():
    # Replace this with actual API call for goal completion
    return 109  # Placeholder for now

# Custom CSS to style the dashboard like the original
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f8cdda, #f67e7d);
    }
    .header {
        font-size: 32px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }
    .metric-container {
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.3);
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
    }
    .metric-header {
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    .metric-value {
        font-size: 36px;
        color: white;
    }
    .chart-container {
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        text-align: center;
    }
    .small-metric {
        color: white;
        font-size: 20px;
    }
    .small-metric-value {
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='header'>Web Analytics Dashboard</h1>", unsafe_allow_html=True)

# Metrics Layout (Total Sessions, Users, Bounce Rate, Goal Conversion Rate)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-header'>Total Sessions</div>", unsafe_allow_html=True)
    total_sessions = get_total_sessions()
    st.markdown(f"<div class='metric-value'>{total_sessions}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-header'>Users</div>", unsafe_allow_html=True)
    users = get_users()
    st.markdown(f"<div class='metric-value'>{users}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-header'>Bounce Rate</div>", unsafe_allow_html=True)
    bounce_rate = get_bounce_rate()
    st.markdown(f"<div class='metric-value'>{bounce_rate:.2f}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-header'>Goal Conversion Rate</div>", unsafe_allow_html=True)
    goal_conversion_rate = get_goal_conversion_rate()
    st.markdown(f"<div class='metric-value'>{goal_conversion_rate:.2f}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Traffic Sources - Pie Chart
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.header("Traffic Source Distribution")
traffic_sources = get_traffic_sources()

if isinstance(traffic_sources, list) and traffic_sources:
    df_traffic = pd.DataFrame(traffic_sources)
    fig = px.pie(df_traffic, values='count', names='source', title='Traffic Sources',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)
else:
    st.error("Error fetching traffic sources or no data available")
st.markdown("</div>", unsafe_allow_html=True)

# Geographic Distribution - Map
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.header("Geographic Distribution")
geo_distribution = get_geographic_distribution()

if isinstance(geo_distribution, list) and geo_distribution:
    df_geo = pd.DataFrame(geo_distribution)
    fig_geo = px.scatter_geo(df_geo, locations="location", size="count",
                             projection="natural earth", title="Traffic by Geography",
                             color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig_geo)
else:
    st.error("Error fetching geographic distribution or no data available")
st.markdown("</div>", unsafe_allow_html=True)

# Sessions and Goals Over Time - Line Chart
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.header("Sessions and Goals Over Time")
df_time = pd.DataFrame({
    "date": pd.date_range(start="2024-01-01", periods=30),
    "sessions": [1000 + i * 20 for i in range(30)],
    "goals": [300 + i * 10 for i in range(30)]
})
fig_time = px.line(df_time, x="date", y=["sessions", "goals"],
                   labels={"value": "Count", "variable": "Metric"},
                   title="Sessions and Goals Over Time")
fig_time.update_layout(legend=dict(orientation="h"))
st.plotly_chart(fig_time)
st.markdown("</div>", unsafe_allow_html=True)

# Previous Period Comparison
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric'>Previous Period Sessions</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric-value'>2.1% ⬆</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric'>Previous Period Users</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric-value'>1.7% ⬆</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric'>Previous Period Bounce Rate</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric-value'>15% ⬆</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Goal Value and Goal Completion
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    goal_completion = get_goal_completion()
    st.markdown(f"<div class='small-metric'>Goal Completion</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric-value'>{goal_completion}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    goal_value = get_goal_value()
    st.markdown(f"<div class='small-metric'>Goal Value</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-metric-value'>${goal_value}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

