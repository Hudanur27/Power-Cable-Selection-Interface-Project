import math
import pandas as pd
import os
import sys

class CableCalculator:
    def __init__(self):
        """Initialize the cable calculator with cable data"""
        self.load_cable_data()
        
    def load_cable_data(self):
        """Load cable data either from CSV file or from embedded data if CSV not found"""
        try:
            # First try to load the cable data from CSV file
            try:
                from main import get_resource_path
                csv_path = get_resource_path('output.csv')
                self.cable_data = pd.read_csv(csv_path, skiprows=1)
            except:
                # If that fails, try current directory
                self.cable_data = pd.read_csv('output.csv', skiprows=1)
                
            # Map the column names to match our application needs
            column_mapping = {
                'Cable ID': 'Cable ID',
                'Cable code': 'Cable Format (mm²)',
                'Voltage level': 'Voltage Level',
                'Current Capacity (A) at 20°C ...': 'Current Capacity Flat (A)',
                'Current Capacity (A) at 20°C :.': 'Current Capacity Trefoil (A)',
                'Resistance (ohm/km)': 'Resistance (ohm/km)',
                'Inductance ... (mH/km)': 'Inductance Flat (mH/km)',
                'Inductance :. (mH/km)': 'Inductance Trefoil (mH/km)',
                'Capacitance (uF/km)': 'Capacitance (μF/km)',
                'Price (TL/km)': 'Price (TL/km)'
            }
            
            self.cable_data = self.cable_data.rename(columns=column_mapping)
            
            # Extract min and max voltage levels for each cable
            # Format is typically like "0.6/1 kV" where 1 is the max voltage
            self.cable_data['Min Voltage (kV)'] = self.cable_data['Voltage Level'].str.extract(r'(\d+\.?\d*)\/').astype(float)
            self.cable_data['Max Voltage (kV)'] = self.cable_data['Voltage Level'].str.extract(r'\/(\d+\.?\d*)').astype(float)
            
            # Convert NA values to 0 for numeric processing
            numeric_columns = ['Current Capacity Flat (A)', 'Current Capacity Trefoil (A)', 
                             'Inductance Flat (mH/km)', 'Inductance Trefoil (mH/km)', 'Capacitance (μF/km)']
            for col in numeric_columns:
                self.cable_data[col] = pd.to_numeric(self.cable_data[col], errors='coerce').fillna(0)
                
            print("Successfully loaded cable data from CSV file")
                
        except Exception as e:
            # If file not found or error in processing, use embedded data instead
            print(f"CSV not found or error: {e}. Using embedded cable data instead.")
            
            # Here we embed the actual cable data directly from output.csv
            data = [
                # Cable ID, Cable Format, Voltage Level, Curr Cap Flat, Curr Cap Trefoil, Resistance, Ind Flat, Ind Trefoil, Capacitance, Price
                [1, '1x10 mm2', '0.6/1 kV', 81, 69, 1.83, 0.34, 0.41, 0, 102300],
                [2, '1x16 mm2', '0.6/1 kV', 108, 92, 1.15, 0.317, 0.387, 0, 156600],
                [3, '1x25 mm2', '0.6/1 kV', 146, 124, 0.727, 0.304, 0.374, 0, 241400],
                [4, '1x35 mm2', '0.6/1 kV', 180, 153, 0.524, 0.291, 0.36, 0, 328300],
                [5, '1x50 mm2', '0.6/1 kV', 220, 187, 0.387, 0.281, 0.351, 0, 434000],
                [6, '1x70 mm2', '0.6/1 kV', 279, 237, 0.268, 0.272, 0.341, 0, 623000],
                [7, '1x95 mm2', '0.6/1 kV', 347, 294, 0.193, 0.264, 0.333, 0, 847000],
                [8, '1x120 mm2', '0.6/1 kV', 405, 343, 0.153, 0.259, 0.329, 0, 1080000],
                [9, '3x16+10 mm2', '0.6/1 kV', 0, 89, 1.15, 0, 0.264, 0, 640000],
                [10, '3x25+16 mm2', '0.6/1 kV', 0, 120, 0.727, 0, 0.265, 0, 990000],
                [11, '3x35+16 mm2', '0.6/1 kV', 0, 147, 0.524, 0, 0.258, 0, 1300000],
                [12, '3x50+25 mm2', '0.6/1 kV', 0, 179, 0.387, 0, 0.256, 0, 1750000],
                [13, '3x70+35 mm2', '0.6/1 kV', 0, 224, 0.268, 0, 0.253, 0, 2520000],
                [14, '3x95+50 mm2', '0.6/1 kV', 0, 277, 0.193, 0, 0.247, 0, 3400000],
                [15, '3x120+70 mm2', '0.6/1 kV', 0, 323, 0.153, 0, 0.246, 0, 4400000],
                [16, '3x150+70 mm2', '0.6/1 kV', 0, 368, 0.124, 0, 0.248, 0, 5200000],
                [17, '1x25 mm2', '3.6/6 kV', 196, 163, 0.727, 0.77, 0.43, 0.25, 351000],
                [18, '1x35 mm2', '3.6/6 kV', 238, 198, 0.524, 0.75, 0.41, 0.28, 532000],
                [19, '1x50 mm2', '3.6/6 kV', 286, 238, 0.387, 0.72, 0.39, 0.31, 638000],
                [20, '1x70 mm2', '3.6/6 kV', 356, 296, 0.268, 0.68, 0.37, 0.36, 825000],
                [21, '1x95 mm2', '3.6/6 kV', 434, 361, 0.193, 0.65, 0.36, 0.4, 1070000],
                [22, '1x120 mm2', '3.6/6 kV', 600, 417, 0.153, 0.63, 0.34, 0.44, 1300000],
                [23, '1x150 mm2', '3.6/6 kV', 559, 473, 0.124, 0.62, 0.33, 0.48, 1640000],
                [24, '1x185 mm2', '3.6/6 kV', 637, 543, 0.0991, 0.6, 0.32, 0.52, 1950000],
                [25, '3x25+16 mm2', '3.6/6 kV', 0, 143, 0.727, 0, 0.37, 0.25, 1647000],
                [26, '3x35+16 mm2', '3.6/6 kV', 0, 172, 0.524, 0, 0.35, 0.28, 2002000],
                [27, '3x50+16 mm2', '3.6/6 kV', 0, 205, 0.387, 0, 0.34, 0.3, 2594000],
                [28, '3x70+16 mm2', '3.6/6 kV', 0, 253, 0.268, 0, 0.32, 0.35, 3450000],
                [29, '3x95+16 mm2', '3.6/6 kV', 0, 307, 0.193, 0, 0.31, 0.39, 4727000],
                [30, '3x120+16 mm2', '3.6/6 kV', 0, 352, 0.153, 0, 0.3, 0.43, 5784000],
                [31, '3x150+25 mm2', '3.6/6 kV', 0, 397, 0.124, 0, 0.29, 0.47, 6963000],
                [32, '3x185+25 mm2', '3.6/6 kV', 0, 453, 0.0991, 0, 0.28, 0.5, 8481000],
                [33, '1x35 mm2', '6/10 kV', 231, 195, 0.524, 0.661, 0.383, 0.223, 785100],
                [34, '1x50 mm2', '6/10 kV', 277, 234, 0.387, 0.636, 0.366, 0.248, 944900],
                [35, '1x70 mm2', '6/10 kV', 345, 292, 0.268, 0.606, 0.349, 0.285, 1226000],
                [36, '1x95 mm2', '6/10 kV', 418, 354, 0.193, 0.582, 0.334, 0.32, 1533000],
                [37, '1x120 mm2', '6/10 kV', 481, 407, 0.153, 0.563, 0.323, 0.35, 1872000],
                [38, '1x150 mm2', '6/10 kV', 537, 460, 0.124, 0.546, 0.313, 0.382, 2362000],
                [39, '1x185 mm2', '6/10 kV', 612, 527, 0.0991, 0.529, 0.304, 0.415, 2838000],
                [40, '3x35 mm2', '6/10 kV', 0, 173, 0.524, 0, 0.374, 0.189, 2127000],
                [41, '3x50 mm2', '6/10 kV', 0, 206, 0.387, 0, 0.355, 0.209, 2716000],
                [42, '3x70 mm2', '6/10 kV', 0, 257, 0.268, 0, 0.336, 0.236, 3603000],
                [43, '3x95 mm2', '6/10 kV', 0, 313, 0.193, 0, 0.32, 0.263, 4901000],
                [44, '3x120 mm2', '6/10 kV', 0, 360, 0.153, 0, 0.308, 0.291, 5934000],
                [45, '3x150 mm2', '6/10 kV', 0, 410, 0.124, 0, 0.299, 0.314, 7125000],
                [46, '3x185 mm2', '6/10 kV', 0, 469, 0.0991, 0, 0.29, 0.341, 8659000],
                [47, '1x95 mm2', '12/20 kV', 420, 358, 0.193, 0.59, 0.36, 0.218, 1560000],
                [48, '1x120 mm2', '12/20 kV', 483, 412, 0.153, 0.571, 0.349, 0.238, 1906000],
                [49, '1x150 mm2', '12/20 kV', 540, 466, 0.124, 0.554, 0.338, 0.258, 2393000],
                [50, '1x185 mm2', '12/20 kV', 614, 534, 0.0991, 0.538, 0.329, 0.278, 2877000],
                [51, '1x240 mm2', '12/20 kV', 718, 627, 0.0754, 0.518, 0.317, 0.308, 3543000],
                [52, '1x300 mm2', '12/20 kV', 813, 715, 0.0601, 0.501, 0.308, 0.336, 4455000],
                [53, '1x400 mm2', '12/20 kV', 904, 819, 0.047, 0.48, 0.298, 0.377, 5669000],
                [54, '1x150 mm2', '20.3/35 kV', 559, 473, 0.124, 0.64, 0.41, 0.17, 1720000],
                [55, '1x185 mm2', '20.3/35 kV', 637, 543, 0.0991, 0.63, 0.39, 0.18, 2020000],
                [56, '1x240 mm2', '20.3/35 kV', 745, 641, 0.0754, 0.6, 0.38, 0.2, 2530000],
                [57, '1x300 mm2', '20.3/35 kV', 846, 735, 0.0601, 0.59, 0.37, 0.21, 3150000],
                [58, '1x400 mm2', '20.3/35 kV', 938, 845, 0.047, 0.57, 0.35, 0.23, 4100000],
                [59, '1x500 mm2', '20.3/35 kV', 1010, 950, 0.0366, 0.55, 0.34, 0.26, 5150000],
                [60, '1x630 mm2', '20.3/35 kV', 1120, 1040, 0.0283, 0.52, 0.33, 0.29, 6550000],
                [61, '3x95 mm2', '20.3/35 kV', 0, 307, 0.193, 0, 0.4, 0.15, 4600000],
                [62, '3x120 mm2', '20.3/35 kV', 0, 352, 0.153, 0, 0.39, 0.16, 5500000],
                [63, '3x150 mm2', '20.3/35 kV', 0, 397, 0.124, 0, 0.37, 0.17, 6400000],
                [64, '3x185 mm2', '20.3/35 kV', 0, 453, 0.0991, 0, 0.36, 0.18, 7500000],
                [65, '3x240 mm2', '20.3/35 kV', 0, 529, 0.0754, 0, 0.35, 0.2, 9400000],
                [66, '3x300 mm2', '20.3/35 kV', 0, 626, 0.0601, 0, 0.29, 0.22, 11300000],
                [67, '3x400 mm2', '20.3/35 kV', 0, 720, 0.047, 0, 0.28, 0.24, 14300000]
            ]
            
            columns = ['Cable ID', 'Cable Format (mm²)', 'Voltage Level', 'Current Capacity Flat (A)', 
                      'Current Capacity Trefoil (A)', 'Resistance (ohm/km)', 'Inductance Flat (mH/km)', 
                      'Inductance Trefoil (mH/km)', 'Capacitance (μF/km)', 'Price (TL/km)']
            
            self.cable_data = pd.DataFrame(data, columns=columns)
            
            # Extract min and max voltage levels for each cable
            self.cable_data['Min Voltage (kV)'] = self.cable_data['Voltage Level'].str.extract(r'(\d+\.?\d*)\/').astype(float)
            self.cable_data['Max Voltage (kV)'] = self.cable_data['Voltage Level'].str.extract(r'\/(\d+\.?\d*)').astype(float)
    
    def get_original_cable_data(self):
        """Return the original cable data"""
        return self.cable_data.copy()
    
    def get_temperature_correction(self, temperature):
        """Get the temperature correction factor based on selected temperature"""
        # Temperature correction factors from Table 1
        temp_correction = {
            5: 1.15,
            10: 1.10,
            15: 1.05,
            20: 1.00,
            25: 0.95,
            30: 0.90,
            35: 0.85,
            40: 0.80
        }
        
        return temp_correction.get(temperature, 1.00)
    
    def get_trench_reduction(self, is_single_core, num_circuits):
        """Get the trench reduction factor based on number of cables in the trench"""
        # For single-core cables, each circuit uses 3 cables (one per phase)
        if is_single_core:
            total_cables = num_circuits * 3
        else:
            total_cables = num_circuits
            
        # Cap at maximum of 6 cables in trench as per project requirements
        total_cables = min(total_cables, 6)
        
        # Trench reduction factors from Table 2
        trench_reduction = {
            1: 1.00,
            2: 0.90,
            3: 0.85,
            4: 0.80,
            5: 0.75,
            6: 0.70
        }
        
        return trench_reduction.get(total_cables, 0.70)  # Default to 0.70 for more than 6 cables
    
    def calculate_load_current(self, active_power, reactive_power, voltage):
        """Calculate the load current based on power and voltage inputs"""
        # Calculate apparent power and current
        apparent_power = math.sqrt(active_power**2 + reactive_power**2)  # kVA
        current = (apparent_power * 1000) / (math.sqrt(3) * voltage)  # A
        
        return current, apparent_power
    
    def filter_cables(self, active_power, reactive_power, voltage, temperature, 
                     is_single_core, is_trefoil, num_circuits):
        """Filter cables based on the specified requirements"""
        # Step 1: Calculate apparent power and load current
        load_current, apparent_power = self.calculate_load_current(active_power, reactive_power, voltage)
        
        # Get voltage level for insulation requirements
        voltage_level_kv = voltage / 1000  # Convert to kV
        
        # Step 2: Determine the suitable voltage level based on input voltage
        # For a given input voltage, select EXACTLY ONE suitable voltage rating
        if 0 <= voltage_level_kv < 1:
            suitable_voltage_level = '0.6/1 kV'
        elif 1 <= voltage_level_kv < 6:
            suitable_voltage_level = '3.6/6 kV'
        elif 6 <= voltage_level_kv < 10:
            suitable_voltage_level = '6/10 kV'
        elif 10 <= voltage_level_kv < 20:
            suitable_voltage_level = '12/20 kV'
        elif 20 <= voltage_level_kv < 35:
            suitable_voltage_level = '20.3/35 kV'
        else:
            raise ValueError(f"Input voltage {voltage}V ({voltage_level_kv}kV) exceeds maximum available cable rating (35kV)")
        
        # Step 3: Get temperature correction factor
        temp_correction = self.get_temperature_correction(temperature)
        
        # Step 4: Apply the smart listing algorithm as specified
        # For Phase 1: Always use maximum circuits and maximum trench reduction factor
        if is_single_core:
            # For single-core cables: Always use 2 circuits and trench reduction of 0.7
            max_circuits = 2
            max_trench_reduction = 0.7
        else:
            # For three-core cables: Always use 6 circuits and trench reduction of 0.7
            max_circuits = 6
            max_trench_reduction = 0.7
        
        # Calculate load current after temperature correction
        load_current_after_temp_correction = load_current / temp_correction
        
        # Apply the smart listing algorithm formula
        required_capacity = load_current_after_temp_correction / (max_trench_reduction * max_circuits)
        
        # Step 5: Filter cables based on requirements
        filtered_cables = self.cable_data.copy()
        
        # Filter by voltage level
        filtered_cables = filtered_cables[filtered_cables['Voltage Level'] == suitable_voltage_level]
        
        # Filter by cable type
        if is_single_core:
            filtered_cables = filtered_cables[filtered_cables['Cable Format (mm²)'].str.contains('1x', na=False)]
            # Select capacity field based on placement
            capacity_field = 'Current Capacity Trefoil (A)' if is_trefoil else 'Current Capacity Flat (A)'
        else:
            filtered_cables = filtered_cables[filtered_cables['Cable Format (mm²)'].str.contains('3x', na=False)]
            capacity_field = 'Current Capacity Trefoil (A)'  # For 3-core cables, use trefoil capacity from CSV
        
        # Filter by current capacity
        # For cables where capacity is NA, filter them out
        filtered_cables = filtered_cables[pd.notna(filtered_cables[capacity_field])]
        # Now filter by required capacity
        filtered_cables = filtered_cables[filtered_cables[capacity_field] >= required_capacity]
        
        # Return results
        results = {
            'filtered_cables': filtered_cables,
            'load_current': load_current,
            'apparent_power': apparent_power,
            'current_per_circuit': load_current / num_circuits,  # This is the actual user-selected number of circuits
            'temp_correction': temp_correction,
            'trench_reduction': max_trench_reduction,  # Using the fixed value from the smart listing algorithm
            'required_capacity': required_capacity,
            'voltage_level_kv': suitable_voltage_level
        }
        
        return results
