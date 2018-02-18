import scrape_images_yahoo
import data_fns 
from selenium import webdriver


# Run this from linux command line using nohup command format

illinois_list = data_fns.gen_state_location_list("Illinois")

driver = webdriver.Firefox()

start_count = 0
cur_count = start_count
for landmark in illinois_list[start_count:]:
	#landmark.get_wiki_data()
	landmark.get_photo_urls("ALL", driver)
	landmark.save_to_file()																																																																																																																																																																

	print("COMPLETED:")
	print(cur_count)
	print(landmark)
	print()
	cur_count += 1
