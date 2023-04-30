from flask import Flask, render_template, request, redirect, url_for
from peewee import *

# Create a Peewee database instance - replace "database.db" with your desired database name
db = SqliteDatabase('database.db')

# Create a Peewee model for the Action Items table
class ActionItem(Model):
    description = CharField()
    owner = CharField()
    due_date = DateField()
    num_open_sub_items = IntegerField()
    is_open = BooleanField()

    class Meta:
        database = db

# Create the Action Items table if it doesn't exist
db.create_tables([ActionItem])

# Initialize the Flask application
app3 = Flask(__name__)

# Define a route for the main table of Action Items
# @app3.route('/')
# def index():
#     action_items = ActionItem.select()
#     return render_template('index3.html', action_items=action_items)


@app3.route('/index3/<int:id>')
def index_item(id):
    # Retrieve the main action item based on the id parameter
    main_item = ActionItem.get_by_id(id)

    # Retrieve the associated sub items for the main item
    sub_items = ActionItem.select().where(ActionItem.parent_item_id == id)

    # Render the show.html template with the main item and associated sub items
    return render_template('show.html', main_item=main_item, sub_items=sub_items)



# Define a route for adding a new Action Item
@app3.route('/add', methods=['POST'])
def add_action_item():
    description = request.form['description']
    owner = request.form['owner']
    due_date = request.form['due_date']
    num_open_sub_items = 0
    is_open = True

    action_item = ActionItem.create(
        description=description,
        owner=owner,
        due_date=due_date,
        num_open_sub_items=num_open_sub_items,
        is_open=is_open
    )

    return redirect(url_for('index'))

# Define a route for clicking on an Action Item and displaying its sub-items
@app3.route('/<int:action_item_id>')
def show_action_item(action_item_id):
    action_item = ActionItem.get(ActionItem.id == action_item_id)
    sub_items = SubItem.select().where(SubItem.action_item_id == action_item_id)
    return render_template('show.html', action_item=action_item, sub_items=sub_items)

# Define a route for adding a new sub-item to an Action Item
@app3.route('/<int:action_item_id>/add_sub_item', methods=['POST'])
def add_sub_item(action_item_id):
    description = request.form['description']
    owner = request.form['owner']
    due_date = request.form['due_date']

    sub_item = SubItem.create(
        description=description,
        owner=owner,
        due_date=due_date,
        action_item_id=action_item_id
    )

    action_item = ActionItem.get(ActionItem.id == action_item_id)
    action_item.num_open_sub_items += 1
    action_item.save()

    return redirect(url_for('show_action_item', action_item_id=action_item_id))

# Define a route for returning to the main table from the sub-item table
@app3.route('/<int:action_item_id>/return_to_main')
def return_to_main(action_item_id):
    return redirect(url_for('index'))

# Define a Peewee model for the sub-items table
class SubItem(Model):
    description = CharField()
    owner = CharField()
    due_date = DateField()
    action_item_id = ForeignKeyField(ActionItem, backref='sub_items')

    class Meta:
        database = db

# Create the sub-items table if it doesn't exist
db.create_tables([SubItem])

# Run the Flask application
if __name__ == '__main__':
    app3.run()
