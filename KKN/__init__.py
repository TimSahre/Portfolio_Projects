# angepasste app.py 

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages import klima_1,klima_2, hydro_1, hydro_2, pedo_1, pedo_2, blankPage # Hier !!

app = Dash(__name__,
    title="Klima Kompass Navigator",
    external_stylesheets=[dbc.icons.FONT_AWESOME] # ???
)

indexLayout = html.Div([
    dcc.Location(id='url', pathname='/klima_1', refresh=False),
    html.Div(id='page-content')
])

# Erstellung des 'kompletten' Layouts, um alle Callbacks zu validieren. Andernfalls wird Dash beim Versuch, sie zu
# validieren, Fehler melden, da sie mit Komponenten verknüpft sind, die sich nicht auf der angezeigten Seite befinden und # daher nicht Teil des aktuellen Layouts sind.
# app.validation_layout = html.Div([
#     indexLayout,
#     start_page_1.layout,
#     start_page_2.layout,
#     klima_1.layout,
#     klima_2.layout,
#     hydro_1.layout,
#     hydro_2.layout,
#     pedo_1.layout,
#     pedo_2.layout,
#     blankPage.layout
# ])

# Tatsächliches Seitenlayout
app.layout = indexLayout

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/klima_1':
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
    
# Dieses Serverobjekt wird vom WSGI-Skript geladen, um als Webapplikation
# auf einem Produktionsserver bereitgestellt zu werden
server = app.server

# Bei lokaler Ausführung 
if __name__ == '__main__':
    app.run_server(debug=True)