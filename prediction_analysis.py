import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class Prediction_analysis:

    def __init__(self, connection, cursor):
        self.connection1 = connection
        self.cursor1 = cursor

    def run(self):
        pass