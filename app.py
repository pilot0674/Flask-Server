from flask import Flask
import json, time
from pytz import timezone
from datetime import datetime
from dateutil import parser
import urllib.request
est = timezone('EST')
app = Flask(__name__)
stopnum = "9147"
url = 'https://api-v3.mbta.com/predictions?&filter[stop]=' + stopnum + '&include=trip,stop,vehicle'
def getDateTime(Time):
    current = datetime.now(est)
    unixtime = time.mktime(current.timetuple())
    arrcnvt = datetime.strptime(Time, '%Y-%m-%dT%H:%M:%S')
    arrEpoch = time.mktime(arrcnvt.timetuple())
    train = int(arrEpoch - unixtime)/60
    mints, secs = str(train).split('.')
    return int(mints)
def nicify(j):
    r = []
    k = {}
    if len(['data']) > 0:
        n = 0
        h = {} 
        for t in j['included']:
            if t['type'] == 'trip':
                h[t['id']] = t['attributes']['headsign']
                #r[h[t['id']]] = []
        for p in j['data']:
            if p['attributes']['departure_time'] == None:
                tm = p['attributes']['arrival_time'][0:19]
            else:
                tm = p['attributes']['departure_time'][0:19]
            hs = h[p['relationships']['trip']['data']['id']]
            r.append({"time":getDateTime(tm), "headsign":hs})
        k['stuff'] = r
        return json.dumps(k)
    else:
        r.append({"time":0, "headsign":"NOPRED"})
        k['stuff'] = r
        return json.dumps(f)
@app.route('/')
def display():
    contents = urllib.request.urlopen(url).read()
    j = json.loads(contents.decode('utf-8'))
    k = nicify(j)
    return k

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

