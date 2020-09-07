# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 20:56:03 2020

@author: DELLRJ5999
"""
import pandas as pd
import dash
import dash_html_components as html
import webbrowser
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate

app=dash.Dash()


def openbro():
    webbrowser.open_new("http://127.0.0.1:8050/")
    
def creatapp():
    main_layout=html.Div([html.Div([ html.H1(id="main_title",children="Terrorism Analysis with Insights"),
                                   html.Img(src="/assets/terrorism.png")],className="Top"),
      html.Div([dcc.Tabs(id="Tabs", value="tab-1",children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="tab-1" ,className="Tab1",children=[
      dcc.Tabs(id = "subtabs", value = "tab-1",children = [
              dcc.Tab(label="World Map tool", id="World", value="tab-1",className="Tab1"),
              dcc.Tab(label="India Map tool", id="India", value="tab-2",className="Tab1")
                ]
                )]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", className="Tab1",children=[
      dcc.Tabs(id = "subtabs2", value = "tab-2",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="tab-3",className="Tab1"),
              dcc.Tab(label="India Chart tool", id="IndiaC", value="tab-4",className="Tab1")]),
              html.Div()
              ])])],className="tab"),html.Div(id="content")],style={ 'background-color': 'rgb(66,196,247)', 'margin': '0px -10px 10px'}
)
    
    return main_layout



@app.callback(
    dash.dependencies.Output('map', 'children'),
    [
    dash.dependencies.Input('month-dropdown', 'value'),
    dash.dependencies.Input('day-dropdown', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attack-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input("Tabs", "value")
     ]
    )
def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,tab):
    print("Data Type of month value = " , str(type(month_value)))
    print("Data of month value = " , month_value)

    print("Data Type of Day value = " , str(type(date_value)))
    print("Data of Day value = " , date_value)

    print("Data Type of region value = " , str(type(region_value)))
    print("Data of region value = " , region_value)

    print("Data Type of country value = " , str(type(country_value)))
    print("Data of country value = " , country_value)

    print("Data Type of state value = " , str(type(state_value)))
    print("Data of state value = " , state_value)

    print("Data Type of city value = " , str(type(city_value)))
    print("Data of city value = " , city_value)

    print("Data Type of Attack value = " , str(type(attack_value)))
    print("Data of Attack value = " , attack_value)

    print("Data Type of year value = " , str(type(year_value)))
    print("Data of year value = " , year_value)
  
    year_range = range(year_value[0], year_value[1]+1)
    df3= df[df["iyear"].isin(year_range)]
    
 
  
    if(month_value):
        df3 =  df3[df3["imonth"].isin(month_value)]
    if(date_value):
        df3 =  df3[(df3["iday"].isin(date_value)) & ( df["imonth"].isin(month_value))]
  
    if(tab=="tab-1"):
        if(region_value):
            df3 =  df3[df3['region_txt'].isin(region_value)]
        if(country_value):
            df3 =  df3[(df3["country_txt"].isin(country_value)) & (df3['region_txt'].isin(region_value))]
        if(state_value):
            df3 =  df3[(df3['provstate'].isin(state_value)) & (df3["country_txt"].isin(country_value)) & (df3['region_txt'].isin(region_value)) ] 
        if(city_value):
            df3 =  df3[(df3["city"].isin(city_value)) & (df3['provstate'].isin(state_value)) & (df3["country_txt"].isin(country_value)) & (df3['region_txt'].isin(region_value))]
 
        if(attack_value):
            df3 =  df3[df3["attacktype1_txt"].isin(attack_value)]
  
        figure = go.Figure()
        if df3.shape[0]:
            pass
        else:
            df3 = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
           'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            df3.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
     
        print(df3)
        figure = px.scatter_mapbox(df3,
                      lat="latitude", 
                      lon="longitude",
                      color="attacktype1_txt",
                      hover_name="city", 
                      hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                      zoom=1
                      )                       
        figure.update_layout(mapbox_style="stamen-terrain",
                  autosize=True,
                  margin=dict(l=0, r=0, t=25, b=20),
                  )
      
        return   dcc.Graph(figure=figure)
    else:
        return  None


#stype=["open-street-map","white-bg","carto-positron","carto-darkmatter","stamen-terrain","stamen-toner","stamen-watercolor"]


@app.callback(
    dash.dependencies.Output('graph', 'children'),
    [
    dash.dependencies.Input('chart-d', 'value'),
    dash.dependencies.Input('input', 'value'),
    dash.dependencies.Input("subtabs2", "value"),
    dash.dependencies.Input("Tabs", "value")
     ])

def update_ui(chart_value,input_value,tab2,maintab):
    print("Data Type of Type value = " , str(type(chart_value)))
    print("Data of Type value = " , chart_value)

    print("Data Type of Filter value = " , str(type(input_value)))
    print("Data of Filter value = " , input_value)
    
    print("Data Type of tab value = " , str(type(tab2)))
    print("Data of tab value = " , tab2)
    
    print("Data Type of Mtab value = " , str(type(maintab)))
    print("Data of Mtab value = " , maintab)
    
    
    df0=df
    if(tab2=="tab-3"):
        df0=df
    elif(tab2=="tab-4"):
        df0=df.country_txt=="India"
        df0=df[df0]
        
    print(df0)
    if(chart_value=="Terrorist Organization"):
        col="gname"
    elif(chart_value=="Target Nationality"):
        col="natlty1_txt"
    elif(chart_value=="Target Type"):
        col="targtype1_txt"
    elif(chart_value=="Type of Attack"):
        col="attacktype1_txt"
    elif(chart_value=="Weapon Type"):
        col="weaptype1_txt"
    elif(chart_value=="Region"):
        col="region_txt"
    elif(chart_value=="Country Attacked"):
        col='country_txt'
    
    if input_value==None:
        dfchart =df0.groupby("iyear")[col].value_counts().reset_index(name = "count")
        
    else:
        dfchart = df0.groupby("iyear")[col].value_counts().reset_index(name="count")
        dfchart= dfchart[dfchart[col].str.contains(input_value, case = False)]
        
    print(dfchart)
    fig = px.area(dfchart, x="iyear", y="count", color=col)

    
    
    return   dcc.Graph(figure=fig)
    





@app.callback(Output("content", "children"),
              [Input("Tabs", "value")])
def update_data(tab_value):
    data = None
    if tab_value =="tab-1":
        data =  html.Div([
        html.Br(),
        html.Div([
        html.Div([dcc.Dropdown(id="month-dropdown",options=month_list,placeholder="Select Month",multi = True,style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="day-dropdown",options=date_list,placeholder="Select Day",multi = True,style={'font-family': 'Charcoal, sans-serif'})],className="d1"),
        html.Div([dcc.Dropdown(id="region-dropdown",options=region_list,placeholder="Select Region",multi = True,style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="country-dropdown",options=[{'label':"All" , 'value':"All"}],placeholder="Select Country",multi = True,style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="state-dropdown",options=[{'label': 'All', 'value': 'All'}],placeholder="Select State or Province",multi = True,style={'font-family': 'Charcoal, sans-serif'})],className="d2"),
        html.Div([dcc.Dropdown(id="city-dropdown",options=[{'label': 'All', 'value': 'All'}],placeholder="Select City",multi = True,style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="attack-dropdown",options=attack_type_list,placeholder="Select Attack Type",multi = True,style={'font-family': 'Charcoal, sans-serif'})],className="d3")],className="row"),
        #dcc.mapbox_style(id="map"),
        #html.Hr(),
        html.Div([html.H3('Select the Year:', id='year_title',style={'margin-left': '1%','font-family': 'Charcoal, sans-serif'}),
        dcc.RangeSlider(id="year-slider",min=min(year_list),max=max(year_list),value=[min(year_list),max(year_list)],marks=iyear_list)],className="d4"),
        html.Hr(),
        html.Center(html.Div(id='map', children = ["Map is loading"],style={'font-family': 'Charcoal, sans-serif'}))
        ])
        
        
    elif(tab_value=="Chart"):
        data=html.Div([
             html.Br(),
             html.Div(dcc.Dropdown(id="chart-d",options=typedict,placeholder="Select...",value='Region'),style={'margin-left': '1%',"margin-right": "50%"}),
             html.Br(),
             html.Div(dcc.Input(id="input",placeholder='Search Filter',type='text',value=''),style={'margin-left': '1%'}), 
             html.Hr(),
             html.Center(html.Div(id='graph', children = ["Graph is loading"],style={'font-family': 'Charcoal, sans-serif'}))
            ])
    else:
        pass
    return data

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "tab-1":
        pass
    elif tab=="tab-2":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
  Output("day-dropdown", "options"),
  [
  Input("month-dropdown", "value")
  ]
  )
def update_date(month):
    date_list = [x for x in range(1, 32)]

    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option


@app.callback(
    Output('country-dropdown', 'options'),
    [
    Input('region-dropdown', 'value')
    ]
    )
def set_country_options(region_value):
    option = []
    
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]





@app.callback(
    Output('state-dropdown', 'options'),
    [
    Input('country-dropdown', 'value')
    ]
    )
def set_state_options(country_value):

    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]



@app.callback(
    Output('city-dropdown', 'options'),
    [
    Input('state-dropdown', 'value')
    ]
    )
def set_city_options(state_value):

    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]




    
def loaddata():
    pd.options.mode.chained_assignment = None
    global df
    global country_list
    global iyear_list
    global year_list
    
    df=pd.read_csv("global_terror.csv")
    
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }
    typelist=["Terrorist Organization","Target Nationality","Target Type","Type of Attack","Weapon Type","Region","Country Attacked"]

    global typedict
    typedict=[{"label":x, "value":x} for x in typelist]

    global month_list
    month_list= [{"label":key, "value":values} for key,values in month.items()]
    
    global date_list
    date_list = [{"label":x, "value":x} for x in range(1, 32)] 
    
    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
    
    #print(df.columns)
    #print(df.sample(5))
    #temp_list=sorted(df["country_txt"].unique().tolist())
    global year_list
    year_list=sorted(df["iyear"].unique().tolist())
    #country_list=[{"label":str(i),"value":str(i)} for i in temp_list]
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

    iyear_list={str(i):str(i) for i in year_list}
    
    
def main():
    print("Hello")
    
    loaddata()
    openbro()  
    global app
    app.layout=creatapp()
    app.title="Terrorism Analysis"
    app.run_server()
    
    #df=pd.read_csv("data1.csv")
    
    #print(df.columns)
    print("Hello   BYE")
    app=None
    df=None
    
if __name__=="__main__":
    main()
    
    
