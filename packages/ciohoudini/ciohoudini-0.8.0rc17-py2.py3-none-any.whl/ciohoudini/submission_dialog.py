import hou
from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui

from ciohoudini.selection_tab import SelectionTab
from ciohoudini.validation_tab import ValidationTab
from ciohoudini.progress_tab import ProgressTab
from ciohoudini.response_tab import ResponseTab
from ciohoudini import validation, utils
import time

import ciocore.loggeria

logger = ciocore.loggeria.get_conductor_logger()


class SubmissionDialog(QtWidgets.QDialog):

    def __init__(self, nodes, parent=None):
        super(SubmissionDialog, self).__init__(parent)
        # super(SubmissionDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Conductor Submission")
        self.setStyleSheet(hou.qt.styleSheet())
        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)

        self.node = nodes[0] if nodes else None
        # logger.debug("SubmissionDialog: Node name: ", self.node.name())
        # logger.debug("SubmissionDialog: Node type: ", self.node.type().name())

        self.payloads = []

        self.selection_tab = SelectionTab(self)
        self.tab_widget.addTab(self.selection_tab, "Selection")
        self.selection_tab.hide()
        self.set_selection_tab(self.node)

        self.validation_tab = ValidationTab(self)
        self.tab_widget.addTab(self.validation_tab, "Validation")

        self.progress_tab = ProgressTab(self)
        self.tab_widget.addTab(self.progress_tab, "Progress")

        self.response_tab = ResponseTab(self)
        self.tab_widget.addTab(self.response_tab, "Response")

        self.setMinimumSize(1200, 742)  # Set minimum window size

        #self.tab_widget.setTabEnabled(1, False)
        #self.tab_widget.setTabEnabled(2, False)

        self.nodes = nodes
 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.run(self.node)

    def use_stage_cameras(self, node):
        return utils.get_parameter_value(node, "use_multiple_cameras")


    def set_selection_tab(self, node):
        multiple_cameras = self.use_stage_cameras(node)
        if multiple_cameras:
            self.selection_tab.show()

    def show_selection_tab(self):
        self.tab_widget.setTabEnabled(0, True)
        self.tab_widget.setCurrentWidget(self.selection_tab)
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        QtCore.QCoreApplication.processEvents()

    def show_validation_tab(self):
        self.tab_widget.setTabEnabled(0, False)
        self.tab_widget.setTabEnabled(1, True)
        self.tab_widget.setCurrentWidget(self.validation_tab)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        QtCore.QCoreApplication.processEvents()


    def show_progress_tab(self):
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setCurrentWidget(self.progress_tab)
        self.tab_widget.setTabEnabled(0, False)
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(3, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def show_response_tab(self):
        self.tab_widget.setTabEnabled(3, True)
        self.tab_widget.setCurrentWidget(self.response_tab)
        self.tab_widget.setTabEnabled(0, False)
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def run(self, node):
        # Single Camera
        if not self.use_stage_cameras(node):
            logger.debug("Single Camera, running validation...")
            self.show_validation_tab()
            errors, warnings, notices = validation.run(self.node)
            self.validation_tab.populate(errors, warnings, notices)
        # Use Multiple Stage Cameras
        else:
            logger.debug("Multiple Stage Cameras, running Selection tab...")
            self.show_selection_tab()
            self.selection_tab.list_stage_cameras(node)


    def on_close(self):
        self.accept()


