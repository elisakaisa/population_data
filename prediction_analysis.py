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
            #TODO: loop through this for every year and search for max correlation?
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

    
    def join_tables_pred_by_group(self):
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

        # only cities with over a certain population increase
        cutoff_a = -200
        cutoff_b = 200
        cutoff_c = 10000
        a_a_list = []
        a_latitude_list = []
        a_longitude_list = []
        b_a_list = []
        b_latitude_list = []
        b_longitude_list = []
        c_a_list = []
        c_latitude_list = []
        c_longitude_list = []
        d_a_list = []
        d_latitude_list = []
        d_longitude_list = []

        for r in result:
            if int(r[1]) < cutoff_a:
                a_a_list.append(int(r[1]))
                a_latitude_list.append(float(r[2]))
                a_longitude_list.append(float(r[3]))
            if int(r[1]) < cutoff_b and int(r[1]) >= cutoff_a:
                b_a_list.append(int(r[1]))
                b_latitude_list.append(float(r[2]))
                b_longitude_list.append(float(r[3]))
            if int(r[1]) < cutoff_c and int(r[1]) >= cutoff_b:
                c_a_list.append(int(r[1]))
                c_latitude_list.append(float(r[2]))
                c_longitude_list.append(float(r[3]))
            if int(r[1]) >= cutoff_c:
                d_a_list.append(int(r[1]))
                d_latitude_list.append(float(r[2]))
                d_longitude_list.append(float(r[3]))

        print(len(a_a_list))
        print(len(b_a_list))
        print(len(c_a_list))
        print(len(d_a_list))

        
        # correlation coefficient (lat/pop)
        print("-----------------------------------")
        print("Correlation between latitude and population increase")
        full_correlation1 = pearsonr(a_a_list,a_latitude_list)
        corr_string_1 = "r = {:0.2f}".format(full_correlation1[0])
        print('Correlation coefficient:',full_correlation1[0])
        print('P-value:',full_correlation1[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop)
        print("-----------------------------------")
        print("Correlation between longitude and population increase")
        full_correlation2 = pearsonr(a_a_list,a_longitude_list)
        corr_string_2 = "r = {:0.2f}".format(full_correlation2[0])
        print('Correlation coefficient:',full_correlation2[0])
        print('P-value:',full_correlation2[1])
        print("-----------------------------------")

        # correlation coefficient (lat/pop) big cities
        print("-----------------------------------")
        print("Correlation between latitude and population increase in cities with a population over ")
        full_correlation3 = pearsonr(b_a_list,b_latitude_list)
        corr_string_3 = "r = {:0.2f}".format(full_correlation3[0])
        print('Correlation coefficient:',full_correlation3[0])
        print('P-value:',full_correlation3[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop) big cities
        print("-----------------------------------")
        print("Correlation between longitude and population increase in cities with a population over ")
        full_correlation4 = pearsonr(b_a_list,b_longitude_list)
        corr_string_4 = "r = {:0.2f}".format(full_correlation4[0])
        print('Correlation coefficient:',full_correlation4[0])
        print('P-value:',full_correlation4[1])
        print("-----------------------------------")

         # correlation coefficient (lat/pop)
        print("-----------------------------------")
        print("Correlation between latitude and population increase")
        full_correlation5 = pearsonr(c_a_list,c_latitude_list)
        corr_string_5 = "r = {:0.2f}".format(full_correlation5[0])
        print('Correlation coefficient:',full_correlation5[0])
        print('P-value:',full_correlation5[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop)
        print("-----------------------------------")
        print("Correlation between longitude and population increase")
        full_correlation6 = pearsonr(c_a_list,c_longitude_list)
        corr_string_6 = "r = {:0.2f}".format(full_correlation2[0])
        print('Correlation coefficient:',full_correlation6[0])
        print('P-value:',full_correlation6[1])
        print("-----------------------------------")

        # correlation coefficient (lat/pop) big cities
        print("-----------------------------------")
        print("Correlation between latitude and population increase in cities with a population over ")
        full_correlation7 = pearsonr(d_a_list,d_latitude_list)
        corr_string_7 = "r = {:0.2f}".format(full_correlation7[0])
        print('Correlation coefficient:',full_correlation7[0])
        print('P-value:',full_correlation7[1])
        print("-----------------------------------")
        # correlation coefficient (lon/pop) big cities
        print("-----------------------------------")
        print("Correlation between longitude and population increase in cities with a population over ")
        full_correlation8 = pearsonr(d_a_list,d_longitude_list)
        corr_string_8 = "r = {:0.2f}".format(full_correlation8[0])
        print('Correlation coefficient:',full_correlation8[0])
        print('P-value:',full_correlation8[1])
        print("-----------------------------------")
                
        fig = plt.figure(figsize=(16, 16))
        ax1 = fig.add_subplot(421)
        ax2 = fig.add_subplot(422)
        ax3 = fig.add_subplot(423)
        ax4 = fig.add_subplot(424)
        ax5 = fig.add_subplot(425)
        ax6 = fig.add_subplot(426)
        ax7 = fig.add_subplot(427)
        ax8 = fig.add_subplot(428)
                
        ax1.scatter(a_latitude_list, a_a_list, c ='b', s = 1, label=corr_string_1)
        ax1.set_xlabel("Latitude")
        ax1.set_ylabel("Population increase (lin reg)")
        ax1.set_title('Predicted pop / latitude, pop increase below %s' % (cutoff_a))
        ax1.legend()
        
        ax2.scatter(a_longitude_list, a_a_list, c ='r', s = 1, label=corr_string_2)
        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Population increase (lin reg)")
        ax2.set_title('Predicted pop / longitude, pop increase below %s' % (cutoff_a))
        ax2.legend()

        ax3.scatter(b_latitude_list, b_a_list, c ='b', s = 1, label=corr_string_3)
        ax3.set_xlabel("Latitude")
        ax3.set_ylabel("Population increase (lin reg)")
        ax3.set_title('Predicted pop / latitude, pop increase between %s and %s' % (cutoff_a, cutoff_b))
        ax3.legend()
        
        ax4.scatter(b_longitude_list, b_a_list, c ='r', s = 1, label=corr_string_4)
        ax4.set_xlabel("Longitude")
        ax4.set_ylabel("Population increase (lin reg)")
        ax4.set_title('Predicted pop / longitude, pop increase between %s and %s' % (cutoff_a, cutoff_b))
        ax4.legend()

        ax5.scatter(c_latitude_list, c_a_list, c ='b', s = 1, label=corr_string_5)
        ax5.set_xlabel("Latitude")
        ax5.set_ylabel("Population increase (lin reg)")
        ax5.set_title('Predicted pop / latitude, pop increase between %s and %s' % (cutoff_b, cutoff_c))
        ax5.legend()
        
        ax6.scatter(c_longitude_list, c_a_list, c ='r', s = 1, label=corr_string_5)
        ax6.set_xlabel("Longitude")
        ax6.set_ylabel("Population increase (lin reg)")
        ax6.set_title('Predicted pop / longitude, pop increase between %s and %s' % (cutoff_b, cutoff_c))
        ax6.legend()

        ax7.scatter(d_latitude_list, d_a_list, c ='b', s = 1, label=corr_string_6)
        ax7.set_xlabel("Latitude")
        ax7.set_ylabel("Population increase (lin reg)")
        ax7.set_title('Predicted pop / latitude pop increase above %s' % (cutoff_c))
        ax7.legend()
        
        ax8.scatter(d_longitude_list, d_a_list, c ='r', s = 1, label=corr_string_7)
        ax8.set_xlabel("Longitude")
        ax8.set_ylabel("Population increase (lin reg)")
        ax8.set_title('Predicted pop / longitude, pop increase above %s' % (cutoff_c))
        ax8.legend()
        
        plt.show()