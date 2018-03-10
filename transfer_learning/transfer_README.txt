#  Liqiang Yu is responsible for /transfer_learning and part of ./django_shell.
#
#                     Documentation of Code Ownership  
#
#  "Direct copy" ~ Provided by TensorFlow tutorial and few edits made
#  
#  label_image.py
#   
#  "Modified" ~ Heavily utilized templates provided by TensorFlow tutorial
#               and meaningful edits made
#
#  retrain.py



###Transfer Learning

#Model Training

Before start, you should install TensorFlow by typing 

$sudo pip3 install tensorflow 

To train the model:

$cd IMAGEine/transfer_learning

$python retrain.py --image_dir ./data/landmark

The result is at IMAGEine/transfer_learning/model_training.png
and IMAGEine/transfer_learning/model_evaluation.png


#Model Using

After training, you can apply the model on a test image by

$python label_image.py \
--graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt \
--input_layer=Mul \
--output_layer=final_result \
--input_mean=128 --input_std=128 \
--image=$HOME/IMAGEine/data/Illinois/Test/lm1/FILE_0.jpg






