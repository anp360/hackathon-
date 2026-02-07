"""Test route planner to see if it's working"""
import json
from route_planner import calculate_delivery_routes

# Load messages and donations
with open('data/messages_db.json', 'r') as f:
    messages_data = json.load(f)
    messages = messages_data['messages']

with open('data/donations.json', 'r') as f:
    donations_data = json.load(f)
    donations = donations_data['donations']

print(f"📊 Loaded {len(messages)} messages and {len(donations)} donations")

# Check for messages with GPS coordinates
messages_with_gps = [m for m in messages if '(' in m.get('analysis', {}).get('location', '')]
print(f"📍 Messages with GPS: {len(messages_with_gps)}")

# Check for donations with GPS coordinates
donations_with_gps = [d for d in donations if '(' in d.get('location', '')]
print(f"📍 Donations with GPS: {len(donations_with_gps)}")

# Show sample data
if messages_with_gps:
    print("\n✅ Sample message with GPS:")
    m = messages_with_gps[0]
    print(f"   Location: {m['analysis']['location']}")
    print(f"   Needs: {m['analysis'].get('needs_list', [])}")
    print(f"   Priority: {m['priority']['urgency_level']}")

if donations_with_gps:
    print("\n✅ Sample donation with GPS:")
    d = donations_with_gps[0]
    print(f"   Location: {d['location']}")
    print(f"   Resources: {d.get('resources', [])}")

# Try to calculate routes
print("\n🔄 Calculating routes...")
routes = calculate_delivery_routes(messages, donations)

print(f"\n✅ Found {len(routes)} routes!")
for i, route in enumerate(routes[:3]):
    print(f"\nRoute {i+1}:")
    print(f"  Priority: {route['urgency_level']} ({route['priority_score']}/100)")
    print(f"  From: {route['donor_location']}")
    print(f"  To: {route['request_location']}")
    print(f"  Distance: {route['distance_km']} km")
    print(f"  Resources: {route['available_resources']}")
