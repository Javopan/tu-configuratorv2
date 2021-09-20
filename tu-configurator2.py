from PyQt5 import QtCore as Qtc
from PyQt5 import QtGui as Qtg
from PyQt5 import QtWidgets as Qtw
from tu_widget import TuConfig


if __name__ == '__main__':
    import sys

    class MainWindow(Qtw.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            # -------------------- widget creation
            self.setWindowTitle('TU-Configurator V1.0.2')
            self.widget = TuConfig(self)
            self.setStyle(Qtw.QStyleFactory.create('Fusion'))
            print(self.style())
            # -------------------- widget layout
            self.setCentralWidget(self.widget)
            self.statusBar().setVisible(True)
            # -------------------- widget connections and actions
            # self.monitor.status_message.connect(self.status_display)
            self.widget.tu.tu_errors.connect(self.statusBar().showMessage)
            self.widget.tu.tu_logs.connect(self.statusBar().showMessage)
            self.widget.tu.tu_logs.connect(self.log)
            self.widget.tu.tu_errors.connect(self.log_error)
            self.widget.tuwidget_changing.connect(self.log_clear)
            self.widget.tuwidget_changing.connect(self.status_clear)
            self.widget.monitored_tu.tu_monitor_log.connect(self.log)
            self.widget.tu_widget_log.connect(self.log_error)

            # Change the size of the form to match the content
            self.setMinimumWidth(938)
            self.setMinimumHeight(520)
            # self.setMaximumSize(666, 330)
            # -------------------- Window Icon
            windows_icon = Qtg.QIcon('Logo-Icon.png')
            self.setWindowIcon(windows_icon)

            ############################
            #
            #     Dock widgets
            #
            ############################
            # open dock widget to open files with drag and drop
            dock_logs = Qtw.QDockWidget('Logs')
            self.addDockWidget(Qtc.Qt.LeftDockWidgetArea, dock_logs)
            # we set the features in this case it can't be closed
            dock_logs.setFeatures(  # this gets a features list separated by |
                Qtw.QDockWidget.DockWidgetMovable |
                Qtw.QDockWidget.DockWidgetFloatable)
            # sizing policy for minimum space
            dock_logs.setSizePolicy(Qtw.QSizePolicy(Qtw.QSizePolicy.Minimum, Qtw.QSizePolicy.Minimum))
            # we set the open widget into the dock
            self.log_list = Qtw.QListWidget(self)

            dock_logs.setWidget(self.log_list)

            self.show()

            # shortcut
            shortcut_unhide = Qtw.QShortcut(Qtg.QKeySequence('Ctrl+Shift+U'), self)
            shortcut_unhide.activated.connect(self.unhide_hidden)

            shortcut_hide = Qtw.QShortcut(Qtg.QKeySequence('Ctrl+Shift+H'), self)
            shortcut_hide.activated.connect(self.hide_hidden)

            shortcut_advanced = Qtw.QShortcut(Qtg.QKeySequence('Ctrl+Shift+A'), self)
            shortcut_advanced.activated.connect(self.enable_advances)

        @Qtc.pyqtSlot(str)
        def log(self, message_):
            item = Qtw.QListWidgetItem(message_)
            self.log_list.addItem(item)

        @Qtc.pyqtSlot(str)
        def log_error(self, message_):
            item = Qtw.QListWidgetItem(message_)
            self.log_list.addItem(item)

        @Qtc.pyqtSlot()
        def log_clear(self):
            self.log_list.clear()

        @Qtc.pyqtSlot(str)
        def status_display(self, message_=None):
            self.statusBar().showMessage(f'{message_}', 2000)

        @Qtc.pyqtSlot()
        def status_clear(self):
            self.statusBar().showMessage('')

        def unhide_hidden(self):
            if self.widget.grp_hidden.isHidden():
                self.widget.grp_hidden.setHidden(False)
                self.widget.txt_ip_hidden.setDisabled(False)
                self.widget.txt_user_hidden.setDisabled(False)
                self.widget.txt_pass_hidden.setDisabled(False)

        def hide_hidden(self):
            if not self.widget.grp_hidden.isHidden():
                self.widget.grp_hidden.setHidden(True)
                self.widget.txt_ip_hidden.setDisabled(True)
                self.widget.txt_user_hidden.setDisabled(True)
                self.widget.txt_pass_hidden.setDisabled(True)

        def enable_advances(self):
            self.widget.pg_advanced_config.setDisabled(self.widget.pg_advanced_config.isEnabled())

    def main():
        app = Qtw.QApplication(sys.argv)
        app.setOrganizationName('Javopan Awesome Systems')
        app.setOrganizationDomain('javoisawesome.com')
        app.setApplicationName('TU-Configuration')
        app.setStyle(Qtw.QStyleFactory.create('Fusion'))
        # app.setStyleSheet(open('Styles.css', 'r', encoding='utf-8').read())
        mw = MainWindow()
        sys.exit(app.exec())

    main()