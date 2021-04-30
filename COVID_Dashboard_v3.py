import dash
import plotly
import pandas as pd
#import plotly.graph_objects as go
import plotly.graph_objs as go
# import dash_leaflet as dl
import datetime
from datetime import datetime as dt #same as import datetime.datetime as dt
from datetime import timedelta
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.offline as py
from pandas import DataFrame as df
import numpy as np
import plotly.express as px
import geopandas as gpd
import json
import dash_table
from glob import glob

#########################################################
#
# region 1 Map Box Access Token
#
#########################################################

#mapbox_access_token = "pk.eyJ1Ijoic2FuYXp6ZWh0YWJpIiwiYSI6ImNpdjE5eG41eDAwNnMyb2xnazJ6bGdxb2UifQ.q6AO75Adqp4PLaUls-D7pA"


#########################################################
#
# endregion 
#
#########################################################

#########################################################
#
# region 2 Reading Raw Files
#
#########################################################

geoJ = gpd.read_file('C:/Users/masro/VScodeProjects/COVID Dashboard/geojson/countries.geojson')
countries = pd.read_csv("C:/Users/masro/VScodeProjects/COVID Dashboard/geojson/countries.csv")
geoD = gpd.read_file('C:/Users/masro/VScodeProjects/COVID Dashboard/geojson/us_states.json')
us_states = pd.read_csv("C:/Users/masro/VScodeProjects/COVID Dashboard/geojson/us_states.csv")
Apple_Mobility_Data = pd.read_csv("C:/Users/masro/VScodeProjects/COVID Dashboard/Apple_Data_Refined.csv")
Apple_State_Data = pd.read_csv("C:/Users/masro/VScodeProjects/COVID Dashboard/Apple_US_state.csv")
Google_Data = pd.read_csv("C:/Users/masro/VScodeProjects/COVID Dashboard/Google_Data_Refined.csv")

country_name = "UNITED STATES"
Country_data = pd.DataFrame()

state_name = "CALIFORNIA"

column = Apple_Mobility_Data['Date']
max_value = column.max()

column2 = Google_Data['date']
max_value_google = column2.max()

#########################################################
#
# endregion 
#
#########################################################

#########################################################
#
# region 3 Funtions
#
#########################################################

#Creating the worldmap
def make_basemap():
    fig=px.choropleth_mapbox(countries,locations='Name',featureidkey='properties.ADMIN',
                            geojson=geoJ,color='zone',mapbox_style="carto-positron", zoom=1,center={'lat':30.2672,'lon':-97.7431},
                            color_continuous_scale='thermal',opacity=0.3)
    fig.update_layout(
        clickmode="event+select"
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


#Creating the state map
def make_statemap():
    fig=px.choropleth_mapbox(us_states,locations='State',featureidkey='properties.NAME',
                            geojson=geoD,color='Zone',mapbox_style="carto-positron", zoom=3,center={'lat':36.2407934124042,'lon':-86.84561122618726},
                            color_continuous_scale='thermal',opacity=0.3)
    fig.update_layout(
        clickmode="event+select"
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def country_title(country_name):
    return country_name

def state_title(country_name):
    return country_name


#creating Apple Mobility Chart for particular mode

def applemobility_country(country_name,mode,tab):
    
    Country_data = Apple_Mobility_Data.loc[(Apple_Mobility_Data.region==country_name) & (Apple_Mobility_Data.transportation_type==mode)]
    united_state_data = Apple_Mobility_Data.loc[(Apple_Mobility_Data.region=='United States') & (Apple_Mobility_Data.transportation_type==mode)]
    fig= go.Figure()
    
    if tab =='state':
        fig.add_trace(go.Scatter(x=united_state_data['Date'], y=united_state_data['Change_from_Baseline'],
                    line = dict(color='#00CC96'),
                    name='US'))

    fig.add_trace(go.Scatter(x=Country_data['Date'], y=Country_data['Change_from_Baseline'],
                    line = dict(color='#636EFA'),
                    name='Mobility Trend'))
    fig.add_trace(go.Scatter(x=Country_data['Date'], y=Country_data['Baseline'],
                    line = dict(color='firebrick', width=1, dash='dash'),
                    name='Baseline'))



    fig.update_layout(margin={"r":20,"t":0,"l":0,"b":0},
                    paper_bgcolor = 'rgba(0,0,0,0)',
					plot_bgcolor = 'rgba(0,0,0,0)',
                    template='plotly_white',)

    fig.update_layout(
        #title_font_family='Century Gothic, sans-serif',
        #title_font_size = 15,
        #title_font_color = 'Black',
        yaxis = dict(
        title = 'Mobility Index',
        titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 10,
        color = 'Grey'
        ),

        ),

        xaxis = dict(  
        #title = 'Date',
        titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 11,
        color = 'Grey'
        ),



        ),


        legend = dict(
        #title = 'Filter Date',
        orientation="h",
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font = dict(
            family = 'Century Gothic, sans-serif',
            size = 10,
            color = 'Grey'
        )
        )
        
    )
    return fig


