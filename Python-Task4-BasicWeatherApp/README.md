````markdown
# Basic Weather App

## Overview

A command-line weather application developed as part of the Oasis Infobyte Python Programming Internship — Task 4.

The application retrieves current weather information for a user-provided city or postal code using the OpenWeatherMap API. It resolves the requested location, retrieves its geographical coordinates, fetches current weather data, and presents the results in a clean terminal-based report.

The project emphasizes Python API integration, JSON data handling, location disambiguation, input validation, exception handling, environment-variable security, and modular program design.

## Features

- **Multi-Format Location Search:** Query weather using city names or ZIP/postal codes.
- **Location Disambiguation:** Resolves ambiguous city names by presenting an interactive selection menu.
- **Coordinate-Based Weather Fetching:** Uses precise geographical coordinates (`lat`, `lon`) for accuracy.
- **Dual Temperature Displays:** Reports temperatures simultaneously in Celsius (°C) and Fahrenheit (°F).
- **Comprehensive Weather Metrics:** Reports humidity percentage, wind speed, and weather condition descriptions.
- **Robust Error Handling:** Recovers from empty inputs, invalid locations, network timeouts, and unauthorized API keys.
- **Interactive Loop:** Supports multiple weather queries within a single application session.

## Technologies Used

- **Python 3.13**
- **Requests** — HTTP library for API communication
- **python-dotenv** — Environment variable management for security
- **OpenWeatherMap API** — Geocoding & Weather Data API
- **JSON** — Data parsing and manipulation

## Project Structure

```text
Python-Task4-BasicWeatherApp/
│
├── src/
│   └── weather_app.py
├── screenshots/
│   ├── successful_weather.png
│   ├── location_selection.png
│   └── error_handling.png
├── .gitignore
├── requirements.txt
└── README.md
```
````

> **Note:** The `.env` file and `.venv/` directory are intentionally excluded from version control to protect API credentials and environment isolation.

## Requirements

- Python 3.13 or compatible Python 3 environment
- OpenWeatherMap API key (Free Tier)
- Active Internet connection

## Installation

1. **Create a virtual environment:**

```powershell
py -3.13 -m venv .venv

```

2. **Activate the environment:**

```powershell
.\.venv\Scripts\Activate.ps1

```

3. **Install dependencies:**

```powershell
pip install -r requirements.txt

```

## API Key Configuration

The application loads credentials from an environment configuration file:

1. Create a file named `.env` in the root folder (`Python-Task4-BasicWeatherApp/`).
2. Add your OpenWeatherMap API key:

```env
OPENWEATHER_API_KEY=your_api_key_here

```

_(Replace `your_api_key_here` with your valid key. Never commit `.env` to version control)._

## Running the Application

Execute the main application script:

```powershell
python .\src\weather_app.py

```

## Example Usage

### City Search

```text
Enter city name or ZIP code: Karachi

```

### Ambiguous City Disambiguation

When multiple locations match a query:

```text
Enter city name or ZIP code: Hyderabad

Multiple locations found for 'Hyderabad':
---------------------------------------------
 [1] Hyderabad, Telangana, IN
 [2] Hyderabad City Taluka, Sindh, PK
 ...
---------------------------------------------
Select location: 2

```

### Sample Terminal Output

```text
=============================================
              WEATHER REPORT
=============================================
Location       : Karachi, Sindh, PK
Weather        : Clear Sky
Temperature    : 38.1 °C
Temperature    : 100.6 °F
Humidity       : 37%
Wind Speed     : 3.6 m/s
=============================================

```

## Technical Architecture & Functions

- **`get_location()`**: Collects and validates user prompt input.
- **`resolve_location()`**: Connects to OpenWeather Geocoding services. Handles postal code resolving, direct geocoding fallbacks, duplicate filtering, and disambiguation prompts.
- **`fetch_weather_by_coords()`**: Queries OpenWeatherMap using resolved coordinates.
- **`parse_weather()`**: Parses JSON payloads and computes Fahrenheit values from Celsius metrics.
- **`display_weather()`**: Formats output into a standardized terminal report card.
- **`main()`**: Controls runtime execution, loop cycles, and error handling.

## Error & Edge Case Handling

- **Empty Input:** Rejects empty submissions with actionable user guidance.
- **Unknown Locations:** Traps API 404 responses gracefully without throwing unhandled exceptions.
- **Network Interruptions:** Catches `requests.exceptions.RequestException` timeouts cleanly.
- **Unauthorized API Key:** Detects invalid API keys (HTTP 401) and alerts the user to verify `.env`.
- **Selection Validation:** Validates numerical selections during city disambiguation menus.

## Learning Outcomes

This project provided practical experience with:

- REST API integration & JSON payload parsing.
- Geocoding and coordinate-based data fetching.
- Environment variable security (`.env` isolation).
- Exception handling and terminal UI formatting.
- Git configuration and secret management.

## Project Status

**Completed** — Oasis Infobyte Python Programming Internship (Task 4 - Beginner Tier).

```

```
