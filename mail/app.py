# importing libraries 
from flask import Flask 
from flask_mail import Mail, Message 

app = Flask(__name__) 
mail = Mail(app) # instantiate the mail class 

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'updatesofaccess@gmail.com'
app.config['MAIL_PASSWORD'] = 'biofilm#987654321'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Use an app-specific password if 2FA is enabled
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return 'Welcome to the Flask Mail Sender!'

@app.route('/send-mail/')
def send_mail():
    try:
        msg = Message(
            'Hello from Flask-Mail',
            sender='your-email@gmail.com',
            recipients=['recipient-email@example.com'],
            body='This is a test email sent from a Flask application using Flask-Mail.'
        )
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)


# message object mapped to a particular URL ‘/’ 
@app.route("/") 
def index(): 
    msg = Message( 'Hello', sender ='updatesofaccess@gmail.com', recipients = ['sherlocksk859@gmail.com'] ) 
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg) 
    return 'Sent'

if __name__ == '__main__': 
    app.run(debug = True) 
