#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Helper functions
def generate_traces(year, color):
    file_path = f"C:/analysis/realfinal/data/서울특별시 구별 강수량_2018~2022(07~08)_성지영 (1)/서울특별시 구별 강수량_{year}(07~08).CSV"
    pcp = pd.read_csv(file_path)
    pcp['조사년월일'] = pcp['조사년월일'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))

    scatter_trace = go.Scatter(
        x=pcp['조사년월일'],
        y=pcp['일일강수량'],
        mode='markers',
        name=f'{year} Scatter Plot'
    )

    line_trace = go.Scatter(
        x=pcp['조사년월일'],
        y=pcp['일일강수량'],
        mode='lines+markers',
        name=f'{year} Line Plot'
    )

    line_trace.update(line=dict(color=color))

    return scatter_trace, line_trace

def create_choropleth_map(tot, localpop):
    merge_tot = pd.merge(tot, localpop, left_on='ADM_NM', right_on='행정동명', how='left')
    tot_json = merge_tot.__geo_interface__

    trace = go.Choroplethmapbox(
        geojson=tot_json,
        locations=merge_tot.index,
        z=merge_tot['평균생활인구수']
    )

    layout = go.Layout(
        mapbox_style='carto-positron',
        mapbox_zoom=8.5,
        mapbox_center={"lat": 37.6, "lon": 127},
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return go.Figure(trace, layout)

def create_scatter_plot(data, title):
    data_cleaned = data[data['평당 월세'] >= 0]
    data_cleaned = data_cleaned.sort_values(by='계약년월')
    fig = px.scatter(data_cleaned, x='계약년월', y='평당 월세', color='평당 월세', size='평당 월세', title=title)
    fig.update_layout(xaxis=dict(type='category'), plot_bgcolor='black', paper_bgcolor='black', font=dict(color='white'))
    return fig

# Load data
tot = gpd.read_file("C:/Users/user/Desktop/_census_data_2022_bnd_dong_bnd_dong_11_2022_2022/bnd_dong_11_2022_2022_2Q.shp", encoding='euc-kr')
tot.geometry = tot.geometry.set_crs("EPSG:5179")
tot.geometry = tot.geometry.to_crs("EPSG:4326")

file1 = pd.read_excel("C:/analysis/realfinal/data/아파트_최종.xlsx")
file2 = pd.read_excel("C:/analysis/realfinal/data/연립다세대_최종.xlsx")
file3 = pd.read_excel("C:/analysis/realfinal/data/단독다가구_최종.xlsx")

localpop = pd.read_excel("C:/analysis/realfinal/data/평균생활인구수.xlsx")

merge_tot = pd.merge(tot, localpop, left_on='ADM_NM', right_on='행정동명', how='left')

tot_json = merge_tot.__geo_interface__

# Set up the Dash app
app = dash.Dash(__name__)

# Define layout for the tabs
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Precipitation in Seoul', children=[
            html.H1("Precipitation in Seoul"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': year, 'value': year} for year in ['2018', '2019', '2020', '2021', '2022']
                ],
                value='2018',
                style={'width': '200px'}
            ),
            dcc.Graph(id='graph-container-tab1')
        ]),
        
        dcc.Tab(label='Average Living Population in Seoul', children=[
            html.H1("Average living population in Seoul"),
            dcc.Graph(id='choropleth-map-tab2'),
            dcc.Dropdown(
                id='map-style-dropdown-tab2',
                options=[{'label': 'Average living population in Seoul', 'value': 'carto-positron'}],
                value='carto-positron',
                style={'color': 'white'}
            )
        ]),
        
        dcc.Tab(label='Actual Transaction Price of Real Estate in the Target Area', children=[
            html.H1("Real estate actual transaction price", style={'color': 'black'}),
            dcc.Dropdown(
                id='property-type-dropdown-tab3',
                options=[
                    {'label': 'Apartment', 'value': '아파트'},
                    {'label': 'Row house', 'value': '연립다세대'},
                    {'label': 'Multi-unit house', 'value': '단독다가구'}
                ],
                value='아파트',
                style={'color': 'black'}
            ),
            dcc.Graph(id='scatter-plot-tab3'),
        ]),
    ])
])

# Callbacks
@app.callback(
    Output('graph-container-tab1', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph_tab1(selected_year):
    scatter_trace, line_trace = generate_traces(selected_year, 'royalblue')
    return {
        'data': [scatter_trace, line_trace],
        'layout': {
            'title': f'{selected_year}년 7~8월 서울특별시 강수량',
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font': {'color': 'white'}
        }
    }

@app.callback(
    Output('choropleth-map-tab2', 'figure'),
    [Input('map-style-dropdown-tab2', 'value')]
)
def update_map_style_tab2(selected_style):
    fig = go.Figure(go.Choroplethmapbox(
        geojson=tot_json,
        locations=merge_tot.index,
        z=merge_tot['평균생활인구수'],
        colorscale='Viridis',
        zmin=merge_tot['평균생활인구수'].min(),
        zmax=merge_tot['평균생활인구수'].max(),
        marker_opacity=0.5,
        marker_line_width=0,
    ))

    fig.update_layout(
        mapbox_style='mapbox://styles/mapbox/dark-v9',
        mapbox_zoom=10,
        mapbox_center={"lat": 37.5665, "lon": 126.9780},
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='black',  
        plot_bgcolor='black' 
    )

    fig.update_layout(mapbox={'accesstoken': "pk.eyJ1Ijoic21iMDEyMyIsImEiOiJjbHB6aGdocWgxYXNmMmtvOGEydnphbmgyIn0.7qugebKjtaeQhnl6TL6KrA"})

    return fig

@app.callback(
    Output('scatter-plot-tab3', 'figure'),
    [Input('property-type-dropdown-tab3', 'value')]
)
def update_scatter_plot_tab3(selected_property_type):
    if selected_property_type == '아파트':
        return create_scatter_plot(file1, '아파트 평당 월세')
    elif selected_property_type == '연립다세대':
        return create_scatter_plot(file2, '연립다세대 평당 월세')
    elif selected_property_type == '단독다가구':
        return create_scatter_plot(file3, '단독다가구 평당 월세')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8010)


# In[ ]:




