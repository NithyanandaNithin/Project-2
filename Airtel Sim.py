import mysql.connector
import random
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="password",  
            database="airtel_db"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Database Error:", e)

    def fetch_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print("Fetch Error:", e)
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()
class SIMProvider:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.db = Database()

    def generate_mobile_number(self):
        return "98" + "".join(str(random.randint(0, 9)) for _ in range(8))  # Generates 10-digit number

    def add_sim(self, customer_name):
        phone_number = self.generate_mobile_number()
        query = "INSERT INTO sim_cards (phone_number, customer_name) VALUES (%s, %s)"
        self.db.execute_query(query, (phone_number, customer_name))
        print(f"SIM {phone_number} added successfully for {customer_name}.")
        return phone_number

    def view_sim(self, phone_number):
        query = "SELECT * FROM sim_cards WHERE phone_number = %s"
        result = self.db.fetch_query(query, (phone_number,))
        if result:
            for row in result:
                print(f"SIM ID: {row[0]}, Phone: {row[1]}, Customer: {row[2]}, Status: {row[3]}")
        else:
            print("SIM not found.")
            
    def delete_sim(self, phone_number):
        query = "DELETE FROM sim_cards WHERE phone_number = %s"
        self.db.execute_query(query, (phone_number,))
        print(f"SIM {phone_number} deleted successfully.")

class AirtelSIM(SIMProvider):
    def __init__(self):
        super().__init__("Airtel")

    def activate_sim(self, phone_number):
        query = "UPDATE sim_cards SET status = 'Active' WHERE phone_number = %s"
        self.db.execute_query(query, (phone_number,))
        print(f"SIM {phone_number} activated.")

    def deactivate_sim(self, phone_number):
        query = "UPDATE sim_cards SET status = 'Inactive' WHERE phone_number = %s"
        self.db.execute_query(query, (phone_number,))
        print(f"SIM {phone_number} deactivated.")

if __name__ == "__main__":
    airtel = AirtelSIM()
  
    new_number = airtel.add_sim("John Doe")
    
    airtel.activate_sim(new_number)
    
    airtel.view_sim(new_number)
    
    airtel.deactivate_sim(new_number)
    
    airtel.delete_sim(new_number)