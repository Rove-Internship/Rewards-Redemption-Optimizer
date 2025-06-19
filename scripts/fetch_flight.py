from amadeus import Client, ResponseError


amadeus = Client(
    client_id="WHSpTTK3EtNGKQwYGFXPK18HQAeEqoXT",
    client_secret="YvNIWVDtJb1AKlVS"
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='JFK',
        destinationLocationCode='LAX',
        departureDate='2025-06-25', 
        adults=1
    )

    for offer in response.data:
        price = offer['price']['total']
        airline = offer['validatingAirlineCodes'][0]
        itinerary = offer['itineraries'][0]
        segments = itinerary['segments']
        print(f"Airline: {airline} | Price: ${price}")
        for seg in segments:
            print(f"  {seg['departure']['iataCode']} → {seg['arrival']['iataCode']} at {seg['departure']['at']}")

except ResponseError as error:
    print("API Error:", error)
