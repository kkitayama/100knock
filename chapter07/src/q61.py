
import sys
import plyvel

name = sys.argv[1].encode()

db = plyvel.DB('./work/db_name2area/', create_if_missing=True)
area_info = db.get(name)
if area_info:
    print(area_info.decode())
else:
    print('There is no area information of the artist.')

db.close()