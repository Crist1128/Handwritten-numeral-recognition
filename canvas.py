from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer
from PIL import Image
from PIL import ImageOps
import numpy as np
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer
from PIL import Image
from PIL import ImageOps
import numpy as np

class DrawingCanvas(QtWidgets.QLabel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 保存对主窗口的引用
        self.canvas = QtGui.QPixmap(self.size())  # 创建画布 QPixmap，与部件大小相同
        self.canvas.fill(Qt.white)  # 填充画布白色
        self.last_x, self.last_y = None, None  # 初始化上一个绘制点为 None
        self.timer = QTimer()  # 创建定时器
        self.timer.setSingleShot(True)  # 设置定时器为一次性触发
        self.timer.timeout.connect(self.save_drawing)  # 定时器触发时调用 save_drawing 函数
        self.last_drawing = np.full((720, 720), 255, dtype=np.uint8)
        self.cnt = 0

    def paintEvent(self, event):
        # 在绘制部件时，绘制当前画布上的内容
        with QtGui.QPainter(self) as painter:
            painter.drawPixmap(0, 0, self.canvas)
        return super().paintEvent(event)

    def resizeEvent(self, event):
        # 当部件大小变化时，调整画布大小以匹配新的部件大小
        self.canvas = QtGui.QPixmap(event.size())  # 创建新的画布，与新部件大小相同
        self.canvas.fill(Qt.white)  # 填充画布白色
        self.last_drawing = np.full((720, 720), 255, dtype=np.uint8)
        self.cnt = 0
        return super().resizeEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:  # 当鼠标左键按下时
            if self.last_x is None:
                self.last_x = event.x()
                self.last_y = event.y()
            else:
                painter = QtGui.QPainter(self.canvas)
                pen = painter.pen()
                pen.setWidth(15)
                pen.setCapStyle(Qt.RoundCap)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(self.last_x, self.last_y, event.x(), event.y())
                painter.end()
                self.last_x = event.x()
                self.last_y = event.y()
                self.update()  # 更新部件，触发 paintEvent
            self.timer.start(200)  # 启动定时器，1秒后触发 save_drawing
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.timer.stop()  # 停止定时器
        self.timer.start(1000)  # 重新启动定时器，1秒后触发 save_drawing
        self.last_x, self.last_y = None, None  # 重置上一个绘制点为 None
        return super().mouseReleaseEvent(event)

    def clear(self):
        self.canvas.fill(Qt.white)  # 清空画布，填充为白色
        self.last_drawing = np.full((720, 720), 255, dtype=np.uint8)
        self.main_window.predicted_digits = []  # 清空预测结果数组
        self.update()  # 更新部件，触发 paintEvent

    def save_drawing(self):
        self.last_x, self.last_y = None, None  # 重置上一个绘制点为 None
        image = self.canvas.toImage()
        image = Image.fromqpixmap(image)  # 转换为 PIL 图像

        image = image.convert('L')  # 转为灰度图像

        image_array = np.array(image)

        image0 = Image.fromarray(image_array.astype(np.uint8))
        image2 = Image.fromarray(self.last_drawing.astype(np.uint8))

        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                num_now = image_array[i, j]
                num_last = self.last_drawing[i, j]
                if num_now <= 127 and num_last <= 127:
                    image_array[i, j] = 255

        self.last_drawing = np.array(image)

        image1 = Image.fromarray(image_array.astype(np.uint8))


        image3 = Image.fromarray(self.last_drawing.astype(np.uint8))
        # 计算本次绘画的结果
        current_drawing = np.where(image_array <= 127, 255, 0)

        # 将 NumPy 数组转换回 PIL 图像对象
        image = Image.fromarray(current_drawing.astype(np.uint8))

        image = image.convert('RGB')  # 转为 RGB 模式
        image = image.resize((28, 28))  # 调整大小为 28x28 像素，以适应模型输入

        image.save("test.png")
        image0.save("test0.png")#画布内容
        image1.save("test1.png")#做差后本次绘制数字
        image2.save("test2.png")#上次
        image3.save("test3.png")

        image = np.array(image) / 255.0  # 像素值归一化
        self.main_window.predict_digit(image)  # 调用主窗口的预测函数
