import wikipedia as wiki 
from selenium import webdriver
import urllib.request
import time 

import json
import io
import os

import scrape_images_yahoo


class Landmark(object):

    LM_NUMBER = 0
    ROOT = "/home/cnederhood/IMAGEine/data"
    SEARCH_PRE = "https://images.search.yahoo.com/search/images;_ylt=AwrEx6zOI4laligA9wKLuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRiY2sDNmxrMXU5dGNwbG0zcCUyNmIlM0QzJTI2cyUzRGNxBGZyAwRncHJpZANyVnZqREVBblNDZXNfRGRfbUtMVzJBBG10ZXN0aWQDbnVsbARuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzExBHF1ZXJ5A3NlYXJzIHRvd2VyBHRfc3RtcAMxNTE4OTM3MDQ0BHZ0ZXN0aWQDbnVsbA--?gprid=rVvjDEAnSCes_Dd_mKLW2A&pvid=vOSplzEwLjFq0D5PWZrYeQwfMjYwMQAAAAAWnBMt&fr2=sb-top-images.search.yahoo.com&p="
    SEARCH_POST = "&ei=UTF-8&iscqry=&fr=sfp"

    def __init__(self, name, state, root=""):
        '''
        Initializer for Landmark class, which is a container
        class representing a national landmark

        Other than name and state, info will be populated
        by calling corresponding methods

        Attributes:
        - name: (str) of landmark name
        - id: (str) standardized id of landmark 
        - state: (str) landmark's state
        - summary: (str) first paragraph from wikipedia
        - full_text: (str) full text from wikipedia entry
        - url: (str) url to wikipedia entry
        - root: (str) directory location used to save data
        - picture_urls: (list) of tuples of url's pulled from yahoo images search, 
                        along with the priority (i.e. ("www.image.com/image0", 1) indicates url is 1st url checked
        - image_file_info: (dict) info on train, test, and errors of images urls
        - success_count: (int) when fetching image url's, the count of 'img' types added to picture_url list
        - fail_count: (int) when fetching image url's, the count of 'img' types NOT added to picture_url list
        - yahoo_images_url: (str) yahoo images search url
        '''

        self.name = name
        self.id = "lm"+str(Landmark.LM_NUMBER)
        Landmark.LM_NUMBER += 1

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
            driver: (webdriver) Selenium firefox webdriver instance
        '''

        image_urls = scrape_images_yahoo.click_thru_save(self.yahoo_images_url, driver, photo_count)

        self.picture_urls = image_urls[0]
        self.success_count = image_urls[1]  
        self.fail_count = image_urls[2] 


    def save_photos(self, test_count, test_location, training_location):
        '''
        Will loop over the image tuples in image urls and downloads
        and saves out images. Creates a dictionary mapping each file name
        to the source url and the count of how far we went to fetch the image (for QC purposes)

        Inputs:
            test_counts: (int) how many photos to include in testing data
            output_location: (str) location to save photo
        ''' 

        # save test data
        in_test_data = 0
        test_errors = []
        test_info = {}
        test_index = 0
        for image_url, result_number in self.picture_urls[::-1]:

            if in_test_data == test_count:
                break
            else:
                file_name = "FILE_"+str(in_test_data)+".jpg"

                try:
                    urllib.request.urlretrieve(image_url, test_location +"/"+file_name)

                    time.sleep(3)
                    in_test_data += 1
                    test_info[file_name] = {'source_url':image_url, 'image_rank':result_number}
                except:
                    test_errors.append( (image_url, result_number) )
                test_index += 1

        # save training data
        in_train_data = 0
        train_errors = []
        train_info = {}
        for image_url, result_number in self.picture_urls[0:len(self.picture_urls) - test_index]:

            file_name = "FILE_"+str(in_train_data)+".jpg"

            try:
                urllib.request.urlretrieve(image_url, training_location +"/"+file_name)
                time.sleep(3)
                in_train_data += 1
                train_info[file_name] = {'source_url':image_url, 'image_rank':result_number}
            except:
                train_errors.append( (image_url, result_number) )

        self.image_file_info = {"TEST_DATA": test_info, "TRAIN_DATA": train_info,
                                "ERRORS_TRAIN": train_errors, "ERRORS_TEST": test_errors }


    def __str__(self):
        '''
        string representation of object instance
        '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        return "STATE: {} \nNAME: {}".format(self.state, self.name)
                                                                                                                                                                                                                                                                    
    def save_to_file(self, test_count):
        '''
        Within Landmark.ROOT, saves the instance information
        into a json file into a file structure ordered by
        ROOT >> State >> {Test, Train, Info} >> self.id

        Inputs: 
            test_count: (int) how many photos to include in test data
        '''

        # Basic file structure
        assert os.path.exists(self.root), "ERROR: check root global value"
        st_root = self.root + "/" + self.state 
        if os.path.exists(st_root) == False:
            os.mkdir(st_root)

        sub_dir = ['Test', 'Train', 'Info']
        for next_dir in sub_dir:
            new_path = st_root + "/" + next_dir
            if os.path.exists(new_path) == False:
                os.mkdir(new_path)

            if os.path.exists(new_path + "/" + self.id) == False:
                os.mkdir(new_path + "/" + self.id)

        test_root = st_root + "/Test/" + self.id
        train_root = st_root + "/Train/" + self.id
        info_root = st_root + "/Info/" + self.id

        # Save landmark_info.json
        info_dict = {"name": self.name, "state":self.state, "summary":self.summary,
                    "full_text": self.full_text, "url": self.url, "id": self.id, 
                    "success_count": self.success_count, "fail_count": self.fail_count}

        info_json = json.dumps(info_dict, sort_keys=True, indent=4)

        info_file = 'landmark_info.json'
        with io.open(info_root + "/" + info_file, 'w', encoding='utf8') as outfile:
            outfile.write(info_json)

        # Save out photos
        print("Calling save_photos with:{}".format(st_root))
        self.save_photos(test_count=test_count , test_location=test_root , training_location=train_root)

        # Save image_info.json
        image_info_json = json.dumps(self.image_file_info, sort_keys=True, indent=4)
        image_info_file = 'image_info.json'
        with io.open(info_root + "/" + image_info_file, 'w', encoding='utf8') as outfile:
            outfile.write(image_info_json)


        print("SAVED AT: \n{}".format(st_root))


        










