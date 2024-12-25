import random
from flask import current_app as app, render_template, session
import matplotlib
from sqlalchemy import and_, case, or_
from backend.helper import generate_horizontal_bar_chart, generate_pie_chart, generate_vertical_bar_chart
matplotlib.use('Agg')  
from backend.models import Admin_Info, Professional_Info, ProfessionalStatus, Service, ServiceRequest, ServiceStatus, User_Info, db


@app.route('/HomeWizard/<string:role>/<int:id>/summary-data')
def summary(role, id):
    session_key = f"{role}_{id}"
    sessions = session.get('sessions', {})  
    if sessions.get(session_key):
        email = sessions[session_key]['email']

        
        colormaps = ['viridis', 'plasma', 'cool', 'autumn', 'winter']
        
        cmap1 = random.choice(colormaps)
        cmap2 = random.choice(colormaps)
        
        if role == 'admin':
            admin = Admin_Info.query.filter_by(email=email).first()
            if not admin:
                return "Admin not found", 404

            
            total_customers = User_Info.query.count()
            total_professionals = Professional_Info.query.filter_by(status=ProfessionalStatus.APPROVED).count()
            total_services = Service.query.count()


            
            vertical_bar_chart_data = generate_vertical_bar_chart(
                {'Customers': total_customers, 'Approved Professionals': total_professionals, 'Services': total_services},
                "Total Registration",
                xlabel="Entity Type",
                cmap=cmap1
            )

            
            status_counts = (
                db.session.query(
                    db.case(
                        (ServiceRequest.service_status == ServiceStatus.REQUESTED, 'Requested'),
                        (ServiceRequest.service_status.in_([ServiceStatus.ASSIGNED, ServiceStatus.ONGOING]), 'Ongoing'),
                        (ServiceRequest.service_status.in_([ServiceStatus.COMPLETED, ServiceStatus.CLOSED]), 'Closed'),
                        else_='Other'
                    ).label('status_group'),
                    db.func.count(ServiceRequest.id)
                )
                .group_by('status_group')
                .all()
            )

            print(status_counts)

            
            status_data = {status: count for status, count in status_counts}

            
            pie_chart_data = generate_pie_chart(status_data, "All Service Request Status Distribution!")


            
            ratings_data = (
                db.session.query(ServiceRequest.rating, db.func.count(ServiceRequest.id))
                .filter(ServiceRequest.service_status.in_([ServiceStatus.COMPLETED, ServiceStatus.CLOSED]))  
                .group_by(ServiceRequest.rating)
                .all()
            )
            data = {rating or 0: count for rating, count in ratings_data}

            
            full_data = {i: data.get(i, 0) for i in range(6)}

            
            labels_with_stars = {i: f"{i} {'★' * i}" if i > 0 else f"{i} (No Stars)" for i in range(6)}

            
            data_with_stars = {labels_with_stars[key]: value for key, value in full_data.items()}

            
            rating_horizontal_bar_chart = generate_horizontal_bar_chart(
                data_with_stars,  
                "Ratings Overview (Closed Services)",
                ylabel="Ratings",
                cmap=cmap2
            )


            return render_template(
                'summary.html',
                admin=admin,
                role=role,
                total_customers=total_customers,
                total_professionals=total_professionals,
                total_services=total_services,
                pie_chart_data=pie_chart_data,
                vertical_bar_chart_data=vertical_bar_chart_data,
                rating_horizontal_bar_chart=rating_horizontal_bar_chart
            )

        elif role == 'user':
            user = User_Info.query.filter_by(email=email).first()
            if not user:
                return "User not found", 404

            
            total_services = ServiceRequest.query.filter_by(customer_id=id).count()
            requested_service = ServiceRequest.query.filter_by(customer_id=id, service_status=ServiceStatus.REQUESTED).count()
            ongoing_services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == id,
                ServiceRequest.service_status.in_([ServiceStatus.ASSIGNED, ServiceStatus.ONGOING])
            ).count()
            completed_services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == id,
                ServiceRequest.service_status.in_([ServiceStatus.COMPLETED, ServiceStatus.CLOSED])
            ).count()

            
            request_data = {
                "Completed": completed_services,
                "Ongoing": ongoing_services,
                "Pending": requested_service
            }

            bar_chart_data = generate_vertical_bar_chart(
                request_data,
                "Your Service Request Status",
                xlabel="Service Status",
                cmap=cmap1
            )

            return render_template(
                'summary.html',
                user=user,
                role=role,
                total_requests=total_services,
                bar_chart_data=bar_chart_data
            )

        elif role == 'professional':
            pro = Professional_Info.query.filter_by(email=email).first()
            if not pro:
                return "Professional not found", 404

            
            pending_requests = ServiceRequest.query.filter(
                and_(
                    ServiceRequest.service_id == pro.service_id,
                    ServiceRequest.professional_id == None,  
                    ServiceRequest.service_status == ServiceStatus.REQUESTED
                )
            ).count()

            
            ongoing_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id == id,
                or_(
                    ServiceRequest.service_status == ServiceStatus.ASSIGNED,
                    ServiceRequest.service_status == ServiceStatus.ONGOING
                )
            ).count()

            
            completed_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id == id,
                or_(
                    ServiceRequest.service_status == ServiceStatus.COMPLETED,
                    ServiceRequest.service_status == ServiceStatus.CLOSED
                )
            ).count()

            request_data = {
                "Pending": pending_requests,
                "Ongoing": ongoing_services,
                "Completed": completed_services,
            }

            
            for key in request_data:
                request_data[key] = request_data[key] or 0

            vertical_bar_chart_data = generate_vertical_bar_chart(
                request_data,
                "Your Service Status Overview",
                xlabel="Service Status",
                cmap=cmap1
            )

            
            ratings_data = (
                db.session.query(ServiceRequest.rating, db.func.count(ServiceRequest.id))
                .filter(ServiceRequest.service_status == ServiceStatus.CLOSED, ServiceRequest.professional_id == id)
                .group_by(ServiceRequest.rating)
                .all()
            )
            data = {rating or 0: count for rating, count in ratings_data}

            
            full_data = {i: data.get(i, 0) for i in range(6)}

            
            labels_with_stars = {i: f"{i} {'★' * i}" if i > 0 else f"{i} (No Stars)" for i in range(6)}

            
            data_with_stars = {labels_with_stars[key]: value for key, value in full_data.items()}

            rating_horizontal_bar_chart_data = generate_horizontal_bar_chart(
                data_with_stars,
                "Your Service Ratings Overview (Closed Services)",
                ylabel="Ratings",
                cmap=cmap2
            )


            return render_template(
                'summary.html',
                pro=pro,
                role=role,
                vertical_bar_chart_data=vertical_bar_chart_data,
                rating_horizontal_bar_chart_data=rating_horizontal_bar_chart_data
            )
    else:
        return "Session not found", 403
