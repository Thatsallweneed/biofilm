import os
import sys
from core.metrics import time_it
from core.logger import get_logger
from cryptography.fernet import Fernet
from app.api.process import Process
from app.api import service
from core.logger import get_logger
import smtplib
from dotenv import load_dotenv
from datetime import datetime
current_date = datetime.now().strftime('%Y-%m-%d')

processor=Process()
config = processor.config
logger = get_logger(__name__)


load_dotenv("biofilm.env")



def send_notification_email(user_email, admin):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    key = os.getenv('KEY')
    subject = "Upload Image Access Granted Notification"

    message = f"""
    Hello,

    This message confirms that access has been successfully granted to the specified user account. Below are the details of the access grant:

    - User Email: {user_email}
    - Granted By: {admin}
    - Date of Grant: {current_date}

    This notification is generated automatically by the system. Please do not reply to this email.

    Thank you

    """

    text = f"Subject: {subject}\n\n{message}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, key)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# def encrypt_values_by_index(values_list):
#     # Generate a key
#     key = Fernet.generate_key()
#     cipher = Fernet(key)
#     # Encrypt email
#     encrypted_email = cipher.encrypt(values_list[3].encode())
#     values_list[3] = encrypted_email.decode()
#     # Encrypt password
#     encrypted_password = cipher.encrypt(values_list[4].encode())
#     values_list[4] = encrypted_password.decode()
#     return values_list


def encrypt_input(input_string):
    # Generate a key
    key = Fernet.generate_key()
    cipher = Fernet(key)
    # Encrypt the input string
    encrypted_value = cipher.encrypt(input_string.encode())
    return encrypted_value.decode()


def compare_password(user_data):
    if user_data:
        cipher = Fernet(user_data['key'])
        decrypted_password = cipher.decrypt(user_data['password']).decode()
        return user_data['password'] == decrypted_password  # Compare decrypted password
    else:
        return False  # Handle invalid username

def fetch_userdata(email):
    try:
        connection = service.db_conn()
        with connection.cursor() as cur:
            cur.execute("""
                SELECT email, password, has_upload_image_access, isadmin
                FROM biofilm.user_info
                WHERE email = %s
            """, (email,))
            result = cur.fetchone()
            return result
            # if result:
            #     return {
            #         'username': result['username'],
            #         'password': result['password'],
            #         'has_upload_image_access': result['has_upload_image_access'],
            #         'isadmin': result['isadmin']
            #     }
            # else:
            #     return None
    except Exception as e:
        logger.error(f"While processing in Function {fetch_userdata.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno}  File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")
        return None
    finally:
        connection.close()

def update_userinfo(valueslist):
    try:
        connection = service.db_conn()
        with connection.cursor() as cur:
            cur.executemany(config['userinfo_insert_query'], [tuple(valueslist)])
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"While processing in Function {update_userinfo.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno}  File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")


def update_user_permissions(email, has_upload_image_access, isadmin):
    try:
        connection = service.db_conn()
        with connection.cursor() as cur:
            cur.execute("""
                UPDATE Biofilm.user_info
                SET has_upload_image_access = %s, isadmin = %s
                WHERE  email = %s
            """, (has_upload_image_access, isadmin, email))
            connection.commit()
            return True
    except Exception as e:
        logger.error(f"While processing in Function {update_user_permissions.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno} File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")
        return False


def check_user_exists(email):
    try:
        connection = service.db_conn()
        with connection.cursor() as cur:
            # SQL query to check existence by username OR email
            sql_query = "SELECT email FROM Biofilm.user_info WHERE email = %s"
            cur.execute(sql_query, (email))
            user = cur.fetchone()
            return user
    except Exception as e:
        logger.error(f"While processing in Function {check_user_exists.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno} File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")
        return None
