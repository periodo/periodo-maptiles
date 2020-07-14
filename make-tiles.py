#! /usr/bin/env python3

import os
import sys
import json
from osgeo import gdal

LATITUDES = [
    +(48 + (7/12)),
    +30,
    +(14 + (29/60)),
    0,
    -(14 + (29/60)),
    -30,
    -(48 + (7/12)),
    -90
]

ZOOM_LEVELS = {
    # zoom level: (tile_count, latitudes, percentage_scale)
    0: (1,  LATITUDES[-1:],  5.0),
    1: (8,  LATITUDES[1::2], 10.0),
    2: (16, LATITUDES,       100.0),
}


source = gdal.Open(sys.argv[1])
height = source.RasterYSize

transform = source.GetGeoTransform()
# ([0], [3]) is the top left corner as (long, lat)
min_longitude = transform[0]
max_latitude = transform[3]
# [1] pixel width: 0.01666666666667 (1/60)
pixel_width = transform[1]
# [5] pixel height: -0.01666666666667 (-1/60)
negative_pixel_height = transform[5]


def longitude(xpixel):
    return round(min_longitude + xpixel * pixel_width, 2)


def latitude(yline):
    return round(max_latitude + yline * negative_pixel_height, 2)


def yline(latitude):
    return int((latitude - max_latitude) / negative_pixel_height)


def iterate_latitudes(latitudes):
    y = 0
    prev_latitude = None
    for latitude in latitudes:
        if prev_latitude is None:
            height = yline(latitude)
        else:
            height = yline(latitude) - yline(prev_latitude)
        yield y, height
        y += height
        prev_latitude = latitude


manifest = [{} for n in range(len(ZOOM_LEVELS))]
tile_id = 0

for zoom, (tile_count, latitudes, scale) in ZOOM_LEVELS.items():
    dirname = f'maptiles/{zoom}'
    os.makedirs(dirname, exist_ok=True)
    tile_width = int(source.RasterXSize / tile_count)
    for x in range(0, source.RasterXSize, tile_width):
        for y, tile_height in iterate_latitudes(latitudes):
            #        <xpixel> <yline> <w> <h>
            window = [x, y, tile_width, tile_height]
            min_lon = longitude(x)
            min_lat = latitude(y + tile_height)
            max_lon = longitude(x + tile_width)
            max_lat = latitude(y)
            filename = f'{min_lon}x{min_lat}x{max_lon}x{max_lat}.jpg'
            path = f'{dirname}/{filename}'
            gdal.Translate(
                path,
                source,
                srcWin=window,
                widthPct=scale,
                heightPct=scale)
            manifest[zoom][f'{tile_id}!{zoom}/{filename}'] = [
                min_lon, min_lat, max_lon, max_lat
            ]
            tile_id += 1
            print(path)

with open('maptiles/manifest.json', 'w') as f:
    json.dump(manifest, f)
