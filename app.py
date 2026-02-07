"""
Flask Web Application for Emergency Responders
Real-time dashboard with location filtering
PERSON 2: Frontend Development
"""

from flask import Flask, render_template, request, jsonify, send_file
from ai_processor import GeminiMessageProcessor
from priority_engine import PriorityEngine
from database import MessageDatabase
from responder_family_tracker import ResponderFamilyTracker
from resource_donation_tracker import ResourceDonationTracker
from route_planner import calculate_delivery_routes
from datetime import datetime
import os
import base64

app = Flask(__name__)

# Initialize components
db = MessageDatabase()
ai_processor = None  # Will initialize when API key is set
priority_engine = PriorityEngine()
family_tracker = ResponderFamilyTracker()
donation_tracker = ResourceDonationTracker()

def init_ai_processor():
    """Initialize AI processor with API key"""
    global ai_processor
    try:
        ai_processor = GeminiMessageProcessor()
        return True
    except Exception as e:
        print(f"Warning: AI processor initialization failed: {e}")
        return False

# Initialize on startup
init_ai_processor()

@app.route('/')
def dashboard():
    """Main dashboard for emergency responders"""
    return render_template('dashboard_enhanced.html')

@app.route('/simple')
def simple_dashboard():
    """Simple dashboard (legacy)"""
    return render_template('dashboard.html')

@app.route('/api/messages')
def get_messages():
    """API endpoint to get messages with optional location filter"""
    location = request.args.get('location', 'all')
    status = request.args.get('status', 'all')
    
    if location.lower() == 'all':
        messages = db.get_all_messages()
    else:
        messages = db.get_messages_by_location(location)
    
    # Filter by status if specified
    if status.lower() != 'all':
        messages = [m for m in messages if m['status'] == status]
    
    return jsonify({
        "success": True,
        "messages": messages,
        "count": len(messages)
    })

@app.route('/api/statistics')
def get_statistics():
    """API endpoint for dashboard statistics"""
    stats = db.get_statistics()
    return jsonify({
        "success": True,
        "statistics": stats
    })

