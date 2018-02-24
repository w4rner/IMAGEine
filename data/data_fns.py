import urllib.parse
import requests
import os
import bs4

import wikipedia as wiki 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import landmark 

STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico','New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
ILLINOIS = ['Illinois']
OTHER_DISTRICTS = ['District of Columbia', 'U.S. Commonwealths and Territories', 'Associated States', 'Foreign States']
URL_ROOT = "https://en.wikipedia.org/wiki/List_of_National_Historic_Landmarks_in_"
TABLE_STRUCTURE = {"class": ["wikitable", "sortable"]}

def url_to_soup(url):
    '''
    Given a url, returns a BS4 soup object
    '''
    req = get_request(url)
    assert req, "CHECK get_request"

    text = read_request2(req)
    assert text != "", "in request_to_soup: text is blank string"

    return bs4.BeautifulSoup(text)

def get_request(url):
    '''
    Open a connection to the specified URL and if successful
    read the data.

    Inputs:
        url: must be an absolute URL

    Outputs:
        request object or None

    Examples:
        get_request("http://www.cs.uchicago.edu")
    '''

    if True:
        try:
            r = requests.get(url)
            if r.status_code == 404 or r.status_code == 403:
                r = None
        except Exception:
            # fail on any kind of error
            r = None
    else:
        r = None

    return r


def read_request2(request):
    '''
    Return data from request object.  Returns result or "" if the read
    fails..
    '''

    try:
        return request.text.encode()
    except Exception:
        print("read failed: " + request.url)
        return ""


def gen_state_location_list(state):
    '''
    Given a string of a full state name, returns a 
    list of location objects in that state 

    State name in format: Illinois, Connecticut
    '''

    location_list = []

    wiki_soup = url_to_soup(URL_ROOT+state)

    sorted_tables = wiki_soup.find_all("table", TABLE_STRUCTURE)
    main_table = sorted_tables[0]
    rows = main_table.find_all("tr")

    # first row is header
    for row in rows[1:]:
        data = row.find_all("td")
        location_name = data[0].text.strip()
        landmark_obj = landmark.Landmark(location_name, state)
        location_list.append(landmark_obj)



    return location_list 


def gen_image_summary(info_path):
	'''
	info_path is an 'Info' directory resulting from the saving 
	out of landmark images for a given state. This function summarizes 
	and aggregates a few important statistics for each landmark and 
	outputs into a csv. 

	Inputs:
		- info_path: (str) of 'Info' directory

	** No return value, creates "lm_summary.csv"
	'''

	info_dir = os.fsencode(info_path)
	lm_dir_list = os.listdir(info_dir)

	with open('lm_summary.csv', 'w') as output_csv:

		for lm_dir in lm_dir_list:
			dir_str = os.fsdecode(lm_dir)

			if dir_str.find('lm') == 0:
				lm_path = info_path + "/" + dir_str

				with open(lm_path + "/landmark_info.json", "r") as lm_file:
					lm_dict = json.load(lm_file)

				with open(lm_path + "/image_info.json", "r") as image_file:
					image_dict = json.load(image_file)

				test_image_url = image_dict['TEST_DATA']['FILE_0.jpg']['source_url']
				lm_data_list = [ lm_dict['id'], lm_dict['name'], test_image_url, lm_dict['summary'], lm_dict['url']   ]

				lm_summary_line = "|".join(lm_data_list)

				output_csv.write(lm_summary_line)
				output_csv.write('\n')











