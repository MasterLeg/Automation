from table_sender.databases.datagate import DataGate
from datetime import datetime
from table_sender.days import Days
from table_sender.table import Table
import numpy as np


class LogicMaster:
    def __init__(self):
        # Current week dates
        current_week_dates = self.get_dates_list()

        # Get data from DataBases
        ordered_matrix_productions = self.get_matrix_values(current_week_dates)
        print(ordered_matrix_productions)
        # Create the visual table
        Table(ordered_matrix_productions)
        # Send the table to the user mail
        # Email()
        self.open_image_explorer()

    def get_dates_list(self):
        # Get current week
        today = datetime.now()
        week_number = int(today.strftime('%V'))
        year = datetime.now().year

        # Get datetime monday
        monday = datetime.fromisocalendar(year, week_number, 1)
        # Create all current week datetime list datetime
        return Days(monday, 7).get_list()

    def get_matrix_values(self, current_week_dates):
        dg = DataGate()

        # For each database of kind 'Finished' gets:
        # For each day in the list, the manufactured cartridges split by shift
        volume_production_shifts = np.array([[db.get_split_shifts_by_day(day)
                                              for day in current_week_dates]
                                             for db in dg.databases['Balances'].values()])

        # The data are returned in a volume, then join each layer one right after the other
        # print('Matrix A:\n', volume_production_shifts[0])
        # print('Matrix B:\n', np.array([0] * 7).reshape(7, 1))
        # print(np.hstack(np.array([0] * 7).reshape(1, 7), volume_production_shifts[0]))
        print(volume_production_shifts[0])
        print(volume_production_shifts[1])

        ordered_matrixes_productions = np.hstack((volume_production_shifts[0], volume_production_shifts[1]))
        return ordered_matrixes_productions

    def open_image_explorer(self):
        import subprocess
        subprocess.Popen(['explorer',
                          r'J:\98_Scaling up plan\14-Proyectos 2021\13_Lean Box\20_Objetivo y Producciones\ObjectivesTable.png'])