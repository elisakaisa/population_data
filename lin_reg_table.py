import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from helper_functions import *

class Lin_reg_table:

    def __init__(self, connection, cursor):
        self.connection1 = connection
        self.cursor1 = cursor
        self.table_name = "linear_prediction"

    def loop_through_db(self):
        """loops through all cities in the database and performs linear regression on the obtained data,
            then adds it to the new table"""
        print("looping through database")
        try:
            self.cursor1.execute("""SELECT city, country, year, population FROM citypops GROUP BY city""")
            
            country_l = []
            city_l = []

            while True:
                # This SQL statement selects all data from the CUSTOMER table.
                result = self.cursor1.fetchone()
                if result is None:
                    break
                country_l.append(result[1])
                city_l.append(result[0])
            
            # loops through the city lists to fetch the population data
            for i in range(len(city_l)):
                self.population_predict(city_l[i], country_l[i])
                
            print("Successfully added all tuples to the database")
            
        except sqlite3.Error as e:
            print("Error message (loop through): ", e.args[0])
            self.connection1.rollback()

    def add_row(self, city, country, a, b, score):
        """ adds a row to the table initialized in init() """
        try:
            query = """INSERT INTO %s VALUES("%s", '%s', %f, %f, %f)""" % (self.table_name, city, country, a, b, score);
            #print("Query", query)
            self.cursor1.execute(query)

            # this commits all executed queries forming a transaction up to this point
            self.connection1.commit()
        except sqlite3.Error as e:
            print("Error message (add row) :", e.args[0], "(", city, country, a, b, score, ")")
            self.connection1.rollback()

    def population_predict(self, city, country):
        """ calculates the linear regression of the given city """
        try:
            query ='SELECT year, population FROM citypops WHERE city == "%s" AND country == "%s"' % (city, country)
            #print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message (lin_regr): ", e.args[0])
            self.connection1.rollback()
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

        #linear regression
        if len(xs) > 1:
            regr = LinearRegression().fit(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
            regr_score = regr.score(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
            #print("The score of the linear regression is: %f" % (regr_score))
            a = regr.coef_[0][0]
            b = regr.intercept_[0]
            [city, country, a, b, regr_score]

            # if successful, add tuple to table
            self.add_row(city, country, a, b, regr_score)


    def query(self):
        # Here we test some concurrency issues.
        xy = "select name, country, a, b, score from %s;" % (self.table_name)
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

    def run(self):
        drop(self.cursor1, self.connection1, self.table_name)
        init_table(self.cursor1, self.connection1, "(name text, country text, a decimal, b decimal, score decimal)", self.table_name)
        self.loop_through_db()
        [name_list, country_list, a_list, b_list, score_list] = self.query()
