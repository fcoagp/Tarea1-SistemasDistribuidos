import psycopg2

DB_NAME='db'
DB_USER='postgres'
DB_PASSWORD='secret'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)


