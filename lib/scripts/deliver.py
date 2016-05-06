import json
import sys
from kindle_feeder import *

f = open(sys.argv[1], "r")
raw_json = f.read()
f.close()

j = json.loads(raw_json)

bk = RailsBook(j)

filename = createMobi(bk)
print filename
