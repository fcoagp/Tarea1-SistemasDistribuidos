from flask import Flask
import redis
import os
import json


app = Flask(__name__)

CACHE_TYPE=os.environ['CACHE_TYPE']
print(CACHE_TYPE)


REDIS_CONNECTIONS = {
    'redis1': redis.Redis(host='redis1', port=6379, db=0),
    'redis2': redis.Redis(host='redis2', port=6379, db=0),
    'redis3': redis.Redis(host='redis3', port=6379, db=0)
}

def getRedisConnection(id): # abstrae la conexion a redis
    if CACHE_TYPE == 'PARTITION':
        redis_server = ['redis1','redis2','redis3'][id % 3]
        return REDIS_CONNECTIONS[redis_server]
    else:
        return REDIS_CONNECTIONS['redis1']


#esta debe ser modificada para recibir un json o diccionario la wea que sea mandada por el grpc
def getFromGRPC(id):
    return {
        'id': id,
        'nconst': 76467246,
        'primaryName': 'John Belushi',
        'birthYear': 2424,
        'deathYear': 2424,
        'primaryProfession': 'actor,miscellaneous,producer',
        'knownForTitles': 'tt0072308,tt0050419,tt0053137,tt0027125'
    }



def saveToRedis(id,data):
    data = json.dumps(data)
    redis_connection = getRedisConnection(id)
    redis_connection.set(id,data)
    if CACHE_TYPE == 'DUPLICATE':
        REDIS_CONNECTIONS['redis2'].set(id,data)
        REDIS_CONNECTIONS['redis3'].set(id,data)
        

def getFromRedis(id):
    redis_connection = getRedisConnection(id)
    data = redis_connection.get(id)
    return json.loads(data) if data is not None else None


#esta es la principal
def getValue(id):
    data = getFromRedis(id)
    if data is None:
        data = getFromGRPC(id)
        saveToRedis(id,data)
    return data

@app.route("/name/<id>")
def hello_world(id):
    
    return getValue(int(id))

if __name__ == "__main__":
    app.run(debug=True)