from PyQt5.QtWidgets import QMainWindow, QFileDialog

from Ui_QtractWindow import Ui_QtractWindow
from OCRGraphicsView import ImageNotFoundError, MissingImagePathError


class QtractWindow(QMainWindow, Ui_QtractWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.select_image_location.pressed.connect(self.new_image_dialog)
        self.extract_text.pressed.connect(self.extract_current_image_text)

    def new_image_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open file", ".", "Image Files (*.png *.jpg *.bmp)"
        )
        if not file_name:
            return
        self.load_new_image(file_name)

    def load_new_image(self, file_name):
        self.ocr_image.set_image(file_name)

    def extract_current_image_text(self):
        self.statusbar.clearMessage()
        try:
            self.ocr_image.extract_text(min_confidence=self.minimal_confidence.value())
        except ImageNotFoundError:
            self.statusbar.showMessage('No image was found at the specified location')
        except MissingImagePathError:
            self.statusbar.showMessage('Select an image location first')
