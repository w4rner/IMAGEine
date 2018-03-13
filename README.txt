#IMAGEine: Cooper Nederhood, Liqiang Yu, Laurence Warner

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

##############################################################################
# Part of project: image classification ######################################
# Location in folder: /transfer_learning #####################################
# Author: Liqiang Yu* ########################################################
##############################################################################
#  Liqiang Yu is responsible for /transfer_learning and part of ./django_shell.
#
#                     Documentation of Code Ownership  
#
#  "Direct copy" ~ Provided by TensorFlow tutorial and few edits made
#
#  ./transfer_learning/label_image.py
#
#  "Modified" ~ Heavily utilized templates provided by TensorFlow tutorial
#               and meaningful edits made
#
#  ./transfer_learning/retrain.py
#
#  "Original"     ~ Original code
#
#  ./django_shell/create_quiz.py


# Documentation for transfer learning process
# Relevant scripts conatined in "IMAGEine/transfer_learning/"

###Transfer Learning

(1) - Python packages to be installed if not installed already. All packages
      can be installed via pip3 according to permissions of current user

	TensorFlow:  an open-source software library for dataflow programming 
        across a range of tasks. It is a symbolic math library, and also used 
	for machine learning applications such as neural networks.

	Before start, you should install TensorFlow by typing 

        $sudo pip3 install tensorflow 


(2) - Train a new model and using the retrained model

	To train the model:

	$cd IMAGEine/transfer_learning
	$python retrain.py --image_dir ./data/landmark

	The model evaluation is at IMAGEine/transfer_learning/model_training.png
	and IMAGEine/transfer_learning/model_evaluation.png

	To use the retrained model:

	After training, you can apply the model on a test image by

	$python label_image.py \
	--graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt \
	--input_layer=Mul \
	--output_layer=final_result \
	--input_mean=128 --input_std=128 \
	--image=$HOME/IMAGEine/data/Illinois/Test/lm1/FILE_0.jpg

	Replace the image directory for your own directory, an example
	output is:

	lm1 0.89462405
	lm81 0.058848068
	lm70 0.006154099
	lm52 0.0041986946
	lm67 0.0025173887

	To view TensorBoard summaries:

	$tensorboard --logdir /tmp/retrain_logs

	then navigate your web browser to localhost:6006 to view the TensorBoard

(3) - High level summaries about model selection and code structure
      beyond the basic doc string in the actual '.py' files

	(1) Algorithm selection: Initially we proposed to use Histogram of Oriented 
	Gradients[1] to extract the features of landmarks and apply a SVM[2] on the 
	feature matrix for landmark recognition. HOG requires all objects to have 
	the same feature dimension, which means images need to have a similar aspect 
	ratio (such as 2:5 for skyscrapers). Another study[7] on this problem adds 
	SURF to extract the features, but it also requires a fixed aspect ratio. After 
	examining the landmark image data we obtained, we found out that they do not 
	usually have a similar aspect ratio thus we have to manually crop them so we gave
	up this method and decided to move forward with other possible approaches.

	Google[5] build the model using additional GPS information, but most online 
	images do not have GPS metadata associated with them. Yunpeng Li et al.[6] use
	a 3D point cloud approach on over 2 million images. Tobias Weyand et al.[8] and
	David J. Crandall et al.[10] approach the problem by using large-scale image 
	collections. These approaches are not feasible for our classification problem 
	since we only have around 2,500 images and most of them do not contain the GPS 
	information. 

	Google also provides a landmark detection API[9], which works well for some 
	famous landmarks in the world. This would not work well for our problem because
	approximately half of 87 landmarks (not famous) in Illinois have less than 30 
	valid results in Google Image search.

	Usually, training a image classification problem from the scratch takes several
	days on multiple GPUs. We found that transfer learning[12][13][14][19][21] is a
	good solution for our problem. Transfer learning is a technique that shortcuts a
	lot of training work by taking a pre-trained model for a set of categories like 
	ImageNet, and retrains from the existing weights for new classes. In our approach,
	we will only modify the last layer of the Inception V3 model since we have a 
	relatively small dataset. And we are able to retrain the model on a single CPU
	with a much smaller image set.

	(2) retrain.py: The script first downloads the Inception V3 model and gets the 
	TensorFlow Graph object, the penultimate layer and the last layer (tensor). 
	Then it splits the image data into a training set, a validation set and a testing
	set. The 'add_jpeg_decoding' uses JPEG decoding function provided by TensorFlow
	and creates a tensor for feeding the image and the output tensor after resizing 
	and decoding. After preprocessing, we calculate the bottleneck values for the 
	penultimate layer and store them locally in 'create_bottleneck_file' and 
	'run_bottleneck_on_image'. And we specify the train step, loss function,
	bottleneck tensor and a new layer for training as well as the evaluation step.
	Last but not the least, we train the final layer using backward propagation. 
	Finally, we evaluate the model performance by testing on the test data and save
	the retrained graph to local folder.


