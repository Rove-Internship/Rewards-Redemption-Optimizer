import sqlite3
import sys
from datetime import datetime

class FlightDataViewer:
    def __init__(self, db_path="flight_data.db"):
        self.db_path = db_path
    
    def check_database_exists(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM flights")
            flight_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM flight_segments")
            segment_count = cursor.fetchone()[0]
            
            conn.close()
            
            print(f"Database: {self.db_path}")
            print(f"Flights: {flight_count}")
            print(f"Segments: {segment_count}")
            return flight_count > 0
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def show_all_searches(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT search_id, origin, destination, departure_date, 
                   COUNT(*) as offer_count, MIN(total_price) as min_price,
                   MAX(total_price) as max_price, currency, created_at
            FROM flights 
            GROUP BY search_id 
            ORDER BY created_at DESC
        ''')
        
        searches = cursor.fetchall()
        conn.close()
        
        if not searches:
            print("No flight searches found in database")
            return
        
        print(f"\nAll Flight Searches ({len(searches)} total):")
        print("=" * 80)
        
        for search in searches:
            search_id, origin, dest, dep_date, count, min_price, max_price, currency, created = search
            print(f"{created} | {origin} → {dest} | {dep_date}")
            print(f"{count} offers | Price: {min_price}-{max_price} {currency}")
            print(f"Search ID: {search_id}")
            print("-" * 50)
    
    def show_cheapest_flights(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.origin, f.destination, f.departure_date, f.total_price, f.currency,
                   GROUP_CONCAT(fs.carrier_code || fs.flight_number) as flights,
                   f.created_at
            FROM flights f
            JOIN flight_segments fs ON f.id = fs.flight_id
            GROUP BY f.id
            ORDER BY f.total_price ASC
            LIMIT ?
        ''', (limit,))
        
        flights = cursor.fetchall()
        conn.close()
        
        if not flights:
            print("No flights found in database")
            return
        
        print(f"\nCheapest Flights (Top {len(flights)}):")
        print("=" * 60)
        
        for flight in flights:
            origin, dest, dep_date, price, currency, flight_nums, created = flight
            print(f"{origin} → {dest} | {dep_date}")
            print(f"Price: {price} {currency}")
            print(f"Flights: {flight_nums}")
            print(f"Found: {created}")
            print("-" * 40)
    
    def show_route_analysis(self, origin=None, destination=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if origin and destination:
            cursor.execute('''
                SELECT departure_date, COUNT(*) as offer_count, 
                       MIN(total_price) as min_price, MAX(total_price) as max_price,
                       AVG(total_price) as avg_price, currency
                FROM flights 
                WHERE origin = ? AND destination = ?
                GROUP BY departure_date, currency
                ORDER BY departure_date
            ''', (origin, destination))
            
            title = f"Route Analysis: {origin} → {destination}"
        else:
            cursor.execute('''
                SELECT origin, destination, COUNT(*) as searches,
                       MIN(total_price) as min_price, MAX(total_price) as max_price,
                       AVG(total_price) as avg_price, currency
                FROM flights 
                GROUP BY origin, destination, currency
                ORDER BY searches DESC, min_price ASC
            ''')
            
            title = "All Routes Analysis"
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("No route data found")
            return
        
        print(f"\n{title}:")
        print("=" * 70)
        
        for result in results:
            if origin and destination:
                dep_date, count, min_p, max_p, avg_p, currency = result
                print(f"{dep_date}: {count} offers")
                print(f"Price range: {min_p:.2f} - {max_p:.2f} {currency}")
                print(f"Average: {avg_p:.2f} {currency}")
            else:
                orig, dest, searches, min_p, max_p, avg_p, currency = result
                print(f"{orig} → {dest}: {searches} searches")
                print(f"Price range: {min_p:.2f} - {max_p:.2f} {currency}")
                print(f"Average: {avg_p:.2f} {currency}")
            print("-" * 40)
    
    def export_to_csv(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flight_data_export_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.search_id, f.offer_id, f.origin, f.destination, f.departure_date,
                   f.total_price, f.currency, f.created_at,
                   fs.carrier_code, fs.flight_number, fs.departure_iata, fs.arrival_iata,
                   fs.departure_time, fs.arrival_time, fs.segment_order
            FROM flights f
            JOIN flight_segments fs ON f.id = fs.flight_id
            ORDER BY f.created_at DESC, fs.segment_order
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            print("No data to export")
            return
        
        with open(filename, 'w') as f:
            f.write("search_id,offer_id,origin,destination,departure_date,total_price,currency,created_at,")
            f.write("carrier_code,flight_number,departure_iata,arrival_iata,departure_time,arrival_time,segment_order\n")
            
            for row in data:
                f.write(','.join(str(col) for col in row) + '\n')
        
        print(f"Exported {len(data)} records to {filename}")

def handle_command(viewer, command, args):
    if command == "searches":
        viewer.show_all_searches()
    elif command == "cheapest":
        limit = int(args[0]) if args else 10
        viewer.show_cheapest_flights(limit)
    elif command == "route":
        origin = args[0] if len(args) > 0 else None
        destination = args[1] if len(args) > 1 else None
        viewer.show_route_analysis(origin, destination)
    elif command == "export":
        filename = args[0] if args else None
        viewer.export_to_csv(filename)
    else:
        print("Unknown command. Available: searches, cheapest, route, export")

def main():
    viewer = FlightDataViewer()
    
    if not viewer.check_database_exists():
        print("No flight data found. Run fetch_flight2.py first to collect data.")
        return
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        handle_command(viewer, command, args)
    else:
        viewer.show_all_searches()
        print()
        viewer.show_cheapest_flights(5)

if __name__ == "__main__":
    main()
