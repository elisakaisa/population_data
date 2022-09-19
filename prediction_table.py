import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from helper_functions import *

"""e) Create a python function and menu entry that uses pure SQL commands to:

• create a new relation “prediction” with the attributes (name, country, population, year) 
that will hold one entry per city and year with the linear predictions for each year from 
1950 to 2050 of population trends according to the parameters of our linearpredictions relation

• Use SQL to select data from linearprediction and simple arithmetic (recall y = ax + b) 
together with SQL INSERT statements to populate the predictions table with one tuple per 
year and city. 
The idea here is to run a python loop over the years with ONE SQL INSERT command per year 
to create all tuples for a given prediction YEAR (do not create one SQL command per tuple, 
which would be very inefficient)! Let the optimized internal code of SQLite3 do the work 
for you. Think about how you can achieve this."""

class Prediction_table:

    def __init__(self, connection, cursor):
        self.connection1 = connection
        self.cursor1 = cursor
        self.table_name = "PredictionTable"

    def run(self):
        #TODO: add chekc that table linear_regression exists
        drop(self.cursor1, self.connection1, self.table_name)
        init_table(self.cursor1, self.connection1, "(name text, country text, population int, year int)", self.table_name)
        [name_list, country_list, a_list, b_list, score_list] = self.query_lin_reg_table()
        self.populate(name_list, country_list, a_list, b_list)

        # for debugging purposes
        #[name_list, country_list, pop_list, year_list] = self.query_pred_table()

    def query_lin_reg_table(self):
        """ queries the table and turns the results into lists"""
        # Here we test some concurrency issues.
        xy = "select name, country, a, b, score from linear_prediction;"
        print("U1: (start) "+ xy)
        try:
            self.cursor1.execute(xy)
            data = self.cursor1.fetchall()
            self.connection1.commit()
        except sqlite3.Error as e:
            print("Error message (query): ", e.args[0])
            self.connection1.rollback()
            exit()

        name_list = []
        country_list = []
        a_list = []
        b_list = []
        score_list = []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            #print("Considering tuple", r)
            if (r[0]!=None and r[1]!=None and r[2]!=None and r[3]!=None and r[4]!=None):
                name_list.append(r[0])
                country_list.append(r[1])
                a_list.append(float(r[2]))
                b_list.append(float(r[3]))
                score_list.append(float(r[4]))
            else:
                print("Dropped tuple ", r)

        return [name_list, country_list, a_list, b_list, score_list]

    def linear_prediction(self, a, b, year):
        return a*year + b
    
    def populate(self, city_list, country_list, a_list, b_list):
        print("Adding data to the table, start")
        years = [*range(1950, 2051, 1)]

        #init
        result = []
        
        for i in range(len(years)):
            print("Adding data for year %i to the table" % (years[i]))
            for j in range(len(city_list)):
                population = self.linear_prediction(a_list[j], b_list[j], years[i])
                city_tuple = (city_list[j], country_list[j], population, years[i])
                #print(city_tuple)
                result.append(city_tuple)
            #print(result)
            try:
                self.cursor1.executemany("""INSERT INTO PredictionTable (name, country, population, year) VALUES (?, ?, ?, ?)""", result)
                self.connection1.commit()
            except sqlite3.Error as e:
                print("Error message (loop through): ", e.args[0])
                self.connection1.rollback()
        print("Successfully added all years of data to the table")
    
    def query_pred_table(self):
        """ queries the table and turns the results into lists"""
        # Here we test some concurrency issues.
        xy = "select name, country, population, year from PredictionTable;"
        print("U1: (start) "+ xy)
        try:
            self.cursor1.execute(xy)
            data = self.cursor1.fetchall()
            self.connection1.commit()
        except sqlite3.Error as e:
            print("Error message (query): ", e.args[0])
            self.connection1.rollback()
            exit()

        name_list = []
        country_list = []
        pop_list = []
        year_list = []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            #print("Considering tuple", r)
            if (r[0]!=None and r[1]!=None and r[2]!=None and r[3]!=None):
                name_list.append(r[0])
                country_list.append(r[1])
                pop_list.append(int(r[2]))
                year_list.append(int(r[3]))
            else:
                print("Dropped tuple ", r)

        #print(name_list)
        #print(pop_list)
        #print(year_list)
        return [name_list, country_list, pop_list, year_list]


    def graph_city(self):
        city = input("Select city to visualize the population: ")
        xy = "select name, country, population, year from PredictionTable;"
        print("U1: (start) "+ xy)
        try:
            query ='SELECT year, population FROM PredictionTable WHERE name == "%s"' % (city)
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.conn.rollback()
            exit()

        xs= []
        ys= []
        for r in result:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))

        plt.scatter(xs, ys, s = 10)
        plt.title('City population of %s' % (city))
        plt.show()