(4) - Papers and documentation read for landmark recognition

	Histogram of Oriented Gradients:
	[1] Histogram of Oriented Gradients: 
	https://www.learnopencv.com/histogram-of-oriented-gradients/

	SVM:
	[2] Handwritten Digits Classification : An OpenCV ( C++ / Python ) Tutorial:
	https://www.learnopencv.com/handwritten-digits-classification-an-opencv-c-python-tutorial/

	[3] Introduction to SURF (Speeded-Up Robust Features):
	http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html

	[4] Object Detection using Single Shot Multibox Detector:
	http://cv-tricks.com/object-detection/single-shot-multibox-detector-ssd/

	Landmark recognition:
	[5] Tour the World: building a web-scale landmark recognition engine
	./transfer_learning/google_landmark_recognition.pdf

	[6] Worldwide Pose Estimation using 3D Point Clouds:
	./transfer_learning/global_pose.pdf

	[7] Study Impact of Architectural Style and Partial View on Landmark Recognition:
	./transfer_learning/Chen-StudyImpactofArchitectural StyleandPartialViewonLandmarkRecognition-report.pdf

	[8] Visual Landmark Recognition from Internet Photo Collections: A Large-Scale Evaluation:
	./transfer_learning/1409.5400.pdf

	[9] Detecting Landmarks:
	https://cloud.google.com/vision/docs/detecting-landmarks

	[10] Recognizing Landmarks in Large-Scale Social Image Collections:
	./transfer_learning/landmarks2015book.pdf

	Deep Neural Network:
	[11] Going Deeper with Convolutions:
	./transfer_learning/GoogLeNet.pdf

	Transfer learning and TensorFlow: 
	[12] DeCAF: A Deep Convolutional Activation Feature for Generic Visual 
	Recognition
	./transfer_learning/1310.1531v1.pdf

	[13] How transferable are features in deep neural networks?
        ./transfer_learning/1411.1792.pdf

	[14] TRANSFER LEARNING IN TENSORFLOW USING A PRE-TRAINED INCEPTION-RESNET-V2 MODEL:
	https://kwotsin.github.io/tech/2017/02/11/transfer-learning.html

	[15] Inception:
	https://github.com/tensorflow/models/tree/master/research/inception

	[16] Object Detection:
	https://github.com/tensorflow/models/tree/master/research/object_detection

	[17] MobileNet:
	https://research.googleblog.com/2017/06/mobilenets-open-source-models-for.html
	
	[18] Tensorflow Tutorial 2: image classifier using convolutional neural network:
	http://cv-tricks.com/tensorflow-tutorial/training-convolutional-neural-network-for-image-classification/

	[19] Using Transfer Learning to Classify Images with TensorFlow:
	https://medium.com/@st553/using-transfer-learning-to-classify-images-with-tensorflow-b0f3142b9366

	[20] Bringing in your own dataset:
	https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md

	[21] Deep learning on Coursera by Andrew Ng:
	https://www.coursera.org/learn/machine-learning-projects

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