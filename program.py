#!/usr/bin/python
import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sys import exit


class Program:
    def __init__(self): #PG-connection setup
        self.conn = sqlite3.connect('mondial.db') # establish database connection
        self.cur = self.conn.cursor() # create a database query cursor

        # specify the command line menu here
        self.actions = [self.city_query, self.population_query, self.population_plot, self.population_avg_plot, self.population_plot_predict, self.exit]
        # menu text for each of the actions above
        self.menu = ["City query", "Population Query", "Plot Population", "Plot average population", "Predict city population", "Exit"]
        self.cur = self.conn.cursor()
    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()
    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not a number, genious.... :(")
 
    def city_query(self):
      
        city = input("city: ")
        print("city: %s" % (city))
        try:
            query ='SELECT * FROM city WHERE name == "%s"' % (city)
            print("Will execute: ", query)
            self.cur.execute(query)
            result = self.cur.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.conn.rollback()
            exit()

        self.print_answer(result)
    
    def population_query(self):
        minpop = input("min_population: ")
        maxpop = input("max_population: ")
        print("minpop: %s, maxpop: %s" % (minpop, maxpop))
        try:
            query ="SELECT * FROM city WHERE population >=%s AND population <= %s" % (minpop, maxpop)
            print("Will execute: ", query)
            self.cur.execute(query)
            result = self.cur.fetchall()
        except sqlite3.Error as e:
            print( "Error message:", e.args[0])
            self.conn.rollback()
            exit()

        self.print_answer(result)
    
    #--------------------------- 2a ---------------------------
    def population_plot(self):
        try:
            query ="SELECT year, population FROM citypops"
            print("Will execute: ", query)
            self.cur.execute(query)
            result = self.cur.fetchall()
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
                
        plt.scatter(xs, ys, s = 0.5)
        plt.title('City population raw data')
        plt.show()

    #--------------------------- 2b ---------------------------
    def population_avg_plot(self):
        try:
            query ="SELECT year, avg(population) FROM citypops GROUP BY year"
            print("Will execute: ", query)
            self.cur.execute(query)
            result = self.cur.fetchall()
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
        plt.title('City population average')
        plt.show()
    
    def population_plot_predict(self):
        city = input("city: ")
        print("city: %s" % (city))
        try:
            query ='SELECT year, population FROM citypops WHERE city == "%s"' % (city)
            print("Will execute: ", query)
            self.cur.execute(query)
            result = self.cur.fetchall()
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

    def exit(self):    
        self.cur.close()
        self.conn.close()
        exit()

    def print_answer(self, result):
        print("-----------------------------------")
        for r in result:
            print(r)
        print("-----------------------------------")

    def run(self):
        while True:
            try:
                self.actions[self.print_menu()-1]()
            except IndexError:
                print("Bad choice")
                continue
