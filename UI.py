from peewee import *
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect

# Define your database
db = SqliteDatabase('my_database.db')
app = Flask(__name__)

# Create tables


#  #Insert records
# User.create(username='john_doe', email='john@example.com', password='password123')
# User.create(username='jane_doe', email='jane@example.com', password='password456')



# Insert a record with an email that already exists
# existing_user = User.get(User.email == 'john@example.com')
# existing_user.username = 'john_doe_updated'
# existing_user.password = 'new_password123'
# existing_user.save()

# print("X")
# #db.close()
# #db1 = SqliteDatabase('tasks.db')
# conn = sqlite3.connect('my_database.db')
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print(tables)
#
# query = f'SELECT * FROM user'
#
# df = pd.read_sql_query(query, conn)
# print(df)

def demo(str):
    conn = sqlite3.connect(str)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    query = f'SELECT * FROM user'
    df = pd.read_sql_query(query, conn)

    return df

# Define your models
class User(Model):
    username = CharField(unique=False,)
    email = CharField(unique=False)
    password = CharField(unique=False)

    class Meta:
        database = db

db.create_tables([User])


def create_table_sqlite():
    # Connecting to sqlite
    conn = sqlite3.connect('my_database.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS LISTS")

    # Creating table as per requirement
    sql = '''CREATE TABLE LISTS(
       ID int NOT NULL AUTO_INCREMENT,
       Category CHAR(20) NOT NULL,
       PRIM_DESC CHAR(20),
       PRIM_OWNER CHAR(20),
       ACTION_DESC CHAR(20),
       ACTION_OWNER CHAR(20),
       DUEDATE text,
       COMPDATE text
    )'''

    cursor.execute(sql)
    print("Table created successfully........")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()



def create_table_sqlite():
    # Connecting to sqlite
    conn = sqlite3.connect('my_database.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS LISTS")

    # Creating table as per requirement
    sql = '''CREATE TABLE LISTS(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       Category CHAR(20) NOT NULL,
       PRIM_DESC CHAR(20),
       PRIM_OWNER CHAR(20),
       ACTION_DESC CHAR(20),
       ACTION_OWNER CHAR(20),
       DUEDATE text,
       COMPDATE text
    )'''

    cursor.execute(sql)
    print("Table created successfully........")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()






class LST(Model):
    id = AutoField()
    Category = CharField(unique=False, null=True)
    Prim_desc = CharField(unique=True, null=True)
    Prim_owner = CharField(unique=False, null=True)
    Action_desc = CharField(unique=False, null=True)
    Action_Owner = CharField(unique=False, null=False)
    Due_Date = DateField()
    Complete_Date = DateField()

    class Meta:
        database = db


#create_table_sqlite()
db.create_tables([LST])



# def display_table():
#     # Get all users from the database
#     users1 = User.select()
#     # Convert the users into a list of dictionaries
#     user_dicts = [user.__dict__['__data__'] for user in users1]
#     # Convert the list of dictionaries into a Pandas dataframe
#     user_df = pd.DataFrame(user_dicts)
#     print(user_df)
#     return render_template('table.html', users=user_df.to_html(classes='table table-bordered'))
#     #return render_template('table.html', users=user_df)
#
#     #return render_template('table.html', users=user_df)
#

def get_db_connection():
    conn = sqlite3.connect('my_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def display_table():
    #users = User.select()

    #lst = LST.select()
    if request.method == 'POST' and 'Display Table' in request.form.values():
        print("X")

    #create_table_sqlite()
    conn = get_db_connection()
    # LISTS = conn.execute('SELECT * FROM LISTS').fetchall()
    sql = 'SELECT DISTINCT CATEGORY, PRIM_DESC, PRIM_OWNER FROM LISTS'
    LISTS = conn.execute('SELECT DISTINCT CATEGORY, PRIM_DESC, PRIM_OWNER FROM LISTS').fetchall()

    sql='SELECT PRIM_DESC, PRIM_OWNER, COUNT(*) AS "Total Count", COUNT(DUEDATE) AS "Total Open" '\
        'FROM LISTS '\
        'GROUP BY PRIM_DESC, PRIM_OWNER'

    df = pd.read_sql_query(sql, conn)
    print(df)
    conn.close()
    return render_template('table2.html', lst=LISTS)






@app.route('/X')
def testout():
    print('C')

    #users = User.select(User.password.distinct()).distinct()
    # users = User.select(User.password.distinct())
    #users = (User.select(User.password).distinct())
    #users = User.select(fn.DISTINCT(User.password))
    print("ZZZ")
    #X = User.select()
    #X = User.select(fn.distinct(User.password))
    print("Z111")
    #X = User.select(User.username,User.email,User.password).distinct().where(User.password).distinct()
    X = User.select(User.password).distinct

    #distinct_list = QSales.select(QSales.account, QSales.tax_code).distinct().where(QSales.trans_num == 3717)
    for user in X:
         print(user.username)
    return render_template('table.html', users=X)

    #return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    #email = 'example@example.com'

@app.route('/add_Primary_Item', methods=['POST'])
def add_P_item():
    Category = request.form['category']
    Prim_desc = request.form['Prim_desc']
    Prim_owner = request.form['Prim_owner']


    ######
    if LST.select().where(LST.Prim_desc == Prim_desc).exists():
        # Handle the case where a user with the given email already exists
        return "<script>alert('Error: a user with the email already exists.');window.location.href='/';</script>"
    ######
    #lst = LST.create(Category=Category, Prim_desc=Prim_desc,Prim_owner=Prim_owner,Action_Owner=,Action_desc= ,Due_Date=Due_Date,Complete_Date=Complete_Date)


    # lst = LST.create(Category=Category, Prim_desc=Prim_desc, Prim_owner=Prim_owner)

    # lst.save()

    db.close()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(tables)

    query = f'SELECT * FROM LISTS'

    df = pd.read_sql_query(query, conn)
    print(df)
    s=f'INSERT INTO LISTS (Category, Prim_desc, Prim_owner) VALUES ("{Category}","{Prim_desc}","{Prim_owner}")'
    cursor.execute(s)
    conn.commit()
    return redirect('/')


@app.route('/filterTBL', methods=['GET','POST'])
def filterTBL():
    item = request.args.get('primary_action_id')
    owner = request.args.get('primary_owner')
    index = int(request.args.get('index', '-1'))
    category = request.args.get('category')
    print(index)
    print(item)
    print(category)


    conn = get_db_connection()
    LISTS = conn.execute(f'SELECT * FROM LISTS where PRIM_DESC = "{item}"').fetchall()
    sql=f'SELECT * FROM LISTS where PRIM_DESC = "{item}"'
    df = pd.read_sql_query(sql, conn)
    print(df)
    conn.close()


    return render_template('table3.html', lst=LISTS, item=item, owner = owner, category = category)
    ##########################
   # return redirect('/')


@app.route('/add_action', methods=['POST'])
def add_action():






    if request.method == 'POST':
        button_name = request.form['button']
        print(button_name)
        Category = request.form['Category']
        Prim_desc = request.form['Prim_desc']
        Prim_owner = request.form['Prim_owner']
        action = request.form['action']
        action_owner = request.form['owner']
        dueDate = request.form['dueDate']
        compDate = request.form['compDate']
        ID = request.form['ID']

        if button_name == 'Back to All':
            return redirect('/')
            display_table
        if button_name == 'Update':
            s = f'UPDATE LISTS ' \
            f'SET PRIM_DESC = "{Prim_desc}",' \
            f'ACTION_DESC = "{action}",' \
            f'ACTION_OWNER = "{action_owner}",' \
            f'PRIM_OWNER = "{Prim_owner}", ' \
            f'DUEDATE = "{dueDate}", ' \
            f'COMPDATE = "{compDate}" ' \
            f'WHERE ID = {ID}'

            print(s)
        if button_name == 'delete':
            s = f'DELETE FROM LISTS WHERE ID = {ID}'
            print(ID)

        if button_name == 'Add':
            s = f'INSERT INTO LISTS (Category, Prim_desc, Prim_owner,ACTION_DESC,ACTION_OWNER,DUEDATE,COMPDATE) VALUES '\
                f'("{Category}","{Prim_desc}","{Prim_owner}","{action}","{action_owner}","{dueDate}","{compDate}")'
            print(s)
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute(s)
        conn.commit()
        conn.close()
        # conn = sqlite3.connect('my_database.db')
        # LISTS = conn.execute(f'SELECT * FROM LISTS where PRIM_DESC = "{Prim_desc}"').fetchall()

        conn = get_db_connection()
        LISTS = conn.execute(f'SELECT * FROM LISTS where PRIM_DESC = "{Prim_desc}"').fetchall()
        conn.close()




    return render_template('table3.html', lst=LISTS, item=Prim_desc, owner=Prim_owner, category=Category)
    #
    #     print(button_name)
    #     print(f'XXXX {Category}, {Prim_desc}')
    # return ''
    #
    #



if __name__ == '__main__':
    app.run(debug=True)
