from urllib import request
from flask import (Flask, g, redirect, render_template, request, session, url_for, flash)
from flask_sqlalchemy import SQLAlchemy
import folium
from folium.plugins import HeatMap
import sqlite3
import itertools
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib
from pmdarima import auto_arima
import matplotlib.pyplot as plt
from flask import Flask

plt.style.use('fivethirtyeight')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
import warnings

warnings.filterwarnings("ignore")
from statsmodels.tsa.arima.model import ARIMA

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = [User(id=1, username='Admin', password='password'),
         User(id=2, username='Aryen', password='secret'),
         User(id=3, username='Carlos', password='somethingsimple')]

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(100))
    date_report = db.Column(db.String(100))
    location = db.Column(db.String(100))
    site = db.Column(db.String(100))
    no_observation = db.Column(db.Integer)
    mode_observation = db.Column(db.String(100))
    threats = db.Column(db.String(100))
    remarks = db.Column(db.String(1000))
    name_observers = db.Column(db.String(500))
    coordinates_lat = db.Column(db.Float)
    coordinates_lng = db.Column(db.Float)

    def __init__(self, species_name, date_report, location, site, no_observation, mode_observation, threats, remarks,
                 name_observers, coordinates_lat, coordinates_lng):
        self.species_name = species_name
        self.date_report = date_report
        self.location = location
        self.site = site
        self.no_observation = no_observation
        self.mode_observation = mode_observation
        self.threats = threats
        self.remarks = remarks
        self.name_observers = name_observers
        self.coordinates_lat = coordinates_lat
        self.coordinates_lng = coordinates_lng


class Population(db.Model):
    population_id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(100))
    pop_name = db.Column(db.String(100))
    pop_date = db.Column(db.String(100))
    population_no = db.Column(db.Integer)
    park_add = db.Column(db.String(100))

    def __init__(self, park_name, pop_name, pop_date, population_no, park_add):
        self.park_name = park_name
        self.pop_name = pop_name
        self.pop_date = pop_date
        self.population_no = population_no
        self.park_add = park_add


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/home')
def index():  # put application's code here
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/Profile:Writhed_Hornbill')
def hornbill():  # put application's code here
    all_data = Data.query
    return render_template('hornbill.html', data=all_data)


@app.route('/Profile:Spotted Deer')
def deer():  # put application's code here
    return render_template('deer.html')


@app.route('/Profile:Warty Pig')
def warty():  # put application's code here
    return render_template('warty.html')


@app.route('/Profile:Monitor Lizard')
def lizard():  # put application's code here
    return render_template('lizard.html')


@app.route('/Profile:Rafflesia speciosa')
def rafflesia():  # put application's code here
    return render_template('rafflesia.html')


@app.route('/data2')
def data2():  # put application's code here

    return render_template('data2.html')


