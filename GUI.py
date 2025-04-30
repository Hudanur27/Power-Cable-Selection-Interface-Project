import sys
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, QWidget, 
                             QGroupBox, QFormLayout, QRadioButton, QButtonGroup,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDoubleValidator
from cable_calculator import CableCalculator

class PowerCableSelectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Power Cable Selection Interface - Phase 1")
        self.setMinimumSize(900, 700)
        
        # Initialize calculator
        self.calculator = CableCalculator()
        self.original_cable_list = self.calculator.get_original_cable_data()
        
        # Create UI components
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create title label
        title_label = QLabel("Power Cable Selection Interface - Phase 1")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create form layout for inputs
        input_layout = QHBoxLayout()
        
        # Create load specifications group
        load_group = QGroupBox("Load Specifications")
        load_layout = QFormLayout()
        
        # Load type combo box
        self.load_type_combo = QComboBox()
        self.load_type_combo.addItems(["Industrial", "Residential", "Municipal", "Commercial"])
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
        load_layout.addRow("Active Power (kW):", self.active_power_input)
        
        # Reactive power input
        self.reactive_power_input = QLineEdit()
        self.reactive_power_input.setValidator(QDoubleValidator(0.001, 100000, 3))
        load_layout.addRow("Reactive Power (kVAR):", self.reactive_power_input)
        
        # Temperature selection
        self.temp_combo = QComboBox()
        self.temp_combo.addItems(["5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"])
        self.temp_combo.setCurrentText("20°C")
        load_layout.addRow("Environment Temperature:", self.temp_combo)
        
        load_group.setLayout(load_layout)
        input_layout.addWidget(load_group)
        
        # Create cable specifications group
        cable_group = QGroupBox("Cable Specifications")
        cable_layout = QFormLayout()
        
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
        self.flat_radio = QRadioButton("Flat (...)")
        self.trefoil_radio = QRadioButton("Trefoil (:·)")
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
        cable_layout.addRow("Cable Length (km):", self.cable_length_input)
        
        cable_group.setLayout(cable_layout)
        input_layout.addWidget(cable_group)
        
        main_layout.addLayout(input_layout)
        
        # Create buttons layout
        buttons_layout = QHBoxLayout()
        
        # Calculate button
        self.calculate_btn = QPushButton("List Available Cables")
        self.calculate_btn.clicked.connect(self.update_cable_list)
        buttons_layout.addWidget(self.calculate_btn)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_inputs)
        buttons_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Cable list display
        self.cable_table = QTableWidget()
        self.cable_table.setColumnCount(9)
        self.cable_table.setHorizontalHeaderLabels([
            "Cable ID", "Cable Format (mm²)", "Current Capacity (A)", "Resistance (ohm/km)", 
            "Inductance (mH/km)", "Capacitance (μF/km)", "Price (TL/km)", "Voltage Level", 
            "Max Circuits"
        ])
        self.cable_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(QLabel("Available Cables:"))
        main_layout.addWidget(self.cable_table)
        
        # Connect signals
        self.single_core_radio.toggled.connect(self.update_placement_visibility)
        self.single_core_radio.toggled.connect(self.update_max_circuits)
        self.three_core_radio.toggled.connect(self.update_max_circuits)
        
        # Initialize the table with all cables
        self.display_all_cables()
        # Initialize placement visibility
        self.update_placement_visibility()
        # Initialize max circuits
        self.update_max_circuits()
        
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
        
        # Reset and display all cables
        self.display_all_cables()
        
    def display_all_cables(self):
        """Display all cables in the table"""
        self.display_cable_list(self.original_cable_list)
        
    def display_cable_list(self, cable_list):
        """Display the provided cable list in the table"""
        self.cable_table.setRowCount(len(cable_list))
        
        for i, (_, cable) in enumerate(cable_list.iterrows()):
            # Handle the Cable ID - ensure it's an integer
            try:
                cable_id = int(cable['Cable ID'])
            except:
                cable_id = i + 1
            self.cable_table.setItem(i, 0, QTableWidgetItem(str(cable_id)))
            
            # Display cable format
            self.cable_table.setItem(i, 1, QTableWidgetItem(str(cable['Cable Format (mm²)'])))
            
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
                
            self.cable_table.setItem(i, 2, QTableWidgetItem(current_capacity_str))
            self.cable_table.setItem(i, 3, QTableWidgetItem(str(cable['Resistance (ohm/km)'])))
            
            # Determine inductance to display based on cable type and placement
            if is_single_core:
                if self.trefoil_radio.isChecked():
                    inductance = cable['Inductance Trefoil (mH/km)']
                else:
                    inductance = cable['Inductance Flat (mH/km)']
            else:
                # For three-core cables, use the available inductance
                if not pd.isna(cable['Inductance Trefoil (mH/km)']) and cable['Inductance Trefoil (mH/km)'] != 0:
                    inductance = cable['Inductance Trefoil (mH/km)']
                else:
                    inductance = cable['Inductance Flat (mH/km)']
                
            # Handle NA/0 values in inductance
            if pd.isna(inductance) or inductance == 0:
                inductance_str = "N/A"
            else:
                inductance_str = str(inductance)
                
            self.cable_table.setItem(i, 4, QTableWidgetItem(inductance_str))
            
            # Handle capacitance, might be NA in CSV
            capacitance = cable['Capacitance (μF/km)']
            if pd.isna(capacitance) or capacitance == 0:
                capacitance_str = "N/A"
            else:
                capacitance_str = str(capacitance)
                
            self.cable_table.setItem(i, 5, QTableWidgetItem(capacitance_str))
            self.cable_table.setItem(i, 6, QTableWidgetItem(str(cable['Price (TL/km)'])))
            self.cable_table.setItem(i, 7, QTableWidgetItem(str(cable['Voltage Level'])))
            
            # Calculate max circuits
            max_circuits = 2 if is_single_core else 6
            self.cable_table.setItem(i, 8, QTableWidgetItem(str(max_circuits)))
    
    def update_cable_list(self):
        """Update the cable list based on input parameters"""
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
            
            # Display filtered cables
            if results['filtered_cables'].empty:
                QMessageBox.information(self, "No Suitable Cables", 
                                       f"No suitable cables found for:\n"
                                       f"- Load Current: {results['load_current']:.2f} A\n"
                                       f"- Required Capacity: {results['required_capacity']:.2f} A\n"
                                       f"- Cable Type: {'Single-Core' if is_single_core else 'Three-Core'}\n"
                                       f"- Placement: {'Trefoil' if is_trefoil and is_single_core else 'Flat'}\n"
                                       f"- Voltage Level: {results['voltage_level_kv']:.2f} kV")
            else:
                self.display_cable_list(results['filtered_cables'])
                QMessageBox.information(self, "Cable Selection Summary", 
                                       f"Load Current: {results['load_current']:.2f} A\n"
                                       f"Current per Circuit: {results['current_per_circuit']:.2f} A\n"
                                       f"Temperature Correction Factor: {results['temp_correction']:.2f}\n"
                                       f"Trench Reduction Factor: {results['trench_reduction']:.2f}\n"
                                       f"Required Current Capacity: {results['required_capacity']:.2f} A\n"
                                       f"Found {len(results['filtered_cables'])} suitable cables")
                
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Please enter valid values: {str(e)}")
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PowerCableSelectionApp()
    window.show()
    sys.exit(app.exec())