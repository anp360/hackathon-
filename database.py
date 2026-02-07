"""
Simple JSON database for storing processed messages
PERSON 1: AI Backend Development
"""

import json
import os
from datetime import datetime
from config import DB_FILE

class MessageDatabase:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        if not os.path.exists(self.db_file):
            self._save_data({"messages": [], "metadata": {"last_updated": None}})
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
            return {"messages": [], "metadata": {"last_updated": None}}
    
    def _save_data(self, data):
        """Save data to JSON file"""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def add_message(self, original_message, analysis, priority, message_id=None):
        """Add a new processed message to database"""
        data = self._load_data()
        
        if message_id is None:
            message_id = len(data['messages']) + 1
        
        message_entry = {
            "id": message_id,
            "original_message": original_message,
            "analysis": analysis,
            "priority": priority,
            "status": "pending",  # pending, assigned, resolved
            "received_at": datetime.now().isoformat(),
            "assigned_to": None,
            "resolved_at": None,
            "notes": ""
        }
        
        data['messages'].append(message_entry)
        data['metadata']['last_updated'] = datetime.now().isoformat()
        
        self._save_data(data)
        return message_entry
    
    def get_all_messages(self):
        """Get all messages sorted by priority"""
        data = self._load_data()
        messages = data['messages']
        
        # Sort by priority score
        messages.sort(key=lambda x: x['priority']['total_score'], reverse=True)
        return messages
    
    def get_messages_by_location(self, location):
        """Filter messages by location"""
        messages = self.get_all_messages()
        
        if location.lower() == "all":
            return messages
            
        return [msg for msg in messages if msg['analysis']['location'].lower() == location.lower()]
    
    def get_messages_by_status(self, status="pending"):
        """Filter messages by status"""
        messages = self.get_all_messages()
        return [msg for msg in messages if msg['status'] == status]
    
    def update_message_status(self, message_id, status, assigned_to=None, notes=None):
        """Update message status"""
        data = self._load_data()
        
        for msg in data['messages']:
            if msg['id'] == message_id:
                msg['status'] = status
                if assigned_to:
                    msg['assigned_to'] = assigned_to
                if notes:
                    msg['notes'] = notes
                if status == "resolved":
                    msg['resolved_at'] = datetime.now().isoformat()
                break
        
        data['metadata']['last_updated'] = datetime.now().isoformat()
        self._save_data(data)
    
    def get_statistics(self):
        """Get summary statistics"""
        messages = self.get_all_messages()
        
        stats = {
            "total_messages": len(messages),
            "by_status": {
                "pending": len([m for m in messages if m['status'] == 'pending']),
                "assigned": len([m for m in messages if m['status'] == 'assigned']),
                "resolved": len([m for m in messages if m['status'] == 'resolved'])
            },
            "by_urgency": {
                "CRITICAL": len([m for m in messages if m['priority']['urgency_level'] == 'CRITICAL']),
                "HIGH": len([m for m in messages if m['priority']['urgency_level'] == 'HIGH']),
                "MEDIUM": len([m for m in messages if m['priority']['urgency_level'] == 'MEDIUM']),
                "LOW": len([m for m in messages if m['priority']['urgency_level'] == 'LOW'])
            },
            "by_location": {}
        }
        
        # Count by location
        for msg in messages:
            loc = msg['analysis']['location']
            stats['by_location'][loc] = stats['by_location'].get(loc, 0) + 1
        
        return stats
    
    def clear_all(self):
        """Clear all messages (use with caution!)"""
        self._save_data({"messages": [], "metadata": {"last_updated": datetime.now().isoformat()}})


# Test function
if __name__ == "__main__":
    db = MessageDatabase()
    
    # Test adding a message
    test_analysis = {
        "need_type": "medical",
        "location": "Velachery",
        "urgency_base_score": 9
    }
    
    test_priority = {
        "total_score": 85.5,
        "urgency_level": "CRITICAL"
    }
    
    db.add_message("Test emergency message", test_analysis, test_priority)
    
    print("=== Testing Message Database ===\n")
    print("All messages:", len(db.get_all_messages()))
    print("\nStatistics:")
    stats = db.get_statistics()
    print(json.dumps(stats, indent=2))
