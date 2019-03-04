#!/usr/bin/env python


import image_slicer
import shutil
import os
import json



destination_dir = "../realTimePictureCreation/mask/"
destination_info = "../realTimePictureCreation/data/tiles.json"

# clean destination file
dir_status= os.path.isdir(destination_dir) and os.path.exists(destination_dir)
if dir_status:
    shutil.rmtree(destination_dir)

try:
    os.mkdir(destination_dir)
except OSError:
    print ("Creation of the directory %s failed" % destination_dir)




tiles = image_slicer.slice('originalImage/TedX.jpg', 1000, save=False)
image_slicer.save_tiles(tiles, directory=destination_dir, prefix='slice')
dict = {}
for tile in tiles:
    tile_dict = {}
    file_path_split = tile.filename.split("/")
    file_name = file_path_split[len(file_path_split)-1]
    # tile_dict["file_name"] = file_name
    tile_dict["number"] = tile.number
    tile_dict["position"] = tile.position
    tile_dict["coords"] = tile.coords
    dict[file_name] = tile_dict

with open(destination_info, 'w') as fp:
    json.dump(dict, fp)
print "done"