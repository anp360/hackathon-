"""
Media Handler for SMS/MMS Emergency Messages
Handles image/video uploads with mock vision analysis for demo purposes
"""

import os
import json
import base64
import random
from datetime import datetime
import io

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    print("WARNING: Pillow not installed. Install with: pip install Pillow")
    print("Thumbnail generation will be disabled.")
    PIL_AVAILABLE = False

class MediaHandler:
    def __init__(self, media_dir='data/media'):
        self.media_dir = media_dir
        self.review_queue_file = 'data/media_review_queue.json'
        
        # Create directories
        os.makedirs(media_dir, exist_ok=True)
        os.makedirs(os.path.join(media_dir, 'thumbnails'), exist_ok=True)
        
        # Initialize review queue
        if not os.path.exists(self.review_queue_file):
            with open(self.review_queue_file, 'w') as f:
                json.dump([], f)
    
    def validate_file(self, file_data, file_type):
        """Validate file size and type"""
        # Check file size
        file_size = len(file_data) / (1024 * 1024)  # Convert to MB
        
        if file_type.startswith('image/'):
            if file_size > 5:  # 5MB limit for images
                return False, "Image size exceeds 5MB limit"
        elif file_type.startswith('video/'):
            if file_size > 50:  # ~50MB for 30 second video
                return False, "Video size exceeds limit (max 30 seconds)"
        else:
            return False, "Unsupported file type"
        
        return True, "Valid"
    
    def save_media(self, file_data, filename, file_type):
        """Save uploaded media file"""
        # Generate unique ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_ext = filename.split('.')[-1]
        unique_filename = f"{timestamp}_{random.randint(1000, 9999)}.{file_ext}"
        filepath = os.path.join(self.media_dir, unique_filename)
        
        # Save file
        with open(filepath, 'wb') as f:
            f.write(file_data)
        
        # Generate thumbnail for images
        thumbnail_path = None
        if file_type.startswith('image/'):
            thumbnail_path = self._generate_thumbnail(filepath, unique_filename)
        
        return {
            'media_id': unique_filename.split('.')[0],
            'filename': unique_filename,
            'filepath': filepath,
            'thumbnail': thumbnail_path,
            'file_type': file_type,
            'size_mb': len(file_data) / (1024 * 1024),
            'uploaded_at': datetime.now().isoformat()
        }
    
    def _generate_thumbnail(self, filepath, filename):
        """Generate thumbnail for images"""
        if not PIL_AVAILABLE:
            print("Pillow not available, skipping thumbnail generation")
            return None
            
        try:
            img = Image.open(filepath)
            img.thumbnail((200, 200))
            
            thumb_filename = f"thumb_{filename}"
            thumb_path = os.path.join(self.media_dir, 'thumbnails', thumb_filename)
            img.save(thumb_path)
            
            return thumb_path
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    def analyze_media_mock(self, media_info, message_text=""):
        """
        Mock vision analysis for demo purposes
        In production, this would call Gemini Vision API
        """
        file_type = media_info['file_type']
        
        # Simulate AI analysis
        analysis = {
            'media_id': media_info['media_id'],
            'analyzed_at': datetime.now().isoformat(),
            'file_type': file_type
        }
        
        if file_type.startswith('image/'):
            analysis.update(self._analyze_image_mock(media_info, message_text))
        elif file_type.startswith('video/'):
            analysis.update(self._analyze_video_mock(media_info, message_text))
        
        return analysis
    
    def _analyze_image_mock(self, media_info, message_text):
        """Mock image analysis"""
        # Simulate different scenarios based on randomness
        scenario = random.choice(['clear', 'clear', 'clear', 'unclear', 'unclear'])
        
        if scenario == 'clear':
            # High confidence scenarios
            emergency_types = [
                {
                    'description': 'Person with visible injury, appears to need medical attention',
                    'urgency': 9,
                    'people_count': 1,
                    'needs': ['medical supplies', 'ambulance'],
                    'has_danger': True
                },
                {
                    'description': 'Multiple people trapped in flooded area',
                    'urgency': 10,
                    'people_count': 3,
                    'needs': ['rescue', 'boats'],
                    'has_danger': True
                },
                {
                    'description': 'Elderly person appears distressed, indoor residential setting',
                    'urgency': 7,
                    'people_count': 1,
                    'needs': ['medical check', 'assistance'],
                    'has_danger': False
                },
                {
                    'description': 'Child showing signs of dehydration, needs immediate water',
                    'urgency': 8,
                    'people_count': 1,
                    'needs': ['water', 'medical'],
                    'has_danger': True
                },
                {
                    'description': 'Building damage visible, people evacuating area',
                    'urgency': 8,
                    'people_count': 5,
                    'needs': ['shelter', 'evacuation'],
                    'has_danger': True
                }
            ]
            selected = random.choice(emergency_types)
            confidence = random.randint(75, 95)
            
        else:
            # Low confidence scenarios
            selected = {
                'description': 'Unable to clearly identify emergency details from image',
                'urgency': 5,
                'people_count': 0,
                'needs': ['clarification needed'],
                'has_danger': False
            }
            confidence = random.randint(40, 65)
        
        # Merge with message text if provided
        if message_text and message_text.strip():
            selected['description'] = f"{message_text.strip()}. Visual analysis: {selected['description']}"
        
        return {
            'vision_description': selected['description'],
            'confidence_score': confidence,
            'detected_urgency': selected['urgency'],
            'detected_people': selected['people_count'],
            'detected_needs': selected['needs'],
            'immediate_danger': selected['has_danger'],
            'requires_review': confidence < 70
        }
    
    def _analyze_video_mock(self, media_info, message_text):
        """Mock video analysis (analyzes first frame concept)"""
        # Simulate video analysis
        scenarios = [
            {
                'description': 'Video shows ongoing flooding, water levels rising rapidly',
                'urgency': 10,
                'people_count': 2,
                'needs': ['rescue', 'evacuation'],
                'has_danger': True
            },
            {
                'description': 'Video captures building collapse, debris falling',
                'urgency': 10,
                'people_count': 0,
                'needs': ['rescue team', 'safety perimeter'],
                'has_danger': True
            },
            {
                'description': 'Video shows person calling for help from rooftop',
                'urgency': 9,
                'people_count': 1,
                'needs': ['helicopter rescue', 'immediate evacuation'],
                'has_danger': True
            }
        ]
        
        selected = random.choice(scenarios)
        confidence = random.randint(70, 90)
        
        if message_text and message_text.strip():
            selected['description'] = f"{message_text.strip()}. Video analysis: {selected['description']}"
        
        return {
            'vision_description': selected['description'],
            'confidence_score': confidence,
            'detected_urgency': selected['urgency'],
            'detected_people': selected['people_count'],
            'detected_needs': selected['needs'],
            'immediate_danger': selected['has_danger'],
            'requires_review': confidence < 70,
            'video_duration': '15-30 seconds'
        }
    
    def add_to_review_queue(self, message_id, media_info, analysis):
        """Add low-confidence media to manual review queue"""
        with open(self.review_queue_file, 'r') as f:
            queue = json.load(f)
        
        review_item = {
            'review_id': f"review_{len(queue) + 1}",
            'message_id': message_id,
            'media_info': media_info,
            'analysis': analysis,
            'status': 'pending',
            'added_at': datetime.now().isoformat(),
            'reviewed_at': None,
            'reviewer_notes': None
        }
        
        queue.append(review_item)
        
        with open(self.review_queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        return review_item
    
    def get_review_queue(self, status='pending'):
        """Get items from review queue"""
        with open(self.review_queue_file, 'r') as f:
            queue = json.load(f)
        
        if status:
            return [item for item in queue if item['status'] == status]
        return queue
    
    def approve_review(self, review_id, reviewer_description, reviewer_priority=None):
        """Approve a review and update the message"""
        with open(self.review_queue_file, 'r') as f:
            queue = json.load(f)
        
        for item in queue:
            if item['review_id'] == review_id:
                item['status'] = 'approved'
                item['reviewed_at'] = datetime.now().isoformat()
                item['reviewer_notes'] = reviewer_description
                if reviewer_priority:
                    item['reviewer_priority'] = reviewer_priority
                break
        
        with open(self.review_queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        return item
    
    def get_media_path(self, media_id):
        """Get full path for media file"""
        # Find file with this media_id
        for filename in os.listdir(self.media_dir):
            if filename.startswith(media_id):
                return os.path.join(self.media_dir, filename)
        return None
    
    def get_thumbnail_path(self, media_id):
        """Get thumbnail path for media"""
        thumb_dir = os.path.join(self.media_dir, 'thumbnails')
        for filename in os.listdir(thumb_dir):
            if filename.startswith(f"thumb_{media_id}"):
                return os.path.join(thumb_dir, filename)
        return None
