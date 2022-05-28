import os, sys, time, copy, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from datetime import datetime
from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators
from ml_util import convert_ts, convert_strtime
import configparser
import json
import requests
import collections


def log(rs):

    with open("/tmp/es_sql.log", "a") as es_sql_debug:
        es_sql_debug.write('\n')
        es_sql_debug.write('-- %s --\n' % type(rs))
        es_sql_debug.write(json.dumps(rs, indent=4))
        es_sql_debug.write('\n')
        es_sql_debug.flush()

    # if type(rs) is dict and  'error' in rs:
    #     if 'reason' in rs['error']:
    #         msg = rs['error']['reason']
    #         msg = msg.replace('{','')
    #         msg = msg.replace('}','')
    #         raise ValueError(msg)

@Configuration(type='reporting', local=True)
class Reports(GeneratingCommand):
    spl = Option(require=True)

    def __init__(self, *args, **kwargs):
        super(Reports, self).__init__(*args, **kwargs)

        config = configparser.ConfigParser()
        config.read('../local/els.conf')
        self.server_url = config.get('SERVER','URL')
        self.server_token = config.get('SERVER','TOKEN')        
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization':self.server_token}


    def generate(self):
        
        # spl = 'tstats c from packetbeat by source.ip'
        post_data = {'spl':self.spl}
        sri = self.search_results_info
        if hasattr(sri, 'search_et'): 
            if hasattr(sri, 'search_lt'):
                post_data['gte'] = convert_ts(sri.search_et)
                post_data['lt'] = convert_ts(sri.search_lt)

        res = requests.post(self.server_url+'/api/els/search',
        headers=self.headers,
        data=json.dumps(post_data))
        log(post_data)
        rs = json.loads(res.content)
        log(rs)
        if len(rs['data']) > 0:
            for item in rs['data'][1]:
                
                record = collections.OrderedDict()
                for idx, key in enumerate(rs['data'][0]):
                    record[key] = item[idx]
                yield record

        
if __name__ == "__main__":
    dispatch(Reports, sys.argv, sys.stdin, sys.stdout, __name__)



   