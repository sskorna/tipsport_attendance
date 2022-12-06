# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv("MatchInfo.csv")
data["dDate"] = pd.to_datetime(data["dDate"])
data_cum = pd.read_csv("MatchInfoCum.csv")
data_cum = data_cum[6:201]
team_averages = [1000, 1000, 1000]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server 

app.layout = html.Div(children=[
    html.H1(children='Spectators in Tipsport league'),

    html.Div(children='''
        Select hockey club
    '''),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': 'Trenčín', 'value': 'TN'},
                    {'label': 'Banská Bystrica', 'value': 'BB'},
                    {'label': 'Košice', 'value': 'KE'},
                    {'label': 'Nitra', 'value': 'NR'},
                    {'label': 'Žilina', 'value': 'ZI'},
                    {'label': 'Zvolen', 'value': 'ZV'},
                    {'label': 'Poprad', 'value': 'PP'},
                    {'label': 'Nové Zámky', 'value': 'NZ'},
                    {'label': 'Liptovský Mikuláš', 'value': 'LM'},
                    {'label': 'Detva', 'value': 'DT'},
                    {'label': 'Martin', 'value': 'MT'},
                    {'label': 'Budapest', 'value': 'BU'},
                    {'label': 'Miskolc', 'value': 'MI'}
#                    ,
#                    {'label': 'all', 'value': 'all'}
                ],
                value='BB'
            ),
            
            dcc.Graph(
                id='my-graph',
                figure={
                    'data': [{
                            'x': ["2016/2017", "2017/2018", "2018/2019"],
                            'y': team_averages,
                            'type': 'bar',
                            'name': u'Montréal'
                    }],
                    'layout': {
                        'title': 'Average attendance per club'
                    }
                }
            )
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='g2',
                figure=go.Figure(
                    data=[
                        go.Scatter(
                            x = np.arange(1,196),
                            y = data_cum["0"],
                            name = "2016/2017",
                            line = dict(
                                color = ('rgb(205, 12, 24)'),
                                width = 4
                            )
                        ),
                        go.Scatter(
                            x = np.arange(1,196),
                            y = data_cum["1"],
                            name = "2017/2018",
                            line = dict(
                                color = ('rgb(55, 83, 109)'),
                                width = 4
                            )
                        ),
                        go.Scatter(
                            x = np.arange(1,196),
                            y = data_cum["2"],
                            name = "2018/2019",
                            line = dict(
                                color = ('rgb(26, 118, 255)'),
                                width = 4
                            )
                        )
                    ],
                layout = dict(title = 'Running sum of spectators over time')
                )
            )
        ], className="six columns"),
    ], className="row")
])
    
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    
    if selected_dropdown_value == "all":
        plotdata = data[["iSpectator", "dDate"]]
    else:
        plotdata = data.loc[data.loc[:,"sHome"] == selected_dropdown_value
                    , ["iSpectators","dDate"]]
    team_averages = []
    for j in range (1, 4):
        start = str(2015 + j) + "-07-01"
        end = str(2016 + j) + "-06-01"        
        mask = (plotdata['dDate'] > start) & (plotdata['dDate'] <= end)
        subset_data = plotdata.loc[mask]
        team_averages.append(np.mean(subset_data["iSpectators"].dropna()))
    print(team_averages)
    return {
        'data': [{
            'x': ["2016/2017", "2017/2018", "2018/2019"],
            'y': team_averages,
            'type': 'bar',
            'name': u'Montréal'
        }],
        'layout': {
            'title': 'Average attendance by club'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
