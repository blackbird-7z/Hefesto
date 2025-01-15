from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSvgWidgets import QSvgWidget


class ResultView(QWidget):
    save_files_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40)  # Margens (esquerda, topo, direita, fundo)
        spacer1 = QSpacerItem(20, 75, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # Margens (Horizontal, Vertical)

        self.svg_icon = QSvgWidget('assets/check.svg')
        self.svg_icon.setFixedSize(100, 100)

        self.info_label = QLabel("Os PDFs foram juntados com sucesso!")
        self.info_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        save_btn = QPushButton("Voltar")
        save_btn.setFixedSize(175, 37)
        save_btn.setStyleSheet("font-size: 14px;")
        save_btn.clicked.connect(self.save_files_requested.emit)
        
        layout.addSpacerItem(spacer1)
        layout.addWidget(self.svg_icon, 1, alignment=Qt.AlignmentFlag.AlignCenter) # Fator 1
        layout.addWidget(self.info_label, 0) # Fator 0
        layout.addSpacerItem(spacer1)
        layout.addWidget(save_btn, 1, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom) # Fator 1
        self.setLayout(layout)

 