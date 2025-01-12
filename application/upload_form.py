from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired 

class logUploadForm(FlaskForm):
        log = FileField(
                'Upload user interaction file',
                    validators =[
                            FileRequired(), # Ensure file provided                                          
                            FileAllowed(['log', 'Only .log files are allowed!'])    # Restrict to .log
                    ]
        )               

        submit = SubmitField('Upload')