import pandas as pd
##pd.set_option('max_rows',20)
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

import dash
from dash.dependencies import Input, Output
from dash import dcc,html
import dash_bootstrap_components as dbc


CONF_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
DEAD_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
RECV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

covid_conf_ts = pd.read_csv(CONF_URL)
covid_dead_ts = pd.read_csv(DEAD_URL)
covid_recv_ts = pd.read_csv(RECV_URL)

#get data in cleaned time series format for country
def process_data(data,cntry='India',window=3):
    conf_ts = data
    conf_ts_cntry = conf_ts[conf_ts['Country/Region']==cntry]
    final_dataset = conf_ts_cntry.T[4:].sum(axis='columns').diff().rolling(window=window).mean()[40:]
    df = pd.DataFrame(final_dataset,columns=['Total'])
    return df

    #get overall wordlwide total for confirmed, recovered and dead cases
def get_overall_total(df):
    return df.iloc[:,-1].sum()

conf_overall_total = get_overall_total(covid_conf_ts)
dead_overall_total = get_overall_total(covid_dead_ts)
mort_overall_total = round((dead_overall_total/conf_overall_total)*100,5)

def get_cntry_total(df,cntry='India'):
    return df[df['Country/Region']==cntry].iloc[:,-1].sum()
    

def fig_world_trend(cntry='India',window=3):
    df = process_data(data=covid_conf_ts,cntry=cntry,window=window)
    df.head(10)
    if window==1:
        yaxis_title = "Daily Cases"
    else:
        yaxis_title = "Daily Cases ({}-day MA)".format(window)
    fig = px.line(df, y='Total', x=df.index, title='Daily confirmed cases trend for {}'.format(cntry),height=600,color_discrete_sequence =['maroon'])
    fig.update_layout(title_x=0.5,plot_bgcolor='#85DCBA',paper_bgcolor='#85DCBA',xaxis_title="Date",yaxis_title=yaxis_title)
    return fig

def fig_world_trend1(cntry='India',window=3):
    df = process_data(data=covid_dead_ts,cntry=cntry,window=window)
    df.head(10)
    if window==1:
        yaxis_title = "Daily Deaths"
    else:
        yaxis_title = "Daily Deaths ({}-day MA)".format(window)
    fig = px.line(df, y='Total', x=df.index, title='Daily Death cases trend for {}'.format(cntry),height=600,color_discrete_sequence =['maroon'])
    fig.update_layout(title_x=0.5,plot_bgcolor='#85DCBA',paper_bgcolor='#85DCBA',xaxis_title="Date",yaxis_title=yaxis_title)
    return fig

external_stylesheets = [dbc.themes.BOOTSTRAP]

sidebar = html.Div(
    [

        dbc.Nav([
                dbc.NavLink("Covid Dashboard", href="/", active="exact", className="navbar-brand" ,external_link=True), 
                dbc.NavLink("Plots", href="/plots", active="exact" ,external_link=True),
                dbc.NavLink("Choropleth", href="/chloro", active="exact",external_link=True) ,
                dbc.NavLink("Covid Detection", href="/xray", active="exact",external_link=True) ,
                dbc.NavLink("Severity Prediction", href="/severity", active="exact",external_link=True) ,
                dbc.NavLink("Support", href="/chatbot", active="exact",external_link=True) ,
            ],
            className="navbar navbar-expand-md navbar-dark bg-dark mb-4"
        ),
    ],
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid-19 Dashboard'    

colors = {
    'background': '#85DCBA',
    'bodyColor':'#85DCBA',
    'text': '#7FDBFF'
}

def get_page_heading_style():
    return {'backgroundColor': colors['background']}


def get_page_heading_title():
    return html.H1(children='COVID-19 Dashboard',
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    })

def get_page_heading_subtitle():
    return html.Div(children='Visualize Covid-19 data generated from sources all over the world.',
                                         style={
                                             'textAlign':'center',
                                             'color':colors['text']
                                         })

def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    subtitle_header = dbc.Row(
                            [
                                dbc.Col(get_page_heading_subtitle(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    header = (main_header,subtitle_header)
    return header

def get_country_list():
    return covid_conf_ts['Country/Region'].unique()

def create_dropdown_list(cntry_list):
    dropdown_list = []
    for cntry in sorted(cntry_list):
        tmp_dict = {'label':cntry,'value':cntry}
        dropdown_list.append(tmp_dict)
    return dropdown_list

def get_country_dropdown(id):
    return html.Div([
                        html.Label('Select Country'),
                        dcc.Dropdown(id='my-id'+str(id),
                            options=create_dropdown_list(get_country_list()),
                            value='India'
                        ),
                        html.Div(id='my-div'+str(id))
                    ])
            
def graph1():
    return dcc.Graph(id='graph1',figure=fig_world_trend('India'),config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','toggleSpikelines','hoverClosestCartesian','hoverCompareCartesian'],'displaylogo': False})

def graph2():
    return dcc.Graph(id='graph2',figure=fig_world_trend1('India'),config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','toggleSpikelines','hoverClosestCartesian','hoverCompareCartesian'],'displaylogo': False})

def generate_card_content(card_header,card_value,overall_value):
    card_head_style = {'textAlign':'center','fontSize':'150%'}
    card_body_style = {'textAlign':'center','fontSize':'200%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f"{card_value:,}", className="card-title",style=card_body_style),
            html.P(
                "Worlwide: {:,}".format(overall_value),
                className="card-text",style={'textAlign':'center'}
            ),
        ]
    )
    card = [card_header,card_body]
    return card

def generate_cards(cntry='India'):
    conf_cntry_total = get_cntry_total(covid_conf_ts,cntry)
    dead_cntry_total = get_cntry_total(covid_dead_ts,cntry)
    mort_cntry_total = round((dead_cntry_total/conf_cntry_total)*100,5) 
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("Confirmed",conf_cntry_total,conf_overall_total), color="danger", inverse=True),md=dict(size=2,offset=3)),
                    dbc.Col(dbc.Card(generate_card_content("Dead",dead_cntry_total,dead_overall_total),color="dark", inverse=True),md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Mortality Rate",mort_cntry_total,mort_overall_total), color="#036bfc", inverse=True),md=dict(size=2)),
                ],
                className="mb-4",
            ),
        ],id='card1'
    )
    return cards

def get_slider():
    return html.Div([  
                        dcc.Slider(
                            id='my-slider',
                            min=1,
                            max=15,
                            step=None,
                            marks={
                                1: '1',
                                3: '3',
                                5: '5',
                                7: '1-Week',
                                14: 'Fortnight'
                            },
                            value=3,
                        ),
                        html.Div([html.Label('Select Moving Average Window')],id='my-div'+str(id),style={'textAlign':'center'})
                    ])

def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [   sidebar,
            generate_cards(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(get_country_dropdown(id=1),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
            [
                    dbc.Col(graph1(),md=dict(size=6,offset=0)),
                    dbc.Col(graph2(),md=dict(size=6,offset=0))
            ],
            align="center",
            ),

            
            dbc.Row(
                [
                    dbc.Col(get_slider(),md=dict(size=4,offset=4))                    
                ]
            
            ),
        ],fluid=True,style={'backgroundColor': colors['bodyColor']}
    )
    return layout
