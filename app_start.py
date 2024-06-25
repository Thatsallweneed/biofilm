import os
from app.api.service import app


app.secret_key = '1234567890-0987654345678i9opo'
if __name__ == "__main__":
    app.run(port=int(os.environ['API_PORT']),debug=True, host='0.0.0.0') 
