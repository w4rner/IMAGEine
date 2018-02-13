import wikipedia as wiki 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import io
import os

import scrape_images


class Landmark(object):

	ROOT = "/home/student/Documents"
	SEARCH_PRE = "https://www.google.com/search?tbm=isch&source=hp&biw=1536&bih=759&ei=i855Wt65KonwsAWRzaTYBw&q="
	SEARCH_MID = "&oq="
	SEARCH_POST = "&gs_l=img.3...5886.7255.0.7448.0.0.0.0.0.0.0.0..0.0....0...1ac.1.64.img..0.0.0....0.uq9inO-sWU0"

	def __init__(self, name, state, root=""):
		'''
		Initializer for Landmark class, which is a container
		class representing a national landmark 
		'''
		self.name = name
		self.state = state
		self.summary = ""
		self.full_text = ""
		self.url = ""
		self.picture_urls = []
		self.pictures = []
		self.training_data = []
		self.testing_data = []
		self.root = Landmark.ROOT if root == "" else root
		self.google_images_url = self.build_search_string()


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
		# 	try:
		# 		pg = wiki.page(self.name+" "+self.state)
		# 	except:
		# 		control = False
		# 		print("ERROR: pg in get_wiki_data not unique")

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
		search_url = Landmark.SEARCH_PRE+search_string+Landmark.SEARCH_MID+search_string+Landmark.SEARCH_POST

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

		image_urls = scrape_images.get_pics_from_search(search_url, driver, photo_count)

		return image_urls  


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

		print("SAVED AT: \n{}".format(lm_root))


		










