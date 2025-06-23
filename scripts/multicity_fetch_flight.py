from dotenv import load_dotenv
import os
import requests
import json
import sqlite3
from datetime import datetime, timedelta

load_dotenv()

class FlightDatabase:
    def __init__(self, db_path="flight_offers.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id TEXT,
                offer_id TEXT,
                origin TEXT,
                destination TEXT,
                departure_date DATE,
                total_price REAL,
                currency TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flight_segments1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER,
                carrier_code TEXT,
                flight_number TEXT,
                departure_iata TEXT,
                arrival_iata TEXT,
                departure_time TIMESTAMP,
                arrival_time TIMESTAMP,
                segment_order INTEGER,
                FOREIGN KEY (flight_id) REFERENCES flights1 (id)
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database initialized: {self.db_path}")

    def store_flight_offers(self, offers, search_params):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        search_id = f"{search_params['search_type']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        stored_count = 0

        for offer in offers:
            itinerary = offer['itineraries'][0] if offer['itineraries'] else None
            if not itinerary:
                continue

            first_segment = itinerary['segments'][0]
            last_segment = itinerary['segments'][-1]

            cursor.execute('''
                INSERT INTO flights1 (search_id, offer_id, origin, destination, departure_date, total_price, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                search_id,
                offer['id'],
                first_segment['departure']['iataCode'],
                last_segment['arrival']['iataCode'],
                first_segment['departure']['at'].split('T')[0],
                float(offer['price']['total']),
                offer['price']['currency']
            ))

            flight_id = cursor.lastrowid

            for itinerary in offer['itineraries']:
                for segment_order, segment in enumerate(itinerary['segments'], 1):
                    cursor.execute('''
                        INSERT INTO flight_segments1 (
                            flight_id, carrier_code, flight_number, departure_iata, 
                            arrival_iata, departure_time, arrival_time, segment_order
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        flight_id,
                        segment['carrierCode'],
                        segment['number'],
                        segment['departure']['iataCode'],
                        segment['arrival']['iataCode'],
                        segment['departure']['at'],
                        segment['arrival']['at'],
                        segment_order
                    ))

            stored_count += 1

        conn.commit()
        conn.close()
        print(f"Stored {stored_count} flight offers in database")
        return stored_count

class AmadeusFlightSearch:
    def __init__(self, db_path="flight_offers.db"):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.base_url = "https://test.api.amadeus.com"
        self.access_token = None
        self.db = FlightDatabase(db_path)

    def get_access_token(self):
        auth_url = f"{self.base_url}/v1/security/oauth2/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = requests.post(auth_url, data=auth_data)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            print("Authentication successful!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False

    def search_flights(self, origin, destination, departure_date, adults=1):
        if not self.access_token and not self.get_access_token():
            return None

        url = f"{self.base_url}/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "max": 5
        }

        try:
            print(f"Searching direct flight: {origin} to {destination} on {departure_date}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Direct flight search failed: {e}")
            return None

    def search_multi_city(self, segments, adults=1):
        if not self.access_token and not self.get_access_token():
            return None

        url = f"{self.base_url}/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        formatted_segments = [
            {
                "id": seg["id"],
                "originLocationCode": seg["originLocationCode"],
                "destinationLocationCode": seg["destinationLocationCode"],
                "departureDateTimeRange": {
                    "date": seg["departureDate"]
                }
            }
            for seg in segments
        ]

        body = {
            "currencyCode": "USD",
            "originDestinations": formatted_segments,
            "travelers": [{"id": "1", "travelerType": "ADULT"}],
            "sources": ["GDS"]
        }

        try:
            print(f"Searching multi-city trip with {len(segments)} legs")
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Multi-city search failed: {e}")
            print(response.text)
            return None

    def search_and_store_multi_city(self, segments):
        results = self.search_multi_city(segments)
        if not results or 'data' not in results:
            print("No flight data to store (multi-city)")
            return None, 0

        search_params = {
            'search_type': 'multi-city'
        }

        stored_count = self.db.store_flight_offers(results['data'], search_params)
        return results, stored_count

    def search_and_store_flights(self, origin, destination, departure_date, adults=1):
        results = self.search_flights(origin, destination, departure_date, adults)
        if not results or 'data' not in results:
            print("No flight data to store (direct)")
            return None, 0

        search_params = {
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'adults': adults,
            'search_type': 'direct'
        }

        stored_count = self.db.store_flight_offers(results['data'], search_params)
        return results, stored_count

def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

def main():
    searcher = AmadeusFlightSearch()

    # Direct flight search
    routes = [("BOS", "SFO"), ("JFK", "LAX"), ("ORD", "SEA")]
    dates = generate_dates("2025-08-01", "2025-08-03")

    for origin, destination in routes:
        for date in dates:
            searcher.search_and_store_flights(origin, destination, date)

    # Multi-city search example
    segments = [
        {"id": "1", "originLocationCode": "BOS", "destinationLocationCode": "LAX", "departureDate": "2025-08-01"},
        {"id": "2", "originLocationCode": "LAX", "destinationLocationCode": "SEA", "departureDate": "2025-08-05"}
    ]

    searcher.search_and_store_multi_city(segments)

if __name__ == "__main__":
    main()
