"""
Resource Donation Portal
Connects safe zones with affected areas for resource donations
HACKATHON STANDOUT FEATURE #2
"""

import json
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import os

class ResourceDonationTracker:
    def __init__(self, 
                 donations_file='data/donations.json',
                 safe_zones_file='data/safe_zones.json'):
        self.donations_file = donations_file
        self.safe_zones_file = safe_zones_file
        self.donations = self._load_donations()
        self.safe_zones = self._load_safe_zones()
        
        # Approximate coordinates for Chennai locations (lat, lon)
        self.location_coords = {
            "Tambaram": (12.9249, 80.1000),
            "Velachery": (12.9756, 80.2201),
            "Perungudi": (12.9610, 80.2433),
            "Saidapet": (13.0210, 80.2231),
            "Porur": (13.0381, 80.1564),
            "Adyar": (13.0067, 80.2565),
            "T Nagar": (13.0418, 80.2341),
            "Anna Nagar": (13.0850, 80.2101),
            "Chrompet": (12.9516, 80.1462),
            "Mylapore": (13.0339, 80.2619)
        }
    
    def _load_donations(self):
        """Load donations data"""
        if os.path.exists(self.donations_file):
            with open(self.donations_file, 'r') as f:
                return json.load(f)
        else:
            sample_data = {
                "donations": [],
                "needs": []
            }
            os.makedirs('data', exist_ok=True)
            with open(self.donations_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            return sample_data
    
    def _load_safe_zones(self):
        """Load safe zones data"""
        if os.path.exists(self.safe_zones_file):
            with open(self.safe_zones_file, 'r') as f:
                return json.load(f)
        else:
            sample_data = {
                "safe_zones": [
                    {
                        "location": "Anna Nagar",
                        "status": "safe",
                        "resources_available": ["food", "water", "medical supplies"],
                        "contact_person": "Community Center - Anna Nagar",
                        "contact_number": "+91-9123456780"
                    },
                    {
                        "location": "T Nagar",
                        "status": "safe",
                        "resources_available": ["shelter", "food", "clothing"],
                        "contact_person": "Relief Center - T Nagar",
                        "contact_number": "+91-9123456781"
                    },
                    {
                        "location": "Adyar",
                        "status": "safe",
                        "resources_available": ["medical supplies", "water", "generators"],
                        "contact_person": "Adyar Relief Hub",
                        "contact_number": "+91-9123456782"
                    },
                    {
                        "location": "Porur",
                        "status": "safe",
                        "resources_available": ["food", "blankets", "hygiene kits"],
                        "contact_person": "Porur Community Hall",
                        "contact_number": "+91-9123456783"
                    }
                ]
            }
            os.makedirs('data', exist_ok=True)
            with open(self.safe_zones_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            return sample_data
    
    def calculate_distance(self, loc1, loc2):
        """Calculate distance between two locations in km"""
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
    
    def add_resource_need(self, location, need_type, quantity, urgency, description=""):
        """Add a resource need from an affected area"""
        need = {
            "id": f"need_{len(self.donations['needs']) + 1:03d}",
            "location": location,
            "need_type": need_type,
            "quantity": quantity,
            "urgency": urgency,
            "description": description,
            "status": "needed",
            "posted_time": datetime.now().isoformat(),
            "fulfilled_by": []
        }
        
        self.donations['needs'].append(need)
        self._save_donations()
        return need
    
    def add_donation_offer(self, donor_name, donor_location, resource_type, 
                          quantity, contact, notes=""):
        """Add a donation offer from a safe zone"""
        donation = {
            "id": f"don_{len(self.donations['donations']) + 1:03d}",
            "donor_name": donor_name,
            "donor_location": donor_location,
            "resource_type": resource_type,
            "quantity": quantity,
            "contact": contact,
            "notes": notes,
            "status": "available",
            "posted_time": datetime.now().isoformat(),
            "assigned_to": None
        }
        
        self.donations['donations'].append(donation)
        self._save_donations()
        return donation
    
    def find_nearby_donors(self, affected_location, resource_type, max_distance_km=15):
        """Find donors near the affected location"""
        nearby_donors = []
        
        for donation in self.donations['donations']:
            if (donation['status'] == 'available' and 
                donation['resource_type'] == resource_type):
                
                distance = self.calculate_distance(affected_location, donation['donor_location'])
                
                if distance is not None and distance <= max_distance_km:
                    nearby_donors.append({
                        **donation,
                        "distance_km": distance,
                        "estimated_time": self._estimate_travel_time(distance)
                    })
        
        return sorted(nearby_donors, key=lambda x: x['distance_km'])
    
    def find_safe_zones_for_donation(self, affected_location, max_distance_km=20):
        """Find safe zones near affected area where people can donate"""
        nearby_safe_zones = []
        
        for zone in self.safe_zones['safe_zones']:
            distance = self.calculate_distance(affected_location, zone['location'])
            
            if distance is not None and distance <= max_distance_km:
                nearby_safe_zones.append({
                    **zone,
                    "distance_km": distance,
                    "estimated_time": self._estimate_travel_time(distance),
                    "affected_area": affected_location
                })
        
        return sorted(nearby_safe_zones, key=lambda x: x['distance_km'])
    
    def _estimate_travel_time(self, distance_km):
        """Estimate travel time based on distance (assuming 20 km/h in disaster conditions)"""
        speed_kmh = 20
        hours = distance_km / speed_kmh
        minutes = int(hours * 60)
        return f"{minutes} mins"
    
    def get_resource_needs_summary(self):
        """Get summary of all resource needs by location"""
        summary = {}
        
        for need in self.donations['needs']:
            if need['status'] == 'needed':
                location = need['location']
                if location not in summary:
                    summary[location] = {
                        "location": location,
                        "needs": [],
                        "urgency_level": "LOW"
                    }
                
                summary[location]['needs'].append({
                    "type": need['need_type'],
                    "quantity": need['quantity'],
                    "urgency": need['urgency']
                })
                
                # Update overall urgency
                if need['urgency'] == 'CRITICAL':
                    summary[location]['urgency_level'] = 'CRITICAL'
                elif need['urgency'] == 'HIGH' and summary[location]['urgency_level'] != 'CRITICAL':
                    summary[location]['urgency_level'] = 'HIGH'
        
        return list(summary.values())
    
    def get_donation_matches(self, affected_location):
        """Get potential donation matches for an affected location"""
        matches = []
        
        # Get all needs for this location
        location_needs = [n for n in self.donations['needs'] 
                         if n['location'] == affected_location and n['status'] == 'needed']
        
        for need in location_needs:
            donors = self.find_nearby_donors(affected_location, need['need_type'])
            
            matches.append({
                "need_id": need['id'],
                "need_type": need['need_type'],
                "quantity_needed": need['quantity'],
                "urgency": need['urgency'],
                "available_donors": donors,
                "total_available": len(donors)
            })
        
        return matches
    
    def _save_donations(self):
        """Save donations to file"""
        with open(self.donations_file, 'w') as f:
            json.dump(self.donations, f, indent=2)
    
    def _save_safe_zones(self):
        """Save safe zones to file"""
        with open(self.safe_zones_file, 'w') as f:
            json.dump(self.safe_zones, f, indent=2)


# Test function
if __name__ == "__main__":
    tracker = ResourceDonationTracker()
    
    print("=" * 70)
    print("RESOURCE DONATION PORTAL - TEST")
    print("=" * 70)
    
    # Add some sample needs
    print("\n📋 ADDING RESOURCE NEEDS FROM AFFECTED AREAS:\n")
    
    needs = [
        ("Tambaram", "food", "50 kg rice", "HIGH", "Families without food for 2 days"),
        ("Velachery", "water", "100 liters", "CRITICAL", "No clean water available"),
        ("Perungudi", "medical supplies", "First aid kits", "HIGH", "Multiple injuries"),
    ]
    
    for location, need_type, quantity, urgency, desc in needs:
        need = tracker.add_resource_need(location, need_type, quantity, urgency, desc)
        print(f"✓ {location}: Needs {quantity} {need_type} - {urgency} urgency")
    
    # Add sample donations
    print("\n\n💝 ADDING DONATION OFFERS FROM SAFE ZONES:\n")
    
    donations = [
        ("Anna Nagar Community", "Anna Nagar", "food", "100 kg rice", "+91-9123456780"),
        ("T Nagar Relief Center", "T Nagar", "water", "200 liters", "+91-9123456781"),
        ("Adyar Hospital", "Adyar", "medical supplies", "10 first aid kits", "+91-9123456782"),
        ("Porur Volunteers", "Porur", "food", "75 kg rice", "+91-9123456783"),
    ]
    
    for name, location, resource, quantity, contact in donations:
        donation = tracker.add_donation_offer(name, location, resource, quantity, contact)
        print(f"✓ {name} ({location}): Offering {quantity} {resource}")
    
    # Find matches
    print("\n\n🔍 FINDING DONATION MATCHES FOR TAMBARAM:\n")
    
    affected = "Tambaram"
    matches = tracker.get_donation_matches(affected)
    
    for match in matches:
        print(f"Need: {match['need_type']} ({match['urgency']} urgency)")
        print(f"Quantity needed: {match['quantity_needed']}")
        print(f"Available donors: {match['total_available']}")
        
        if match['available_donors']:
            print("Nearby donors:")
            for donor in match['available_donors'][:3]:  # Show top 3
                print(f"  • {donor['donor_name']} ({donor['donor_location']})")
                print(f"    Distance: {donor['distance_km']} km | ETA: {donor['estimated_time']}")
                print(f"    Contact: {donor['contact']}")
        print()
    
    # Show safe zones for donations
    print("\n📍 SAFE ZONES WHERE PEOPLE CAN DONATE FOR TAMBARAM:\n")
    
    safe_zones = tracker.find_safe_zones_for_donation(affected, max_distance_km=15)
    
    for zone in safe_zones:
        print(f"✓ {zone['location']} - {zone['distance_km']} km away (ETA: {zone['estimated_time']})")
        print(f"  Contact: {zone['contact_person']} - {zone['contact_number']}")
        print(f"  Can accept: {', '.join(zone['resources_available'])}")
        print()
