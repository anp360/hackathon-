"""
Add demo data with GPS coordinates for delivery routes demo
"""
import json
from datetime import datetime

# Load existing data
with open('data/messages_db.json', 'r') as f:
    messages_data = json.load(f)

with open('data/donations.json', 'r') as f:
    donations_data = json.load(f)

# Add demo messages with GPS coordinates (Chennai area)
demo_messages = [
    {
        "id": 9001,
        "original_message": "Urgent: Family of 4 needs food and water at Tambaram - children crying from hunger",
        "message_text": "Urgent: Family of 4 needs food and water at Tambaram - children crying from hunger",
        "analysis": {
            "need_type": "food and water",
            "location": "Tambaram (12.9229, 80.1275)",
            "urgency_base_score": 9,
            "vulnerable_groups": ["children"],
            "has_immediate_danger": True,
            "needs_list": ["food", "water"],
            "estimated_people_count": 4
        },
        "priority": {
            "total_score": 92,
            "urgency_level": "CRITICAL",
            "score_breakdown": {
                "base_urgency": 27.0,
                "time_sensitivity": 25.0,
                "vulnerable_groups": 20.0,
                "immediate_danger": 15.0,
                "people_count": 5.0
            }
        },
        "status": "pending",
        "received_at": datetime.now().isoformat()
    },
    {
        "id": 9002,
        "original_message": "Elderly person needs medical supplies at Velachery - critical condition",
        "message_text": "Elderly person needs medical supplies at Velachery - critical condition",
        "analysis": {
            "need_type": "medical",
            "location": "Velachery (12.9756, 80.2219)",
            "urgency_base_score": 10,
            "vulnerable_groups": ["elderly"],
            "has_immediate_danger": True,
            "needs_list": ["medical supplies", "medicine"],
            "estimated_people_count": 1
        },
        "priority": {
            "total_score": 88,
            "urgency_level": "CRITICAL",
            "score_breakdown": {
                "base_urgency": 30.0,
                "time_sensitivity": 25.0,
                "vulnerable_groups": 20.0,
                "immediate_danger": 15.0,
                "people_count": 2.0
            }
        },
        "status": "pending",
        "received_at": datetime.now().isoformat()
    },
    {
        "id": 9003,
        "original_message": "Pregnant woman needs water and shelter at Adyar - immediate help required",
        "message_text": "Pregnant woman needs water and shelter at Adyar - immediate help required",
        "analysis": {
            "need_type": "water and shelter",
            "location": "Adyar (13.0067, 80.2571)",
            "urgency_base_score": 9,
            "vulnerable_groups": ["pregnant"],
            "has_immediate_danger": True,
            "needs_list": ["water", "shelter"],
            "estimated_people_count": 2
        },
        "priority": {
            "total_score": 85,
            "urgency_level": "HIGH",
            "score_breakdown": {
                "base_urgency": 27.0,
                "time_sensitivity": 20.0,
                "vulnerable_groups": 20.0,
                "immediate_danger": 15.0,
                "people_count": 3.0
            }
        },
        "status": "pending",
        "received_at": datetime.now().isoformat()
    }
]

# Add demo donations with GPS coordinates
demo_donations = [
    {
        "id": "demo_don_001",
        "donor_name": "Chrompet Relief Center",
        "location": "Chrompet (12.9517, 80.1410)",
        "resources": ["food", "water", "blankets"],
        "quantity": "100 kg rice, 200L water",
        "contact": "+91-9876543210",
        "status": "available",
        "posted_time": datetime.now().isoformat()
    },
    {
        "id": "demo_don_002",
        "donor_name": "Guindy Medical Center",
        "location": "Guindy (13.0067, 80.2206)",
        "resources": ["medical supplies", "medicine", "first aid"],
        "quantity": "20 first aid kits, medicines",
        "contact": "+91-9876543211",
        "status": "available",
        "posted_time": datetime.now().isoformat()
    },
    {
        "id": "demo_don_003",
        "donor_name": "T Nagar Community Kitchen",
        "location": "T Nagar (13.0418, 80.2341)",
        "resources": ["food", "water"],
        "quantity": "150 kg rice, 300L water",
        "contact": "+91-9876543212",
        "status": "available",
        "posted_time": datetime.now().isoformat()
    },
    {
        "id": "demo_don_004",
        "donor_name": "Saidapet Water Station",
        "location": "Saidapet (13.0214, 80.2231)",
        "resources": ["water", "shelter"],
        "quantity": "500L clean water",
        "contact": "+91-9876543213",
        "status": "available",
        "posted_time": datetime.now().isoformat()
    }
]

# Add demo data to existing
messages_data['messages'].extend(demo_messages)
donations_data['donations'].extend(demo_donations)

# Save updated data
with open('data/messages_db.json', 'w') as f:
    json.dump(messages_data, f, indent=2)

with open('data/donations.json', 'w') as f:
    json.dump(donations_data, f, indent=2)

print("✅ Added demo data:")
print(f"   - {len(demo_messages)} emergency messages with GPS coordinates")
print(f"   - {len(demo_donations)} donation centers with GPS coordinates")
print("\n📍 Now refresh the dashboard and click 'Generate Optimal Routes'!")
