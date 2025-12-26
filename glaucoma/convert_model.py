import tensorflow as tf
import os

# Define paths
model_path = 'combine_cnn.h5'
tflite_path = 'model.tflite'

print(f"Loading model from {model_path}...")
try:
    # Load the Keras model
    model = tf.keras.models.load_model(model_path)
    
    # Convert the model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    # Save the model
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
        
    print(f"Success! Model saved to {tflite_path}")
    
    # Print size comparison
    h5_size = os.path.getsize(model_path) / (1024 * 1024)
    tflite_size = os.path.getsize(tflite_path) / (1024 * 1024)
    print(f"Original Size: {h5_size:.2f} MB")
    print(f"TFLite Size:   {tflite_size:.2f} MB")

except Exception as e:
    print(f"Error during conversion: {e}")
