#!/usr/bin/env python


import cv2
from time import sleep
import os
import random
import image_slicer
from image_slicer import Tile
import numpy as np
import json
from PIL import Image

path_to_mosaic_image = "mosaicImages/"
path_to_mask = "mask/"
path_to_masked_pictures = "maskedPictures/"
previous_picture_list = "data/pictureList.json"
previous_mask_list = "data/maskList"
path_to_tiles_info = "data/tiles.json"

path_to_result_image = "../ResultAndUpload/resultPicture/res.png"

#loop to see if any new picture was added
# in the loop
#  list all picture in file
#  compare them to pictures that has already been used
#  loop through the new pictures
#   add name to name list
#   choose random mask from available masks
#   create new pictures
#  generate new picture from the list of all pictures
#  sleeo(5)


#slice_[row]_[column]

def clean_and_init():
    #add a clean of the folder
    img = cv2.imread(path_to_mask + "slice_01_01.png")
    height, width, rrr = img.shape
    blank_image = np.zeros((height, width, rrr), np.uint8)
    all_masks = os.listdir(path_to_mask)
    for mask_name in all_masks:
        cv2.imwrite(path_to_masked_pictures + mask_name, blank_image)


def run():
    i=0
    while True:
        picture_list = list_pictures()
        new_pictures_only = compare_to_previous(picture_list)

        new_addings = False
        # print new_pictures_only
        for pic_name in new_pictures_only:
            print pic_name
            add_picture_to_previous(pic_name)
            mask_file_name = choose_random_mask()
            if (mask_file_name != ""):
                pic_path = path_to_mosaic_image+pic_name
                mask_path = path_to_mask+mask_file_name
                new_picture = create_new_picture(pic_path, mask_path)
                save_picture(new_picture, mask_file_name)
                add_mask_to_used(mask_file_name)
                new_addings = True
        i = i + 1
        print i
        if new_addings:
            generate_result_picture()
        sleep(5)


def list_pictures():
    picture_list = os.listdir(path_to_mosaic_image)
    return picture_list

def compare_to_previous(all_pictures):
    only_new_pics = []
    f = open(previous_picture_list, "r")
    used_pics = f.read().split("\n")
    f.close()
    for p in all_pictures:
        if p not in used_pics:
            only_new_pics.append(p)

    return only_new_pics

def add_picture_to_previous(pic):
    f = open(previous_picture_list, "a")
    f.write(pic +"\n")
    f.close()

def choose_random_mask():
    all_masks = os.listdir(path_to_mask)
    with open(previous_mask_list) as f: s = f.read()
    used_masks = s.split("\n")
    unused_masks = []
    for o_mask in all_masks:
        to_be_added = True
        for u_mask in used_masks:
            if o_mask == u_mask:
                to_be_added = False
                break
        if to_be_added:
            unused_masks.append(o_mask)
    # print unused_masks
    if  len(unused_masks) > 0:
        return random.choice(unused_masks)
    else:
        return ""

def create_new_picture(path_to_pic, path_to_mask):
    img = cv2.imread(path_to_pic)
    mask = cv2.imread(path_to_mask)

    height, width, rrr = mask.shape

    resized_image = cv2.resize(img, (width, height))

    dst = cv2.addWeighted(resized_image, 0.3, mask, 0.7, 0)

    return dst

def add_mask_to_used(mask_name):
    with open(previous_mask_list, 'a') as file:
        file.write("\n"+mask_name)

def save_picture(pic, mask_name):
    cv2.imwrite(path_to_masked_pictures + mask_name, pic)

def generate_result_picture():
    all_pictures = os.listdir(path_to_masked_pictures)
    # tiles_info = {}
    with open(path_to_tiles_info) as json_file:
        tiles_info = json.load(json_file)

    tiles = []
    for pict_name in all_pictures:
        if pict_name in tiles_info.keys():
            image = Image.open(path_to_masked_pictures+pict_name)
            tile = Tile(image, tiles_info[pict_name]["number"], tiles_info[pict_name]["position"], tiles_info[pict_name]["coords"])
            tiles.append(tile)
            # print tile
        else:
            print "ERROR: the following picture does not exist in original data"
            print pict_name

    glob_image = image_slicer.join(tiles)
    glob_image.save(path_to_result_image)
    # glob_image.show()

import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))


clean_and_init()
run()

