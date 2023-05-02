from peewee import *
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect
import datetime
import numpy as np

# Define your database
db = SqliteDatabase('my_database.db')
app = Flask(__name__)

print("does this work?")

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

def count_nan(series):
    return np.isnan(series).sum()


def format_df():
    str = 'C:\\Users\\223037435\\Desktop\\Plant II\\df.csv'
    df = pd.read_csv(str)
    df['Open_Actions'] = df['is_date1_after_date2']
    df['DUEDATE'] = pd.to_datetime(df['DUEDATE'])
    today = datetime.datetime.now().date()
    df['Over_Due'] = ((df['DUEDATE'].dt.date < today) & (df['COMPDATE'].isna())).astype(int)
    df = df.rename(columns={'is_date1_after_date2': 'Late'})
    df['Completed'] = df['Late'] + df['On_Time']
    df0 = df
    df =df.groupby(['Category', 'PRIM_DESC', 'PRIM_OWNER']).agg({'On_Time': 'sum', 'Late': 'sum','Open_Actions': count_nan, 'Completed':'sum', 'Over_Due': 'sum'})
    df = pd.DataFrame(df).reset_index()
    df['Perc_On_Time'] = (df['On_Time'] / df['Completed'] *100).map('{:.1f}%'.format)
    df['Perc_On_Time'] = df['Perc_On_Time'].replace('nan%','')

    return df


@app.route('/Y', methods=['POST'])
def Y():
    print("X")
    category = request.form['category']
    print(category)
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def display_table():
    #users = User.select()
    category = 'CID'
    #lst = LST.select()
    if request.method == 'POST' and 'Display Table' in request.form.values():
        print("X")
    if request.method == 'POST':
        category = request.form['category']
        print(category)


    #create_table_sqlite()
    conn = get_db_connection()
    # LISTS = conn.execute('SELECT * FROM LISTS').fetchall()
    sql = 'SELECT DISTINCT CATEGORY, PRIM_DESC, PRIM_OWNER FROM LISTS'
    # LISTS = conn.execute('SELECT DISTINCT CATEGORY, PRIM_DESC, PRIM_OWNER FROM LISTS').fetchall()

    # sql='SELECT PRIM_DESC, PRIM_OWNER, COUNT(*) AS "Total Count", COUNT(DUEDATE) AS "Total Open" '\
    #     'FROM LISTS '\
    #     'GROUP BY PRIM_DESC, PRIM_OWNER'

# ###################
#     # Begin transaction
#     conn.execute('BEGIN')
#
#     # Add column to the table
#     conn.execute('ALTER TABLE LISTS RENAME COLUMN "On Time" TO On_Time')
    # conn.execute('ALTER TABLE LISTS RENAME COLUMN "Over Due" TO Over_Due')
#
#     # Update the values in the column
    sql1="UPDATE LISTS SET is_date1_after_date2 = (strftime('%Y-%m-%d', 'now') < date(COMPDATE));"
    sql1 = "UPDATE LISTS SET is_date1_after_date2 = date(DUEDATE) < date(COMPDATE);"
    conn.execute(sql1)
    sql1 = "UPDATE LISTS SET 'On_Time' = date(DUEDATE) > date(COMPDATE);"
    conn.execute(sql1)
    # sql1 = "UPDATE LISTS SET 'Over Due' = CASE WHEN date('now') > date(DUEDATE) AND COMPDATE IS NULL THEN 1 ELSE 0 END;"
    # conn.execute(sql1)

    # conn.execute('UPDATE LISTS SET is_date1_after_date2 = (DUEDATE > COMPDATE)')
#
#     # Commit the transaction
#     conn.commit()
# ###################

    sql='SELECT PRIM_DESC, PRIM_OWNER, COUNT(*) AS "Total Count", COUNT(DUEDATE) AS "Total Open" '\
        'FROM LISTS '\
        'GROUP BY PRIM_DESC, PRIM_OWNER'

    sql ="SELECT PRIM_Owner, PRIM_DESC, "\
       "SUM(CASE WHEN is_date1_after_date2 = 1.0 THEN 1 ELSE 0 END) AS 'Completed On Time', " \
         "SUM(CASE WHEN is_date1_after_date2 = 0.0 THEN 1 ELSE 0 END) AS 'Not Completed On Time', " \
         "SUM(CASE WHEN is_date1_after_date2 IS NULL THEN 1 ELSE 0 END) AS 'Open Actions' " \
       "FROM LISTS "\
        "GROUP BY PRIM_OWNER, PRIM_DESC;"

    sql2 = 'SELECT * FROM LISTS'


    # print(sql)


    df = pd.read_sql_query(sql, conn)
    df2 = pd.read_sql_query(sql2,conn)
    # print(df2)
    # print(df)
    df2.to_csv('C:\\Users\\223037435\\Desktop\\Plant II\\df.csv', index=False)
    # print(category)
    df3 = format_df()

    # print(df3)
    df3 = df3[df3['Category']==category]
    # print(df3)
    # conn.execute('DROP TABLE IF EXISTS mytable')

    df3.to_sql('mytable', conn, if_exists='replace', index=False)

    LISTS2 = conn.execute(f'SELECT DISTINCT CATEGORY, PRIM_DESC, PRIM_OWNER,Open_Actions,Over_Due,Perc_On_Time FROM mytable WHERE CATEGORY = "{category}"').fetchall()

    cursor = conn.cursor()
    rows = LISTS2
    # for r in rows:
    #     print(f'x  {r}')


    conn.close()
    return render_template('table2.html', lst=LISTS2)






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
