import wikipedia as wiki 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time 

import json
import io
import os

# By Cooper Nederhood (original)


def click_via_action_keys(base_url, driver, target_count):
    '''
    Given a base_url from which to begin the image scraping, a
    FireFox Selenium browser instance and a target_count of pictures to
    fetch, returns image urls and summary information about the data
    gathering process used for data verification purposes

    Inputs:
        - base_url (string): of a url address to yahoo images search result
        - driver (selenium firefox webdriver): headless browser instance
        - target_count (int): goal number of photos
                NOTE: accepts "ALL" if user wants all images in first page of search
    '''

    driver.get(base_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    all_imgs = driver.find_elements_by_tag_name('img')

    total_img_count = len(all_imgs)

    if target_count == "ALL":
        target_count = total_img_count

    img_urls = []
    success_count = 0
    fail_count = 0

    cur_img_num = -1

    for first_img in all_imgs:
        cur_img_num += 1

        if len(img_urls) == target_count:
            break

        # only click on first image if it is clickable
        if hasattr(first_img, 'click') == True:
            first_img.click()
            time.sleep(2)

            # Now do the level two clicking
            all_hrefs = driver.find_elements_by_tag_name('a')
            filtered_hrefs = [el for el in all_hrefs if el.get_attribute('title') == 'View Image']

            next_elem_to_click = filtered_hrefs[0]

            # CONTROL+click to open in new tab
            cur_window_handle = driver.window_handles[0]
            if hasattr(next_elem_to_click, 'click') == True:
                shift_click = ActionChains(driver)
                shift_click.key_down(Keys.CONTROL)
                shift_click.click(next_elem_to_click)
                shift_click.key_up(Keys.CONTROL)
                shift_click.perform()
                time.sleep(2)

                # Switch windows to new tab
                next_window_handle = driver.window_handles[-1]
                driver.switch_to_window(next_window_handle)
                time.sleep(2)
                
                # Get the new url
                cur_url = driver.current_url
                cur_url_lower = cur_url.lower()

                # Verify the image and append, if np
                if ".jpg" in cur_url_lower or ".png" in cur_url_lower or ".jpeg" in cur_url_lower: 
                    img_urls.append(  (cur_url, cur_img_num)  )
                    print("CURRENT COUNT = {}".format(len(img_urls)))
                    success_count += 1

                else:
                    print("Final image file type did not conform: FAIL")
                    print("\t\t", cur_url)
                    fail_count += 1

                # close the new window and move back to original window
                driver.close()
                driver.switch_to_window(cur_window_handle)
                time.sleep(2)

                driver.back()
                time.sleep(2)

            else:
                print("Second level clickthru not possible: FAIL")
                fail_count += 1
                continue

        else:
            print("First level 'img' not clickable: FAIL")
            fail_count += 1
            continue

    return img_urls, success_count, fail_count 