def country_comparison_bar_chart(country_name,mode):
    Locations = ['United States', 'United Kingdom', 'Brazil', 'Canada', 'India', 'South Africa']
    flag = 1
    x = country_name
    for var in Locations:
        if var == x:
            flag = 0

    if flag == 1:
        Locations.append(x)

    Filtered_df = pd.DataFrame()
    for var in Locations:
        Filtered_df = Filtered_df.append(Apple_Mobility_Data.loc[(Apple_Mobility_Data.region==var) & (Apple_Mobility_Data.transportation_type==mode) & (Apple_Mobility_Data.Date==max_value)])

    fig2 = go.Figure(go.Bar(x=Filtered_df['Change_from_Baseline'], y=Filtered_df['region'],orientation='h'))
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    paper_bgcolor = 'rgba(0,0,0,0)',
					plot_bgcolor = 'rgba(0,0,0,0)',
                    template='plotly_white',)

    for data in fig2.data:
        data["width"] = 0.15 #Change this value for bar widths

    fig2.update_layout(
        #title_font_family='Century Gothic, sans-serif',
        #title_font_size = 15,
        #title_font_color = 'Black',
        yaxis = dict(
        #title = ' ',
        titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 10,
        color = 'Grey'
        ),

        ),

        xaxis = dict(  
        #title = ' ',
         titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 11,
        color = 'Grey'
        ),



        ),
        
    )

 

    return fig2



def Google_Country_Data(country_name,location_type,tab):
    print("Entered")
    if tab=="country":
        Google_Filtered = Google_Data.loc[(Google_Data.country_region==country_name) & (Google_Data.sub_region_1=='0') & (Google_Data.sub_region_2=='0')]
    if tab=="state":
        Google_Filtered = Google_Data.loc[(Google_Data.sub_region_1==country_name) & (Google_Data.sub_region_2=='0')]
    #activity = ['Retail & Recreational', 'Grocery and Pharmacy', 'Parks', 'Transit Stations', 'Workplace', 'Residential']
    if location_type == 'Retail & Recreational':
        chart_type = 'retail_and_recreation_percent_change_from_baseline'
    elif location_type == 'Grocery and Pharmacy':
        chart_type = 'grocery_and_pharmacy_percent_change_from_baseline'
    elif location_type == 'Parks':
        chart_type = 'parks_percent_change_from_baseline'
    elif location_type == 'Transit Stations':
        chart_type = 'transit_stations_percent_change_from_baseline'
    elif location_type == 'Workplace':
        chart_type = 'workplaces_percent_change_from_baseline'
    elif location_type == 'Residential':
        chart_type = 'residential_percent_change_from_baseline'
    else:
        print('Invalid')
    
    fig3= go.Figure()
    fig3.add_trace(go.Scatter(x=Google_Filtered['date'], y=Google_Filtered[chart_type],
                    mode='lines',
                    name='lines'))
    fig3.update_layout(margin={"r":20,"t":0,"l":0,"b":0},
                    paper_bgcolor = 'rgba(0,0,0,0)',
					plot_bgcolor = 'rgba(0,0,0,0)',
                    template='plotly_white',)
    fig3.update_layout(
        #title_font_family='Century Gothic, sans-serif',
        #title_font_size = 15,
        #title_font_color = 'Black',
        yaxis = dict(
        #title = ' ',
        titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 10,
        color = 'Grey'
        ),

        ),

        xaxis = dict(  
        #title = ' ',
         titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 11,
        color = 'Grey'
        ),
        ),
        
    )
    return fig3


