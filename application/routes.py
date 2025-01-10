from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpenses
import json

@app.route("/")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()               # Retrieve all entries as a list of objects ordered by date desc
                                                                                            # Each entry in entries is an IncomeExpense object with attributes that correspond to columns in db table
    return render_template('index.html', title = 'index', entries = entries)                # Pass the entries information to the html file

@app.route("/add", methods = ["GET", "POST"])
def add_expense():
    form = UserInputForm()                                              # Creates an instance of the UserInputForm, a child of flask_wtf FlaskForm
    if form.validate_on_submit():                                       # Returns true if all validators (DataRequired checks) are true
        entry = IncomeExpenses(type = form.type.data,                   # Creates an instance of IncomeExpenses representing a new row in the Income Expenses class
                               amount = form.amount.data,
                               category = form.category.data,
                               )
        db.session.add(entry)                                           # Session is temporary holding area for database changes that need to be committed
        db.session.commit()                                             # Add current session to the income_expenses table
        flash("Successful Entry", 'success')                            # flash is a flask global function that sens one-time message

        return redirect(url_for('index'))                               # If form valid, return user to index page

    return render_template("add.html", title = 'add', form = form)      # I do not understand how jinja2 is receiving this form...

@app.route("/delete/<int:entry_id>")                                    # Defines dynamic route where entry_id is a variable int: converter ensures that the value extracted is an integer
def delete(entry_id):                                                   # This information is passed from index.html using the url_for() flask function
        entry = IncomeExpenses.query.get_or_404(int(entry_id))          # Attempt to get or instead returns "404 not found" error
        db.session.delete(entry)                                        # Delete the entry from db
        db.session.commit()                                             # Commit changes to db
        flash("Delete was success", 'success')                          # Flash the user success
        return redirect(url_for('index'))                               # Bring the user back to index page


@app.route("/dashboard")
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_expense = []
    for total_amount, _ in income_vs_expense:
         income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []

    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template("dashboard.html", 
                           title = 'dashboard',
                           income_vs_expenses = json.dumps(income_expense),
                           over_time_expenditure = json.dumps(over_time_expenditure),
                           dates_label = json.dumps(dates_label)
                           )

@app.route("/upload")
def upload():
    
    return redirect(url_for('index'))