import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Create the src directory structure if it doesn't exist
src_dir = os.path.join(os.path.dirname(__file__), 'src')
routes_dir = os.path.join(src_dir, 'routes')
models_dir = os.path.join(src_dir, 'models')

for directory in [src_dir, routes_dir, models_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create __init__.py files if they don't exist
for directory in [src_dir, routes_dir, models_dir]:
    init_file = os.path.join(directory, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')

try:
    from src.routes.user import user_bp
except ImportError:
    print("Warning: user routes not found, creating minimal blueprint")
    from flask import Blueprint
    user_bp = Blueprint('user', __name__)

try:
    from src.routes.video import video_bp
except ImportError:
    print("Warning: video routes not found, creating minimal blueprint")
    from flask import Blueprint
    video_bp = Blueprint('video', __name__)

# Try to import database models
try:
    from src.models.user import db
    DB_AVAILABLE = True
except ImportError:
    print("Warning: Database models not found, running without database")
    DB_AVAILABLE = False
    db = None

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app, origins=['*'])

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(video_bp, url_prefix='/api')

# Database setup (only if available)
if DB_AVAILABLE and db is not None:
    database_dir = os.path.join(os.path.dirname(__file__), 'database')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(database_dir, 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'ViralCraft AI Backend',
        'database': 'connected' if DB_AVAILABLE else 'not available',
        'version': '1.0.0'
    })

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    
    if static_folder_path is None:
        return jsonify({
            'error': 'Static folder not configured',
            'message': 'Please build the React app and place files in the static folder'
        }), 404

    # If path exists, serve it
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    
    # Otherwise serve index.html (for SPA routing)
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return jsonify({
            'error': 'Frontend not found',
            'message': 'Please build the React frontend first',
            'api_status': 'Backend is running on /api/*'
        }), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found',
        'available_endpoints': [
            '/api/health',
            '/api/generate-video',
            '/api/trending-elements',
            '/api/analytics',
            '/api/register',
            '/api/login',
            '/api/profile'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting ViralCraft AI Backend...")
    print(f"📍 Running on: http://0.0.0.0:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"💾 Database: {'Available' if DB_AVAILABLE else 'Not configured'}")
    print(f"📁 Static folder: {app.static_folder}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        use_reloader=debug_mode
    )