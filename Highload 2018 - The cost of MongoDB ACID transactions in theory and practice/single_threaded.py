"""
Measuring latency for simple single threaded writes and reads
"""

config = {
#   Test config
    'test_name': 'Single threaded tests',
    'iterations': 100,
    'mongodb_url': 'mongodb+srv://dsi-user:oyKDMvndicnuIz8H@hltest-5thdf.mongodb-dev.net/test?retryWrites=true'
    #'mongodb_url': 'mongodb://10.2.0.200/test?retryWrites=true'
    #'mongodb_url': 'mongodb://localhost/test?retryWrites=true'
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
from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

#### functions to test
# Note that we expect caller has set global variable `db`

def foo(arg):
    print "Hello " + str(arg)

def update():
    db.hltest.update_one( {'_id': 1}, {'$inc': {'n': 1}} )

def readwrite(session=None):
    amount = random.randint(-100, 100)
    result1 = db.hltest.find_one( { '_id': 1 }, session=session )
    db.hltest.update_one( {'_id': 1}, {'$inc': {'n': -amount}}, session=session )
    result2 = db.hltest.find_one( { '_id': 2 }, session=session )
    db.hltest.update_one( {'_id': 2}, {'$inc': {'n': amount}}, session=session )
    cursor = db.hltest.aggregate( [ { '$group': { '_id': 'foo', 'total' : { '$sum': '$n' } } } ], session=session )
    result = cursor.next()
    if result['total'] != 200:
        print "ERROR: sum total = %s" % result['total']

def rw_session():
    with db.client.start_session(causal_consistency=True) as session:
        readwrite(session=session)

def rw_trx(write_concern=None, read_concern=None, read_preference=None):
    with db.client.start_session(causal_consistency=True) as session:
        session.start_transaction(write_concern=write_concern, read_concern=read_concern, read_preference=read_preference)
        readwrite(session=session)
        session.commit_transaction()

# (test_function, *args, write_concern, read_concern, read_preference)
#tests = [
#(update, [], (WriteConcern(w=0), None, None)),
#(update, [], (WriteConcern(w=1), None, None)),
#(update, [], (WriteConcern(w=2), None, None)),
#(update, [], (WriteConcern(w=3), None, None)),
#(update, [], (WriteConcern(j=True), None, None)),
#(update, [], (WriteConcern(w=2, j=True), None, None)),
#(update, [], (WriteConcern(w="majority", j=False), None, None)),
#(update, [], (WriteConcern(w="majority", j=True), None, None)),
#]

tests = [
(readwrite, [], (WriteConcern(w=0), ReadConcern(level="local"), ReadPreference.PRIMARY)),
(readwrite, [], (WriteConcern(w=1), ReadConcern(level="local"), ReadPreference.PRIMARY)),
(readwrite, [], (WriteConcern(w=1), ReadConcern(level="local"), ReadPreference.SECONDARY)),
(readwrite, [], (WriteConcern(w="majority"), ReadConcern(level="majority"), ReadPreference.PRIMARY)),
(readwrite, [], (WriteConcern(w="majority"), ReadConcern(level="majority"), ReadPreference.SECONDARY)),
(readwrite, [], (WriteConcern(w="majority"), ReadConcern(level="linearizable"), ReadPreference.PRIMARY)),
(rw_session, [], (WriteConcern(w="majority"), ReadConcern(level="majority"), ReadPreference.PRIMARY)),
(rw_session, [], (WriteConcern(w="majority"), ReadConcern(level="majority"), ReadPreference.SECONDARY)),
(rw_trx, [], (WriteConcern(w="majority"), ReadConcern(level="snapshot"), ReadPreference.PRIMARY)),
(rw_trx, [WriteConcern(w="majority"), ReadConcern(level="snapshot"), ReadPreference.PRIMARY], (WriteConcern(w="majority"), ReadConcern(level="snapshot"), ReadPreference.PRIMARY)),
#(rw_trx, [WriteConcern(w="majority"), ReadConcern(level="snapshot"), ReadPreference.SECONDARY], (WriteConcern(w="majority"), ReadConcern(level="snapshot"), ReadPreference.SECONDARY)),
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


def get_db(db_opts=None) :
    write_concern=db_opts[0] if db_opts else None
    read_concern=db_opts[1] if db_opts else None
    read_preference=db_opts[2] if db_opts else None

    client = pymongo.MongoClient( config["mongodb_url"] )
    return pymongo.database.Database(client=client, name="test", write_concern=write_concern, read_concern=read_concern, read_preference=read_preference)

# Test initialization
def db_init() :
  db = get_db()
  db.hltest.drop()
  # These tests do finds and updates on a single record
  db.hltest.insert( {'_id': 1, 'n': 100} )
  db.hltest.insert( {'_id': 2, 'n': 100} )


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
    print "90%% percentile :\t%s" % numpy.percentile(timings, 90)
    print "95%% percentile :\t%s" % numpy.percentile(timings, 95) 
    print "98%% percentile :\t%s" % numpy.percentile(timings, 98) 
    print "99%% percentile :\t%s" % numpy.percentile(timings, 99) 
    print "Max            :\t%s" % numpy.max(timings)
    print
    if config['iterations'] <= 100:
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
    for f, args, db_opts in tests:
        global db
        db = get_db(db_opts)
        db_init()
        timings = loop(f, *args)
        report(timings, counter)
        counter += 1

if __name__ == '__main__':
    main()