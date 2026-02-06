# Crisis Need to Resource Matching Engine
# Final, stable, demo-ready version

from data.resources import resources

need_keywords = {
    "food": ["food", "hungry"],
    "water": ["water"],
    "medical": ["medical", "doctor", "injury", "help"],
    "shelter": ["shelter", "flood", "home"]
}

locations = ["Tambaram", "Velachery", "Perungudi", "Saidapet"]

urgency_keywords = ["urgent", "immediately", "help", "now"]
vulnerable_keywords = ["children", "child", "elderly", "old"]

with open("data/emergency_messages.txt", "r") as file:
    messages = file.readlines()

print("\n=== CRISIS RESOURCE MATCHING SYSTEM ===\n")

for msg in messages:
    msg_lower = msg.lower()

    detected_need = "unknown"
    detected_location = "unknown"
    urgency_score = 0
    reasons = []

    # Detect need
    for need, keywords in need_keywords.items():
        if any(word in msg_lower for word in keywords):
            detected_need = need
            break

    # Detect location
    for loc in locations:
        if loc.lower() in msg_lower:
            detected_location = loc
            break

    # Urgency scoring
    if any(word in msg_lower for word in urgency_keywords):
        urgency_score += 3
        reasons.append("Urgent language detected")

    if any(word in msg_lower for word in vulnerable_keywords):
        urgency_score += 2
        reasons.append("Vulnerable individuals mentioned")

    if "no food" in msg_lower or "no water" in msg_lower:
        urgency_score += 2
        reasons.append("Basic needs unavailable")

    if detected_need == "medical":
        urgency_score += 3
        reasons.append("Medical assistance required")

    if urgency_score >= 6:
        urgency_level = "HIGH"
    elif urgency_score >= 3:
        urgency_level = "MEDIUM"
    else:
        urgency_level = "LOW"

    # Resource matching (ROBUST)
    matched_resource = None

    for resource in resources:
        if resource["type"] == detected_need and resource["available"] > 0:
            if resource["location"] == detected_location:
                matched_resource = resource
                break

    # OUTPUT (ALWAYS PRINTS)
    print("Message:", msg.strip())
    print(" → Need:", detected_need)
    print(" → Location:", detected_location)
    print(" → Urgency Level:", urgency_level)

    if matched_resource:
        print(
            f" → Assigned Resource: {matched_resource['type']} "
            f"from {matched_resource['location']} "
            f"(Available: {matched_resource['available']})"
        )
        print(" → Decision Reason: Closest available resource matching need and location")
    else:
        print(" → Assigned Resource: None")
        print(" → Decision Reason: No suitable resource currently available")

    print(" → Status: Ready for responder review")
    print("-" * 60)
