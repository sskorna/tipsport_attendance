# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv("MatchInfo.csv")
team_averages = [1000, 1000, 1000]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server 

app.layout = html.Div(children=[
    html.H1(children='Spectators in Tipsport league'),

    html.Div(children='''
        Select team
    '''),
             
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
            {'label': 'Liptovský Mikuláš', 'value': 'LM'}
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
                'title': 'Average attendance'
            }
        }
    )
])
    
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    
    plotdata = data.loc[data.loc[:,"sHome"] == selected_dropdown_value
                    , {"iSpectators","dDate"}]
    team_averages = []
    for j in range (1, 4):
        start = str(2015 + j) + "-07-01"
        end = str(2016 + j) + "-06-01"        
        mask = (plotdata['dDate'] > start) & (plotdata['dDate'] <= end)
        subset_data = plotdata.loc[mask]
        team_averages.append(np.mean(subset_data["iSpectators"]))
    
    return {
        'data': [{
            'x': ["2016/2017", "2017/2018", "2018/2019"],
            'y': team_averages,
            'type': 'bar',
            'name': u'Montréal'
        }],
        'layout': {
            'title': 'Average attendance'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
