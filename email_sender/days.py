from datetime import datetime, timedelta


class Days:
    def __init__(self, start_date, edge_parameter):

        """
        Gets a list from a date. The length is the same as the desired days to study
        F. Ex:  [datetime(2020, 9, 18), ..., datetime(2020, 9, 22)]
        :param edge_parameter:
        [int] Quantity of days to show (returned list length). F.Ex: 5
        :return dates: [list: datetime] Ordered list from older date to newer of the dates in string format.
        """
        # Clean the hours, minutes and seconds from the datetime object
        start_date = datetime(year=start_date.year, month=start_date.month, day=start_date.day)

        # Complete list
        if isinstance(edge_parameter, int):
            dates_list = [start_date + timedelta(days=i) for i in range(edge_parameter)]
            self.dates_list = dates_list

        elif isinstance(edge_parameter, datetime):
            quantity_days = (edge_parameter - start_date).days + 1
            dates_list = [start_date + timedelta(days=i) for i in range(quantity_days)]
            self.dates_list = dates_list
        else:
            raise ValueError('Impossible create the array with current parameters')

    def get_list(self):
        return self.dates_list

    def get_string_list(self):
        """
        Splits a list of datetime entries into strings with only the day date and month.

        F.Ex: [datetime(2021, 3, 8), datetime(2021, 3, 9), datetime(2021, 3, 10),
        datetime(2021, 3,11), datetime(2021, 3, 12), datetime(2021, 3, 13). datetime(2021, 3, 14) =>
        ['11/3', '12/3', '13/3', '14/3', '15/3', '16/3', '17/3']
        :param dates_list: [list: [datetime]] Dates to transform to strings
        :return str_dates_list: List of dates in string format as 'dd/mm'
        """

        str_dates_list = [date.strftime('%d/%m') for date in self.dates_list]

        return str_dates_list