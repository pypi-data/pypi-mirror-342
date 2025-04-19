from flask import Blueprint, request, jsonify, render_template, session
from flask_login import current_user, login_required
from .models import create_visit_model
from .utils import get_visitor_info
from datetime import datetime, timedelta
from sqlalchemy import func
import json
import uuid

class MetricsVisitors:
    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        if app is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        self.db = db
        
        # Create the Visit model
        self.Visit = create_visit_model(db)
        
        # Register the blueprint
        bp = Blueprint('metrics_visitors', __name__, 
                      template_folder='templates',
                      static_folder='static',
                      url_prefix='/metrics')
        
        # Register routes
        @bp.route('/')
        @login_required
        def metrics_dashboard():
            # Get visit statistics for the last 24 hours
            visits_24h = self.Visit.query.filter(
                self.Visit.timestamp >= datetime.utcnow() - timedelta(days=1)
            ).all()
            
            # Get unique visits for the last 24 hours
            unique_visits_24h = len(set(v.session_id for v in visits_24h))
            
            # Get visit statistics for the last 7 days
            visits_7d = self.Visit.query.filter(
                self.Visit.timestamp >= datetime.utcnow() - timedelta(days=7)
            ).all()
            
            # Get unique visits for the last 7 days
            unique_visits_7d = len(set(v.session_id for v in visits_7d))
            
            # Get geographical data
            locations = db.session.query(
                self.Visit.country, 
                func.count(self.Visit.id).label('count')
            ).group_by(self.Visit.country).all()
            
            # Get referrer data
            referrers = db.session.query(
                self.Visit.referrer,
                func.count(self.Visit.id).label('count')
            ).group_by(self.Visit.referrer).all()
            
            return render_template('metrics/dashboard.html',
                                 visits_24h=len(visits_24h),
                                 unique_visits_24h=unique_visits_24h,
                                 visits_7d=len(visits_7d),
                                 unique_visits_7d=unique_visits_7d,
                                 locations=locations,
                                 referrers=referrers)

        @bp.route('/data')
        @login_required
        def metrics_data():
            page = request.args.get('page', 1, type=int)
            per_page = 10
            
            visits = self.Visit.query.order_by(self.Visit.timestamp.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'visits': [{
                    'timestamp': visit.timestamp.isoformat(),
                    'ip': visit.ip,
                    'country': visit.country,
                    'city': visit.city,
                    'referrer': visit.referrer,
                    'user_agent': visit.user_agent
                } for visit in visits.items],
                'total': visits.total,
                'pages': visits.pages,
                'current_page': visits.page
            })

        @bp.route('/chart-data')
        @login_required
        def chart_data():
            now = datetime.utcnow()
            
            # Get hourly data for last 24 hours
            hourly_data = []
            for i in range(24):
                hour_start = now - timedelta(hours=i)
                hour_end = hour_start + timedelta(hours=1)
                
                visits = self.Visit.query.filter(
                    self.Visit.timestamp >= hour_start,
                    self.Visit.timestamp < hour_end
                ).all()
                
                unique_visits = len(set(v.session_id for v in visits))
                
                hourly_data.append({
                    'hour': hour_start.strftime('%H:00'),
                    'timestamp': hour_start.isoformat(),
                    'visits': len(visits),
                    'unique_visits': unique_visits
                })
            
            # Get daily data for last 7 days
            daily_data = []
            for i in range(7):
                day_start = now - timedelta(days=i)
                day_end = day_start + timedelta(days=1)
                
                visits = self.Visit.query.filter(
                    self.Visit.timestamp >= day_start,
                    self.Visit.timestamp < day_end
                ).all()
                
                unique_visits = len(set(v.session_id for v in visits))
                
                daily_data.append({
                    'day': day_start.strftime('%Y-%m-%d'),
                    'timestamp': day_start.isoformat(),
                    'visits': len(visits),
                    'unique_visits': unique_visits
                })
            
            return jsonify({
                'hourly': hourly_data,
                'daily': daily_data,
                'timezone': 'UTC'  # Indicate that timestamps are in UTC
            })

        @bp.route('/update-session', methods=['POST'])
        @login_required
        def update_session():
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'status': 'error', 'message': 'No data provided'}), 400
                    
                session_id = data.get('session_id')
                if not session_id:
                    return jsonify({'status': 'error', 'message': 'No session ID provided'}), 400
                    
                duration = data.get('duration', 0)
                clicks = data.get('clicks', 0)
                page_url = data.get('page_url')
                activity_log = data.get('activity_log', [])
                
                # Get the most recent visit for this session
                visit = self.Visit.query.filter_by(
                    session_id=session_id
                ).order_by(
                    self.Visit.timestamp.desc()
                ).first()
                
                current_time = datetime.utcnow()
                
                if visit:
                    # Update existing visit
                    visit.session_duration = duration
                    visit.total_clicks = clicks
                    visit.last_activity = current_time
                    
                    # Store activity log as JSON in the visit record
                    visit.activity_log = json.dumps(activity_log)
                    
                    # If the page URL has changed, create a new visit record
                    if page_url and visit.page_url != page_url:
                        new_visit = self.Visit(
                            user_id=current_user.id,
                            session_id=session_id,
                            ip=visit.ip,
                            country=visit.country,
                            city=visit.city,
                            referrer=request.referrer,
                            user_agent=request.user_agent.string,
                            page_url=page_url,
                            session_duration=duration,
                            total_clicks=clicks,
                            last_activity=current_time,
                            activity_log=json.dumps(activity_log)
                        )
                        db.session.add(new_visit)
                else:
                    # Create new visit record if none exists
                    visitor_info = get_visitor_info(request)
                    visit = self.Visit(
                        user_id=current_user.id,
                        session_id=session_id,
                        ip=visitor_info['ip'],
                        country=visitor_info['country'],
                        city=visitor_info['city'],
                        referrer=request.referrer,
                        user_agent=request.user_agent.string,
                        page_url=page_url,
                        session_duration=duration,
                        total_clicks=clicks,
                        last_activity=current_time,
                        activity_log=json.dumps(activity_log)
                    )
                    db.session.add(visit)
                
                db.session.commit()
                
                return jsonify({
                    'status': 'success',
                    'session_id': session_id,
                    'duration': duration,
                    'clicks': clicks,
                    'next_update': 'scheduled'  # Indicate that the frontend should schedule next update
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500

        @bp.route('/session-stats')
        @login_required
        def session_stats():
            # Get filter parameters
            session_id = request.args.get('session_id')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            # Base query
            query = self.Visit.query.filter(
                self.Visit.timestamp >= datetime.utcnow() - timedelta(days=1)
            )
            
            # Apply session filter if provided
            if session_id:
                query = query.filter_by(session_id=session_id)
            
            # Get paginated results
            paginated_visits = query.order_by(self.Visit.timestamp.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            # Get average session duration for last 24 hours
            avg_duration_24h = db.session.query(
                func.avg(self.Visit.session_duration)
            ).filter(
                self.Visit.timestamp >= datetime.utcnow() - timedelta(days=1)
            ).scalar() or 0
            
            # Get average clicks per session for last 24 hours
            avg_clicks_24h = db.session.query(
                func.avg(self.Visit.total_clicks)
            ).filter(
                self.Visit.timestamp >= datetime.utcnow() - timedelta(days=1)
            ).scalar() or 0
            
            # Get hourly session data
            hourly_data = []
            for i in range(24):
                hour_start = datetime.utcnow() - timedelta(hours=i)
                hour_end = hour_start + timedelta(hours=1)
                
                visits = self.Visit.query.filter(
                    self.Visit.timestamp >= hour_start,
                    self.Visit.timestamp < hour_end
                ).all()
                
                if visits:
                    avg_duration = sum(v.session_duration for v in visits) / len(visits)
                    avg_clicks = sum(v.total_clicks for v in visits) / len(visits)
                else:
                    avg_duration = 0
                    avg_clicks = 0
                
                hourly_data.append({
                    'timestamp': hour_start.isoformat(),
                    'avg_duration': avg_duration,
                    'avg_clicks': avg_clicks
                })
            
            # Get detailed session data
            sessions = []
            for visit in paginated_visits.items:
                # Get all pages visited in this session
                pages_visited = self.Visit.query.filter_by(
                    session_id=visit.session_id
                ).with_entities(
                    self.Visit.page_url,
                    self.Visit.timestamp
                ).order_by(self.Visit.timestamp.asc()).all()
                
                # Get session duration and clicks
                session_duration = visit.session_duration or 0
                total_clicks = visit.total_clicks or 0
                
                sessions.append({
                    'session_id': visit.session_id,
                    'timestamp': visit.timestamp.isoformat(),
                    'session_duration': session_duration,
                    'total_clicks': total_clicks,
                    'pages_visited': [{
                        'url': p[0] or 'Unknown',
                        'timestamp': p[1].isoformat()
                    } for p in pages_visited if p[0]],
                    'ip': visit.ip,
                    'country': visit.country,
                    'city': visit.city
                })
            
            return jsonify({
                'avg_duration_24h': avg_duration_24h,
                'avg_clicks_24h': avg_clicks_24h,
                'hourly': hourly_data,
                'sessions': sessions,
                'pagination': {
                    'total': paginated_visits.total,
                    'pages': paginated_visits.pages,
                    'current_page': paginated_visits.page,
                    'per_page': per_page
                }
            })

        @bp.route('/session-analytics')
        @login_required
        def session_analytics():
            return render_template('metrics/session_analytics.html')

        app.register_blueprint(bp)
        
        # Register before_request handler to track visits
        @app.before_request
        def track_visit():
            if current_user.is_authenticated and request.endpoint != 'static':
                # Get session ID from headers or cookies
                session_id = request.headers.get('X-Session-ID')
                
                # If no session ID in headers, check cookies
                if not session_id:
                    session_id = request.cookies.get('session_id')
                
                # Only create new session ID if none exists
                if not session_id:
                    session_id = str(uuid.uuid4())
                
                visitor_info = get_visitor_info(request)
                
                # Get the current page URL
                page_url = request.path
                if request.query_string:
                    page_url += '?' + request.query_string.decode('utf-8')
                    
                # Check if there's an existing visit for this session
                existing_visit = self.Visit.query.filter_by(
                    session_id=session_id
                ).order_by(self.Visit.timestamp.desc()).first()
                
                # Only create a new visit record if the page URL has changed
                if not existing_visit or existing_visit.page_url != page_url:
                    # Create new visit record
                    visit = self.Visit(
                        user_id=current_user.id,
                        session_id=session_id,
                        ip=visitor_info['ip'],
                        country=visitor_info['country'],
                        city=visitor_info['city'],
                        referrer=request.referrer,
                        user_agent=request.user_agent.string,
                        page_url=page_url,
                        session_duration=existing_visit.session_duration if existing_visit else 0,
                        total_clicks=existing_visit.total_clicks if existing_visit else 0,
                        last_activity=datetime.utcnow()
                    )
                    
                    db.session.add(visit)
                    db.session.commit()
                
                # Store session ID for after_request handler
                request.session_id = session_id

        @app.after_request
        def add_session_header(response):
            if hasattr(request, 'session_id'):
                response.headers['X-Session-ID'] = request.session_id
                # Also set a cookie for the session ID
                response.set_cookie('session_id', request.session_id, httponly=True, secure=True, samesite='Strict', max_age=86400)  # 24 hours
            return response 