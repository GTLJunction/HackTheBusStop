import flask
import pymongo
import gpxpy.geo
from bson import Binary, Code
from bson.json_util import dumps
app = flask.Flask(__name__)
mongo = pymongo.MongoClient()


# ------------------------------------------------
# INDEX
# ------------------------------------------------
@app.route('/')
def index():
    stops = mongo.busstopsdb.stops.find({})
    return dumps(stops)



# ------------------------------------------------
# NEW STOP
# ------------------------------------------------
@app.route('/newstop', methods = ['GET'])
def new_stop_page():
    return flask.render_template('new_stop.html')
    
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
    return flask.redirect('/busstop/%s' % flask.request.form['stopname'])

def create_stop(stopdict):
    mongo.busstopsdb.stops.insert(stopdict)



# ------------------------------------------------
# BUS STOP
# ------------------------------------------------
@app.route('/busstop/<string:stopname>')
def busstop_page(stopname):
    busstop = mongo.busstopsdb.stops.find_one({'stopname' : stopname})
    happiness = busstop['pet']['interaction'] * .5 + busstop['pet']['thirst'] * .25 + busstop['pet']['hunger'] * .25
    return flask.render_template('bus_stop.html', busstop=busstop, happiness=happiness)



# ------------------------------------------------
# QR SCAN
# ------------------------------------------------
@app.route('/busstop/<string:stopname>/scancode', methods = ['GET'])
def scan_code_page(stopname):
    return flask.render_template('scan_code.html', stopname = stopname)

QR_DATA_FUNCTIONS = ['EAT','DRINK','WALK','PLAY']
# WALK|45|60,EAT|12,DRINK|3
# INTERACT|4

    
@app.route('/busstop/<string:stopname>/scancode', methods = ['POST'])
def scan_code(stopname):
    if not flask.request.form:
        flask.abort(400)
        return
    print flask.request.form['data']
    qrdata = flask.request.form['data']
    ops = [func.split('|') for func in qrdata.split(',')]
    output = []
    for op in ops:
        print op
        if op[0] in QR_DATA_FUNCTIONS:
            if op[0] == 'EAT':
                output.append(pet_eat(stopname, op[1:]))
            elif op[0] == 'DRINK':
                output.append(pet_drink(stopname, op[1:]))
            elif op[0] == 'WALK':
                output.append(pet_walk(stopname, op[1:]))
            elif op[0] == 'PLAY':
                output.append(pet_play(stopname, op[1:]))
            
    print output
    return flask.redirect('/busstop/%s' % stopname)

def pet_eat(stopname, quantity):
    quantity = int(quantity[0])
    mongo.busstopsdb.stops.update_many({'stopname' : stopname}, {'$inc' : {'pet.hunger' : quantity}})
    mongo.busstopsdb.stops.update_many({'pet.hunger' : {'$gt' : 100}}, {'$set' : {'pet.hunger' : 100}})
    return ('EAT', quantity)

def pet_drink(stopname, quantity):
    quantity = int(quantity[0])
    mongo.busstopsdb.stops.update_many({'stopname' : stopname}, {'$inc' : {'pet.thirst' : quantity}})
    mongo.busstopsdb.stops.update_many({'pet.thirst' : {'$gt' : 100}}, {'$set' : {'pet.thirst' : 100}})
    return ('DRINK', quantity)

def pet_walk(stopname, coordinates):
    lat= float(coordinates[0])
    lon = float(coordinates[1])
    curr = mongo.busstopsdb.stops.find_one({'stopname' : stopname}, {'lat' : 1, 'lon' : 1})
    distance = gpxpy.geo.haversine_distance(float(curr['lat']), float(curr['lon']), lat, lon)/1000.0
    mongo.busstopsdb.stops.update_many({'stopname' : stopname}, {'$inc' : {'pet.distance' : distance}})
    return ('WALK', distance)

def pet_play(stopname, quantity):
    quantity = int(quantity[0])
    mongo.busstopsdb.stops.update_many({'stopname' : stopname}, {'$inc' : {'pet.interaction' : quantity}})
    mongo.busstopsdb.stops.update_many({'pet.interaction' : {'$gt' : 100}}, {'$set' : {'pet.interaction' : 100}})
    return ('PLAY', quantity)
    


def main(debug=True, host='127.0.0.1', port=80):
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main()