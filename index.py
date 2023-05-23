import dash
from dash import html, dcc 
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import plotly.express as px 
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app = dash.Dash(__name__)
server = app.server 

import pandas as pd
import numpy as np
from app import *


load_figure_template("litera")

area_cliente = pd.read_csv('assets/area_cliente_final.csv', sep=',')

available_types = area_cliente['tipo'].unique()

available_year = area_cliente['ano'].unique()

available_distance = area_cliente['distancia'].unique()

# ============ Layout ============= # 
app.layout = html.Div(children=[

    dbc.Row([
        dbc.Col([
           dbc.Card([
                html.H2("ECCON", style={"font-family": "Arial", "font-size": "60px", "margin-top": "30px", "margin-left": "30px"}),
                html.Hr(),
                html.P("Classificação da área de pastagem", style = {"margin-top": "30px", "margin-left": "10px"}),
                dcc.Dropdown(id = "check_type",
                options=[{'label': i, 'value': i} for i in available_types],
                value=['degradação moderada', 'não degradado'],
                multi=True,
                style={'color': 'Black', 'font-size': 15}),
                
                html.P("Distância da fazenda", style = {"margin-top": "30px", "margin-left": "10px"}),
                dcc.Dropdown(id = "check_distance",
                options=[{'label': i, 'value': i} for i in available_distance],
                value='nenhuma distância',
                multi=False,
                style={'color': 'Black', 'font-size': 13}),
                html.P("Série histórica da pastagem", style = {"margin-top": "30px", "margin-left": "10px"}),
                dcc.Dropdown(id = "check_series",
                options=[{'label': i, 'value': i} for i in available_types],
                value='degradação moderada',
                multi=False,
                style={'color': 'Black', 'font-size': 13}),
                html.P("Ano da pastagem (gráfico de pizza)", style = {"margin-top": "30px", "margin-left": "10px"}),
                dcc.Input(id = "check_year",
                placeholder='Insira um ano de interesse...',
                type='number',
                value=2021,
                style={'color': 'Black', 'font-size': 13})
                    ]),
                
                ], sm = 3),
    
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id="type_fig"),], sm = 6),
                dbc.Col([dcc.Graph(id="pie_fig"),], style = {"margin-top": "30px"}, sm = 6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="series_fig"),], sm = 12)
            ])
            # dbc.Row([
            # dbc.Col([dcc.Graph(id="city_car_series"),], sm = 6),
            # dbc.Col([dcc.Graph(id="car_soytimes"),], sm = 6)
        
        ], sm = 9),
        
    ])
]
)

# ============== Callbacks ============== # 
@app.callback( 
                Output('type_fig', 'figure'),
                Output('series_fig', 'figure'),
                Output('pie_fig', 'figure')
                ,
                Input('check_type', 'value'),
                Input('check_distance', 'value'),
                Input('check_series', 'value'),
                Input('check_year', 'value'),
                )

def render_graphs(types, distance, series_type, year):

    operation = np.sum

    #area_cliente['ano'] = area_cliente['ano'].as_type(int)

    df_filtered = area_cliente[area_cliente["tipo"].isin(types) & area_cliente["distancia"].isin([distance])]

    df_pie_filtered = area_cliente[area_cliente["ano"].isin([year]) & area_cliente["distancia"].isin([distance])]

    
    #df_filtered = area_cliente[area_cliente["ano"].isin([2020]) & area_cliente["tipo"].isin(['degradação moderada'])]

    #df_series = df_type_filtered.groupby(["tipo", "ano"])["area_pasto"].apply(operation).to_frame().reset_index()

    fig_pie = fig = px.pie(df_pie_filtered, values="area_pasto", names="tipo", 
             title='Qualidade de pastagem', hover_data=["area_pasto"])
    
    df_types = df_filtered.groupby(["tipo", "ano"], group_keys=False)["area_pasto"].apply(operation).to_frame().reset_index()

    df_type_filtered = area_cliente[area_cliente["tipo"].isin([series_type]) & area_cliente["distancia"].isin([distance])]

    df_series = df_type_filtered.groupby(["tipo", "ano"], group_keys=False)["area_pasto"].apply(operation).to_frame().reset_index()

    fig_types = px.bar(df_types, x = "ano", y = "area_pasto", barmode = 'group',
    color = "tipo")

    series_fig = px.line(df_series, x = "ano", y = 'area_pasto')

    for fig in [fig_types, series_fig, fig_pie]:

        fig.update_layout(margin = dict(l = 20, r = 20, t = 20, b = 20), height = 400, template = "litera")
        fig.update_layout(font={'size': 10})

    series_fig.update_traces(mode='lines+markers')

    series_fig.update_xaxes(showgrid=False)
    series_fig.add_annotation(x=0, y=1, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text='Série Histórica da classificação de degradação em pastagem por hectares')

    series_fig.update_traces(mode='lines+markers')


    return fig_types, series_fig, fig_pie

# =================== Run Server =================== #
if __name__ == "__main__":
    app.run_server(port=8052, debug=True)