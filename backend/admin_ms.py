from datetime import datetime
from flask import flash, render_template, request, redirect, session, url_for
from sqlalchemy import or_
from .models import db, Admin_Info, Service
from flask import current_app as app
from PIL import Image
from werkzeug.utils import secure_filename
import os
        


@app.route('/HomeWizard/admin/<int:id>/manage-services')
def services(id):
    session_key = f"admin_{id}"
    sessions = session.get('sessions', {})
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        admin = Admin_Info.query.filter_by(email=email).first()
        
        all_services = db.session.query(Service)

        
        search_query = request.args.get('search', '').strip().lower()

        if search_query:
            
            try:
                search_price = float(search_query)
            except ValueError:
                search_price = None

            all_services = all_services.filter(
                or_(
                    Service.name.ilike(f"%{search_query}%"),  
                    Service.base_price == search_price if search_price is not None else False  
                )
            )

            all_services = all_services.all()


        return render_template('manage_services.html', 
                               role='admin', 
                               services=all_services, 
                               id=admin.id)
    else:
        return redirect(url_for('admin_login'))




def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  
        return True
    except Exception as e:
        return False


@app.route('/HomeWizard/admin/<int:id>/manage-services/add-service', methods=['POST'])
def add_service(id):
    session_key = f"admin_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        admin = Admin_Info.query.filter_by(email=email).first()

        
        name = request.form['name']
        description = request.form['description']
        base_price = request.form['base_price']
        time_required = request.form['time_required']
        
        
        image = request.files['image_filename']
        image_filename = None  
        
        if image and image.filename != '':  
            image_filename = secure_filename(image.filename)  
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(save_path)  

            if is_valid_image(save_path):  
                
                pass
            else:
                
                os.remove(save_path)
                flash('Invalid image format. Only JPG, JPEG, PNG, and GIF formats are allowed.', 'danger')
                return redirect(url_for('services', id=admin.id))  
        
        
        new_service = Service(
            name=name,
            description=description,
            base_price=float(base_price),
            time_required=time_required,
            image_filename=image_filename,  
            created_at=datetime.now()
        )

        
        try:
            db.session.add(new_service)
            db.session.commit()
            flash('Service added successfully!', 'success')  
        except:
            db.session.rollback()  
            flash('Error adding the service.', 'error')  
        
        return redirect(url_for('services', id=admin.id))  
    
    else:
        return redirect(url_for('admin_login'))

@app.route('/HomeWizard/admin/<int:id>/manage-services/edit-service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(id, service_id):
    session_key = f"admin_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        admin = Admin_Info.query.filter_by(email=email).first()
        
        service = Service.query.get(service_id)
        
        if not service:
            flash("Service not found!", "error")
            return redirect(url_for('services'))
        
        if request.method == 'POST':
            
            service.name = request.form['name']
            service.description = request.form['description']
            service.base_price = request.form['base_price']
            service.time_required = request.form['time_required']
            
            
            if 'image_filename' in request.files:
                image_file = request.files['image_filename']
                if image_file.filename != '':
                    
                    image_filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                    service.image_filename = image_filename

            
            try:
                db.session.commit()
                flash("Service updated successfully.", "success")
            except:
                db.session.rollback()
                flash("Error updating service.", "error")
            
            return redirect(url_for('services', id=admin.id))

        
        return render_template('edit_service.html', service=service)
    
    else:
        return redirect(url_for('admin_login'))

@app.route('/HomeWizard/admin/<int:id>/manage-services/delete-service/<int:service_id>', methods=['POST'])
def delete_service(id, service_id):
    session_key = f"admin_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']
        
        admin = Admin_Info.query.filter_by(email=email).first()

        
        service = Service.query.get(service_id)
        
        if not service:
            flash("Service not found!", "error")
            return redirect(url_for('services', id=admin.id))  
        
        
        try:
            db.session.delete(service)
            db.session.commit()
            flash("Service deleted successfully.", "success")
        except:
            db.session.rollback()
            flash("Error deleting service.", "error")
        
        return redirect(url_for('services', id=admin.id))
    
    else:
        return redirect(url_for('admin_login'))