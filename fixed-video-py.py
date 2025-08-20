from flask import Blueprint, request, jsonify
import random
import time
from datetime import datetime

video_bp = Blueprint('video', __name__)

# Enhanced trending elements data
TRENDING_SOUNDS = [
    {"name": "Viral Dance Beat #1", "category": "dance", "popularity": 95},
    {"name": "Trending Audio Clip", "category": "comedy", "popularity": 88},
    {"name": "Popular Song Remix", "category": "music", "popularity": 92},
    {"name": "Comedy Sound Effect", "category": "comedy", "popularity": 85},
    {"name": "Motivational Speech Clip", "category": "inspiration", "popularity": 78},
    {"name": "Satisfying ASMR Sound", "category": "asmr", "popularity": 82},
    {"name": "Trending Meme Audio", "category": "meme", "popularity": 90}
]

TRENDING_EFFECTS = [
    {"name": "Neon Glow Transition", "category": "transition", "popularity": 88},
    {"name": "Glitch Effect", "category": "artistic", "popularity": 85},
    {"name": "Zoom Blur", "category": "dynamic", "popularity": 80},
    {"name": "Color Pop Filter", "category": "color", "popularity": 87},
    {"name": "Vintage Film Look", "category": "retro", "popularity": 75},
    {"name": "3D Perspective Shift", "category": "modern", "popularity": 91},
    {"name": "Lightning Fast Cuts", "category": "dynamic", "popularity": 89}
]

TRENDING_MEMES = [
    {"name": "POV Format", "category": "storytelling", "popularity": 92},
    {"name": "Before/After", "category": "transformation", "popularity": 86},
    {"name": "Day in My Life", "category": "lifestyle", "popularity": 83},
    {"name": "Rating Things", "category": "review", "popularity": 79},
    {"name": "Explaining to My Past Self", "category": "educational", "popularity": 88},
    {"name": "Get Ready With Me", "category": "beauty", "popularity": 81},
    {"name": "Things I Wish I Knew", "category": "advice", "popularity": 84}
]

