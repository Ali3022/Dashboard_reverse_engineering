```python
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['analytics']

kpis = ['Sessions', 'Page Views', 'Users', 'Website Visits']
kpis_dict = {kpi: dbc.Col(dbc.Card([
    dbc.CardHeader(kpi),
    dbc.CardBody(
        [
            html.H4(id=f"{kpi}-value", className="card-title"),
            html.P(id=f"{kpi}-change", className="card-text"),
        ]
    ),
], color="light")) for kpi in kpis}

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Website Analytics"), width={'size': 6, 'offset': 3}), className="mb-4 mt-4"),
    dbc.Row([kpis_dict[kpi] for kpi in kpis]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='date-range', options=[{'label': 'Last 7 days', 'value': '7'},
                                                        {'label': 'Last 30 days', 'value': '30'},
                                                        {'label': 'Last 90 days', 'value': '90'}], value='30'),
                width=4, className="mb-4"),
        dbc.Col(dcc.Dropdown(id='services', options=[{'label': 'Service 1', 'value': '1'},
                                                      {'label': 'Service 2', 'value': '2'},
                                                      {'label': 'Service 3', 'value': '3'}], value='1'),
                width=4, className="mb-4"),
        dbc.Col(dcc.Dropdown(id='posts', options=[{'label': 'Post 1', 'value': '1'},
                                                  {'label': 'Post 2', 'value': '2'},
                                                  {'label': 'Post 3', 'value': '3'}], value='1'),
                width=4, className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='line-chart'), width=12, className="mb-4"),
        dbc.Col(dcc.Graph(id='bar-chart'), width=12, className="mb-4"),
    ])
], fluid=True)


@app.callback(
    Output('line-chart', 'figure'),
    Output('bar-chart', 'figure'),
    *[Output(f"{kpi}-value", 'children') for kpi in kpis],
    *[Output(f"{kpi}-change", 'children') for kpi in kpis],
    Input('date-range', 'value'),
    Input('services', 'value'),
    Input('posts', 'value')
)
def update_metrics(date_range, services, posts):
    line_chart = go.Figure()
    bar_chart = go.Figure()

    for kpi in kpis:
        current_value = db[kpi].find_one(sort=[('_id', -1)])['value']
        previous_value = db[kpi].find_one(sort=[('_id', -2)])['value']
        percent_change = ((current_value - previous_value) / previous_value) * 100

        yield line_chart, bar_chart, current_value, f'{percent_change:.2f}%'

    line_chart.update_layout(transition_duration=500)
    bar_chart.update_layout(transition_duration=500)


if __name__ == '__main__':
    app.run_server(debug=True)
```