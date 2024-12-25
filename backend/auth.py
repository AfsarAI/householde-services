from datetime import datetime
from flask import Flask, flash, logging, render_template, request, redirect, send_from_directory, session, url_for
from backend.helper import set_session
from .models import ProfessionalStatus, db, User_Info, Professional_Info, Admin_Info, Service
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from werkzeug.utils import secure_filename
import logging
import os



# Image files serve karne ke liye route
@app.route('/static/img/<path:filename>')
def uploaded_file_body(filename):
    images_folder = r'C:\Users\moham\OneDrive\Desktop\Project Files\images'
    return send_from_directory(images_folder, filename)


@app.route('/')
@app.route('/HomeWizard/home')
def home():
    return render_template('home.html')


@app.route('/HomeWizard/contact')
def contact():
    admin = db.session.query(Admin_Info).first()
    return render_template('contact.html', admin=admin)

@app.route('/HomeWizard/register/user', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('fullname')
        dob = request.form.get('dob')
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        gender = request.form.get('gender')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        phone_number = request.form.get('phone')

        existing_user = User_Info.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please login or use a different email.', 'danger')
            return redirect(url_for('user_register'))

        
        hashed_password = generate_password_hash(password)
        new_user = User_Info(
            email=email, pwd=hashed_password, full_name=full_name, dob=dob_date, gender=gender,
            address=address, pincode=pincode, phone_number=phone_number, created_at=datetime.now()
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please login to continue.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  
            flash('Error: Unable to complete signup. Please try again.', 'danger')
            return redirect(url_for('user_register'))
        
    return render_template('user_signup.html')



@app.route('/HomeWizard/register/professional', methods=['GET', 'POST'])
def professional_register():
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password') 
        full_name = request.form.get('fullname') 
        dob = request.form.get('dob')
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        gender = request.form.get('gender')
        address = request.form.get('address') 
        pincode = request.form.get('pincode') 
        phone_number = request.form.get('mobile') 
        experience = request.form.get('experience') 
        service_id = int(request.form.get('service_name'))
        file = request.files.get('file_attachment')

        
        existing_professional = Professional_Info.query.filter_by(email=email).first()
        if existing_professional:
            flash('Email address already exists. Please try a different one.', 'danger')
            return redirect(url_for('professional_register'))

        
        resume_filename = None
        if file:
            resume_filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
            file.save(upload_path)

        
        hashed_password = generate_password_hash(password)
        new_professional = Professional_Info(
            email=email, pwd=hashed_password, full_name=full_name, dob=dob_date, gender=gender,
            address=address, pincode=pincode, phone_number=phone_number,
            service_id=service_id, experience=experience, resume_filename=resume_filename, created_at=datetime.now()
        )
        
        try:
            db.session.add(new_professional)
            db.session.commit()
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: Unable to complete registration. Please try again.', 'danger')
            return redirect(url_for('professional_register'))
    
    all_services = Service.query.all()
    return render_template('professional_signup.html', services=all_services)



@app.route('/HomeWizard/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        
        admin = Admin_Info.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.pwd, pwd):  
            set_session(id=admin.id, email=admin.email, role='admin')
            return redirect(url_for('dashboard', role='admin', id=admin.id))
        
        flash("Invalid email or password.", 'danger')
    return render_template('admin_login.html')



@app.route('/HomeWizard/login/user/professional', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        role = request.form.get('role')

        if role == 'user':
            user = User_Info.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.pwd, pwd):  
                    set_session(id=user.id, email=user.email, role=role)
                    return redirect(url_for('dashboard', id=user.id, role=role))
                else:
                    flash('Invalid password!', 'danger')
            else:
                flash('Invalid email!', 'danger')
        
        elif role == 'professional':
            professional = Professional_Info.query.filter_by(email=email).first()
            
            if professional:
                if check_password_hash(professional.pwd, pwd):  
                
                    if professional.status == ProfessionalStatus.PENDING:
                        flash('Your request is still pending approval from the admin.', 'warning')
                    elif professional.status == ProfessionalStatus.REJECTED:
                        flash('Your request has been rejected by the admin.', 'danger')
                    else:
                        set_session(id=professional.id, email=professional.email, role=role)
                        return redirect(url_for('dashboard', id=professional.id, role=role))
                else:
                    flash('Invalid password!', 'danger')
            else:
                flash('Invalid email!', 'danger')
        
        else:
            flash('Role is not defined.', 'danger')

    return render_template('uplogin.html')

@app.route('/HomeWizard/reset/password', methods=['POST'])
def reset_password():
    role = request.form.get('role')
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        flash('Passwords do not match. Please try again.', 'danger')
        return redirect(url_for('login'))

    hashed_password = generate_password_hash(new_password)

    if role == 'user':
        user = User_Info.query.filter_by(email=email).first()
        user.pwd = hashed_password
        db.session.commit()
        flash("Password updated successfully!", "success")
        return redirect(url_for('login'))
    elif role == 'professional':
        pro = Professional_Info.query.filter_by(email=email).first()
        pro.pwd = hashed_password
        db.session.commit()
        flash("Password updated successfully!", "success")
        return redirect(url_for('login'))
    else:
        flash('Role is not defined!', 'danger')
        return redirect(url_for(('login')))


@app.route('/HomeWizard/<string:role>/<int:id>/logout', methods=['POST'])
def logout(role, id):
    if not role:
        return redirect(url_for('home'))  
    
    if id is None:
        return redirect(url_for('home'))  
    
    email = session.get(f"{role}_email")
    if email is None:
        return redirect(url_for('home'))  
    
    session_key = f"{role}_{id}"  

    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        session['sessions'].pop(session_key, None) 
        logging.debug(f"Session cleared for {role}: {session_key}")

    if role == 'admin':
        return redirect(url_for('admin_login'))
    elif role in ['user', 'professional']:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))

