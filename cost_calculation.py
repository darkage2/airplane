def calculate_trip_cost(flight_route, nights, adults, local_data):
    departure_cost, return_cost = get_flight_prices(flight_route, local_data)
    accommodation_cost = get_accommodation_cost(flight_route, nights, adults, local_data)

    total_cost = (departure_cost + return_cost) * adults + accommodation_cost
    return total_cost

def get_flight_prices(flight_route, local_data):
    # Extract flight prices for departure and return flights from local_data
    pass

def get_accommodation_cost(flight_route, nights, adults, local_data):
    # Extract the average accommodation cost per night per person at the destination city
    pass
