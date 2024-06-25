from flask import Flask, session, Blueprint, render_template, request, flash, redirect, url_for
from utils import  update_userinfo, fetch_userdata, update_user_permissions, check_user_exists, encrypt_input, send_notification_email
from flask_bcrypt import Bcrypt

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '123456789'  # Set the secret key before any session-related operations

bcrypt = Bcrypt(app)  # Initialize Bcrypt

# Define views blueprint
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/searchAttributes')
def searchAttributes():
    if 'user' not in session:
        flash('You need to be logged in to access this page')
        return redirect(url_for('auth.login'))
    return render_template('searchAttributes.html')

@views.route('/uploadImage', methods=['GET', 'POST'])
def uploadImage():
    if 'user' not in session:
        flash('You need to be logged in to access this page')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        # Handle the image upload here
        flash('Image uploaded successfully')
        return redirect(url_for('views.uploadImage'))
    return render_template("uploadImage.html")

# Define auth blueprint
auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # Fetch user details including permissions
#         user_details = ["username", "password", "biofilm.user_info"]
#         user_details = fetch_userdata(username)
#         print("user_details",user_details)
#         if user_details and user_details['password'] == password:
#             # Set user session details
#             session['user'] = username
#             session['is_admin'] = user_details['isadmin'] == 1
#             session['upload_image_access'] = user_details['has_Upload_image_access'] == 1
#             return redirect(url_for('views.home'))
#         else:
#             flash('Invalid username or password')
#     return render_template("loginsam.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_credentials = fetch_userdata(email)

        #print("user_credentials", user_credentials)
        
        if user_credentials:
            stored_password = user_credentials.get('password')
            # Check if the stored password is a valid hash
            if stored_password and stored_password.startswith('$2b$'):
                if bcrypt.check_password_hash(stored_password, password):
                    session['user'] = email
                    session['is_admin'] = user_credentials.get('isadmin') == 1
                    session['upload_image_access'] = user_credentials.get('has_upload_image_access') == 1
                    return redirect(url_for('views.home'))
                else:
                    flash('Invalid username or password')
            else:
                flash('Invalid password format stored.')
        else:
            flash('Invalid username or password')

    return render_template("loginsam.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userinput = request.form
        user_details = check_user_exists(userinput['email'])
        if user_details:
            flash('Username or email already exists.', 'danger')  # Changed "error" to "danger" for Bootstrap
            return redirect(url_for('auth.signup'))
        #encrypted_password = encrypt_input(userinput['password'])
        hashed_password = bcrypt.generate_password_hash(userinput['password']).decode('utf-8')
        values_list = [userinput[key] for key in userinput.keys()][:3] + [hashed_password]
        if update_userinfo(values_list):
            flash('Account created successfully!', 'success')
        else:
            flash('Failed to register. Please try again.', 'danger')
        return redirect(url_for('auth.signup'))
    return render_template('signup.html')

@views.route('/grantAccess', methods=['GET', 'POST'])
def grantAccess():
    # Ensure user is logged in
    if 'user' not in session:
        flash('You need to be logged in to access this page', 'error')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        email = request.form.get('grantEmail')
        #username = request.form.get('grantUsername')
        upload_image_access = 'uploadImageAccess' in request.form
        admin_access = 'grantAccess' in request.form
        #print('username:', username)  # For debugging

        user = check_user_exists(email)
        if user:
            # Ensure the email matches the one stored, assuming user.email is the correct attribute
            if email != user["email"]:
                flash("Username and email don't match", 'error')
            else:
                # Update user permissions if email matches
                success = update_user_permissions(email, upload_image_access, admin_access)
                if success:
                    flash(f'Access granted successfully for {email}', 'success')
                    send_notification_email(email, session['user'])
                else:
                    flash(f'An error occurred while granting access for {email}', 'error')
        else:
            flash(f'User {email} not found', 'error')
        return redirect(url_for('views.grantAccess'))
    return render_template("grantAccess.html")

@auth.route('/logout')
def logout():
    session.pop('user', None)  # Log out the user by clearing session
    return redirect(url_for('views.home'))

# Register the blueprints
app.register_blueprint(views)
app.register_blueprint(auth)

