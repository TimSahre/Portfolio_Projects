from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages import (start_page_1, start_page_2, klima_1, klima_2, 
                   hydro_1, hydro_2, pedo_1, pedo_2, blankPage)

# Initialize Dash app
app = Dash(__name__,
           title="Klima Kompass Navigator",
           external_stylesheets=[dbc.icons.FONT_AWESOME],
           suppress_callback_exceptions=True)

# Define index layout
index_layout = html.Div([
    dcc.Location(id='url', pathname='/', refresh=False),
    html.Div(id='page-content')
])

# Create the 'complete' layout to validate all callbacks
app.validation_layout = html.Div([
    index_layout,
    start_page_1.layout,
    start_page_2.layout,
    klima_1.layout,
    klima_2.layout,
    hydro_1.layout,
    hydro_2.layout,
    pedo_1.layout,
    pedo_2.layout,
    blankPage.layout
])

# Define app layout
app.layout = index_layout

# Callback to display pages based on URL pathname
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if not pathname or pathname == '/':
        return start_page_1.layout
    elif pathname == '/start_page_2':
        return start_page_2.layout
    elif pathname == '/klima_1':
        return klima_1.layout
    elif pathname == '/klima_2':
        return klima_2.layout
    elif pathname == '/hydro_1':
        return hydro_1.layout
    elif pathname == '/hydro_2':
        return hydro_2.layout
    elif pathname == '/pedo_1':
        return pedo_1.layout
    elif pathname == '/pedo_2':
        return pedo_2.layout
    else:
        return blankPage.layout
    
# Define server object for deployment
server = app.server

# For local execution
if __name__ == '__main__':
    app.run_server(debug=True)
