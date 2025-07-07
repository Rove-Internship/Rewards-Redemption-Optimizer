from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

class ValueCalculator:
    def __init__(self, db_path="flight_offers.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def calculate_value_per_mile(self, cash_price, miles_used, fees):
        if miles_used == 0:
            return 0.0
        total_cost = fees if fees is not None else 0.0
        value_per_mile = (cash_price - total_cost) / miles_used
        return round(value_per_mile, 4)

    def get_all_redemptions(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, origin, destination, total_price, miles_used, fees 
            FROM flights1 
            WHERE miles_used IS NOT NULL AND miles_used > 0
        ''')
        results = cursor.fetchall()
        conn.close()
        return results

    def show_redemption_values(self):
        redemptions = self.get_all_redemptions()
        if not redemptions:
            print("No redemption data found.")
            return

        print("\nRedemption Value (cents per mile):")
        print("-" * 60)
        for r in redemptions:
            flight_id, origin, destination, price, miles, fees = r
            value = self.calculate_value_per_mile(price, miles, fees)
            print(f"Flight ID: {flight_id} | {origin} → {destination} | Cash: ${price} | Miles: {miles} | Fees: ${fees} | Value: {value} cpm")


def main():
    calc = ValueCalculator()
    calc.show_redemption_values()

if __name__ == "__main__":
    main()
