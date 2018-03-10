import scrape_images_yahoo
import data_fns 
from selenium import webdriver
import sys

# Run this from linux command line using nohup command format
# python3 get_wiki_data.py "Illinois" "Illinois_wiki"

def pull_wiki_data(state, file_name):
    '''
    Given a state outputs a csv file of the wiki information for 
    each of the landmarks for that state. Names file according 
    to file_name

    Pulling wiki data takes time, so to prioritize the fetching
    of photos, the user can opt NOT to download wiki data when 
    running get_data.py
    
    This function then gets the wiki data after the fact

    Inputs:
        - state (string): state to pull data for
        - file_name (string): name of output file
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
