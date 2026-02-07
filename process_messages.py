"""
Demo Script - Process existing emergency messages
Run this to populate the database with test data
PERSON 1 or PERSON 2 can run this
"""

from ai_processor import GeminiMessageProcessor
from priority_engine import PriorityEngine
from database import MessageDatabase
import os

def load_emergency_messages():
    """Load messages from the existing file"""
    try:
        with open("data/emergency_messages.txt", "r") as f:
            messages = [line.strip() for line in f.readlines() if line.strip()]
        return messages
    except FileNotFoundError:
        # Fallback test messages
        return [
            "Need food urgently near Tambaram, no food for 2 days",
            "Medical help needed for elderly person in Velachery",
            "No water available, family with children in Perungudi",
            "Shelter required after flooding near Saidapet at night",
            "Trapped in flooded building with pregnant woman in Tambaram - help immediately!",
            "Running out of medicine for diabetic child in Velachery, please send medical supplies",
            "Entire family of 6 without shelter in Perungudi after house collapse",
            "Elderly man having chest pain, cannot reach hospital in Saidapet",
            "Need drinking water urgently for 15 people in Tambaram community center",
            "Children crying from hunger, no food since yesterday morning in Velachery"
        ]

def main():
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        print("\n" + "="*60)
        print("⚠️  WARNING: GEMINI_API_KEY not set!")
        print("="*60)
        print("\nPlease set your API key first:")
        print("  Windows PowerShell: $env:GEMINI_API_KEY='your-api-key'")
        print("  Windows CMD: set GEMINI_API_KEY=your-api-key")
        print("  Linux/Mac: export GEMINI_API_KEY='your-api-key'")
        print("\nGet your free API key at: https://makersuite.google.com/app/apikey")
        print("\nUsing fallback keyword-based analysis instead...")
        print("="*60 + "\n")
    
    # Initialize components
    print("Initializing AI Processor...")
    processor = GeminiMessageProcessor()
    
    print("Initializing Priority Engine...")
    engine = PriorityEngine()
    
    print("Initializing Database...")
    db = MessageDatabase()
    
    # Clear existing messages (optional)
    print("\nClearing existing database...")
    db.clear_all()
    
    # Load emergency messages
    print("Loading emergency messages...")
    messages = load_emergency_messages()
    print(f"Found {len(messages)} messages to process\n")
    
    # Process each message
    print("="*60)
    print("PROCESSING MESSAGES WITH AI")
    print("="*60 + "\n")
    
    for i, msg_text in enumerate(messages, 1):
        print(f"[{i}/{len(messages)}] Processing: {msg_text[:60]}...")
        
        try:
            # AI Analysis
            analysis = processor.analyze_message(msg_text)
            
            # Priority Calculation
            priority = engine.calculate_priority_score(analysis)
            
            # Store in database
            db.add_message(msg_text, analysis, priority)
            
            print(f"  ✓ Need: {analysis['need_type']} | Location: {analysis['location']}")
            print(f"  ✓ Priority: {priority['urgency_level']} ({priority['total_score']:.1f}/100)")
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
            continue
    
    # Display statistics
    print("="*60)
    print("PROCESSING COMPLETE")
    print("="*60 + "\n")
    
    stats = db.get_statistics()
    print(f"Total Messages Processed: {stats['total_messages']}")
    print(f"\nBy Urgency Level:")
    print(f"  CRITICAL: {stats['by_urgency']['CRITICAL']}")
    print(f"  HIGH:     {stats['by_urgency']['HIGH']}")
    print(f"  MEDIUM:   {stats['by_urgency']['MEDIUM']}")
    print(f"  LOW:      {stats['by_urgency']['LOW']}")
    
    print(f"\nBy Location:")
    for loc, count in stats['by_location'].items():
        print(f"  {loc}: {count}")
    
    print("\n" + "="*60)
    print("🎉 SUCCESS! Database populated with processed messages")
    print("="*60)
    print("\nNext Steps:")
    print("1. Run the web application: python app.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. View the emergency responder dashboard")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
