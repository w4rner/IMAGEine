import wikipedia as wiki 
from selenium import webdriver
import urllib.request
import time 

import json
import io
import os

import scrape_images_yahoo


urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")


class Landmark(object):

    ROOT = "/home/student/IMAGEine/data"
    SEARCH_PRE = "https://images.search.yahoo.com/search/images;_ylt=AwrEx6zOI4laligA9wKLuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRiY2sDNmxrMXU5dGNwbG0zcCUyNmIlM0QzJTI2cyUzRGNxBGZyAwRncHJpZANyVnZqREVBblNDZXNfRGRfbUtMVzJBBG10ZXN0aWQDbnVsbARuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzExBHF1ZXJ5A3NlYXJzIHRvd2VyBHRfc3RtcAMxNTE4OTM3MDQ0BHZ0ZXN0aWQDbnVsbA--?gprid=rVvjDEAnSCes_Dd_mKLW2A&pvid=vOSplzEwLjFq0D5PWZrYeQwfMjYwMQAAAAAWnBMt&fr2=sb-top-images.search.yahoo.com&p="
    SEARCH_POST = "&ei=UTF-8&iscqry=&fr=sfp"

    def __init__(self, name, state, root=""):
        '''
        Initializer for Landmark class, which is a container
        class representing a national landmark

        Other than name and state, info will be populated
        by calling corresponding methods 
        '''
        self.name = name
        self.state = state
        self.summary = ""
        self.full_text = ""
        self.url = ""

        self.root = Landmark.ROOT if root == "" else root

        self.picture_urls = []
        self.image_file_info = {}
        self.success_count = None
        self.fail_count = None
        self.yahoo_images_url = self.build_search_string()
        self.error_retrieving = []



    def get_wiki_data(self):
        '''
        Populates the summary and the full_text
        which are from the corresponding wiki pages
        '''

        control = True
        try:
            pg = wiki.page(self.name)
        except:
            control = False


        # Some names are not unique enough to return a single result - FIX
        # except:
        #   try:
        #       pg = wiki.page(self.name+" "+self.state)
        #   except:
        #       control = False
        #       print("ERROR: pg in get_wiki_data not unique")

        if control == True:
            self.summary = pg.summary
            self.full_text = pg.content
            self.url = pg.url

    def pretty_print(self, summary=False):
        '''
        Formatted print summary of landmark 
        '''

        if summary == True:
            string = "STATE: {} \nNAME: {}\n\nSUMMARY: {}\n".format(self.state, self.name, self.summary)
        
        else:
            string = "STATE: {} \nNAME: {}\n".format(self.state, self.name)

        print(string)


    def build_search_string(self):
        '''
        Constructor method, builds the google url search string 
        '''
        str_name = self.name 
        search_terms = str_name.split()
        search_terms.append(self.state)
        search_string = "+".join(search_terms)
        search_url = Landmark.SEARCH_PRE+search_string+Landmark.SEARCH_POST

        return search_url


    def get_photo_urls(self, photo_count, driver):
        '''
        Searches the globally defined search engine for images
        and returns the urls of images. Finds up to number specified
        in photo_count. Appends url's to self.picture_urls

        Inputs: 
            photo_count: (int) number of photo url's to grab
            close_driver: (boolean) for debugging, close driver when finished
        '''

        image_urls = scrape_images_yahoo.click_thru_save(self.yahoo_images_url, driver, photo_count)

        self.picture_urls = image_urls[0]
        self.success_count = image_urls[1]  
        self.fail_count = image_urls[2] 


    def save_photos(self, output_location=""):
        '''
        Will loop over the image tuples in image urls and downloads
        and saves out images. Creates a dictionary mapping each file name
        to the source url and the count of how far we went to fetch the image (for QC purposes)
        ''' 

        count = 0

        file_info = {}
        errors = []

        for image_url, result_number in self.picture_urls:
            
            file_name = "FILE_"+str(count)

            try:
                urllib.request.urlretrieve(image_url, output_location+"/"+file_name)
                time.sleep(3)
                count += 1
            except:
                errors.append(image_url)


            file_info[file_name] = {'source_url':image_url, 'image_rank':result_number}

        file_info['~summary'] = {'urls_scraped': self.success_count, 'urls_not_scraped': self.fail_count}
        self.image_file_info = file_info
        self.error_retrieving = errors[:]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   


    def __str__(self):
        '''
        string representation of object instance
        '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        return "STATE: {} \nNAME: {}".format(self.state, self.name)
                                                                                                                                                                                                                                                                    
    def save_to_file(self):
        '''
        Within Landmark.ROOT, saves the instance information
        into a json file into a file structure ordered by
        ROOT >> State >> Landmark Name >> Files
        '''

        info_dict = {"name": self.name, "state":self.state, "summary":self.summary,
                    "full_text": self.full_text, "url": self.url, "picture_urls": self.picture_urls}

        info_json = json.dumps(info_dict, sort_keys=True, indent=4)

        # File structure
        assert os.path.exists(self.root), "ERROR: check root global value"
        st_root = self.root + "/" + self.state 
        if os.path.exists(st_root) == False:
            os.mkdir(st_root)

        lm_root = st_root + "/" + self.name.strip().replace(" ", "_")
        if os.path.exists(lm_root) == False:
            os.mkdir(lm_root)

        info_file = 'landmark_info.json'
        with io.open(lm_root + "/" + info_file, 'w', encoding='utf8') as outfile:
            outfile.write(info_json)

        if os.path.exists(lm_root+"/pics") == False:
            os.mkdir(lm_root+"/pics")

        self.save_photos(lm_root+"/pics")
        image_info_json = json.dumps(self.image_file_info, sort_keys=True, indent=4)
        image_info_file = 'image_info.json'
        with io.open(lm_root + "/" + image_info_file, 'w', encoding='utf8') as outfile:
            outfile.write(image_info_json)

        error_dict = {"failed_retrieving_urls": self.error_retrieving}
        error_retrieving_json = json.dumps(error_dict)
        error_retrieving_file = 'error_retrieving.json'
        with io.open(lm_root + "/" + error_retrieving_file, 'w', encoding='utf8') as outfile:
            outfile.write(error_retrieving_json)


        print("SAVED AT: \n{}".format(lm_root))


        










