#from scancovia import ScanCovModel
#model = ScanCovModel()

import io
import base64
from flask import Flask,render_template,request,make_response,redirect,Response,render_template_string
import json
from get_data import get_data,fig_world_trend
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
from plots import get_chloro, get_vacc1, get_vacc2, get_vacc3, get_chloro1
from mortality import *
from coviddata import deaths,confirmed
import cv2
import os

import dash
from dash import Dash
from dash.dependencies import Input, State, Output
import dash_bootstrap_components as dbc
from dash_gui import fig_world_trend,generate_layout,generate_cards, fig_world_trend1
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from chatbot import get_response
from covid_xray import *

server = Flask(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
   __name__,
   server=server,
   url_base_pathname='/',
   suppress_callback_exceptions=True,
   external_stylesheets=external_stylesheets
)
app.layout = generate_layout()

@app.callback(
    [Output(component_id='graph1',component_property='figure'),
    Output(component_id='graph2',component_property='figure'), #line chart
    Output(component_id='card1',component_property='children')], #overall card numbers
    [Input(component_id='my-id1',component_property='value'), #dropdown
     Input(component_id='my-slider',component_property='value')] #slider
)
def update_output_div(input_value1,input_value2):
    return fig_world_trend(input_value1,input_value2),fig_world_trend1(input_value1,input_value2),generate_cards(input_value1)

# @server.route("/")
# def index():
#     return render_template('home.html')

# @app.route("/home")
# def home():
#     return render_template('home.html')


@server.route("/stats/", methods=["GET", "POST"])
def notdash11():
    return render_template('stats.html',PageTitle = "COVID-19 Stats")

@server.route('/stats.png')
def stats():
    fig = Stats()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@server.route("/plots/")
def notdash():
    return render_template('plots.html',PageTitle = "COVID-19 Plots")

@server.route("/vacc1/")
def notdash1():
    return render_template('vacc1.html',PageTitle = "COVID-19 Plots")

@server.route("/vacc2/")
def notdash2():
    return render_template('vacc2.html',PageTitle = "COVID-19 Plots")

@server.route("/vacc3/")
def notdash3():
    return render_template('vacc3.html',PageTitle = "COVID-19 Plots")

@server.route("/deaths/")
def notdash4():
    return render_template('deaths.html',PageTitle = "COVID-19 Plots")

@server.route("/mortality/")
def notdash5():
    return render_template('mortality.html',PageTitle = "COVID-19 Plots")

@server.route('/vacc1.png')
def vacc1_png():
    fig = get_vacc1()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@server.route('/vacc2.png')
def vacc2_png():
    fig = get_vacc2()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@server.route('/vacc3.png')
def vacc3_png():
    fig = get_vacc3()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@server.route('/confirmed.png')
def confirmed_png():
    fig = confirmed()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@server.route('/deaths.png')
def deaths_png():
    fig = deaths()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@server.route("/chloro", methods=["GET", "POST"])
def chloro():
    fig = get_chloro()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('chloro.html', graphJSON=graphJSON)

@server.route("/chloro1", methods=["GET", "POST"])
def chloro1():
    fig = get_chloro1()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('chloro1.html', graphJSON=graphJSON)

@server.route("/xray")
def xray():
    return render_template('covid_xray.html')

@server.route("/xray_result", methods=["POST"])
def xray_result():
    if request.method == 'POST':
        f = request.files['xray']
        f.save(f.filename)
        res = xray_predict(f.filename)
        os.remove(f.filename)
        #x = cv2.imread(f.filename)
        #x=x/255
        #x = cv2.resize(x,(224,224))
        #x = np.expand_dims(x, axis=0)
        #res = xray_predict(x)    
        return render_template('result.html',prediction = res)
    
def severity_pred(val):
    print(val)
    risk_val = model(val)
    return risk_val

@server.route("/severity")
def mortality():
    return render_template('severity_form.html')

def conv(di):
    for key,value in di.items():
        if key in ['Age','Sex','SARS-CoV-2 nucleic acids','Computed tomography (CT)']:
            di[key] = int(value)
        else:
            di[key] = float(value)
    return di

@server.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        del to_predict_list['upload']
        to_predict_list = conv(to_predict_list)      
        prediction = ClinicalPredict(to_predict_list)
        print('############################')
        print(prediction)
        return render_template('result.html',prediction=prediction)

@server.route("/chatbot")
def chatbot():
    return render_template('chatbot.html')

@server.route("/getBotResponse")
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))  

if __name__ == '__main__':
    server.run(debug=True)