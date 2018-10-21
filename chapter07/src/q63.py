
import sys
import plyvel
import pickle

name = sys.argv[1].encode()

db = plyvel.DB('./work/db_name2tags/', create_if_missing=True)
tags_info = db.get(name)
if tags_info:
    print('value\tcount\n--------------------')
    for tag in pickle.loads(tags_info):
        print(tag['value']+'\t+'+str(tag['count']))
else:
    print('There is no tags information of the artist.')

db.close()