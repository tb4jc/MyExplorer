import argparse
import os
import sys
from pathlib import Path
from tkinter import filedialog
import fsutils.functions
from helpers.base_ini_file import BaseIniFile

from PyQt5.uic import loadUiType
from PyQt5.QtCore import pyqtSlot, QStringListModel, QByteArray
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

MYEXPLORER_INI_FILE = 'myexplorer.ini'


def copy_files(src_dir, dst_dir, log_func, order_type='ext', use_filter=False, filter_list=None):
    log_func('-start')
    len_offset = len(src_dir.split(os.sep))
    pathIterator = fsutils.functions.scan_tree(src_dir)
    try:
        while True:
            item = next(pathIterator)
            if item is not None:
                rec_level = len(item.path.split(os.sep))
                if item.is_file(follow_symlinks=False):
                    ext = Path(item.name).suffix[1:]
                    if not use_filter or (filter_list is not None and ext in filter_list):
                        fsutils.functions.copy_entry(item, dst_dir, order_type, log_func)
                        log_func('f{0}: item "{1}" copied'.format(rec_level, item.name))
                    else:
                        log_func('f{0}: item "{1}" skipped'.format(rec_level, item.name))
                else:
                    log_func('d{0}: {1}'.format(rec_level, item.name))
    except StopIteration:
        pass
    pathIterator.close()
    log_func('-finish')


def calc_size(root_dir, log_func):
    dir_size = fsutils.functions.get_tree_size(root_dir, log_func)
    if dir_size > 1073741824:
        dir_size_out = '%2.3f TB' % (dir_size / 1073741824)
    elif dir_size > 1048576:
        dir_size_out = '%2.3f MB' % (dir_size / 1048576)
    elif dir_size > 1024:
        dir_size_out = '%2.3f kB' % (dir_size / 1024)
    else:
        dir_size_out = '%u bytes' % dir_size
    log_func('Total size of files in {0} is {1}\n'.format(root_dir, dir_size_out))


form_class, base_class = loadUiType('myexplorer.ui')


class MEIniFile(BaseIniFile):
    LAYOUT = 0
    PARAMS = 1
    SRC_DIRS = 2
    DST_DIRS = 3
    FILTERS = 4
    LAYOUT_ITEMS = ['geometry', 'PosX', 'PosY', 'Width', 'Height', 'state']
    PARAM_ITEMS = ['FilterOrdering', 'YearOrdering']
    CONFIG_DATA = {
        'section_names': {
            LAYOUT: 'GuiLayout',
            PARAMS: 'Parameters',
            SRC_DIRS: 'SourceDirectories',
            DST_DIRS: 'DestinationDirectories',
            FILTERS:  'Filters'

        },
        'section_metas': {
            LAYOUT: {BaseIniFile.KEY_TYPE: BaseIniFile.SECTION_TPYE_STRUCT, BaseIniFile.KEY_ITEMS: LAYOUT_ITEMS},
            PARAMS: {BaseIniFile.KEY_TYPE: BaseIniFile.SECTION_TPYE_STRUCT, BaseIniFile.KEY_ITEMS: PARAM_ITEMS},
            SRC_DIRS: {BaseIniFile.KEY_TYPE: BaseIniFile.SECTION_TYPE_SIMPLE, BaseIniFile.KEY_SIZE: 10},
            DST_DIRS: {BaseIniFile.KEY_TYPE: BaseIniFile.SECTION_TYPE_SIMPLE, BaseIniFile.KEY_SIZE: 10},
            FILTERS: {BaseIniFile.KEY_TYPE: BaseIniFile.SECTION_TYPE_SIMPLE, BaseIniFile.KEY_SIZE: 50},
        }
    }

    def __init__(self, file_name):
        super().__init__(file_name, MEIniFile.CONFIG_DATA)


