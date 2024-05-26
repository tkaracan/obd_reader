def kmh_to_mph(speed_kmh, time_minutes, distance_km):
    # Convert speed from km/h to mph
    speed_mph = int(speed_kmh * 0.621371)

    # Convert time from minutes to hours
    time_hours = time_minutes / 60.0

    # Convert distance from kilometers to miles
    distance_miles = distance_km * 0.621371

    # Calculate average speed in mph
    if time_hours > 0:
        avg_speed_mph = distance_miles / time_hours
    else:
        avg_speed_mph = 0  # Avoid division by zero

    return {
        "Speed": speed_mph,
        "Total Time": f"{time_minutes:.2f} min",
        "Total Miles": f"{distance_miles:.2f} mil",
        "av Speed": f"{avg_speed_mph:.2f} mph"
    }


def celsius_to_fahrenheit(temp_c):
    return (temp_c * 9 / 5) + 32


def percent(value, mini, maxi):
    if maxi == mini:
        return 0  # Avoid division by zero if min and max are the same
    percentage = ((value - mini) / (maxi - mini)) * 100
    return percentage  # Placeholder for more complex conversions if needed


def rpm_to_rpm(value):
    return value  # Direct conversion, adjust if necessary


def fuel_level_to_percent(fuel_level):
    x = {"AHMET:": "BOKLA", "KIC:": "33", "NABER:": "34276"}
    return x


def calculate_distance(value):
    # return value - 16786 + 228510.7
    return value


def dict_test(value):
    x = {"AHMET:": "BOKLA", "KIC:": "33", "NABER:": "34276"}
    return x


# Additional conversion functions can be defined here as needed.
# data_calculations.py

def calculate_mpg(distance_km, percentage_at_start, percentage_now, total_fuel_capacity_liters=127):
    if percentage_at_start == 0 or percentage_now == 0 or total_fuel_capacity_liters == 0:
        return 0  # Avoid division by zero or undefined behavior
    fuel_used_liters = total_fuel_capacity_liters * ((percentage_at_start - percentage_now) / 100)
    miles_traveled = distance_km / 1.609  # Convert kilometers to miles
    gallons_used = fuel_used_liters / 3.785  # Convert liters to gallons
    if gallons_used == 0:
        return float('inf')  # Avoid division by zero, return infinite MPG

    mpg = miles_traveled / gallons_used

    return {"MPG": f"{mpg:.2f}", "Fuel Left": f"%{percentage_now:.2f}", "Fuel Used": f"{gallons_used:.2f} gal"}