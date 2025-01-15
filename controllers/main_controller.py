from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import pyqtSlot, QThread, QObject, pyqtSignal

from views.initial_view import InitialView
from views.preview_view import PreviewView
from views.result_view import ResultView
from models.file_manager import FileManager

class FileManagerWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, file_manager):
        super().__init__()
        self.file_manager = file_manager

    @pyqtSlot()
    def run(self):
        try:
            self.file_manager.join_files_by_format()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hefesto")
        self.setMinimumSize(800, 600)

        self.file_manager = FileManager()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.initial_view = InitialView()
        self.preview_view = PreviewView()
        self.result_view = ResultView()

        self.stacked_widget.addWidget(self.initial_view)
        self.stacked_widget.addWidget(self.preview_view)
        self.stacked_widget.addWidget(self.result_view)
    
        self.initial_view.files_selected.connect(self.on_files_selected)
        self.preview_view.join_files_requested.connect(self.on_join_files_requested)
        self.result_view.save_files_requested.connect(self.on_save_files_requested)

        self.thread = None
        self.worker = None
        
    @pyqtSlot(dict)
    def on_files_selected(self, data):
        abs_files = data["absolute"]
        rel_files = data["relative"]
        self.file_manager.set_files(abs_files)
        self.preview_view.set_files(rel_files)
        self.stacked_widget.setCurrentWidget(self.preview_view)

    @pyqtSlot()
    def on_join_files_requested(self):
        self.preview_view.show_loading()
        # Desativa o botão para evitar cliques duplicados
        self.preview_view.join_btn.setEnabled(False)

        self.worker = FileManagerWorker(self.file_manager)
        self.thread = QThread()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self.on_join_files_finished)
        self.worker.error.connect(self.on_join_files_error)

        self.thread.start()

    def on_join_files_finished(self):
        self.preview_view.hide_loading()
        # Reativa o botão após a conclusão
        self.preview_view.join_btn.setEnabled(True)
        self.stacked_widget.setCurrentWidget(self.result_view)

    def on_join_files_error(self, error_msg):
        self.preview_view.hide_loading()
        # Reativa o botão mesmo em caso de erro
        self.preview_view.join_btn.setEnabled(True)
        self.stacked_widget.setCurrentWidget(self.result_view)

    @pyqtSlot()
    def on_save_files_requested(self):
        self.stacked_widget.setCurrentWidget(self.initial_view)
