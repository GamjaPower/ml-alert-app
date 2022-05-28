import os, sys, time, copy, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from datetime import datetime
from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators
import json


@Configuration(type='events', local=True)
class Hello(GeneratingCommand):
    
    def __init__(self, *args, **kwargs):
        super(Hello, self).__init__(*args, **kwargs)

    def generate(self):
        item = {'no':'1', 'name':'jason', 'count':100}
        yield {'_time':time.time(), '_raw':json.dumps(item)}

        
if __name__ == "__main__":
    dispatch(Hello, sys.argv, sys.stdin, sys.stdout, __name__)



   
