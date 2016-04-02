Based on
[OSM Wiki information](http://wiki.openstreetmap.org/wiki/OSM_Map_On_Garmin)
and
[instructions for contour lines](https://openmtbmap.org/about-2/archive/create-elevation-contourline-maps/).

0. Get planet extracts from [Geofabrik](http://download.geofabrik.de/).

0. Get boundaries: [bounds.zip](http://osm2.pleiades.uni-wuppertal.de/bounds/latest/bounds.zip)

0. Get sea file: [sea.zip](http://osm2.pleiades.uni-wuppertal.de/sea/latest/sea.zip)

0. Install required packages

    ```
    yaourt -S splitter mkgmap
    ```

1. Split big map file into smaller tiles:

    ```
    splitter --output-dir=./data/osm-tiles ./data/planet/europe-140130.osm.pbf
    ```

2. Figure out lat/lon bounding box of the area of interest

    ```
                     57.757
        -6.899                  -2.219
                     55.560
    ```

3. Edit findtiles.py to cover the bounding box

4. Run `findtiles.py` to generate the next commands to execute:

    ```
    python findtiles.py
    ```

5. Convert `.osm.pbf` tiles returned by `findtiles.py` to Garmin `.img`.

    ```
    mkgmap --remove-ovm-work-files 63240014.osm.pbf
    ```

6. Generate topographic data

    ```
    mono /opt/srtm2osm/Srtm2Osm.exe -bounds1 54.799805 -6.020508 55.590820 -1.801758 -o 53240014.osm -step 10 -cat 400 100
    […]
    ```

7. Make the topographic data transparent and convert to Garmin format

    ```
    mkgmap --draw-priority=10000 --transparent --remove-ovm-work-files 5*.osm
    ```

8. Copy `[56]*.img` files to the GPS' Garmin directory:

    ```
    cp [56]*.img /var/run/media/…/GARMIN/Garmin/
    ```
