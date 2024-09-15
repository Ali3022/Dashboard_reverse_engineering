import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from flask_pymongo import PyMongo
import plotly.graph_objects as go
import pandas as pd

# Initialize Flask server and configure MongoDB URI
server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/website_analytics?retryWrites=true&w=majority"
mongo = PyMongo(server)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# App layout
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Update every 60 seconds
        n_intervals=0
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Sessions", className="card-title"),
                    html.P(id="sessions", className="card-text"),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Page Views", className="card-title"),
                    html.P(id="page_views", className="card-text"),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Users", className="card-title"),
                    html.P(id="users", className="card-text"),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Website Visits", className="card-title"),
                    html.P(id="website_visits", className="card-text"),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='page_views_chart'),
            dcc.Graph(id='web_traffic_chart')
        ], width=6),
    ]),
])

# Callback to update metrics and charts
@app.callback(
    [Output('sessions', 'children'),
     Output('page_views', 'children'),
     Output('users', 'children'),
     Output('website_visits', 'children'),
     Output('page_views_chart', 'figure'),
     Output('web_traffic_chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n):
    # Fetch data from KPIBoxes collection
    kpi_data = mongo.db.KPIBoxes.find_one()
    #print(f"kpi_data: {kpi_data}")  # Debug print

    sessions = kpi_data.get("sessions", "N/A") if kpi_data else "N/A"
    page_views = kpi_data.get("page_views", "N/A") if kpi_data else "N/A"
    users = kpi_data.get("users", "N/A") if kpi_data else "N/A"
    website_visits = kpi_data.get("website_visits", "N/A") if kpi_data else "N/A"

    # Fetch page views data for the chart from GraphsAndCharts collection
    page_views_data = pd.DataFrame(list(mongo.db.GraphsAndCharts.find()))
    #print(f"page_views_data: {page_views_data}")  # Debug print
    page_views_chart = go.Figure()

    # Extract the 'date' and 'sessions' fields from the 'page_views_chart' column
    if not page_views_data.empty:
        try:
            page_views_data_expanded = pd.json_normalize(page_views_data['page_views_chart'])  # Extract the JSON data
            #print(page_views_data_expanded)  # Debug print to verify extracted data
            page_views_chart.add_trace(go.Scatter(x=page_views_data_expanded['date'], y=page_views_data_expanded['sessions'], mode='lines'))
        except KeyError:
            pass
            #print("Error: 'date' and 'sessions' fields not found in page_views_data")

    # Fetch web traffic data for the chart from GraphsAndCharts collection
    web_traffic_data = pd.DataFrame(list(mongo.db.GraphsAndCharts.find()))
    #print(f"web_traffic_data: {web_traffic_data}")  # Debug print
    web_traffic_chart = go.Figure()

    # Extract the 'date', 'sessions', and 'page_views' fields from the 'page_views_chart' column
    if not web_traffic_data.empty:
        try:
            web_traffic_data_expanded = pd.json_normalize(web_traffic_data['page_views_chart'])  # Extract the JSON data
            #print(web_traffic_data_expanded)  # Debug print to verify extracted data
            web_traffic_chart.add_trace(go.Bar(x=web_traffic_data_expanded['date'], y=web_traffic_data_expanded['sessions'], name='Sessions'))
            web_traffic_chart.add_trace(go.Scatter(x=web_traffic_data_expanded['date'], y=web_traffic_data_expanded['page_views'], name='Page Views'))
        except KeyError:
            pass
            #print("Error: 'date', 'sessions', and 'page_views' fields not found in web_traffic_data")

    # Return the updated values and charts
    return sessions, page_views, users, website_visits, page_views_chart, web_traffic_chart

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
