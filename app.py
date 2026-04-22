from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import json

# MySQL imports
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass
    
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'quantumpix_secret_key_2024'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1477'  # Update your password
app.config['MYSQL_DB'] = 'quantumpix'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Camera types with prices and images
CAMERAS = {
    'canon_r5': {
        'name': 'Canon EOS R5', 
        'price': 2500,
        'image': 'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0?w=300',
        'description': '45MP Full-Frame Mirrorless'
    },
    'sony_a7iii': {
        'name': 'Sony A7 III', 
        'price': 2000,
        'image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300',
        'description': '24MP Full-Frame Mirrorless'
    },
    'nikon_z6': {
        'name': 'Nikon Z6 II', 
        'price': 2200,
        'image': 'https://images.unsplash.com/photo-1510127034890-bc275c5f9a9f?w=300',
        'description': '24.5MP Full-Frame Mirrorless'
    },
    'fujifilm_xt4': {
        'name': 'Fujifilm X-T4', 
        'price': 1800,
        'image': 'https://images.unsplash.com/photo-1581595220892-b0739db3ba8c?w=300',
        'description': '26MP APS-C Mirrorless'
    }
}

# Event types with images and descriptions
EVENTS = [
    {'id': 'wedding', 'name': 'Wedding', 'icon': 'fa-ring', 'image': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=400', 'color': '#ff6b9d'},
    {'id': 'birthday', 'name': 'Birthday', 'icon': 'fa-birthday-cake', 'image': 'https://images.unsplash.com/photo-1464349153735-7db50ed83c35?w=400', 'color': '#ffa502'},
    {'id': 'prewedding', 'name': 'Pre-wedding', 'icon': 'fa-heart', 'image': 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400', 'color': '#e84393'},
    {'id': 'tourism', 'name': 'Tourism', 'icon': 'fa-plane', 'image': 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400', 'color': '#1e90ff'},
    {'id': 'corporate', 'name': 'Corporate', 'icon': 'fa-building', 'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400', 'color': '#2ed573'},
    {'id': 'fashion', 'name': 'Fashion', 'icon': 'fa-tshirt', 'image': 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=400', 'color': '#7bed9f'}
]

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                flash('Welcome back! ✨', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password!', 'danger')
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login error! Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        role = request.form.get('role', 'normal')
        
        # Validate input
        if not name or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        
        if len(password) < 4:
            flash('Password must be at least 4 characters long!', 'danger')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        
        try:
            cur = mysql.connection.cursor()
            
            # Check if email already exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            
            if existing_user:
                cur.close()
                flash('Email already exists! Please use a different email or login.', 'danger')
                return render_template('register.html')
            
            # Insert new user
            cur.execute("""
                INSERT INTO users (name, email, password, role) 
                VALUES (%s, %s, %s, %s)
            """, (name, email, hashed_password, role))
            
            mysql.connection.commit()
            cur.close()
            
            flash('✨ Registration successful! Please login to continue.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Registration error: {e}")
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        # Get recent bookings
        cur.execute("""
            SELECT b.*, p.name as photographer_name 
            FROM bookings b
            JOIN photographers p ON b.photographer_id = p.id
            WHERE b.user_id = %s
            ORDER BY b.created_at DESC
            LIMIT 3
        """, (session['user_id'],))
        recent_bookings = cur.fetchall()
        
        # Get total bookings count
        cur.execute("SELECT COUNT(*) as total FROM bookings WHERE user_id = %s", (session['user_id'],))
        total_bookings = cur.fetchone()['total']
        
        cur.close()
    except Exception as e:
        print(f"Dashboard error: {e}")
        recent_bookings = []
        total_bookings = 0
    
    return render_template('dashboard.html', 
                         events=EVENTS, 
                         cameras=CAMERAS,
                         recent_bookings=recent_bookings,
                         total_bookings=total_bookings)

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.*, p.name as photographer_name, p.image_url
            FROM bookings b
            JOIN photographers p ON b.photographer_id = p.id
            WHERE b.user_id = %s
            ORDER BY b.created_at DESC
        """, (session['user_id'],))
        bookings = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"My bookings error: {e}")
        bookings = []
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        event_type = request.form['event_type']
        camera_type = request.form['camera_type']
        days = int(request.form['days'])
        photographer_id = int(request.form['photographer_id'])
        
        camera_price = CAMERAS[camera_type]['price']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT price_per_day FROM photographers WHERE id = %s", (photographer_id,))
            photographer = cur.fetchone()
            
            if not photographer:
                flash('Photographer not found!', 'danger')
                return redirect(url_for('booking'))
            
            total_price = (camera_price + photographer['price_per_day']) * days
            
            cur.execute("""
                INSERT INTO bookings (user_id, photographer_id, event_type, camera_type, days, total_price, booking_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], photographer_id, event_type, camera_type, days, total_price, date.today(), 'confirmed'))
            mysql.connection.commit()
            
            booking_id = cur.lastrowid
            cur.close()
            
            flash('🎉 Booking confirmed successfully!', 'success')
            return redirect(url_for('confirmation', booking_id=booking_id))
        except Exception as e:
            print(f"Booking error: {e}")
            flash('Booking failed! Please try again.', 'danger')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, price_per_day, specialty, experience, rating FROM photographers WHERE available = TRUE")
        photographers = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"Fetch photographers error: {e}")
        photographers = []
    
    return render_template('booking.html', events=EVENTS, cameras=CAMERAS, photographers=photographers)

@app.route('/premium-booking', methods=['GET', 'POST'])
def premium_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        event_type = request.form['event_type']
        camera_type = request.form['camera_type']
        days = int(request.form['days'])
        photographer_id = int(request.form['photographer_id'])
        
        camera_price = CAMERAS[camera_type]['price']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT price_per_day FROM photographers WHERE id = %s", (photographer_id,))
            photographer = cur.fetchone()
            
            if not photographer:
                flash('Photographer not found!', 'danger')
                return redirect(url_for('premium_booking'))
            
            total_price = (camera_price + photographer['price_per_day']) * days
            
            cur.execute("""
                INSERT INTO bookings (user_id, photographer_id, event_type, camera_type, days, total_price, booking_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], photographer_id, event_type, camera_type, days, total_price, date.today(), 'confirmed'))
            mysql.connection.commit()
            
            booking_id = cur.lastrowid
            cur.close()
            
            flash('🎉 Premium booking confirmed!', 'success')
            return redirect(url_for('confirmation', booking_id=booking_id))
        except Exception as e:
            print(f"Premium booking error: {e}")
            flash('Booking failed!', 'danger')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, price_per_day, specialty, experience, rating FROM photographers WHERE available = TRUE")
        photographers = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"Fetch photographers error: {e}")
        photographers = []
    
    return render_template('premium_booking.html', events=EVENTS, cameras=CAMERAS, photographers=photographers)

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.*, p.name as photographer_name, p.price_per_day
            FROM bookings b
            JOIN photographers p ON b.photographer_id = p.id
            WHERE b.id = %s AND b.user_id = %s
        """, (booking_id, session['user_id']))
        booking = cur.fetchone()
        cur.close()
    except Exception as e:
        print(f"Confirmation error: {e}")
        booking = None
    
    return render_template('confirmation.html', booking=booking)

@app.route('/photographers')
def photographers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, name, specialty, experience, rating, price_per_day, image_url, available 
            FROM photographers 
            WHERE available = TRUE
        """)
        photographers = cur.fetchall()
        cur.close()
        
        # Ensure all photographers have default values for missing fields
        for p in photographers:
            if 'specialty' not in p or not p['specialty']:
                p['specialty'] = 'Professional Photographer'
            if 'experience' not in p or not p['experience']:
                p['experience'] = 5
            if 'rating' not in p or not p['rating']:
                p['rating'] = 4.5
                
    except Exception as e:
        print(f"Photographers error: {e}")
        photographers = []
    
    return render_template('photographers.html', photographers=photographers)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is admin
    if session.get('user_role') != 'admin':
        flash('Access denied! Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        bookings = cur.fetchall()
        cur.execute("SELECT id, name, email, role, created_at FROM users")
        users = cur.fetchall()
        cur.execute("SELECT * FROM photographers")
        photographers = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"Admin error: {e}")
        bookings = []
        users = []
        photographers = []
    
    return render_template('admin.html', bookings=bookings, users=users, photographers=photographers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)