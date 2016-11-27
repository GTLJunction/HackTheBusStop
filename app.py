import flask
import pymongo
import gpxpy.geo

app = flask.Flask(__name__)
mongo = pymongo.MongoClient()


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
    return flask.redirect('/%s' % flask.request.form['stopname'])

def create_stop(stopdict):
    mongo.busstopsdb.stops.insert(stopdict)



# ------------------------------------------------
# BUS STOP
# ------------------------------------------------
@app.route('/<string:stopname>')
def busstop_page(stopname):
    busstop = mongo.busstopsdb.stops.find_one({'stopname' : stopname})
    print busstop
    happiness = busstop['pet']['interaction'] * .5 + busstop['pet']['thirst'] * .25 + busstop['pet']['hunger'] * .25
    return flask.render_template('bus_stop.html', busstop=busstop, happiness=happiness)



# ------------------------------------------------
# QR SCAN
# ------------------------------------------------
@app.route('/<string:stopname>/scancode', methods = ['GET'])
def scan_code_page(stopname):
    return flask.render_template('scan_code.html', stopname = stopname)

QR_DATA_FUNCTIONS = {
        'EAT' : 'pet_eat', 
        'DRINK' : 'pet_drink', 
        'WALK' : 'pet_walk', 
        'PLAY' : 'pet_play'
    }
# WALK|45|60,EAT|12,DRINK|3
# INTERACT|4

    
@app.route('/<string:stopname>/scancode', methods = ['POST'])
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

def pet_eat(stopname, quantity):
    mongo.busstopsdb.stops.update({'stopname' : stopname}, {'$inc' : {'pet.hunger' : quantity}})
    mongo.busstopsdb.stops.update({'$gt' : 100}, {'$set' : {'pet.hunger' : 100}})
    return ('EAT', quantity)

def pet_drink(stopname, quantity):
    mongo.busstopsdb.stops.update({'stopname' : stopname}, {'$inc' : {'pet.thirst' : quantity}})
    mongo.busstopsdb.stops.update({'$gt' : 100}, {'$inc' : {'pet.thirst' : 100}})
    return ('DRINK', quantity)

def pet_walk(stopname, coordinates):
    curr = mongo.busstopsdb.stops.find_one({'stopname' : stopname}, {'lat' : 1, 'lon' : 1})
    distance = gpxpy.geo.haversine_distance(curr['lat'], curr['lon'], coordinates[0], coordinates[1])/1000.0
    mongo.busstopsdb.stops.update({'stopname' : stopname}, {'$set' : {'pet.distance' : distance}})
    return ('WALK', distance)

def pet_play(stopname, quantity):
    mongo.busstopsdb.stops.update({'stopname' : stopname}, {'$inc' : {'pet.interaction' : quantity}})
    mongo.busstopsdb.stops.update({'$gt' : 100}, {'$inc' : {'pet.interaction' : 100}})
    return ('PLAY', quantity)
    


def main(debug=False, host='127.0.0.1', port=80):
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    main()