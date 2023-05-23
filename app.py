import dash_bootstrap_components as dbc
import dash
from app import *

from dash_bootstrap_templates import load_figure_template

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

load_figure_template("minty")
    
if __name__ == "__main__":
    app.run_server(port=8052, debug=True)


                        

