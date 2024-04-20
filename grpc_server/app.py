import psycopg2
import grpc
import service_pb2
import service_pb2_grpc
from concurrent import futures
import logging

DB_HOST='db'
DB_NAME='db'
DB_USER='postgres'
DB_PASSWORD='secret'

db_conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,host=DB_HOST)


def getFromDB(id):
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM public.dataset WHERE id = {};".format(id))
    data = cur.fetchone()
    cur.close()
    print(data)
    return {
            'id': data[0],
            'nconst': data[1],
            'primaryName': data[2],
            'birthYear': data[3],
            'deathYear': data[4],
            'primaryProfession': data[5],
            'knownForTitles': data[6],
        }



class Name(service_pb2_grpc.NameServicer):
    def getName(self, request, context):
        
        data = getFromDB(request.id)
        print(data)
        return service_pb2.NameReply(
           **data
        )


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_NameServicer_to_server(Name(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
    db_conn.close()