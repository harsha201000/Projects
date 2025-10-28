# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

# window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Paint")

        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)
        
        # Set window icon
        self.setWindowIcon(QIcon('ms_paint_icon.jpg'))

        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # variables
        self.drawing = False
        self.brushSize = 2
        self.eraserSize = 10  # 🔹 default eraser size
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.eraserMode = False  # 🔹 new flag for eraser

        # creating menu bar
        mainMenu = self.menuBar()

        # creating menus
        fileMenu = mainMenu.addMenu("File")
        b_size = mainMenu.addMenu("Brush Size")
        b_color = mainMenu.addMenu("Brush Color")
        toolsMenu = mainMenu.addMenu("Tools")  # 🔹 New Tools menu
        e_size = mainMenu.addMenu("Eraser Size")  # 🔹 New Eraser Size menu

        # File menu actions
        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        # Brush sizes
        for size, func in [(4, self.Pixel_4), (7, self.Pixel_7), (9, self.Pixel_9), (12, self.Pixel_12)]:
            act = QAction(f"{size}px", self)
            b_size.addAction(act)
            act.triggered.connect(func)

        # Eraser sizes
        for size, func in [(4, self.Eraser_4), (7, self.Eraser_7), (9, self.Eraser_9), (12, self.Eraser_12)]:
            act = QAction(f"{size}px", self)
            e_size.addAction(act)
            act.triggered.connect(func)

        # Brush colors
        colors = {
            "Black": Qt.black, "White": Qt.white, "Green": Qt.green,
            "Yellow": Qt.yellow, "Red": Qt.red, "Orange": Qt.darkYellow,
            "Blue": Qt.blue, "Purple": Qt.magenta, "Pink": Qt.darkMagenta,
            "Grey": Qt.gray
        }
        for name, color in colors.items():
            act = QAction(name, self)
            b_color.addAction(act)
            act.triggered.connect(lambda _, c=color: self.changeColor(c))

        # 🔹 Eraser Tool
        eraserAction = QAction("Eraser", self)
        toolsMenu.addAction(eraserAction)
        eraserAction.triggered.connect(self.useEraser)

    # ========== MOUSE EVENTS ==========
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)

            # 🔹 If eraser is active, use white color and eraser size
            if self.eraserMode:
                color = Qt.white
                size = self.eraserSize
            else:
                color = self.brushColor
                size = self.brushSize

            painter.setPen(QPen(color, size,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # ========== FILE METHODS ==========
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        if filePath:
            self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    # ========== BRUSH SIZE METHODS ==========
    def Pixel_4(self): self.brushSize = 4
    def Pixel_7(self): self.brushSize = 7
    def Pixel_9(self): self.brushSize = 9
    def Pixel_12(self): self.brushSize = 12

    # ========== ERASER SIZE METHODS ==========
    def Eraser_4(self): self.eraserSize = 4
    def Eraser_7(self): self.eraserSize = 7
    def Eraser_9(self): self.eraserSize = 9
    def Eraser_12(self): self.eraserSize = 12

    # ========== COLOR + TOOL METHODS ==========
    def changeColor(self, new_color):
        self.brushColor = new_color
        self.eraserMode = False  # disable eraser when picking color

    def useEraser(self):
        self.eraserMode = True  # enable eraser

# create pyqt5 app
App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
