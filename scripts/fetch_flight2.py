from dotenv import load_dotenv
import os
import requests
import json

# Load .env file
load_dotenv()

'''
This script fetches flight offers from the Amadeus API using direct API calls. unlike `flight.py` which uses the Amadeus Python SDK.
'''

class AmadeusFlightSearch:
    def __init__(self):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.base_url = "https://test.api.amadeus.com"
        self.access_token = None
        
    def get_access_token(self):
        """Get access token for API authentication"""
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
        """Search for flights using direct API call"""
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
            "max": 5  # Limit to 5 results for cleaner output
        }
        
        try:
            print(f" Searching flights from {origin} to {destination} on {departure_date}...")
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f" Flight search failed: {e}")
            return None

def main():
    # Check credentials
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print(" Missing API credentials. Please check .env file.")
        return
    
    # Initialize flight search
    flight_search = AmadeusFlightSearch()
    
    # Search for flights
    results = flight_search.search_flights(
        origin='JFK',
        destination='LAX', 
        departure_date='2025-06-25',
        adults=1
    )
    
    if not results or 'data' not in results:
        print(" No flight data received")
        return
    
    # Display results
    offers = results['data']
    print(f"\n Found {len(offers)} flight offers:")
    print("=" * 50)
    
    for i, offer in enumerate(offers, 1):
        price = offer['price']['total']
        currency = offer['price']['currency']
        
        print(f"\n Offer {i}: {price} {currency}")
        
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

if __name__ == "__main__":
    main()