@app.route('/api/submit_message', methods=['POST'])
def submit_message():
    """API endpoint to submit and process a new emergency message"""
    data = request.json
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return jsonify({
            "success": False,
            "error": "Message text is required"
        }), 400
    
    if ai_processor is None:
        return jsonify({
            "success": False,
            "error": "AI processor not initialized. Please set GEMINI_API_KEY."
        }), 500
    
    try:
        # Step 1: AI Analysis
        analysis = ai_processor.analyze_message(message_text)
        
        # Step 2: Priority Calculation
        priority = priority_engine.calculate_priority_score(analysis)
        
        # Step 3: Store in database
        message_entry = db.add_message(message_text, analysis, priority)
        
        # Step 4: STANDOUT FEATURE - Auto-check responder family safety
        location = analysis.get('location', 'unknown')
        family_alerts = []
        if location != 'unknown':
            at_risk_families = family_tracker.check_family_safety(location, radius_km=10)
            if at_risk_families:
                # Auto-ping families in affected zone
                pings = family_tracker.auto_ping_families(location)
                family_alerts = at_risk_families
        
        # Step 5: STANDOUT FEATURE - Auto-add resource needs
        need_type = analysis.get('need_type', 'unknown')
        resource_alert = None
        if need_type in ['food', 'water', 'medical', 'shelter'] and location != 'unknown':
            urgency = priority['urgency_level']
            # Auto-create resource need
            resource_need = donation_tracker.add_resource_need(
                location, 
                need_type, 
                "Requested via emergency message",
                urgency,
                message_text[:100]
            )
            resource_alert = {
                "need_id": resource_need['id'],
                "nearby_donors": len(donation_tracker.find_nearby_donors(location, need_type))
            }
        
        return jsonify({
            "success": True,
            "message": "Message processed successfully",
            "data": message_entry,
            "family_safety_alerts": family_alerts,
            "resource_alert": resource_alert
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/update_status', methods=['POST'])
def update_status():
    """API endpoint to update message status"""
    data = request.json
    message_id = data.get('message_id')
    status = data.get('status')
    assigned_to = data.get('assigned_to')
    notes = data.get('notes')
    
    if not message_id or not status:
        return jsonify({
            "success": False,
            "error": "message_id and status are required"
        }), 400
    
    try:
        db.update_message_status(message_id, status, assigned_to, notes)
        return jsonify({
            "success": True,
            "message": "Status updated successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/process_bulk', methods=['POST'])
def process_bulk_messages():
    """Process messages from a file"""
    data = request.json
    messages = data.get('messages', [])
    
    if not messages:
        return jsonify({
            "success": False,
            "error": "No messages provided"
        }), 400
    
    if ai_processor is None:
        return jsonify({
            "success": False,
            "error": "AI processor not initialized"
        }), 500
    
    processed = []
    for msg_text in messages:
        try:
            analysis = ai_processor.analyze_message(msg_text)
            priority = priority_engine.calculate_priority_score(analysis)
            message_entry = db.add_message(msg_text, analysis, priority)
            processed.append(message_entry)
        except Exception as e:
            print(f"Error processing message: {e}")
            continue
    
    return jsonify({
        "success": True,
        "message": f"Processed {len(processed)} messages",
        "processed_count": len(processed)
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "ai_processor_ready": ai_processor is not None,
        "timestamp": datetime.now().isoformat()
    })

# ============================================================
# STANDOUT FEATURE #1: RESPONDER FAMILY SAFETY TRACKER
# ============================================================

@app.route('/api/family_safety/check', methods=['POST'])
def check_family_safety():
    """Check if responder families are in affected zone"""
    data = request.json
    affected_location = data.get('location')
    radius_km = data.get('radius_km', 10)
    
    if not affected_location:
        return jsonify({
            "success": False,
            "error": "Location is required"
        }), 400
    
    try:
        at_risk = family_tracker.check_family_safety(affected_location, radius_km)
        pings = family_tracker.auto_ping_families(affected_location)
        
        return jsonify({
            "success": True,
            "affected_location": affected_location,
            "families_at_risk": at_risk,
            "count": len(at_risk),
            "auto_pings_sent": pings
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/family_safety/all')
def get_all_family_status():
    """Get status of all responder families"""
    try:
        families = family_tracker.get_all_family_status()
        return jsonify({
            "success": True,
            "families": families,
            "count": len(families)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/family_safety/update', methods=['POST'])
def update_family_status():
    """Update family safety status"""
    data = request.json
    responder_id = data.get('responder_id')
    status = data.get('status')
    notes = data.get('notes', '')
    
    if not responder_id or not status:
        return jsonify({
            "success": False,
            "error": "responder_id and status are required"
        }), 400
    
    try:
        family_tracker.update_family_status(responder_id, status, notes)
        return jsonify({
            "success": True,
            "message": "Family status updated successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================
# STANDOUT FEATURE #2: RESOURCE DONATION PORTAL
# ============================================================

@app.route('/api/donations/needs', methods=['GET', 'POST'])
def manage_resource_needs():
    """Get or add resource needs"""
    if request.method == 'GET':
        try:
            summary = donation_tracker.get_resource_needs_summary()
            return jsonify({
                "success": True,
                "needs": summary
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    else:  # POST
        data = request.json
        location = data.get('location')
        need_type = data.get('need_type')
        quantity = data.get('quantity')
        urgency = data.get('urgency')
        description = data.get('description', '')
        
        if not all([location, need_type, quantity, urgency]):
            return jsonify({
                "success": False,
                "error": "location, need_type, quantity, and urgency are required"
            }), 400
        
        try:
            need = donation_tracker.add_resource_need(
                location, need_type, quantity, urgency, description
            )
            return jsonify({
                "success": True,
                "message": "Resource need added successfully",
                "data": need
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

@app.route('/api/donations/offer', methods=['POST'])
def offer_donation():
    """Submit a donation offer"""
    data = request.json
    donor_name = data.get('donor_name')
    donor_location = data.get('donor_location')
    resource_type = data.get('resource_type')
    quantity = data.get('quantity')
    contact = data.get('contact')
    notes = data.get('notes', '')
    
    if not all([donor_name, donor_location, resource_type, quantity, contact]):
        return jsonify({
            "success": False,
            "error": "All fields except notes are required"
        }), 400
    
    try:
        donation = donation_tracker.add_donation_offer(
            donor_name, donor_location, resource_type, quantity, contact, notes
        )
        return jsonify({
            "success": True,
            "message": "Donation offer submitted successfully",
            "data": donation
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/donations/offers')
def get_donation_offers():
    """Get all donation offers"""
    try:
        return jsonify({
            "success": True,
            "offers": donation_tracker.donations['donations']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/donations/matches/<location>')
def get_donation_matches(location):
    """Get donation matches for an affected location"""
    try:
        matches = donation_tracker.get_donation_matches(location)
        safe_zones = donation_tracker.find_safe_zones_for_donation(location)
        
        return jsonify({
            "success": True,
            "location": location,
            "matches": matches,
            "safe_zones": safe_zones
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/donations/safe_zones')
def get_safe_zones():
    """Get all safe zones"""
    try:
        return jsonify({
            "success": True,
            "safe_zones": donation_tracker.safe_zones['safe_zones']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================================================
# DELIVERY ROUTE PLANNING (STANDOUT FEATURE #3)
# ========================================================================

@app.route('/api/delivery/routes')
def get_delivery_routes():
    """Get optimized delivery routes matching urgent requests with donations"""
    try:
        # Get all messages and donations
        messages = db.get_all_messages()
        donations = donation_tracker.donations.get('donations', [])
        
        # Calculate optimal routes
        routes = calculate_delivery_routes(messages, donations)
        
        return jsonify({
            "success": True,
            "routes": routes,
            "total_routes": len(routes)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "routes": []
        }), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("🆘 RESQ-AI - SMART EMERGENCY RESPONSE")
    print("="*60)
    print(f"\n📍 Dashboard URL: http://localhost:5000")
    print("\n⚠️  Make sure to set GEMINI_API_KEY environment variable!")
    print("   Windows: $env:GEMINI_API_KEY='your-key-here'")
    print("   Linux/Mac: export GEMINI_API_KEY='your-key-here'")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

