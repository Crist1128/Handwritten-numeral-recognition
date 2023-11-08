# validate_model.py

from data_processing import load_and_preprocess_data
import tensorflow as tf
from tensorflow import keras as kr
from keras.models import load_model

# 数据路径
data_dir = "E:/pythontraining/MNIST/test"

# 加载和预处理测试数据
test_data = load_and_preprocess_data(data_dir)

# 加载训练好的模型
model = load_model('mnist_model.h5')  # 请使用你训练好的模型文件名

# 评估模型准确性
test_loss, test_accuracy = model.evaluate(test_data)

print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
