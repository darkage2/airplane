import requests
from bs4 import BeautifulSoup
import datetime
import json
from flask import Flask, render_template, request


# Define constants
CURRENCY = "HUF"
MAX_NIGHTS = 30
MAX_ADULTS = 10
AIRPORTS = get_available_airports()

app = Flask(name)

def sanitize_input(input_str):
    """
    Sanitizes user input to ensure it is safe and does not contain harmful characters.

    Args:
        input_str (str): The user input string to sanitize.

    Returns:
        str: The sanitized input string.
    """
    # Remove all non-alphanumeric characters except whitespace and hyphens
    input_str = re.sub(r'[^a-zA-Z0-9\s-]+', '', input_str)

    # Convert the input string to lowercase
    input_str = input_str.lower()

    # Strip leading and trailing whitespace
    input_str = input_str.strip()

    return input_str

def get_exchange_rate(currency_from, currency_to):
    """
    Retrieves the current exchange rate from currency_from to currency_to.
    """
    url = f"https://api.exchangeratesapi.io/latest?base={currency_from}&symbols={currency_to}"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data["rates"][currency_to]
    return exchange_rate

def convert_currency(amount, currency_from):
    """
    Converts the given amount from the given currency to the target currency defined in CURRENCY constant.
    """
    exchange_rate = get_exchange_rate(currency_from, CURRENCY)
    converted_amount = amount * exchange_rate
    return converted_amount

def get_available_airports():
    """
    Retrieves a dictionary of all available airports from the Skyscanner API, with IATA codes as keys.
    """
    url = "https://skyscanner-api.p.rapidapi.com/apiservices/reference/v1.0/airports"
    headers = {
        "X-RapidAPI-Key": "c3740eeb62mshda375eb7383032dp1af6f5jsn553327cd3e8e",
        "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
    }
    params = {
        "country": "US",
        "currency": "USD",
        "locale": "en-US"
    }
    response = requests.get(url, headers=headers, params=params)
    airports = response.json()["Airports"]
    airport_dict = {airport["IataCode"]: airport for airport in airports}
    return airport_dict

def get_airports_by_country(country):
    """
    Retrieves a list of all airports in the given country from the dictionary.
    """
    airports = []
    for code, airport in AIRPORTS.items():
        if airport["CountryName"] == country:
            airports.append(airport["Name"])
    return airports

def get_airports_by_city(city):
    """
    Retrieves a list of all airports in the given city from the dictionary.
    """
    airports = []
    for code, airport in AIRPORTS.items():
        if airport["CityName"] == city:
            airports.append(airport["Name"])
    return airports

def display_airports_and_cities(user_input):
    """
    Displays a dropdown list of available airports and cities based on user input.
    """
    if user_input.lower() == "country":
        countries = set([airport["CountryName"] for airport in AIRPORTS.values()])
        countries_list = list(countries)
        countries_list.sort()
        print("Available countries:")
        for country in countries_list:
            print(country)
    elif user_input.lower() == "city":
        cities = set([airport["CityName"] for airport in AIRPORTS.values()])
        cities_list = list(cities)
        cities_list.sort()
        print("Available cities:")
        for city in cities_list:
            print(city)
    else:
        print("Invalid input. Please enter 'country' or 'city'.")

@app.route('/', methods=['GET', 'POST'])
def search_flights(departure_airport, destination_airport, nights, adults):
    """
    Searches for the cheapest flights available from departure_airport to destination_airport and back to departure_airport
    while spending the given number of nights at the destination.

    Args:
        departure_airport (str): The IATA code of the departure airport.
        destination_airport (str): The IATA code of the destination airport.
        nights (int): The number of nights to spend at the destination.
        adults (int): The number of adults traveling.

    Returns:
        list: A list of dictionaries containing detailed information about the 10 cheapest flights available.
    """
    if request.method == 'POST':
    # Retrieve the user input from the form
    departure = sanitize_input(request.form['departure'])
    destination = sanitize_input(request.form['destination'])
    nights = int(request.form['nights'])
    adults = int(request.form['adults'])
    
    # TODO: Implement flight search and display results
        
    # Render the search form template
    return render_template('search_flights.html')