class MEMainWindowImpl(QMainWindow, form_class):
    BASE_EXT_FILTERS = ['doc', 'docx', 'xls', 'xlsx', 'zip']

    def __init__(self, *args):
        super(MEMainWindowImpl, self).__init__(*args)
        self.config = MEIniFile(MYEXPLORER_INI_FILE)
        self.setupUi(self)
        self.src_dirs = QStringListModel(self.config.get_section_values(MEIniFile.SRC_DIRS))
        self.cbSrcDir.setModel(self.src_dirs)
        self.dst_dirs = QStringListModel(self.config.get_section_values(MEIniFile.DST_DIRS))
        self.cbDstDir.setModel(self.dst_dirs)
        tmp_filters = self.config.get_section_values(MEIniFile.FILTERS)
        if len(tmp_filters) == 0:
            tmp_filters = MEMainWindowImpl.BASE_EXT_FILTERS
        self.filters = QStringListModel(tmp_filters)
        self.cbFilterList.setModel(self.filters)
        params = self.config.get_full_section(MEIniFile.PARAMS)
        if type(params) is dict:
            if 'FilterOrdering' in params:
                self.cbFilterOrdering.setChecked(params.get('FilterOrdering') == "True")
            else:
                self.cbFilterOrdering.checked = False
            if 'YearOrdering' in params:
                self.cbYearOrdering.setChecked(params.get('YearOrdering') == "True")
            else:
                self.cbYearOrdering.checked = False
        layout = self.config.get_full_section(MEIniFile.LAYOUT)
        if type(layout) is dict:
            if 'geometry'in layout:
                byte_array = bytes(layout['geometry'], 'utf-8')
                self.restoreGeometry(QByteArray.fromBase64(byte_array))
            elif 'PosX' in layout:
                self.move(layout['PosX'], layout['PosY'])
                self.resize(layout['Width'], layout['Height'])
            if 'state' in layout:
                byte_array = bytes(layout['state'], 'utf-8')
                self.restoreState(QByteArray.fromBase64(byte_array))
        pass

    def log_msg(self, msg):
        self.teLog.append(msg)

    def update_dir_combox(self, id, path, combox, model):
        try:
            idx = model.stringList().index(path)
            combox.setCurrentIndex(idx)
        except ValueError:
            combox.insertItem(0, path)  # adds it automatically to the list model too
            combox.setCurrentIndex(0)
        # fetch stringList again as it was updated in the model through the insert above
        self.config.update_section(id, model.stringList())

    @pyqtSlot()
    def on_app_about_to_quit(self):
        pos = self.pos()
        layout = dict()
        layout['PosX'] = str(pos.x())
        layout['PosY'] = str(pos.y())
        size = self.size()
        layout['Height'] = str(size.height())
        layout['Width'] = str(size.width())
        geometry = str(self.saveGeometry().toBase64())
        layout['geometry'] = bytes(self.saveGeometry().toBase64()).decode()
        layout['state'] = bytes(self.saveState().toBase64()).decode()
        self.config.update_section(MEIniFile.LAYOUT, layout)
        self.config.update_section(MEIniFile.SRC_DIRS, self.src_dirs.stringList())
        self.config.update_section(MEIniFile.FILTERS, self.filters.stringList())
        params = {'FilterOrdering': str(self.cbFilterOrdering.isChecked()), 'YearOrdering': str(self.cbYearOrdering.isChecked())}
        self.config.update_section(MEIniFile.PARAMS, params)
        self.config.save_config()
        return True

    @pyqtSlot(bool)
    def on_srcDirSel_clicked(self, checked):
        dialog_options = QFileDialog.Options()
        dialog_options |= QFileDialog.ShowDirsOnly
        dialog_options |= QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Source Directory", 'c:', options=dialog_options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(MEIniFile.SRC_DIRS, str(Path(selected_dir)), self.cbSrcDir, self.src_dirs)
        pass

    @pyqtSlot(bool)
    def on_dstDirSel_clicked(self, checked):
        dialog_options = QFileDialog.Options()
        dialog_options |= QFileDialog.ShowDirsOnly
        dialog_options |= QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Destination Directory", 'c:', options=dialog_options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(MEIniFile.DST_DIRS, str(Path(selected_dir)), self.cbDstDir, self.dst_dirs)
        pass

    @pyqtSlot(bool)
    def on_pbCopyFiles_clicked(self, checked):
        self.log_msg("copy files pressed")
        src_dir = self.cbSrcDir.currentText()
        dst_dir = self.cbDstDir.currentText()
        if self.cbYearOrdering.isChecked():
            o_type = 'year'
        else:
            o_type = 'ext'
        # log_list = []
        filters = self.filters
        copy_files(src_dir, dst_dir, self.log_msg, order_type=o_type, use_filter=self.cbFilterOrdering.isChecked(), filter_list=filters.stringList())
        # for entry in log_list:
        #    self.teLog.append(entry)

    @pyqtSlot(bool)
    def on_pbCalcSize_clicked(self, checked):
        self.teLog.append("calc size pressed")
        src_dir = self.cbSrcDir.currentText()
        # log_list = []
        calc_size(src_dir, self.log_msg)
        # for entry in log_list:
        #    self.teLog.append(entry)

    @pyqtSlot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses a given directory and its subdirectories and copies the files ordered to \
                                                  the given destination path')
    parser.add_argument('-c', '--copy-files', action='store_true', dest='copy_files',
                        help='Test case number, selects the way to parse the source_path')
    parser.add_argument('-s', '--source', action='store', dest='source_path',
                        help='Identifies the source path')
    parser.add_argument('-d', '--destination', action='store', dest='dest_path',
                        help='Identifies the destination path')
    parser.add_argument('-f', '--useextfilter', action='store_true', dest='use_filter',
                        help='Activate filter usage')
    parser.add_argument('-g', '--gui', action='store_true', dest='use_gui',
                        help='Use GUI mode')

    args = parser.parse_args()

    ext_filter = ['doc', 'docx', 'xls', 'xlsx', 'zip']
    if args.source_path:
        source_path = args.source_path
    else:
        source_path = 'C:\\Users\\Thomas\\Documents'

    if args.dest_path:
        dest_path = args.dest_path
    else:
        dest_path = 'C:\\Daten\\_TestDir'

    if args.use_gui:
        myexp = QApplication(sys.argv)
        form = MEMainWindowImpl()
        myexp.aboutToQuit.connect(form.on_app_about_to_quit)
        # myexp.focusChanged.connect(form.on_app_focus_changed)
        form.show()
        sys.exit(myexp.exec_())
    else:
        if args.source_path is None:
            root_dir = filedialog.askdirectory(initialdir='C:\\', title='Choose a directory to copy from')
            if root_dir is not None:
                print('root_dir = %s' % str(root_dir))
                root_dir = str(Path(root_dir).absolute())
                print('root_dir = %s' % root_dir)
        else:
            root_dir = args.source_path
        # root_dir = 'c:\\tmp' if args.source_path is None else args.source_path
        # root_dir = 'c:\\Daten\\Audio\\20-Tobias-Collection'

        if args.dest_path is None:
            dest_dir = filedialog.askdirectory(initialdir='C:\\', title='Choose a directory to copy to')
            if dest_dir is not None:
                print('dest_dir = %s' % str(dest_dir))
        else:
            dest_dir = args.dest_path
        if args.copy_files:
            copy_files(root_dir, dest_dir)
        else:
            calc_size(root_dir)
