// Crisis Management AI Dashboard - JavaScript
// PERSON 2: Frontend Development

let allMessages = [];
let currentLocation = 'all';
let currentStatus = 'all';

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    refreshMessages();
    
    // Auto-refresh every 30 seconds
    setInterval(refreshMessages, 30000);
});

// Fetch and display messages
async function refreshMessages() {
    try {
        const response = await fetch(`/api/messages?location=${currentLocation}&status=${currentStatus}`);
        const data = await response.json();
        
        if (data.success) {
            allMessages = data.messages;
            displayMessages(allMessages);
            updateStatistics();
        } else {
            showError('Failed to load messages');
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
        showError('Network error. Please check connection.');
    }
}

// Display messages in the UI
function displayMessages(messages) {
    const container = document.getElementById('messages-container');
    
    if (messages.length === 0) {
        container.innerHTML = '<div class="loading">No messages found</div>';
        return;
    }
    
    container.innerHTML = messages.map(msg => createMessageCard(msg)).join('');
}

// Create HTML for a message card
function createMessageCard(msg) {
    const urgency = msg.priority.urgency_level;
    const analysis = msg.analysis;
    const priority = msg.priority;
    
    // Check if message has media
    const hasMedia = msg.media && msg.media.media_id;
    const mediaIcon = hasMedia ? `<span style="background: #9b59b6; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin-left: 8px;">📷 Media</span>` : '';
    const manualReview = msg.manually_reviewed ? `<span style="background: #f39c12; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin-left: 8px;">✓ Reviewed</span>` : '';
    
    return `
        <div class="message-card ${urgency}" onclick="showMessageDetail(${msg.id})">
            <div class="message-header">
                <span class="message-id">ID: ${msg.id}${mediaIcon}${manualReview}</span>
                <div>
                    <span class="urgency-badge ${urgency}">${urgency}</span>
                    <span class="status-badge ${msg.status}">${msg.status}</span>
                </div>
            </div>
            <div class="message-text">${escapeHtml(msg.original_message)}</div>
            <div class="message-info">
                <div class="info-item">
                    <strong>Need:</strong> ${analysis.need_type}
                </div>
                <div class="info-item">
                    <strong>📍 Location:</strong> ${analysis.location}
                </div>
                <div class="info-item">
                    <strong>⏰ Time:</strong> ${formatTime(msg.received_at)}
                </div>
                ${analysis.vulnerable_groups && analysis.vulnerable_groups.length > 0 ? 
                    `<div class="info-item">
                        <strong>⚠️ Vulnerable:</strong> ${analysis.vulnerable_groups.join(', ')}
                    </div>` : ''
                }
            </div>
            <div class="score-display">
                Priority Score: ${priority.total_score} / 100
            </div>
        </div>
    `;
}

// Show detailed message view
function showMessageDetail(messageId) {
    const msg = allMessages.find(m => m.id === messageId);
    if (!msg) return;
    
    const analysis = msg.analysis;
    const priority = msg.priority;
    
    // Media section (if available)
    let mediaSection = '';
    if (msg.media && msg.media.media_id) {
        const media = msg.media;
        const isImage = media.file_type.startsWith('image/');
        const isVideo = media.file_type.startsWith('video/');
        
        mediaSection = `
            <div class="detail-section" style="background: #f8f9fa;">
                <h3>📷 Attached Media ${msg.manually_reviewed ? '<span style="color: #f39c12;">(Manually Reviewed)</span>' : ''}</h3>
                <div style="text-align: center; padding: 20px;">
                    ${isImage ? `<img src="/api/media/${media.media_id}" style="max-width: 100%; max-height: 400px; border-radius: 8px; border: 2px solid #ddd;" />` : ''}
                    ${isVideo ? `<video controls src="/api/media/${media.media_id}" style="max-width: 100%; max-height: 400px; border-radius: 8px; border: 2px solid #ddd;"></video>` : ''}
                </div>
                ${media.vision_analysis ? `
                    <div style="margin-top: 15px; padding: 15px; background: white; border-radius: 8px;">
                        <h4 style="margin-bottom: 10px;">🤖 AI Vision Analysis</h4>
                        <p><strong>Description:</strong> ${media.vision_analysis.vision_description}</p>
                        <p><strong>Confidence:</strong> ${media.vision_analysis.confidence_score}%</p>
                        <p><strong>Detected Urgency:</strong> ${media.vision_analysis.detected_urgency}/10</p>
                        ${media.vision_analysis.detected_people ? `<p><strong>People Detected:</strong> ${media.vision_analysis.detected_people}</p>` : ''}
                        ${media.vision_analysis.requires_review ? '<p style="color: #e74c3c;"><strong>⚠️ Flagged for manual review</strong></p>' : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    const detailHtml = `
        <h2>Message Detail - ID: ${msg.id}</h2>
        
        <div class="detail-section">
            <h3>📝 Original Message</h3>
            <p style="font-size: 16px; font-weight: 500;">${escapeHtml(msg.original_message)}</p>
        </div>
        
        ${mediaSection}
        
        <div class="detail-section">
            <h3>🤖 AI Analysis</h3>
            <p><strong>Need Type:</strong> ${analysis.need_type}</p>
            <p><strong>Location:</strong> ${analysis.location}</p>
            <p><strong>Base Urgency Score:</strong> ${analysis.urgency_base_score}/10</p>
            <p><strong>Immediate Danger:</strong> ${analysis.has_immediate_danger ? 'YES ⚠️' : 'No'}</p>
            ${analysis.vulnerable_groups && analysis.vulnerable_groups.length > 0 ? 
                `<p><strong>Vulnerable Groups:</strong> ${analysis.vulnerable_groups.join(', ')}</p>` : ''
            }
            ${analysis.estimated_people_count ? 
                `<p><strong>Estimated People:</strong> ${analysis.estimated_people_count}</p>` : ''
            }
            ${analysis.keywords_found && analysis.keywords_found.length > 0 ? 
                `<p><strong>Keywords:</strong> ${analysis.keywords_found.join(', ')}</p>` : ''
            }
        </div>
        
        <div class="detail-section">
            <h3>⚡ Priority Assessment</h3>
            <p><strong>Overall Score:</strong> ${priority.total_score}/100</p>
            <p><strong>Urgency Level:</strong> <span class="urgency-badge ${priority.urgency_level}">${priority.urgency_level}</span></p>
            <p><strong>Score Breakdown:</strong></p>
            <ul style="list-style: none; padding-left: 20px;">
                <li>• Base Urgency: ${priority.score_breakdown.base_urgency.toFixed(1)}</li>
                <li>• Time Sensitivity: ${priority.score_breakdown.time_sensitivity.toFixed(1)}</li>
                <li>• Vulnerable Groups: ${priority.score_breakdown.vulnerable_groups.toFixed(1)}</li>
                <li>• Immediate Danger: ${priority.score_breakdown.immediate_danger.toFixed(1)}</li>
                <li>• People Count: ${priority.score_breakdown.people_count.toFixed(1)}</li>
            </ul>
        </div>
        
        <div class="detail-section">
            <h3>📋 Priority Reasons</h3>
            <ul class="reasons-list">
                ${priority.priority_reasons.map(reason => `<li>${reason}</li>`).join('')}
            </ul>
        </div>
        
        <div class="detail-section">
            <h3>📊 Status Management</h3>
            <p><strong>Current Status:</strong> <span class="status-badge ${msg.status}">${msg.status}</span></p>
            <p><strong>Received:</strong> ${formatTime(msg.received_at)}</p>
            ${msg.assigned_to ? `<p><strong>Assigned To:</strong> ${msg.assigned_to}</p>` : ''}
            ${msg.resolved_at ? `<p><strong>Resolved:</strong> ${formatTime(msg.resolved_at)}</p>` : ''}
            ${msg.notes ? `<p><strong>Notes:</strong> ${msg.notes}</p>` : ''}
        </div>
        
        <div class="modal-actions">
            <button class="btn btn-success" onclick="updateMessageStatus(${msg.id}, 'assigned')">Assign</button>
            <button class="btn btn-primary" onclick="updateMessageStatus(${msg.id}, 'resolved')">Resolve</button>
            <button class="btn btn-secondary" onclick="closeDetailModal()">Close</button>
        </div>
    `;
    
    document.getElementById('message-detail').innerHTML = detailHtml;
    document.getElementById('detail-modal').style.display = 'block';
}

// Update message status
async function updateMessageStatus(messageId, newStatus) {
    try {
        const response = await fetch('/api/update_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message_id: messageId,
                status: newStatus,
                assigned_to: newStatus === 'assigned' ? 'Responder Team' : null
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            closeDetailModal();
            refreshMessages();
            showSuccess('Status updated successfully');
        } else {
            showError('Failed to update status');
        }
    } catch (error) {
        console.error('Error updating status:', error);
        showError('Network error');
    }
}

// Filter messages
function filterMessages() {
    currentLocation = document.getElementById('location-filter').value;
    currentStatus = document.getElementById('status-filter').value;
    refreshMessages();
}

// Update statistics display
async function updateStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            document.getElementById('stat-critical').textContent = stats.by_urgency.CRITICAL || 0;
            document.getElementById('stat-high').textContent = stats.by_urgency.HIGH || 0;
            document.getElementById('stat-medium').textContent = stats.by_urgency.MEDIUM || 0;
            document.getElementById('stat-low').textContent = stats.by_urgency.LOW || 0;
        }
    } catch (error) {
        console.error('Error fetching statistics:', error);
    }
}

