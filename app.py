from flask import Flask
from datetime import timedelta
from backend.models import *
import os

app = None

def init_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', '786921')
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household.db"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.app_context().push()
    db.init_app(app)


    if not os.path.exists("household.db"):
        with app.app_context():
            db.create_all()
            Admin_Info.main_admin()
            print("Database created and default admin added.")

            
    else:
        print("Database already exists. No changes made.")

    return app


app = init_app()


from backend.models import *
from backend.auth import *
from backend.summary import *
from backend.admin_ms import *
from backend.dashboard import *
from backend.u_sr import *
from backend.p_sr import *
from backend.profile import *

if __name__ == "__main__":
    app.run(debug=True)


#just try???