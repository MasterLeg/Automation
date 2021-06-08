from email_sender.databases.datagate import DataGate
from datetime import datetime
from email_sender.days import Days
from email_sender.table import Table
from email_sender.email_sender import Email
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
        Email()


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
                                             for db in dg.databases['Finished'].values()])

        # The data are returned in a volume, then join each layer one right after the other
        ordered_matrixes_productions = np.hstack((volume_production_shifts[0], volume_production_shifts[1]))
        return ordered_matrixes_productions

