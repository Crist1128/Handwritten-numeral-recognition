from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap
from canvas import DrawingCanvas
from keras.models import load_model
from PIL import Image
import numpy as np

# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Handwritten Digit Recognizer")
        self.setFixedSize(QSize(720, 720))
        self.predicted_digits = []

        # 创建一个用于绘制的画布部件
        self.drawing_canvas = DrawingCanvas(self)

        # 创建清除按钮
        clear_button = QPushButton(text="Clear")
        button_layout = QVBoxLayout()
        button_layout.addWidget(clear_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.drawing_canvas, 10)
        main_layout.addWidget(button_widget, 1)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 连接清除按钮的点击事件到处理函数
        clear_button.clicked.connect(self.clear_drawing)

        # 加载预训练模型
        self.model = load_model('mnist_model_20.h5')

        # 标签用于显示预测的数字
        self.result_label = QLabel("Predicted Digit: ")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label, 1)

    # 处理清除按钮点击事件
    def clear_drawing(self):
        self.drawing_canvas.clear()
        self.predicted_digits = []

    # 预测数字并更新结果标签
    def predict_digit(self, image):
        prediction = self.model.predict(image.reshape(1, 28, 28, 3))
        predicted_digit = np.argmax(prediction)
        self.predicted_digits.append(str(predicted_digit))
        self.result_label.setText(f"Predicted Digit: {''.join(self.predicted_digits)}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()