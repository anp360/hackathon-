# Crisis Need to Resource Matching Engine
# Final demo-ready version with urgency-based prioritization

from data.resources import resources

# -----------------------------
# Configuration
# -----------------------------

need_keywords = {
    "food": ["food", "hungry"],
    "water": ["water"],
    "medical": ["medical", "doctor", "injury", "help"],
    "shelter": ["shelter", "flood", "home"]
}

locations = ["Tambaram", "Velachery", "Perungudi", "Saidapet"]

urgency_keywords = ["urgent", "immediately", "help", "now"]
vulnerable_keywords = ["children", "child", "elderly", "old"]

urgency_rank = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

# -----------------------------
# Read emergency messages
# -----------------------------

with open("data/emergency_messages.txt", "r") as file:
    messages = file.readlines()

results = []

# -----------------------------
# Process each message
# -----------------------------

for msg in messages:
    msg_lower = msg.lower()

    detected_need = "unknown"
    detected_location = "unknown"
    urgency_score = 0

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

    if any(word in msg_lower for word in vulnerable_keywords):
        urgency_score += 2

    if "no food" in msg_lower or "no water" in msg_lower:
        urgency_score += 2

    if detected_need == "medical":
        urgency_score += 3

    # Determine urgency level
    if urgency_score >= 6:
        urgency_level = "HIGH"
    elif urgency_score >= 3:
        urgency_level = "MEDIUM"
    else:
        urgency_level = "LOW"

    # Resource matching
    matched_resource = None
    for resource in resources:
        if (
            resource["type"] == detected_need
            and resource["location"] == detected_location
            and resource["available"] > 0
        ):
            matched_resource = resource
            break

    # Store result
    results.append({
        "message": msg.strip(),
        "need": detected_need,
        "location": detected_location,
        "urgency_level": urgency_level,
        "urgency_rank": urgency_rank[urgency_level],
        "resource": matched_resource
    })

# -----------------------------
# Sort by urgency (HIGH → LOW)
# -----------------------------

results.sort(key=lambda x: x["urgency_rank"], reverse=True)

# -----------------------------
# Final Output
# -----------------------------

print("\n=== CRISIS RESOURCE MATCHING SYSTEM (PRIORITIZED) ===\n")

for item in results:
    print("Message:", item["message"])
    print(" → Need:", item["need"])
    print(" → Location:", item["location"])
    print(" → Urgency Level:", item["urgency_level"])

    if item["resource"]:
        print(
            f" → Assigned Resource: {item['resource']['type']} "
            f"from {item['resource']['location']} "
            f"(Available: {item['resource']['available']})"
        )
        print(" → Decision Reason: Closest available resource matching need and location")
    else:
        print(" → Assigned Resource: None")
        print(" → Decision Reason: No suitable resource currently available")

    print(" → Status: Ready for responder review")
    print("-" * 60)
