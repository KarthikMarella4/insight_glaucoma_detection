import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def representative_dataset_gen():
    for _ in range(10):
        # Generate random input data of the correct shape and type
        # VGG19 input is 256x256x3. Range 0-255 or normalized?
        # The model expects preprocessed input. Let's assume standard float input.
        yield [np.random.uniform(0, 255, size=(1, 256, 256, 3)).astype(np.float32)]

try:
    print("Loading model...")
    model = keras.models.load_model('combine_cnn.h5')
    
    print("Configuring converter...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Enforce full integer quantization
    converter.representative_dataset = representative_dataset_gen
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    
    # Optional: restricts input/output to int8 too (further reduction but needs careful IO handling)
    # Let's keep IO as float for compatibility with existing code, 
    # but weights will be int8 (4x smaller).
    converter.inference_input_type = tf.float32 
    converter.inference_output_type = tf.float32

    print("Converting...")
    tflite_model = converter.convert()

    with open('model_int8.tflite', 'wb') as f:
        f.write(tflite_model)
        
    size_mb = os.path.getsize('model_int8.tflite') / (1024 * 1024)
    print(f"Success! model_int8.tflite created. Size: {size_mb:.2f} MB")

except Exception as e:
    print(f"Error: {e}")
