from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse,HttpResponse




from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from django.http import FileResponse
from django.conf import settings
import os



def home(request):
    return render(request,'index.html')

def prediction(request):
    def softmax(x):
        exp_x = np.exp(x - np.max(x))  # Subtracting max value for numerical stability
        return exp_x / exp_x.sum(axis=1, keepdims=True)
    if request.method=='POST' and request.FILES['image']:
        image=request.FILES['image']

        with open('temp_image.jpg','wb+')as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # TFLite Inference
        lite_model_path = 'model.tflite'
        interpreter = tf.lite.Interpreter(model_path=lite_model_path)
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Load image
        img = load_img('temp_image.jpg', target_size=(256,256))
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = img_array.reshape(1, 256, 256, 3) # Specific shape for TFLite

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], img_array)

        # Run inference
        interpreter.invoke()

        # Get output tensor
        predict = interpreter.get_tensor(output_details[0]['index'])
        
        normalized_output_exp = softmax(predict)
        percentages_exp = normalized_output_exp * 100
        print(percentages_exp)
        result = np.argmax(predict)
        output=''

        if result == 0:
            if percentages_exp[0][0]> 70:
                output="Severe Stage"
            else:
                output="Initial Stage"
        else:
            output="Normal Eye"

        prediction=output

        os.remove('temp_image.jpg')

        return JsonResponse({'prediction':prediction})
    # else:
        # return JsonResponse({'error':'invalid request'})
    
    return HttpResponse("hi")
    
    
    

