from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import requests
import plotly.graph_objs as go
import random

# Initialize Dash app
app = dash.Dash(__name__)

# Flask API base URL
API_BASE_URL = "http://127.0.0.1:5000/api"

# Global Styles
light_pink_bg = '#f3c2c2'
dark_pink_bg = '#e69e9e'
white_color = '#fff'
black_color = '#000'
grey_color = '#666'
accent_color = '#5F9EA0'

app.layout = html.Div(
    style={'backgroundColor': light_pink_bg, 'padding': '20px'},
    children=[
        # Header Section
        html.H1(
            "Web Analytics Dashboard",
            style={
                'textAlign': 'center', 
                'color': white_color, 
                'fontSize': '40px',
                'fontFamily': 'Arial',
                'fontWeight': 'bold',
                'backgroundColor': dark_pink_bg,
                'padding': '30px 15px',  
                'borderRadius': '10px',
                'marginBottom': '50px'
            }
        ),

        # KPI Boxes (Total Sessions, Users, Bounce Rate)
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '50px'},  
            children=[
                # Total Sessions Box
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='total-sessions', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Total Sessions", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                    ]
                ),
                # Users Box
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='total-users', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Users", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                    ]
                ),
                # Bounce Rate Box
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='bounce-rate', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Bounce Rate", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                    ]
                ),
            ]
        ),

        # Traffic Source Pie Chart and World Map Section
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '50px'},
            children=[
                # Pie Chart (Traffic Source)
                html.Div(
                    style={
                        'backgroundColor': white_color,
                        'padding': '20px',
                        'borderRadius': '10px',
                        'width': '47%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        dcc.Graph(id='traffic-source-pie-chart', style={'height': '500px'})  # Increased height for better visibility
                    ]
                ),
                # World Map (Traffic Source)
                html.Div(
                    style={
                        'backgroundColor': white_color,
                        'padding': '20px',
                        'borderRadius': '10px',
                        'width': '47%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        dcc.Graph(id='traffic-source-world-map', style={'height': '500px'})  # Increased height for better visibility
                    ]
                )
            ]
        ),

        # Dropdown and Main Line Chart
        html.Div(
            style={'marginBottom': '50px'},
            children=[
                dcc.Dropdown(
                    id='goal-dropdown',
                    options=[
                        {'label': 'Goal 1', 'value': 'Goal 1'},
                        {'label': 'Goal 2', 'value': 'Goal 2'},
                        {'label': 'Goal 3', 'value': 'Goal 3'},
                    ],
                    value='Goal 3',
                    style={'width': '50%', 'marginBottom': '20px'}
                ),
                dcc.Graph(id='main-line-chart')
            ]
        ),

        # Additional KPI Boxes (Goal Completion, Goal Value, Goal Conversion Rate) with Graphs
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '50px'},  
            children=[
                # Goal Completion Box with Graph
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='goal-completion', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Goal Completion", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                        dcc.Graph(id='goal-completion-graph', style={'height': '150px'})  # Mini graph for goal completion
                    ]
                ),
                # Goal Value Box with Graph
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='goal-value', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Goal Value", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                        dcc.Graph(id='goal-value-graph', style={'height': '150px'})  # Mini graph for goal value
                    ]
                ),
                # Goal Conversion Rate Box with Graph
                html.Div(
                    style={
                        'backgroundColor': '#f3e6e6',
                        'padding': '30px',
                        'borderRadius': '10px',
                        'width': '30%',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'
                    },
                    children=[
                        html.H2(id='goal-conversion-rate', style={'textAlign': 'center', 'fontSize': '40px', 'color': black_color, 'fontFamily': 'Arial'}),
                        html.P("Goal Conversion Rate", style={'textAlign': 'center', 'fontSize': '20px', 'color': grey_color, 'fontFamily': 'Arial'}),
                        dcc.Graph(id='goal-conversion-rate-graph', style={'height': '150px'})  # Mini graph for goal conversion rate
                    ]
                )
            ]
        )
    ]
)

# Generate random data for goal progress, value, and conversion rate to make graphs dynamic
def generate_random_data(num_points, base_value, variance):
    return [base_value + random.uniform(-variance, variance) for _ in range(num_points)]

# Callback to update the pie chart for traffic source
@app.callback(
    Output('traffic-source-pie-chart', 'figure'),
    [Input('goal-dropdown', 'value')]
)
def update_traffic_source_pie_chart(goal):
    labels = ['Direct', 'Organic Search', 'Paid Search', 'Email', 'Referral', 'Social']
    values = [50, 20, 15, 5, 5, 5]  # Example data
    figure = {
        'data': [go.Pie(labels=labels, values=values, hole=0.3)],
        'layout': go.Layout(title='Traffic Source', height=500, showlegend=True)
    }
    return figure

