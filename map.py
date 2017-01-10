#!/usr/bin/env python
#%matplotlib inline
#pbf  http://download.geofabrik.de/europe.html
#https://switch2osm.org/serving-tiles/building-a-tile-server-from-packages/
# localy http://a.tile.osm.org/3/4/2.png
# http://a.tile.komoot.de/komoot-2/3/4/2.png
#feh --reload 0.3 map.png
# for ((i=0;i<100;i++)); do echo map.jpg; done | xargs  mpv -speed=0.8
#
# downloadosmtiles --lat=49:51 --lon=13:16 --zoom=15

import time 
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display

m1 = StaticMap(256, 256, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=15)
Step=0.006
maxmar=1
for xrng in range(100):
    XOffs=Step*xrng
    for yrng in range(100):
        YOffs=Step*yrng
        XCoor,YCoor=(14.2397+XOffs, 49.8644+YOffs)
        print(XCoor,YCoor,'    ',XOffs,YOffs,'  ',xrng,yrng)
        mam=CircleMarker( (XCoor,YCoor),  'red', 5)
        m1.add_marker(mam, maxmarkers=maxmar )
        image=m1.render()
        #image=image.resize( (1000,600) )
        if yrng%10: image.save('map.png')
        ##display( image )
        ##image.show()
        ##time.sleep(0.1)
#        mam=CircleMarker( (XCoor,YCoor),  'blue', 5)
#        m1.add_marker( mam, maxmarkers=maxmar )


