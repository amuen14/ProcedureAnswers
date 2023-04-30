from flask import Flask, render_template, request, redirect, url_for
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField

# Initialize a database connection
db = SqliteDatabase('action_items.db')


# Define a model for the ActionItem table
class ActionItem(Model):
    description = CharField()
    owner = CharField()
    due_date = DateField()
    num_open_sub_items = IntegerField(default=0)
    is_open = CharField(default='Open')

    class Meta:
        database = db


app2 = Flask(__name__)

# Create the ActionItem table if it doesn't exist
with db:
    db.create_tables([ActionItem])


@app2.route('/')
def index():
    action_items = ActionItem.select()
    return render_template('index2.html', action_items=action_items)


@app2.route('/add_action_item', methods=['GET', 'POST'])
def add_action_item():
    if request.method == 'POST':
        ActionItem.create(
            description=request.form['description'],
            owner=request.form['owner'],
            due_date=request.form['due_date'],
            num_open_sub_items = 0,
            is_open = 'Open'
        )
        print("X")
        return redirect(url_for('index'))

    return render_template('add_action_item.html')


if __name__ == '__main__':
    app2.run(debug=True)
