# Phenom 100 CG Calc
Phenom CG Calc is a simple app to calculate the center of gravity of the Phenom 100. It allows users to generate a detailed flight report in PDF format, including essential information such as origin, destination, crew, passengers, notes, a complete weight and balance table, and a graphical representation of the data.


## Project Status
Completed


## Usage
-   Open the application and enter the required flight data.
-   The app will calculate the center of gravity and display the results.
-   You can generate a PDF report with the calculations and a graphical representation.
-   You can change the default values if necessary


## Installation
To simplify library installation, the project includes two setup scripts:

- **setupProjectFedora.sh** → for Fedora/Linux  
- **setupProjectWindows.bat** → for Windows

These scripts will:

-> Create a Python virtual environment  
->  Install all required libraries  
-> Generate a `requirements.txt` file


## How to Use the Installation Scripts
### On Fedora/Linux
1. Make the script executable:
   ```bash
   chmod +x setupProjectFedora.sh
2. Run the script
    ```bash
    ./setupProjectFedora.sh
### On Windows
1. Run the script
    ```bat
    setupProjectWindows.bat
