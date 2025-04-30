import math
import pandas as pd

class CableCalculator:
    def __init__(self):
        """Initialize the cable calculator with cable data"""
        self.load_cable_data()
        
    def load_cable_data(self):
        """Load cable data from CSV file with the real cable specifications"""
        try:
            # Try to load the cable data from CSV file
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
                
        except Exception as e:
            # If file not found or error in processing, create simple empty dataframe with correct columns
            print(f"Error loading cable data: {e}")
            
            columns = ['Cable ID', 'Cable Format (mm²)', 'Voltage Level', 'Min Voltage (kV)', 'Max Voltage (kV)',
                      'Current Capacity Flat (A)', 'Current Capacity Trefoil (A)', 
                      'Resistance (ohm/km)', 'Inductance Flat (mH/km)', 'Inductance Trefoil (mH/km)',
                      'Capacitance (μF/km)', 'Price (TL/km)']
            
            self.cable_data = pd.DataFrame(columns=columns)
    
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
        
        # Step 2: Get temperature correction factor
        temp_correction = self.get_temperature_correction(temperature)
        
        # Step 3: Get trench reduction factor
        trench_reduction = self.get_trench_reduction(is_single_core, num_circuits)
        
        # Calculate current per circuit
        current_per_circuit = load_current / num_circuits
        
        # Calculate required current capacity after corrections
        required_capacity = current_per_circuit / (temp_correction * trench_reduction)
        
        # Step 4: Filter cables based on requirements
        filtered_cables = self.cable_data.copy()
        
        # Filter by voltage level - must be suitable for the operation voltage (not too low, not too high)
        # For proper insulation, the cable's max voltage should be >= operation voltage
        filtered_cables = filtered_cables[(filtered_cables['Max Voltage (kV)'] >= voltage_level_kv)]
        
        # Don't use cables with excessive insulation (more than 2 voltage levels above the requirement)
        # This is an example of filtering out cables with too much isolation
        if voltage_level_kv <= 1:  # Low voltage
            filtered_cables = filtered_cables[filtered_cables['Max Voltage (kV)'] <= 6]
        elif voltage_level_kv <= 6:  # Medium-low voltage
            filtered_cables = filtered_cables[filtered_cables['Max Voltage (kV)'] <= 10]
        elif voltage_level_kv <= 10:  # Medium voltage
            filtered_cables = filtered_cables[filtered_cables['Max Voltage (kV)'] <= 20]
        
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
            'current_per_circuit': current_per_circuit,
            'temp_correction': temp_correction,
            'trench_reduction': trench_reduction,
            'required_capacity': required_capacity,
            'voltage_level_kv': voltage_level_kv
        }
        
        return results