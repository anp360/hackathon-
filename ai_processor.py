"""
AI Processor using Google Gemini AI
Handles intelligent message interpretation and extraction
PERSON 1: AI Backend Development
"""

import google.generativeai as genai
import json
from config import GEMINI_API_KEY, GEMINI_MODEL, NEED_CATEGORIES, LOCATIONS
import re

class GeminiMessageProcessor:
    def __init__(self, api_key=None):
        """Initialize Gemini AI"""
        self.api_key = api_key or GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
    def analyze_message(self, message_text):
        """
        Use Gemini AI to analyze emergency message
        Returns: dict with need_type, location, urgency, vulnerable_groups, etc.
        """
        
        prompt = f"""
You are an AI assistant for emergency response. Analyze this distress message and extract key information.

Message: "{message_text}"

Respond with ONLY a valid JSON object (no markdown, no extra text) with these fields:
{{
    "need_type": "one of: food, water, medical, shelter, rescue, clothing, unknown",
    "location": "extracted location or 'unknown'",
    "urgency_base_score": "number from 1-10",
    "vulnerable_groups": ["list any: children, elderly, pregnant, disabled, or empty list"],
    "has_immediate_danger": true/false,
    "keywords_found": ["list key distress words found"],
    "estimated_people_count": number or null,
    "additional_context": "brief relevant details"
}}

Important locations to check: {', '.join(LOCATIONS)}

Analyze carefully for urgency indicators like: "urgent", "immediately", "dying", "critical", "help", "drowning", "trapped", "bleeding", etc.
"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            
            # Parse JSON
            analysis = json.loads(result_text)
            
            # Validate and sanitize
            analysis['need_type'] = analysis.get('need_type', 'unknown').lower()
            if analysis['need_type'] not in NEED_CATEGORIES:
                analysis['need_type'] = 'unknown'
                
            analysis['urgency_base_score'] = min(10, max(1, int(analysis.get('urgency_base_score', 5))))
            analysis['vulnerable_groups'] = analysis.get('vulnerable_groups', [])
            analysis['has_immediate_danger'] = bool(analysis.get('has_immediate_danger', False))
            
            return analysis
            
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            # Fallback to basic extraction
            return self._fallback_analysis(message_text)
    
    def _fallback_analysis(self, message_text):
        """Fallback keyword-based analysis if AI fails"""
        msg_lower = message_text.lower()
        
        # Basic need detection (check medical first for breathing emergencies)
        need_type = "unknown"
        # Check medical emergencies FIRST (including respiratory)
        if any(word in msg_lower for word in ["medical", "doctor", "injury", "sick", "hospital", "medicine", "breathing", "respiratory"]):
            need_type = "medical"
        elif any(word in msg_lower for word in ["food", "hungry", "starving", "eat"]):
            need_type = "food"
        elif any(word in msg_lower for word in ["water", "thirsty", "drink"]):
            need_type = "water"
        elif any(word in msg_lower for word in ["shelter", "roof", "homeless", "flood", "house"]):
            need_type = "shelter"
        elif any(word in msg_lower for word in ["rescue", "trapped", "stuck", "drowning"]):
            need_type = "rescue"
            
        # Location detection
        location = "unknown"
        for loc in LOCATIONS:
            if loc.lower() in msg_lower:
                location = loc
                break
                
        # Urgency scoring
        urgency_score = 5  # default medium
        if any(word in msg_lower for word in ["urgent", "immediately", "dying", "critical", "help"]):
            urgency_score += 3
        if any(word in msg_lower for word in ["trapped", "drowning", "bleeding"]):
            urgency_score += 2
        # Respiratory emergencies are life-threatening
        if any(phrase in msg_lower for phrase in ["not breathing", "can't breathe", "cannot breathe", "respiratory", "difficulty breathing"]):
            urgency_score = 10  # Max urgency for breathing issues (CRITICAL)
            
        # Vulnerable groups
        vulnerable_groups = []
        if any(word in msg_lower for word in ["child", "children"]):
            vulnerable_groups.append("children")
        if any(word in msg_lower for word in ["baby", "babies", "infant", "newborn"]):
            vulnerable_groups.append("baby")
        if any(word in msg_lower for word in ["elderly", "old", "senior"]):
            vulnerable_groups.append("elderly")
        if "pregnant" in msg_lower:
            vulnerable_groups.append("pregnant")
            
        # Duration detection (extended suffering)
        extended_duration = False
        if any(phrase in msg_lower for phrase in ["2 days", "3 days", "4 days", "5 days", "days", "week"]):
            extended_duration = True
            urgency_score += 1  # Small boost for extended suffering
            
        return {
            "need_type": need_type,
            "location": location,
            "urgency_base_score": min(10, urgency_score),
            "vulnerable_groups": vulnerable_groups,
            "has_immediate_danger": urgency_score >= 8,
            "extended_duration": extended_duration,
            "keywords_found": [],
            "estimated_people_count": None,
            "additional_context": "Fallback analysis used"
        }

    def batch_analyze(self, messages):
        """Analyze multiple messages"""
        results = []
        for msg in messages:
            analysis = self.analyze_message(msg)
            results.append({
                "original_message": msg,
                "analysis": analysis
            })
        return results


# Test function
if __name__ == "__main__":
    processor = GeminiMessageProcessor()
    
    test_messages = [
        "Need food urgently near Tambaram, no food for 2 days",
        "Medical help needed for elderly person in Velachery",
        "Trapped in flooding water with children in Perungudi, please help immediately!",
        "Shelter required after flooding near Saidapet at night"
    ]
    
    print("=== Testing Gemini AI Message Processor ===\n")
    for msg in test_messages:
        print(f"Message: {msg}")
        result = processor.analyze_message(msg)
        print(f"Analysis: {json.dumps(result, indent=2)}")
        print("-" * 60)
