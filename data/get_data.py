import scrape_images_yahoo
import data_fns 
from selenium import webdriver


# Run this from linux command line using nohup command format

illinois_list = data_fns.gen_state_location_list("Illinois")

driver = webdriver.Firefox()
# lm10 = illinois_list[10]
# lm10.get_photo_urls(20, driver)


start_count = 0
cur_count = start_count

for landmark in illinois_list[start_count:]:
	#landmark.get_wiki_data()
	landmark.get_photo_urls(26, driver)
	landmark.save_to_file(test_count=1)																																																																																																																																																																

	print("COMPLETED:")
	print(cur_count)
	print(landmark)
	print()
	cur_count += 1