@app.route('/data')
def data():  # put application's code here

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    query = "SELECT * FROM Data"
    cursor.execute(query)
    result = cursor.fetchall()
    for item in result:
        print(item)
    df = pd.read_sql_query(query, connection)
    df
    df.to_csv('data.csv')

    cursor.close()

    all_data = Data.query
    return render_template('data.html', data=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        species_name = request.form['species_name']
        date_report = request.form['date_report']
        location = request.form['location']
        site = request.form['site']
        no_observation = request.form['no_observation']
        mode_observation = request.form['mode_observation']
        threats = request.form['threats']
        remarks = request.form['remarks']
        name_observers = request.form['name_observers']
        coordinates_lat = request.form['coordinates_lat']
        coordinates_lng = request.form['coordinates_lng']

        my_data = Data(species_name, date_report, location, site, no_observation, mode_observation, threats, remarks,
                       name_observers, coordinates_lat, coordinates_lng)
        db.session.add(my_data)
        db.session.commit()

        flash("Report Entry Added Successfully")

        return redirect(url_for('data'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('report_id'))

        my_data.species_name = request.form['species_name']
        my_data.date_report = request.form['date_report']
        my_data.location = request.form['location']
        my_data.site = request.form['site']
        my_data.no_observation = request.form['no_observation']
        my_data.mode_observation = request.form['mode_observation']
        my_data.threats = request.form['threats']
        my_data.remarks = request.form['remarks']
        my_data.name_observers = request.form['name_observers']
        my_data.coordinates_lat = request.form['coordinates_lat']
        my_data.coordinates_lng = request.form['coordinates_lng']

        db.session.commit()
        flash("Report Entry Updated Successfully")

        return redirect(url_for('data'))


@app.route('/delete/<report_id>/', methods=['GET', 'POST'])
def delete(report_id):
    my_data = Data.query.get(report_id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Report Entry Deleted Successfully")

    return redirect(url_for('data'))


@app.route('/popdata')
def popdata():  # put application's code here
    pp_data = Population.query

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    query = "SELECT * FROM Population"
    cursor.execute(query)
    result = cursor.fetchall()
    for item in result:
        print(item)
    df = pd.read_sql_query(query, connection)
    df.to_csv('popdata.csv')

    cursor.close()
    return render_template('popdata.html', pop=pp_data)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        park_name = request.form['park_name']
        pop_name = request.form['pop_name']
        pop_date = request.form['pop_date']
        population_no = request.form['population_no']
        park_add = request.form['park_add']

        pop_data = Population(park_name, pop_name, pop_date, population_no, park_add)
        db.session.add(pop_data)
        db.session.commit()

        flash("Report Entry Added Successfully")

        return redirect(url_for('popdata'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        pop_data = Population.query.get(request.form.get('population_id'))

        pop_data.species_name = request.form['park_name']
        pop_data.pop_name = request.form['pop_name']
        pop_data.pop_date = request.form['pop_date']
        pop_data.population_no = request.form['population_no']
        pop_data.park_add = request.form['park_add']

        db.session.commit()
        flash("Report Entry Updated Successfully")

        return redirect(url_for('popdata'))


@app.route('/delt/<population_id>/', methods=['GET', 'POST'])
def delt(population_id):
    pop_data = Population.query.get(population_id)
    db.session.delete(pop_data)
    db.session.commit()
    flash("Report Entry Deleted Successfully")

    return redirect(url_for('popdata'))


@app.route('/Mapping')
def mapping():
    return render_template('map.html')


@app.route('/Hornbill Mapping')
def Hmapping():
    return render_template('hmap.html')


@app.route('/Deer Mapping')
def Dmapping():
    return render_template('dmap.html')


@app.route('/Warty Mapping')
def Wmapping():
    return render_template('wmap.html')


@app.route('/Rafflesia Mapping')
def Rmapping():
    return render_template('rmap.html')


@app.route('/RSmap')
def RSmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Raflesia speciosa (Panay Rafflesia)"]

    PANAY = [11.102947, 122.516279]
    Map = folium.Map(PANAY, zoom_start=9, tiles='Stamen Terrain')
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]["coordinates_lat"], data.iloc[i]["coordinates_lng"]],
                      tooltip=data.iloc[i]["species_name"],
                      popup='Date:''<br>' + str(data.iloc[i]["date_report"]) + '<br>''Sightings:''<br>' + str(
                          data.iloc[i]["no_observation"])).add_to(Map)
    Map.save('templates/RSmap.html')
    return render_template('RSmap.html')


@app.route('/WSmap')
def WSmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Sus cebifrons (Visayan Warty Pig)"]

    PANAY = [11.102947, 122.516279]
    Map = folium.Map(PANAY, zoom_start=9, tiles='Stamen Terrain')
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]["coordinates_lat"], data.iloc[i]["coordinates_lng"]],
                      tooltip=data.iloc[i]["species_name"],
                      popup='Date:''<br>' + str(data.iloc[i]["date_report"]) + '<br>''Sightings:''<br>' + str(
                          data.iloc[i]["no_observation"])).add_to(Map)
    Map.save('templates/WSmap.html')
    return render_template('WSmap.html')


@app.route('/DSmap')
def DSmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Rusa alfredi (Visayan Spotted Deer)"]

    PANAY = [11.102947, 122.516279]
    Map = folium.Map(PANAY, zoom_start=9, tiles='Stamen Terrain')
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]["coordinates_lat"], data.iloc[i]["coordinates_lng"]],
                      tooltip=data.iloc[i]["species_name"],
                      popup='Date:''<br>' + str(data.iloc[i]["date_report"]) + '<br>''Sightings:''<br>' + str(
                          data.iloc[i]["no_observation"])).add_to(Map)
    Map.save('templates/DSmap.html')
    return render_template('DSmap.html')


