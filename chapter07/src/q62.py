
import sys
import plyvel

area = sys.argv[1].encode()
count = 0

db = plyvel.DB('./work/db_name2area/', create_if_missing=True)
for key, val in db:
    if val == area:
        count += 1
print(count)

db.close()