import flask
from flask.pymongo import PyMongo
import gpxpy.geo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'busstopdb'
mongo = PyMongo(app)


# ------------------------------------------------
# INDEX
# ------------------------------------------------
@app.route('/')
def index():
    return "Homepage under construction"
    # return flask.render_template('index.html')



# ------------------------------------------------
# NEW STOP
# ------------------------------------------------
@app.route('/newstop', methods = ['GET'])
def new_stop_page():
    return flask.render_template('newstop.html')
    
@app.route('/newstop', methods = ['POST'])
def new_stop():
    if not flask.request.form:
        flask.abort(400)
        return
    stopdict = {
        'stopname' : flask.request.form['stopname'],
        'lat' : flask.request.form['lat'],
        'lon' : flask.request.form['lon'],
        'pet' : {
            'hunger' : 50,
            'thirst' : 50,
            'distance' : 0,
            'interaction' : 50
        }
    }
    create_stop(stopdict)
    return flask.redirect('/%s' % flask.request.form['stopname'])

def create_stop(stopdict):
    mongo.db.stops.insert(stopdict)



# ------------------------------------------------
# BUS STOP
# ------------------------------------------------
@app.route('/<string:stopname>')
def busstop_page(stopname):
    busstop = mongo.db.stops.find_one({'stopname' : stopname})
    return flask.render_template('busstop.html', busstop=busstop)



# ------------------------------------------------
# QR SCAN
# ------------------------------------------------
@app.route('<string:stopname>/scancode', methods = ['GET'])
def scan_code_page(stopname):
    return flask.render_template('scancode.html', stopname = stopname)

QR_DATA_FUNCTIONS = {
        'EAT' : pet_eat, 
        'DRINK' : pet_drink, 
        'WALK' : pet_walk, 
        'PLAY' : pet_play
    }
# WALK|45|60,EAT|12,DRINK|3
# INTERACT|4

    
@app.route('<string:stopname>/scancode', methods = ['POST'])
def scan_code(stopname):
    if not flask.request.form:
        flask.abort(400)
        return
    
    qrdata = flask.request.form.keys[0]
    ops = [func.split('|') for func in qrdata.split(',')]
    output = []
    for op in ops:
        if op[0] in QR_DATA_FUNCTIONS:
            output.append(QR_DATA_FUNCTIONS[op[0]](stopname, op[1:]))
    print output
    return flask.redirect('/%s' % stopname)

# TODO: max at 100
def pet_eat(stopname, quantity):
    mongo.db.stops.update({'stopname' : stopname}, {'$inc' : {'pet.hunger' : quantity}})
    return ('EAT', quantity)

def pet_drink(stopname, quantity):
    mongo.db.stops.update({'stopname' : stopname}, {'$inc' : {'pet.thirst' : quantity}})
    return ('DRINK', quantity)

def pet_walk(stopname, coordinates):
    curr = mongo.db.stops.find_one({'stopname' : stopname}, {'lat' : 1, 'lon' : 1})
    distance = gpxpy.geo.haversine_distance(curr['lat'], curr['lon'], coordinates[0], coordinates[1])/1000.0
    mongo.db.stops.update({'stopname' : stopname}, {'$set' : {'pet.distance' : distance}})
    return ('WALK', distance)

def pet_play(stopname, quantity):
    mongo.db.stops.update({'stopname' : stopname}, {'$inc' : {'pet.interaction' : quantity}})
    return ('PLAY', quantity)
    


def main(debug=False, host=127.0.0.1, port=80):
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main()