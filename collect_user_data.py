import sys, os
import time
import json

import untappd_api as pythonUntappd
from untappd_credentials import *


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-u", '--username', help='User name',
            type='str', dest='username', default='ovarol')               
    parameters, args = parser.parse_args(sys.argv[1:])

    api = pythonUntappd.api(CLIENT_ID,CLIENT_SECRET)
    userData = api.user_info(parameters.username)['response']

    uniqueBeers = list()

    count, keepCollect = 0, True
    scanCount = 0
    while keepCollect:
        resp = api.user_distinct_beers(parameters.username, offset=count)['response']
        count += resp['beers']['count']
        uniqueBeers.extend(resp['beers']['items'])
        print('Unique beers collected: {}'.format(len(uniqueBeers)))
        scanCount += 1
        if resp['beers']['count'] != 0:
            time.sleep(1)
        else:
            break

    with open('docs/data/{}_untappd_data.json'.format(parameters.username),'w') as fl:
        fl.write(json.dumps({'user_data':userData, 'beer_data':uniqueBeers}))

