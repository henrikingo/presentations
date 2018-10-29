"""
Measuring latency for simple single threaded writes and reads
"""

config = {
#   Test config
    'test_name': 'Single threaded tests',
    'iterations': 100,
#   DB config
    'dbhost': 'localhost',
    'dbport': '27017',
    'dbname': 'test',
#    'dbuser': '',
#    'dbpassword': '',
}


import datetime
import math
import matplotlib.pyplot as pyplot
from   multiprocessing import Pool
import numpy
import random
import sys
import time
import pprint
import pymongo

#### functions to test
# Note that we expect caller has set global variable `db`

def foo(arg):
    print "Hello " + str(arg)

def update():
    db.hltest.update_one( {'_id': 1}, {'$inc': {'n': 1}} )

# (test_function, *args, write_concern, read_concern, read_preference)
tests = [
(update, [], pymongo.write_concern.WriteConcern(w=0)),
(update, [], pymongo.write_concern.WriteConcern(w=1)),
(update, [], pymongo.write_concern.WriteConcern(w=2)),
(update, [], pymongo.write_concern.WriteConcern(w=3)),
(update, [], pymongo.write_concern.WriteConcern(j=True)),
(update, [], pymongo.write_concern.WriteConcern(w=2, j=True)),
(update, [], pymongo.write_concern.WriteConcern(w="majority", j=False)),
(update, [], pymongo.write_concern.WriteConcern(w="majority", j=True)),
]

#### MongoDB

db = None

# provide mongod and pymongo version so that it is recorded as part of various output
def get_db_info(c) :
  c["client_name"]    = "pymongo"
  c["client_version"] = pymongo.version
  c["server_name"]    = "mongodb"
  db = get_db()
  serverStatus = db.command("serverStatus")
  c["server_version"] = serverStatus["version"]
  c["storage_engine"]  = serverStatus.get("storageEngine")
  return c


def get_db(write_concern=None) :
    client = pymongo.MongoClient( "mongodb://%s:%s/" % (config["dbhost"], config["dbport"]) )
    return pymongo.database.Database(client=client, name=config["dbname"], write_concern=write_concern)

# Test initialization
def db_init() :
  db = get_db()
  db.hltest.drop()
  # These tests do finds and updates on a single record
  db.hltest.insert( {'_id': 1, 'n': 0} )


#### test facilities

def timeit(f, *args, **kwargs):
    """Execute f and return the time it took (milliseconds)."""
    start = time.time()
    f(*args, **kwargs)
    return (time.time() - start) * 1000


def loop(f, *args, **kwargs):
    timings = []
    for i in range(config['iterations']):
        timings.append(timeit(f, *args, **kwargs))
    return timings


def report(timings, i):
    print_stats(timings, i)
    generate_graphs(timings, i)

def print_stats(timings, i):
    print "\nResults for %s iterations of %s with %s:" % (config["iterations"], tests[i][0].__name__, tests[i][2])
    print "Average (ms)   :\t%s" % numpy.average(timings)
    print "Variance (ms^2):\t%s" % numpy.var(timings)
    print "Variance/Mean  :\t%s" % ( numpy.var(timings) / numpy.average(timings) )
    print "Range (max-min/median):\t%s" % ((numpy.max(timings) - numpy.min(timings))/numpy.median(timings))
    print "Min            :\t%s" % numpy.min(timings)
    print "Median (50%%)   :\t%s" % numpy.median(timings)
    print "90%% percentile :\t%s" % numpy.percentile(timings, 0.9)
    print "95%% percentile :\t%s" % numpy.percentile(timings, 0.95) 
    print "98%% percentile :\t%s" % numpy.percentile(timings, 0.98) 
    print "99%% percentile :\t%s" % numpy.percentile(timings, 0.99) 
    print "Max            :\t%s" % numpy.max(timings)
    print
    print ", ".join(map(str, timings))
    sys.stdout.flush()

def generate_graphs(timings, i):
    pyplot.plot( range(1, config["iterations"]+1), timings, "." )
    pyplot.title( "%s, %s, %s" % (tests[i][0].__name__, tests[i][2], config["server_version"] ) )
    pyplot.ylabel("seconds")
    pyplot.xlabel("iteration")
    pyplot.ylim(0.0, pyplot.ylim()[1])  #  Set y-axis to always start from 0
    pyplot.savefig("%s-%s-%s-%s.png" % (tests[i][0].__name__, tests[i][2], config["server_version"], config["timestring"] ) , 
                   bbox_inches='tight')
    pyplot.close()





def main():
    config["timestring"] = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    get_db_info(config)
    print "Start single_threaded.py dataload with following config: "
    pprint.pprint(config)

    counter = 0
    for f, args, w in tests:
        global db
        db = get_db(w)
        db_init()
        timings = loop(f, *args)
        report(timings, counter)
        counter += 1

if __name__ == '__main__':
    main()