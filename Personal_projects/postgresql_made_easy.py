import psycopg2

# todo: func for parsing info, calling info, deleting info


class postgresql:
    def __init__(self):

        # Login information for database
        self.db_name = ""
        self.sb_user = ""
        self.db_pass = ""
        self.db_host = ""
        self.db_port = ""

        self.conn = None
        self.cur = None
        self.attempts = 0

    # Creates a connection with the database
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db_name, user=self.sb_user,
                password=self.db_pass, host=self.db_host,
                port=self.db_port)
            print('Connection established')
        except psycopg2.OperationalError:
            print('No connection')
            exit()
        self.cur = self.conn.cursor()

    # Attempts to create a new table: tablename
    # Kwargs is used for. For example age='int'
    def maketable(self, tablename, **kwargs):
        self.connect()

        # The first part is writing the SQL code required to create a table from kwargs info.
        strings = []
        tablestr = 'CREATE TABLE %s\n(\nID INT PRIMARY KEY NOT NULL,\n' % tablename
        for x, z in kwargs.items():
            strings.append('%s %s NOT NULL,\n' % (str(x).upper(), str(z).upper()))
        strings[-1] = strings[-1].replace(',', '')
        last_part = ')'
        result = tablestr
        for item in strings:
            result += item
        result += last_part

        # Attempts to make the table.
        try:
            self.cur.execute(result)
            self.conn.commit()
            print('Table created successfully')
            self.attempts = 0
            self.conn.close()
        except:
            if self.attempts > 2:
                self.attempts = 0
                print('3 failed attempts. Exiting code.')
                exit()
            print('Failed to make table. Trying again')
            self.attempts += 1
            self.maketable(tablename, **kwargs)


# example of how to call this function so far.
a = postgresql()
a.maketable('tablename', name='text', hometown='text', age='int', weight='float')
