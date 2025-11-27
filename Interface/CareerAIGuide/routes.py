from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse as url_parse
from app import app, db
from models import User, CareerProfile
from forms import LoginForm, RegistrationForm, CareerProfileForm

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Account created successfully! Welcome to Career Compass!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    profile = CareerProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', title='Dashboard', profile=profile)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Career profile form"""
    # Get existing profile or create new one
    career_profile = CareerProfile.query.filter_by(user_id=current_user.id).first()
    
    form = CareerProfileForm()
    
    if form.validate_on_submit():
        if career_profile:
            # Update existing profile
            career_profile.full_name = form.full_name.data
            career_profile.age = form.age.data
            career_profile.current_profession = form.current_profession.data
            career_profile.area_of_interests = form.area_of_interests.data
            career_profile.career_goals = form.career_goals.data
            career_profile.current_skills = form.current_skills.data
            career_profile.preferred_work_environment = form.preferred_work_environment.data
            career_profile.expected_salary_min = form.expected_salary_min.data
            career_profile.expected_salary_max = form.expected_salary_max.data
            career_profile.education_level = form.education_level.data
            career_profile.years_of_experience = form.years_of_experience.data
            career_profile.willing_to_relocate = form.willing_to_relocate.data
        else:
            # Create new profile
            career_profile = CareerProfile(
                user_id=current_user.id,
                full_name=form.full_name.data,
                age=form.age.data,
                current_profession=form.current_profession.data,
                area_of_interests=form.area_of_interests.data,
                career_goals=form.career_goals.data,
                current_skills=form.current_skills.data,
                preferred_work_environment=form.preferred_work_environment.data,
                expected_salary_min=form.expected_salary_min.data,
                expected_salary_max=form.expected_salary_max.data,
                education_level=form.education_level.data,
                years_of_experience=form.years_of_experience.data,
                willing_to_relocate=form.willing_to_relocate.data
            )
            db.session.add(career_profile)
        
        db.session.commit()
        flash('Profile saved successfully! Your information has been updated.', 'success')
        return redirect(url_for('index'))
    
    # Pre-populate form with existing data
    if career_profile and request.method == 'GET':
        form.full_name.data = career_profile.full_name
        form.age.data = career_profile.age
        form.current_profession.data = career_profile.current_profession
        form.area_of_interests.data = career_profile.area_of_interests
        form.career_goals.data = career_profile.career_goals
        form.current_skills.data = career_profile.current_skills
        form.preferred_work_environment.data = career_profile.preferred_work_environment
        form.expected_salary_min.data = career_profile.expected_salary_min
        form.expected_salary_max.data = career_profile.expected_salary_max
        form.education_level.data = career_profile.education_level
        form.years_of_experience.data = career_profile.years_of_experience
        form.willing_to_relocate.data = career_profile.willing_to_relocate
    
    return render_template('profile.html', title='Career Profile', form=form, profile=career_profile)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
