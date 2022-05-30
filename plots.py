import warnings
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly as pt
import pandas as pd
from get_date import get_date
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px



def get_chloro():
    d3 = datetime.today()-timedelta(days=2)
    d3=d3.strftime('%#m/%#d/%y')
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df1 = pd.read_csv('population_by_country_2020.csv')
    df = df.rename(columns= {"Country/Region" : "Country", "Province/State": "Province"})

    total_list = df.groupby('Country')[d3].sum().tolist()
    df1.sort_values(by=['Country'],inplace=True)
    df1.reset_index(inplace=True)
    listOfPop = []
    


    country_list = df["Country"].tolist()
    country_set = set(country_list)
    country_list = list(country_set)
    country_list.sort()

    new_df = pd.DataFrame(list(zip(country_list, total_list)), 
                columns =['Country', 'Total_Cases'])
    

    ab = pd.DataFrame()
    abc = pd.DataFrame()

    for i in new_df['Country']:
        ab = ab.append(df1.loc[df1['Country'] == i], ignore_index = True)
    for i in ab['Country']:
        abc = abc.append(new_df.loc[new_df['Country'] == i], ignore_index = True)
    ab.drop('index',axis=1,inplace=True)
    ab['Total_Cases'] = abc['Total_Cases']
    ab['Result'] = (ab['Total_Cases']/ab['Population'])*100
    ab.to_csv("NewUpdated.csv")


    colors = ["#F9F9F5", "#FAFAE6", "#FCFCCB", "#FCFCAE",  "#FCF1AE", "#FCEA7D", "#FCD97D",
            "#FCCE7D", "#FCC07D", "#FEB562", "#F9A648",  "#F98E48", "#FD8739", "#FE7519",
            "#FE5E19", "#FA520A", "#FA2B0A", "#9B1803",  "#861604", "#651104", "#570303",]


    fig = go.Figure(data=go.Choropleth(
        locationmode = "country names",
        locations = ab['Country'],
        z = ab['Result'],
        text = ab['Result'],
        #color='unemp',
        #color_continuous_scale="Viridis",
        colorscale = colors,
        #autocolorscale=True,
        #range_color=(0, 12),
        #reversescale=True,
        colorbar_title = 'Reported Covid-19 Cases per 100 Population'
    ))

    return fig

def get_chloro1():
    DF=pd.read_csv("country_vaccinations.csv")
    DF.fillna(0, inplace = True)
    DF.drop(DF.index[DF['iso_code'] == 0], inplace = True)
    DF['date'] =  pd.to_datetime(DF['date'], format='%Y-%m-%d')
    DF.drop(["people_fully_vaccinated","daily_vaccinations_raw","people_fully_vaccinated_per_hundred",
            "daily_vaccinations_per_million","people_vaccinated_per_hundred", "source_name","source_website"],axis=1, inplace=True)
    fig = px.choropleth(DF.reset_index(), locations="iso_code",
    color="total_vaccinations_per_hundred",
    color_continuous_scale=px.colors.diverging.BrBG,
    title= "Total vaccinations per 100")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) #No margin on left, right, top and bottom
    return fig


def get_vacc1():
    DF=pd.read_csv("country_vaccinations.csv")
    DF.fillna(0, inplace = True)
    DF.drop(DF.index[DF['iso_code'] == 0], inplace = True)
    DF['date'] =  pd.to_datetime(DF['date'], format='%Y-%m-%d')
    DF.drop(["people_fully_vaccinated","daily_vaccinations_raw","people_fully_vaccinated_per_hundred",
            "daily_vaccinations_per_million","people_vaccinated_per_hundred", "source_name","source_website"],axis=1, inplace=True)
    vacc_by_country = DF.groupby('country').max().sort_values('total_vaccinations', ascending=False)
    vacc_by_country = vacc_by_country.iloc[:10]
    vacc_by_country = vacc_by_country.sort_values('total_vaccinations_per_hundred', ascending=False)
    fig = plt.figure(figsize=(20, 12))
    plt.bar(vacc_by_country.index, vacc_by_country.total_vaccinations_per_hundred)
    plt.xticks(rotation = 90)
    plt.ylabel('Vaccinations per 100')
    plt.xlabel('Country')
    plt.title("TOP 10 COUNTRIES IN VACCINATION PER 100 POPULATION\n",
            size=15,color='#28a9ff')
    return fig

def get_vacc2():
    DF=pd.read_csv("country_vaccinations.csv")
    DF.fillna(0, inplace = True)
    DF.drop(DF.index[DF['iso_code'] == 0], inplace = True)
    DF['date'] =  pd.to_datetime(DF['date'], format='%Y-%m-%d')
    DF.drop(["people_fully_vaccinated","daily_vaccinations_raw","people_fully_vaccinated_per_hundred",
            "daily_vaccinations_per_million","people_vaccinated_per_hundred", "source_name","source_website"],axis=1, inplace=True)
    total_vacc_by_country = DF.groupby('country').max().sort_values('total_vaccinations', ascending=False)
    total_vacc_by_country = total_vacc_by_country.iloc[:10]
    fig = plt.figure(figsize=(20, 12))
    plt.bar(total_vacc_by_country.index, total_vacc_by_country.total_vaccinations)
    plt.title("TOTAL VACCINATIONS PER COUNTRY\n",
            size=15,color='#28a9ff')
    plt.xticks(rotation = 90)
    plt.ylabel('Total vaccinations')
    plt.xlabel('Country')
    return fig

def get_vacc3():
    DF=pd.read_csv("country_vaccinations.csv")
    DF.fillna(0, inplace = True)
    DF.drop(DF.index[DF['iso_code'] == 0], inplace = True)
    DF['date'] =  pd.to_datetime(DF['date'], format='%Y-%m-%d')
    DF.drop(["people_fully_vaccinated","daily_vaccinations_raw","people_fully_vaccinated_per_hundred",
            "daily_vaccinations_per_million","people_vaccinated_per_hundred", "source_name","source_website"],axis=1, inplace=True)
    vacc_names_by_country = DF.groupby('vaccines').max().sort_values('total_vaccinations', ascending=False)
    vacc_names_by_country = vacc_names_by_country.iloc[:10]
    vacc_names_by_country=vacc_names_by_country.reset_index()
    fig = plt.figure(figsize=(20,12))
    sns.barplot(data = vacc_names_by_country, x='vaccines', y = 'total_vaccinations', hue = 'country', dodge=False)
    plt.xticks(rotation=90)
    plt.title("TOP VACCINES IN TOP 10 CCOUNTRIES\n",
            size=15,color='#28a9ff')
    return fig



get_vacc1()
get_vacc2()
get_vacc3()