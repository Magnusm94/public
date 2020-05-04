import psycopg2
import pandas as pd


# Class for not having to deal with SQL anymore.
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
        self.data = None

    # Creates a connection with the database
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db_name, user=self.sb_user,
                password=self.db_pass, host=self.db_host,
                port=self.db_port)
            print('Connection established')
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError:
            print('Connection failed')

    def commit(self, command, fetch=False):
        worked = None
        self.connect()
        self.cur.execute(command)
        try:
            if fetch:
                self.data = self.cur.fetchall()
            else:
                self.conn.commit()
            worked = True
        except:
            worked = False
        finally:
            self.conn.close()
            return worked

    # Attempts to create a new table: tablename
    # Kwargs is used for. For example age='int'
    # NULL is accepted for all values.
    def maketable_null_accepted(self, tablename, **kwargs):
        # The first part is writing the SQL code required to create a table from kwargs info.
        strings = []
        tablestr = 'CREATE TABLE %s\n(\nID SERIAL,\n' % tablename
        for x, z in kwargs.items():
            strings.append('%s %s,\n' % (str(x).upper(), str(z).upper()))
        strings[-1] = strings[-1].replace(',', '')
        last_part = ')'
        command = tablestr
        for item in strings:
            command += item
        command += last_part
        try:
            if self.commit(command):
                print('Table created successfully.')
            else:
                print('Failed to create table.')
        except:
            print('Table already exists')

    # Same as previous, but does not accept null.
    def maketable_no_null(self, tablename, **kwargs):
        # The first part is writing the SQL code required to create a table from kwargs info.
        strings = []
        tablestr = 'CREATE TABLE %s\n(\nID SERIAL,\n' % tablename
        for x, z in kwargs.items():
            strings.append('%s %s NOT NULL,\n' % (str(x).upper(), str(z).upper()))
        strings[-1] = strings[-1].replace(',', '')
        last_part = ')'
        command = tablestr
        for item in strings:
            command += item
        command += last_part
        try:
            if self.commit(command):
                print('Table created successfully.')
            else:
                print('Failed to create table.')
        except:
            print('Table already exists')

    def insert(self, tablename, **kwargs):
        items = []
        values = []
        for x, z in kwargs.items():
            items.append(x + ', ')
            values.append(z)
        items[-1] = items[-1].replace(', ', '')
        values = "".join(str(values))
        values = values.replace('[', '(')
        values = values.replace(']', ')')
        items = "".join(items)
        items = '(%s)' % items
        command = 'INSERT INTO %s %s VALUES %s' % (tablename, items, values)
        if self.commit(command):
            print('Data inserted successfully')
        else:
            print('Failed to insert data.')

    def select(self, tablename, *args):
        command = 'SELECT '
        for arg in args[:-1]:
            command += str(arg).upper() + ', '
        command += str(args[-1]).upper() + ' FROM %s' % str(tablename).upper()
        if self.commit(command, fetch=True):
            print('Successfully grabbed data.')
            return self.data
        else:
            print('Failed to obtain data.')

    def dataframe(self, tablename, *args):
        df = pd.DataFrame(self.select(tablename, *args))
        return df

    def update(self, tablename, ID, **kwargs):
        items = []
        for x, z in kwargs.items():
            items.append("%s = '%s', " % (x, z))
        items[-1] = str(items[-1].replace(', ', ''))
        items = "".join(items)
        command = 'UPDATE %s set %s WHERE %s' % (tablename, items, ID)

        if self.commit(command):
            print('Successfully updated table')
        else:
            print('Failed to update table')

    def delete(self, tablename, ID):
        command = 'DELETE FROM %s WHERE %s' % (tablename, ID)
        if self.commit(command):
            print('Deleted successfully.')
        else:
            print('Failed to delete.')


""""
Example of how to call this function so far.

Initialize class
a = postgresql()

Make a new table. Note that ID is set to serial.
a.maketable('complete', v1='int', v2='float', v3='text')

Insert into a table
a.insert('complete', v1=1000, v2=13.37, v3='some text')

Select data from given table
print(a.select('complete', 'v1', 'v2', 'v3'))

Get dataframe of table
print(a.dataframe('complete', 'v1', 'v2', 'v3'))

Update table info
a.update('complete', 'v1 = 2000', v2=1.5, v3='other text')

Delete table info
a.delete('complete', 'v1=2000')
"""