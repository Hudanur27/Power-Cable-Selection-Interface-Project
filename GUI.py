
import sys
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, QWidget, 
                             QGroupBox, QFormLayout, QRadioButton, QButtonGroup,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                             QSplitter, QFrame, QTabWidget, QListWidget, QListWidgetItem,
                             QScrollArea, QSizePolicy, QDialog, QTextBrowser, QCheckBox,
                             QGridLayout, QToolTip)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QDoubleValidator, QColor, QPalette, QIcon
from EE374_group_no_50 import CableCalculator

class ModernStyleFrame(QFrame):
    """A styled frame with a modern look"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

class ResultsDialog(QDialog):
    """Enhanced dialog for displaying detailed calculation results"""
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cable Selection Results")
        self.setMinimumSize(700, 500)
        
        # Set up layout
        main_layout = QVBoxLayout(self)
        
        # Results title
        title_label = QLabel("Detailed Calculation Results")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px 0 20px 0;")
        main_layout.addWidget(title_label)
        
        # Create grid layout for displaying calculation results
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        grid_layout.setContentsMargins(15, 15, 15, 15)
        
        # Styling for section headers
        section_style = "font-weight: bold; font-size: 14px; color: #2980b9; margin-top: 10px;"
        value_style = "font-size: 13px; background-color: #f8f9fa; padding: 8px; border-radius: 4px; border: 1px solid #e0e0e0;"
        
        # Add Load Information Section
        load_header = QLabel("Load Information")
        load_header.setStyleSheet(section_style)
        grid_layout.addWidget(load_header, 0, 0, 1, 2)
        
        # Load current
        grid_layout.addWidget(QLabel("Load Current:"), 1, 0)
        load_current_value = QLabel(f"{results.get('load_current', 'N/A'):.2f} A")
        load_current_value.setStyleSheet(value_style)
        grid_layout.addWidget(load_current_value, 1, 1)
        
        # Current per circuit
        grid_layout.addWidget(QLabel("Current per Circuit:"), 2, 0)
        circuit_current_value = QLabel(f"{results.get('current_per_circuit', 'N/A'):.2f} A")
        circuit_current_value.setStyleSheet(value_style)
        grid_layout.addWidget(circuit_current_value, 2, 1)
        
        # Add Correction Factors Section
        factors_header = QLabel("Correction Factors")
        factors_header.setStyleSheet(section_style)
        grid_layout.addWidget(factors_header, 3, 0, 1, 2)
        
        # Temperature correction
        grid_layout.addWidget(QLabel("Temperature Correction Factor:"), 4, 0)
        temp_factor_value = QLabel(f"{results.get('temp_correction', 'N/A'):.3f}")
        temp_factor_value.setStyleSheet(value_style)
        grid_layout.addWidget(temp_factor_value, 4, 1)
        
        # Trench reduction
        grid_layout.addWidget(QLabel("Trench Reduction Factor:"), 5, 0)
        trench_factor_value = QLabel(f"{results.get('trench_reduction', 'N/A'):.3f}")
        trench_factor_value.setStyleSheet(value_style)
        grid_layout.addWidget(trench_factor_value, 5, 1)
        
        # Combined factor
        grid_layout.addWidget(QLabel("Combined Correction Factor:"), 6, 0)
        combined_factor = results.get('temp_correction', 1.0) * results.get('trench_reduction', 1.0)
        combined_factor_value = QLabel(f"{combined_factor:.3f}")
        combined_factor_value.setStyleSheet(value_style)
        grid_layout.addWidget(combined_factor_value, 6, 1)
        
        # Add Required Capacity Section
        capacity_header = QLabel("Required Cable Capacity")
        capacity_header.setStyleSheet(section_style)
        grid_layout.addWidget(capacity_header, 7, 0, 1, 2)
        
        # Required capacity
        grid_layout.addWidget(QLabel("Required Current Capacity:"), 8, 0)
        req_capacity_value = QLabel(f"{results.get('required_capacity', 'N/A'):.2f} A")
        req_capacity_value.setStyleSheet(value_style + "font-weight: bold;")
        grid_layout.addWidget(req_capacity_value, 8, 1)
        
        # Add Configuration Section
        config_header = QLabel("Cable Configuration")
        config_header.setStyleSheet(section_style)
        grid_layout.addWidget(config_header, 9, 0, 1, 2)
        
        # Cable type
        grid_layout.addWidget(QLabel("Cable Type:"), 10, 0)
        cable_type_value = QLabel(f"{'Single-Core' if results.get('is_single_core', True) else 'Three-Core'}")
        cable_type_value.setStyleSheet(value_style)
        grid_layout.addWidget(cable_type_value, 10, 1)
        
        # Placement type
        grid_layout.addWidget(QLabel("Placement Type:"), 11, 0)
        placement_type_value = QLabel(f"{'Trefoil' if results.get('is_trefoil', True) else 'Flat'}")
        placement_type_value.setStyleSheet(value_style)
        grid_layout.addWidget(placement_type_value, 11, 1)
        
        # Number of circuits
        grid_layout.addWidget(QLabel("Number of Circuits:"), 12, 0)
        circuits_value = QLabel(f"{results.get('num_circuits', 'N/A')}")
        circuits_value.setStyleSheet(value_style)
        grid_layout.addWidget(circuits_value, 12, 1)
        
        # Voltage level
        grid_layout.addWidget(QLabel("Voltage Level:"), 13, 0)
        voltage_value = QLabel(f"{results.get('voltage_level_kv', 'N/A')} kV")
        voltage_value.setStyleSheet(value_style)
        grid_layout.addWidget(voltage_value, 13, 1)
        
        # Add this layout to a scrollable area
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_content.setLayout(grid_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)
        
        # Found cables count
        cables_count = len(results.get('filtered_cables', []))
        cables_label = QLabel(f"Found {cables_count} suitable cables")
        cables_label.setAlignment(Qt.AlignCenter)
        cables_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 15px 0;")
        main_layout.addWidget(cables_label)
        
        # Check if recommended cables exist in results dictionary
        if 'recommended_cables' in results:
            recommended_label = QLabel("Recommended Cables:")
            recommended_label.setStyleSheet("font-size: 13px; font-weight: bold;")
            main_layout.addWidget(recommended_label)
            
            recommended_text = QTextBrowser()
            recommended_text.setHtml(results['recommended_cables'])
            recommended_text.setStyleSheet("background-color: #f8f9fa; border: 1px solid #e0e0e0;")
            main_layout.addWidget(recommended_text)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

class PowerCableSelectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Power Cable Selection Interface Project Phase 1 - METU EE374")
        self.setMinimumSize(1000, 750)
        
        # Initialize calculator
        self.calculator = CableCalculator()
        self.original_cable_list = self.calculator.get_original_cable_data()
        
        # Set application style
        self.setup_style()
        
        # Create UI components
        self.init_ui()
        
    def setup_style(self):
        """Set up the application style"""
        # Apply a modern style to the application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QTableWidget {
                alternate-background-color: #f9f9f9;
                gridline-color: #d3d3d3;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 4px;
                border: 1px solid #c0c0c0;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 4px;
                background-color: white;
            }
            QComboBox::drop-down {
                border-left-width: 1px;
                border-left-color: #c0c0c0;
                border-left-style: solid;
                width: 20px;
            }
            QRadioButton {
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        
    def init_ui(self):
        """Initialize the UI components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create title label
        title_label = QLabel("Power Cable Selection Interface")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        main_layout.addWidget(title_label)
        
        # Create subtitle
        subtitle_label = QLabel("METU EE374 - Group 50 - HÜDANUR DEMİR 2515930 ")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # Create form layout for inputs
        input_container = ModernStyleFrame()
        input_layout = QHBoxLayout(input_container)
        input_layout.setSpacing(20)
        
        # Create load specifications group
        load_group = QGroupBox("Load Specifications")
        load_layout = QFormLayout()
        load_layout.setSpacing(10)
        load_layout.setContentsMargins(15, 15, 15, 15)
        
        # Load type combo box
        self.load_type_combo = QComboBox()
        self.load_type_combo.addItems(["Industrial", "Residential", "Municipal", "Commercial"])
        self.load_type_combo.setMinimumWidth(150)
        load_layout.addRow("Load Type:", self.load_type_combo)
        
        # Voltage level input with common options
        voltage_layout = QHBoxLayout()
        self.voltage_level_input = QLineEdit()
        self.voltage_level_input.setValidator(QDoubleValidator(0.1, 40000, 2))
        self.voltage_level_input.setText("400")
        self.voltage_level_input.setFixedWidth(100)
        
        # Add common voltage levels dropdown
        self.voltage_presets = QComboBox()
        self.voltage_presets.addItems(["Custom", "230 V", "400 V", "6.3 kV", "10.5 kV", "34.5 kV"])
        self.voltage_presets.currentIndexChanged.connect(self.update_voltage_preset)
        
        voltage_layout.addWidget(self.voltage_level_input)
        voltage_layout.addWidget(QLabel("V"))
        voltage_layout.addWidget(self.voltage_presets)
        load_layout.addRow("Voltage Level:", voltage_layout)
        
        # Active power input
        self.active_power_input = QLineEdit()
        self.active_power_input.setValidator(QDoubleValidator(0.001, 100000, 3))
        self.active_power_input.setPlaceholderText("Enter power in kW")
        load_layout.addRow("Active Power (kW):", self.active_power_input)
        
        # Reactive power input
        self.reactive_power_input = QLineEdit()
        self.reactive_power_input.setValidator(QDoubleValidator(0.001, 100000, 3))
        self.reactive_power_input.setPlaceholderText("Enter power in kVAR")
        load_layout.addRow("Reactive Power (kVAR):", self.reactive_power_input)
        
        # Temperature selection with visual indicators
        self.temp_combo = QComboBox()
        temp_options = ["5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"]
        
        for temp in temp_options:
            self.temp_combo.addItem(temp)
            
        self.temp_combo.setCurrentText("20°C")
        load_layout.addRow("Environment Temperature:", self.temp_combo)
        
        load_group.setLayout(load_layout)
        input_layout.addWidget(load_group)
        
        # Create cable specifications group
        cable_group = QGroupBox("Cable Specifications")
        cable_layout = QFormLayout()
        cable_layout.setSpacing(10)
        cable_layout.setContentsMargins(15, 15, 15, 15)
        
        # Cable type selection (single-core or three-core)
        cable_type_layout = QHBoxLayout()
        self.single_core_radio = QRadioButton("Single-Core")
        self.three_core_radio = QRadioButton("Three-Core")
        self.cable_type_group = QButtonGroup()
        self.cable_type_group.addButton(self.single_core_radio)
        self.cable_type_group.addButton(self.three_core_radio)
        self.single_core_radio.setChecked(True)
        
        cable_type_layout.addWidget(self.single_core_radio)
        cable_type_layout.addWidget(self.three_core_radio)
        cable_layout.addRow("Cable Type:", cable_type_layout)
        
        # Placement type (only for single-core)
        placement_layout = QHBoxLayout()
        self.flat_radio = QRadioButton("Flat Layout (...)")
        self.trefoil_radio = QRadioButton("Trefoil Layout (:·)")
        self.placement_group = QButtonGroup()
        self.placement_group.addButton(self.flat_radio)
        self.placement_group.addButton(self.trefoil_radio)
        self.flat_radio.setChecked(True)
        
        placement_layout.addWidget(self.flat_radio)
        placement_layout.addWidget(self.trefoil_radio)
        cable_layout.addRow("Placement:", placement_layout)
        
        # Number of circuits
        self.circuits_combo = QComboBox()
        self.circuits_combo.addItems(["1", "2", "3", "4", "5", "6"])
        cable_layout.addRow("Number of Circuits:", self.circuits_combo)
        
        # Cable length input
        self.cable_length_input = QLineEdit()
        self.cable_length_input.setValidator(QDoubleValidator(0.001, 10000, 3))
        self.cable_length_input.setPlaceholderText("Enter length in km")
        cable_layout.addRow("Cable Length (km):", self.cable_length_input)
        
        cable_group.setLayout(cable_layout)
        input_layout.addWidget(cable_group)
        
        main_layout.addWidget(input_container)
        
        # Create buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        # Calculate button
        self.calculate_btn = QPushButton("List Available Cables")
        self.calculate_btn.setMinimumHeight(40)
        self.calculate_btn.clicked.connect(self.update_cable_list)
        buttons_layout.addWidget(self.calculate_btn)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_inputs)
        buttons_layout.addWidget(self.clear_btn)
        
        # View Results button
        self.view_results_btn = QPushButton("View Detailed Results")
        self.view_results_btn.setMinimumHeight(40)
        self.view_results_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.view_results_btn.clicked.connect(self.show_detailed_results)
        self.view_results_btn.setEnabled(False)  # Disabled until calculation is performed
        buttons_layout.addWidget(self.view_results_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Results section
        results_container = ModernStyleFrame()
        results_layout = QVBoxLayout(results_container)
        
        # Cable selection results header
        results_header_layout = QHBoxLayout()
        
        results_header = QLabel("Available Cables")
        results_header_font = QFont()
        results_header_font.setPointSize(12)
        results_header_font.setBold(True)
        results_header.setFont(results_header_font)
        results_header_layout.addWidget(results_header)
        
        # Add selection count label
        self.selection_label = QLabel("No cables selected")
        self.selection_label.setStyleSheet("color: #7f8c8d;")
        results_header_layout.addWidget(self.selection_label, alignment=Qt.AlignRight)
        
        results_layout.addLayout(results_header_layout)
        
        # Cable list display in a modern table with selection checkboxes
        self.cable_table = QTableWidget()
        self.cable_table.setColumnCount(5)  # Added a column for checkboxes
        self.cable_table.setHorizontalHeaderLabels([
            "Select", "Cable ID", "Cable Format", "Current Capacity (A)", "Voltage Level"
        ])
        
        # Set table properties for better appearance
        self.cable_table.setAlternatingRowColors(True)
        self.cable_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cable_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cable_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cable_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.cable_table.verticalHeader().setVisible(False)
        
        # Connect cell changed signal to update selection count
        self.cable_table.cellChanged.connect(self.update_selection_count)
        
        results_layout.addWidget(self.cable_table)
        
        # Add a button to export selected cables
        self.export_btn = QPushButton("Export Selected Cables")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.export_btn.clicked.connect(self.export_selected_cables)
        results_layout.addWidget(self.export_btn, alignment=Qt.AlignRight)
        
        main_layout.addWidget(results_container)
        
        # Status bar
        self.statusBar().showMessage("Ready. Please enter load specifications and click 'List Available Cables'")
        
        # Connect signals
        self.single_core_radio.toggled.connect(self.update_placement_visibility)
        self.single_core_radio.toggled.connect(self.update_max_circuits)
        self.three_core_radio.toggled.connect(self.update_max_circuits)
        self.flat_radio.toggled.connect(self.refresh_table)
        self.trefoil_radio.toggled.connect(self.refresh_table)
        
        # Initialize the table with all cables
        self.display_all_cables()
        # Initialize placement visibility
        self.update_placement_visibility()
        # Initialize max circuits
        self.update_max_circuits()
        
        # Store last calculation results
        self.last_results = None
        
    def update_selection_count(self):
        """Update the selection count display"""
        selected_count = 0
        selected_ids = []
        
        for row in range(self.cable_table.rowCount()):
            checkbox_item = self.cable_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                selected_count += 1
                selected_ids.append(self.cable_table.item(row, 1).text())
        
        if selected_count == 0:
            self.selection_label.setText("No cables selected")
        else:
            id_text = ", ".join(selected_ids[:5])
            if len(selected_ids) > 5:
                id_text += f" and {len(selected_ids) - 5} more"
            self.selection_label.setText(f"{selected_count} cables selected: {id_text}")
    
    def export_selected_cables(self):
        """Export the selected cables to a file or system clipboard"""
        selected_cables = []
        
        for row in range(self.cable_table.rowCount()):
            checkbox_item = self.cable_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                cable_id = self.cable_table.item(row, 1).text()
                cable_format = self.cable_table.item(row, 2).text()
                current_capacity = self.cable_table.item(row, 3).text()
                voltage_level = self.cable_table.item(row, 4).text()
                
                selected_cables.append({
                    "Cable ID": cable_id,
                    "Cable Format": cable_format,
                    "Current Capacity": current_capacity,
                    "Voltage Level": voltage_level
                })
        
        if not selected_cables:
            QMessageBox.warning(self, "No Selection", "Please select at least one cable to export.")
            return
        
        # Display the selected cables in a simple dialog
        export_info = "\n".join([
            f"Cable ID: {cable['Cable ID']}, Format: {cable['Cable Format']}, " +
            f"Current Capacity: {cable['Current Capacity']}, Voltage: {cable['Voltage Level']}"
            for cable in selected_cables
        ])
        
        export_message = QMessageBox(self)
        export_message.setWindowTitle("Selected Cables")
        export_message.setText(f"Selected {len(selected_cables)} cables:")
        export_message.setDetailedText(export_info)
        export_message.setIcon(QMessageBox.Information)
        export_message.exec()
    
    def show_detailed_results(self):
        """Show the detailed calculation results in a modern dialog"""
        if self.last_results:
            dialog = ResultsDialog(self.last_results, self)
            dialog.exec()
        else:
            QMessageBox.information(self, "No Results", "Please calculate available cables first.")
        
    def refresh_table(self):
        """Refresh the table when placement option changes"""
        if hasattr(self, 'last_filtered_cables'):
            # If we have filtered cables, redisplay them with new placement
            self.display_cable_list(self.last_filtered_cables)
        else:
            # Otherwise show all cables
            self.display_all_cables()
        
    def update_voltage_preset(self):
        """Update voltage level field based on preset selection"""
        preset = self.voltage_presets.currentText()
        
        if preset != "Custom":
            # Extract numeric value
            if "kV" in preset:
                value = float(preset.split()[0]) * 1000  # Convert kV to V
            else:
                value = float(preset.split()[0])
                
            self.voltage_level_input.setText(str(int(value)))
        
    def update_max_circuits(self):
        """Update maximum available circuits based on cable type"""
        if self.single_core_radio.isChecked():
            # Single-core cables limited to 2 circuits max (as per project requirements)
            current_index = self.circuits_combo.currentIndex()
            self.circuits_combo.clear()
            self.circuits_combo.addItems(["1", "2"])
            # Keep current selection if possible
            if current_index < 2:
                self.circuits_combo.setCurrentIndex(current_index)
        else:
            # Three-core cables can have up to 6 circuits
            current_index = self.circuits_combo.currentIndex()
            self.circuits_combo.clear()
            self.circuits_combo.addItems(["1", "2", "3", "4", "5", "6"])
            # Keep current selection if possible
            self.circuits_combo.setCurrentIndex(min(current_index, 5))
        
    def update_placement_visibility(self):
        """Update the visibility of placement options based on cable type selection"""
        is_single_core = self.single_core_radio.isChecked()
        self.flat_radio.setEnabled(is_single_core)
        self.trefoil_radio.setEnabled(is_single_core)
        
        # If three-core is selected, force trefoil (since that's what we have data for)
        if not is_single_core:
            self.trefoil_radio.setChecked(True)
        
    def clear_inputs(self):
        """Clear all input fields and reset cable list"""
        self.active_power_input.clear()
        self.reactive_power_input.clear()
        self.voltage_level_input.setText("400")
        self.voltage_presets.setCurrentIndex(0)
        self.load_type_combo.setCurrentIndex(0)
        self.temp_combo.setCurrentText("20°C")
        self.single_core_radio.setChecked(True)
        self.flat_radio.setChecked(True)
        self.circuits_combo.setCurrentIndex(0)
        self.cable_length_input.clear()
        
        # Reset last filtered cables
        if hasattr(self, 'last_filtered_cables'):
            delattr(self, 'last_filtered_cables')
            
        # Reset last results
        self.last_results = None
        self.view_results_btn.setEnabled(False)
            
        # Reset and display all cables
        self.display_all_cables()
        self.statusBar().showMessage("Inputs cleared. Showing all available cables.")
        
    def display_all_cables(self):
        """Display all cables in the table"""
        self.display_cable_list(self.original_cable_list)
        
    def display_cable_list(self, cable_list):
        """Display the provided cable list in the table with checkboxes"""
        self.cable_table.setRowCount(len(cable_list))
        # Temporarily disconnect the cellChanged signal to prevent multiple updates
        self.cable_table.cellChanged.disconnect(self.update_selection_count)
        
        for i, (_, cable) in enumerate(cable_list.iterrows()):
            # Add checkbox for selection
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.cable_table.setItem(i, 0, checkbox_item)
            
            # Handle the Cable ID - ensure it's an integer
            try:
                cable_id = int(cable['Cable ID'])
            except:
                cable_id = i + 1
            
            # Create items with better styling
            id_item = QTableWidgetItem(str(cable_id))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.cable_table.setItem(i, 1, id_item)
            
            # Display cable format
            format_item = QTableWidgetItem(str(cable['Cable Format (mm²)']))
            format_item.setTextAlignment(Qt.AlignCenter)
            self.cable_table.setItem(i, 2, format_item)
            
            # Determine which current capacity to display based on cable format and placement
            is_single_core = str(cable['Cable Format (mm²)']).lower().startswith('1x')
            
            # Get the appropriate current capacity based on cable type and placement
            if is_single_core:
                if self.trefoil_radio.isChecked():
                    current_capacity = cable['Current Capacity Trefoil (A)']
                else:
                    current_capacity = cable['Current Capacity Flat (A)']
            else:
                # For three-core cables, always use trefoil capacity as that's what's available in the CSV
                current_capacity = cable['Current Capacity Trefoil (A)']
            
            # Handle NA/0 values in current capacity    
            if pd.isna(current_capacity) or current_capacity == 0:
                current_capacity_str = "N/A"
            else:
                current_capacity_str = str(current_capacity)
                
            capacity_item = QTableWidgetItem(current_capacity_str)
            capacity_item.setTextAlignment(Qt.AlignCenter)
            self.cable_table.setItem(i, 3, capacity_item)
            
            # Display voltage level
            voltage_item = QTableWidgetItem(str(cable['Voltage Level']))
            voltage_item.setTextAlignment(Qt.AlignCenter)
            self.cable_table.setItem(i, 4, voltage_item)
        
        # Reconnect the cellChanged signal after populating
        self.cable_table.cellChanged.connect(self.update_selection_count)
        # Update the selection count
        self.update_selection_count()
    
    def update_cable_list(self):
   
    # Check if required fields are filled
        if not (self.active_power_input.text() and self.reactive_power_input.text() and 
            self.voltage_level_input.text()):
            QMessageBox.warning(self, "Input Error", "Please fill in all required load specification fields!")
            return
    
        try:
             # Get input values
            active_power = float(self.active_power_input.text())  # kW
            reactive_power = float(self.reactive_power_input.text())  # kVAR
            voltage = float(self.voltage_level_input.text())  # V
        
            # Get temperature from combobox (remove °C and convert to int)
            temperature = int(self.temp_combo.currentText().split('°')[0])
        
            # Get cable configuration
            is_single_core = self.single_core_radio.isChecked()
            is_trefoil = self.trefoil_radio.isChecked()
            num_circuits = int(self.circuits_combo.currentText())
        
            # Use the calculator to filter cables
            results = self.calculator.filter_cables(
            active_power, reactive_power, voltage, temperature,
            is_single_core, is_trefoil, num_circuits
            )
        
            # Ensure the UI selections are properly stored in the results
            results['is_single_core'] = is_single_core
            results['is_trefoil'] = is_trefoil
            results['num_circuits'] = num_circuits
        
             # Store results for detailed view later
            self.last_results = results
            # Enable the view results button
            self.view_results_btn.setEnabled(True)
        
            # Store the filtered cables for later reference (when toggling placement options)
            self.last_filtered_cables = results['filtered_cables']
        
            # Display filtered cables
            if results['filtered_cables'].empty:
                QMessageBox.information(self, "No Suitable Cables", 
                                   f"No suitable cables found for:\n"
                                   f"- Load Current: {results['load_current']:.2f} A\n"
                                   f"- Required Capacity: {results['required_capacity']:.2f} A\n"
                                   f"- Cable Type: {'Single-Core' if is_single_core else 'Three-Core'}\n"
                                   f"- Placement: {'Trefoil' if is_trefoil and is_single_core else 'Flat'}\n"
                                   f"- Voltage Level: {results['voltage_level_kv']}")
                self.statusBar().showMessage("No suitable cables found for the given specifications.")
            else:
                self.display_cable_list(results['filtered_cables'])
            
                # Get cable IDs as a comma-separated string
                cable_ids = [str(int(cable['Cable ID'])) for _, cable in results['filtered_cables'].iterrows()]
                cable_id_str = ", ".join(cable_ids[:10])
                if len(cable_ids) > 10:
                    cable_id_str += f", and {len(cable_ids) - 10} more"
            
                # Show compact notification message
                notification = QMessageBox(self)
                notification.setWindowTitle("Cables Found")
                notification.setText(f"Found {len(results['filtered_cables'])} suitable cables.")
                notification.setInformativeText(f"Cable IDs: {cable_id_str}\n\n"
                                         f"Click 'View Detailed Results' for complete information.")
                notification.setIcon(QMessageBox.Information)
                notification.addButton("OK", QMessageBox.AcceptRole)
                view_btn = notification.addButton("View Details", QMessageBox.ActionRole)
                notification.exec()
            
                # If user clicked "View Details", show the detailed results dialog
                if notification.clickedButton() == view_btn:
                    self.show_detailed_results()
            
                self.statusBar().showMessage(f"Found {len(results['filtered_cables'])} suitable cables. Use checkbox to select specific cables.")
            
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Please enter valid values: {str(e)}")
            return