def display_flight_information():
    departure = input("Enter departure airport: ")
    departure = sanitize_input(departure)
    destination = input("Enter destination airport: ")
    destination = sanitize_input(destination)
    nights = input("Enter number of nights at destination: ")
    try:
        nights = int(nights)
        if nights < 1 or nights > MAX_NIGHTS:
            raise ValueError
    except ValueError:
        print(f"Invalid input: {nights}. Number of nights must be a positive integer not greater than {MAX_NIGHTS}.")
        return
    adults = input("Enter number of adults: ")
    try:
        adults = int(adults)
        if adults < 1 or adults > MAX_ADULTS:
            raise ValueError
    except ValueError:
        print(f"Invalid input: {adults}. Number of adults must be a positive integer not greater than {MAX_ADULTS}.")
        return
    print("Searching for flights...")

    # TODO: Implement flight search and display of results

def get_flight_prices(departure, destination, departure_date, return_date):
    cache_key = f"{departure}_{destination}_{departure_date}_{return_date}"
    cache_data = _get_cached_data(cache_key)
    if cache_data is not None:
        return cache_data

    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/"
    headers = {
        "X-RapidAPI-Key": "c3740eeb62mshda375eb7383032dp1af6f5jsn553327cd3e8e",
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }
    params = {
        "originplace": departure + "-sky",
        "destinationplace": destination + "-sky",
        "outbounddate": departure_date.strftime("%Y-%m-%d"),
        "inbounddate": return_date.strftime("%Y-%m-%d"),
        "adults": 1,
        "currency": "USD",
        "locale": "en-US"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    prices = []
    for route in data["Routes"]:
        if len(route["QuoteIds"]) > 0:
            quote_id = route["QuoteIds"][0]
            for quote in data["Quotes"]:
                if quote["QuoteId"] == quote_id:
                    prices.append(quote["MinPrice"])
                    break

    _cache_data(cache_key, prices)
    return prices

def calculate_cheapest_flights(departure, destination, departure_date, return_date, nights):
    prices = get_flight_prices(departure, destination, departure_date, return_date)
    cheapest_price = min(prices)

    total_price = cheapest_price * 2 + nights * 50
    return total_price


def _get_cached_data(cache_key):
    # implementation of getting cached data from a cache store
    cache = {}
    if cache_key in cache:
        return cache[cache_key]
    else:
        return None


def _cache_data(cache_key, data):
    # implementation of caching data in a cache store
    cache = {}
    cache[cache_key] = data

booking_headers = {
    "X-RapidAPI-Key": "c3740eeb62mshda375eb7383032dp1af6f5jsn553327cd3e8e",
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}

def get_lodging_cost(city, headers):
    """
    Retrieves the average lodging cost per night per person in the given city from the booking.com API.
    """
    url = "https://booking-com.p.rapidapi.com/v1/metadata/exchange-rates"
    params = {
        "city_name": city,
        "currency_code": "USD"
    }
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    if "hotels_prices" not in response_json:
        return None
    prices = [float(hotel["price"]["price_in_user_currency"]) for hotel in response_json["hotels_prices"]]
    if not prices:
        return None
    return sum(prices) / len(prices)

def display_flights(flight_prices):
    """
    Displays the given list of flight prices in the GUI.
    """
    root = tk.Tk()
    root.title("Flight Prices")
    for itinerary in flight_prices:
        price = itinerary["PricingOptions"][0]["Price"]
        outbound_carrier = itinerary["OutboundLeg"]["CarrierIds"][0]
        inbound_carrier = itinerary["InboundLeg"]["CarrierIds"][0]
        outbound_time = itinerary["OutboundLeg"]["Departure"]
        inbound_time = itinerary["InboundLeg"]["Departure"]
        tk.Label(root, text=f"Price: {price} USD\nOutbound: {outbound_carrier} at {outbound_time}\nInbound: {inbound_carrier} at {inbound_time}").pack()
    root.mainloop()

def main():
    # Initialize GUI
    # TODO: Implement GUI initialization

    # Retrieve available airports
    available_airports = get_available_airports()

    # Main event loop
    while True:
        # Wait for user to input departure airport
        departure_airport = gui.wait_for_departure_airport_input(available_airports)

        # Wait for user to input destination airport
        destination_airport = gui.wait_for_destination_airport_input(available_airports)

        # Wait for user to input departure date
        departure_date = gui.wait_for_departure_date_input()

        # Wait for user to input return date
        return_date = gui.wait_for_return_date_input(departure_date, MAX_NIGHTS)

        # Wait for user to input number of adults
        adults = gui.wait_for_adults_input(MAX_ADULTS)

        # Retrieve flight prices
        flight_prices = get_flight_prices(departure_airport, destination_airport, departure_date, return_date, adults)

        # Display flight prices
        display_flights(flight_prices)

        # Retrieve lodging cost
        lodging_cost = get_lodging_cost(destination_airport.city)

        # Display lodging cost
        gui.display_lodging_cost(lodging_cost)
