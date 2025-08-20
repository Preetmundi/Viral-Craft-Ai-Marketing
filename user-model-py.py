from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Profile information
    bio = db.Column(db.Text)
    favorite_categories = db.Column(db.Text)  # JSON string
    subscription_plan = db.Column(db.String(20), default='free')
    
    # Usage statistics
    videos_generated = db.Column(db.Integer, default=0)
    total_viral_score = db.Column(db.Float, default=0.0)
    
    # Relationships
    video_history = db.relationship('VideoHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def get_favorite_categories(self):
        """Get favorite categories as list"""
        if self.favorite_categories:
            try:
                return json.loads(self.favorite_categories)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_favorite_categories(self, categories):
        """Set favorite categories from list"""
        self.favorite_categories = json.dumps(categories) if categories else None
    
    def get_average_viral_score(self):
        """Calculate average viral score"""
        if self.videos_generated > 0:
            return round(self.total_viral_score / self.videos_generated, 1)
        return 0.0
    
    def update_stats(self, viral_score):
        """Update user statistics"""
        self.videos_generated += 1
        self.total_viral_score += viral_score
        db.session.commit()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'bio': self.bio,
            'favorite_categories': self.get_favorite_categories(),
            'subscription_plan': self.subscription_plan,
            'videos_generated': self.videos_generated,
            'average_viral_score': self.get_average_viral_score(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class VideoHistory(db.Model):
    """Model for storing user's video generation history"""
    __tablename__ = 'video_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    applied_trends = db.Column(db.Text)  # JSON string
    viral_score = db.Column(db.Float, default=0.0)
    content_category = db.Column(db.String(50))
    suggested_platforms = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    
    def get_applied_trends(self):
        """Get applied trends as list"""
        if self.applied_trends:
            try:
                return json.loads(self.applied_trends)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_applied_trends(self, trends):
        """Set applied trends from list"""
        self.applied_trends = json.dumps(trends) if trends else None
    
    def get_suggested_platforms(self):
        """Get suggested platforms as list"""
        if self.suggested_platforms:
            try:
                return json.loads(self.suggested_platforms)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_suggested_platforms(self, platforms):
        """Set suggested platforms from list"""
        self.suggested_platforms = json.dumps(platforms) if platforms else None
    
    def to_dict(self):
        """Convert video history to dictionary"""
        return {
            'id': self.id,
            'prompt': self.prompt,
            'description': self.description,
            'applied_trends': self.get_applied_trends(),
            'viral_score': self.viral_score,
            'content_category': self.content_category,
            'suggested_platforms': self.get_suggested_platforms(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_favorite': self.is_favorite
        }
    
    def __repr__(self):
        return f'<VideoHistory {self.id}: {self.prompt[:50]}...>'

class TrendingElement(db.Model):
    """Model for storing trending elements data"""
    __tablename__ = 'trending_elements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # sound, effect, meme
    category = db.Column(db.String(50))
    popularity = db.Column(db.Float, default=0.0)
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def update_popularity(self, new_popularity):
        """Update popularity score"""
        self.popularity = new_popularity
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        db.session.commit()
    
    def to_dict(self):
        """Convert trending element to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'popularity': self.popularity,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TrendingElement {self.name} ({self.type})>'