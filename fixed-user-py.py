from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os

user_bp = Blueprint('user', __name__)

# This would typically come from environment variables
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-here')

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Basic validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters long'}), 400
        
        if not email or '@' not in email:
            return jsonify({'error': 'Valid email is required'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # In a real app, you'd check if user exists in database
        # For now, we'll simulate a successful registration
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Create JWT token
        token = jwt.encode({
            'user_id': f"user_{username}_{datetime.datetime.utcnow().timestamp()}",
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'username': username,
                'email': email,
                'created_at': datetime.datetime.utcnow().isoformat()
            },
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # In a real app, you'd verify credentials against database
        # For demo purposes, we'll accept any non-empty credentials
        
        if len(username) < 3:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create JWT token
        token = jwt.encode({
            'user_id': f"user_{username}_{datetime.datetime.utcnow().timestamp()}",
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': username,
                'last_login': datetime.datetime.utcnow().isoformat()
            },
            'token': token
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    """Get user profile"""
    try:
        # In a real app, you'd fetch from database
        # For demo, return mock profile data
        
        profile_data = {
            'user_id': current_user_id,
            'username': current_user_id.split('_')[1],
            'email': f"{current_user_id.split('_')[1]}@example.com",
            'created_at': '2024-01-01T00:00:00Z',
            'subscription': 'free',
            'videos_generated': 47,
            'viral_score_avg': 82,
            'favorite_categories': ['dance', 'food', 'comedy']
        }
        
        return jsonify({
            'success': True,
            'profile': profile_data
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch profile',
            'message': str(e)
        }), 500

@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user_id):
    """Update user profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # In a real app, you'd update the database
        # For demo, just return success
        
        allowed_fields = ['email', 'bio', 'favorite_categories', 'preferences']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'updated_fields': list(update_data.keys())
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update profile',
            'message': str(e)
        }), 500

@user_bp.route('/history', methods=['GET'])
@token_required
def get_video_history(current_user_id):
    """Get user's video generation history"""
    try:
        # Mock history data
        history = [
            {
                'id': 1,
                'prompt': 'A funny reaction to trying a new food trend',
                'viral_score': 87,
                'created_at': '2024-01-15T10:30:00Z',
                'applied_trends': ['Trending Audio Clip', 'POV Format']
            },
            {
                'id': 2,
                'prompt': 'Dance challenge with my pet dog',
                'viral_score': 92,
                'created_at': '2024-01-14T15:45:00Z',
                'applied_trends': ['Viral Dance Beat #1', 'Neon Glow Transition']
            },
            {
                'id': 3,
                'prompt': 'Tutorial on organizing your room in 60 seconds',
                'viral_score': 78,
                'created_at': '2024-01-13T09:20:00Z',
                'applied_trends': ['Before/After', 'Color Pop Filter']
            }
        ]
        
        return jsonify({
            'success': True,
            'history': history,
            'total': len(history)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch history',
            'message': str(e)
        }), 500

@user_bp.route('/favorites', methods=['POST'])
@token_required
def add_favorite(current_user_id):
    """Add video concept to favorites"""
    try:
        data = request.get_json()
        
        if not data or 'video_id' not in data:
            return jsonify({'error': 'Video ID is required'}), 400
        
        # In a real app, you'd save to database
        return jsonify({
            'success': True,
            'message': 'Added to favorites successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to add favorite',
            'message': str(e)
        }), 500

@user_bp.route('/subscription', methods=['GET'])
@token_required
def get_subscription_info(current_user_id):
    """Get user subscription information"""
    try:
        subscription_info = {
            'plan': 'free',
            'videos_remaining': 3,
            'videos_total': 5,
            'reset_date': '2024-02-01T00:00:00Z',
            'features': {
                'hd_export': False,
                'unlimited_videos': False,
                'premium_trends': False,
                'analytics': False
            },
            'upgrade_options': [
                {
                    'plan': 'pro',
                    'price': '$19.99/month',
                    'features': ['Unlimited videos', 'HD export', 'Premium trends']
                },
                {
                    'plan': 'business',
                    'price': '$49.99/month',
                    'features': ['All Pro features', 'Team collaboration', 'Analytics dashboard']
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'subscription': subscription_info
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch subscription info',
            'message': str(e)
        }), 500