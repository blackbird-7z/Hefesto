from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtSvgWidgets import QSvgWidget

class PreviewView(QWidget):
    join_files_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40)

        self.info_label = QLabel("Pré-visualização dos arquivos selecionados:")
        self.info_label.setStyleSheet("font-size: 18px;")

        self.files_list_widget = QListWidget()

        self.join_btn = QPushButton("Juntar Arquivos")
        self.join_btn.setFixedSize(200, 37)
        self.join_btn.setStyleSheet("font-size: 14px;")
        self.join_btn.clicked.connect(self.join_files_requested.emit)

        self.loading_svg = QSvgWidget('assets/loading.svg')
        self.loading_svg.setFixedSize(64, 64)
        self.loading_svg.setVisible(False)

        layout.addWidget(self.info_label)
        layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.files_list_widget)
        layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.loading_svg, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.join_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def set_files(self, file_list):
        self.files_list_widget.clear()
        self.files_list_widget.addItems(file_list)

    def show_loading(self):
        self.loading_svg.setVisible(True)

    def hide_loading(self):
        self.loading_svg.setVisible(False)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        file_paths = [u.toLocalFile() for u in urls]
        self.set_files(file_paths)
