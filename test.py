import requests
import time
import csv
from random import randrange

URL = "http://localhost:8000/name/"
FILENAME = "tests_{}.csv".format(time.time())
HEADERS = ['request_id','db_id','time','source']
file = open(FILENAME,'w')
csv_file = csv.DictWriter(file,fieldnames=HEADERS)
csv_file.writeheader()

r = requests.get("http://localhost:8000/deleteKeys")
print(r.text)


for i in range(100000):
    id = randrange(1000,21000)
    start_time = time.time_ns()
    r = requests.get(URL + str(id))
    ms = time.time_ns() - start_time
    row = {
        'request_id': i,
        'db_id': id,
        'time': ms,
        'source': r.json()['source']
    }
    print(row)
    csv_file.writerow(
        row
    )
    
    
file.close()
    