#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE dataset (
        id serial4 NOT NULL,
        nconst varchar,
        primaryname varchar,
        birthyear varchar,
        deathyear varchar,
        primaryprofession varchar ,
        knownfortitles varchar,
        CONSTRAINT dataset_pkey PRIMARY KEY (id)
    );
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    COPY dataset( nconst, primaryname, birthyear,deathyear,primaryprofession,knownfortitles)
    FROM '/docker-entrypoint-initdb.d/names.csv'
    DELIMITER ','
    CSV HEADER;
EOSQL