from flask import Flask, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Visitor (%s)' % self.name

     
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    visitor = db.relationship('Visitor',
        backref=db.backref('visits', lazy='dynamic'))
        
    def __init__(self, visitor, date):
        self.visitor = visitor
        self.date = date
          
    def __repr__(self):
        return 'Visit (%s, %s)' % (self.visitor.name, self.date)


@app.route("/", methods=["GET"])
def index():
    not_checked_in = Visitor.query.all() # todo
    checked_in = not_checked_in # todo
    return render_template("index.html", 
                           checked_in=checked_in, not_checked_in=not_checked_in,
                           visits=Visit.query.all())

@app.route("/checked_in", methods=["POST"])
def check_in():
    visitor_id = request.form['visitor_id']
    visitor = Visitor.query.get(visitor_id)
    now = date.today()
    new_visit = Visit(visitor, now)
    db.session.add(new_visit)
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route("/create_visitor", methods=["POST"])
def create_visitor():
    new_visitor = Visitor(request.form['name'])
    db.session.add(new_visitor)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

