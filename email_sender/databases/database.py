import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import time
import numpy as np
from email_sender.datesconverter import DatesConverter


class DataBase:
    def __init__(self, kind, line, host, database, user, password, table, time_field):

        self.kind = kind
        self.line = line
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.time_field = time_field
        self.name = kind + ' - ' + line

        try:
            self.connection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)

            if self.connection.is_connected():
                self.status = 'Ok'
                # self.cursor = self.connection.cursor() # Not used as it is declared in the execution methods
            else:
                self.status = 'ERROR'
                print(f'DataBase: {self.name}\t Status: {self.status}')

        except Error as e:
            print(f"Error while connecting to {self.name}\t", e)

        db_time = self.get_current_timestamp()
        real_time = datetime.now()

        self.timedelta = db_time - real_time
        self.unix_timedelta = self.datetime_to_unix(db_time) - self.datetime_to_unix(real_time)

    def execute_query_get_one(self, query):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()[0]
        cursor.close()
        return data

    def execute_query_get_all(self, query):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_type(self):
        return self.kind

    def get_line(self):
        return self.line

    def get_current_timestamp(self):
        query = f"""
        SELECT CURRENT_TIMESTAMP;
        """
        database_timestamp = self.execute_query_get_one(query)
        return database_timestamp

    def get_timedelta(self):
        return self.timedelta

    def get_unix_timedelta(self):
        return self.unix_timedelta

    def datetime_to_unix(self, date):
        unixtime = int(time.mktime(date.timetuple()))
        return unixtime

    def get_cartridges_between_datetimes(self, start_hour, end_hour):
        """
        Gets the cartridges manufactured between te two dates introduced
        :param start_hour: [datetime] Starting hour to count
        :param end_hour: [datetime] End time to count
        :return: Manufactured cartridges quantity between the two dates
        """

        # Only for the balances weight data base, convert to a Julian date format
        if self.kind == 'Balances':
            converter = DatesConverter()
            start_hour = converter.date_to_float(start_hour)
            end_hour = converter.date_to_float(end_hour)

            query = f"""
                     SELECT COUNT(DISTINCT SN)
                     FROM {self.table}
                     WHERE Station = 2
                     AND {self.time_field} BETWEEN {start_hour}
                     AND {end_hour}
                     """

        # Note: to improve precision add: + self.timedelta to get the exact time to start_hour and end_hour
        else:
            query = f"""
                     SELECT COUNT(DISTINCT SN)
                     FROM {self.table}
                     WHERE {self.time_field} BETWEEN '{start_hour}'
                     AND '{end_hour}'
                     """
        one_hour_cartridges = self.execute_query_get_one(query)

        return one_hour_cartridges

    def get_split_shifts_by_day(self, day):
        """
        Only for Monday to Friday (3 turns): Gives the quantity manufactured by each turn. F.Ex:
        [IN] get_split_turns_by_day('2020-09-20')
        [OUT] (Weekdays): [143, 543, 786, nan, nan]
        [OUT] (Weekends): [nan, nan, nan, 845, 746]

        :param day: [datetime] Day which you want to know the manufactured cartridges but split by shifts
        :return: [list] Integers indicating. [first entry] => First turn (night, from 22:00h to 6:00h),
        [second entry] => Second turn (morning, from 6:00h to 14:00h) and
        [third entry] => Third turn (afternoon / evening, from 14:00h to 22:00h)
        [fourth entry] => Weekend night shift (from 22:00h to 10:00h)
        [fifth entry] => Weekend morning shift (from 10:00h to 22:00h)
        """

        # Start previous day
        night_turn_start = datetime(year=day.year, month=day.month, day=day.day, hour=22) - timedelta(days=1)

        if day.weekday() < 5:
            quantity_shifts = 3
        else:
            quantity_shifts = 2

        hours_shift = 24 / quantity_shifts

        # Creating a numpy array with paired the starting shift datetime and the ending shift datetime
        shifts_hours_array = np.array([(night_turn_start + i * timedelta(hours=hours_shift),
                                        night_turn_start + (i + 1) * timedelta(hours=hours_shift))
                                       for i in range(quantity_shifts)])

        # F.Ex: array([[datetime.datetime(2021, 6, 2, 22, 0), datetime.datetime(2021, 6, 3, 6, 0)],
        #        [datetime.datetime(2021, 6, 3, 6, 0), datetime.datetime(2021, 6, 3, 14, 0)],
        #        [datetime.datetime(2021, 6, 3, 14, 0), datetime.datetime(2021, 6, 3, 22, 0)]])

        total_split_quantities = [self.get_cartridges_between_datetimes(shift_start_hour, shift_end_hour)
                                  for shift_start_hour, shift_end_hour in shifts_hours_array]

        # Adding the not found values
        if quantity_shifts == 3:
            total_split_quantities += [np.nan] * 2
        else:
            total_split_quantities = [np.nan] * 3 + total_split_quantities

        print(total_split_quantities)
        return total_split_quantities