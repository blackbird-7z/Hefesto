import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QFrame,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal

class InitialView(QWidget):
    files_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40)
        spacer1 = QSpacerItem(20, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        title_label = QLabel("Juntar PDFs")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_label = QLabel("... ou solte os arquivos aqui")
        drop_label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        select_folder_btn = QPushButton("Escolher Pasta")
        select_folder_btn.setFixedSize(200, 37)
        select_folder_btn.setStyleSheet("font-size: 14px;")
        select_folder_btn.clicked.connect(self.select_folder_dialog)

        layout.addWidget(title_label, 0)
        layout.addSpacerItem(spacer1)
        layout.addWidget(drop_label, 1)
        layout.addSpacerItem(spacer1)
        layout.addWidget(select_folder_btn, 0, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

        self.setAcceptDrops(True)

    def select_folder_dialog(self):
        """
        Essa função abre o QFileDialog para selecionar uma PASTA.
        Em seguida, busca todos os PDFs dentro da pasta selecionada (recursivamente).
        Converte para caminhos relativos e absolutos.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Selecione a Pasta")
        if folder_path:
            pdf_files_abs = self._get_all_pdfs_in_folder(folder_path)
            if pdf_files_abs:
                # Gera caminhos relativos
                pdf_files_rel = [os.path.relpath(p, start=folder_path) for p in pdf_files_abs]

                # Emite ambos num dicionário
                data = {
                    "absolute": pdf_files_abs,
                    "relative": pdf_files_rel
                }
                self.files_selected.emit(data)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        all_pdf_files_abs = []
        folder_path = None

        # Caso arraste apenas uma pasta
        if len(urls) == 1:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                folder_path = path

        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                pdfs_in_dir = self._get_all_pdfs_in_folder(path)
                all_pdf_files_abs.extend(pdfs_in_dir)
            else:
                if path.lower().endswith(".pdf"):
                    all_pdf_files_abs.append(path)

        if all_pdf_files_abs:
            if folder_path:
                # Se foi uma pasta única
                pdf_files_rel = [os.path.relpath(p, start=folder_path) for p in all_pdf_files_abs]
            else:
                # Arrastou vários itens (ou várias pastas)
                pdf_files_rel = all_pdf_files_abs

            data = {
                "absolute": all_pdf_files_abs,
                "relative": pdf_files_rel
            }
            self.files_selected.emit(data)

    def _get_all_pdfs_in_folder(self, folder_path: str) -> list:
        # Retorna lista de caminhos ABSOLUTOS dos PDFs.
        pdf_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(root, file)
                    pdf_files.append(full_path)
        return pdf_files
