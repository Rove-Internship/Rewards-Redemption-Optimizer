# Rewards-Redemption-Optimizer

**Usage:**
First run
`python scripts/fetch_flight2.py`
Then
`python scripts/view_flight_data.py`


# Flight Data Collector and Analyzer

This project retrieves and stores flight offer data using the **Amadeus Flight Offers Search API**, storing structured results in a local SQLite database.

---

## Project Files

### `fetch_flight.py`

Main script for fetching flight data:

* `AmadeusFlightSearch`: Connects to the Amadeus API, fetches flight data
* `FlightDatabase`: Initializes and writes to `flight_data.db`
* Iterates over **3 routes**:

  * BOS → SFO
  * JFK → LAX
  * ORD → SEA
* Pulls flights for **each day in August 2025**
* Stores all flight offers and their segments in a local database
* Run `python scripts/fetch_flight2.py`

### `view_flight_data.py`

Command-line tool for exploring stored flight data. Functionality includes:

* Displaying all previous searches
* Showing the cheapest flights by price
* Summarizing route-based statistics (min, max, avg price)
* Exporting full flight segment data to a CSV
* Run `python scripts/view_flight_data.py`

---

## Database 

Saved to: `flight_data.db`

### Table: `flights`

| Column           | Description                     |
| ---------------- | ------------------------------- |
| `search_id`      | Unique identifier for a search  |
| `origin`         | Origin airport (IATA code)      |
| `destination`    | Destination airport (IATA code) |
| `departure_date` | Date of departure               |
| `total_price`    | Total fare price (in currency)  |
| `currency`       | Currency (e.g. USD)             |

### Table: `flight_segments`

Each flight offer can include multiple segments (e.g., layovers).

| Column                           | Description                |
| -------------------------------- | -------------------------- |
| `flight_id`                      | Foreign key from `flights` |
| `carrier_code`                   | Airline code (e.g. AA, DL) |
| `flight_number`                  | Specific flight number     |
| `departure_iata`, `arrival_iata` | Airports                   |
| `departure_time`, `arrival_time` | ISO timestamps             |
| `segment_order`                  | Position in itinerary      |

