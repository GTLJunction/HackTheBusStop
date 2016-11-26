from flask import Flask, render_template, redirect, request, url_for, abort, jsonify

app = Flask(__name__)

qrcodes = {'eat': lambda stopname: update_hunger(stopname, 5), 'drink': lambda stopname: update_thirst(stopname, 5) ,
    'happy': lambda stopname : update_mood(stopname, 'Happy'), 'sad': lambda stopname: update_mood(stopname, 'Sad') }

busstops = {}
#     {'republique':
#         {'lat': 123,
#         'lon': 12,
#         'pet': {
#             'hunger':0,
#             'thirst':0,
#             'distancewalked':0
#         }}
#     },{'gare':
#         {}
# }]

@app.route('/')
def index():
    return "Homepage"

@app.route('/busstop/<string:stopname>', methods=['PUT'])
def put_stop(stopname):
    busstops[stopname] = {}
    return jsonify(busstops)

@app.route('/addStop', methods=['POST'])
def add_stop():
    if not request.form:
        abort(400)
    busstops[request.form['stopname']] = {'lat': request.form['lat'], 'lon': request.form['lon'], 'pet': {'mood': None, 'distance': 0, 'hunger': 0, 'thirst': 0}}
    return jsonify(busstops)


def add_stop(stopname, lat, lon):
    busstops['stopname'] = {'lat': request.form['lat'], 'lon': request.form['lon'], 'pet': {'mood': None, 'distance': 0, 'hunger': 0, 'thirst': 0}}
    return jsonify(busstops)

@app.route('/addStop', methods=['GET'])
def add_stop_page():
    return app.send_static_file('addStopForm.html')

@app.route('/busstop/<string:stopname>', methods=['POST'])
def result(stopname):
    return render_template("busStopPage.html")#, stopname = busstops[stopname], lat = busstops[stopname][lat], lon = busstops[stopname][lon])

# @app.route('/busstop/<string:stopname>', methods=['GET'])
# def bus_stop_page():
#     retur

## post
@app.route('/busstop/<string:stopname>/lat/<float:latitude>', methods=['POST'])
def update_lat(stopname, latitude):
    if stopname in busstops:
        busstops[stopname]['lat'] = latitude
        return jsonify(busstops)
    else:
        return "Error"

@app.route('/busstop/<string:stopname>/lon/<float:longitude>', methods=['POST'])
def update_lon(stopname, longitude):
    if stopname in busstops:
        busstops[stopname]['lon'] = longitude
        return jsonify(busstops)
    else:
        return "Error"

@app.route('/busstop/<string:stopname>/pet/hunger/<float:hungermod>', methods=['POST'])
def update_hunger(stopname, hungermod):
    if stopname in busstops:
        busstops[stopname]['pet']['hunger'] += hungermod
        return jsonify(busstops)
    else:
        return "Error"

@app.route('/busstop/<string:stopname>/pet/thirst/<float:thirstmod>', methods=['POST'])
def update_thirst(stopname, thirstmod):
    if stopname in busstops:
        busstops[stopname]['pet']['thirst'] += thirstmod
        return jsonify(busstops)
    else:
        return "Error"

@app.route('/busstop/<string:stopname>/pet/distancewalked/<float:distancemod>', methods=['POST'])
def update_distance(stopname, distancemod):
    if stopname in busstops:
        busstops[stopname]['pet']['distancewalked'] += distancemod
        return jsonify(busstops)
    else:
        return "Error"

@app.route('/busstop/<string:stopname>/pet/mood/<string:mood>', methods=['POST'])
def update_mood(stopname, mood):
    if stopname in busstops:
        busstops[stopname]['pet']['mood'] = mood
        return jsonify(busstops)
    else:
        return "Error"


@app.route('/scancode', methods=['POST'])
def post_data():
    print request
    return data

@app.route('/busstop/<string:stopname>', methods=['GET'])
def get_stop(stopname):
    #if stopname in busstops:
    return render_template('busStopPage.html', stopname=stopname, stopdict = busstops[stopname])
    #else:
        #return str(stopname is not None)

# @app.route('/busstop/<string:stopname>', methods=['DELETE'])
# def delete_stop(stopname):
#     if stopname in busstops:
#         del busstops[stopname]
#     return jsonify(busstops)


if __name__ == '__main__':
    app.run(debug=True, port=80)
    addStop('Gare', 49.110860, 6.176966)
