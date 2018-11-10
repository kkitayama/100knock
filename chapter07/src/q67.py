
import sys
from pymongo import MongoClient
import pprint as pp

target = sys.argv[1]

client = MongoClient('localhost', 27017)
db_artist = client.database_artist
collection_artist = db_artist.collection_artist

for have_aliases in collection_artist.find({'aliases': {'$exists': True}}):
    for aliase in have_aliases['aliases']:
        if aliase['name'] == target:
            pp.pprint(have_aliases)