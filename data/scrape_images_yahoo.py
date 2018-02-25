import wikipedia as wiki 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time 

import json
import io
import os

def click_via_action_keys(base_url, driver, target_count):

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




def click_thru_save(base_url, driver, target_count):
    '''
    Given a yahoo base_url, first click on an img type.
    Then, click on the button called "view image"
    Save the current_url
    Go back two levels
    Click on the next button
    '''

    driver.get(base_url)
    print(base_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    all_imgs = driver.find_elements_by_tag_name('img')

    img_count = len(all_imgs)

    if target_count == "ALL":
        target_count = img_count


    img_urls = []
    success_count = 0
    fail_count = 0

    print("Original search finds {} images".format(img_count))
    for cur_img_num in range(img_count): 

        if len(img_urls) < target_count:
            img_url = get_img_number_x(base_url, driver, cur_img_num)
            if img_url != None:
                img_urls.append(  (img_url, cur_img_num)  )
                success_count += 1
            else:
                print("Valid image not found: Next")
                fail_count += 1
        else:
            break


    return img_urls, success_count, fail_count 

    

def get_img_number_x(base_url, driver, cur_img_num):
    '''
    There are documented issues with Seleniums ability to send
    keys and open up new tabs. When opening up the final image tab,
    the original link is lost. Going 'back' cannot recover the now stale 
    link. This workaround results in less efficiency, but it is necessary
    '''
 
    driver.get(base_url)

    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    all_imgs = driver.find_elements_by_tag_name('img')
    print("----subcall finds {} images, getting image #{}".format(len(all_imgs), cur_img_num))
 
    img = all_imgs[cur_img_num]

    try:
        img.click()
        time.sleep(3)

        all_hrefs = driver.find_elements_by_tag_name('a')
        filtered_hrefs = [el for el in all_hrefs if el.get_attribute('title') == 'View Image']

        assert len(filtered_hrefs) == 1, "ERROR: found >1 'view image' link"
        next_elem_to_click = filtered_hrefs[0]

        next_elem_to_click.click()
        time.sleep(3)

        cur_url = driver.current_url
        cur_url_lower = cur_url.lower()

        if ".jpg" in cur_url_lower or ".png" in cur_url_lower or ".jpeg" in cur_url_lower: 
            rv = cur_url

        else:
            print("Link not jpg or png \n{}".format(cur_url))
            rv = None
    except:
        print("Found not clickable img object - continue")
        rv = None 

    return rv 







