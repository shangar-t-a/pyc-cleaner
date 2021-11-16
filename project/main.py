import sys
import os
import traceback
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

from cache_manager import CacheRemover


class MainWindow(QDialog):
    """Main window for py-cache-cleaner(pcc)"""

    def __init__(self):
        """Constructor for pcc"""

        super(MainWindow,self).__init__()

        self.cache_cleaner = CacheRemover()

        loadUi('gui.ui', self)

        self._enable_disable_widgets()
        self._bind_widgets_functions()

    def _enable_disable_widgets(self):
        """Initialize Enable or Disable widgets"""

        self.filename_back.setEnabled(False)
        self.browse_back.setEnabled(False)

    def _bind_widgets_functions(self):
        """Bind all the widgets to the corresponding methods"""

        self.browse_root.clicked.connect(self._browsefiles)
        self.collect_cache.clicked.connect(self._collect_cache)
        self.backup.stateChanged.connect(self._enablebackup)
        self.clear_cache.clicked.connect(self._removecache)

    def _browsefiles(self):
        """Bind browse_root button to Folder browser"""

        fname = str(QFileDialog.getExistingDirectory(self, 'Open folder', 'C:'))
        self.filename_root.setText(fname)
        self.cache_display.setText('')
        self.cache_count.setText('')
        self.output_message.setText('')

    def _collect_cache(self):
        """Collect all files of the selectd directory"""

        selected_folder = self.filename_root.text()
        self.cache_cleaner._reinitialize_data()
        self.cache_display.setText('')
        self.cache_count.setText('')
        self.output_message.setText('')
        if os.path.isdir(selected_folder):
            self.cache_cleaner.collect_cache_files(root_dir=selected_folder)
            if self.cache_cleaner.cache_files:
                self.cache_count.setText(str(len(self.cache_cleaner.cache_files)))
                self.cache_display.setText('\n'.join(self.cache_cleaner.cache_files))
            else:
                self.cache_count.setText('0')
                self.cache_display.setText('No Cache found...')
        else:
            self.cache_display.setText('Please select a valid directory...')

    def _removecache(self) -> None:
        """Remove all available cache files"""

        if self.cache_cleaner.cache_files:
            try:
                self.cache_cleaner.removecache()
            except:
                self.output_message.setText(traceback.format_exc())
            else:
                self.cache_display.setText('')
                self.cache_count.setText('')
                self.output_message.setText('Successfully removed all cache files...')
        else:
            self.output_message.setText('No Cache to remove...')

    def _enablebackup(self, checked):
        """Enable widgets tp backup cache files"""

        if checked:
            self.filename_back.setEnabled(True)
            self.browse_back.setEnabled(True)
        else:
            self.filename_back.setEnabled(False)
            self.browse_back.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(500)
    widget.setFixedHeight(600)
    widget.show()
    sys.exit(app.exec_())