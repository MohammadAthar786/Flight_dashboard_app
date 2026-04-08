import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv("Credentials.env")
class DB:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                
                
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=int(os.getenv("DB_PORT")),
                database=os.getenv("DB_NAME"),
            )
            

            self.mycursor = self.conn.cursor()
            print("Connection established")

        except Exception as e:
            print("Connection error:", e)

    def fetch_city_names(self):
        city=[]
        cursor=self.conn.cursor()
        cursor.execute("""
            SELECT source FROM flights_data
            UNION
            SELECT destination FROM flights_data
        """)
        
        data = cursor.fetchall()

        # convert list of tuples → list
        for i in data:
            city.append(i[0])
        cursor.close()
        return city
    def fetch_all_flights(self,source,destination):
        cursor=self.conn.cursor()
        cursor.execute("""
                              SELECT Airline,Date_of_Journey,Route,Dep_Time,Duration,Price  from flights_data
                             WHERE Source='{}' AND Destination='{}'

                              
                              """.format(source,destination))
        data=cursor.fetchall()
        cursor.close()
        return data
    def fetch_airlines(self ):
        airlines=[]
        frequency=[]
        cursor=self.conn.cursor()
        cursor.execute("""        
               SELECT Airline,COUNT(*) from flights_data
               GROUP BY Airline;
                              
                              """)
        data=cursor.fetchall()
        for item in data:
            airlines.append(item[0])
            frequency.append(item[1])
        cursor.close()
        return airlines,frequency
    
    def busiest_airport(self):
        airport = []
        traffic = []
        cursor = self.conn.cursor()  # fresh cursor each time
        cursor.execute("""
            SELECT airport, COUNT(*) as traffic
            FROM (
                SELECT source AS airport FROM flights_data
                UNION ALL
                SELECT destination AS airport FROM flights_data
            ) t
            GROUP BY airport
            ORDER BY traffic DESC
            LIMIT 10
        """)
        data = cursor.fetchall()
        for item in data:
            airport.append(item[0])
            traffic.append(item[1])
        cursor.close()
        return airport, traffic
    def daily_number_of_flights(self):
        date=[]
        flights_count=[]
        cursor=self.conn.cursor()
        cursor.execute("""
                     SELECT Date_of_Journey ,COUNT(*) FROM flights_data
                      GROUP by Date_of_Journey   
                       
                       """)
        data=cursor.fetchall()
        for item in data:
            date.append(item[0])
            flights_count.append(item[1])
        cursor.close()
        return date,flights_count
    def avg_price_per_airline(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT Airline, AVG(Price)
            FROM flights_data
            GROUP BY Airline
        """)
        data = cursor.fetchall()
        cursor.close()

        airlines = [i[0] for i in data]
        prices = [i[1] for i in data]

        return airlines, prices
    def expensive_routes(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT Source, Destination, AVG(Price) as avg_price
            FROM flights_data
            GROUP BY Source, Destination
            ORDER BY avg_price DESC
            LIMIT 10
        """)
        data = cursor.fetchall()
        cursor.close()
        return data
    def flights_per_month(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT MONTH(STR_TO_DATE(Date_of_Journey, '%d/%m/%Y')) as month,
                COUNT(*)
            FROM flights_data
            GROUP BY month
            ORDER BY month
        """)
        data = cursor.fetchall()
        cursor.close()
        return data