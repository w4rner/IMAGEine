import scrape_images_yahoo
import data_fns 
from selenium import webdriver
import sys

# Run this from linux command line using nohup command format
# nohup python3 get_data.py "Illinois" 30 1 0
# nohup python3 get_data.py "Illinois" 30 1 28

def pull_wiki_data(state, file_name):
    '''
    Given a state outputs a csv file of the wiki information for 
    each of the landmarks for that state.

    Inputs:
        - state (string): state to pull data for
    '''

    landmark_list = data_fns.gen_state_location_list(state)

    for landmark in landmark_list:
        print(landmark)
        landmark.get_wiki_data()

    with open(file_name+'.csv', "w") as f:

        cols = ['id', 'wiki_url', 'wiki_summary']
        header_line = "|".join(cols)
        f.write(header_line)
        f.write("\n")

        cur_line = 0
        for lm in landmark_list:
            data_line = lm.id + "|" + lm.url + "|" + lm.summary
            f.write(data_line)
            f.write("\n")
            cur_line+=1

    return landmark_list
    

if __name__ == "__main__":
    state = str(sys.argv[1])
    file_name = str(sys.argv[2])

    print("Getting wiki data for: {}".format(state))
    print("Saving to file: {}".format(file_name))
    print()

    pull_wiki_data(state, file_name)

    print("**************DATA PULL COMPLETE**************")
