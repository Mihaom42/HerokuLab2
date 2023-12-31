from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lzfrvzpibdnern:d44df762448bfc51210d94c30cd365fd2b189185ac1b900fe0b9f57226acd620@ec2-44-215-22-37.compute-1.amazonaws.com:5432/dan84hpffdpf0n'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    new_event = Event(title=title, date=date)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
