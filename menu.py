#!/usr/bin/python
import sqlite3
import matplotlib.pyplot as plt
from sys import exit

# for Python 2.x users
try: input = raw_input
except NameError: pass

class Program:
    def __init__(self): #PG-connection setup
        self.conn = sqlite3.connect('mondial.db') # establish database connection
        self.cur = self.conn.cursor() # create a database query cursor

        # specify the command line menu here
        self.actions = [self.population_query, self.population_plot ,self.exit]
        # menu text for each of the actions above
        self.menu = ["Population Query", "Plot Population","Exit"]
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

if __name__ == "__main__":
    db = Program()
    db.run()
    