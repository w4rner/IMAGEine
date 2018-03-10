import scrape_images_yahoo
import data_fns 
from selenium import webdriver
import sys

# Run this from linux command line using nohup command format
# nohup python3 get_data.py "Illinois" 30 1 0
# nohup python3 get_data.py "Illinois" 30 1 28

def pull_data(state, photo_count, test_photo_count, start_count, get_wiki=False):
    '''
    Given a state, and counts for photos and test number, 
    downloads and saves out structured data.

    Inputs:
        - state (string): state to pull data for
        - photo_count (int): total number of photos to shoot for
        - test_photo_count (int): number of test photos
        - start_count (int): landmarks are indexed from zero. This 
                    tells which landmark to begin at. The script can take a long
                    time to run depending on the desired image count. If the machine
                    times out, breaking the script, this allows for the user to 
                    resume scraping at the point the script broke, rather than regather
                    all earlier photos. Suppressing output with the 'nohup' run assists this
        - get_wiki (bool): eventually the user needs to get relevant wiki data. This can be done
                    now (True) or later using a different function (False). This is added to prioritize
                    the more difficult task of image gathering
    '''

    print("get_wiki=", get_wiki)
    landmark_list = data_fns.gen_state_location_list(state)

    driver = webdriver.Firefox()

    cur_count = start_count

    for landmark in landmark_list[start_count:]:
        if get_wiki == True:
            print("In inner loop")
            landmark.get_wiki_data()
        landmark.get_photo_urls(photo_count, driver)
        landmark.save_to_file(test_count=test_photo_count)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

        print()
        print("COMPLETED:")
        print(cur_count)
        print(landmark)
        print()
        cur_count += 1

    driver.close()

if __name__ == "__main__":
    print(sys.argv)
    print(len(sys.argv))
    state = str(sys.argv[1])
    photo_count = int(sys.argv[2])
    test_photo_count = int(sys.argv[3])
    start_count = int(sys.argv[4])

    if len(sys.argv) > 5:
        wiki_bool = bool(sys.argv[5])
    else:
        wiki_bool = False

    print("Getting data for: {}".format(state))
    print("Target photo count is: {}".format(photo_count))
    print("Test photo count is: {}".format(test_photo_count))
    print("Will begin at landmark #: {}".format(start_count))
    print("Getting wikipedia data now: {}".format(wiki_bool))
    print()

    pull_data(state, photo_count, test_photo_count, start_count, wiki_bool)

    print("**************DATA PULL COMPLETE**************")

    info_file_location = "/" + state + "/Info"
    data_fns.gen_image_summary(info_file_location)