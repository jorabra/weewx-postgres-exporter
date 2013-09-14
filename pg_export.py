#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import time
import sqlite3 as sqlite
import psycopg2

"""
Script for exporting the weewx archive database to a remote postgresql database.
"""

SQLITE_ARCHIVE = "/var/lib/weewx/weewx.sdb"
PG_HOST = "some.host.tld"
PG_DB = "db_name"
PG_PORT = 5432
PG_USER = "username"
PG_PASS = "password"

## TESTING AREA
def main():
    local_dt = get_latest_archive_row_datetime_local()
    remote_dt = get_latest_archive_row_datetime_remote()

    if not local_dt:
        print "Local database empty. Not populated yet?"
        sys.exit(0)
    if not remote_dt:
        print "Remote database empty"
        remote_dt = datetime.fromtimestamp(0)

    if local_dt != remote_dt:
        print "Unequal timestamps between local and remote database."
        result = fetch_archive_rows_since_datetime(remote_dt)
        print "Number of new rows: %s" % len(result)
        #convert_values(result)
        write_to_pg_db(result)
    else:
        print "In sync. Nothing to do."


def _query_sqlite(query):
    con = None
    try:
        con = sqlite.connect(SQLITE_ARCHIVE)
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    except sqlite.Error, e:
        print "Error fetching SQLite data %s" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

def _connect_to_remote_pg():
    try:
        con_string = "host={host} dbname={db_name} user={user} password={password}".format(host=PG_HOST, db_name=PG_DB, user=PG_USER, password=PG_PASS)
        con = psycopg2.connect(con_string)
        return con

    except Exception, e:
        print "Error fetching PostgreSQL data: %s" % e.args[0]
        sys.exit(1)

def _query_pg(query):
    con = None
    try:
        con = _connect_to_remote_pg()
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    except Exception, e:
        print "Error fetching PostgreSQL data: %s" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

def _insert_pg(query):
    con = None
    try:
        con = _connect_to_remote_pg()
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    except Exception, e:
        print "Error inserting data to PostgreSQL database: %s" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

def fetch_archive_rows_since_datetime(date_time):
    """Fetch the rows from the 'archive' SQLite database since given datetime"""
    timestamp = int(time.mktime(date_time.timetuple()))
    query = "SELECT * FROM archive WHERE dateTime > {timestamp}".format(
                timestamp=timestamp)
    return _query_sqlite(query)

def get_latest_archive_row_datetime_local():
    """Return the datetime of the latest row written"""
    query = "SELECT dateTime FROM archive ORDER BY dateTime DESC LIMIT 1"
    result = _query_sqlite(query)
    if len(result):
        dt = datetime.fromtimestamp(result[0][0])
        print dt.strftime('%Y-%m-%d %H:%M:%S')
        return dt
    else:
        return None

def get_latest_archive_row_datetime_remote():
    """Return the datetime of the latest row written"""
    query = "SELECT datetime FROM archive ORDER BY datetime DESC LIMIT 1"
    result = _query_pg(query)
    if len(result):
        print result[0][0].strftime('%Y-%m-%d %H:%M:%S')
        return result[0][0]
    else:
        return None

def convert_values(rows):
    """Convert values to a more suited format"""
    print rows[0]

def write_to_pg_db(rows):
    """Write retrieved archive rows to remote PostgreSQL database"""
    con = _connect_to_remote_pg()
    cur = con.cursor()
    try:
        for row in rows:
            query = """INSERT INTO archive (
                            datetime,
                            usunits,
                            interval,
                            barometer,
                            pressure,
                            altimeter,
                            intemp,
                            outtemp,
                            inhumidity,
                            outhumidity,
                            windspeed,
                            winddir,
                            windgust,
                            windgustdir,
                            rainrate,
                            rain,
                            dewpoint,
                            windchill,
                            heatindex,
                            et,
                            radiation,
                            uv,
                            extratemp1,
                            extratemp2,
                            extratemp3,
                            soiltemp1,
                            soiltemp2,
                            soiltemp3,
                            soiltemp4,
                            leaftemp1,
                            leaftemp2,
                            extrahumid1,
                            extrahumid2,
                            soilmoist1,
                            soilmoist2,
                            soilmoist3,
                            soilmoist4,
                            leafwet1,
                            leafwet2,
                            rxcheckpercent,
                            txbatterystatus,
                            consbatteryvoltage,
                            hail,
                            hailrate,
                            heatingtemp,
                            heatingvoltage,
                            supplyvoltage,
                            referencevoltage,
                            windbatterystatus,
                            rainbatterystatus,
                            outtempbatterystatus,
                            intempbatterystatus
                        ) VALUES (
                            to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s
                        );"""

            cur.execute(query, row)
            print "Add data point from %s" % datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S')
            #print cur.fetchone()[0]
            con.commit()

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        print "PostgreSQL error: %s" % e
        sys.exit(1)

    finally:
        if con:
            con.close()


if __name__ == "__main__":
    main()