@app.route('/HSmap')
def HSmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]

    PANAY = [11.102947, 122.516279]
    Map = folium.Map(PANAY, zoom_start=9, tiles='Stamen Terrain')
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]["coordinates_lat"], data.iloc[i]["coordinates_lng"]],
                      tooltip=data.iloc[i]["species_name"],
                      popup='Date:''<br>' + str(data.iloc[i]["date_report"]) + '<br>''Sightings:''<br>' + str(
                          data.iloc[i]["no_observation"])).add_to(Map)
    Map.save('templates/HSmap.html')
    return render_template('HSmap.html')


@app.route('/RHmap')
def RHmap():
    data = pd.read_csv('data.csv')
    data2 = data[data['species_name'] == "Raflesia speciosa (Panay Rafflesia)"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=10, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data2['coordinates_lat'] = data2['coordinates_lat'].astype(float)
    data2['coordinates_lng'] = data2['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data2
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    # Plot it on the map
    HeatMap(heat_data).add_to(Hmap)

    # Display the map
    Hmap.save('templates/RHmap.html')
    return render_template('RHmap.html')


@app.route('/WHmap')
def WHmap():
    data = pd.read_csv('data.csv')
    data2 = data[data['species_name'] == "Sus cebifrons (Visayan Warty Pig)"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=10, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data2['coordinates_lat'] = data2['coordinates_lat'].astype(float)
    data2['coordinates_lng'] = data2['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data2
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(Hmap)

    # Display the map
    Hmap.save('templates/WHmap.html')
    return render_template('WHmap.html')


@app.route('/DHmap')
def DHmap():
    data = pd.read_csv('data.csv')
    data2 = data[data['species_name'] == "Rusa alfredi (Visayan Spotted Deer)"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=10, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data2['coordinates_lat'] = data2['coordinates_lat'].astype(float)
    data2['coordinates_lng'] = data2['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data2
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(Hmap)
    Hmap.save('templates/DHmap.html')
    return render_template('DHmap.html')


@app.route('/HHmap')
def HHmap():
    data = pd.read_csv('data.csv')
    data2 = data[data['species_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data2['coordinates_lat'] = data2['coordinates_lat'].astype(float)
    data2['coordinates_lng'] = data2['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data2
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(Hmap)
    Hmap.save('templates/HHmap.html')
    return render_template('HHmap.html')


@app.route('/TLHmap')
def TLHmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]
    data = data[data['threats'] == "Loss of Habitat"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/TLHmap.html')
    return render_template('TLHmap.html')


@app.route('/THHmap')
def THHmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]
    data = data[data['threats'] == "Hunting"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/THHmap.html')
    return render_template('THHmap.html')


@app.route('/TLWmap')
def TLWmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Sus cebifrons (Visayan Warty Pig)"]
    data = data[data['threats'] == "Loss of Habitat"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/TLWmap.html')
    return render_template('TLWmap.html')


@app.route('/THWmap')
def THWmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Sus cebifrons (Visayan Warty Pig)"]
    data = data[data['threats'] == "Hunting"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/THWmap.html')
    return render_template('THWmap.html')


@app.route('/TLDmap')
def TLDmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Rusa alfredi (Visayan Spotted Deer)"]
    data = data[data['threats'] == "Loss of Habitat"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/TLDmap.html')
    return render_template('TLDmap.html')


@app.route('/THDmap')
def THDmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Rusa alfredi (Visayan Spotted Deer)"]
    data = data[data['threats'] == "Hunting"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/THDmap.html')
    return render_template('THDmap.html')


@app.route('/TLRmap')
def TLRmap():
    data = pd.read_csv('data.csv')
    data = data[data['species_name'] == "Raflesia speciosa (Panay Rafflesia)"]
    data = data[data['threats'] == "Loss of Habitat"]

    Hmap = folium.Map(location=[11.102947, 122.516279],
                      zoom_start=9, tiles='Stamen Terrain')

    # Ensure you're handing it floats

    data['coordinates_lat'] = data['coordinates_lat'].astype(float)
    data['coordinates_lng'] = data['coordinates_lng'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs

    heat_df = data
    heat_df = heat_df[['coordinates_lat', 'coordinates_lng']]
    heat_df = heat_df.dropna(axis=0, subset=['coordinates_lat', 'coordinates_lng'])

    heat_data = [[row['coordinates_lat'], row['coordinates_lng']] for index, row in heat_df.iterrows()]
    gradient = {.44: 'red', .66: 'lime', 1: 'blue'}
    # Plot it on the map
    HeatMap(heat_data, gradient=gradient).add_to(Hmap)
    Hmap.save('templates/TLRmap.html')
    return render_template('TLRmap.html')


@app.route('/Visualisation')
def Vis():
    return render_template('vis.html')


@app.route('/Population Forecasting')
def popfor():
    return render_template('popfor.html')


@app.route('/Seasonality Forecasting')
def seafor():
    return render_template('seafor.html')


@app.route('/Warty Forecast')
def WPF():
    data = pd.read_csv('popdata.csv', parse_dates=True)
    df = data[data['pop_name'] == "Sus cebifrons (Visayan Warty Pig)"]
    df = df[['pop_date', 'population_no']]
    df['pop_date'] = pd.to_datetime(df['pop_date'])
    df = df.groupby('pop_date')['population_no'].sum().reset_index()
    df = df.set_index('pop_date')
    df.index

    y = df['population_no'].resample('M').mean()
    from pylab import rcParams
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')
    fig = decomposition.plot()
    plt.show()

    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    print('Examples of parameter combinations for Seasonal ARIMA...')
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=True,
                                                enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(16, 8))
    plt.show()

    pred = results.get_prediction(start=pd.to_datetime('2020-12-31'), dynamic=False)
    pred_ci = pred.conf_int()
    ax = y['2016':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.show()

    pred_uc = results.get_forecast(steps=24)
    pred_ci = pred_uc.conf_int()
    ax = y.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.savefig('static/images/WPFplot.png')
    plt.show()
    return render_template('popfor.html')


@app.route('/Hornbill Forecast')
def HPF():
    data = pd.read_csv('popdata.csv', parse_dates=True)
    df = data[data['pop_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]
    df = df[['pop_date', 'population_no']]
    df['pop_date'] = pd.to_datetime(df['pop_date'])
    df = df.groupby('pop_date')['population_no'].sum().reset_index()
    df = df.set_index('pop_date')
    df.index

    y = df['population_no'].resample('M').mean()
    from pylab import rcParams
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')
    fig = decomposition.plot()
    plt.show()

    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    print('Examples of parameter combinations for Seasonal ARIMA...')
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=True,
                                                enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(16, 8))
    plt.show()

    pred = results.get_prediction(start=pd.to_datetime('2020-12-31'), dynamic=False)
    pred_ci = pred.conf_int()
    ax = y['2016':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.show()

    pred_uc = results.get_forecast(steps=24)
    pred_ci = pred_uc.conf_int()
    ax = y.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.savefig('static/images/HPFplot.png')
    plt.show()
    return render_template('popfor.html')


@app.route('/Deer Forecast')
def DPF():
    data = pd.read_csv('popdata.csv', parse_dates=True)
    df = data[data['pop_name'] == "Rusa alfredi (Visayan Spotted Deer)"]
    df = df[['pop_date', 'population_no']]
    df['pop_date'] = pd.to_datetime(df['pop_date'])
    df = df.groupby('pop_date')['population_no'].sum().reset_index()
    df = df.set_index('pop_date')
    df.index

    y = df['population_no'].resample('M').mean()
    from pylab import rcParams
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')
    fig = decomposition.plot()
    plt.show()

    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    print('Examples of parameter combinations for Seasonal ARIMA...')
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=True,
                                                enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(16, 8))
    plt.show()

    pred = results.get_prediction(start=pd.to_datetime('2020-12-31'), dynamic=False)
    pred_ci = pred.conf_int()
    ax = y['2016':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.show()

    pred_uc = results.get_forecast(steps=24)
    pred_ci = pred_uc.conf_int()
    ax = y.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Population')
    plt.legend()
    plt.savefig('static/images/DPFplot.png')
    plt.show()
    return render_template('popfor.html')


@app.route('/Seasonality Deer Forecast')
def SDF():
    data = pd.read_csv("data.csv")
    data = data[data['species_name'] == "Rusa alfredi (Visayan Spotted Deer)"]
    data = data[['date_report', 'no_observation']]
    data.head()

    data.index = pd.to_datetime(data['date_report'])
    data.drop(columns='date_report', inplace=True)
    data.head()
    data = data.resample('M').sum()

    data.isna().sum()
    data.plot()

    from statsmodels.tsa.seasonal import seasonal_decompose
    decompose_data = seasonal_decompose(data, model="additive")
    decompose_data.plot()
    seasonality = decompose_data.seasonal
    seasonality.plot(color='green')

    from statsmodels.tsa.stattools import adfuller
    dftest = adfuller(data.no_observation, autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    rolling_mean = data.rolling(window=12).mean()
    data['rolling_mean_diff'] = rolling_mean - rolling_mean.shift()
    ax1 = plt.subplot()
    data['rolling_mean_diff'].plot(title='after rolling mean & differencing')
    ax2 = plt.subplot()
    data.plot(title='original')

    dftest = adfuller(data['rolling_mean_diff'].dropna(), autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    Sarimax_model = auto_arima(data.no_observation,
                               start_p=0,
                               start_q=0,
                               max_p=3,
                               max_q=3,
                               m=12,
                               test='adf',
                               seasonal=True,
                               d=1,
                               D=1,
                               trace=True,
                               error_action='ignore',
                               suppress_warnings=True,
                               stepwise=True)

    Sarimax_model.summary()

    model = ARIMA(data['no_observation'], order=(0, 1, 1))
    history = model.fit()
    history.summary()

    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    model = ARIMA(data['rolling_mean_diff'].dropna(), order=(0, 1, 1))
    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['rolling_mean_diff', 'forecast']].plot(figsize=(12, 8))

    import statsmodels.api as sm
    model = sm.tsa.statespace.SARIMAX(data['no_observation'], order=(0, 1, 1), seasonal_order=(0, 1, 2, 12))
    results = model.fit()
    data['forecast'] = results.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    s_residuals = data['no_observation'] - data['forecast']
    print('Mean Absolute Percent Error:', round(np.mean(abs(s_residuals / data.no_observation)), 2))
    print('Root Mean Squared Error:', np.sqrt(np.mean(s_residuals ** 2)))
    from pandas.tseries.offsets import DateOffset
    pred_date = [data.index[-1] + DateOffset(months=x) for x in range(0, 24)]
    pred_date = pd.DataFrame(index=pred_date[1:], columns=data.columns)
    pred_date

    data = pd.concat([data, pred_date])
    data['forecast'] = results.predict(start=71, end=96, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))
    plt.savefig('static/images/SDFplot.png')
    data

    data.tail(24)
    return render_template('seafor.html')


@app.route('/Seasonality Hornbill Forecast')
def SHF():
    data = pd.read_csv("data.csv")
    data = data[data['species_name'] == "Aceros waldeni (Visayan Writhed Hornbill)"]
    data = data[['date_report', 'no_observation']]
    data.head()

    data.index = pd.to_datetime(data['date_report'])
    data.drop(columns='date_report', inplace=True)
    data.head()
    data = data.resample('M').sum()

    data.isna().sum()
    data.plot()

    from statsmodels.tsa.seasonal import seasonal_decompose
    decompose_data = seasonal_decompose(data, model="additive")
    decompose_data.plot()
    seasonality = decompose_data.seasonal
    seasonality.plot(color='green')

    from statsmodels.tsa.stattools import adfuller
    dftest = adfuller(data.no_observation, autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    rolling_mean = data.rolling(window=12).mean()
    data['rolling_mean_diff'] = rolling_mean - rolling_mean.shift()
    ax1 = plt.subplot()
    data['rolling_mean_diff'].plot(title='after rolling mean & differencing')
    ax2 = plt.subplot()
    data.plot(title='original')

    dftest = adfuller(data['rolling_mean_diff'].dropna(), autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    Sarimax_model = auto_arima(data.no_observation,
                               start_p=0,
                               start_q=0,
                               max_p=3,
                               max_q=3,
                               m=12,
                               test='adf',
                               seasonal=True,
                               d=1,
                               D=1,
                               trace=True,
                               error_action='ignore',
                               suppress_warnings=True,
                               stepwise=True)

    Sarimax_model.summary()

    model = ARIMA(data['no_observation'], order=(0, 1, 1))
    history = model.fit()
    history.summary()

    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    model = ARIMA(data['rolling_mean_diff'].dropna(), order=(0, 1, 1))
    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['rolling_mean_diff', 'forecast']].plot(figsize=(12, 8))

    import statsmodels.api as sm
    model = sm.tsa.statespace.SARIMAX(data['no_observation'], order=(0, 1, 1), seasonal_order=(0, 1, 2, 12))
    results = model.fit()
    data['forecast'] = results.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    s_residuals = data['no_observation'] - data['forecast']
    print('Mean Absolute Percent Error:', round(np.mean(abs(s_residuals / data.no_observation)), 2))
    print('Root Mean Squared Error:', np.sqrt(np.mean(s_residuals ** 2)))
    from pandas.tseries.offsets import DateOffset
    pred_date = [data.index[-1] + DateOffset(months=x) for x in range(0, 24)]
    pred_date = pd.DataFrame(index=pred_date[1:], columns=data.columns)
    pred_date

    data = pd.concat([data, pred_date])
    data['forecast'] = results.predict(start=71, end=96, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))
    plt.savefig('static/images/SHFplot.png')
    data

    data.tail(24)
    return render_template('seafor.html')


@app.route('/Seasonalit Warty Forecast')
def SWF():
    data = pd.read_csv("data.csv")
    data = data[data['species_name'] == "Sus cebifrons (Visayan Warty Pig)"]
    data = data[['date_report', 'no_observation']]
    data.head()

    data.index = pd.to_datetime(data['date_report'])
    data.drop(columns='date_report', inplace=True)
    data.head()
    data = data.resample('M').sum()

    data.isna().sum()
    data.plot()

    from statsmodels.tsa.seasonal import seasonal_decompose
    decompose_data = seasonal_decompose(data, model="additive")
    decompose_data.plot()
    seasonality = decompose_data.seasonal
    seasonality.plot(color='green')

    from statsmodels.tsa.stattools import adfuller
    dftest = adfuller(data.no_observation, autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    rolling_mean = data.rolling(window=12).mean()
    data['rolling_mean_diff'] = rolling_mean - rolling_mean.shift()
    ax1 = plt.subplot()
    data['rolling_mean_diff'].plot(title='after rolling mean & differencing')
    ax2 = plt.subplot()
    data.plot(title='original')

    dftest = adfuller(data['rolling_mean_diff'].dropna(), autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

    Sarimax_model = auto_arima(data.no_observation,
                               start_p=0,
                               start_q=0,
                               max_p=3,
                               max_q=3,
                               m=12,
                               test='adf',
                               seasonal=True,
                               d=1,
                               D=1,
                               trace=True,
                               error_action='ignore',
                               suppress_warnings=True,
                               stepwise=True)

    Sarimax_model.summary()

    model = ARIMA(data['no_observation'], order=(0, 1, 1))
    history = model.fit()
    history.summary()

    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    model = ARIMA(data['rolling_mean_diff'].dropna(), order=(0, 1, 1))
    model_fit = model.fit()
    data['forecast'] = model_fit.predict(start=60, end=72, dynamic=True)
    data[['rolling_mean_diff', 'forecast']].plot(figsize=(12, 8))

    import statsmodels.api as sm
    model = sm.tsa.statespace.SARIMAX(data['no_observation'], order=(0, 1, 1), seasonal_order=(0, 1, 2, 12))
    results = model.fit()
    data['forecast'] = results.predict(start=60, end=72, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))

    s_residuals = data['no_observation'] - data['forecast']
    print('Mean Absolute Percent Error:', round(np.mean(abs(s_residuals / data.no_observation)), 2))
    print('Root Mean Squared Error:', np.sqrt(np.mean(s_residuals ** 2)))
    from pandas.tseries.offsets import DateOffset
    pred_date = [data.index[-1] + DateOffset(months=x) for x in range(0, 24)]
    pred_date = pd.DataFrame(index=pred_date[1:], columns=data.columns)
    pred_date

    data = pd.concat([data, pred_date])
    data['forecast'] = results.predict(start=71, end=96, dynamic=True)
    data[['no_observation', 'forecast']].plot(figsize=(12, 8))
    plt.savefig('static/images/SWFplot.png')
    data

    data.tail(24)
    return render_template('seafor.html')


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


# run flask app
if __name__ == "__main__":
    app.run(debug=True)

