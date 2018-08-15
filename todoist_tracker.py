#  from pytodoist import todoist
#
#  user1 = todoist.login('felarof.nayak@gmail.com', 'fel@rof666')
#
import numpy as np
np.random.seed(1)

from bokeh.layouts import gridplot
from bokeh.models import AjaxDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    plot_script, plot_div = make_ajax_plot()
    kwargs = {'plot_script': plot_script, 'plot_div': plot_div}
    kwargs['title'] = 'Todoist'
    if request.method == 'GET':
        return render_template('index.html', **kwargs)
    abort(404)
    abort(Respone('Error'))

def _create_data():
   karma = np.random.uniform(0.05, 0.95, size=1)
   return karma[0]

def _moving_avg(karma_list, days=7):
    if len(karma_list) < 7: return 0.
    return np.convolve(np.array(karma_list[-7:]), np.ones(7, dtype=float), mode='valid')[0] / days

t=0
karma_list=[]
karma_inc_list=[]

@app.route('/data/', methods=['POST'])
def update():
    global t, karma_list, karma_inc_list
    
    t += 1
    karma = _create_data()
    new_data = dict(
            time=[t],
            karma=[karma],
            )

    karma_list.append(karma)
    daily_inc = karma - karma_list[-2:][0]

    new_data['daily_inc'] = [daily_inc]
    
    karma_inc_list.append(daily_inc)
    ma_week = _moving_avg(karma_inc_list, 7)
    new_data['ma_week'] = [ma_week]

    if len(karma_list) > 10:
        karma_list = karma_list[-10:]
        karma_inc_list = karma_inc_list[-10:]

    return jsonify(new_data)

def make_ajax_plot():

    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=100, mode='append', max_size=300)
    source.data = dict(
                    time=[], karma=[],
                    daily_inc=[], ma_week=[]
                  )


    p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_type=None, y_axis_location="right")
    p.x_range.follow = "end"
    p.x_range.follow_interval = 100
    p.x_range.range_padding_units = 'absolute'
    p.x_range.range_padding = 10
    p.line(x='time', y='karma', alpha=0.2, line_width=3, color='orange', source=source)
    p.line(x='time', y='karma', alpha=0.2, line_width=3, color='orange', source=source)

    p2 = figure(plot_height=250, x_range=p.x_range, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
    p2.segment(x0='time', y0=0, x1='time', y1='daily_inc', line_width=6, color='black', alpha=0.5, source=source)
    p2.line(x='time', y='ma_week', color='red', source=source)

    final_plot = gridplot([[p], [p2]], toolbar_location="left", plot_width=1000)

    script, div = components(final_plot)
    return script, div

if __name__ == '__main__':
    app.run(debug=True)
