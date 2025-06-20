from dotenv import load_dotenv
import os
import requests
import json
import sqlite3
from datetime import datetime

load_dotenv()

class FlightDatabase:
    def __init__(self, db_path="flight_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
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
            CREATE TABLE IF NOT EXISTS flight_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER,
                carrier_code TEXT,
                flight_number TEXT,
                departure_iata TEXT,
                arrival_iata TEXT,
                departure_time TIMESTAMP,
                arrival_time TIMESTAMP,
                segment_order INTEGER,
                FOREIGN KEY (flight_id) REFERENCES flights (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized: {self.db_path}")
    
    def store_flight_offers(self, offers, search_params):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_id = f"{search_params['origin']}-{search_params['destination']}-{search_params['departure_date']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        stored_count = 0
        
        for offer in offers:
            cursor.execute('''
                INSERT INTO flights (search_id, offer_id, origin, destination, departure_date, total_price, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                search_id,
                offer['id'],
                search_params['origin'],
                search_params['destination'],
                search_params['departure_date'],
                float(offer['price']['total']),
                offer['price']['currency']
            ))
            
            flight_id = cursor.lastrowid
            
            for itinerary in offer['itineraries']:
                for segment_order, segment in enumerate(itinerary['segments'], 1):
                    cursor.execute('''
                        INSERT INTO flight_segments (
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
    
    def get_recent_searches(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT search_id, origin, destination, departure_date, 
                   COUNT(*) as offer_count, MIN(total_price) as min_price,
                   MAX(total_price) as max_price, currency, created_at
            FROM flights 
            GROUP BY search_id 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_flights_by_route(self, origin, destination, limit=20):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, fs.carrier_code, fs.flight_number, fs.departure_iata, 
                   fs.arrival_iata, fs.departure_time, fs.arrival_time
            FROM flights f
            JOIN flight_segments fs ON f.id = fs.flight_id
            WHERE f.origin = ? AND f.destination = ?
            ORDER BY f.created_at DESC, fs.segment_order
            LIMIT ?
        ''', (origin, destination, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_cheapest_flights(self, origin=None, destination=None, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT origin, destination, departure_date, MIN(total_price) as min_price, 
                   currency, COUNT(*) as offer_count, created_at
            FROM flights 
        '''
        params = []
        
        if origin and destination:
            query += ' WHERE origin = ? AND destination = ?'
            params.extend([origin, destination])
        elif origin:
            query += ' WHERE origin = ?'
            params.append(origin)
        elif destination:
            query += ' WHERE destination = ?'
            params.append(destination)
        
        query += '''
            GROUP BY origin, destination, departure_date 
            ORDER BY min_price ASC 
            LIMIT ?
        '''
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

class AmadeusFlightSearch:
    def __init__(self, db_path="flight_data.db"):
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
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            print("Authentication successful!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f" Authentication failed: {e}")
            return False
    
    def search_flights(self, origin, destination, departure_date, adults=1):
        if not self.access_token and not self.get_access_token():
            return None
        
        search_url = f"{self.base_url}/v2/shopping/flight-offers"
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
            print(f"Searching flights from {origin} to {destination} on {departure_date}...")
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Flight search failed: {e}")
            return None
    
    def search_and_store_flights(self, origin, destination, departure_date, adults=1):
        search_params = {
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'adults': adults
        }
        
        results = self.search_flights(origin, destination, departure_date, adults)
        
        if not results or 'data' not in results:
            print("No flight data to store")
            return None, 0
        
        stored_count = self.db.store_flight_offers(results['data'], search_params)
        
        return results, stored_count

def main():
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Missing API credentials. Please check .env file.")
        return
    
    flight_search = AmadeusFlightSearch()
    
    results, _ = flight_search.search_and_store_flights(
        origin='BOS',
        destination='SFO', 
        departure_date='2025-08-01',
        adults=1
    )
    
    if not results or 'data' not in results:
        print("No flight data received")
        return
    
    offers = results['data']
    print(f"\nFound {len(offers)} flight offers:")
    print("=" * 50)
    
    for i, offer in enumerate(offers, 1):
        price = offer['price']['total']
        currency = offer['price']['currency']
        
        print(f"\nOffer {i}: {price} {currency}")
        
        for itinerary in offer['itineraries']:
            segments = itinerary['segments']
            
            for segment in segments:
                dep_code = segment['departure']['iataCode']
                arr_code = segment['arrival']['iataCode']
                dep_time = segment['departure']['at']
                arr_time = segment['arrival']['at']
                airline = segment['carrierCode']
                flight_num = segment['number']
                
                print(f"  {airline}{flight_num}: {dep_code} → {arr_code}")
                print(f"  Departure: {dep_time} | Arrival: {arr_time}")
        
        print("-" * 30)
    
    print("\nRecent searches from database:")
    print("=" * 50)
    recent_searches = flight_search.db.get_recent_searches(5)
    
    for search in recent_searches:
        _, origin, destination, dep_date, offer_count, min_price, max_price, currency, created_at = search
        print(f"{created_at}: {origin} → {destination} on {dep_date}")
        print(f"{offer_count} offers found | Price range: {min_price}-{max_price} {currency}")
        print("-" * 30)

if __name__ == "__main__":
    main()
