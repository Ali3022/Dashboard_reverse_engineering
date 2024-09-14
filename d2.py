import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objs as go
import requests

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Add custom CSS for fonts, box sizes, and text alignment
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Web Analytics Dashboard</title>
        {%css%}
        {%favicon%}
        {%scripts%}
        <style>
            @import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');
            body {
                background: linear-gradient(to bottom, #f8ccd7, #f2a3b5);
                margin: 0;
                padding: 0;
                font-family: 'Open Sans', sans-serif;
            }
            .container {
                padding: 20px;
            }
            h1 {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                text-align: center;
                padding-bottom: 20px;
            }
            .metric-box {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                text-align: center;
                font-weight: bold;
                font-size: 24px;
                color: #333333;
                height: 150px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .card {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                height: 300px; /* Fixed height for all cards */
                display: flex;
                flex-direction: column;
                justify-content: center; /* Center content vertically */
                align-items: center;
                overflow: hidden; /* Hide overflow if content exceeds */
                text-align: center; /* Center text horizontally */
            }
            .card h4 {
                font-size: 22px;
                margin-bottom: 10px;
                margin-top: 10px; /* Ensures margin between header and chart */
                text-align: center;
            }
            /* Adjust the size of graphs to fit within the cards */
            .card .dash-graph {
                flex-grow: 1;
                width: 100%;
            }
            /* New classes for metric numbers and titles */
            .metric-number {
                font-size: 48px;
                font-weight: bold;
                margin: 0;
                color: #333333;
            }
            .metric-title {
                font-size: 18px;
                margin: 0;
                color: #666666;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Fetch data from API (replace these with real endpoints if available)
total_sessions = requests.get('http://localhost:5000/api/total_sessions').json()['total_sessions']
avg_bounce_rate = requests.get('http://localhost:5000/api/bounce_rate').json()['avg_bounce_rate']
goal_completion = requests.get('http://localhost:5000/api/goal_completion').json()['goal_completion']
goal_conversion_rate = requests.get('http://localhost:5000/api/goal_conversion_rate').json()['goal_conversion_rate']

# Traffic Source Breakdown (Pie Chart Data)
traffic_source_data = go.Figure(data=[
    go.Pie(labels=["Direct", "Social", "Referral", "Email", "Organic"], 
           values=[50, 18, 7, 5, 20], hole=.4)
])

# World Map for Traffic Sources
world_map_data = go.Figure(data=go.Scattergeo(
    lon=[-95.7129, -106.3468, 10.4515, 78.9629, 133.7751],  # Longitude points
    lat=[37.0902, 56.1304, 51.1657, 20.5937, -25.2744],     # Latitude points
    text=["USA", "Canada", "Germany", "India", "Australia"],
    mode='markers',
    marker=dict(size=[10, 8, 6, 4, 2], color="blue", opacity=0.7)
))
world_map_data.update_layout(title="Geographical Traffic Distribution", geo=dict(showland=True))

# Sessions vs Goals Line Chart
sessions_goals_line_chart = go.Figure(data=[
    go.Scatter(x=['Nov 1', 'Nov 7', 'Nov 15', 'Nov 23', 'Nov 30'], y=[1000, 2000, 1500, 2500, 3000],
               mode='lines', name='Sessions', line=dict(color='#96d8f2', width=3)),
    go.Scatter(x=['Nov 1', 'Nov 7', 'Nov 15', 'Nov 23', 'Nov 30'], y=[500, 1000, 750, 1250, 1500], 
               mode='lines', name='Goals', line=dict(color='#e088b7', width=3, dash='dash'))
])
sessions_goals_line_chart.update_layout(title="Sessions and Goals Over Time", xaxis_title='Date', yaxis_title='Count')

# Placeholder data for Goal Completion chart and Goal Value chart (similar to reference)
goal_completion_chart = go.Figure(data=[
    go.Scatter(x=['Nov 1', 'Nov 7', 'Nov 15', 'Nov 23', 'Nov 30'], y=[20, 40, 35, 45, 50], mode='lines', name='Goal Completion', line=dict(color='#96d8f2', width=2))
])
goal_value_chart = go.Figure(data=[
    go.Scatter(x=['Nov 1', 'Nov 7', 'Nov 15', 'Nov 23', 'Nov 30'], y=[200, 300, 350, 400, 450], mode='lines', name='Goal Value', line=dict(color='#e088b7', width=2))
])

# Adjust graph sizes to fit within the cards
for fig in [traffic_source_data, world_map_data, sessions_goals_line_chart, goal_completion_chart, goal_value_chart]:
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=220  # Adjust height to fit within card
    )

# Layout of the dashboard
app.layout = dbc.Container([
    # Title
    html.H1('Web Analytics Dashboard'), 
    
    # Row 1: Top Metrics
    dbc.Row([
        dbc.Col(html.Div([
            html.Div(f"Total Sessions: {total_sessions}", className="metric-box"),
        ]), width=4),
        
        dbc.Col(html.Div([
            html.Div("Users: 51,790", className="metric-box"),
        ]), width=4),
        
        dbc.Col(html.Div([
            html.Div(f"Bounce Rate: {avg_bounce_rate:.2f}%", className="metric-box"),
        ]), width=4),
    ], justify="around", align="center", style={'margin-bottom': '30px'}),  
    
    # Row 2: Traffic Source Pie Chart and World Map
    dbc.Row([
        dbc.Col(html.Div([
            dcc.Graph(figure=traffic_source_data, className="dash-graph")
        ], className="card"), width=6),
        dbc.Col(html.Div([
            dcc.Graph(figure=world_map_data, className="dash-graph")
        ], className="card"), width=6),
    ], style={'margin-bottom': '30px'}),
    
    # Row 3: Sessions vs Goals Line Chart
    dbc.Row([
        dbc.Col(html.Div([
            dcc.Graph(figure=sessions_goals_line_chart, className="dash-graph")
        ], className="card"), width=12),
    ], style={'margin-bottom': '30px'}),
    
    # Row 4: Goal Completion, Goal Value, and Conversion Rate Metrics with Charts
    dbc.Row([
        dbc.Col(html.Div([
            html.H4(f"Goal Completion: {goal_completion}"),
            dcc.Graph(figure=goal_completion_chart, className="dash-graph")
        ], className="card"), width=4),
        
        dbc.Col(html.Div([
            html.H4("Goal Value: $352"),
            dcc.Graph(figure=goal_value_chart, className="dash-graph")
        ], className="card"), width=4),
        
        dbc.Col(html.Div([
            html.H1(f"{goal_conversion_rate:.2f}%", className="metric-number"),
            html.P("Goal Conversion Rate", className="metric-title")
        ], className="card"), width=4),
    ], style={'margin-bottom': '30px'}),
    
    # Row 5: Previous Period Metrics
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("67,730", className="metric-number"),
            html.P("Total Sessions (2.1% increase)", className="metric-title")
        ], className="card"), width=4),
        
        dbc.Col(html.Div([
            html.H1("51,790", className="metric-number"),
            html.P("Users (1.7% increase)", className="metric-title")
        ], className="card"), width=4),
        
        dbc.Col(html.Div([
            html.H1("47%", className="metric-number"),
            html.P("Bounce Rate (15% improvement)", className="metric-title")
        ], className="card"), width=4),
    ])
], fluid=True)

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

