from email_sender.databases.database import DataBase

class DBPouch(DataBase):

    def __init__(self, kind, line, host, database, user, password, table, time_field):
        super().__init__(kind, line, host, database, user, password, table, time_field)


