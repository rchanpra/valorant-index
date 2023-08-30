import mysql.connector
from prettytable import PrettyTable

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="valorant"
)

dbcursor = db.cursor()

weapon = input('weapon?')

dbcursor.execute("SELECT name, category, cost, fire_rate, magazine_size, reload_time FROM weapons WHERE name=%s", [weapon])

data = dbcursor.fetchone()

table = PrettyTable(['name', 'category', 'cost', 'fire rate', 'magazine size', 'reload time'])
table.add_row(data)
print(table)
