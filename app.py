from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'college-event-management-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_events_new.db'  # New database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models - Clean and Working
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='student')
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), default='general')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')

class LoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    session_duration = db.Column(db.Integer, nullable=True)

# Helper Functions
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))

        user = db.session.get(User, session['user_id'])
        if not user or user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def track_login(user_id):
    """Track user login activity"""
    try:
        activity = LoginActivity(
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:200] if request.headers.get('User-Agent') else ''
        )
        db.session.add(activity)

        # Update user's last login
        user = db.session.get(User, user_id)
        if user:
            user.last_login = datetime.utcnow()
        db.session.commit()

        # Store login activity ID in session for logout tracking
        session['login_activity_id'] = activity.id
    except Exception as e:
        print(f"Login tracking error: {e}")
        db.session.rollback()

def track_logout():
    """Track user logout activity"""
    try:
        if 'login_activity_id' in session:
            activity = db.session.get(LoginActivity, session['login_activity_id'])
            if activity:
                activity.logout_time = datetime.utcnow()
                if activity.login_time:
                    duration = (activity.logout_time - activity.login_time).total_seconds() / 60
                    activity.session_duration = int(duration)
                db.session.commit()
    except Exception as e:
        print(f"Logout tracking error: {e}")

# Routes
@app.route('/')
def index():
    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.event_date >= date.today(),
        Event.status == 'active'
    ).order_by(Event.event_date.asc()).limit(6).all()

    # Get stats for homepage
    total_events = Event.query.filter(Event.status == 'active').count()
    total_users = User.query.filter(User.role == 'student').count()
    total_registrations = Registration.query.count()

    return render_template('index.html',
                         events=upcoming_events,
                         total_events=total_events,
                         total_users=total_users,
                         total_registrations=total_registrations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()

        # Validation
        if not all([username, email, password, full_name]):
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use another email.', 'error')
            return render_template('register.html')

        # Create new user
        try:
            password_hash = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                full_name=full_name
            )

            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            print(f"Registration error: {e}")
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['full_name'] = user.full_name

            # Track login activity
            track_login(user.id)

            flash(f'Welcome back, {user.full_name}!', 'success')

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Track logout activity
    track_logout()

    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = db.session.get(User, session['user_id'])

    # Get user's registered events
    user_registrations = db.session.query(Event, Registration).join(
        Registration, Event.id == Registration.event_id
    ).filter(Registration.user_id == user.id).all()

    # Get available events for registration
    registered_event_ids = [reg.event_id for reg in Registration.query.filter_by(user_id=user.id).all()]
    available_events = Event.query.filter(
        Event.event_date >= date.today(),
        Event.status == 'active',
        ~Event.id.in_(registered_event_ids) if registered_event_ids else True
    ).order_by(Event.event_date.asc()).limit(8).all()

    # Get user stats
    upcoming_events = [reg for reg in user_registrations if reg[0].event_date >= date.today()]

    return render_template('dashboard.html',
                         user=user,
                         user_events=user_registrations,
                         available_events=available_events,
                         upcoming_count=len(upcoming_events))

