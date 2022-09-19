import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class Raw_data_queries:

    def __init__(self, connection, cursor):
        self.connection1 = connection
        self.cursor1 = cursor

    def city_query(self):
        city = input("city: ")
        print("city: %s" % (city))
        try:
            query ='SELECT * FROM city WHERE name == "%s"' % (city)
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.connection1.rollback()
            exit()

        return result

    def population_query(self):
        minpop = input("min_population: ")
        maxpop = input("max_population: ")
        print("minpop: %s, maxpop: %s" % (minpop, maxpop))
        try:
            query ="SELECT * FROM city WHERE population >=%s AND population <= %s" % (minpop, maxpop)
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.connection1.rollback()
            exit()

        return result
    
    def population_plot(self):
        try:
            query ="SELECT year, population FROM citypops"
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
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
                
        plt.scatter(xs, ys, s = 0.5)
        plt.title('City population raw data')
        plt.show()

    def population_sum_plot(self):
        try:
            query ="SELECT year, sum(population) FROM citypops GROUP BY year"
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.connection1.rollback()
            exit()

        xs= []
        ys= []
        for r in result:
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
                
        plt.scatter(xs, ys, s = 10)
        plt.title('City population sum')
        plt.show()

    def population_plot_predict(self):
        city = input("city: ")
        print("city: %s" % (city))
        try:
            query ='SELECT year, population FROM citypops WHERE city == "%s"' % (city)
            print("Will execute: ", query)
            self.cursor1.execute(query)
            result = self.cursor1.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.connection1.rollback()
            exit()

        xs= []
        ys= []
        for r in result:
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))

        #linear regression
        regr = LinearRegression().fit(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
        score = regr.score(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
        print("The score of the linear regression is: %s" % (score))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]

        x_regression = np.array(xs).reshape([-1,1])
        y_regression = a*x_regression + b
        label = "%s * x + %s" % (a, b)

        plt.scatter(xs, ys, s = 10)
        plt.plot(xs, y_regression, '-r', label=label)
        plt.legend(loc='upper left')
        plt.title('City population of %s' % (city))
        plt.show()