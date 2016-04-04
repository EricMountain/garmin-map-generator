#!/usr/bin/env python3

import re

# Bounding box (lat, lon, lat, lon) bottom-left - top-right
# Same format as areas.list
box = (55.560, -6.899, 57.757, -2.219)

def checkOverlap(box, area):
    if min(box[1], box[3]) > max(area[1], area[3]): return False
    if max(box[1], box[3]) < min(area[1], area[3]): return False
    if min(box[0], box[2]) > max(area[0], area[2]): return False
    if max(box[0], box[2]) < min(area[0], area[2]): return False
    return True

print(box)

f = open('./data/osm-tiles/areas.list', 'r')
prevLineIsTile = False
tile = None
for line in f:
    match1 = re.match('^#       : ([-0-9.]+),([-0-9.]+) to ([-0-9.]+),([-0-9.]+)', line)
    if match1:
        # Note input is lat, lon, lat, lon
        area = [float(match1.group(i)) for i in range(1, 5)]
        if checkOverlap(box, area):
            print('/usr/bin/time mkgmap --precomp-sea=./data/planet/sea.zip --bounds=./data/planet/bounds.zip --max-jobs --remove-ovm-work-files --output-dir=./data/garmin ./data/osm-tiles/%s.osm.pbf' % (tile))
            print('/usr/bin/time mono /opt/srtm2osm/Srtm2Osm.exe -d ./data/srtm -bounds1 %f %f %f %f -o ./data/osm-tiles/5%s.osm -step 10 -cat 400 100' % (area[0], area[1], area[2], area[3], tile[1:]))
            print('/usr/bin/time mkgmap --draw-priority=10000 --transparent --remove-ovm-work-files --output-dir=./data/garmin ./data/osm-tiles/5%s.osm' % (tile[1:]))
            tile = None

    match2 = re.match('([0-9]+): .*', line)
    if match2:
        tile = match2.group(1)

f.close()
