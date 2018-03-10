import pandas as pd 

path_landmarks = "../data/Illinois/Info/summary_lm.csv"
path_machine_guess = "../transfer_learning/machine_guess.csv"
path_wiki_info = "../data/Illinois/Illinois_wiki.csv"

# By Cooper Nederhood (original)

def create_template(path_landmarks, path_machine_guess, output_filename, path_wiki_info = None):
	'''
	Data relevant for the quiz template resides in 2 locations, possible 3 
	depending on how the wiki data was pulled. Gather this information and
	prepare in format easiest to incorporate into Django. Save as csv (pipe delimited)

	Inputs:
		- path_landmarks: (str) path to landmark 'summary_lm.csv'
		- path_machine_guess: (str) path to ML alogrithm guess
		- output_filename: (str) name of output file
		- path_wiki_info: (str) if wiki data added after, path to wiki info

	'''

	need_wiki = path_wiki_info != None

	if need_wiki == True:
		df_landmarks = pd.read_csv(path_landmarks, delimiter="|", usecols=['id', 'name', 'test_image_url'])
		df_wiki = pd.read_csv(path_wiki_info, delimiter="|")
	else:
		df_landmarks = pd.read_csv(path_landmarks, delimiter="|", usecols=['id', 'name', 'test_image_url', 'wiki_url', 'wiki_summary'])

	df_machine = pd.read_csv(path_machine_guess)

	merge_df = df_landmarks.merge(df_machine, on='id', how='outer')
	if need_wiki == True:
		merge_df = merge_df.merge(df_wiki, on='id', how='outer')

	# decode the machine guess by merging on the landmark file
	merge_df.rename( columns={"id":'num_id', "name": "name_landmark", "machine_guess":"id"}, inplace = True)
	merge_df = merge_df.merge(df_landmarks[['id', 'name']], on='id', how='outer')
	merge_df.rename( columns={"id":'num_id', "name": "machine_guess_name", "id":"machine_guess"}, inplace = True)

	merge_df['num_id'] = merge_df['num_id'].str.replace("lm", "")
	merge_df['num_id'] = pd.to_numeric(merge_df['num_id'], errors='coerce') 

	merge_df['machine_guess'] = merge_df['machine_guess'].str.replace("lm", "")
	merge_df['machine_guess'] = pd.to_numeric(merge_df['machine_guess'], errors='coerce') 

	order = ['num_id', 'name_landmark', 'machine_guess', 'machine_guess_name', 'score', 'test_image_url', 'wiki_url', 'wiki_summary']
	merge_df = merge_df[order]
	merge_df.sort_values('num_id', inplace=True)


	merge_df = merge_df[ pd.isnull(merge_df.num_id) == False]


	merge_df.to_csv(output_filename, sep="|", index=False)

	return  merge_df, df_landmarks, df_machine, df_wiki

merge_df, df_landmarks, df_machine, df_wiki = create_template(path_landmarks, path_machine_guess, "template.csv", path_wiki_info)