// Submit new message modal
function showSubmitModal() {
    document.getElementById('submit-modal').style.display = 'block';
    document.getElementById('new-message').value = '';
    document.getElementById('submit-result').innerHTML = '';
}

function closeSubmitModal() {
    document.getElementById('submit-modal').style.display = 'none';
}

function closeDetailModal() {
    document.getElementById('detail-modal').style.display = 'none';
}

// Submit new emergency message
async function submitMessage() {
    const messageText = document.getElementById('new-message').value.trim();
    
    if (!messageText) {
        showSubmitError('Please enter a message');
        return;
    }
    
    const resultDiv = document.getElementById('submit-result');
    resultDiv.innerHTML = 'Processing...';
    resultDiv.className = '';
    
    try {
        const response = await fetch('/api/submit_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: messageText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = '✓ Message processed successfully!';
            resultDiv.className = 'success';
            
            setTimeout(() => {
                closeSubmitModal();
                refreshMessages();
            }, 1500);
        } else {
            showSubmitError(data.error || 'Failed to process message');
        }
    } catch (error) {
        console.error('Error submitting message:', error);
        showSubmitError('Network error. Please try again.');
    }
}

function showSubmitError(message) {
    const resultDiv = document.getElementById('submit-result');
    resultDiv.innerHTML = '✗ ' + message;
    resultDiv.className = 'error';
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTime(timestamp) {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

function showError(message) {
    console.error(message);
    // Could add toast notification here
}

function showSuccess(message) {
    console.log(message);
    // Could add toast notification here
}

// Close modals on outside click
window.onclick = function(event) {
    const submitModal = document.getElementById('submit-modal');
    const detailModal = document.getElementById('detail-modal');
    
    if (event.target === submitModal) {
        closeSubmitModal();
    }
    if (event.target === detailModal) {
        closeDetailModal();
    }
}
