import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sys import exit

from raw_data_queries import Raw_data_queries
from lin_reg_table import Lin_reg_table
from prediction_table import Prediction_table


class Program:
    def __init__(self): #PG-connection setup
        self.conn = sqlite3.connect('mondial.db') # establish database connection
        self.cur = self.conn.cursor() # create a database query cursor

        # init classes
        self.raw_data_queries = Raw_data_queries(self.conn, self.cur)
        self.prediction_table = Prediction_table(self.conn, self.cur)
        self.lin_reg = Lin_reg_table(self.conn, self.cur)

        # specify the command line menu here
        self.actions = [    self.menu_1, self.menu_2, 
                            self.menu_3, self.menu_4, 
                            self.menu_5, self.lin_reg_table, 
                            self.create_prediction_table, self.plot_city_prediction_table, 
                            self.plot_city_predictions, self.menu_10,
                            self.exit]
        # menu text for each of the actions above
        self.menu = [   "City query", "Population Query", 
                        "Plot Population (2a)", 
                        "Plot average population (2b)", 
                        "Predict city population (2c)", 
                        "Create table with the linear regressions of all cities (2d)", 
                        "Create a table with predictions for all years (2e)", 
                        "Plot the prediction for a city (2e)", 
                        "Visualize population trends for all cities (2f)", 
                        "Visualize population trend average (2f)",
                        "Exit"]

    def print_menu(self):
        """Prints a menu of all functions this program offers.  
        Returns the numerical correspondent of the choice made."""
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()
        
    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, 
        it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not a number, genius.... :(")
 
    def menu_1(self):
        result = self.raw_data_queries.city_query()
        self.print_answer(result)
    
    def menu_2(self):
        result = self.raw_data_queries.population_query()
        self.print_answer(result)
    
    def menu_3(self):
        self.raw_data_queries.population_plot()

    def menu_4(self):
        self.raw_data_queries.population_avg_plot()
    
    def menu_5(self):
        self.raw_data_queries.population_plot_predict()

    def lin_reg_table(self):
        self.lin_reg.run()
    
    def create_prediction_table(self):
        self.prediction_table.run()

    def plot_city_prediction_table(self):
        self.prediction_table.graph_city()
    
    def plot_city_predictions(self):
        self.prediction_table.graph_all_cities()

    def menu_10(self):
        self.prediction_table.graph_city_avg()

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
