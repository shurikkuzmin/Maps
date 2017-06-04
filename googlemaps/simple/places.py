import csv
import sqlite3
import os

class Places(object):
    def __init__(self):
        dbFile = os.path.dirname(os.path.realpath(__file__)) + "/locs.db"
        self.connection = sqlite3.connect(dbFile)

        if not self.dbHasData():
            self.populateData()   

    def dbHasData(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT Count(*) FROM sqlite_master WHERE name='cities';")
        data = cursor.fetchone()[0]

        if data > 0:
            cursor.execute("SELECT Count(*) FROM cities;")
            data = cursor.fetchone()[0]
            return data > 0
        
        return False

    def populateData(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS cities")    

        cursor.execute("CREATE TABLE cities(continent_code TEXT, continent_name TEXT, country_iso_code TEXT, country_name TEXT, \
                       subdivision_iso_code TEXT, subdivision_name TEXT, city_name TEXT, time_zone TEXT)")
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        with open(currentDirectory+"/data/GeoLite2-City-Locations.csv", "r", errors = "ignore") as info:
            reader = csv.reader(info)
            index = 0
            for row in reader:
                if index == 0:
                    index = index + 1
                    continue
                index = index + 1
                continent_code = row[1]
                continent_name = row[2]
                country_iso_code = row[3]
                country_name = row[4]
                subdivision_iso_code = row[5] 
                subdivision_name = row[6] 
                city_name = row[7]
                time_zone = row[8] 

                cursor.execute("INSERT INTO cities VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (continent_code, continent_name, country_iso_code, \
                country_name, subdivision_iso_code, subdivision_name, city_name, time_zone))

            self.connection.commit()
    
    def findCities(self, listCities):
        cursor = self.connection.cursor()
        realCities = []
        
        #Test database
        #cursor.execute('SELECT * FROM cities')
        #rows = cursor.fetchall()
        #for row in rows:
        #    print("Test=", row)
        for city in listCities:
            cursor.execute('SELECT * FROM cities WHERE city_name = "' + city + '"')
            rows = cursor.fetchall()
            if len(rows) > 0:
                realCities.append(True)
            else:
                realCities.append(False)
        return realCities
