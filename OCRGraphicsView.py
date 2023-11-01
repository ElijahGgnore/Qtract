import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPen, QCursor, QBrush
from PyQt5.QtWidgets import QGraphicsView, QFrame, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, \
    QGraphicsItem, QApplication
from pytesseract import pytesseract


class ImageNotFoundError(Exception):
    pass


class MissingImagePathError(Exception):
    pass


class WordRect(QGraphicsRectItem):
    def __init__(self, word, line_num, word_num, confidence, *args, **kwargs):
        """
        QGraphicsRectItem to store the information about the word detected at it's location
        """
        super().__init__(*args, **kwargs)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip(word)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # Set default pen
        rect_pen = QPen(Qt.red)
        rect_pen.setWidth(2)
        self.setPen(rect_pen)

        self.selected_color = QColor(255, 0, 0, 100)  # Default brush color that's to be set when the word is selected

        self.word = word
        self.confidence = confidence

        # Store the detected line and word numbers for text copying according to the OCR engine
        self.line_num = line_num
        self.word_num = word_num

    def itemChange(self, change, value):
        # TODO: find a way to overwrite the default dashed selection outline. Create custom rect by inheriting
        #  QGraphicsItem?

        #  Change brush color to the specified when the word is selected and back to transparent when unselected
        if change == QGraphicsItem.ItemSelectedChange:
            self.setBrush(QBrush(self.selected_color) if value else QBrush(Qt.transparent))
        return QGraphicsItem.itemChange(self, change, value)


class OCRGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEnabled(False)  # Disable by default and only enable when an image is specified
        self.setFrameShape(QFrame.NoFrame)
        self.setFixedSize(100, 100)

        # TODO: Make custom word selection instead of the default rubberband
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.current_image_path = None
        self.words = []

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # Select all words with A key and deselect all if alt is being held
        if event.key() == Qt.Key_A:
            select = False if event.modifiers() & Qt.AltModifier else True
            for r in self.words:
                r.setSelected(select)

        # The Ctrl + C copying behaviour
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                lines = {}
                for word in self.words:
                    if word.isSelected():
                        line = word.line_num
                        if line in lines:
                            lines[line].append(word)
                        else:
                            lines[line] = [word]
                if lines:
                    QApplication.clipboard().setText('\n'.join(
                        ' '.join(w.word for w in sorted(lines[i], key=lambda w: w.word_num)) for i in sorted(lines)))

    def set_new_image(self, image_path):
        """
        Resets the widget and sets a new image path
        """
        self.clear()
        self.setEnabled(True)
        self.current_image_path = image_path
        pixmap = QPixmap(image_path)
        pic = QGraphicsPixmapItem()
        pic.setPixmap(pixmap)
        x, y, w, h = pixmap.rect().getRect()
        self.scene.setSceneRect(x, y, w, h)
        self.setFixedSize(w, h)
        self.scene.addItem(pic)

    def clear(self):
        """
        Resets the state of the widget
        """
        self.setEnabled(False)
        self.scene.clear()
        self.words.clear()
        self.current_image_path = None

    def remove_word_rects(self):
        """
        Remove the last generated word rectangles, but keep the current image
        """
        for r in self.words:
            self.scene.removeItem(r)
        self.words.clear()

    def filter_words(self, min_confidence):
        """
        Enable only the words with confidence above or equal to the threshold
        """
        for w in self.words:
            w.setVisible(w.confidence >= min_confidence)

    def extract_text(self, min_confidence=90.0):
        """
        Attempt to extract text from the image at the current specified location and raise errors on failure
        """
        if self.current_image_path is None:
            raise MissingImagePathError
        if not os.path.isfile(self.current_image_path):
            self.clear()
            raise ImageNotFoundError

        self.remove_word_rects()
        # TODO: This requires pandas module. Implement with dictionaries to remove extra dependency
        detected_words = pytesseract.image_to_data(self.current_image_path, output_type=pytesseract.Output.DATAFRAME)
        detected_words = detected_words[detected_words['conf'] >= 0]

        for index, row in detected_words.iterrows():
            word, line_num, word_num, confidence, x, y, w, h = row['text'], row['line_num'], row['word_num'], \
                row['conf'], row['left'], row['top'], row['width'], row['height']

            rect = WordRect(word, line_num, word_num, confidence, x, y, w, h)
            self.words.append(rect)
            self.scene.addItem(rect)

        self.filter_words(min_confidence)
