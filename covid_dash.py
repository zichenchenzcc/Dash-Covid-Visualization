# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:47:50 2020

@author: czc
"""
import dash 
from dash.dependencies import Input, Output, State, MATCH
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import os

os.chdir("C:\\Users\\czc\\Desktop\\Python2\\Project 3\\happiness score")
df = pd.read_csv("covid_19_data_sub.csv")
df.iloc[:,0:8] = df.iloc[:,0:8].fillna(0)
df.iloc[:,8:18] = df.iloc[:,8:18].fillna(0)
column_list = [0,1,2,3,5,7,8,13,16]
df_group = df.iloc[:,column_list]
df_agg = df_group.groupby(['country']).agg({'new_cases':'sum','new_deaths':'sum'}).reset_index()

column_list1 = [0,1,2,8,13,16]
df_new = df.iloc[:,column_list1]
df_new = df_new.drop_duplicates().reset_index()
df_new = df_new.drop('index',axis=1)
df_new['Total Case'] = df_agg['new_cases']
df_new['Total Death'] = df_agg['new_deaths']
df_new.loc[df_new['Total Case'] == df_new['Total Case'].max()]
df_new = df_new.drop([188])
df_new['Logarithmic Total Case'] = np.log(df_new['Total Case']+1)
df_new.columns = ['ISO Code','Continent','Country','Population','GDP/Capita','Life Expectancy','Total Case','Total Death','Logarithmic Total Case']
df_new['GDP/Capita'] = df_new['GDP/Capita'].round(4)
columns = ['ISO Code','Continent','Country','Population','GDP/Capita','Life Expectancy','Total Case','Total Death']
dff = df.iloc[:,[0,1,2,3,4,5,6,7,8,9,13,16]]
dff.columns = ['ISO Code','Continent','Country','Date','Total Case','New Case','Total Death','New Death','Population','Population Density','GDP/Capita','Life Expectancy']
dff = dff.drop(dff.loc[dff['Date']=='1/22/2020'].index)

app = dash.Dash(__name__) 
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "selectable": True}
            if i == "Country" or i == "Total Case" or i == "Total Death"
            else {"name": i, "id": i, "selectable": True, "hideable": True}
            for i in columns
        ],
        data=df_new.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['ISO Code','Continent','Country']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='choromap-container'),
    html.Br(),
    html.Div([
    html.Div(children=[html.Button('Add Customized Chart', id='add-chart', n_clicks=0)]),
    html.Div(id='container', children=[])
            ])
])

# Create choropleth map
@app.callback(
    Output(component_id='choromap-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dfff = pd.DataFrame(all_rows_data)
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dfff))]

    if "ISO Code" in dfff and "Population" in dfff and "Country" in dfff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 500},
                      figure=px.choropleth(
                          data_frame=dfff,
                          locations='ISO Code',
                          scope="world",
                          color="Logarithmic Total Case",
                          title="Covid-19 Across World",
                          template='plotly_dark',
                          hover_data=['Country', 'Total Case','Total Death','Population'],
                      ).update_layout(showlegend=False, title=dict(font=dict(size=24), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders,
                                     marker_line_color='lightblue',
                                     hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                   "<b>Total Case:  "+"%{customdata[1]}</b><br>"+
                                                   "<b>Total Death: "+"%{customdata[2]}</b><br>"+
                                                   "<b>Population:  "+"%{customdata[3]}</b>")          
                      )
            ]

# Add and display customized charts
@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Line Chart', 'value': 'line'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df_new['Country'].unique())],
                multi=True,
                value=["United States", "United Kingdom", "France"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                options=[{'label': n, 'value': n} for n in ['Total Case','Total Death','Population','GDP/Capita','Life Expectancy']],
                value='Total Case',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children

# Return different options for bar chart and line chart
@app.callback(
    [Output({'type': 'dynamic-dpn-num', 'index': MATCH}, 'options'),
     Output({'type': 'dynamic-dpn-num', 'index': MATCH}, 'value')],
    [Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def choose_graph(chart_choice):
    if chart_choice == 'bar':
        option=[{'label': n, 'value': n} for n in ['Total Case','Total Death','Population','GDP/Capita','Life Expectancy']]
        return option,'Total Case'
    elif chart_choice == 'line':
        option=[{'label': n, 'value': n} for n in ['Total Case','New Case','Total Death','New Death']]
        return option,'Total Case'

# Update each added chart
@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-s', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(s_value, num_value, chart_choice):
    if chart_choice == 'bar':
        dfbar = df_new[df_new['Country'].isin(s_value)]
        fig = px.bar(dfbar, x='Country', y=num_value, title="{} Across Countries".format(num_value)).update_layout(xaxis={'categoryorder': 'total descending'})
        fig.update_layout(
                        font_family="Courier New",
                        font_color="blue",
                        title_font_family="Times New Roman",
                        title_font_color="blue",
                        legend_title_font_color="green",
                        title={'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                        font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="RebeccaPurple"
                                )
                        )
        return fig
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            dfline = dff[dff['Country'].isin(s_value)]
            fig = px.line(dfline, x='Date', y=num_value, color='Country', title="{} Across Countries".format(num_value), range_x=['2020-01-23','2020-12-05'])
            fig.update_layout(
                        font_family="Courier New",
                        font_color="blue",
                        title_font_family="Times New Roman",
                        title_font_color="blue",
                        legend_title_font_color="green",
                        title={'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                        font=dict(
                                    family="Courier New, monospace",
                                    size=18,
                                    color="RebeccaPurple"
                                )
                        )
            return fig
    
        return fig

# Highlight selected column
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
