import bcrypt
from Personal_projects import postgresql_made_easy


# This function checks if a user exists in a database.
# If it exists, it checks if the salted password stored in database matches the input.
def login():
    sql = postgresql_made_easy.postgresql()
    username = str(input('Username: ')).lower()
    password = str(input('Password: ')).encode()
    users = sql.dataframe('login', 'username', 'password')
    check = (users[users[0] == username])
    try:
        db_pw = check.iloc[0, 1]
        if bcrypt.checkpw(password, db_pw.encode()):
            print('Logged in')
            return True
        else:
            print('Wrong password')
            return False
    except IndexError:
        print("User doesn't exist")
        return False


# Allows a non-existing user to register with login. Stores hashed password in database
def register():
    sql = postgresql_made_easy.postgresql()
    username = input('Username: ').lower()
    password = input('Password: ')
    if password == input('Repeat password: '):
        check = sql.dataframe('login', 'username')
        if len(check[check[0] == username]):
            print('User already exists')
            return False
        sql.insert('login', username=username)
        ID = "username = '%s'" % username
        if sql.update_encrypted('login', ID, password=password):
            print('User registered')
            return True
    else:
        print("Passwords didn't match")
        return False