def Google_percentage(country_name,location_type,tab):
    if tab=="country":
        Google_Filtered = Google_Data.loc[(Google_Data.country_region==country_name) & (Google_Data.sub_region_1=='0') & (Google_Data.sub_region_2=='0') & (Google_Data.date==max_value_google)]
    if tab=="state":
        Google_Filtered = Google_Data.loc[(Google_Data.sub_region_1==country_name) & (Google_Data.sub_region_2=='0') & (Google_Data.date==max_value_google)]
    #activity = ['Retail & Recreational', 'Grocery and Pharmacy', 'Parks', 'Transit Stations', 'Workplace', 'Residential']
    if location_type == 'Retail & Recreational':
        chart_type = 'retail_and_recreation_percent_change_from_baseline'
    elif location_type == 'Grocery and Pharmacy':
        chart_type = 'grocery_and_pharmacy_percent_change_from_baseline'
    elif location_type == 'Parks':
        chart_type = 'parks_percent_change_from_baseline'
    elif location_type == 'Transit Stations':
        chart_type = 'transit_stations_percent_change_from_baseline'
    elif location_type == 'Workplace':
        chart_type = 'workplaces_percent_change_from_baseline'
    elif location_type == 'Residential':
        chart_type = 'residential_percent_change_from_baseline'
    else:
        print('Invalid')
    p = Google_Filtered[chart_type]
    percentage = p.values.tolist()
    percentage = str(percentage[0]) + '%'
    return percentage


def states_comparison(country_name,mode):
    us_state_data = Apple_State_Data.loc[(Apple_State_Data['transportation_type']==mode)&(Apple_State_Data['Date']==max_value)]
    us_state_data2 = us_state_data.loc[(us_state_data['region']!=country_name)]
    fig_state = go.Figure(go.Bar(x=us_state_data2['region'], y=us_state_data2['Change_from_Baseline'], marker_color='#eaeaea'))
    data_filtered = us_state_data.loc[(us_state_data['region']==country_name)]
    fig_state.add_trace(go.Bar(x=data_filtered['region'], y=data_filtered['Change_from_Baseline']))
    fig_state.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    paper_bgcolor = 'rgba(0,0,0,0)',
					plot_bgcolor = 'rgba(0,0,0,0)',
                    template='plotly_white',)

    for data in fig_state .data:
        data["width"] = 0.25 #Change this value for bar widths

    fig_state.update_layout(
        showlegend=False,
        #title_font_family='Century Gothic, sans-serif',
        #title_font_size = 15,
        #title_font_color = 'Black',
        yaxis = dict(
        #title = ' ',
        titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 10,
        color = 'Grey'
        ),

        ),

        xaxis = dict(  
        #title = ' ',
         titlefont = dict(
            family = 'Century Gothic, sans-serif',
            size = 12,
            color = 'Black'
        ),
        tickfont = dict(
        family = 'Century Gothic, sans-serif',
        size = 12,
        color = 'Grey'
        ),



        ),
        
    )

    fig_state.update_layout(xaxis={'categoryorder':'total descending'})

    return fig_state 


#########################################################
#
# endregion 
#
#########################################################


#########################################################
#
# region 1 - UI Development
#
#########################################################