def get_content_category(prompt):
    """Analyze prompt to determine content category"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['dance', 'dancing', 'choreography', 'moves']):
        return 'dance'
    elif any(word in prompt_lower for word in ['food', 'cooking', 'recipe', 'eating', 'taste']):
        return 'food'
    elif any(word in prompt_lower for word in ['tutorial', 'how to', 'learn', 'teach', 'guide']):
        return 'tutorial'
    elif any(word in prompt_lower for word in ['pet', 'dog', 'cat', 'animal']):
        return 'pet'
    elif any(word in prompt_lower for word in ['reaction', 'react', 'respond', 'review']):
        return 'reaction'
    elif any(word in prompt_lower for word in ['makeup', 'beauty', 'skincare', 'outfit']):
        return 'beauty'
    elif any(word in prompt_lower for word in ['room', 'home', 'decor', 'organize']):
        return 'lifestyle'
    elif any(word in prompt_lower for word in ['funny', 'comedy', 'joke', 'humor']):
        return 'comedy'
    else:
        return 'general'

def generate_enhanced_description(prompt, content_category, applied_trends):
    """Generate detailed AI suggestions based on content type"""
    
    base_description = f"🎬 Enhanced version of your idea: \"{prompt}\"\n\n🚀 AI Suggestions:\n"
    
    # Category-specific suggestions
    category_suggestions = {
        'dance': [
            "• Sync movements with beat drops and audio cues",
            "• Use quick cuts between different angles",
            "• Add mirror or split-screen effects for comparison",
            "• Include slow-motion highlights of key moves",
            "• Use trending dance hashtags and challenges"
        ],
        'food': [
            "• Capture close-up shots with satisfying sound effects",
            "• Add text overlay with ratings or taste reactions",
            "• Use trending food styling and presentation techniques",
            "• Include before/during/after shots",
            "• Add popular food-related audio clips"
        ],
        'tutorial': [
            "• Break down into clear step-by-step segments",
            "• Use text overlays for each step",
            "• Include before/after comparison shots",
            "• Add time-lapse for longer processes",
            "• Use educational trending formats"
        ],
        'pet': [
            "• Capture cute pet reaction shots",
            "• Use trending pet sounds and effects",
            "• Include popular pet challenge formats",
            "• Add funny captions and text overlays",
            "• Use pet-specific viral audio clips"
        ],
        'reaction': [
            "• Use split-screen reaction format",
            "• Add trending reaction sounds and effects",
            "• Include emotional text overlays",
            "• Capture genuine expressions and responses",
            "• Use popular reaction challenge formats"
        ],
        'beauty': [
            "• Use good lighting and close-up shots",
            "• Add before/after transformation reveals",
            "• Include trending beauty audio and effects",
            "• Use popular makeup/skincare formats",
            "• Add product recommendations and links"
        ],
        'lifestyle': [
            "• Show transformation process with time-lapse",
            "• Use aesthetic trending effects and filters",
            "• Add satisfying organization moments",
            "• Include trending lifestyle audio",
            "• Use popular home/lifestyle formats"
        ],
        'comedy': [
            "• Perfect timing with comedic beats",
            "• Use trending comedy audio and sound effects",
            "• Add funny text overlays and captions",
            "• Include popular comedy formats and structures",
            "• Use relatable humor and situations"
        ],
        'general': [
            "• Apply trending visual effects for engagement",
            "• Include popular audio elements",
            "• Use current meme formats and structures",
            "• Add dynamic transitions and cuts",
            "• Include trending hashtags and challenges"
        ]
    }
    
    suggestions = category_suggestions.get(content_category, category_suggestions['general'])
    for suggestion in suggestions[:4]:  # Limit to 4 suggestions
        base_description += suggestion + "\n"
    
    base_description += f"\n✨ Trending elements applied: {', '.join([t['name'] for t in applied_trends])}\n"
    
    # Add platform-specific tips
    base_description += "\n🎯 Platform Optimization Tips:\n"
    base_description += "• TikTok: Hook viewers in first 3 seconds\n"
    base_description += "• Instagram Reels: Use trending audio and hashtags\n"
    base_description += "• YouTube Shorts: Strong thumbnail and title\n"
    
    return base_description

@video_bp.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Simulate AI processing time (2-4 seconds)
        processing_time = 2 + random.random() * 2
        time.sleep(processing_time)
        
        # Determine content category
        content_category = get_content_category(prompt)
        
        # Select trending elements to apply based on content category
        applied_trends = []
        
        # Smart selection based on content type
        relevant_sounds = [s for s in TRENDING_SOUNDS if s['popularity'] > 80]
        relevant_effects = [e for e in TRENDING_EFFECTS if e['popularity'] > 80]
        relevant_memes = [m for m in TRENDING_MEMES if m['popularity'] > 80]
        
        # Randomly select 1-3 elements
        if random.random() > 0.2:  # 80% chance
            applied_trends.append(random.choice(relevant_sounds))
        if random.random() > 0.3:  # 70% chance
            applied_trends.append(random.choice(relevant_effects))
        if random.random() > 0.4:  # 60% chance
            applied_trends.append(random.choice(relevant_memes))
        
        # Generate enhanced description
        enhanced_description = generate_enhanced_description(prompt, content_category, applied_trends)
        
        # Calculate viral score based on various factors
        base_score = 70
        if len(prompt) > 50:  # Detailed prompts get higher scores
            base_score += 10
        if content_category in ['dance', 'food', 'pet']:  # Popular categories
            base_score += 5
        if len(applied_trends) >= 2:  # Multiple trends applied
            base_score += 8
        
        viral_score = min(95, base_score + random.randint(0, 10))
        
        # Determine best platforms based on content category
        platform_mapping = {
            'dance': ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
            'food': ['TikTok', 'Instagram Reels', 'Pinterest'],
            'tutorial': ['YouTube Shorts', 'TikTok', 'Instagram Reels'],
            'pet': ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
            'beauty': ['Instagram Reels', 'TikTok', 'YouTube Shorts'],
            'lifestyle': ['Instagram Reels', 'Pinterest', 'TikTok'],
            'comedy': ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
            'general': ['TikTok', 'Instagram Reels', 'YouTube Shorts']
        }
        
        suggested_platforms = platform_mapping.get(content_category, ['TikTok', 'Instagram Reels', 'YouTube Shorts'])
        
        response = {
            'success': True,
            'description': enhanced_description,
            'appliedTrends': [trend['name'] for trend in applied_trends],
            'estimatedViralScore': viral_score,
            'suggestedPlatforms': suggested_platforms,
            'contentCategory': content_category,
            'processingTime': round(processing_time, 2),
            'generatedAt': int(time.time()),
            'recommendations': {
                'bestPostingTime': '6-9 PM or 12-3 PM',
                'suggestedHashtags': f"#{content_category}video #viral #trending #fyp",
                'estimatedReach': f"{random.randint(10, 100)}K - {random.randint(500, 2000)}K views"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@video_bp.route('/trending-elements', methods=['GET'])
def get_trending_elements():
    """Get current trending elements with enhanced data"""
    try:
        # Simulate slight variations in popularity (trending elements change over time)
        sounds = []
        for sound in TRENDING_SOUNDS[:5]:  # Return top 5
            popularity_variance = random.randint(-3, 3)
            sounds.append({
                'name': sound['name'],
                'popularity': max(70, min(98, sound['popularity'] + popularity_variance)),
                'category': sound['category']
            })
        
        effects = []
        for effect in TRENDING_EFFECTS[:5]:  # Return top 5
            popularity_variance = random.randint(-3, 3)
            effects.append({
                'name': effect['name'],
                'popularity': max(70, min(98, effect['popularity'] + popularity_variance)),
                'category': effect['category']
            })
        
        memes = []
        for meme in TRENDING_MEMES[:5]:  # Return top 5
            popularity_variance = random.randint(-3, 3)
            memes.append({
                'name': meme['name'],
                'popularity': max(70, min(98, meme['popularity'] + popularity_variance)),
                'category': meme['category']
            })
        
        trending_data = {
            'sounds': sounds,
            'effects': effects,
            'memes': memes,
            'lastUpdated': datetime.now().isoformat(),
            'totalTrends': len(sounds) + len(effects) + len(memes)
        }
        
        return jsonify(trending_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch trending elements',
            'message': str(e)
        }), 500

@video_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get viral content analytics and insights"""
    try:
        analytics_data = {
            'topPerformingCategories': [
                {'category': 'dance', 'avgViralScore': 89, 'growth': '+12%'},
                {'category': 'food', 'avgViralScore': 85, 'growth': '+8%'},
                {'category': 'pet', 'avgViralScore': 87, 'growth': '+15%'},
                {'category': 'comedy', 'avgViralScore': 83, 'growth': '+5%'}
            ],
            'platformInsights': {
                'TikTok': {'bestTime': '6-9 PM', 'engagement': 'High', 'trending': 'Dance & Comedy'},
                'Instagram': {'bestTime': '12-3 PM', 'engagement': 'Medium-High', 'trending': 'Beauty & Lifestyle'},
                'YouTube': {'bestTime': '7-10 PM', 'engagement': 'Medium', 'trending': 'Tutorials & Reviews'}
            },
            'viralFactors': [
                'Hook within first 3 seconds',
                'Trending audio usage',
                'Strong visual appeal',
                'Relatable content',
                'Clear call-to-action'
            ]
        }
        
        return jsonify(analytics_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch analytics',
            'message': str(e)
        }), 500