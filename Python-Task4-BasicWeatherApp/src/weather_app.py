import os
import requests
from dotenv import load_dotenv

# -----------------------------------
# Configuration
# -----------------------------------

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
ZIP_URL = "http://api.openweathermap.org/geo/1.0/zip"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


# -----------------------------------
# Input
# -----------------------------------

def get_location():
    """Ask the user for a city name or ZIP code."""
    while True:
        location = input("\nEnter city name or ZIP code: ").strip()
        if location:
            return location
        print("Location cannot be empty. Please enter a valid city name or ZIP code.")


# -----------------------------------
# Flexible Location Disambiguation
# -----------------------------------

def resolve_location(query):
    """
    Flexibly resolve any query (numeric, postal code, city name) across 
    OpenWeather endpoints without blocking the user with artificial errors.
    """
    if not API_KEY:
        raise ValueError("API key is missing in .env file.")

    clean_query = query.strip().strip("'\"").strip()
    if not clean_query:
        raise LookupError("Location cannot be empty.")

    parts = [p.strip() for p in clean_query.split(",")]
    
    # -------------------------------------------------------------
    # 1. Attempt ZIP API Endpoint First
    # -------------------------------------------------------------
    zip_candidates = [clean_query]
    
    # If pure 5-digit number without country, add fallback candidate for Pakistan
    if len(parts) == 1 and clean_query.isdigit() and len(clean_query) == 5:
        zip_candidates.append(f"{clean_query},PK")

    for zip_param in zip_candidates:
        params = {"zip": zip_param, "appid": API_KEY}
        try:
            response = requests.get(ZIP_URL, params=params, timeout=10)
            if response.ok:
                loc = response.json()
                return loc.get("lat"), loc.get("lon"), loc.get("name"), loc.get("country", ""), ""
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            raise ConnectionError("Unable to connect to the weather service.")
        except Exception:
            pass

    # -------------------------------------------------------------
    # 2. Attempt Direct Geocoding (City/State/Region) Endpoint
    # -------------------------------------------------------------
    params = {"q": clean_query, "limit": 5, "appid": API_KEY}

    try:
        response = requests.get(GEO_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        raise TimeoutError("The geocoding service took too long to respond.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Unable to connect to the weather service.")

    if not response.ok:
        raise RuntimeError("Failed to resolve location details.")

    results = response.json()

    # Deduplicate results based on lat/lon
    unique_results = []
    seen_coords = set()
    for loc in results:
        coord_key = (round(loc.get("lat", 0), 2), round(loc.get("lon", 0), 2))
        if coord_key not in seen_coords:
            seen_coords.add(coord_key)
            unique_results.append(loc)

    results = unique_results

    # If no results found from both endpoints
# If no results found from both endpoints
    if not results:
        hint_text = f" (e.g., '{clean_query}, US')" if "," not in clean_query else ""
        raise LookupError(
            f"No matching locations or postal codes found for '{clean_query}'."
            f" Please check your spelling{hint_text}."
        )

    # Single match -> return directly
    if len(results) == 1:
        loc = results[0]
        return loc["lat"], loc["lon"], loc["name"], loc.get("country", ""), loc.get("state", "")

    # Multiple matches -> ask user to choose or skip
    print(f"\nMultiple locations found for '{clean_query}':")
    print("-" * 45)
    for index, loc in enumerate(results, start=1):
        city = loc["name"]
        state = f", {loc['state']}" if "state" in loc else ""
        country = f", {loc.get('country', '')}"
        print(f" [{index}] {city}{state}{country}")
    print(f" [0] Skip / Enter another location")
    print("-" * 45)

    while True:
        choice = input(f"Select location [0-{len(results)}]: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                raise LookupError("Location selection skipped by user.")
            if 1 <= idx <= len(results):
                loc = results[idx - 1]
                return loc["lat"], loc["lon"], loc["name"], loc.get("country", ""), loc.get("state", "")
        print(f"Invalid choice. Please enter a number between 0 and {len(results)}.")


# -----------------------------------
# Weather API Request (By Coordinates)
# -----------------------------------

def fetch_weather_by_coords(lat, lon):
    """Fetch current weather data using geographical coordinates."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        raise TimeoutError("The weather service took too long to respond.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Unable to connect to the weather service.")

    response_data = response.json()

    if response.status_code == 401:
        raise PermissionError("The API key is invalid or unauthorized.")

    if not response.ok:
        message = response_data.get("message", "The weather service returned an error.")
        raise RuntimeError(message)

    return response_data


# -----------------------------------
# Data Processing
# -----------------------------------

def parse_weather(data, selected_name, selected_country, selected_state):
    """Extract and format weather details."""
    celsius = data["main"]["temp"]
    fahrenheit = (celsius * 9 / 5) + 32

    location_str = selected_name
    if selected_state:
        location_str += f", {selected_state}"
    if selected_country:
        location_str += f", {selected_country}"

    return {
        "location": location_str,
        "temperature_c": celsius,
        "temperature_f": fahrenheit,
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


# -----------------------------------
# Display
# -----------------------------------

def display_weather(weather):
    """Display the weather report."""
    print("\n" + "=" * 45)
    print("              WEATHER REPORT")
    print("=" * 45)
    print(f"Location       : {weather['location']}")
    print(f"Weather        : {weather['description'].title()}")
    print(f"Temperature    : {weather['temperature_c']:.1f} °C")
    print(f"Temperature    : {weather['temperature_f']:.1f} °F")
    print(f"Humidity       : {weather['humidity']}%")
    print(f"Wind Speed     : {weather['wind_speed']:.1f} m/s")
    print("=" * 45)


# -----------------------------------
# Main Program
# -----------------------------------

def main():
    """Run the weather application."""
    print("=" * 45)
    print("           PYTHON WEATHER APP")
    print("=" * 45)

    while True:
        query = get_location()

        try:
            lat, lon, name, country, state = resolve_location(query)
            data = fetch_weather_by_coords(lat, lon)
            weather = parse_weather(data, name, country, state)
            display_weather(weather)

        except ValueError as error:
            print(f"\nError: {error}")
        except PermissionError as error:
            print(f"\nAPI Error: {error}")
        except LookupError as error:
            print(f"\nLocation Info: {error}")
        except TimeoutError as error:
            print(f"\nNetwork Error: {error}")
        except ConnectionError as error:
            print(f"\nNetwork Error: {error}")
        except requests.exceptions.JSONDecodeError:
            print("\nError: The weather service returned invalid data.")
        except RuntimeError as error:
            print(f"\nWeather Service Error: {error}")
        except KeyError:
            print("\nError: The weather response did not contain expected fields.")

        # Prompt to continue or exit
        while True:
            choice = input("\nWould you like to check another location? (y/n): ").strip().lower()
            if choice in ["y", "yes", "n", "no"]:
                break
            print("Invalid choice. Please enter 'y' to continue or 'n' to exit.")

        if choice in ["n", "no"]:
            print("\nThank you for using the Python Weather App.")
            break


# -----------------------------------
# Program Entry Point
# -----------------------------------

if __name__ == "__main__":
    main()