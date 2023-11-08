# data_processing.py
import tensorflow as tf
from tensorflow import keras as kr
from keras.preprocessing.image import ImageDataGenerator

def load_and_preprocess_data(data_dir):
    datagen = ImageDataGenerator(
        rescale=1.0/255.0,
    )

    train_data = datagen.flow_from_directory(
        data_dir,
        target_size=(28, 28),
        batch_size=32,
        class_mode='categorical'
    )

    return train_data
