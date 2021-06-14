from table_sender.databases.database import DataBase


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

        self.db_SSL1_balances = DataBase(kind='Balances',
                                         line='SSL1',
                                         host='10.156.9.78',
                                         database='resultdata',
                                         user='qiastat_ro',
                                         password='READStat2020',
                                         table='results',
                                         time_field='Time2')

        self.db_SSL3_balances = DataBase(kind='Balances',
                                         line='SSL3',
                                         host='10.156.12.26',
                                         database='resultdata',
                                         user='qiastat_ro',
                                         password='READStat2020',
                                         table='results',
                                         time_field='Time2')

        self.databases = {'Started': {'SSL1': self.db_SSL1_started,
                                      'SSL3': self.db_SSL3_started},
                          'Finished': {'SSL1': self.db_SSL1_finished,
                                       'SSL3': self.db_SSL3_finished},
                          'Balances': {'SSl1': self.db_SSL1_balances,
                                       'SSL3': self.db_SSL3_balances}}