#########################################################
#
# region 1-1 - Navigation Section
#
#########################################################

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
app.title = "COVID Dashbord"
app.layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.Img(src="/assets/Stantec-Logo.white.png", width="130",className="stantec_logo" ),
                html.P("Daily Mobility Index",className="nav_title")
            ],className="Nav_bar"),md=12),            
        ],no_gutters=True,
        ),
        

#########################################################
#
# region 1-2 - Filter Section
#
#########################################################



    dbc.Row([
        dbc.Col(html.Div([
            dbc.Row(
                        [
                                dbc.Col(html.Div(
                                        [
                                        html.H1("DATA MOBILITY INDEX DASHBOARD", className="Heading"),
                                        html.P("This site was designed to help you understand the chnage in traddic levels at the country and state level since early March. Select a state, country, and mode (driving,walking, or transit), and select the Main Chart tabs to view results. You can also view summmaries by state or metro areas", className="intro_p"),
                                        html.H1("LAST UPDATED",className="Slider_tag"),
                                        html.P("December 9th 2020",className="intro_p1"),
                                        html.H1("DATA THROUGH",className="Slider_tag"),
                                        html.P("December 9th 2020",className="intro_p1"),
                                        ],className="intro"                          
                                    )
                                )
                        ],className="Input_Container"
                        ),






              dbc.Row(
                        [
                                dbc.Col(html.Div(
                                        [
                                        html.H1("SELECT COUNTRY", className="Slider_tag"),
                                        dcc.Dropdown(
                                        id='Country',
                                        options=[
                                                    {'label': '2018', 'value': 2018},
                                                    {'label': '2019', 'value': 2019},
                                                    {'label': '2020', 'value': 2020}
                                                ],
                                        #value= 2020,
                                        multi=False
                                        ),
                                    ],className='sliderbox'    
                                    ),
                                ),
                        ],className="Filter_Block"
                        ),


             dbc.Row(
                        [
                                dbc.Col(html.Div(
                                        [
                                        html.H1("SELECT STATE", className="Slider_tag"),
                                        dcc.Dropdown(
                                        id='State_Dropdown',
                                        options=[
                                                    {'label': 'Alabama', 'value':  'Alabama'},
                                                    {'label': 'Alaska', 'value':  'Alaska'},
                                                    {'label': 'Arizona', 'value': 'Arizona'},
                                                    {'label': 'Arkansas', 'value': 'Arkansas'},
                                                    {'label': 'California', 'value': 'California'},
                                                    {'label': 'Colorado', 'value': 'Colorado'},
                                                    {'label': 'Connecticut', 'value': 'Connecticut'},
                                                    {'label': 'Delaware', 'value': 'Delaware'},
                                                    {'label': 'Florida', 'value': 'Florida'},
                                                    {'label': 'Georgia', 'value': 'Georgia'},
                                                    {'label': 'Hawaii', 'value': 'Hawaii'},
                                                    {'label': 'Idaho', 'value': 'Idaho'},
                                                    {'label': 'Illinois', 'value': 'Illinois'},
                                                    {'label': 'Indiana', 'value': 'Indiana'},
                                                    {'label': 'Iowa', 'value': 'Iowa'},
                                                    {'label': 'Kansas', 'value': 'Kansas'},
                                                    {'label': 'Louisiana', 'value': 'Louisiana'},
                                                    {'label': 'Maine', 'value': 'Maine'},
                                                    {'label': 'Maryland', 'value': 'Maryland'},
                                                    {'label': 'Massachusetts', 'value': 'Massachusetts'},
                                                    {'label': 'Michigan', 'value': 'Michigan'},
                                                    {'label': 'Minnesota', 'value': 'Minnesota'},
                                                    {'label': 'Mississippi', 'value': 'Mississippi'},
                                                    {'label': 'Missouri', 'value': 'Missouri'},
                                                    {'label': 'Montana', 'value': 'Montana'},
                                                    {'label': 'Nebraska', 'value': 'Nebraska'},
                                                    {'label': 'Nevada', 'value': 'Nevada'},
                                                    {'label': 'New Hampshire', 'value': 'New Hampshire'},
                                                    {'label': 'New Jersey', 'value': 'New Jersey'},
                                                    {'label': 'New Mexico', 'value': 'New Mexico'},
                                                    {'label': 'North Carolina', 'value': 'North Carolina'},
                                                    {'label': 'North Dakota', 'value': 'North Dakota'},
                                                    {'label': 'Ohio', 'value': 'Ohio'},
                                                    {'label': 'Oklahoma', 'value': 'Oklahoma'},
                                                    {'label': 'Oregon', 'value': 'Oregon'},
                                                    {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
                                                    {'label': 'Rhode Island', 'value': 'Rhode Island'},
                                                    {'label': 'South Carolina', 'value': 'South Carolina'},
                                                    {'label': 'South Dakota', 'value': 'South Dakota'},
                                                    {'label': 'Tennessee', 'value': 'Tennessee'},
                                                    {'label': 'Texas', 'value': 'Texas'},
                                                    {'label': 'Utah', 'value': 'Utah'},
                                                    {'label': 'Vermont', 'value': 'Vermont'},
                                                    {'label': 'Virginia', 'value': 'Virginia'},
                                                    {'label': 'Washington', 'value': 'Washington'},
                                                    {'label': 'West Virginia', 'value': 'West Virginia'},
                                                    {'label': 'Wisconsin', 'value': 'Wisconsin'},
                                                    {'label': 'Wyoming', 'value': 'Wyoming'},
                                                 ],
                                        #value= 2020,
                                        multi=False
                                        ),
                                    ],className='sliderbox'    
                                    ),
                                ),
                        ],className="Filter_Block"
                        ),

             dbc.Row(
                        [
                                dbc.Col(html.Div(
                                        [
                                        html.H1("SELECT COUNTY", className="Slider_tag"),
                                        dcc.Dropdown(
                                        id='County',
                                        options=[
                                                    {'label': '2018', 'value': 2018},
                                                    {'label': '2019', 'value': 2019},
                                                    {'label': '2020', 'value': 2020}
                                                ],
                                        #value= 2020,
                                        multi=False
                                        ),
                                    ],className='sliderbox'    
                                    ),
                                ),
                        ],className="Filter_Block"
                        ),

             dbc.Row(
                        [
                                dbc.Col(html.Div(
                                        [
                                        html.H1("SELECT MODE", className="Slider_tag"),
                                        dcc.Dropdown(
                                        id='Mode',
                                        options=[
                                                    {'label': 'Driving', 'value': 'driving'},
                                                    {'label': 'Walking', 'value': 'walking'},
                                                    {'label': 'Transit', 'value': 'transit'}
                                                ],
                                        value= 'driving',
                                        multi=False
                                        ),
                                    ],className='sliderbox'    
                                    ),
                                ),
                        ],className="Filter_Block"
                        ),




        ],className="Filter_Container"),md=2),

    

  
#########################################################
#
# region 1-4 - Tab Section
#
#########################################################


    dbc.Col(html.Div([

        dcc.Tabs([
        dcc.Tab(label='MAIN CHARTS', 
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            dbc.Row([
                    dbc.Col(html.Div([
                    dcc.Graph(id='map',figure=make_basemap(),
                    config={"autosizable":True,"scrollZoom": True, "displayModeBar": False})
                    ],className="plot_1"),md=4),
                    dbc.Col(html.Div([

                        dbc.Row([

                            dbc.Col(html.Div([

                                html.P( id="country", children = country_title(country_name)),

                            ],className="Country_Title"),md=12)
                        ]),
                        
                        dbc.Row([
                            dbc.Col(html.Div([


                                dcc.Graph(id='Apple_Country_Graph',figure=applemobility_country("United States","driving","country"))

                            ],className="Apple_country"),md=12)

                ])
                        


                    ]),md=5),

                    dbc.Col(html.Div([

                        dbc.Row([

                            dbc.Col(html.Div([


                                dcc.Graph(id='Country_Comparison_bar',figure=country_comparison_bar_chart("United States","driving"))
                            ]))
                        ])
                    ],className="Comparison_Bar"),md=3)
                
                    ],className="Row1"),

            dbc.Row([

                dbc.Col( html.Div([

                    html.H1("Location Activity Trends", className="Section_Heading"),
                ]),md=4),

                dbc.Col( html.Div([

                    dcc.Dropdown(
                                        id='Activity',
                                        options=[
                                                    {'label': 'Retail & Recreational', 'value': 'Retail & Recreational'},
                                                    {'label': 'Grocery and Pharmacy', 'value': 'Grocery and Pharmacy'},
                                                    {'label': 'Parks', 'value': 'Parks'},
                                                    {'label': 'Transit Stations', 'value': 'Transit Stations'},
                                                    {'label': 'Workplace', 'value': 'Workplace'},
                                                    {'label': 'Residential', 'value': 'Residential'},
                                                ],
                                        value= 'Retail & Recreational',
                                        multi=False
                                        ),
                ],className='sliderbox'),md=3)
            ],className="Row2"),
            
            dbc.Row([
                dbc.Col(html.Div([

                dcc.Graph(id='Activity_Charts',figure=Google_Country_Data("United States","Retail & Recreational","country"))

                ]),md=9),
                
                dbc.Col(html.Div([

                html.P( id="title"),
                html.Hr(),
                html.P( id="percentage", children = Google_percentage("United States","Retail & Recreational","country")),
                html.P("Compared to Baseline", className='note'),
                html.P("As of", className='note2',),
                html.P(className="datetime",children = max_value_google),

                ],className='percentage'),md=3)
            ],className="Row3")



        ]),

#########################################################
#
# region 1-4 - State Summary
#
#########################################################
        dcc.Tab(label='STATE SUMMARY', 
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            dbc.Row([
                dbc.Col(html.Div([
                dcc.Graph(id='map2',figure=make_statemap(),
                config={"autosizable":True,"scrollZoom": True, "displayModeBar": False})
                ],className="plot_1"),md=5),
                dbc.Col(html.Div([

                    dbc.Row([

                        dbc.Col(html.Div([

                            html.P( id="State", children = state_title(state_name)),

                        ],className="Country_Title"),md=12)
                        ]),
                        
                    dbc.Row([
                        dbc.Col(html.Div([


                        dcc.Graph(id='Apple_Country_Graph_State',figure=applemobility_country("California","driving","state"))

                        ],className="Apple_country2"),md=12)
                ]),

                dbc.Row([

                    dbc.Col(html.Div([
                        dcc.Graph(id="state_comparison",figure=states_comparison("California","driving"))

                    ],className="Apple_country2"),md=12)
                ])
                
                    ]),md=7),
            ],className="Row1"),

            dbc.Row([

                dbc.Col( html.Div([

                html.H1("Location Activity Trends", className="Section_Heading"),
            ]),md=4),

                dbc.Col( html.Div([
                    dcc.Dropdown(
                                id='Activity2',
                                options=[
                                            {'label': 'Retail & Recreational', 'value': 'Retail & Recreational'},
                                            {'label': 'Grocery and Pharmacy', 'value': 'Grocery and Pharmacy'},
                                            {'label': 'Parks', 'value': 'Parks'},
                                            {'label': 'Transit Stations', 'value': 'Transit Stations'},
                                            {'label': 'Workplace', 'value': 'Workplace'},
                                            {'label': 'Residential', 'value': 'Residential'},
                                        ],
                                        value= 'Retail & Recreational',
                                        multi=False
                                        ),
                ],className='sliderbox'),md=3)
            ],className="Row2"),
            
            dbc.Row([
                dbc.Col(html.Div([

                dcc.Graph(id='Activity_Charts_State',figure=Google_Country_Data("California","Retail & Recreational","state"))

                ]),md=9),
                
                dbc.Col(html.Div([

                html.P( id="title_state"),
                html.Hr(),
                html.P( id="percentage_state", children = Google_percentage("California","Retail & Recreational","state")),
                html.P("Compared to Baseline", className='note'),
                html.P("As of", className='note2',),
                html.P(className="datetime",children = max_value_google),
                ],className='percentage'),md=3)
            ],className="Row3")
        ]),

#########################################################
#
# region 1-4 - Metro Summary
#
#########################################################

        dcc.Tab(label='METRO AREA', 
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
#########################################################
#
# region 1-4 - Comparison Summary
#
#########################################################
        dcc.Tab(label='COMPARISON', 
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        ],className="Tab_Container"),

#########################################################
#
# endregion 
#
#########################################################


    
        ],className="Tab_Section"),md=10),
    



    ],no_gutters=True,
    ),


    ],
)



