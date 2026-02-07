"""
Responder Family Safety Tracker
Auto-checks if responder families are in affected zones
HACKATHON STANDOUT FEATURE #1
"""

import json
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import os

class ResponderFamilyTracker:
    def __init__(self, responders_file='data/responders.json'):
        self.responders_file = responders_file
        self.responders = self._load_responders()
        
        # Approximate coordinates for Chennai locations (lat, lon)
        self.location_coords = {
            "Tambaram": (12.9249, 80.1000),
            "Velachery": (12.9756, 80.2201),
            "Perungudi": (12.9610, 80.2433),
            "Saidapet": (13.0210, 80.2231),
            "Porur": (13.0381, 80.1564),
            "Adyar": (13.0067, 80.2565),
            "T Nagar": (13.0418, 80.2341),
            "Anna Nagar": (13.0850, 80.2101)
        }
    
    def _load_responders(self):
        """Load responder data from JSON file"""
        if os.path.exists(self.responders_file):
            with open(self.responders_file, 'r') as f:
                return json.load(f)
        else:
            # Create sample responders data
            sample_data = {
                "responders": [
                    {
                        "id": "resp_001",
                        "name": "Rajesh Kumar",
                        "role": "Emergency Coordinator",
                        "assigned_zone": "Tambaram",
                        "family": {
                            "members": ["Wife: Priya", "Son: Arun (8 years)"],
                            "location": "Velachery",
                            "contact": "+91-9876543210",
                            "last_contact": None,
                            "status": "unknown"
                        }
                    },
                    {
                        "id": "resp_002",
                        "name": "Lakshmi Devi",
                        "role": "Medical Team Lead",
                        "assigned_zone": "Velachery",
                        "family": {
                            "members": ["Husband: Suresh", "Daughter: Meena (5 years)"],
                            "location": "Perungudi",
                            "contact": "+91-9876543211",
                            "last_contact": None,
                            "status": "unknown"
                        }
                    },
                    {
                        "id": "resp_003",
                        "name": "Mohamed Ali",
                        "role": "Rescue Team Lead",
                        "assigned_zone": "Saidapet",
                        "family": {
                            "members": ["Mother: Fatima (65 years)", "Brother: Hassan"],
                            "location": "Tambaram",
                            "contact": "+91-9876543212",
                            "last_contact": None,
                            "status": "unknown"
                        }
                    },
                    {
                        "id": "resp_004",
                        "name": "Priya Sharma",
                        "role": "Logistics Coordinator",
                        "assigned_zone": "Perungudi",
                        "family": {
                            "members": ["Parents: Both elderly"],
                            "location": "Anna Nagar",
                            "contact": "+91-9876543213",
                            "last_contact": None,
                            "status": "safe"
                        }
                    }
                ]
            }
            
            # Save sample data
            os.makedirs('data', exist_ok=True)
            with open(self.responders_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            
            return sample_data
    
    def calculate_distance(self, loc1, loc2):
        """Calculate distance between two locations in km using Haversine formula"""
        if loc1 not in self.location_coords or loc2 not in self.location_coords:
            return None
        
        lat1, lon1 = self.location_coords[loc1]
        lat2, lon2 = self.location_coords[loc2]
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Earth radius in kilometers
        
        return round(c * r, 2)
    
    def check_family_safety(self, affected_location, radius_km=5):
        """
        Check if any responder families are near the affected location
        Returns list of at-risk families
        """
        at_risk_families = []
        
        for responder in self.responders['responders']:
            family_location = responder['family']['location']
            distance = self.calculate_distance(affected_location, family_location)
            
            if distance is not None and distance <= radius_km:
                at_risk_families.append({
                    "responder_name": responder['name'],
                    "responder_id": responder['id'],
                    "responder_role": responder['role'],
                    "family_location": family_location,
                    "family_members": responder['family']['members'],
                    "distance_km": distance,
                    "contact": responder['family']['contact'],
                    "last_status": responder['family']['status'],
                    "alert_priority": self._calculate_alert_priority(distance, responder['family']['status']),
                    "affected_zone": affected_location
                })
        
        return sorted(at_risk_families, key=lambda x: x['distance_km'])
    
    def _calculate_alert_priority(self, distance, current_status):
        """Calculate alert priority based on distance and current status"""
        if current_status == "needs_help":
            return "CRITICAL"
        elif distance < 2:
            return "HIGH"
        elif distance < 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def update_family_status(self, responder_id, status, notes=""):
        """Update family safety status"""
        for responder in self.responders['responders']:
            if responder['id'] == responder_id:
                responder['family']['status'] = status
                responder['family']['last_contact'] = datetime.now().isoformat()
                if notes:
                    responder['family']['notes'] = notes
                break
        
        # Save updated data
        with open(self.responders_file, 'w') as f:
            json.dump(self.responders, f, indent=2)
    
    def get_all_family_status(self):
        """Get status of all responder families"""
        all_families = []
        
        for responder in self.responders['responders']:
            all_families.append({
                "responder_name": responder['name'],
                "responder_id": responder['id'],
                "responder_role": responder['role'],
                "assigned_zone": responder['assigned_zone'],
                "family_location": responder['family']['location'],
                "family_members": responder['family']['members'],
                "contact": responder['family']['contact'],
                "status": responder['family'].get('status', 'unknown'),
                "last_contact": responder['family'].get('last_contact'),
                "notes": responder['family'].get('notes', '')
            })
        
        return all_families
    
    def auto_ping_families(self, affected_location):
        """
        Simulate auto-ping to families in affected zones
        In real implementation, this would send SMS/WhatsApp
        """
        at_risk = self.check_family_safety(affected_location)
        
        ping_results = []
        for family in at_risk:
            ping_results.append({
                "responder_name": family['responder_name'],
                "responder_id": family['responder_id'],
                "family_location": family['family_location'],
                "distance_km": family['distance_km'],
                "contact": family['contact'],
                "ping_sent": True,
                "ping_time": datetime.now().isoformat(),
                "message": f"Auto-safety check: Are you safe? Reply YES/NO. Location: {affected_location}"
            })
        
        return ping_results


# Test function
if __name__ == "__main__":
    tracker = ResponderFamilyTracker()
    
    print("=" * 60)
    print("RESPONDER FAMILY SAFETY TRACKER - TEST")
    print("=" * 60)
    
    # Test affected location
    affected = "Tambaram"
    print(f"\n🚨 New emergency in: {affected}")
    print("\nChecking responder families within 10km...")
    
    at_risk = tracker.check_family_safety(affected, radius_km=10)
    
    if at_risk:
        print(f"\n⚠️  Found {len(at_risk)} responder families near affected zone:\n")
        for family in at_risk:
            print(f"👤 Responder: {family['responder_name']} ({family['responder_role']})")
            print(f"   📍 Family Location: {family['family_location']} ({family['distance_km']} km away)")
            print(f"   👨‍👩‍👧‍👦 Members: {', '.join(family['family_members'])}")
            print(f"   📞 Contact: {family['contact']}")
            print(f"   🚦 Alert Priority: {family['alert_priority']}")
            print(f"   ⏰ Status: {family['last_status']}")
            print()
    else:
        print("\n✅ No responder families in affected zone")
    
    # Test auto-ping
    print("\n" + "=" * 60)
    print("AUTO-PING TEST")
    print("=" * 60)
    
    pings = tracker.auto_ping_families(affected)
    print(f"\n📲 Sent {len(pings)} auto-safety pings:\n")
    for ping in pings:
        print(f"✉️  To: {ping['responder_name']}'s family")
        print(f"   📍 {ping['family_location']} ({ping['distance_km']} km from danger)")
        print(f"   📞 {ping['contact']}")
        print(f"   💬 Message: {ping['message']}")
        print()
