import pymongo
import time


mongo = pymongo.MongoClient()

def main():
    while True:
        mongo.busstopsdb.stops.update(
            {
                'pet.hunger' : {'$gt' : 1}
            }, 
            {
                '$inc' : {'pet.hunger' : -1.0/6.0}
            })
        mongo.busstopsdb.stops.update(
            {
                'pet.thirst' : {'$gt' : 2}
            }, 
            {
                '$inc' : {'pet.thirst' : -2.0/6.0}
            })
        mongo.busstopsdb.stops.update(
            {
                'pet.interaction' : {'$gt' : 3}
            }, 
            {
                '$inc' : {'pet.interaction' : -3/6.0}
            })
        time.sleep(10)

if __name__ == '__main__':
    main()
