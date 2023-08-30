import requests
import json
import mysql.connector
from prettytable import PrettyTable

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

dbcursor = db.cursor()

try:
    dbcursor.execute("CREATE DATABASE valorant")
except mysql.connector.errors.DatabaseError:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="valorant"
    )

dbcursor = db.cursor()

try:
    dbcursor.execute("""CREATE TABLE weapons (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        category VARCHAR(255),
                        cost INT,
                        fire_rate FLOAT,
                        magazine_size INT,
                        reload_time FLOAT
                        )""")
except mysql.connector.errors.ProgrammingError:
    dbcursor.execute("DROP TABLE weapons")
    dbcursor.execute("""CREATE TABLE weapons (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        category VARCHAR(255),
                        cost INT,
                        fire_rate FLOAT,
                        magazine_size INT,
                        reload_time FLOAT
                        )""")

response = requests.get('https://valorant-api.com/v1/weapons')
weapon_data = json.loads(response.text)

for weapon in weapon_data['data']:
    if weapon['weaponStats'] != None:
        sql = "INSERT INTO weapons (name, category, cost, fire_rate, magazine_size, reload_time) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (weapon['displayName'],
               weapon['shopData']['category'],
               weapon['shopData']['cost'],
               weapon['weaponStats']['fireRate'],
               weapon['weaponStats']['magazineSize'],
               weapon['weaponStats']['reloadTimeSeconds'])
        dbcursor.execute(sql, val)

db.commit()

dbcursor.execute("SELECT name, category, cost, fire_rate, magazine_size, reload_time FROM weapons ORDER BY name")

data = dbcursor.fetchall()

table = PrettyTable(['name', 'category', 'cost', 'fire rate', 'magazine size', 'reload time'])
for row in data:
    table.add_row(row)
print(table)
