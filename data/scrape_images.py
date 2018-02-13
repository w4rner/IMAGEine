import wikipedia as wiki 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import io
import os

#url = "https://www.google.com/search?tbm=isch&source=hp&biw=1536&bih=759&ei=TS16WuKfDseAtgWEzKcw&q=sears+tower&oq=sears+tower&gs_l=img.3...64600.66152.0.66263.0.0.0.0.0.0.0.0..0.0....0...1ac.1.64.img..0.0.0....0.q996ARtSelE"

#driver = webdriver.Firefox()


def get_first_level_urls(url, driver):
    '''
    Given a firefox webdriver and desired url,
    returns a list of the valid hrefs to explore.
    This is akin to the first level of clicking on a
    result in a google images search 

    Inputs: 
        url: (string) corresponding to the url of the google images search 
        driver: (selenium driver) Firefox type selenium webdriver instance

    Returns:
        filtered_hrefs: (list) of strings which are urls to search for images
    '''

    # Goes to the google images search results page
    driver.get(url)

    # Get links. So filtered_hrefs will contain all the first level clicks, ie they
    #               will get you to the point where you only need to click "View Image"
    element_search = driver.find_elements_by_tag_name("a")

    all_hrefs = []
    for element in element_search:
        
        href = element.get_attribute('href')
        all_hrefs.append(href)

    filtered_hrefs = []
    for href in all_hrefs:
        if href != None:
            if "imgres?imgurl" in href:
                filtered_hrefs.append(href)

    return filtered_hrefs

def get_final_level_urls(list_filtered_hrefs, driver, image_count):
    '''
    Once we have gathered the hrefs for the first layer, we can then explore 
    each of the next layer and find the .jpg link stored within that next 
    layer

    Inputs:
        list_filtered_hrefs: (list) of strings which are urls to search for images
        driver: (selenium driver) Firefox type selenium webdriver instance
        image_count: (int) max number of image urls to gather 

    Returns:
        all_jpgs: (list) of image urls (.jpg or .png)
    '''

    all_jpgs = []
    for filtered_href in list_filtered_hrefs:

        # Check if we are at the desired image count
        if len(all_jpgs) >= image_count:
            break

        try:
            new_jpgs = find_jpg_url(filtered_href, driver)
            all_jpgs.extend(new_jpgs)

        except:
            print("ERROR: {}".format(filtered_href))

    return all_jpgs

def find_jpg_url(filtered_href, driver):
    '''
    Given a single filtered_href, the filtered_href shouuld contain a url link 
    to a .jpg image, which is what we want. This should search 
    for such links and return a list of candidates

    TO-DO: each should return just 1 link but we are not 
            explicitly checking for that now

    Inputs:
        filtered_hrefs: (string) which is urls to search for images
        driver: (selenium driver) Firefox type selenium webdriver instance

    Returns:
        probable_links: (list) of image urls (.jpg or .png)
    '''

    all_jpg_results = []
    # Now that we have each of the valid 2nd layer refs, go to them

#   for filtered_href in filtered_hrefs[1:]:
    driver.get(filtered_href)

    a_type_elements = driver.find_elements_by_tag_name("a")

    probable_links = []

    for element in a_type_elements:
        el_target = element.get_attribute('target')
        el_class = element.get_attribute('class')
        el_href = element.get_attribute('href')

        if el_target == "_blank" and el_class == "irc_fsl i3596" and el_href != None:
            if ".jpg" in el_href or ".png" in el_href:
                probable_links.append(el_href)
                all_jpg_results.append(el_href)

    return probable_links


def get_pics_from_search(google_image_url, driver, image_count):
    '''
    Given a google images url to scrape, returns a list of .png and .jpg 
    urls. Returns pic_count number of urls 

    Inputs:
        google_image_url: (string) of google images search url 
        driver: (selenium driver) Firefox type selenium webdriver instance
        image_count: (int) max number of image urls to gather 

    Returns:
         all_jpgs: (list) of image urls (.jpg or .png)
   
    '''

    first_level_urls = get_first_level_urls(google_image_url, driver)
    all_image_urls = get_final_level_urls(first_level_urls, driver, image_count)

    if len(all_image_urls) < image_count:
        print("ERROR: could not get desired image count")

    return all_image_urls




