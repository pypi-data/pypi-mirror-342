from datetime import datetime

def create_visit_model(db):
    """Create and return the Visit model class"""
    class Visit(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        session_id = db.Column(db.String(36), nullable=False)  # For tracking unique visits
        ip = db.Column(db.String(45), nullable=False)
        country = db.Column(db.String(2), nullable=True)
        city = db.Column(db.String(100), nullable=True)
        referrer = db.Column(db.String(500), nullable=True)
        user_agent = db.Column(db.String(500), nullable=True)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        session_duration = db.Column(db.Integer, default=0)  # Duration in seconds
        total_clicks = db.Column(db.Integer, default=0)
        last_activity = db.Column(db.DateTime, default=datetime.utcnow)
        page_url = db.Column(db.String(500), nullable=True)  # Track which page was visited

        def __repr__(self):
            return f'<Visit {self.id}>'
    
    return Visit 