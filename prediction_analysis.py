import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

class Prediction_analysis:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def join_tables_pop(self):
        try:
            print("running query")
            query = """SELECT PredictionTable.name, PredictionTable.population, PredictionTable.year, PopData.latitude, PopData.longitude 
                        FROM PredictionTable JOIN PopData
                        WHERE PredictionTable.name = PopData.name
                        GROUP BY PredictionTable.name, PredictionTable.year;"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except sqlite3.Error as e:
            print( "Error message (join_tables): ", e.args[0])
            self.connection.rollback()
            exit()

        # all cities
        population_list = []
        latitude_list = []
        longitude_list = []

        # only cities with over certain population
        cutoff = 5000000
        big_population_list = []
        big_latitude_list = []
        big_longitude_list = []

        for r in result:
            population_list.append(int(r[1]))
            latitude_list.append(float(r[3]))
            longitude_list.append(float(r[4]))

            if int(r[1]) > cutoff:
                big_population_list.append(int(r[1]))
                big_latitude_list.append(float(r[3]))
                big_longitude_list.append(float(r[4]))
        
        print(len(population_list))
        print(len(big_population_list))

        
        # correlation coefficient (lat/pop)
        print("-----------------------------------")
        print("Correlation between latitude and population")
        full_correlation1 = pearsonr(population_list,latitude_list)
        corr_string_1 = "r = {:0.2f}".format(full_correlation1[0])
        print('Correlation coefficient:',full_correlation1[0])
        print('P-value:',full_correlation1[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop)
        print("-----------------------------------")
        print("Correlation between longitude and population")
        full_correlation2 = pearsonr(population_list,longitude_list)
        corr_string_2 = "r = {:0.2f}".format(full_correlation2[0])
        print('Correlation coefficient:',full_correlation2[0])
        print('P-value:',full_correlation2[1])
        print("-----------------------------------")

        # correlation coefficient (lat/pop) big cities
        print("-----------------------------------")
        print("Correlation between latitude and population in cities with a population over ", cutoff)
        full_correlation3 = pearsonr(big_population_list,big_latitude_list)
        corr_string_3 = "r = {:0.2f}".format(full_correlation3[0])
        print('Correlation coefficient:',full_correlation3[0])
        print('P-value:',full_correlation3[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop) big cities
        print("-----------------------------------")
        print("Correlation between longitude and population in cities with a population over ", cutoff)
        full_correlation4 = pearsonr(big_population_list,big_longitude_list)
        corr_string_4 = "r = {:0.2f}".format(full_correlation4[0])
        print('Correlation coefficient:',full_correlation4[0])
        print('P-value:',full_correlation4[1])
        print("-----------------------------------")
                
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)
                
        ax1.scatter(latitude_list, population_list, c ='b', s = 1, label=corr_string_1)
        ax1.set_xlabel("Latitude")
        ax1.set_ylabel("Population")
        ax1.set_title('Predicted population per latitude')
        ax1.legend()
        
        ax2.scatter(longitude_list, population_list, c ='r', s = 1, label=corr_string_2)
        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Population")
        ax2.set_title('Predicted population per longitude')
        ax2.legend()

        ax3.scatter(big_latitude_list, big_population_list, c ='b', s = 1, label=corr_string_3)
        ax3.set_xlabel("Latitude")
        ax3.set_ylabel("Population")
        ax3.set_title('Predicted population per latitude for cities over "%s" inhabitants' % (cutoff))
        ax3.legend()
        
        ax4.scatter(big_longitude_list, big_population_list, c ='r', s = 1, label=corr_string_4)
        ax4.set_xlabel("Longitude")
        ax4.set_ylabel("Population")
        ax4.set_title('Predicted population per longitude for cities over "%s" inhabitants' % (cutoff))
        ax4.legend()
        
        plt.show()

    def join_tables_pred(self):
        try:
            print("running query")
            query = """SELECT linear_prediction.name, linear_prediction.a, PopData.latitude, PopData.longitude 
                        FROM linear_prediction JOIN PopData
                        WHERE linear_prediction.name = PopData.name
                        GROUP BY linear_prediction.name;"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except sqlite3.Error as e:
            print( "Error message (join_tables): ", e.args[0])
            self.connection.rollback()
            exit()

        # all cities
        a_list = []
        latitude_list = []
        longitude_list = []

        # only cities with over a certain population increase
        cutoff = 100000
        big_a_list = []
        big_latitude_list = []
        big_longitude_list = []

        for r in result:
            a_list.append(int(r[1]))
            latitude_list.append(float(r[2]))
            longitude_list.append(float(r[3]))

            if int(r[1]) > cutoff:
                big_a_list.append(int(r[1]))
                big_latitude_list.append(float(r[2]))
                big_longitude_list.append(float(r[3]))

        
        # correlation coefficient (lat/pop)
        print("-----------------------------------")
        print("Correlation between latitude and population increase")
        full_correlation1 = pearsonr(a_list,latitude_list)
        corr_string_1 = "r = {:0.2f}".format(full_correlation1[0])
        print('Correlation coefficient:',full_correlation1[0])
        print('P-value:',full_correlation1[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop)
        print("-----------------------------------")
        print("Correlation between longitude and population increase")
        full_correlation2 = pearsonr(a_list,longitude_list)
        corr_string_2 = "r = {:0.2f}".format(full_correlation2[0])
        print('Correlation coefficient:',full_correlation2[0])
        print('P-value:',full_correlation2[1])
        print("-----------------------------------")

        # correlation coefficient (lat/pop) big cities
        print("-----------------------------------")
        print("Correlation between latitude and population increase in cities with a population over ", cutoff)
        full_correlation3 = pearsonr(big_a_list,big_latitude_list)
        corr_string_3 = "r = {:0.2f}".format(full_correlation3[0])
        print('Correlation coefficient:',full_correlation3[0])
        print('P-value:',full_correlation3[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop) big cities
        print("-----------------------------------")
        print("Correlation between longitude and population increase in cities with a population over ", cutoff)
        full_correlation4 = pearsonr(big_a_list,big_longitude_list)
        corr_string_4 = "r = {:0.2f}".format(full_correlation4[0])
        print('Correlation coefficient:',full_correlation4[0])
        print('P-value:',full_correlation4[1])
        print("-----------------------------------")
                
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)
                
        ax1.scatter(latitude_list, a_list, c ='b', s = 1, label=corr_string_1)
        ax1.set_xlabel("Latitude")
        ax1.set_ylabel("Population increase (lin reg)")
        ax1.set_title('Predicted population per latitude')
        ax1.legend()
        
        ax2.scatter(longitude_list, a_list, c ='r', s = 1, label=corr_string_2)
        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Population increase (lin reg)")
        ax2.set_title('Predicted population per longitude')
        ax2.legend()

        ax3.scatter(big_latitude_list, big_a_list, c ='b', s = 1, label=corr_string_3)
        ax3.set_xlabel("Latitude")
        ax3.set_ylabel("Population increase (lin reg)")
        ax3.set_title('Predicted population per latitude for cities over "%s" increase' % (cutoff))
        ax3.legend()
        
        ax4.scatter(big_longitude_list, big_a_list, c ='r', s = 1, label=corr_string_4)
        ax4.set_xlabel("Longitude")
        ax4.set_ylabel("Population increase (lin reg)")
        ax4.set_title('Predicted population per longitude for cities over "%s" increase' % (cutoff))
        ax4.legend()
        
        plt.show()