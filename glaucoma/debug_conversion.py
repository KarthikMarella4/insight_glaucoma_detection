import tensorflow as tf
from tensorflow import keras
import os

def convert_and_measure(name, strategy_fn):
    print(f"\n--- Attempting: {name} ---")
    try:
        model = keras.models.load_model('combine_cnn.h5')
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        # Apply strategy
        strategy_fn(converter)
        
        tflite_model = converter.convert()
        
        filename = f"model_{name}.tflite"
        with open(filename, 'wb') as f:
            f.write(tflite_model)
            
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"Result: {filename} = {size_mb:.2f} MB")
        return filename, size_mb
    except Exception as e:
        print(f"Failed: {e}")
        return None, 0

def strategy_float16(converter):
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

def strategy_dynamic_int8(converter):
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # No target_spec means dynamic range quantization (Int8 weights)
    
def strategy_experimental_size(converter):
    # Some versions support this
    converter.optimizations = [tf.lite.Optimize.EXPERIMENTAL_SPARSITY]

    if not os.path.exists('combine_cnn.h5'):
        print("Error: combine_cnn.h5 not found")
    else:
        # convert_and_measure("float16", strategy_float16)
        convert_and_measure("dynamic_int8", strategy_dynamic_int8)
