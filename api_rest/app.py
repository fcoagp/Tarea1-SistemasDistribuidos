from flask import Flask
import redis
import os
import json
import grpc
import service_pb2
import service_pb2_grpc


app = Flask(__name__)

CACHE_TYPE=os.environ['CACHE_TYPE']
GRPC_SERVER=os.environ['GRPC_SERVER']


REDIS_CONNECTIONS = {
    'redis1': redis.Redis(host='redis1', port=6379, db=0),
    'redis2': redis.Redis(host='redis2', port=6379, db=0),
    'redis3': redis.Redis(host='redis3', port=6379, db=0)
}

def getRedisConnection(id):
    if CACHE_TYPE == 'PARTITION':
        redis_server = ['redis1','redis2','redis3'][id % 3]
        return redis_server,REDIS_CONNECTIONS[redis_server]
    else:
        return 'redis1',REDIS_CONNECTIONS['redis1']



def getFromGRPC(id):
    with grpc.insecure_channel(GRPC_SERVER) as channel:
        stub = service_pb2_grpc.NameStub(channel)
        response = stub.getName(service_pb2.NameRequest(id=str(id)))
        print(response)
        return 'db',{
            'id': response.id,
            'nconst': response.nconst,
            'primaryName': response.primaryName,
            'birthYear': response.birthYear,
            'deathYear': response.deathYear,
            'primaryProfession': response.primaryProfession,
            'knownForTitles': response.knownForTitles
        }

def saveToRedis(id,data):
    data = json.dumps(data)
    _,redis_connection = getRedisConnection(id)
    redis_connection.set(id,data)
    if CACHE_TYPE == 'DUPLICATE':
        REDIS_CONNECTIONS['redis2'].set(id,data)
        REDIS_CONNECTIONS['redis3'].set(id,data)
        

def getFromRedis(id):
    redis_server,redis_connection = getRedisConnection(id)
    data = redis_connection.get(id)
    return redis_server,json.loads(data) if data is not None else None


def getValue(id):
    source,data = getFromRedis(id)
    if data is None:
        source,data = getFromGRPC(id)
        saveToRedis(id,data)
    return source,data

@app.route("/deleteKeys")
def deleteKeys():
    for client in REDIS_CONNECTIONS.values():
        for key in client.keys('*'):
            client.delete(key)
    return 'OK'


@app.route("/name/<id>")
def hello_world(id):
    source,data = getValue(int(id))
    data['source'] = source
    return data
if __name__ == "__main__":
    app.run(debug=True)