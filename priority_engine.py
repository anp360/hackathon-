"""
Priority Engine with Time-Aware Scoring
Ranks emergency messages based on multiple factors
PERSON 1: AI Backend Development
"""

from datetime import datetime
from config import TIME_SENSITIVE_NEEDS, URGENCY_LEVELS

class PriorityEngine:
    def __init__(self):
        self.weights = {
            "base_urgency": 0.30,
            "time_sensitivity": 0.25,
            "vulnerable_groups": 0.20,
            "immediate_danger": 0.15,
            "people_count": 0.10
        }
    
    def calculate_priority_score(self, analysis, timestamp=None):
        """
        Calculate comprehensive priority score
        Returns: dict with total_score, urgency_level, reasons
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        score_breakdown = {}
        reasons = []
        
        # 1. Base urgency from AI (0-10 scale, normalized to 0-100)
        base_score = analysis.get('urgency_base_score', 5) * 10
        score_breakdown['base_urgency'] = base_score * self.weights['base_urgency']
        
        if base_score >= 80:
            reasons.append("High urgency keywords detected")
        
        # 2. Time sensitivity (0-100 scale)
        time_score = self._calculate_time_sensitivity(
            analysis.get('need_type', 'unknown'),
            timestamp
        )
        score_breakdown['time_sensitivity'] = time_score * self.weights['time_sensitivity']
        
        if time_score > 70:
            need_type = analysis.get('need_type', 'unknown')
            if need_type in TIME_SENSITIVE_NEEDS:
                reasons.append(TIME_SENSITIVE_NEEDS[need_type]['reason'])
        
        # 3. Vulnerable groups multiplier (0-100)
        vulnerable_score = self._calculate_vulnerable_score(
            analysis.get('vulnerable_groups', [])
        )
        score_breakdown['vulnerable_groups'] = vulnerable_score * self.weights['vulnerable_groups']
        
        if vulnerable_score > 0:
            groups = analysis.get('vulnerable_groups', [])
            reasons.append(f"Vulnerable groups present: {', '.join(groups)}")
        
        # 4. Immediate danger bonus (0 or 100)
        danger_score = 100 if analysis.get('has_immediate_danger', False) else 0
        score_breakdown['immediate_danger'] = danger_score * self.weights['immediate_danger']
        
        if danger_score > 0:
            reasons.append("Life-threatening situation detected")
        
        # 5. People count factor (scaled to 0-100)
        people_score = self._calculate_people_score(
            analysis.get('estimated_people_count')
        )
        score_breakdown['people_count'] = people_score * self.weights['people_count']
        
        if people_score > 50:
            count = analysis.get('estimated_people_count', 0)
            reasons.append(f"Multiple people affected ({count})")
        
        # Calculate total
        total_score = sum(score_breakdown.values())
        
        # 6. Extended duration bonus (suffering for days) - added after base calculation
        extended_duration_boost = 0
        if analysis.get('extended_duration', False):
            need_type = analysis.get('need_type', 'unknown')
            # Water and food deprivation for days is serious
            if need_type in ['water', 'food']:
                extended_duration_boost = 12  # Larger boost for water/food deprivation
            else:
                extended_duration_boost = 8  # Moderate boost for other extended situations
            total_score += extended_duration_boost
            reasons.append("Extended duration - suffering for multiple days")
        
        # 7. Special case: Baby/infant with immediate danger = CRITICAL
        vulnerable_groups = analysis.get('vulnerable_groups', [])
        if 'baby' in vulnerable_groups and analysis.get('has_immediate_danger', False):
            total_score += 15  # Extra boost for babies in immediate danger
            reasons.append("CRITICAL: Baby/infant with life-threatening emergency")
        
        # 8. Water deprivation with vulnerable groups = HIGH priority
        need_type = analysis.get('need_type', 'unknown')
        if need_type == 'water' and len(vulnerable_groups) > 0 and analysis.get('extended_duration', False):
            total_score += 12  # Water deprivation with children/vulnerable is serious
            reasons.append("Water deprivation with vulnerable groups")
        
        # Determine urgency level
        urgency_level = self._get_urgency_level(total_score)
        
        return {
            "total_score": round(total_score, 2),
            "urgency_level": urgency_level,
            "score_breakdown": {k: round(v, 2) for k, v in score_breakdown.items()},
            "priority_reasons": reasons,
            "timestamp": timestamp.isoformat()
        }
    
    def _calculate_time_sensitivity(self, need_type, timestamp):
        """Calculate time-based urgency (nighttime shelter, etc.)"""
        current_hour = timestamp.hour
        
        if need_type in TIME_SENSITIVE_NEEDS:
            critical_hours = TIME_SENSITIVE_NEEDS[need_type]['critical_hours']
            if current_hour in critical_hours:
                return 100  # Maximum priority during critical hours
            else:
                return 50   # Still important, but less critical
        
        return 30  # Default for non-time-sensitive needs
    
    def _calculate_vulnerable_score(self, vulnerable_groups):
        """Score based on vulnerable populations"""
        if not vulnerable_groups:
            return 0
            
        # Each vulnerable group adds points
        score = 0
        for group in vulnerable_groups:
            if group == "children":
                score += 40
            elif group == "baby":
                score += 70  # Babies/infants/newborns get CRITICAL priority!
            elif group == "elderly":
                score += 35
            elif group == "pregnant":
                score += 40
            elif group == "disabled":
                score += 35
                
        return min(100, score)
    
    def _calculate_people_score(self, people_count):
        """Score based on number of people affected"""
        if people_count is None or people_count <= 0:
            return 40  # Assume single person if not specified
            
        # Scale: 1 person = 40, 5+ people = 100
        score = min(100, 40 + (people_count - 1) * 15)
        return score
    
    def _get_urgency_level(self, total_score):
        """Convert numeric score to urgency level"""
        if total_score >= 80:
            return "CRITICAL"
        elif total_score >= 60:
            return "HIGH"
        elif total_score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def rank_messages(self, processed_messages):
        """
        Rank a list of processed messages by priority
        Returns sorted list with priority scores
        """
        ranked = []
        
        for msg_data in processed_messages:
            analysis = msg_data.get('analysis', {})
            priority = self.calculate_priority_score(analysis)
            
            ranked.append({
                **msg_data,
                "priority": priority
            })
        
        # Sort by total score (highest first)
        ranked.sort(key=lambda x: x['priority']['total_score'], reverse=True)
        
        return ranked


# Test function
if __name__ == "__main__":
    from datetime import datetime
    
    engine = PriorityEngine()
    
    # Test case 1: Nighttime shelter request with children
    test_analysis_1 = {
        "need_type": "shelter",
        "urgency_base_score": 7,
        "vulnerable_groups": ["children"],
        "has_immediate_danger": False,
        "estimated_people_count": 4
    }
    
    # Simulate nighttime (9 PM)
    night_time = datetime(2026, 2, 6, 21, 0, 0)
    
    print("=== Testing Priority Engine ===\n")
    print("Test 1: Nighttime shelter request with children")
    priority = engine.calculate_priority_score(test_analysis_1, night_time)
    print(f"Priority Score: {priority['total_score']}")
    print(f"Urgency Level: {priority['urgency_level']}")
    print(f"Reasons: {priority['priority_reasons']}")
    print("-" * 60)
    
    # Test case 2: Daytime medical emergency
    test_analysis_2 = {
        "need_type": "medical",
        "urgency_base_score": 9,
        "vulnerable_groups": ["elderly"],
        "has_immediate_danger": True,
        "estimated_people_count": 1
    }
    
    day_time = datetime(2026, 2, 6, 14, 0, 0)
    
    print("\nTest 2: Daytime medical emergency with elderly")
    priority2 = engine.calculate_priority_score(test_analysis_2, day_time)
    print(f"Priority Score: {priority2['total_score']}")
    print(f"Urgency Level: {priority2['urgency_level']}")
    print(f"Reasons: {priority2['priority_reasons']}")
