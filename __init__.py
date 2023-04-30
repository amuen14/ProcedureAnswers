# from flask import Flask
# from models import db
# app = Flask(__name__)
# db.init_app(app)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class PrimaryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<PrimaryItem %r>' % self.name

@app.route('/')
def index():
    items = PrimaryItem.query.all()
    return '<br>'.join([item.name for item in items])

if __name__ == '__main__':
    app.run(debug=True)
