from classify_image import *

allowed = ["radio"]
class ImageRecognition:
    isAbuse = False
    image = ""
    def __init__(self):pass
    def check(self):
        possiblePredictions=""
        listOfPredictions = []
        try:
            os.system("raspistill -n -o /tmp/output.jpeg")
            predictionsData = run_inference_on_image("/tmp/output.jpeg")
            for prediction, score in predictionsData:
                possiblePredictions += prediction+","
            listOfPredictions = [i.strip() for i in possiblePredictions.split(",")]
        except:
            pass
        #print(predictionsData)
        commonThings = list(set(listOfPredictions).intersection(allowed))
        if len(commonThings) > 0:
            self.isAbuse = False
        else:
            self.isAbuse = True
            
im = ImageRecognition()
im.check()
print(im.isAbuse)
