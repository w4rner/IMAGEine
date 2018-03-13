##########################################################################

# Part of project: Prototype Django web application: "Know Your State" ########################################

# Location in folder: /prototype ##############################################

# Author: Laurence Warner ##############################################

##########################################################################

#                     Documentation of Code Ownership  
# All file paths within prototype/
#  "Direct copy" ~ 
#
#  All except noted below
#
#  "Modified" ~ 

#	prototype/
		settings.py
		urls.py
	quiz/
		urls.py
		views.py
		

#  "Original"     ~ Original code
#
#  quiz/
		models.py
		static/
		templates/

Also: within django_shell/
#	"Original" - create_quiz.py 
Collaborative effort with Cooper & Rex.


(1) External packages to be installed

Django 2.0
	pip3 install --user django

(2) Python packages to install if not installed already

os
sys
pandas

(3) How to run app

From the top prototype/ folder, run the following command line arguments:

python3 manage.py runserver

In your web browser go to the url provided.

python3 manage.py makemigrations quiz
python3 manage.py migrate

To launch the ipython3 shell:

python3 manage.py shell

From within the shell:

run ../django_shell/create_quiz.py

This will populate the website with questions.
Click on a question number to play that question. Enjoy trying to outguess the machine!

(4) Notes on code.

prototype/quiz/
	models.py 
		creates the two classes for the quiz: Landmark & Choice. Note: photo_url is a string.
	views.py
		how pages are created. Note how user choice is collected: each time a user votes, all choice objects have the guess attribute reset to False. Then only the one chosen changes to True. 
	templates/quiz/
		All three files use bootstrap styling. 

		detail.html
			A question page for given landmark passed to template. Ingenuity: passing image url as attribute of landmark into img tag.
			A form to collect user vote. For the given landmark passed to the template, loop through choices and display. 

		results.html
			Results. If statements to show different outcomes depending upon user choice & whether machine is correct. E.g. for each choice, check whether machine guessed. If not the correct landmark, display info on this choice too.

django_shell/
	create_quiz.py
		1). Read csv as pandas dataframe
		2). Loop over rows. For each row:
		a) collect info on that Landmark object's attributes
		b) if machine guessed a different landmark, collect attributes from that row for Choice
		c) randomly generate unused rows to ensure four choices in total
		d) Create the Landmark and Choice objects and save them into the database.
