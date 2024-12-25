from datetime import datetime
from flask import flash, redirect, session, url_for
from sqlalchemy import or_
from .models import ServiceStatus, db, Professional_Info, ServiceRequest
from flask import current_app as app


@app.route('/HomeWizard/<string:role>/<int:id>/accept-service-request/<int:request_id>', methods=['POST'])
def accept_service_request(role, id, request_id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        
        pro = Professional_Info.query.filter_by(email=email).first()

        
        ongoing_service = ServiceRequest.query.filter(
            ServiceRequest.professional_id == id,
            or_(
                ServiceRequest.service_status == ServiceStatus.ONGOING, 
                ServiceRequest.service_status == ServiceStatus.ASSIGNED 
            )
        ).first()

        if ongoing_service:
            flash('You already have an ongoing service. Complete it before accepting a new request.', 'danger')
            return redirect(url_for('dashboard', role=role, id=pro.id))

        
        service_request = ServiceRequest.query.get(request_id)

        if service_request and service_request.professional_id is None:
            
            service_request.professional_id = id
            service_request.service_status = ServiceStatus.ASSIGNED
            db.session.commit()
            flash('Request accepted successfully.', 'success')
        else:
            flash('Request has already been accepted by another professional.', 'danger')

        return redirect(url_for('dashboard', role=role, id=pro.id))
    else:
        return redirect(url_for('login'))


@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/start-service', methods=['POST'])
def start_service_p(role, id, service_id):
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
    


@app.route('/HomeWizard/<string:role>/<int:id>/service/<int:service_id>/end-service', methods=['POST'])
def end_service_p(role, id, service_id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):

        servicerequest = ServiceRequest.query.get(service_id)

        if servicerequest and servicerequest.service_status == ServiceStatus.ONGOING:
            servicerequest.service_status = ServiceStatus.COMPLETED
            servicerequest.date_of_completion = datetime.now()
            db.session.commit()
            flash('Your rating request goinge to customer! wait for rating!', 'success')
        else:
            flash('Unable to sent request for rating!', 'danger')
        return redirect(url_for('dashboard', role=role, id=id))