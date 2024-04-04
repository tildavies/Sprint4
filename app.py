# %%
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, State

# %%
data = pd.read_csv("data.csv")

# %%
data['AvgPitStopDuration'] = data.groupby(['raceId', 'driverId'])['pitStopDuration'].transform('mean')
data['AvgPitStopDuration'] = data['AvgPitStopDuration'] / 1000

# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

app.layout = html.Div([
    html.Div(
        children=[
            html.Div('Formula 1 Dashboard',className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Description'),
            html.Div('''
                     Interact with the dashboard below to view both driver and Grand Prix overall perfromance from the year 1950 till now. 
            ''')
        ])
    ),
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in data['year'].unique()],
            value=data['year'].min(),
            clearable=False)
    ]),
    html.Div([
        dcc.Graph(id='graph')])
])

##########################################################
#################APP CALLBACKS############################
##########################################################

@app.callback(
    Output('graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    filtered_df = data[data['year'] == selected_year]
    fig = px.line(filtered_df, x= 'name',
              y='AvgPitStopDuration',
              color='driverRef',
              title= 'Average Pit Stop Duration per Grand Prix, by driver')
    fig.update_xaxes(title_text='Grand Prix')
    fig.update_yaxes(title_text='Average Pit Stop Duration')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



