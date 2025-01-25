from application import db
from datetime import datetime, timezone 

class IncomeExpenses(db.Model):                                                             # Inherits db.Model, creates a table in the database db
    id = db.Column(db.Integer, primary_key = True)                                          # Standard SQLAlchemy Object Relation Mapping pattern class = table attributes = columns
    type = db.Column(db.String(30), default = 'income', nullable = False)
    category = db.Column(db.String(30), default= 'rent', nullable = False)
    date = db.Column(db.DateTime, default = datetime.now(timezone.utc), nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    def __str__(self):
        return self.id     # when an object of this class is printed as a string use the primary key id
    
# Database model for cleaned log file
class Log(db.Model):
    user = db.Column(db.Integer, primary_key = True)
    start = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    seed = db.Column(db.Integer, nullable = False)
    problem_number = db.Column(db.Integer, nullable = False)
    problem_type = db.Column(db.String(8), nullable = False)
    problem_status = db.Column(db.String(50), nullable = False)
    response = db.Column(db.String(100), nullable = True)

    def __str__(self):
        return self.user     # when an object of this class is printed as a string use the primary key id