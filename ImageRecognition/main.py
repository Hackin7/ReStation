#!/usr/bin/env python

# From https://medium.com/@guymodscientist/image-prediction-with-10-lines-of-code-3266f4039c7a
from imageai.Prediction import ImagePrediction
import os
execution_path = os.getcwd()
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath( execution_path + "/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

#image = "/arduino.jpeg" #Works, sort of, identifies as other forms of electronics
#image = "/Book.jpeg" #Doesn't work, identifies envelop or something
#image = "/usedClothes.jpeg"  #Works, can identify specialised items inside
image = "/thumbdrive.jpeg" #Not very well, identifies modem, and other elctronic stuff
image = "/flower.jpeg" #not very well
image = "/Car.jpeg" #Works very well, baseline

predictions, percentage_probabilities = prediction.predictImage(execution_path+image, result_count=5)
for index in range(len(predictions)):
    print(predictions[index] , " : " , percentage_probabilities[index])
#view rawFirstPrediction.py hosted with love by GitHub
'''
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
'''
