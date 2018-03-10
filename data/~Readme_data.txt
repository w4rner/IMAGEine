##########################################################################
# Part of project: data gathering ########################################
# Location in folder: /data ##############################################
# Author: Cooper Nederhood* ##############################################
##########################################################################
* 3 small utility fn's from the webscraping PA are used. See data_fns.py for details. All other code is 100% original

# Documentation for data gathering and validation process
# Relevant scripts conatined in "IMAGEine/data/"

(1) - External programs to be installed

	geckodriver: Launching a firefox instance through selenium to do the
	web automated picture scraping requires the user to install 'geckodriver' from
	Mozilla. Earlier versions of Selenium did not need an additional driver, but current versions do. 
	Note, every browser has a different driver, so 'geckodriver' works
	for Firefox only. It needs to be in "PATH" and when I installed it automatically
	installed in the correct place, no future changes needed. I just clicked and downloaded
	at the link immediately below

	Available for download at: https://github.com/mozilla/geckodriver/releases

	For more informatin see: http://selenium-python.readthedocs.io/installation.html


(2) - Python packages to be installed if not installed already. All packages
		can be installed via pip3 according to permissions of current user

	wikipedia: 		wikipedia API to gather landmark information

	selenium: 		Selenium web automation

	urllib.request: for html retrieval and parsing
	urllib.parse: 	for html retrieval and parsing
	requests:		for html retrieval and parsing
	bs4:			for html retrieval and parsing

	time: 			to slow scraping script to avoid being shut down

	json, io, os:	general libraries for saving data

	sys:			used to accept command line arguments

	pillow:			PIL (Python Image Library) used to check if file is picture type


(3) - How to get data for a given state?
	From the command line execute the single following command:
		$ python3 get_data.py "{State}" {photo_count} {test_count} {landmark_start} {get_wiki_boolean}
			note: {get_wiki_boolean} is optional

		Examples:
			python3 get_data.py "Illinois" 30 1 0
				- gets 30 pictures for each Illinois landmark, 1 test photo. Starts at landmark #0

			nohup python3 get_data.py "North Dakota" 10 5 10 True
				- gets 10 pictures for each North Dakota landmark, 5 test photos. 
					Starts at landmark #10 and also gets the wikipedia information.
					Suppresses output and appends to .txt file

		See get_data.py for more information on command arguments


(3) - High level summaries about code structure, class design, and features beyond the basic doc 
	string in the actual '.py' files

	By running "get_data.py" the above line of code first calls the "gen_state_location_list" function
	from 'data_fns.py' which creates a list of Landmark class instances. 

	The Landmark class is defined in "Landmark.py". Essentially, this is a contained class with
	each instance reflecting a landmark in the given state. Each instance is initialized with just the
	name and the state. Landmark methods then perform the other relevant operations on the Landmark.
	These operations include getting the wiki information, getting the photo urls, and saving the photo 
	urls to disk in a structure most readily incorporated into later analyses. The operations of querying
	wikipedia for information and getting the photo urls is incredibly time consuming. To increase efficiency
	and avoid unecessary re-running of code the "save_to_file" method in the Landmark class saves out as much relevant information as possible. Each landmark has an associated 'image_info.json' file with details 
	on the data scraping process, as well as a 'landmark_info.json' file with info about the landmark. 

	As discussed, the user may want to separate the tasks of gathering the photos and gathering the wiki
	data. If the wiki data is bypassed in the run of "get_data.py" as shown above, the user can run
	the function "get_wiki_data.py" to create a csv file of the relevant wiki information. The implementation
	of the Illinois quiz uses this approach. This allowed for other streams of work, like the Machine Learning
	algorithm to procede.

	Finally, as discussed in our presentation, validating that the data retrieval process, which took days of running, 
	was a succesful representation of the available images required the generation of summary statistics when data 
	scraping. Summarizing this through the "gen_image_summary" function in 'data_fns.py' creates a simple easy to read summary for the given state summarizing the fail/successes for each images. The current incarnation of the quiz 
	uses only Illinois data, but the structure and flexibly functionality can easily be scaled to other states. In
	fact, to test that the code was still working I ran preliminary scrapes on North Dakota and Connecticut and the 
	corresponding output file structure populated as planned. 

