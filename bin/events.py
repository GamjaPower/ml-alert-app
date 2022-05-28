import os, sys, time, copy, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from datetime import datetime
from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators
import configparser
import json
import requests
import collections
from ml_util import convert_ts, convert_strtime

def log(rs):

    with open("/tmp/es_sql.log", "a") as es_sql_debug:
        es_sql_debug.write('\n')
        es_sql_debug.write('-- %s --\n' % type(rs))
        es_sql_debug.write(json.dumps(rs, indent=4))
        es_sql_debug.write('\n')
        es_sql_debug.flush()


@Configuration(type='events', local=True)
class Events(GeneratingCommand):
    spl = Option(require=True)

    def __init__(self, *args, **kwargs):
        super(Events, self).__init__(*args, **kwargs)

        config = configparser.ConfigParser()
        config.read('../local/els.conf')
        self.server_url = config.get('SERVER','URL')
        self.server_token = config.get('SERVER','TOKEN')
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization':self.server_token}


    def generate(self):
        
        # spl = 'index=fw _all'
        post_data = {'spl':self.spl}
        sri = self.search_results_info
        if hasattr(sri, 'search_et'): 
            if hasattr(sri, 'search_lt'):
                post_data['gte'] = convert_ts(sri.search_et)
                post_data['lt'] = convert_ts(sri.search_lt)
        log(post_data)
        res = requests.post(self.server_url+'/api/elp/search',
            data=json.dumps(post_data),
            headers=self.headers
        )
        
        rs = json.loads(res.content)
        log(rs)
        if len(rs['items']) > 0:
            for item in rs['items']:
                if '_raw' not in item: 
                    item['_raw'] = json.dumps(item)                
                if '_time' not in item and '@timestamp' in item and (item['@timestamp'].startswith('20') or item['@timestamp'].startswith('19')):
                    item['_time'] = convert_strtime(item['@timestamp'])
                yield item

        
if __name__ == "__main__":
    dispatch(Events, sys.argv, sys.stdin, sys.stdout, __name__)



   
