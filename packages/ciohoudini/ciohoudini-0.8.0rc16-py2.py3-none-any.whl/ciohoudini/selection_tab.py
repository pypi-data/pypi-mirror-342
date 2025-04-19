from PySide2 import QtWidgets, QtCore
from ciohoudini.buttoned_scroll_panel import ButtonedScrollPanel
from ciohoudini import utils, validation, payload, render_rops, cameras

import ciocore.loggeria
import hou
import os
import re
from pathlib import Path

logger = ciocore.loggeria.get_conductor_logger()

class SelectionTab(ButtonedScrollPanel):
    def __init__(self, dialog):
        super(SelectionTab, self).__init__(
            dialog,
            buttons=[("close", "Close"), ("continue", "Continue Submission")]
        )
        self.dialog = dialog
        self.node = self.dialog.node
        self.all_checkboxes = []  # Keep track of all node checkboxes
        self.node_map = {}  # Map checkboxes to their corresponding nodes
        self.camera_rop_dict = {}
        self.rop_checkboxes = []  # Keep track of all rop checkboxes
        self.configure_signals()

        # Add "Select all nodes" and "Deselect all nodes" buttons at the top
        self.add_global_buttons()

    def configure_signals(self):
        """Connect button signals to their respective handlers."""
        self.buttons["close"].clicked.connect(self.dialog.on_close)
        self.buttons["continue"].clicked.connect(self.on_continue)

    def add_global_buttons(self):
        """Add global buttons for selecting and deselecting all nodes."""
        button_layout = QtWidgets.QHBoxLayout()
        select_all_button = QtWidgets.QPushButton("Select all nodes")
        deselect_all_button = QtWidgets.QPushButton("Deselect all nodes")

        # Connect the buttons to their respective slots
        select_all_button.clicked.connect(self.select_all_nodes)
        deselect_all_button.clicked.connect(self.deselect_all_nodes)

        # Add buttons to the layout
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(deselect_all_button)
        self.layout.addLayout(button_layout)

    def list_stage_cameras(self, node):
        """
        Lists the name of each rop connected to the generator node and adds checkboxes for nodes in the rops.
        """
        logger.debug("Selection tab: Listing rop nodes...")

        if not node:
            logger.debug("Selection tab: No node provided.")
            return

        # Clear existing content in the layout to prepare for new content
        self.clear()
        self.all_checkboxes = []  # Reset the list of all node checkboxes
        self.node_map = {}  # Reset the node map
        self.camera_rop_dict = {}
        self.rop_checkboxes = []  # Reset the list of rop checkboxes


        # Add the global buttons again at the top
        self.add_global_buttons()

        render_rops_data = render_rops.get_render_rop_data(node)
        for render_rop in render_rops_data:
            rop_path = render_rop.get("path", None)
            camera_list = cameras.find_stage_cameras(rop_path)

            # Create a horizontal layout for the rop title and checkbox
            rop_row_layout = QtWidgets.QHBoxLayout()

            # Create a checkbox for the rop
            rop_checkbox = QtWidgets.QCheckBox()
            rop_checkbox.setToolTip(f"Toggle all cameras in rop: {rop_path}")
            rop_row_layout.addWidget(rop_checkbox)
            self.rop_checkboxes.append(rop_checkbox)  # Track rop checkbox globally

            # Create a label for the rop name and style it
            rop_name_label = QtWidgets.QLabel(f"Rop: {rop_path}")
            rop_name_label.setStyleSheet("font-weight: bold;")  # Make the text bold
            rop_row_layout.addWidget(rop_name_label)

            # Align rop name to the left
            rop_row_layout.setAlignment(QtCore.Qt.AlignLeft)

            # Add the rop row layout to the main layout
            self.layout.addLayout(rop_row_layout)

            # Create a vertical layout to group checkboxes for nodes within the rop
            node_container_layout = QtWidgets.QVBoxLayout()
            node_container_layout.setContentsMargins(40, 0, 0, 0)  # Indent for better grouping
            self.layout.addLayout(node_container_layout)

            # Add checkboxes for each node in the rop
            node_checkboxes = []
            for camera_path in camera_list:
                self.camera_rop_dict[camera_path] = render_rop  # Map camera path to its render_rop
                # logger.debug(f"Adding checkbox for node: {child_node.name()}")
                checkbox = QtWidgets.QCheckBox(camera_path)
                node_container_layout.addWidget(checkbox)
                node_checkboxes.append(checkbox)
                self.all_checkboxes.append(checkbox)  # Track globally
                self.node_map[checkbox] = camera_path  # Map checkbox to its node

            # Connect the rop checkbox to toggle all child node checkboxes
            rop_checkbox.stateChanged.connect(
                lambda state, checkboxes=node_checkboxes: self.toggle_rop_nodes(state, checkboxes)
            )
        # print(self.node_map.items())
        # Add a stretch to align content to the top
        self.layout.addStretch()

    def toggle_rop_nodes(self, state, checkboxes):
        """
        Toggles the state of all node checkboxes under a rop.

        Args:
            state (int): The state of the rop checkbox (0: unchecked, 2: checked).
            checkboxes (list): List of node checkboxes under the rop.
        """
        is_checked = state == QtCore.Qt.Checked
        for checkbox in checkboxes:
            checkbox.setChecked(is_checked)

    def select_all_nodes(self):
        """Sets all node and rop checkboxes to checked."""
        logger.debug("Selecting all nodes...")
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(True)
        for rop_checkbox in self.rop_checkboxes:
            rop_checkbox.setChecked(True)

    def deselect_all_nodes(self):
        """Sets all node and rop checkboxes to unchecked."""
        logger.debug("Deselecting all nodes...")
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(False)
        for rop_checkbox in self.rop_checkboxes:
            rop_checkbox.setChecked(False)
    def get_payloads(self):
        """
        Generates payloads for all checked nodes.

        Returns:
            list: A list of payloads for all checked nodes.
        """
        logger.debug("Generating payloads for all checked nodes...")
        payload_list = []
        kwargs = {}  # Add any additional arguments needed for payload generation

        for checkbox, camera_path in self.node_map.items():
            if checkbox.isChecked():  # Process only checked nodes
                render_rop = self.camera_rop_dict.get(camera_path)
                if not render_rop:
                    # logger.warning(f"Could not find render_rop mapping for camera {camera_path}. Skipping payload.")
                    continue

                rop_path = render_rop.get("path", None)
                if not rop_path:
                    # logger.warning(f"Render ROP data for camera {camera_path} is missing 'path'. Skipping payload.")
                    continue

                #logger.debug(f"Generating payload for camera: {camera_path} and rop: {rop_path}")
                kwargs["override_camera"] = camera_path

                # rop_name may be used later if we have multiple ROP names
                # rop_name = os.path.basename(rop_path)
                # kwargs["rop_name"] = rop_name

                camera_name = os.path.basename(camera_path)
                camera_number = self.get_camera_number(camera_name)
                kwargs["camera_number"] = camera_number

                subject_name = utils.get_parameter_value(self.node, "subject_name")
                subject_name = subject_name.replace(" ", "_")
                kwargs["subject_name"] = subject_name

                version_number = utils.get_parameter_value(self.node, "version_number")
                version_number = f"v{int(version_number):02d}"
                kwargs["version_number"] = version_number

                # Get the hip folder (directory containing the .hip file)
                output_folder = None
                hip_folder = hou.getenv("HIP")
                if hip_folder:
                    hip_folder = os.path.abspath(hip_folder)  # Ensure it's an absolute path
                    # Construct the output folder path using os.path.join for cross-platform compatibility
                    # This ensures the correct separators ('/' or '\') are used.
                    output_folder = os.path.join(hip_folder, "render", subject_name)

                if not hip_folder:
                    # Get the 'output_folder' parameter from self.node if HIP is not set
                    ren_folder = self.node.parm("output_folder").eval()
                    output_folder = os.path.join(ren_folder, subject_name)

                if output_folder:
                    # Normalize and convert to absolute path
                    output_folder = os.path.abspath(output_folder)
                    output_folder = os.path.normpath(output_folder)

                    # Ensure consistent cross-platform formatting for payloads (use forward slashes)
                    output_folder = Path(output_folder).as_posix()

                    kwargs["camera_output_folder"] = output_folder
                    kwargs["camera_output_path"] = output_folder

                kwargs["task_limit"] = -1 # Ensure all tasks are generated for the payload
                # print("kwargs: ", kwargs)
                try:
                    # Assuming get_payload handles the kwargs correctly
                    node_payload = payload.get_payload(self.node, render_rop, **kwargs)
                    if node_payload:
                        payload_list.append(node_payload)
                except Exception as e:
                    logger.error(f"Error generating payload for node {self.node.name()} with ROP {rop_path} and Camera {camera_path}: {e}", exc_info=True) # Add exc_info for traceback

        return payload_list

    def get_camera_number(self, camera_name):
        """
        Extracts the camera number from the camera name.
        For example, if the camera name is "Instance11", extract 11
        then add 1 -> 12
        Then make it padding of 5 -> 00012

        Args:
            camera_name (str): The name of the camera (e.g., "Instance11", "/path/to/cam_05").

        Returns:
            str or None: The formatted camera number string (e.g., "00012") or None if extraction fails.
        """
        if not camera_name:
            logger.warning("get_camera_number received an empty camera name.")
            return None

        # Use regex to find one or more digits at the very end of the string
        match = re.search(r'\d+$', camera_name)

        if match:
            try:
                # Extract the digits found
                number_str = match.group(0)
                # Convert to integer
                number_int = int(number_str)
                # Add 1
                number_int += 1
                # Format with 5-digit zero padding
                formatted_number = f"{number_int:05d}"
                return formatted_number
            except ValueError:
                logger.error(
                    f"Could not convert extracted digits '{number_str}' from camera name '{camera_name}' to an integer.")
                return "00000"
            except Exception as e:
                logger.error(f"An unexpected error occurred in get_camera_number for '{camera_name}': {e}")
                return "00000"
        else:
            # If no trailing digits are found, log a warning and return None or a default
            logger.warning(
                f"Could not find trailing digits in camera name: '{camera_name}'. Cannot determine camera number.")

            return "00000"


    def on_continue(self):
        """Handles the 'Continue Submission' button click."""
        logger.debug("Validation tab: Continue Submission...")

        # Generate payloads for all checked nodes
        self.dialog.payloads = self.get_payloads()
        logger.debug(f"Generated {len(self.dialog.payloads)} payloads.")
        # logger.debug("Payloads: ", payloads)

        if self.node:
            # Show the validation tab in the dialog
            self.dialog.show_validation_tab()
            logger.debug("Validation tab: Running validation...")

            # Run validation and populate the validation tab with results
            errors, warnings, notices = validation.run(self.node)
            logger.debug("Validation tab: Populating validation results...")
            self.dialog.validation_tab.populate(errors, warnings, notices)
