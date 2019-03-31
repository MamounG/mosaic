#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.error
from urllib import request
from bs4 import BeautifulSoup
import ssl
import json

hashtag = "tedxodense"

class Insta_Image_Links_Scraper:


    def getlinks(self, hashtag, url):
        print(url)
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
            t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        print ('Scraping links with #' + hashtag+"...........")
        img_links = []
        for post in data['entry_data']['TagPage'][0]['graphql'
        ]['hashtag']['edge_hashtag_to_media']['edges']:
            image_src = post['node']['thumbnail_resources'][1]['src']
            img_links.append(image_src)
            # hs = open(hashtag + '.txt', 'a')
            # hs.write(image_src + '\n')
            # hs.close()
        return img_links


    #compare links to previous ones
    def find_new_links(self, img_links, file_path):
        hs = open(file_path, 'r')
        data = hs.read()
        data_list = data.split("\n")
        new_links = []
        for line in img_links:
            tmp = False
            for img_path in data_list:
                if line == img_path:
                    tmp = True
                    break
            if not tmp:
                new_links.append(line)

        print(new_links)
        print(len(new_links))



        return new_links

    #download new images
    def download_new_images(self, img_list, target_dir):
        i = 0
        for im in img_list:
            print(im)
            v_list = im.split(".jpg")[0].split("/")
            s = v_list[len(v_list) - 1]
            f = open(target_dir + s + ".jpg", 'wb')
            f.write(request.urlopen(im).read())
            f.close()
            hs = open(hashtag + '.txt', 'a')
            hs.write(im + '\n')
            hs.close()


    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        with open('hashtag_list.txt') as f:
            self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        all_img_links = self.getlinks(hashtag,
                                      'https://www.instagram.com/explore/tags/'
                                      + hashtag + '/')
        new_img_link = self.find_new_links(all_img_links, hashtag + ".txt")
        # self.download_new_images(new_img_link, "hashtag_pictures/")
        self.download_new_images(new_img_link, "../../realTimePictureCreation/mosaicImages/")

if __name__ == '__main__':
    obj = Insta_Image_Links_Scraper()
    obj.main()
