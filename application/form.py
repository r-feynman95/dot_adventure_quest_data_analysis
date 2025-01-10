from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class UserInputForm(FlaskForm):                                             #UserInputForm is the child of FlaskForm. Inheritance
    type = SelectField('Type', validators= [DataRequired()], 
                       choices=[('income', 'income'), 
                                ('expense', 'expense')
                                ])
    category = SelectField('Category', validators= [DataRequired()], 
                    choices=[('rent', 'rent'), 
                            ('salary', 'salary'),
                            ('investment', 'investment'),
                            ('side_hustle', 'side_hustle')
                            ])

    amount = IntegerField("Amount", validators = [DataRequired()])

    submit = SubmitField("Generate Report")