from datetime import datetime


class DatesConverter:
    def __init__(self):
        pass

    def float_to_date(self, valuetodate):
        """
        Transform from an Excel only understandable values to ISO date format
        F.Ex: 44081.627417 => datetime (2020, 9, 7, 15, 3, 29)
        :param valuetodate: [float] Date in Excel only understandable date, known as valuetodate or Julian date.
        F.Ex: 44081.627417
        -> 44081 => Days from 1st January 1900.
        -> 0.627417 => Percentage completed from the day. At 00:00h is 0%
        :return dt: [datetime] The date in format: dd/mm/yyyy hh:mm:ss
        """

        substituted_date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(valuetodate) - 2)

        # Get the decimals
        dec = valuetodate % 1

        # Transform decimals to hours, minutes and seconds
        hour = dec * 24
        minutes = (hour % 1) * 60
        seconds = (minutes % 1) * 60

        try:
            transformed_date = substituted_date.replace(hour=int(hour), minute=int(minutes), second=int(seconds))
            print('El valor de dt es: ', transformed_date)
            return transformed_date

        except Exception:
            print(f'Error en los valores: {hour}, {minutes} y {seconds}')

    def date_to_float(self, date):
        """
        Transforms from a date format to the Julian Microsoft (Excel understandable) format (valuetodate).
        F.Ex: date_to_float(datetime(2020, 9, 8, 9, 44, 33))  => 44052.4059375
        :param date: [datetime] date desired to transform, F.Ex: datetime(2020, 9, 8, 9, 44, 33)
        :return: [float] Transformed date in valuetodate format, F.Ex: 44052.4059375
        """
        temp = datetime(1899, 12, 30)  # Note: not 31st Dec but 30th!
        delta = date - temp
        valuetodate = float(delta.days) + (float(delta.seconds) / 86400)
        return valuetodate

    def str_to_date(self, day_str):
        """
        Transforms a string into a datetime object
        F.Ex: '2020-09-02 00:00:01' =>  datetime(2020-09-02 00:00:01)

        :param day_str: [str] Desired date in string ISO format
        :return date_time_obj: [datetime] Desired date in datetime object format
        """
        date_time_obj = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
        return date_time_obj

    def str_to_float(self, day_str):
        """
        Transforms a string to the Julian Microsoft (Excel understandable) format (valuetodate).
        F.Ex: str_to_date('2020-09-02 00:00:01') =>  44052.4059375
        :param day_str: [str] Desired date in ISO format
        :return valuetodate: [float] Desired date in valuetodate (Excel format)
        """
        date = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
        valuetodate = self.date_to_float(date)
        return valuetodate

    def minutes_to_float(self, minutes):
        """
        Gets the valuedate form of the desired increment.
        F.Ex: minutes_to_float(minutes=30) => 0.020833333335758653
        :param minutes: [int] Desired increment in minutes. F.Ex: 30 => 30 minutes, half an hour.
        :return delta: [float] Increment in valuetodate form. F.Ex: 0.020833333335758653
        """
        # Transform first random starting date
        d1 = self.date_to_float(datetime(2020, 9, 8, 0, 0))
        # Transform second random same date but added the increment
        d2 = self.date_to_float(datetime(2020, 9, 8, 0, minutes))
        # Get the difference (in valuetodate format)
        delta = d2 - d1
        return delta