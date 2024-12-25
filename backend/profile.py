from flask import flash, render_template, request, redirect, session, url_for

from backend.helper import format_dates
from .models import db, User_Info, Professional_Info, Admin_Info
from werkzeug.security import generate_password_hash
from flask import current_app as app
  



@app.route('/HomeWizard/<string:role>/<int:id>/profile')
def profile(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        if role == 'admin':
            admin = Admin_Info.query.filter_by(email=email).first()
            admin = format_dates(admin, ['created_at'])
            return render_template('profile.html', admin=admin, role=role, edit_mode=False)
        elif role == 'user':
            user = User_Info.query.filter_by(email=email).first()
            user = format_dates(user, ['dob', 'created_at'])
            return render_template('profile.html', user=user, role=role, edit_mode=False)
        elif role == 'professional':
            pro = Professional_Info.query.filter_by(email=email).first()
            pro = format_dates(pro, ['dob', 'created_at'])
            return render_template('profile.html', pro=pro, role=role, edit_mode=False)

    else:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))


@app.route('/HomeWizard/<string:role>/<int:id>/profile/edit/view')
def edit_profile_view(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        if role == 'admin':
            admin = Admin_Info.query.filter_by(email=email).first()
            return render_template('profile.html', admin=admin, role=role, edit_mode=True)
        elif role == 'user':
            user = User_Info.query.filter_by(email=email).first()
            return render_template('profile.html', user=user, role=role, edit_mode=True)
        elif role == 'professional':
            pro = Professional_Info.query.filter_by(email=email).first()
            return render_template('profile.html', pro=pro, role=role, edit_mode=True)
        
    else:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))


@app.route('/HomeWizard/profile')
def d_profile():
    flash("Unauthorized access.", "danger")
    return redirect(url_for('login'))



@app.route('/HomeWizard/<string:role>/<int:id>/profile/edit', methods=['POST'])
def edit_profile(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

    
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        if role == 'user':
            user = User_Info.query.filter_by(email=email).first()
            user.full_name = full_name
            user.phone_number = phone
            user.address = address
            user.pincode = pincode
            if password:
                user.pwd = generate_password_hash(password)
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile', id=user.id, role=role, user=user))

        elif role == 'professional':
            pro = Professional_Info.query.filter_by(email=email).first()
            pro.full_name = full_name
            pro.phone_number = phone
            pro.address = address
            pro.pincode = pincode
            if password:
                pro.pwd = generate_password_hash(password)
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile', id=pro.id, role=role, pro=pro))
        else:
            flash('Role not defined', 'danger')

    else:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))
