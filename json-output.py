#!/usr/bin/env python
import psycopg2
import json
import sys

SQL_DOMAIN = "select domain from usage group by domain"
# Top 20 domains by bytes
SQL_DOMAIN_BYTES = SQL_DOMAIN + " order by sum(bytes) desc limit 20;"
# Top 20 domains by requests
SQL_DOMAIN_HITS = SQL_DOMAIN + " order by sum(hits) desc limit 20;"

def error(msg):
    print msg
    sys.exit(1)

try:
    conn = psycopg2.connect("dbname='www_usage'")
except:
    error("Unable to connect to database")

cur = conn.cursor()
cur.execute(SQL_DOMAIN_BYTES)
top_bytes = [x[0] for x in cur]
cur.execute(SQL_DOMAIN_HITS)
top_hits = [x[0] for x in cur]

data = dict(by_bytes=top_bytes, by_hits=top_hits, domains={})

DATERANGE = "> now() - '14 days'::interval"

cur.execute("""SELECT date, domain, sum(hits) as hits, sum(bytes) as bytes
               FROM usage
               WHERE date """ + DATERANGE + """
               GROUP BY date, domain
               ORDER BY domain, date;""")
totals = []
for date, domain, tr_hits, tr_bytes in cur:
    d = data['domains'].get(domain, [])
    d.append([str(date), long(tr_hits), long(tr_bytes)])
    data['domains'][domain] = d

cur.execute("""SELECT date, sum(hits) as hits, sum(bytes) as bytes
               FROM usage
               WHERE date """ + DATERANGE + """
               GROUP BY date
               ORDER BY date;""")
totals = []
for date, tr_hits, tr_bytes in cur:
    totals.append([str(date), long(tr_hits), long(tr_bytes)])
data['domains']['TOTAL'] = totals

#print json.dumps(data, indent=2)
print json.dumps(data)