#########################################################
#
# region 4 - Callbacks
#
#########################################################


@app.callback(
    Output('country', 'children'),
    Input('map', 'clickData'))

def update_name(value):
    zone=value['points'][0]['location']
    print(zone)
    return country_title(zone)


@app.callback(
    Output('State', 'children'),
    Input('map2', 'clickData'))

def update_name_state(value):
    zone=value['points'][0]['location']
    print(zone)
    return state_title(zone)


@app.callback(
    Output('Apple_Country_Graph','figure'),
    Input ('map','clickData'), Input('Mode','value')
)

def update_country_mobility_chart(clickData,value):
    zone=clickData['points'][0]['location']
    return applemobility_country(zone,value,"country")


@app.callback(
    Output('Apple_Country_Graph_State','figure'),
    Input ('map2','clickData'), Input('Mode','value')
)

def update_country_mobility_chart_state(clickData,value):
    zone=clickData['points'][0]['location']
    return applemobility_country(zone,value,"state")


@app.callback(
    Output('Country_Comparison_bar','figure'),
    Input ('map','clickData'), Input('Mode','value')
)

def update_country_comparison_bar(clickData,value):
    zone=clickData['points'][0]['location']
    return country_comparison_bar_chart(zone,value)

@app.callback(
    Output('Activity_Charts','figure'),
    Input ('map','clickData'), Input('Activity','value')
)

