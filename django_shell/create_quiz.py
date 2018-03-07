from quiz.models import Landmark, Choice
import pandas as pd

# clear previous questions
for l in Landmark.objects.all():
    l.delete()

# load csv template into pd dataframe
path = "template.csv"
df = pd.read_csv(path, delimiter="|")
df = df.dropna()

# iterrows down df, create questions
for index, row in df.iterrows():
    temp_set = set()
    visited_set = set()
    correct = row['name_landmark']
    machine_guess = row['machine_guess_name']
    if correct == machine_guess:
        c1 = (correct, True, True)
        visited_set.add(correct)
        temp_set.add(c1)

    else:
        c1 = (correct, True, False)
        c2 = (machine_guess, False, True)
        visited_set.add(correct)
        visited_set.add(machine_guess) 
        temp_set.add(c1)
        temp_set.add(c2)

    while len(visited_set) < 4:
        rand_row = df.sample(n=1)
        rand_name = rand_row['name_landmark'].values[0]

        if rand_name not in visited_set:
            c_new = (rand_name, False, False)
            visited_set.add(rand_name)
            temp_set.add(c_new)

    args = [row['num_id'], row['name_landmark'], row['test_image_url'], row['wiki_url'], row['wiki_summary']]
    choices = list(temp_set)

    #Create landmark object
    lm = Landmark(i_d = args[0], name = args[1], photo = args[2], wiki_url = args[3], wiki_sum = args[4])
    lm.save()

    #Create choices
    for c in choices:
        lm.choice_set.create(name = c[0], correct = c[1], machine = c[2])

