import os
import base64
from pathlib import Path
from dash import html, Input, Output, State, callback, dcc
import dash_bootstrap_components as dbc
import dash
from dash_extensions import BeforeAfter
from utils import dataManager as dm
from utils import layoutFunctions as lf

# Initialize utility objects and useful functions
dataFolder = Path(__file__).parent.parent.absolute() / 'assets/batagaika_crater'

# Load the necessary data
satellite_data = [
    {'label': '13.08.1991', 'value': '19910813_Crater.png'},
    {'label': '27.08.1999', 'value': '19990827_Crater.png'},
    {'label': '20.08.2005', 'value': '20050820_Crater.png'},
    {'label': '15.06.2010', 'value': '20100615_Crater.png'},
    {'label': '11.07.2014', 'value': '20140711_Crater.png'},
    {'label': '07.08.2018', 'value': '20180807_Crater.png'},
    {'label': '10.08.2022', 'value': '20220810_Crater.png'},
    {'label': '11.08.2022', 'value': '20220811_Crater.png'},
]

# LAYOUT
layout = html.Div(
    [
        dbc.Row(lf.make_NavBar()),  
        dbc.Row(
            [
                dbc.Col(lf.make_pedo_2_sidebar(), width=4, lg=3, md=12),  
                dbc.Col(
                    [
                        lf.make_pedo_2_settings(),
                        dcc.Tabs([
                            dcc.Tab(label='Zeitraffer', children=[
                                html.Div([
                                    dbc.Row([
                                        dbc.Col(html.H1("Zeitraffer", style={'textAlign': 'center'}), width=12),
                                        html.Hr(),
                                        dbc.Col(
                                            dbc.Button('Play', id='play-button', n_clicks=0, color='primary', className='mr-2'),
                                            width='auto'
                                        ),
                                        dbc.Col(
                                            dbc.Button('Stopp', id='stop-button', n_clicks=0, color='primary', className='mr-2'),
                                            width='auto'
                                        ),
                                        dbc.Col(
                                            dbc.Button('Vorwärts', id='next-button', n_clicks=0, color='primary'),
                                            width='auto'
                                        ),
                                    ], justify='center', className='mb-3'),
                                    html.Iframe(id='image-display', style={'width': '80%', 'height': '96.5vh', 'border': '1px solid #000', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                                    dcc.Interval(id='play-interval', interval=300, n_intervals=0, disabled=True),
                                ], style={'text-align': 'center'}),
                            ]),

                            dcc.Tab(label='Vergleich', children=[
                                dbc.Container([
                                    dbc.Row(
                                        dbc.Col(html.H1("Vorher- Nachher Vergleich", style={'textAlign': 'center'}), width=12)
                                    ),
                                    html.Hr(),
                                    dbc.Row([
                                        dbc.Col([
                                            html.H2("Aufnahme für Vorher-Vergleich auswählen"),
                                            dcc.RadioItems(
                                                id='before-radio',
                                                options=[
                                                    {'label': data['label'], 'value': data['value']} for data in satellite_data
                                                ],
                                                value='19910813_Crater.png',
                                                labelStyle={'display': 'block', 'margin-bottom': '20px'},  
                                            ),
                                        ], width=3),
                                        dbc.Col([
                                            BeforeAfter(id='image-slider', width=612, height=512, defaultProgress=0.5),
                                        ], width=6),
                                        dbc.Col([
                                            html.H2("Aufnahme für Nachher-vergleich auswählen"),
                                            dcc.RadioItems(
                                                id='after-radio',
                                                options=[
                                                    {'label': data['label'], 'value': data['value']} for data in satellite_data
                                                ],
                                                value='20220811_Crater.png',
                                                labelStyle={'display': 'block', 'margin-bottom': '20px'}, 
                                            ),
                                        ], width=3),
                                    ]),
                                ]),
                            ]),
                         ]),
                    ],
                    width=8, lg=9, md=12  
                ),
            ],
            className="g-0",  
        ),
        dbc.Row([lf.make_footer()]),
    ],
    className="my-3", 
)

@callback(
    Output('play-interval', 'disabled'),
    Output('image-display', 'srcDoc'),
    Input('play-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    Input('next-button', 'n_clicks'),
    Input('play-interval', 'n_intervals')
)
def update_image_and_control_interval(play_clicks, stop_clicks, next_clicks, n_intervals):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'play-button':
        selected_index = play_clicks % len(satellite_data)
        return False, generate_iframe(selected_index)
    elif triggered_id == 'stop-button':
        return True, dash.no_update
    elif triggered_id == 'next-button':
        selected_index = next_clicks % len(satellite_data)
        return True, generate_iframe(selected_index)
    elif triggered_id == 'play-interval':
        selected_index = n_intervals % len(satellite_data)
        return False, generate_iframe(selected_index)
    else:
        return True, dash.no_update

def generate_iframe(selected_index):
    selected_data = satellite_data[selected_index]
    image_path = os.path.join(dataFolder, selected_data['value'])
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    iframe_code = f'''
        <div style="position: relative; width: 100%; height: 100%;">
            <img src="data:image/png;base64,{encoded_image}" style="width: 100%; height: 100%;">
            <div style="position: absolute; top: 10px; right: 10px; font-size: 18px; color: black; background-color: white; padding: 5px; z-index: 1;">{selected_data['label']}</div>
        </div>
    '''
    return iframe_code

@callback(
    Output('image-slider', 'after'),
    Output('image-slider', 'before'),
    Input('before-radio', 'value'),
    Input('after-radio', 'value')
)
def update_images(before_image, after_image):
    return f'assets/batagaika_crater/{before_image}', f'assets/batagaika_crater/{after_image}'

@callback(
    Output('satellitendaten-modal', 'is_open'),
    [Input('open-satellitendaten-modal-button', 'n_clicks'), Input('close-satellitendaten-modal-button', 'n_clicks')],
    [State('satellitendaten-modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
