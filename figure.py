#!/usr/bin/python

import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


connection1 = sqlite3.connect('mondial.db') # establish database connection
cursor1 = connection1.cursor() # create a database query cursor

# This scripts illustrates how you can use output from a query, cast it to python floats,
# and then use a figure plotting library called Matplotlib to create a scatterplot of the
# data.

# Make sure you have installed python as well as sqlite3 python libraries

# documentation of plotting library: https://matplotlib.org/, you can use any other
# library if you like

#----------------- INIT VARIABLE ---------------
table_name = "linear_prediction"

def drop():
    # delete the table XYData if it does already exist
    try:
        query = "DROP TABLE %s;" % (table_name)
        #print("Query", query)
        cursor1.execute(query)
        connection1.commit()  
        # by default in pgdb, all executed queries for connection 1 up to here form a transaction
        # we can also explicitly start tranaction by executing BEGIN TRANSACTION
    except sqlite3.Error as e:
        print("ROLLBACK: %s table does not exists or other error." % (table_name))
        print("Error message:", e.args[0])
        connection1.rollback()
        pass

def init():
    try:
        # Create table sales and add initial tuples
        # new relation “linearprediction” with attributes “name, country, a, b, score” 
        query = "CREATE TABLE %s(name text, country text, a decimal, b decimal, score decimal);" % (table_name)
        cursor1.execute(query)

        # TODO: loop through this with all cities
        query = """INSERT INTO %s VALUES('SL', 'test', 2.45555, 4.3222222, 3.2)""" % (table_name);
        print("Query", query)
        cursor1.execute(query)

        # this commits all executed queries forming a transaction up to this point
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()

def query():
    # Here we test some concurrency issues.
    xy = "select name, country, a, b, score from %s;" % (table_name)
    print("U1: (start) "+ xy)
    try:
        cursor1.execute(xy)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()

    name = []
    country = []
    a = []
    b = []
    score = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0]!=None and r[1]!=None and r[2]!=None and r[3]!=None and r[4]!=None):
            name.append(r[0])
            country.append(r[1])
            a.append(float(r[2]))
            b.append(float(r[3]))
            score.append(float(r[4]))
        else:
            print("Dropped tuple ", r)
    print("name:", name)
    print("country:", country)
    print("a: ", a)
    print("b: ", b)
    print("score: ", score)
    return [name, country, a, b, score]

def close():
    connection1.close()


# when calling python filename.py the following functions will be executed:
drop()
init()
[name, country, a, b, score] = query()
#plt.scatter(xs, ys)
#plt.savefig("figure.png") # save figure as image in local directory
#plt.show()  # display figure if you run this code locally, otherwise comment out
close()


