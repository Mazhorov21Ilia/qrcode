import sys
import os
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog
import qrcode
from PIL.ImageQt import ImageQt
from design import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.generate_qrcode)
        self.ui.pushButton_2.clicked.connect(self.save_qrcode_to_file)

    def generate_qrcode(self):
        text = self.ui.textEdit.toPlainText()
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            qimage = ImageQt(img).convertToFormat(
                QtGui.QImage.Format.Format_RGB32)
            self.pixmap = QtGui.QPixmap.fromImage(qimage)

            self.ui.label.setPixmap(self.pixmap.scaled(
                self.ui.label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def save_qrcode_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить QR-код", ".", "PNG Files (*.png)")

        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'

            self.pixmap.save(file_path)

        self.ui.textEdit.clear()
        # self.ui.label.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


main()
