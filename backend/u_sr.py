from flask import flash, request, redirect, session, url_for
from .models import ProfessionalStatus, ServiceStatus, db, User_Info, Professional_Info, ServiceRequest
from flask import current_app as app
from datetime import datetime      


@app.route('/HomeWizard/<string:role>/<int:id>/service-request', methods=['POST'])
def service_request(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']
        
        
        service_id = request.form.get('service_id')
        
        
        user = User_Info.query.filter_by(email=email).first()
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('login'))
        
        customer_id = user.id

        
        professionals_for_service = Professional_Info.query.filter_by(service_id=service_id, status=ProfessionalStatus.APPROVED).all()
        if not professionals_for_service:
            flash("No professionals available for the requested service. Please try again later.", "danger")
            return redirect(url_for('dashboard', role=role, id=user.id))
        
        existing_sr = ServiceRequest.query.filter(
            ServiceRequest.service_id == service_id,
            ServiceRequest.customer_id == customer_id,
            ServiceRequest.service_status.in_([ServiceStatus.REQUESTED, ServiceStatus.ONGOING, ServiceStatus.ASSIGNED])  
        ).first()

        if existing_sr:
            flash('You already have a pending or ongoing service request for this service.', 'danger')
            return redirect(url_for('dashboard', role=role, id=user.id))

        
        
        new_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer_id,  
            professional_id=None,
            date_of_request=datetime.now(),
            date_of_completion=None,
            service_status=ServiceStatus.REQUESTED,
            review=None,
            rating=None
        )

        
        db.session.add(new_request)

        try:
            
            db.session.commit()
            flash('Service request has been created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error creating service request: {}'.format(e), 'error')

        return redirect(url_for('dashboard', role=role, id=user.id))  
    else:
        return redirect(url_for('login'))  

@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/cancel-service-request', methods=['POST'])
def cancel_service_request(role, id, service_id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):

        servicerequest = ServiceRequest.query.get(service_id)
        if servicerequest and servicerequest.service_status == ServiceStatus.REQUESTED:
            db.session.delete(servicerequest)
            db.session.commit()
            flash('Service request has been canceled.', 'danger')
        else:
            flash('Unable to cancel the service request.')
        return redirect(url_for('dashboard', role=role, id=id))
    else:
        return redirect(url_for('login'))

@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/edit-service-request', methods=['POST'])
def edit_service_request(role, id, service_id):
    
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if not sessions.get(session_key):
        return "Unauthorized access", 403

    
    service_request = ServiceRequest.query.get(service_id)
    if not service_request:
        return "Service Request not found", 404

    
    date_option = request.form.get('date_option')
    custom_date = request.form.get('custom_date')

    
    if date_option == "default":
        service_request.date_of_request = datetime.now()
    elif date_option == "custom" and custom_date:
        try:
            service_request.date_of_request = datetime.fromisoformat(custom_date)
        except ValueError:
            return "Invalid date format", 400

    
    db.session.commit()
    return redirect(url_for('dashboard', role=role, id=id))



@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/submit-review', methods=['POST'])
def submit_service_review(role, id, service_id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        
        review_text = request.form.get('review')
        rating = request.form.get('rating')

        servicerequest = ServiceRequest.query.get(service_id)

        if servicerequest and servicerequest.service_status in [ServiceStatus.ONGOING, ServiceStatus.COMPLETED]:
            servicerequest.service_status = ServiceStatus.CLOSED
            servicerequest.review = review_text
            servicerequest.rating = rating
            servicerequest.date_of_completion = datetime.now()
            db.session.commit()
            flash('Thank you for your feedback. The service has been closed.', 'success')
        else:
            flash('Unable to submit the review for this service.', 'danger')
        return redirect(url_for('dashboard', role=role, id=id))
    

@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/service-start', methods=['POST'])
def service_start_u(role, id, service_id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):

        servicerequest = ServiceRequest.query.get(service_id)

        if servicerequest and servicerequest.service_status == ServiceStatus.ASSIGNED:
            servicerequest.service_status = ServiceStatus.ONGOING
            db.session.commit()
            flash('Your service start now!', 'success')
        else:
            flash('Unable to work!', 'danger')
        return redirect(url_for('dashboard', role=role, id=id))