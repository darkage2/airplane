import sys
from PyQt5.QtWidgets import QApplication
from gui import FlightSearchApp
from api_updates import update_local_data
from flight_search import find_cheapest_flights

def main():
    # Check if local_data needs to be updated
    update_local_data()

    # Create the GUI application
    app = QApplication(sys.argv)
    ex = FlightSearchApp()

    # Connect GUI signals to corresponding functions
    ex.search_button.clicked.connect(handle_search)

    # Start the GUI event loop
    sys.exit(app.exec_())

def handle_search():
    # Get user input from the GUI
    departure, destination, nights, adults = ex.get_user_input()

    # Find the 10 cheapest flights and their costs
    cheapest_flights = find_cheapest_flights(departure, destination, nights, adults, local_data)

    # Display the results in the GUI
    ex.display_results(cheapest_flights)

if __name__ == '__main__':
    main()
