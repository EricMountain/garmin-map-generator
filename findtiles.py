#!/usr/bin/env python3

# Can't remember where the original came from, possibly the defunct
# http://touren.mospace.de/kachel.html

import re

# Bounding box (lat, lon, lat, lon) bottom-left - top-right
# Same format as areas.list
box = (55.560, -6.899, 57.757, -2.219)

def checkInsideArea(area, coords):
    if (coords[0] >= area[0] and
        coords[0] <= area[2] and
        coords[1] >= area[1] and
        coords[1] <= area[3]):
        return True
    else:
        return False

def checkBoxPartlyInsideArea(box, area):
    if (checkInsideArea(area, [box[0], box[1]]) or
        checkInsideArea(area, [box[0], box[3]]) or
        checkInsideArea(area, [box[2], box[1]]) or
        checkInsideArea(area, [box[2], box[3]])):
        return True
    else:
        return False

print(box)

f = open('./data/osm-tiles/areas.list', 'r')
prevLineIsTile = False
tile = None
for line in f:
    match1 = re.match('^#       : ([-0-9.]+),([-0-9.]+) to ([-0-9.]+),([-0-9.]+)', line)
    if match1:
        # Note input is lat, lon, lat, lon
        area = [float(match1.group(i)) for i in range(1, 5)]
        if checkBoxPartlyInsideArea(box, area):
            #print(area)
            #print(tile)
            print('mkgmap --precomp-sea=./data/planet/sea.zip --bounds=./data/bounds.zip --max-jobs --remove-ovm-work-files --output-dir=./data/garmin ./data/osm-tiles/%s.osm.pbf' % (tile))
            print('mono /opt/srtm2osm/Srtm2Osm.exe -bounds1 %f %f %f %f -o 5%s.osm -step 10 -cat 400 100' % (area[0], area[1], area[2], area[3], tile[1:]))
            print('mkgmap --draw-priority=10000 --transparent --remove-ovm-work-files 5%s.osm' % (tile[1:]))
            tile = None

    match2 = re.match('([0-9]+): .*', line)
    if match2:
        tile = match2.group(1)

f.close()
