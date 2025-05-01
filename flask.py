import os
import logging
from flask import Flask, request, redirect, send_from_directory, url_for, render_template, session, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps
import random

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = 'C:/Users/banshika/OneDrive/Desktop/cam/ball game/.vscode/my-website'

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# PostgreSQL connection parameters
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'gum_chat'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'banshika'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)

# In-memory storage for memes
memes = []

# Predefined meme templates with kind
meme_templates = [
    {'id': 1, 'url': 'https://i.imgflip.com/1bij.jpg', 'kind': 'funny'},  # Distracted Boyfriend
    {'id': 2, 'url': 'https://i.imgflip.com/1h7in3.jpg', 'kind': 'funny'},  # Drake Hotline Bling
    {'id': 3, 'url': 'https://i.imgflip.com/1g8my4.jpg', 'kind': 'motivational'},  # Change My Mind
    {'id': 4, 'url': 'https://i.imgflip.com/1o00in.jpg', 'kind': 'funny'},  # Two Buttons
    {'id': 5, 'url': 'https://i.imgflip.com/1ur9b0.jpg', 'kind': 'motivational'},  # Expanding Brain
    # Add more templates as needed...
]

# Create the templates directory if it doesn't exist
if not os.path.exists('public/templates'):
    os.makedirs('public/templates')

# User signup route
@app.route('/signup', methods=['POST'])
def signup():
    if 'profile_picture' not in request.files:
        return jsonify({"error": "Profile picture is required."}), 400

    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    data = request.form  # Use request.form to get other form data
    username = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    hashed_password = generate_password_hash(password)

    cursor = conn.cursor()
    try:
        # Check if the username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s;", (username, email))
        if cursor.fetchone():
            return jsonify({"error": "Username or email already exists."}), 409

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (username, email, password, profile_picture) VALUES (%s, %s, %s, %s) RETURNING id;",
            (username, email, hashed_password, file_path)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"User   {username} registered successfully.")

        return jsonify({"message": "User   registered successfully!", "redirect": url_for('login')}), 201
    except Exception as e:
        conn.rollback()
        logging.error(f"An error occurred during signup: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[1], password):
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration
        }, app.secret_key, algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'error': 'Unauthorized access'}), 401

        try:
            data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            current_user_id = data['user_id']
        except Exception as e:
            return jsonify({'error': 'Unauthorized access'}), 401

        return f(current_user_id, *args, **kwargs)
    return decorated_function

# Chat functionality routes
@app.route('/messages', methods=['GET'])
@token_required
def get_messages(current_user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC;")
    messages = cursor.fetchall()
    cursor.close()
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
@token_required
def send_message(current_user_id):
    data = request.json
    receiver_id = data['receiver_id']
    text = data['text']

    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, text, timestamp) VALUES (%s, %s, %s, NOW()) RETURNING id;", (current_user_id, receiver_id, text))
    message_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()

    return jsonify({
        'id': message_id,
        'sender': 'You',  # You can customize this to return the actual sender's name
        'text': text,
        'timestamp': datetime.datetime.now()  # Return the current timestamp
    }), 201

@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users;")
    users = cursor.fetchall()
    cursor.close()

    user_list = [{'id': user[0], 'username': user[1]} for user in users]
    return jsonify(user_list)

@app.route('/meme', methods=['GET'])
def get_memes():
    return jsonify(memes)

@app.route('/meme', methods=['POST'])
@token_required
def create_meme(current_user_id):
    data = request.json
    meme_id = data.get('meme_id')
    meme_template = next((meme for meme in meme_templates if meme['id'] == meme_id), None)

    if not meme_template:
        return jsonify({"error": "Meme template not found."}), 404

    meme = {
        'id': len(memes) + 1,
        'user_id': current_user_id,
        'template': meme_template,
        'text': data.get('text', ''),
        'created_at': datetime.datetime.now()
    }
    memes.append(meme)
    return jsonify(meme), 201

@app.route('/meme/random', methods=['GET'])
def get_random_meme():
    if not memes:
        return jsonify({"error": "No memes available."}), 404
    return jsonify(random.choice(memes))

@app.route('/meme/like/<int:meme_id>', methods=['POST'])
@token_required
def like_meme(current_user_id, meme_id):
    # Logic to like a meme (e.g., increment like count in the database)
    return jsonify({"message": "Meme liked!"}), 200

@app.route('/meme/comment/<int:meme_id>', methods=['POST'])
@token_required
def comment_on_meme(current_user_id, meme_id):
    data = request.json
    comment = data.get('comment')
    # Logic to add a comment to the meme (e.g., save to database)
    return jsonify({"message": "Comment added!"}), 201

@app.route('/meme/filter', methods=['GET'])
def filter_memes():
    kind = request.args.get('kind')
    filtered_memes = [meme for meme in memes if meme['template']['kind'] == kind]
    return jsonify(filtered_memes)

@app.route('/memes/<kind>', methods=['GET'])
def get_memes_by_kind(kind):
    filtered_memes = [meme for meme in memes if meme['template']['kind'] == kind]
    return jsonify(filtered_memes)

@app.route('/chat', methods=['GET'], endpoint='chat_page')
def chat_page():
    return render_template('chat.html')

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        return jsonify({"message": "User  is logged in", "user_id": session['user_id']}), 200
    else:
        return jsonify({"error": "User  is not logged in"}), 401

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Ensure this points to your contact.html file

@app.route('/getstarted')
def getstarted():
    return render_template('getstarted.html')

@app.route('/inbox')
def inbox():
    return render_template('inbox.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/AudioTrack')
def audio_track():
    return render_template('AudioTrack.html')

@app.route('/memehouse')
def memehouse():
    return render_template('memehouse.html')

@app.route('/videoshort')
def videoshort():
    return render_template('videoshort.html')

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('templates/images', path)

@app.route('/songs/<path:path>')
def send_songs(path):
    return send_from_directory('templates/songs', path)

@app.route('/swipematching', methods=['GET', 'POST'])
def swipematching():
    if request.method == 'POST':
        if 'profile_picture' not in request.files:
            return redirect(request.url)
        
        file = request.files['profile_picture']
        if file.filename == '':
            return redirect(request.url)
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Save the file path in session
        session['profile_picture_url'] = file_path
        
        return redirect(url_for('swipe_matching'))

    # For GET request
    profile_picture_url = session.get('profile_picture_url', None)
    return render_template('swipematching.html', profile_picture_url=profile_picture_url)

@app.route('/moodBoardProfiles')
def moodBoardProfiles():
    return render_template('moodBoardProfiles.html')

@app.route('/lovecalculator')
def lovecalculator():
    return render_template('lovecalculator.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/login', methods=['GET'], endpoint='login_page')
def login_page():
    return render_template('login.html')  # Render your login template

@app.route('/logout')
def logout():
    session.clear()
    logging.info("User   logged out successfully.")
    return redirect(url_for('home'))

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({"error": "Bad request: " + str(e)}), 400

@app.errorhandler(409)
def handle_conflict(e):
    return jsonify({"error": "Conflict: " + str(e)}), 409

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")
    return jsonify({"error": "An internal error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
