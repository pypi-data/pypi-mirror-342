// Session tracking
let sessionStartTime = null;
let clickCount = 0;
let sessionId = null;
let currentPage = window.location.pathname + window.location.search;
let lastUpdate = null;
let checkInSchedule = [
    { interval: 10000, remaining: 1 },    // 10s
    { interval: 20000, remaining: 1 },    // 20s
    { interval: 30000, remaining: 1 },    // 30s
    { interval: 60000, remaining: 1 },    // 1m
    { interval: 180000, remaining: 1 },   // 3m
    { interval: 300000, remaining: 1 },   // 5m
];
let currentScheduleIndex = 0;
let activityLog = [];

// Get session ID from cookie or headers
function getSessionId() {
    if (!sessionId) {
        // First try to get from cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'session_id') {
                sessionId = value;
                break;
            }
        }
        
        // If no cookie, try headers
        if (!sessionId) {
            const headerSessionId = document.querySelector('meta[name="X-Session-ID"]')?.content;
            if (headerSessionId) {
                sessionId = headerSessionId;
            }
        }
    }
    return sessionId;
}

// Initialize or restore session data
function initializeSession() {
    // Get session ID first
    sessionId = getSessionId();
    
    // Initialize session start time if this is a new session
    if (!sessionStartTime) {
        const storedStartTime = localStorage.getItem('session_start_time_' + sessionId);
        if (storedStartTime) {
            sessionStartTime = parseInt(storedStartTime);
        } else {
            sessionStartTime = Date.now();
            localStorage.setItem('session_start_time_' + sessionId, sessionStartTime);
        }
    }
    
    // Initialize click count
    const storedClickCount = localStorage.getItem('click_count_' + sessionId);
    if (storedClickCount) {
        clickCount = parseInt(storedClickCount);
    }
    
    // Initialize activity log
    const storedLog = localStorage.getItem('activity_log_' + sessionId);
    if (storedLog) {
        activityLog = JSON.parse(storedLog);
    }
    
    // Log session start
    logActivity('Session started or resumed');
}

// Log activity with timestamp
function logActivity(action) {
    const entry = {
        timestamp: new Date().toISOString(),
        action: action,
        page: currentPage
    };
    activityLog.push(entry);
    
    // Keep only last 100 entries
    if (activityLog.length > 100) {
        activityLog = activityLog.slice(-100);
    }
    
    // Store updated log
    localStorage.setItem('activity_log_' + sessionId, JSON.stringify(activityLog));
}

// Track clicks
document.addEventListener('click', function(e) {
    clickCount++;
    localStorage.setItem('click_count_' + sessionId, clickCount);
    logActivity('Click recorded');
    updateSessionStats('click');
});

// Schedule next check-in
function scheduleNextUpdate() {
    if (!sessionId) return;
    
    // Clear any existing timeout
    if (window.sessionUpdateTimeout) {
        clearTimeout(window.sessionUpdateTimeout);
    }
    
    // Find the next applicable interval
    let nextInterval;
    if (currentScheduleIndex < checkInSchedule.length) {
        const schedule = checkInSchedule[currentScheduleIndex];
        if (schedule.remaining > 0) {
            nextInterval = schedule.interval;
            schedule.remaining--;
        } else {
            currentScheduleIndex++;
            if (currentScheduleIndex < checkInSchedule.length) {
                nextInterval = checkInSchedule[currentScheduleIndex].interval;
            } else {
                nextInterval = 300000; // Default to 5 minutes
            }
        }
    } else {
        nextInterval = 300000; // Default to 5 minutes
    }
    
    // Schedule next update
    window.sessionUpdateTimeout = setTimeout(() => {
        updateSessionStats('scheduled');
    }, nextInterval);
    
    logActivity(`Next check-in scheduled for ${nextInterval/1000}s`);
}

// Update session stats
function updateSessionStats(trigger) {
    if (!sessionId) return;
    
    const now = Date.now();
    const duration = Math.floor((now - sessionStartTime) / 1000); // Convert to seconds
    
    logActivity(`Updating session stats (trigger: ${trigger})`);
    
    fetch('/metrics/update-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Session-ID': sessionId
        },
        body: JSON.stringify({
            session_id: sessionId,
            duration: duration,
            clicks: clickCount,
            page_url: currentPage,
            activity_log: activityLog
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        logActivity('Session stats updated successfully');
        
        // If we're on the session analytics page, refresh the data
        if (window.location.pathname.includes('/metrics/session-analytics') && typeof loadSessionStats === 'function') {
            loadSessionStats();
        }
        
        // Schedule next update
        scheduleNextUpdate();
    }).catch(error => {
        logActivity(`Error updating session stats: ${error.message}`);
        console.error('Error updating session stats:', error);
        
        // Still schedule next update even if this one failed
        scheduleNextUpdate();
    });
}

// Update stats when page is about to be unloaded
window.addEventListener('beforeunload', function() {
    if (!sessionId) return;
    
    const duration = Math.floor((Date.now() - sessionStartTime) / 1000);
    logActivity('Page unloading - final update');
    
    // Use sendBeacon for more reliable delivery during page unload
    const data = {
        session_id: sessionId,
        duration: duration,
        clicks: clickCount,
        page_url: currentPage,
        activity_log: activityLog
    };
    
    const blob = new Blob([JSON.stringify(data)], {
        type: 'application/json'
    });
    
    navigator.sendBeacon('/metrics/update-session', blob);
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        logActivity('Page hidden');
    } else {
        logActivity('Page visible');
        updateSessionStats('visibility_change');
    }
});

// Initialize session tracking
document.addEventListener('DOMContentLoaded', function() {
    initializeSession();
    if (sessionId) {
        logActivity('Page loaded');
        updateSessionStats('page_load');
    }
}); 