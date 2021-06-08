from email_sender.databases.database import DataBase


class DataGate:

    def __init__(self):
        self.db_SSL1_started = DataBase(kind='Started',
                                        line='SSL1',
                                        host='10.156.8.3',
                                        database='qiastatdxssl',
                                        user='pilot',
                                        password='READStat2020',
                                        table='serialnumber',
                                        time_field='Time'
                                        )

        self.db_SSL3_started = DataBase(kind='Started',
                                        line='SSL1',
                                        host='10.156.12.33',
                                        database='qiastatdxssl',
                                        user='pilot',
                                        password='READStat2020',
                                        table='serialnumber',
                                        time_field='Time'
                                        )

        self.db_SSL1_finished = DataBase(kind='Finished',
                                         line='SSL1',
                                         host='10.156.9.72',
                                         database='qiastatdxssl',
                                         user='pilot',
                                         password='READStat2020',
                                         table='pouch',
                                         time_field='Date')

        self.db_SSL3_finished = DataBase(kind='Finished',
                                         line='SSL3',
                                         host='10.156.12.27',
                                         database='qiastatdxssl',
                                         user='pilot',
                                         password='READStat2020',
                                         table='pouch',
                                         time_field='Date')

        self.databases = {'Started': {'SSL1': self.db_SSL1_started,
                                      'SSL3': self.db_SSL3_started},
                          'Finished': {'SSL1': self.db_SSL1_finished,
                                       'SSL3': self.db_SSL3_finished}}
