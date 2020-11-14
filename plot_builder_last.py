#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

random_values = []

def rescale(value, old_min, old_max, new_min, new_max):
    rescaled = (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
    return rescaled

app = dash.Dash(__name__)

df = pd.read_csv('sensor_readings.csv')

app.layout = html.Div([

    # хедер
    html.H1('Панель мониторинга показаний датчиков', style={'text-align': 'center'}),

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

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sensors_info', component_property='figure')],
    [Input(component_id='slct_sensor', component_property='value'),
     Input('interval', 'n_intervals')]
)
def update_graph(option_slctd, times_clicked):
    print(option_slctd)
    print(type(option_slctd))

    container = 'Выбранный датчик: {}'.format(option_slctd)

    leakage_sensor = np.random.binomial(10,0.5)
    leakage_sensor = rescale(leakage_sensor, 0, 10, 0, 1)
    leakage_sensor_1 = round(leakage_sensor)
    smoke_sensor = np.random.gumbel(0,1)
    smoke_sensor = rescale(smoke_sensor, -5, 6, 0, 1)
    smoke_sensor_1 = round(smoke_sensor)
    gas_leak_sensor = np.random.laplace(loc=0.0, scale=1.0, size=None)
    gas_leak_sensor = rescale(gas_leak_sensor, -5, 5, 0, 50)
    temp_sensor = np.random.power(0.7)
    temp_sensor = rescale(temp_sensor, 0, 1, 0, 50)
    humidity_sensor = np.random.uniform(0, 100)
    motion_sensor = np.random.weibull(2)
    motion_sensor = rescale(motion_sensor, 0, 3, 0, 1)
    motion_sensor_1 = round(motion_sensor)
    opening_sensor = np.random.normal(100, 10)
    opening_sensor = rescale(opening_sensor, 70, 120, 0, 1)
    opening_sensor_1 = round(opening_sensor)
    
    csv_data = datetime.datetime.now()

    random_values.append([
        csv_data,
        leakage_sensor_1,
        smoke_sensor_1,
        gas_leak_sensor,
        temp_sensor,
        humidity_sensor,
        motion_sensor_1,
        opening_sensor_1,
    ])

    frame = pd.DataFrame(random_values, columns=['datatime', 'leakage', 'smoke', 'gas', 'temp', 'hum', 'motion', 'open'])
    frame.to_csv('sensor_readings.csv', index=False)

    print('Data recorded')
    
    df = pd.read_csv('sensor_readings.csv')
    
    trace = go.Scatter(
        y=df[option_slctd],
        x=df['datatime'],
        name='lines+markers'
     )
    
    fig = go.Figure(trace)

    return container, fig

if __name__ == '__main__':
    app.run_server()


# In[ ]:




