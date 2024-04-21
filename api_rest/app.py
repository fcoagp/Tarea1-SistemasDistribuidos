from flask import Flask
import os
import json
import grpc
import service_pb2
import service_pb2_grpc
from custom_redis import CustomRedis
import random


app = Flask(__name__)

CACHE_TYPE=os.environ['CACHE_TYPE']
GRPC_SERVER=os.environ['GRPC_SERVER']

REDIS_HOSTS=['redis1','redis2','redis3']

redis = CustomRedis(REDIS_HOSTS,CACHE_TYPE)





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
    redis.set(id,data)
    
        

def getFromRedis(id):
    redis_server,data = redis.get(id)
    if data is None:
        return None,None
    return redis_server,json.loads(data)


def getValue(id):
    source,data = getFromRedis(id)
    if data is None:
        source,data = getFromGRPC(id)
        saveToRedis(id,data)
    return source,data

@app.route("/deleteKeys")
def deleteKeys():
    redis.deleteAllKeys()
    return 'OK'


@app.route("/name/<id>")
def hello_world(id):
    source,data = getValue(int(id))
    data['source'] = source
    return data

if __name__ == "__main__":
    app.run(debug=True)