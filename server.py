from flask import Flask, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date, datetime
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


# Models:
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    street_address = db.Column(db.String(80))
    zip_code = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    city = db.Column(db.String(80))

    def __init__(self, first_name, last_name, gender, street_address, zip_code, date_of_birth, city):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.street_address = street_address
        self.zip_code = zip_code
        self.date_of_birth = date_of_birth
        self.city = city

    def __repr__(self):
        return 'Visitor (%s %s)' % (self.first_name, self.last_name) 
       
    def name(self):
        return '%s %s' % (self.first_name, self.last_name) 
       
    def here_today(self):
        return self.visits.filter(Visit.date == date.today()).count() > 0

     
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
        return 'Visit (%s %s, %s)' % (self.visitor.first_name, self.visitor.last_name, self.date)


# Views:
@app.route("/", methods=["GET"])
def index():
    all_visitors = Visitor.query.all()
    here = list(filter(lambda v: v.here_today(), all_visitors))
    not_here = filter(lambda v: not v.here_today(), all_visitors)
    not_here = list(sorted(not_here, key=lambda v:v.first_name))
    not_here_by_letter = OrderedDict()
    for v in not_here:
        letter = v.first_name[0].upper()
        if letter not in not_here_by_letter:
            not_here_by_letter[letter] = []
        not_here_by_letter[letter].append(v)
    return render_template("index.html", 
                           here=here, not_here_by_letter=not_here_by_letter,
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
    
@app.route("/create_visitor", methods=["GET"])
def visitor_form():
    return render_template("create_visitor.html")
      
@app.route("/create_visitor", methods=["POST"])
def create_visitor():
    form = {key: values for key, values in request.form.items()}
    form["date_of_birth"] = datetime.strptime(form["date_of_birth"], "%Y-%m-%d").date()
    new_visitor = Visitor(**form)
    db.session.add(new_visitor)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

