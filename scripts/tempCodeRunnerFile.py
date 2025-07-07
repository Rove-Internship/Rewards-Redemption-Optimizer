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

    def add_sample_redemption_data(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(flights1)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'miles_used' not in columns:
            cursor.execute("ALTER TABLE flights1 ADD COLUMN miles_used INTEGER DEFAULT 0")
        if 'fees' not in columns:
            cursor.execute("ALTER TABLE flights1 ADD COLUMN fees REAL DEFAULT 0.0")

        cursor.execute("SELECT id, total_price FROM flights1 WHERE miles_used IS NULL OR miles_used = 0 LIMIT 15")
        flights = cursor.fetchall()

        sample_redemptions = [
            (25000, 50.0), (30000, 75.0), (20000, 40.0), (35000, 100.0), (15000, 30.0),
            (40000, 125.0), (18000, 45.0), (22000, 55.0), (28000, 70.0), (12000, 25.0),
            (32000, 80.0), (16000, 35.0), (38000, 95.0), (14000, 30.0), (26000, 65.0),
        ]

        for i, (flight_id, price) in enumerate(flights):
            if i < len(sample_redemptions):
                miles, fees = sample_redemptions[i]
                scaled_price = max(price * 3, 300)
                cursor.execute("""
                    UPDATE flights1
                    SET total_price = ?, miles_used = ?, fees = ?
                    WHERE id = ?
                """, (scaled_price, miles, fees, flight_id))

        conn.commit()
        conn.close()
        print(f"Added sample redemption data to {len(flights)} flights.")

    def calculate_value_per_mile(self, cash_price, miles_used, fees, method="standard"):
        if miles_used == 0:
            return 0.0
        total_cost = fees if fees is not None else 0.0

        if method == "standard":
            return round((cash_price - total_cost) / miles_used, 4)
        elif method == "opportunity_cost":
            miles_earned = cash_price * 0.01
            net_miles = miles_used - miles_earned
            return round((cash_price - total_cost) / net_miles if net_miles > 0 else 0, 4)
        elif method == "conservative":
            net_savings = cash_price - total_cost - (miles_used * 0.01)
            return round(net_savings / miles_used if miles_used > 0 else 0, 4)
        else:
            raise ValueError(f"Unknown calculation method: {method}")

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

    def get_all_redemptions(self):
        if not self.check_database_structure():
            print("Database missing data. Adding sample data...")
            self.add_sample_redemption_data()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, origin, destination, total_price, miles_used, fees, departure_date, created_at
            FROM flights1
            WHERE miles_used IS NOT NULL AND miles_used > 0
        ''')
        results = cursor.fetchall()
        conn.close()
        return results

    def analyze_route_values(self, origin, destination):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT departure_date, total_price, miles_used, fees, created_at
            FROM flights1
            WHERE origin = ? AND destination = ?
            AND miles_used IS NOT NULL AND miles_used > 0
            ORDER BY departure_date
        ''', (origin, destination))
        redemptions = cursor.fetchall()
        conn.close()

        if not redemptions:
            return None

        values = [{
            'date': dep_date,
            'value': self.calculate_value_per_mile(price, miles, fees),
            'category': self.get_value_category(self.calculate_value_per_mile(price, miles, fees)),
            'price': price,
            'miles': miles,
            'fees': fees,
            'created': created
        } for dep_date, price, miles, fees, created in redemptions]

        return {
            'route': f"{origin} → {destination}",
            'redemptions': values,
            'avg_value': statistics.mean([v['value'] for v in values]),
            'min_value': min([v['value'] for v in values]),
            'max_value': max([v['value'] for v in values]),
            'count': len(values)
        }

    def get_best_redemptions(self, limit=10, min_value=1.0):
        redemptions = self.get_all_redemptions()
        best = []
        for r in redemptions:
            flight_id, origin, destination, price, miles, fees, dep_date, created = r
            value = self.calculate_value_per_mile(price, miles, fees)
            if value >= min_value:
                best.append({
                    'flight_id': flight_id,
                    'route': f"{origin} → {destination}",
                    'date': dep_date,
                    'value': value,
                    'category': self.get_value_category(value),
                    'price': price,
                    'miles': miles,
                    'fees': fees,
                    'created': created
                })
        best.sort(key=lambda x: x['value'], reverse=True)
        return best[:limit]

    def show_redemption_values(self, method="standard"):
        redemptions = self.get_all_redemptions()
        print(f"\nRedemption Values ({method.upper()}):")
        for r in redemptions:
            flight_id, origin, destination, price, miles, fees, dep_date, created = r
            value = self.calculate_value_per_mile(price, miles, fees, method)
            category = self.get_value_category(value)
            print(f"{flight_id}: {origin} → {destination}, {dep_date}, ${price}, {miles} miles, ${fees} fees → {value:.4f} cpm ({category})")

    def show_route_analysis(self, origin, destination):
        analysis = self.analyze_route_values(origin, destination)
        if not analysis:
            print(f"No data for {origin} → {destination}")
            return
        print(f"\nRoute Analysis for {analysis['route']}")
        print(f"Total: {analysis['count']}, Avg: {analysis['avg_value']:.4f} cpm, Range: {analysis['min_value']:.4f}-{analysis['max_value']:.4f}")
        for redemption in analysis['redemptions']:
            print(f"{redemption['date']}: {redemption['value']:.4f} cpm ({redemption['category']})")

    def show_best_redemptions(self, limit=10, min_value=1.0):
        best = self.get_best_redemptions(limit, min_value)
        if not best:
            print("No high-value redemptions found.")
            return
        print("\nBest Redemptions:")
        for r in best:
            print(f"{r['route']} on {r['date']}: {r['value']} cpm ({r['category']}) - ${r['price']}, {r['miles']} miles, ${r['fees']} fees")

    def export_value_analysis(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"value_analysis_{timestamp}.csv"
        redemptions = self.get_all_redemptions()
        with open(filename, 'w') as f:
            f.write("flight_id,origin,destination,date,cash_price,miles_used,fees,value\n")
            for r in redemptions:
                flight_id, origin, destination, price, miles, fees, dep_date, created = r
                value = self.calculate_value_per_mile(price, miles, fees)
                f.write(f"{flight_id},{origin},{destination},{dep_date},{price},{miles},{fees},{value:.4f}\n")
        print(f"Exported to {filename}")
        return filename

# ---------------- Main CLI -------------------

def main():
    calc = ValueCalculator()
    print("\n✈️  Flight Redemption Value Calculator")
    print("=" * 50)

    origin = input("Enter origin airport IATA code (e.g., JFK): ").strip().upper()
    destination = input("Enter destination airport IATA code (e.g., LAX): ").strip().upper()

    while True:
        print("\nSelect an option:")
        print("1. Show all redemption values")
        print("2. Show best redemptions")
        print("3. Analyze this route")
        print("4. Export data to CSV")
        print("0. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            calc.show_redemption_values()
        elif choice == "2":
            min_value = input("Minimum value-per-mile threshold (default 1.5): ").strip()
            min_value = float(min_value) if min_value else 1.5
            calc.show_best_redemptions(limit=10, min_value=min_value)
        elif choice == "3":
            calc.show_route_analysis(origin, destination)
        elif choice == "4":
            calc.export_value_analysis()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
