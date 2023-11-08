# train.py

from data_processing import load_and_preprocess_data
from model import build_model

# 数据路径
data_dir = "E:/pythontraining/MNIST/train"

# 加载和预处理数据
train_data = load_and_preprocess_data(data_dir)

# 构建模型
model = build_model()

# 训练模型
model.fit(train_data, epochs=20)

# 保存模型
model.save('mnist_model_20.h5')
