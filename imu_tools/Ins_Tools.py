import matplotlib.pyplot as plt

import pandas as pd

GPSpath = r"C:\Users\NailinLiao\PycharmProjects\Mark_location\data\ins\ins1\gps_ins.txt"


class Ins_Tools:
    @staticmethod
    def show_gps(gps_ins_file_path):
        imu_data = pd.read_csv(gps_ins_file_path)
        plt.plot(imu_data['Longitude'], imu_data['Lattitude'], c='black')
        plt.axis('equal')
        plt.show()
