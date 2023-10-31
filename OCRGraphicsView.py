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
    def __init__(self, word, line_num, word_num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.IBeamCursor))
        self.setToolTip(word)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.word_rect_pen = QPen(QColor(255, 0, 0))
        self.word_rect_pen.setWidth(2)
        self.setPen(self.word_rect_pen)
        self.selected_color = QColor(255, 0, 0, 100)
        self.word = word
        # store the detected line and word numbers for easier text copying
        self.line_num = line_num
        self.word_num = word_num

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.setBrush(QBrush(self.selected_color) if value else QBrush(Qt.transparent))
        return QGraphicsItem.itemChange(self, change, value)


class OCRGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEnabled(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFixedSize(100, 100)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.current_image_path = None
        self.words = []

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_A:
            select = False if event.modifiers() & Qt.AltModifier else True
            for r in self.words:
                r.setSelected(select)
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

    def set_image(self, image_path):
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
        self.setEnabled(False)
        self.scene.clear()
        self.words.clear()

    def remove_word_rects(self):
        for r in self.words:
            self.scene.removeItem(r)
        self.words.clear()

    def extract_text(self, min_confidence=90.0):
        if self.current_image_path is None:
            raise MissingImagePathError
        if not os.path.isfile(self.current_image_path):
            self.clear()
            raise ImageNotFoundError
        self.remove_word_rects()
        detected_words = pytesseract.image_to_data(self.current_image_path, output_type=pytesseract.Output.DATAFRAME)
        detected_words = detected_words[detected_words['conf'] >= min_confidence]
        for index, row in detected_words.iterrows():
            word, line_num, word_num, x, y, w, h = row['text'], row['line_num'], row['word_num'], row['left'], \
                row['top'], row['width'], row['height']
            rect = WordRect(word, line_num, word_num, x, y, w, h)

            self.words.append(rect)
            self.scene.addItem(rect)
