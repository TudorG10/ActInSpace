from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k 
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import pandas as pd
import numpy as np
from scipy import ndimage
import pdb

dataset = pd.read_csv("commercial.txt")
#print(dataset.head())


mask = np.random.rand(len(dataset)) < 0.9

training_set = dataset[mask]
valid_set = dataset[~mask]

#print len(dataset), len(training_set), len(valid_set)

img_arr = []
label_arr = []
#print(training_set[1:])

val_img_arr = []
val_label_arr = []

predict_arr = []
imframe2 = ndimage.imread("./../Aircraft/resized-dataset/AVLQSqgadElP9sj8MQ71.jpg")
predict_arr.append(imframe2)
np_predict_arr = np.array(predict_arr)
#pdb.set_trace()

for (x,y) in valid_set.values:
    #print((i,j))
    imframe = ndimage.imread("./../Aircraft/resized-dataset/" + x)
    val_img_arr.append(imframe)
    val_label_arr.append(np.eye(3)[y])


for (i,j) in training_set.values:
    #print((i,j))
    imframe = ndimage.imread("./../Aircraft/resized-dataset/" + i)
    img_arr.append(imframe)
    label_arr.append(np.eye(3)[j])

np_img_arr = np.array(img_arr)
np_label_arr = np.array(label_arr)
np_val_img_arr = np.array(val_img_arr)
np_val_label_arr = np.array(val_label_arr)
#print(img_arr)
#print(label_arr)

img_width, img_height = 50,50
train_data_dir = "~/Aircraft/resized-dataset"
validation_data_dir = "~/Aircraft/commercial-aircraft-valid"
nb_train_samples = 1864
nb_validation_samples = 206 
batch_size = 32
epochs = 1

model = applications.VGG19(weights = "imagenet", include_top=False, input_shape = (img_width, img_height, 3))

"""
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         (None, 256, 256, 3)       0         
_________________________________________________________________
block1_conv1 (Conv2D)        (None, 256, 256, 64)      1792      
_________________________________________________________________
block1_conv2 (Conv2D)        (None, 256, 256, 64)      36928     
_________________________________________________________________
block1_pool (MaxPooling2D)   (None, 128, 128, 64)      0         
_________________________________________________________________
block2_conv1 (Conv2D)        (None, 128, 128, 128)     73856     
_________________________________________________________________
block2_conv2 (Conv2D)        (None, 128, 128, 128)     147584    
_________________________________________________________________
block2_pool (MaxPooling2D)   (None, 64, 64, 128)       0         
_________________________________________________________________
block3_conv1 (Conv2D)        (None, 64, 64, 256)       295168    
_________________________________________________________________
block3_conv2 (Conv2D)        (None, 64, 64, 256)       590080    
_________________________________________________________________
block3_conv3 (Conv2D)        (None, 64, 64, 256)       590080    
_________________________________________________________________
block3_conv4 (Conv2D)        (None, 64, 64, 256)       590080    
_________________________________________________________________
block3_pool (MaxPooling2D)   (None, 32, 32, 256)       0         
_________________________________________________________________
block4_conv1 (Conv2D)        (None, 32, 32, 512)       1180160   
_________________________________________________________________
block4_conv2 (Conv2D)        (None, 32, 32, 512)       2359808   
_________________________________________________________________
block4_conv3 (Conv2D)        (None, 32, 32, 512)       2359808   
_________________________________________________________________
block4_conv4 (Conv2D)        (None, 32, 32, 512)       2359808   
_________________________________________________________________
block4_pool (MaxPooling2D)   (None, 16, 16, 512)       0         
_________________________________________________________________
block5_conv1 (Conv2D)        (None, 16, 16, 512)       2359808   
_________________________________________________________________
block5_conv2 (Conv2D)        (None, 16, 16, 512)       2359808   
_________________________________________________________________
block5_conv3 (Conv2D)        (None, 16, 16, 512)       2359808   
_________________________________________________________________
block5_conv4 (Conv2D)        (None, 16, 16, 512)       2359808   
_________________________________________________________________
block5_pool (MaxPooling2D)   (None, 8, 8, 512)         0         
=================================================================
Total params: 20,024,384.0
Trainable params: 20,024,384.0
Non-trainable params: 0.0
"""

# Freeze the layers which you don't want to train. Here I am freezing the first 5 layers.
for layer in model.layers[:5]:
    layer.trainable = False

#Adding custom Layers 
#the smaller the number, the weaker the network capacity, but it will train faster
x = model.output
x = Flatten()(x)
x = Dense(512, activation="relu")(x)
#higher = less overfitting, but harder to train
x = Dropout(0.2)(x)
x = Dense(512, activation="relu")(x)
predictions = Dense(3, activation="softmax")(x)

# creating the final model 
model_final = Model(input = model.input, output = predictions)

# compile the model 
model_final.compile(loss = "categorical_crossentropy", optimizer = optimizers.SGD(lr=0.0001, momentum=0.9), metrics=["accuracy"])

# Initiate the train and test generators with data Augumentation 
'''
train_datagen = ImageDataGenerator(
rescale = 1./255,
horizontal_flip = True,
fill_mode = "nearest",
zoom_range = 0.3,
width_shift_range = 0.3,
height_shift_range=0.3,
rotation_range=30)

test_datagen = ImageDataGenerator(
rescale = 1./255,
horizontal_flip = True,
fill_mode = "nearest",
zoom_range = 0.3,
width_shift_range = 0.3,
height_shift_range=0.3,
rotation_range=30)

train_generator = train_datagen.flow_from_directory(
train_data_dir,
target_size = (img_height, img_width),
batch_size = batch_size, 
class_mode = "categorical")

validation_generator = test_datagen.flow_from_directory(
validation_data_dir,
target_size = (img_height, img_width),
class_mode = "categorical")
'''
# Save the model according to the conditions  
checkpoint = ModelCheckpoint("vgg16_1.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=10, verbose=1, mode='auto')



#pdb.set_trace()
# Train the model 
'''
model_final.fit(np_img_arr,np_label_arr, batch_size = batch_size, epochs = epochs, verbose = 1,
validation_data = (np_val_img_arr, np_val_label_arr))
'''
'''
model_final.fit_generator(
train_generator,
samples_per_epoch = nb_train_samples,
epochs = epochs,
validation_data = validation_generator,
nb_val_samples = nb_validation_samples,
callbacks = [checkpoint, early])
'''
answer_array = model_final.predict(np_predict_arr, batch_size = batch_size, verbose = 1)
biggest = 0
j = 0
#print(answer_array[0][0])

for i in range(len(answer_array[0])):
   # print('this is i:')
   # print(i)
    if answer_array[0][i] > biggest:
        biggest = answer_array[0][i]
        j = i
print(answer_array)
print(j)


    
