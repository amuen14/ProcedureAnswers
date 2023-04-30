import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify
from peewee import *
import datetime
import pandas as pd


# define the database
db = SqliteDatabase('tasks.db')

app = Flask(__name__)

class BaseModel(Model):
    class Meta:
        database = db

class PrimaryAction(BaseModel):
    primary_desc = CharField()
    primary_owner = CharField()
    sub_desc = CharField()
    sub_owner = CharField()
    sub_due_date = DateField()


    # description = CharField()
    # owner = CharField()
    # due_date = DateField()


class Subaction(BaseModel):
    primary_action = ForeignKeyField(PrimaryAction, backref='subactions')
    description = CharField()
    owner = CharField()
    due_date = DateField()

# create tables if they don't exist
db.create_tables([PrimaryAction, Subaction])

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.route('/')
def index():
    # retrieve all primary actions
    #primary_actions = PrimaryAction.select().order_by(PrimaryAction.due_date)
    primary_actions = PrimaryAction.select().order_by(PrimaryAction.primary_desc)

    # highlight rows if due date is past
    # for primary_action in primary_actions:
    #     if primary_action. < datetime.date.today():
    #         primary_action.row_class = 'bg-warning'
    #
    #     for subaction in primary_action.subactions:
    #         if subaction.due_date < datetime.date.today():
    #             subaction.row_class = 'bg-warning'

    return render_template('index.html', primary_actions=primary_actions)


@app.route('/unique_values', methods=['GET'])
def unique_values():
    #primary_actions = PrimaryAction.select().order_by(PrimaryAction.due_date)


    print("X")
    db.close()
    db1 = SqliteDatabase('tasks.db')
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(tables)
    #
    #
    query = f'SELECT * FROM primaryaction'

    df = pd.read_sql_query(query, conn)


    print(df)
    # print(df)
    # Get data for the table
    # ...
    # Extract unique values from the first column
    #unique_values = set(row[0] for row in primary_actions)
    x="Y"
    return x #jsonify(list(df))


@app.route('/search')
def search():
    query = request.args.get('q')

    # search primary actions by description
    primary_actions = PrimaryAction.select().where(PrimaryAction.description.contains(query))

    return render_template('index.html', primary_actions=primary_actions)





@app.route('/add-primary-action', methods=['GET', 'POST'])
def add_primary_action():
    if request.method == 'POST':
        PrimaryAction.create(
            description=request.form['primary_desc'],
            owner=request.form['primary_owner'],
            #due_date=request.form['due_date']
        )
        return redirect(url_for('index'))

    return render_template('add_primary_action.html')


@app.route('/edit_primary_action/<int:primary_action_id>', methods=['GET', 'POST'])
def edit_primary_action(primary_action_id):
    primary_action = PrimaryAction.get_or_404(id=primary_action_id)

    if request.method == 'POST':
        # update primary action details
        primary_action.description = request.form['description']
        primary_action.owner = request.form['owner']
        primary_action.due_date = request.form['due_date']
        primary_action.save()

        return redirect(url_for('index'))

    return render_template('edit_primary_action.html', primary_action=primary_action)


@app.route('/delete_primary_action/<int:primary_action_id>', methods=['POST'])
def delete_primary_action(primary_action_id):
    primary_action = PrimaryAction.get_or_404(id=primary_action_id)

    # delete primary action and its subactions
    Subaction.delete().where(Subaction.primary_action == primary_action.id).execute()
    primary_action.delete_instance()

    return redirect(url_for('index'))


@app.route('/add_subaction/<int:primary_action_id>', methods=['GET', 'POST'])
def add_subaction(primary_action_id):
    primary_action = PrimaryAction.get_or_404(id=primary_action_id)

    if request.method == 'POST':
        # create new subaction
        Subaction.create(
            primary_action=primary_action,
            description=request.form['description'],
            owner=request.form['owner'],
            due_date=request.form['due_date']
        )

        return redirect(url_for('index'))

    return render_template('add_subaction.html', primary_action=primary_action)


@app.route('/edit_subaction/<int:subaction_id>', methods=['GET', 'POST'])
def edit_subaction(subaction_id):
    subaction = Subaction.get_or_404(id=subaction_id)

    if request.method == 'POST':
        # update subaction details
        subaction.description = request.form['description']
        subaction.owner = request.form['owner']
        subaction.due_date = request.form['due_date']
        subaction.save()

        return redirect(url_for('index'))

    return render_template('edit_subaction.html', subaction=subaction)


@app.route('/delete_subaction/<int:subaction_id>', methods=['POST'])
def delete_subaction(subaction_id):
    subaction = Subaction.get_or_404(id=subaction_id)

    # delete subaction
    subaction.delete_instance()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
