from flask import Blueprint, request, jsonify
import random
import time

video_bp = Blueprint('video', __name__)

# Mock trending elements data
TRENDING_SOUNDS = [
    "Viral Dance Beat #1", "Trending Audio Clip", "Popular Song Remix", 
    "Comedy Sound Effect", "Motivational Speech Clip"
]

TRENDING_EFFECTS = [
    "Neon Glow Transition", "Glitch Effect", "Zoom Blur", 
    "Color Pop Filter", "Vintage Film Look"
]

TRENDING_MEMES = [
    "POV Format", "Before/After", "Day in My Life", 
    "Rating Things", "Explaining to My Past Self"
]

@video_bp.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Simulate AI processing time
        time.sleep(2)
        
        # Generate mock response based on prompt
        applied_trends = []
        
        # Randomly select trending elements to apply
        if random.random() > 0.3:
            applied_trends.append(random.choice(TRENDING_SOUNDS))
        if random.random() > 0.4:
            applied_trends.append(random.choice(TRENDING_EFFECTS))
        if random.random() > 0.5:
            applied_trends.append(random.choice(TRENDING_MEMES))
        
        # Generate enhanced description
        enhanced_description = f"Enhanced version of your idea: {prompt}\n\n"
        enhanced_description += "AI Suggestions:\n"
        
        if "dance" in prompt.lower():
            enhanced_description += "• Add trending dance moves synchronized with popular beat\n"
            enhanced_description += "• Use quick cuts and zoom effects for dynamic feel\n"
        elif "food" in prompt.lower():
            enhanced_description += "• Include close-up shots with satisfying sound effects\n"
            enhanced_description += "• Add text overlay with ratings or reactions\n"
        elif "tutorial" in prompt.lower():
            enhanced_description += "• Use step-by-step text overlays\n"
            enhanced_description += "• Add before/after comparison shots\n"
        else:
            enhanced_description += "• Apply trending visual effects for engagement\n"
            enhanced_description += "• Include popular audio elements\n"
        
        enhanced_description += f"\nTrending elements applied: {', '.join(applied_trends)}"
        
        response = {
            'success': True,
            'description': enhanced_description,
            'appliedTrends': applied_trends,
            'estimatedViralScore': random.randint(75, 95),
            'suggestedPlatforms': ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
            'generatedAt': time.time()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/trending-elements', methods=['GET'])
def get_trending_elements():
    """Get current trending elements"""
    try:
        trending_data = {
            'sounds': [{'name': sound, 'popularity': random.randint(80, 98)} for sound in TRENDING_SOUNDS[:3]],
            'effects': [{'name': effect, 'popularity': random.randint(75, 95)} for effect in TRENDING_EFFECTS[:3]],
            'memes': [{'name': meme, 'popularity': random.randint(85, 97)} for meme in TRENDING_MEMES[:3]]
        }
        
        return jsonify(trending_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

