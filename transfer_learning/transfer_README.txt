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

	


	




