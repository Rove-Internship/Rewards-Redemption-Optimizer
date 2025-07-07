from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime
import statistics

load_dotenv()

class ValueCalculator:
    def __init__(self, db_path="flight_offers.db"):
        self.db_path = db_path
        self.EXCELLENT_VALUE = 2.0
        self.GOOD_VALUE = 1.5
        self.FAIR_VALUE = 1.0
        self.POOR_VALUE = 0.8

    def connect(self):
        return sqlite3.connect(self.db_path)

    def check_database_structure(self):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(flights1)")
            columns = [col[1] for col in cursor.fetchall()]
            conn.close()
            return 'miles_used' in columns and 'fees' in columns
        except sqlite3.OperationalError:
            conn.close()
            return False

    def add_sample_redemption_data(self, origin=None, destination=None):
        conn = self.connect()
        cursor = conn.cursor()

        sample_data = [
            (350, 25000, 50.0), (450, 30000, 75.0), (200, 20000, 40.0),
            (550, 35000, 100.0), (180, 15000, 30.0), (600, 40000, 125.0)
        ]

        for price, miles, fees in sample_data:
            cursor.execute("""
                INSERT INTO flights1 (origin, destination, departure_date, total_price, miles_used, fees)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (origin or "XXX", destination or "YYY", datetime.now().strftime("%Y-%m-%d"), price, miles, fees))

        conn.commit()
        conn.close()
        print(f"Added {len(sample_data)} sample flights for {origin} → {destination}")

    def show_redemption_values(self, origin=None, destination=None):
        conn = self.connect()
        cursor = conn.cursor()

        query = "SELECT id, origin, destination, total_price, miles_used, fees, departure_date FROM flights1"
        params = []
        if origin and destination:
            query += " WHERE origin = ? AND destination = ?"
            params = [origin, destination]

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        print("\nRedemption Values:")
        for row in results:
            print(f"{row[0]}: {row[1]} → {row[2]}, {row[6]}, ${row[3]:.2f}, {row[4]} miles, ${row[5]:.2f} fees")

    def get_best_redemptions(self, limit=10, min_value=1.0):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT origin, destination, total_price, miles_used, fees, departure_date FROM flights1")
        flights = cursor.fetchall()
        conn.close()

        redemptions = []
        for origin, destination, price, miles, fees, date in flights:
            if miles == 0:
                continue
            vpm = round((price - fees) / miles, 4)
            if vpm >= min_value:
                category = self.get_value_category(vpm)
                redemptions.append({'route': f"{origin} → {destination}", 'date': date,
                                    'value': vpm, 'category': category,
                                    'price': price, 'miles': miles, 'fees': fees})
        redemptions.sort(key=lambda x: x['value'], reverse=True)
        return redemptions[:limit]

    def get_value_category(self, value_per_mile):
        if value_per_mile >= self.EXCELLENT_VALUE:
            return "EXCELLENT"
        elif value_per_mile >= self.GOOD_VALUE:
            return "GOOD"
        elif value_per_mile >= self.FAIR_VALUE:
            return "FAIR"
        elif value_per_mile >= self.POOR_VALUE:
            return "POOR"
        else:
            return "AVOID"

    def get_cheapest_flights(self, origin=None, destination=None, limit=10):
        conn = self.connect()
        cursor = conn.cursor()

        query = "SELECT id, origin, destination, total_price, miles_used, fees, departure_date FROM flights1"
        params = []
        if origin and destination:
            query += " WHERE origin = ? AND destination = ?"
            params.extend([origin, destination])

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        sorted_results = sorted(results, key=lambda x: x[3])
        return sorted_results[:limit]

# ---------------- Main CLI -------------------

def main():
    calc = ValueCalculator()
    print("\n✈️  Flight Redemption Value Calculator")
    print("=" * 50)

    origin = input("Enter origin airport IATA code (or press Enter to skip): ").strip().upper() or None
    destination = input("Enter destination airport IATA code (or press Enter to skip): ").strip().upper() or None

    # Automatically add sample data if no flights exist for the route
    if not calc.get_cheapest_flights(origin, destination):
        print(f"No flights found for {origin} → {destination}. Adding sample data...")
        calc.add_sample_redemption_data(origin, destination)

    while True:
        print("\nSelect an option:")
        print("1. Show all flights' cash prices, miles, and VPM")
        print("2. Show top redemptions (best VPM)")
        print("3. Show cheapest flights")
        print("4. Add/Reset sample data")
        print("0. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            calc.show_redemption_values(origin, destination)

        elif choice == "2":
            min_value = input("Minimum value-per-mile threshold (default 1.5): ").strip()
            min_value = float(min_value) if min_value else 1.5
            best = calc.get_best_redemptions(limit=10, min_value=min_value)
            for r in best:
                print(f"{r['route']} on {r['date']}: {r['value']} cpm ({r['category']}) - ${r['price']}, {r['miles']} miles, ${r['fees']} fees")

        elif choice == "3":
            cheapest = calc.get_cheapest_flights(origin, destination)
            print("\nCheapest Flights:")
            for r in cheapest:
                print(f"{r[1]} → {r[2]}, {r[6]}, ${r[3]:.2f}, {r[4]} miles, ${r[5]:.2f} fees")

        elif choice == "4":
            calc.add_sample_redemption_data(origin, destination)

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
