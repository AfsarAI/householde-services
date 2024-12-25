from datetime import datetime
import os
from flask import flash, render_template, request, redirect, send_from_directory, session, url_for
from sqlalchemy import String, case, cast, func, or_
from backend.helper import format_dates
from .models import ProfessionalStatus, ServiceStatus, db, User_Info, Professional_Info, Admin_Info, Service, ServiceRequest
from flask import current_app as app
        


@app.route('/HomeWizard/<string:role>/<int:id>/dashboard', methods=['GET', 'POST'])
def dashboard(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        
        user = User_Info.query.filter_by(email=email).first() if role == 'user' else None
        pro = Professional_Info.query.filter_by(email=email).first() if role == 'professional' else None
        admin = Admin_Info.query.filter_by(email=email).first() if role == 'admin' else None

        
        user = format_dates(user, ['created_at'])
        pro = format_dates(pro, ['created_at'])
        admin = format_dates(admin, ['created_at'])

        
        search_query = request.args.get('search', '').strip().lower()
        filter_by = request.args.get('filter_by', '')  

        if role == 'user':
            
            professionals = {prof.id: prof for prof in Professional_Info.query.all()}

            
            all_services = db.session.query(Service)

            
            requested_services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == user.id,
                ServiceRequest.service_status == ServiceStatus.REQUESTED
            )

            
            ongoing_services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == user.id,
                ServiceRequest.service_status.in_([ServiceStatus.ASSIGNED, ServiceStatus.ONGOING])
            )

            
            closed_services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == user.id,
                ServiceRequest.service_status.in_([ServiceStatus.COMPLETED, ServiceStatus.CLOSED])
            )

            if search_query:
                
                if filter_by == 'service_name':
                    all_services = Service.query.filter(Service.name.ilike(f"%{search_query}%"))
                    requested_services = requested_services.join(Service).filter(Service.name.ilike(f"%{search_query}%"))
                    ongoing_services = ongoing_services.join(Service).filter(Service.name.ilike(f"%{search_query}%"))
                    closed_services = closed_services.join(Service).filter(Service.name.ilike(f"%{search_query}%"))

                elif filter_by == 'status':
                    requested_services = requested_services.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )
                    ongoing_services = ongoing_services.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )
                    closed_services = closed_services.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )

                elif filter_by == 'date':
                    try:
                        
                        search_date = datetime.strptime(search_query, "%Y-%m-%d").date()
                        
                        
                        requested_services = requested_services.filter(func.date(ServiceRequest.date_of_request) == search_date)
                        ongoing_services = ongoing_services.filter(func.date(ServiceRequest.date_of_request) == search_date)
                        closed_services = closed_services.filter(
                            or_(
                                func.date(ServiceRequest.date_of_request) == search_date,
                                func.date(ServiceRequest.date_of_completion) == search_date
                            )
                        )
                    except ValueError:
                        
                        flash("Invalid date format. Please use YYYY-MM-DD.")
                    except Exception as e:
                        print("Query Error:", str(e))

                elif filter_by == 'location':
                    
                    all_services = all_services.join(Professional_Info).filter(
                        or_(
                            Professional_Info.address.ilike(f"%{search_query}%"),
                            Professional_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )
                    
                    
                    requested_services = requested_services.join(Service).join(Professional_Info).filter(
                        or_(
                            Professional_Info.address.ilike(f"%{search_query}%"),
                            Professional_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )
                    ongoing_services = ongoing_services.join(Service).join(Professional_Info).filter(
                        or_(
                            Professional_Info.address.ilike(f"%{search_query}%"),
                            Professional_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )
                    
                    closed_services = closed_services.filter(
                        ServiceRequest.professional_id.isnot(None)
                    ).join(Professional_Info).filter(
                        or_(
                            Professional_Info.address.ilike(f"%{search_query}%"),
                            Professional_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )

            
            all_services = all_services.all()
            requested_services = requested_services.all()
            ongoing_services = ongoing_services.all()
            closed_services = closed_services.all()

            all_services = format_dates(all_services, ['created_at'])
            services_with_professionals = []
            for service in all_services:
                
                professionals_for_service = Professional_Info.query.filter(
                    Professional_Info.service_id == service.id,
                    Professional_Info.status == ProfessionalStatus.APPROVED  
                ).all()

                
                professional_data = []
                total_ratings = 0  
                rated_professionals = 0  
                average_service_rating = 0  


                for professional in professionals_for_service:
                    
                    total_services = db.session.query(func.count(ServiceRequest.id)).filter(
                        ServiceRequest.professional_id == professional.id,
                        ServiceRequest.service_status.in_([
                            ServiceStatus.COMPLETED,  
                            ServiceStatus.CLOSED      
                        ])
                    ).scalar()
                    
                    
                    avg_rating = db.session.query(func.avg(ServiceRequest.rating)).filter(
                        ServiceRequest.professional_id == professional.id
                    ).scalar()

                    if avg_rating:
                        total_ratings += avg_rating
                        rated_professionals += 1
                    
                    avg_rating = round(avg_rating, 2) if avg_rating else "No Ratings Yet"
                    total_services = total_services if total_services else 0  
                    
                    
                    professional_data.append({
                        'id': professional.id,
                        'full_name': professional.full_name,
                        'pincode': professional.pincode,
                        'phone_number': professional.phone_number,
                        'average_rating': avg_rating,
                        'total_services': total_services
                    })

                    
                    average_service_rating = (total_ratings / rated_professionals) if rated_professionals > 0 else 0
                
                
                services_with_professionals.append({
                    'service': service,
                    'professionals': professional_data,
                    'professional_count': len(professional_data),
                    'average_service_rating': round(average_service_rating, 2)
                })

           
            services_with_professionals.sort(
                key=lambda x: (x['professional_count'], x['average_service_rating']),
                reverse=True  
            )

            
            closed_services = sorted(
                closed_services,
                key=lambda cs: (cs.rating is not None, -cs.rating if cs.rating else 0)
            )



            
            requested_services = format_dates(requested_services, ['date_of_request', 'date_of_completion'])
            ongoing_services = format_dates(ongoing_services, ['date_of_request', 'date_of_completion'])
            closed_services = format_dates(closed_services, ['date_of_request', 'date_of_completion'])


            
            return render_template(
                'user_dashboard.html',
                role=role,
                user=user,
                professionals=professionals,
                services=all_services,
                services_with_professionals=services_with_professionals,
                requested_services=requested_services,
                ongoing_services=ongoing_services,
                closed_services=closed_services,
                filter_by=filter_by,
                search_query=search_query
            )




        elif role == 'professional':

            service = Service.query.filter_by(id=pro.service_id).first()

            
            pending_requests = ServiceRequest.query.filter_by(
                service_id=pro.service_id,
                professional_id=None,
                service_status=ServiceStatus.REQUESTED  
            )

            
            ongoing_services = ServiceRequest.query.filter(
                ServiceRequest.service_id == pro.service_id,
                ServiceRequest.professional_id == id,
                ServiceRequest.service_status.in_([
                    ServiceStatus.ASSIGNED,
                    ServiceStatus.ONGOING
                ])
            )

            
            closed_services = ServiceRequest.query.filter(
                ServiceRequest.service_id == pro.service_id,
                ServiceRequest.professional_id == id,
                ServiceRequest.service_status.in_([
                    ServiceStatus.COMPLETED, 
                    ServiceStatus.CLOSED
                ])
            )


            if search_query:
                
                if filter_by == 'customer_name':
                    pending_requests = pending_requests.join(User_Info).filter(
                        User_Info.full_name.ilike(f"%{search_query}%")
                    )
                    ongoing_services = ongoing_services.join(User_Info).filter(
                        User_Info.full_name.ilike(f"%{search_query}%")
                    )
                    closed_services = closed_services.join(User_Info).filter(
                        User_Info.full_name.ilike(f"%{search_query}%")
                    )

                elif filter_by == 'status':
                    pending_requests = pending_requests.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )
                    ongoing_services = ongoing_services.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )
                    closed_services = closed_services.filter(
                        cast(ServiceRequest.service_status, String).ilike(f"%{search_query}%")
                    )


                elif filter_by == 'date':
                    try:
                        
                        search_date = datetime.strptime(search_query, "%Y-%m-%d").date()
                        
                        
                        pending_requests = pending_requests.filter(func.date(ServiceRequest.date_of_request) == search_date)
                        ongoing_services = ongoing_services.filter(func.date(ServiceRequest.date_of_request) == search_date)
                        closed_services = closed_services.filter(
                            or_(
                                func.date(ServiceRequest.date_of_request) == search_date,
                                func.date(ServiceRequest.date_of_completion) == search_date
                            )
                        )
                    except ValueError:
                        
                        flash("Invalid date format. Please use YYYY-MM-DD.")
                    except Exception as e:
                        print("Query Error:", str(e))

                elif filter_by == 'location':
                    
                    
                    pending_requests = pending_requests.join(Service).join(User_Info).filter(
                        or_(
                            User_Info.address.ilike(f"%{search_query}%"),
                            User_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )

                    
                    ongoing_services = ongoing_services.join(Service).join(User_Info).filter(
                        or_(
                            User_Info.address.ilike(f"%{search_query}%"),
                            User_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )

                    
                    closed_services = closed_services.join(Service).join(User_Info).filter(
                        or_(
                            User_Info.address.ilike(f"%{search_query}%"),
                            User_Info.pincode == int(search_query) if search_query.isdigit() else False
                        )
                    )


            
            pending_requests = pending_requests.all()
            ongoing_services = ongoing_services.all()
            closed_services = closed_services.all()
            
            closed_services = sorted(
                closed_services,
                key=lambda cs: (cs.rating is not None, cs.rating if cs.rating else 0),
                reverse=True
            )

            
            ongoing_services = format_dates(ongoing_services, ['date_of_request', 'date_of_completion'])
            closed_services = format_dates(closed_services, ['date_of_request', 'date_of_completion'])
            pending_requests = format_dates(pending_requests, ['date_of_request'])

            return render_template(
                'professional_dashboard.html',
                role=role,
                pro=pro,
                service=service,
                requests=pending_requests,
                ongoing_services=ongoing_services,
                closed_services=closed_services,
                search_query=search_query,
                filter_by=filter_by
            )

        elif role == 'admin':
            
            pending_professionals = (
                db.session.query(Professional_Info)
                .filter(Professional_Info.status == ProfessionalStatus.PENDING)  
            )


            
            all_service_requests = db.session.query(ServiceRequest)

            all_professionals = Professional_Info.query.all()

            
            professionals_dict = {professional.id: professional for professional in all_professionals}

            
            if search_query:
                
                pending_professionals = (
                    pending_professionals
                    .join(Service)  
                    .filter(
                        db.or_(
                            Professional_Info.full_name.ilike(f"%{search_query}%"),
                            Professional_Info.email.ilike(f"%{search_query}%"),
                            Professional_Info.address.ilike(f"%{search_query}%"),
                            Professional_Info.pincode == int(search_query) if search_query.isdigit() else None,
                            Service.name.ilike(f"%{search_query}%")  
                        )
                    )
                )

                
                all_service_requests = (
                    all_service_requests
                    .join(Service, Service.id == ServiceRequest.service_id)
                    .join(User_Info, User_Info.id == ServiceRequest.customer_id)
                    .outerjoin(Professional_Info, Professional_Info.id == ServiceRequest.professional_id)  
                    .filter(
                        db.or_(
                            Service.name.ilike(f"%{search_query}%"),
                            User_Info.full_name.ilike(f"%{search_query}%"),
                            User_Info.address.ilike(f"%{search_query}%"),
                            User_Info.pincode == int(search_query) if search_query.isdigit() else None,
                            cast(ServiceRequest.service_status, String).ilike(f"%{search_query.lower()}%"),
                            Professional_Info.full_name.ilike(f"%{search_query}%")  
                        )
                    )
                )



            
            if request.method == 'POST':
                professional_id = request.form.get('professional_id')
                action = request.form.get('action')

                if professional_id and action:
                    
                    professional = Professional_Info.query.get(professional_id)

                    if action == 'approve':
                        professional.status = ProfessionalStatus.APPROVED  
                        professional.created_at = datetime.now()
                        flash(f'Professional {professional.full_name} approved successfully.', 'success')
                    elif action == 'reject':
                        professional.status = ProfessionalStatus.REJECTED  
                        flash(f'Professional {professional.full_name} rejected.', 'danger')

                    db.session.commit()
                
                
                return redirect(url_for('dashboard', role=role, id=id))

            
            pending_professionals = pending_professionals.all()

            
            all_service_requests = all_service_requests.all()
            all_service_requests = sorted(
                all_service_requests,
                key=lambda cs: (cs.rating is not None, cs.rating if cs.rating else 0),
                reverse=True
            )

            
            pending_professionals = format_dates(pending_professionals, ['created_at'])
            all_service_requests = format_dates(all_service_requests, ['date_of_request', 'date_of_completion'])

            return render_template(
                'admin_dashboard.html',
                role = role,
                admin = admin,
                pending_professionals = pending_professionals,
                all_service_requests = all_service_requests,
                professionals_dict = professionals_dict,
                search_query = search_query
            )
        else:
            return redirect(url_for('admin_login'))

    else:
        return redirect(url_for('home'))




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        app.logger.info(f"Serving file: {file_path}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        app.logger.error(f"File not found: {file_path}")
        return "File not found", 404



@app.route('/HomeWizard/<string:role>/<int:id>/dashboard/users-professionals-list', methods=['GET', 'POST'])
def uplist(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        admin = Admin_Info.query.filter_by(email=email).first() if role == 'admin' else None
        
        admin = format_dates(admin, ['created_at'])

        
        approved_professionals = db.session.query(
            Professional_Info,
            Service.name.label('service_name'),  
            func.round(func.avg(ServiceRequest.rating), 2).label('average_rating'),
            func.count(
                case(
                    (ServiceRequest.service_status.in_([ServiceStatus.COMPLETED, ServiceStatus.CLOSED]), 1),  
                    else_=None
                )
            ).label('total_services')  
        ).outerjoin(
            ServiceRequest, ServiceRequest.professional_id == Professional_Info.id
        ).outerjoin(
            Service, Service.id == Professional_Info.service_id  
        ).filter(
            Professional_Info.status == ProfessionalStatus.APPROVED
        ).group_by(Professional_Info.id, Service.name).order_by(
            func.avg(ServiceRequest.rating).asc().nullsfirst()  
        )

        
        all_users = db.session.query(
            User_Info,
            func.count(ServiceRequest.id).label('total_services')
        ).outerjoin(
            ServiceRequest, ServiceRequest.customer_id == User_Info.id
        ).group_by(User_Info.id).order_by(
            func.count(ServiceRequest.id).desc()  
        )

        
        search_query = request.args.get('search', '').strip().lower()
        
        
        if search_query:
            approved_professionals = approved_professionals.filter(
                db.or_(
                    Professional_Info.full_name.ilike(f"%{search_query}%"),
                    Professional_Info.email.ilike(f"%{search_query}%"),
                    Professional_Info.phone_number.ilike(f"%{search_query}%"),
                    Professional_Info.address.ilike(f"%{search_query}%"),
                    Professional_Info.pincode == int(search_query) if search_query.isdigit() else None,
                    Service.name.ilike(f"%{search_query}%")
                )
            )

            all_users = all_users.filter(
                db.or_(
                    User_Info.full_name.ilike(f"%{search_query}%"),
                    User_Info.email.ilike(f"%{search_query}%"),
                    User_Info.address.ilike(f"%{search_query}%"),
                    User_Info.pincode == int(search_query) if search_query.isdigit() else None
                )
            )

        
        approved_professionals = approved_professionals.all()

        
        professionals_data = []
        for professional, service_name, avg_rating, total_services in approved_professionals:
            professional_data = {
                "professional": format_dates(professional, ['created_at']),
                "service_name": service_name if service_name else "No service assigned",
                "average_rating": round(avg_rating, 2) if avg_rating else "No Ratings Yet",
                "total_services": total_services if total_services else 0  
            }
            professionals_data.append(professional_data)


        all_users = all_users.all()

        
        users_data = []
        for user, total_services in all_users:
            user_data = {
                "user": format_dates(user, ['created_at']),
                "total_services": total_services if total_services > 0 else "No services availed"
            }
            users_data.append(user_data)

        
        if request.method == 'POST' and request.form.get('action') == 'block':
            professional_id = request.form.get('professional_id')
            professional_to_block = Professional_Info.query.get(professional_id)

            if professional_to_block:
                professional_to_block.status = ProfessionalStatus.BLOCKED
                professional_to_block.created_at = datetime.now()
                db.session.commit()
                flash(f'Professional {professional_to_block.full_name} has been marked as blocked.', 'danger')
            else:
                flash('Professional not found!', 'danger')

            return redirect(url_for('uplist', role=role, id=id))

        
        return render_template(
            'admin_uplist.html',
            role=role,
            admin=admin,
            professionals=professionals_data,  
            users=users_data,  
        )

@app.route('/HomeWizard/<string:role>/<int:id>/dashboard/blocked-and-rejected-professionals-list', methods=['GET', 'POST'])
def trash(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        admin = Admin_Info.query.filter_by(email=email).first() if role == 'admin' else None
        
        admin = format_dates(admin, ['created_at'])

        
        blocked_professionals = db.session.query(
            Professional_Info,
            Service.name.label('service_name'),  
            func.avg(ServiceRequest.rating).label('average_rating'),
            func.count(ServiceRequest.id).label('total_services')
        ).outerjoin(
            ServiceRequest, ServiceRequest.professional_id == Professional_Info.id
        ).outerjoin(
            Service, Service.id == Professional_Info.service_id  
        ).filter(
            Professional_Info.status == ProfessionalStatus.BLOCKED
        ).group_by(Professional_Info.id, Service.name).order_by(
            func.avg(ServiceRequest.rating).asc().nullsfirst()  
        )

        
        blocked_professionals = blocked_professionals.all()

        
        blocked_professionals_data = []
        for professional, service_name, avg_rating, total_services in blocked_professionals:
            professional_data = {
                "professional": format_dates(professional, ['created_at']),
                "service_name": service_name if service_name else "No service assigned",
                "average_rating": round(avg_rating, 2) if avg_rating else "N/A",
                "total_services": total_services,
                "professional_id": professional.id
            }
            blocked_professionals_data.append(professional_data)

        
        rejected_professionals = db.session.query(
            Professional_Info,
            Service.name.label('service_name'),  
            func.avg(ServiceRequest.rating).label('average_rating'),
            func.count(ServiceRequest.id).label('total_services')
        ).outerjoin(
            ServiceRequest, ServiceRequest.professional_id == Professional_Info.id
        ).outerjoin(
            Service, Service.id == Professional_Info.service_id  
        ).filter(
            Professional_Info.status == ProfessionalStatus.REJECTED
        ).group_by(Professional_Info.id, Service.name).order_by(
            func.avg(ServiceRequest.rating).asc().nullsfirst()  
        )

        
        rejected_professionals = rejected_professionals.all()

        
        rejected_professionals_data = []
        for professional, service_name, avg_rating, total_services in rejected_professionals:
            professional_data = {
                "professional": format_dates(professional, ['created_at']),
                "service_name": service_name if service_name else "No service assigned",
                "average_rating": round(avg_rating, 2) if avg_rating else "N/A",
                "total_services": total_services,
                "professional_id": professional.id
            }
            rejected_professionals_data.append(professional_data)



        
        if request.method == 'POST' and request.form.get('action') == 'delete':
            professional_id = request.form.get('professional_id')
            professional_to_delete = Professional_Info.query.get(professional_id)

            if professional_to_delete:
                db.session.delete(professional_to_delete)
                db.session.commit()
                flash('Professional permanently deleted!', 'success')
            else:
                flash('Professional not found!', 'danger')

            return redirect(url_for('trash', role=role, id=id))

        
        if request.method == 'POST' and request.form.get('action') == 'unblock_approve':
            professional_id = request.form.get('professional_id')
            professional_to_unblock = Professional_Info.query.get(professional_id)

            if professional_to_unblock:
                professional_to_unblock.status = ProfessionalStatus.APPROVED  
                db.session.commit()
                flash('Professional unblocked successfully!', 'success')
            else:
                flash('Professional not found!', 'danger')

            return redirect(url_for('trash', role=role, id=id))

        
        if request.method == 'POST' and request.form.get('action') == 'delete_all_b':
            professionals_to_delete = Professional_Info.query.filter_by(status=ProfessionalStatus.BLOCKED).all()

            for professional in professionals_to_delete:
                db.session.delete(professional)
            db.session.commit()
            flash('All blocked professionals deleted!', 'success')

            return redirect(url_for('trash', role=role, id=id))
        
        
        if request.method == 'POST' and request.form.get('action') == 'delete_all_r':
            professionals_to_delete = Professional_Info.query.filter_by(status=ProfessionalStatus.REJECTED).all()

            for professional in professionals_to_delete:
                db.session.delete(professional)
            db.session.commit()
            flash('All rejected professionals deleted!', 'success')

            return redirect(url_for('trash', role=role, id=id))

        
        if request.method == 'POST' and request.form.get('action') == 'unblock_all':
            professionals_to_unblock = Professional_Info.query.filter_by(status=ProfessionalStatus.BLOCKED).all()

            for professional in professionals_to_unblock:
                professional.status = ProfessionalStatus.APPROVED  
            db.session.commit()
            flash('All blocked professionals unblocked!', 'success')

            
        if request.method == 'POST' and request.form.get('action') == 'approve_all':
            professionals_to_unblock = Professional_Info.query.filter_by(status=ProfessionalStatus.REJECTED).all()

            for professional in professionals_to_unblock:
                professional.status = ProfessionalStatus.APPROVED  
            db.session.commit()
            flash('All rejected professionals approved!', 'success')

            return redirect(url_for('trash', role=role, id=id))

        return render_template('admin_trash.html',
                               role=role,
                               admin=admin,
                               blocked_professionals=blocked_professionals_data,
                               rejected_professionals=rejected_professionals_data)
