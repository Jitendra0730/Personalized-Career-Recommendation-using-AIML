from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=20, message="Username must be between 4 and 20 characters")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords must match")
    ])

class CareerProfileForm(FlaskForm):
    # Personal Information
    full_name = StringField('Full Name', validators=[
        DataRequired(), 
        Length(min=2, max=100, message="Full name must be between 2 and 100 characters")
    ])
    age = IntegerField('Age', validators=[
        Optional(), 
        NumberRange(min=16, max=100, message="Age must be between 16 and 100")
    ])
    
    # Professional Information
    current_profession = StringField('Current Profession', validators=[
        Optional(), 
        Length(max=100)
    ])
    area_of_interests = TextAreaField('Areas of Interest', validators=[
        Optional(), 
        Length(max=1000, message="Please keep interests under 1000 characters")
    ], description="Describe your professional interests, hobbies, and passions")
    
    career_goals = TextAreaField('Career Goals', validators=[
        Optional(), 
        Length(max=1000, message="Please keep career goals under 1000 characters")
    ], description="What do you want to achieve in your career?")
    
    current_skills = TextAreaField('Current Skills', validators=[
        Optional(), 
        Length(max=1000, message="Please keep skills under 1000 characters")
    ], description="List your technical and soft skills")
    
    # Work Preferences
    preferred_work_environment = SelectField('Preferred Work Environment', choices=[
        ('', 'Select an option'),
        ('office', 'Office'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('fieldwork', 'Field Work'),
        ('no_preference', 'No Preference')
    ], validators=[Optional()])
    
    expected_salary_min = IntegerField('Minimum Expected Salary (Annual)', validators=[
        Optional(), 
        NumberRange(min=0, max=10000000, message="Please enter a valid salary amount")
    ])
    
    expected_salary_max = IntegerField('Maximum Expected Salary (Annual)', validators=[
        Optional(), 
        NumberRange(min=0, max=10000000, message="Please enter a valid salary amount")
    ])
    
    # Additional Information
    education_level = SelectField('Education Level', choices=[
        ('', 'Select an option'),
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    years_of_experience = IntegerField('Years of Experience', validators=[
        Optional(), 
        NumberRange(min=0, max=50, message="Years of experience must be between 0 and 50")
    ])
    
    willing_to_relocate = BooleanField('Willing to Relocate')