@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get comprehensive stats
    total_events = Event.query.count()
    active_events = Event.query.filter(Event.status == 'active').count()
    total_users = User.query.count()
    student_users = User.query.filter(User.role == 'student').count()
    total_registrations = Registration.query.count()

    # Get recent login activities
    recent_logins = db.session.query(LoginActivity, User).join(
        User, LoginActivity.user_id == User.id
    ).order_by(LoginActivity.login_time.desc()).limit(10).all()

    # Get user activity stats
    active_today = LoginActivity.query.filter(
        LoginActivity.login_time >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()

    # Get recent events
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()

    # Get events by category for chart
    event_categories = db.session.query(Event.category, db.func.count(Event.id)).group_by(Event.category).all()

    return render_template('admin.html',
                         total_events=total_events,
                         active_events=active_events,
                         total_users=total_users,
                         student_users=student_users,
                         total_registrations=total_registrations,
                         recent_logins=recent_logins,
                         active_today=active_today,
                         recent_events=recent_events,
                         event_categories=event_categories)

@app.route('/admin/users')
@admin_required
def admin_users():
    # Get all users with their last login info
    users = User.query.order_by(User.created_at.desc()).all()

    # Get detailed login activities
    login_activities = db.session.query(LoginActivity, User).join(
        User, LoginActivity.user_id == User.id
    ).order_by(LoginActivity.login_time.desc()).limit(50).all()

    return render_template('admin_users.html', users=users, login_activities=login_activities)

@app.route('/events')
def events():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    date_filter = request.args.get('date', '')

    query = Event.query.filter(Event.status == 'active')

    if search:
        query = query.filter(Event.title.contains(search))

    if category:
        query = query.filter(Event.category == category)

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(Event.event_date == filter_date)
        except:
            pass

    events_list = query.order_by(Event.event_date.asc()).all()

    # Get event categories for filter
    categories = db.session.query(Event.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]

    return render_template('events.html',
                         events=events_list,
                         search=search,
                         category=category,
                         date_filter=date_filter,
                         categories=categories)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    is_registered = False
    registration_count = Registration.query.filter_by(event_id=event_id, status='registered').count()

    if 'user_id' in session:
        is_registered = Registration.query.filter_by(
            user_id=session['user_id'],
            event_id=event_id
        ).first() is not None

    return render_template('event_detail.html',
                         event=event,
                         is_registered=is_registered,
                         registration_count=registration_count)

@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_for_event(event_id):
    event = Event.query.get_or_404(event_id)
    user_id = session['user_id']

    # Check if already registered
    existing_registration = Registration.query.filter_by(
        user_id=user_id, event_id=event_id
    ).first()

    if existing_registration:
        flash('You are already registered for this event.', 'warning')
        return redirect(url_for('event_detail', event_id=event_id))

    # Check capacity
    current_registrations = Registration.query.filter_by(event_id=event_id, status='registered').count()
    if current_registrations >= event.capacity:
        flash('Event is full. Registration closed.', 'error')
        return redirect(url_for('event_detail', event_id=event_id))

    # Create registration
    try:
        new_registration = Registration(user_id=user_id, event_id=event_id)
        db.session.add(new_registration)
        db.session.commit()

        flash('Successfully registered for the event!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Registration failed. Please try again.', 'error')
        print(f"Registration error: {e}")

    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/create_event', methods=['GET', 'POST'])
@admin_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        event_date = request.form.get('event_date')
        event_time = request.form.get('event_time')
        venue = request.form.get('venue', '').strip()
        capacity = request.form.get('capacity')
        category = request.form.get('category', 'general')

        # Validation
        if not all([title, event_date, event_time, venue, capacity]):
            flash('All fields are required.', 'error')
            return render_template('create_event.html')

        try:
            capacity = int(capacity)
            if capacity <= 0:
                flash('Capacity must be a positive number.', 'error')
                return render_template('create_event.html')
        except ValueError:
            flash('Invalid capacity value.', 'error')
            return render_template('create_event.html')

        try:
            event_date_obj = datetime.strptime(event_date, '%Y-%m-%d').date()
            event_time_obj = datetime.strptime(event_time, '%H:%M').time()

            new_event = Event(
                title=title,
                description=description,
                event_date=event_date_obj,
                event_time=event_time_obj,
                venue=venue,
                capacity=capacity,
                category=category,
                created_by=session['user_id']
            )

            db.session.add(new_event)
            db.session.commit()

            flash('Event created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash('Failed to create event. Please check your inputs.', 'error')
            print(f"Event creation error: {e}")

    return render_template('create_event.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

def init_database():
    """Initialize database with fresh data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")

        # Create admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_password = generate_password_hash('admin123')
            admin = User(
                username='admin',
                email='admin@college.edu',
                password_hash=admin_password,
                full_name='System Administrator',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created - Username: admin, Password: admin123")

        # Create sample events
        if Event.query.count() == 0:
            sample_events = [
                Event(
                    title='Tech Fest 2025',
                    description='Annual technology festival featuring coding competitions, AI workshops, robotics demonstrations, and keynote speeches from industry leaders. Join us for three days of innovation and learning.',
                    event_date=date(2025, 1, 15),
                    event_time=datetime.strptime('09:00', '%H:%M').time(),
                    venue='Main Auditorium',
                    capacity=500,
                    category='technology',
                    created_by=1
                ),
                Event(
                    title='Cultural Night 2025',
                    description='A vibrant celebration of diversity through music, dance, drama, and art performances. Experience the rich cultural heritage of our college community.',
                    event_date=date(2025, 2, 14),
                    event_time=datetime.strptime('18:00', '%H:%M').time(),
                    venue='College Amphitheater',
                    capacity=1000,
                    category='cultural',
                    created_by=1
                ),
                Event(
                    title='Career Fair 2025',
                    description='Meet with top companies and explore exciting career opportunities. Network with recruiters, attend workshops, and learn about the latest industry trends.',
                    event_date=date(2025, 1, 25),
                    event_time=datetime.strptime('10:00', '%H:%M').time(),
                    venue='Sports Complex',
                    capacity=300,
                    category='career',
                    created_by=1
                ),
                Event(
                    title='Inter-College Sports Meet',
                    description='Annual sports tournament featuring cricket, football, basketball, tennis, and track events. Compete with the best athletes from neighboring colleges.',
                    event_date=date(2025, 3, 5),
                    event_time=datetime.strptime('08:00', '%H:%M').time(),
                    venue='Sports Ground',
                    capacity=800,
                    category='sports',
                    created_by=1
                ),
                Event(
                    title='Science Exhibition',
                    description='Showcase of innovative science projects, research presentations, and interactive experiments by students and faculty members.',
                    event_date=date(2025, 2, 20),
                    event_time=datetime.strptime('10:00', '%H:%M').time(),
                    venue='Science Building',
                    capacity=400,
                    category='academic',
                    created_by=1
                ),
                Event(
                    title='Entrepreneurship Summit',
                    description='Learn from successful entrepreneurs, attend pitch sessions, and discover how to turn your ideas into successful businesses.',
                    event_date=date(2025, 3, 12),
                    event_time=datetime.strptime('09:30', '%H:%M').time(),
                    venue='Conference Hall',
                    capacity=200,
                    category='career',
                    created_by=1
                )
            ]

            for event in sample_events:
                db.session.add(event)

            db.session.commit()
            print(f"✅ {len(sample_events)} sample events created")

"""if __name__ == '__main__':
    print("🚀 Starting College Event Management System...")
    print("🗄️ Initializing fresh database...")

    init_database()

    print("✅ System ready at http://localhost:5000")
    print("🔑 Admin Login: username='admin', password='admin123'") 
    print("📚 Student Registration: Create a new account or use existing student credentials")
    print("🎉 All features working: Events, Registration, Admin Panel, Login Tracking")
    print()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
"""
