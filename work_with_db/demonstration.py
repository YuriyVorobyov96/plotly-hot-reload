import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlite3
import rsa_decoder

app = dash.Dash(__name__)

connection = sqlite3.connect('shows.db', check_same_thread=False)
cursor = connection.cursor()

number_of_sensors = 7

app.layout = html.Div([

    html.H1('Web Application Dashboards For Sensors', style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_sensor',
                 options=[
                     {'label': 'Датчик контроля протечек', 'value': 'leakage'},
                     {'label': 'Датчик задымления', 'value': 'smoke'},
                     {'label': 'Датчик утечки газа', 'value': 'gas'},
                     {'label': 'Датчик температуры', 'value': 'temp'},
                     {'label': 'Датчик влажности воздуха', 'value': 'hum'},
                     {'label': 'Датчик движения', 'value': 'motion'},
                     {'label': 'Датчик открытия окон и дверей', 'value': 'open'},
                 ],
                 multi=False,
                 value='leakage',
                 style={'width': '40%'}
                 ),

    dcc.Interval(id='interval', interval=3 * 1000, n_intervals=0),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='sensors_info', figure={})

])


# ------------------------------------------------------------------------------
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sensors_info', component_property='figure')],
    [Input(component_id='slct_sensor', component_property='value'),
     Input('interval', 'n_intervals')]
)
def update_graph(option_slctd, times_clicked):
    print(option_slctd)

    container = 'The sensor chosen by user was: {}'.format(option_slctd)
    
    cursor.execute("SELECT * FROM Shows")
    data_from_db = cursor.fetchall()
    
    values = []
    
    for i in range(len(data_from_db)):
        data_from_db_as_list = list(data_from_db[i])
        data_list = []
        for j in range(len(data_from_db_as_list)):
            data = rsa_decoder.decode(data_from_db_as_list[j])
            data_list.append(data)
        values.append(data_list)
    
    df = pd.DataFrame(values, columns=['datatime', 'leakage', 'smoke', 'gas', 'temp', 'hum', 'motion', 'open'])

    trace = go.Scatter(
        y=df[option_slctd],
        x=df['datatime'],
        name='lines+markers'
    )

    fig = go.Figure(trace)

    return container, fig


if __name__ == '__main__':
    app.run_server()




