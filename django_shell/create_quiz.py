#Run this file to populate website with quiz questions.

from quiz.models import Landmark, Choice
import pandas as pd

# clear previous questions
for l in Landmark.objects.all():
    l.delete()

# load csv template into pd dataframe
path = "~/IMAGEine/django_shell/template.csv"
orig_df = pd.read_csv(path, delimiter="|", index_col = "num_id")
#remove questions where machine didn't guess
df = orig_df[orig_df['machine_guess'].notnull()] 

# iterrows down df, create questions
for index, row in df.iterrows():
    temp_set = set() #choices
    visited_set = set() #avoids duplication

    correct = row['name_landmark']
    machine_guess = row['machine_guess_name']
    dec_score = row['score']
    score = "{:.2%}".format(dec_score) #convert to string percentage

    if correct == machine_guess:
        c1 = (correct, '', '', True, True)
        visited_set.add(correct)
        temp_set.add(c1)

    else:
        c1 = (correct, '', '', True, False)
        #extract row of machine's guess from original data frame
        machine_id = int(row['machine_guess'])
        machine = orig_df.loc[machine_id]
        photo = machine['test_image_url']
        wiki_url = machine['wiki_url']
        c2 = (machine_guess, photo, wiki_url, False, True)

        visited_set.add(correct)
        visited_set.add(machine_guess) 
        temp_set.add(c1)
        temp_set.add(c2)

    while len(visited_set) < 4:
        #random sample of rows
        rand_row = df.sample(n=1)
        rand_name = rand_row['name_landmark'].values[0]
        #avoid duplication
        if rand_name not in visited_set:
            c_new = (rand_name, '', '', False, False)
            visited_set.add(rand_name)
            temp_set.add(c_new)

    #set up lists of arguments
    args = [index, row['name_landmark'], row['test_image_url'], row['wiki_url'], row['wiki_summary'], score]
    choices = list(temp_set)

    #Create landmark object
    lm = Landmark(i_d = args[0], name = args[1], photo = args[2], wiki_url = args[3], wiki_sum = args[4], score = args[5])
    lm.save()

    #Create choices
    for c in choices:
        lm.choice_set.create(name = c[0], photo = c[1], wiki_url = c[2], correct = c[3], machine = c[4])