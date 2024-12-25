from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAlchemyEnum  
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()



class ProfessionalStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    BLOCKED = 'Blocked'

class ServiceStatus(Enum):
    REQUESTED = 'Requested'
    ASSIGNED = 'Assigned'
    ONGOING = 'Ongoing'
    COMPLETED = 'Completed'
    CLOSED = 'Closed'



class Admin_Info(db.Model):
    __tablename__ = "admin_info"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    @staticmethod
    def main_admin():
        
        admin = Admin_Info.query.first()  
        if not admin:
            
            new_admin = Admin_Info(
                email="Admin@xyz.com",  
                pwd=generate_password_hash("Admin@123"),  
                full_name="Admin Afsar!",
                address="Lucknow",
                pincode=226030,
                phone_number="8604766241",
                created_at=datetime.now()
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin created.")
        else:
            print("Admin already exists.")

class User_Info(db.Model):
    __tablename__ = "user_info"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)

class Professional_Info(db.Model):
    __tablename__ = "professional_info"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    resume_filename = db.Column(db.String, nullable=True)
    status = db.Column(SQLAlchemyEnum(ProfessionalStatus), default=ProfessionalStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.now())

    
    service = db.relationship('Service', backref='professionals', lazy=True)


class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String, nullable=True)
    time_required = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional_info.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.now())
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(SQLAlchemyEnum(ServiceStatus), default=ServiceStatus.REQUESTED)
    review = db.Column(db.Text, nullable=True)  
    rating = db.Column(db.Integer, nullable=True)  

