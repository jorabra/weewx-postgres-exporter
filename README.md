Weewx PostgreSQL exporter
=========================

A simple script for exporting data from Weewx's SQLite database to a PostgreSQL database.


Installation and usage
----------------------

1. Simply create your database with the script:

        psql -d <your_database> -f weewx_pg.sql
    
2. Configure the PostgreSQL parameters at the beginning of the `pg_export.py` script.

3. Add the script to crontab:

        */5 * * * * python /home/pi/scripts/pg_export.py >> /your/log/location/pg-export.log


License
-------

MIT
