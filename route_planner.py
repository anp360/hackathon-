"""
Route Planning System for Emergency Resource Delivery
Matches urgent requests with nearest available resources
"""

from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    return round(R * c, 2)

def extract_gps_from_location(location_str):
    """Extract GPS coordinates from location string"""
    try:
        if '(' in location_str and ')' in location_str:
            coords = location_str.split('(')[1].split(')')[0]
            lat, lon = coords.split(',')
            return float(lat.strip()), float(lon.strip())
    except:
        pass
    return None, None

def match_resources(needs, available):
    """Check if available resources match needs"""
    needs_lower = [n.lower() for n in needs]
    available_lower = [a.lower() for a in available]
    
    matches = []
    for need in needs_lower:
        for avail in available_lower:
            if need in avail or avail in need:
                matches.append(need)
                break
    
    return len(matches), matches

def calculate_delivery_routes(messages, donations):
    """
    Calculate optimal delivery routes matching urgent requests with donations
    
    Args:
        messages: List of emergency message dicts
        donations: List of donation dicts
        
    Returns:
        List of route dicts sorted by priority and distance
    """
    routes = []
    
    # Filter for high priority messages that need resources
    urgent_messages = [
        msg for msg in messages 
        if msg.get('priority', {}).get('urgency_level') in ['CRITICAL', 'HIGH']
        and msg.get('analysis', {}).get('needs_list')
    ]
    
    # Filter for available donations
    available_donations = [
        d for d in donations 
        if d.get('status') == 'available' and d.get('resources')
    ]
    
    for message in urgent_messages:
        msg_location = message.get('analysis', {}).get('location', 'unknown')
        msg_lat, msg_lon = extract_gps_from_location(msg_location)
        
        if not msg_lat or not msg_lon:
            continue
            
        needed_resources = message.get('analysis', {}).get('needs_list', [])
        if not needed_resources:
            continue
        
        best_match = None
        best_match_score = 0
        
        for donation in available_donations:
            donor_location = donation.get('location', '')
            donor_lat, donor_lon = extract_gps_from_location(donor_location)
            
            if not donor_lat or not donor_lon:
                continue
            
            # Calculate distance
            distance = haversine_distance(msg_lat, msg_lon, donor_lat, donor_lon)
            
            # Check resource match
            available_resources = donation.get('resources', [])
            match_count, matched_resources = match_resources(needed_resources, available_resources)
            
            if match_count == 0:
                continue
            
            # Calculate match score (higher is better)
            # Factor in: resource match percentage, inverse of distance
            match_percentage = (match_count / len(needed_resources)) * 100
            distance_score = max(0, 100 - distance)  # Closer is better
            match_score = (match_percentage * 0.7) + (distance_score * 0.3)
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_match = {
                    'message_id': message.get('id'),
                    'message_text': message.get('message_text', '')[:100],
                    'priority_score': message.get('priority', {}).get('total_score', 0),
                    'urgency_level': message.get('priority', {}).get('urgency_level', 'MEDIUM'),
                    'request_location': msg_location.split('(')[0].strip(),
                    'needed_resources': needed_resources,
                    'people_count': message.get('analysis', {}).get('estimated_people_count', 'Unknown'),
                    'donor_name': donation.get('donor_name', 'Anonymous'),
                    'donor_location': donor_location.split('(')[0].strip(),
                    'available_resources': available_resources,
                    'distance_km': distance,
                    'estimated_time': f"{int(distance * 2)} minutes" if distance < 10 else f"{int(distance / 40)} hours",
                    'match_quality': 'Perfect' if match_count == len(needed_resources) else 'Good',
                    'match_score': round(match_score, 2)
                }
        
        if best_match:
            routes.append(best_match)
    
    # Sort by priority score (descending) then distance (ascending)
    routes.sort(key=lambda x: (-x['priority_score'], x['distance_km']))
    
    return routes