# Callback to update the world map chart for traffic source
@app.callback(
    Output('traffic-source-world-map', 'figure'),
    [Input('goal-dropdown', 'value')]
)
def update_traffic_source_world_map(goal):
    # Example data with countries and user counts
    locations = ['USA', 'CAN', 'DEU', 'IND', 'AUS', 'BRA']  # Using country codes for Scattergeo
    latitudes = [37.0902, 56.1304, 51.1657, 20.5937, -25.2744, -14.2350]
    longitudes = [-95.7129, -106.3468, 10.4515, 78.9629, 133.7751, -51.9253]
    user_counts = [5000, 3000, 2000, 1500, 1200, 1000]

    figure = {
        'data': [
            go.Scattergeo(
                lat=latitudes,
                lon=longitudes,
                text=locations,
                marker=dict(
                    size=[20, 15, 10, 8, 7, 6],  # Marker size relative to user counts
                    color=user_counts,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar_title="User Count"
                )
            )
        ],
        'layout': go.Layout(
            title='User Distribution',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                landcolor='lightgray',
                showcountries=True,
                countrycolor='black'
            ),
            height=500  # Increased height for visibility
        )
    }
    return figure

# Callback to update the additional KPI boxes (Goal Completion, Value, Conversion Rate) and their graphs
@app.callback(
    [Output('goal-completion', 'children'),
     Output('goal-value', 'children'),
     Output('goal-conversion-rate', 'children'),
     Output('goal-completion-graph', 'figure'),
     Output('goal-value-graph', 'figure'),
     Output('goal-conversion-rate-graph', 'figure')],
    [Input('goal-dropdown', 'value')]
)
def update_goal_kpis(goal):
    # Simulating dynamic data for the graphs
    dates = ['Nov 7', 'Nov 8', 'Nov 9', 'Nov 10']
    goal_completion_data = generate_random_data(4, 1300, 50)
    goal_value_data = generate_random_data(4, 4200, 200)
    conversion_rate_data = generate_random_data(4, 3, 0.5)

    goal_completion_figure = {
        'data': [go.Scatter(x=dates, y=goal_completion_data, mode='lines+markers')],
        'layout': go.Layout(margin={'t': 0, 'b': 0}, height=100)
    }
    goal_value_figure = {
        'data': [go.Scatter(x=dates, y=goal_value_data, mode='lines+markers')],
        'layout': go.Layout(margin={'t': 0, 'b': 0}, height=100)
    }
    goal_conversion_rate_figure = {
        'data': [go.Scatter(x=dates, y=conversion_rate_data, mode='lines+markers')],
        'layout': go.Layout(margin={'t': 0, 'b': 0}, height=100)
    }

    return (f"{goal_completion_data[-1]:,.0f}", f"${goal_value_data[-1]:,.0f}", f"{conversion_rate_data[-1]:.2f}%",
            goal_completion_figure, goal_value_figure, goal_conversion_rate_figure)

# Callback to update the main line chart (Sessions and Goal Progress)
@app.callback(
    Output('main-line-chart', 'figure'),
    [Input('goal-dropdown', 'value')]
)
def update_main_line_chart(goal):
    # Simulate dynamic data for sessions and goal progress
    dates = ['Nov 7', 'Nov 8', 'Nov 9', 'Nov 10']
    sessions_data = generate_random_data(4, 1500, 300)
    goal_progress_data = generate_random_data(4, 1.2, 0.3)

    figure = {
        'data': [
            go.Scatter(
                x=dates,
                y=sessions_data,
                mode='lines+markers',
                name='Sessions',
                line=dict(color='#5F9EA0')
            ),
            go.Scatter(
                x=dates,
                y=goal_progress_data,
                mode='lines+markers',
                name=goal,
                line=dict(color='#FF69B4'),
                yaxis='y2'
            ),
        ],
        'layout': go.Layout(
            title='Sessions and Goal Progress',
            title_x=0.5,
            font=dict(color=black_color, family='Arial'),
            yaxis=dict(title='Sessions', titlefont=dict(color=black_color)),
            yaxis2=dict(title='Goal Progress (%)', overlaying='y', side='right', titlefont=dict(color=black_color)),
            showlegend=True,
            legend=dict(x=0, y=1)
        )
    }
    return figure

# Callback to update the KPI values (Total Sessions, Users, Bounce Rate)
@app.callback(
    [Output('total-sessions', 'children'),
     Output('total-users', 'children'),
     Output('bounce-rate', 'children')],
    [Input('goal-dropdown', 'value')]
)
def update_kpis(goal):
    # Fetch total sessions, users, and bounce rate from API
    response = requests.get(f'{API_BASE_URL}/sessions_users?start_date=2023-11-01&end_date=2023-11-10')
    if response.status_code == 200:
        data = response.json()
        # Extract values and pass them to the front-end
        total_sessions = f"{data['total_sessions']:,}"
        total_users = f"{data['total_users']:,}"
        bounce_rate = f"{data['avg_bounce_rate']:.2f}%"
        return total_sessions, total_users, bounce_rate
    else:
        return "N/A", "N/A", "N/A"

if __name__ == '__main__':
    app.run_server(debug=True)

