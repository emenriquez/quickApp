from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sampledb.db'
db = SQLAlchemy(app)

# Databse classes
class Visitor(db.Model):
    username = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    numVisits = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        if self.username:
            return f'{self.username} - {self.numVisits}' 
        else:
            return f'unknown - {self.numVisits}'



# Create tables
with app.app_context():
    db.create_all()

def createSomePeople(names):
    for name in names:
        visitor = Visitor(username=name)
        db.session.add(visitor)
    db.session.commit()

# Function to read in details for page
def readDetails(filname):
    with open(filname, 'r') as f:
        return [line for line in f]








# ROUTES
@app.route('/')
def homePage():
    name = "Me Myname"
    details = readDetails('static/details.txt')
    return render_template("base.html", name=name, aboutMe=details)

@app.route('/user/<name>')
def greet(name):
    return f'<p>Hello, {name}!</p>'

@app.route('/form', methods=['GET', 'POST'])
def formDemo():
    name = None
    if request.method == 'POST':
        name = request.form['name']
        visitor = Visitor.query.get(name)
        if visitor:
            visitor.numVisits += 1
        else:
            visitor = Visitor(username=name)
            db.session.add(visitor)
        db.session.commit()
    return render_template('form.html', name=name)

@app.route("/visitors")
def visitors():
    # createSomePeople(['Amy', "Barry", "Chicklet"]) # Test for quick add
    people = Visitor.query.all()
    return render_template('visitors.html', people=people)

if __name__ == '__main__':
    app.run(debug=True)
