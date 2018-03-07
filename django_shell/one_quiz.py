from quiz.models import Landmark, Choice


# Landmark args
# list: i_d, name, photo
args = [0, "Robert S. Abbott House",'''https://upload.wikimedia.org/wikipedia/commons/2/2a/Robert_S
._Abbott_House%2C_4742_Martin_Luther_King_Drive%2C_Chicago_Cook_Cou
nty%2C_Illinois.jpg''']

# Choices args
# list: name, correct, machine
c0 = ["Robert S. Abbott House", True, False]
c1 = ["Lincoln's Tomb", False, True]
c2 = ["Cahokia Mounds", False, False]
c3 = ["Willis Tower", False, False]
choices = [c0, c1, c2, c3]



#Create landmark object
lm = Landmark(i_d = args[0], name = args[1], photo = args[2])
lm.save()

#Create choices
for c in choices:
    lm.choice_set.create(name = c[0], correct = c[1], machine = c[2])