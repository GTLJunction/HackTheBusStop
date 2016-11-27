import pymongo
import time


mongo = pymongo.MongoClient()

def main():
    while True:
        mongo.busstopsdb.stops.update_many(
            {}, 
            {
                '$inc' : {'pet.hunger' : -2.0/60.0}
            })
        mongo.busstopsdb.stops.update_many(
            {}, 
            {
                '$inc' : {'pet.thirst' : -4.0/60.0}
            })
        mongo.busstopsdb.stops.update_many(
            {}, 
            {
                '$inc' : {'pet.interaction' : -6.0/60.0}
            })
        mongo.busstopsdb.stops.update_many({'pet.thirst' : {'$lt' : 0}}, {'$set' : {'pet.thirst' : 0}})
        mongo.busstopsdb.stops.update_many({'pet.hunger' : {'$lt' : 0}}, {'$set' : {'pet.thirst' : 0}})
        mongo.busstopsdb.stops.update_many({'pet.interaction' : {'$lt' : 0}}, {'$set' : {'pet.thirst' : 0}})

        time.sleep(1)

if __name__ == '__main__':
    main()
