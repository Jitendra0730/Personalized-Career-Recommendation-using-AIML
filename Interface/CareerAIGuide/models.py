from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to career profile
    career_profile = db.relationship('CareerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class CareerProfile(db.Model):
    __tablename__ = 'career_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    
    # Professional Information
    current_profession = db.Column(db.String(100), nullable=True)
    area_of_interests = db.Column(db.Text, nullable=True)
    career_goals = db.Column(db.Text, nullable=True)
    current_skills = db.Column(db.Text, nullable=True)
    
    # Work Preferences
    preferred_work_environment = db.Column(db.String(50), nullable=True)
    expected_salary_min = db.Column(db.Integer, nullable=True)
    expected_salary_max = db.Column(db.Integer, nullable=True)
    
    # Additional Information
    education_level = db.Column(db.String(50), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    willing_to_relocate = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CareerProfile {self.full_name}>'
