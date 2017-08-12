from flask import Flask, render_template, request
from datetime import datetime,timedelta
import sqlite3
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello, world'


@app.route('/display_temperature_humidity')
def display_temperature_humidity():
    # get lookback (in hours)
    lookback = request.args.get('lookback',24)
    lookback = int(lookback)

    lookback_to = datetime.now() - timedelta(hours=lookback)
    query = """
        select *
        from temperature_humidity
        where created_at >= '%s'
    """ % str(lookback_to)

    connection = sqlite3.connect('temperature.db')
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    
    timestamps = [datetime.strptime(datum[2],'%Y-%m-%d %H:%M:%S.%f') for datum in data]
    temperatures = [float(datum[0]) for datum in data]
    humidities = [float(datum[1]) for datum in data]

    #temperature_figure = figure(width=950,height=550,x_axis_type='datetime')
    temperature_figure = figure(width=950,height=550)
    #temperature_figure.line(timestamps,temperatures,line_dash=[6,3])
    temperature_figure.line(range(len(temperatures)),temperatures,line_dash=[6,3])
    temperature_figure.title.text = 'Temperature'
    temperature_figure.xaxis.axis_label = 'Time'
    temperature_figure.yaxis.axis_label = 'Temperature'
    
    #humidity_figure = figure(width=950,height=550,x_axis_type='datetime')
    humidity_figure = figure(width=950,height=550)
    #humidity_figure.line(timestamps,humidities,line_dash=[6,3])
    humidity_figure.line(range(len(humidities)),humidities,line_dash=[6,3])
    humidity_figure.title.text = 'Humidity'
    humidity_figure.xaxis.axis_label = 'Time'
    humidity_figure.yaxis.axis_label = 'Humidity'

    p = column([temperature_figure,humidity_figure])
    script, div = components(p)
    return render_template('show_data.html',div=div,script=script)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)