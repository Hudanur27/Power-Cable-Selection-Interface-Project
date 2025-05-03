Power Cable Selection Interface
EE374 Fundamentals of Power Systems and Electrical Equipment - Spring 2024-2025
This project provides a graphical interface application for power cable selection based on load specifications, environmental conditions, and economic analysis as required by the EE374 course project.

Project Overview
The Power Cable Selection Interface allows engineers to:

Specify load requirements (type, power demand, voltage level)
Select environmental conditions
Choose between single-core and three-core cables with appropriate placement options
Calculate line losses, voltage regulation, and perform economic analysis
Filter suitable cables based on input parameters with a smart listing algorithm

Repository Structure

EE374_group_no_50.py: Main application file containing the cable filtering algorithm and core functionality
convert_csv.py: Utility script to convert the provided Excel data to CSV format for easier processing
GUI.py: Contains the user interface design and layout implementation
main.py: Entry point for generating the executable application

How to Use
Option 1: Download and Run the Executable
The easiest way to use this application is to download the executable file from the Releases section:

Go to the "Releases" section of this repository
Download the latest release: EE374_group_no_50.exe
Run the executable by double-clicking it
No installation is required - the application will start immediately


Run the application by clicking twice and wait:
python EE374_group_no_50.exe


Features

Smart Cable Listing: Automatically filters cables based on:

Voltage level compatibility
Current carrying capacity with temperature correction
Cable type (single-core vs. three-core)
Trench configuration and placement options


Calculations:

Line loss calculations (active and reactive power)
Voltage regulation analysis
Economic analysis over a 10-year period


User-Friendly Interface:

Intuitive input sections
Clear display of results
Responsive design



Development Notes

Cable data is processed from CSV format for efficiency
PyInstaller was used to create the standalone executable

Phase-1 Release
This is the Phase-1 release of the project, focusing on:

Overall GUI design
Load specification inputs
Cable type selection
Smart listing algorithm implementation

Additional features will be included in the final Phase-2 release.

Contributors
Group 50 - only member is Hüdanur Demir with ID: 2515930