def update_Google_Activity_Chart(clickData,value):
    zone=clickData['points'][0]['location']
    return Google_Country_Data(zone,value,"country")

@app.callback(
    Output('percentage','children'),
    Input ('map','clickData'), Input('Activity','value')
)

def update_Google_percentage(clickData,value):
    zone=clickData['points'][0]['location']
    return Google_percentage(zone,value,"country")



@app.callback(
    Output('Activity_Charts_State','figure'),
    Input ('map2','clickData'), Input('Activity2','value')
)

def update_Google_Activity_Chart_state(clickData,value):
    zone=clickData['points'][0]['location']
    return Google_Country_Data(zone,value,"state")

@app.callback(
    Output('percentage_state','children'),
    Input ('map2','clickData'), Input('Activity2','value')
)

def update_Google_percentage_state(clickData,value):
    zone=clickData['points'][0]['location']
    return Google_percentage(zone,value,"state")





@app.callback(
    Output('title','children'),
    Input('Activity','value')
)

def update_title(value):
    return value


@app.callback(
    Output('title_state','children'),
    Input('Activity2','value')
)

def update_title2(value):
    return value



@app.callback(
    Output('state_comparison','figure'),
    Input ('map2','clickData'), Input('Mode','value')
)

def comparison(clickData,value):
    zone=clickData['points'][0]['location']
    print("Inside callback")
    return states_comparison(zone,value)

#########################################################
#
# endregion 
#
#########################################################


if __name__ == "__main__":
    app.run_server()
