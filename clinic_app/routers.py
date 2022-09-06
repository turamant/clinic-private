from flask import render_template, url_for
from flask_login import login_required, current_user

from clinic_app import app, Appointment, Doctor, db, Patient, Specialty, Comment


@app.route('/')
def index():
    specialty = db.session.query(Doctor.family, Specialty.title).join(Specialty).filter(Doctor.specialty_id == Specialty.id).all()

    query = db.session.query(Appointment).join(Doctor)\
        .filter(Appointment.doctor_id == Doctor.id)\
        .order_by(Appointment.data, Doctor.family)

    records = query.all()

    return render_template('index.html', records=records, specialty=specialty)


@app.route('/profile/')
@login_required
def profile():
    image_file = url_for('static', filename='images/' + current_user.image)
    return render_template('profile.html', username=current_user.username, image_file=image_file)


@app.route('/appoints/')
def index_appoints():
    specialty = db.session.query(Doctor.family, Specialty.title).join(Specialty).filter(
        Doctor.specialty_id == Specialty.id).all()
    for spec in specialty:
        print("...speciality..= ", spec.family, spec.title)

    query = db.session.query(Appointment.id, Appointment.data, Specialty.title, Doctor.family, Patient.family).select_from(Appointment)\
        .join(Doctor) \
        .filter(Appointment.doctor_id == Doctor.id)\
        .join(Specialty)\
        .filter(Doctor.specialty_id == Specialty.id)\
        .outerjoin(Patient)\
        .order_by(Doctor.family, Appointment.data)

    records = query.all()
    print(query)

    for appointment in records:
        print("....appointment=..", appointment)
        print("....records=..", records)
    return render_template('index_appoints.html', records=records, specialty=specialty)


@app.route('/doctors/')
def index_doctors():
    doctors = db.session.query(Doctor.id, Doctor.family, Specialty.title).filter(Doctor.specialty_id==Specialty.id).all()
    print("...doctors..=", doctors)
    return render_template('doctors.html', doctors=doctors)


@app.route('/doctors/<title>/')
def get_doctors(title):
    '''
    select patients.family, doctors.family, specialties.title from patients
    JOIN appointments ON appointments.patient_id=patients.id
    JOIN doctors ON appointments.doctor_id=doctors.id
    JOIN specialties ON doctors.specialty_id=specialties.id
    where title='Окулист';

    '''
    query = db.session.query(Patient, Doctor, Specialty, Appointment.data, Appointment.time)\
        .select_from(Patient)\
        .join(Appointment).filter(Appointment.patient_id == Patient.id)\
        .join(Doctor).filter(Appointment.doctor_id == Doctor.id)\
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id)\
        .filter(Specialty.title == title)
    patients = query.all()

    return render_template('patients_specialty.html', patients=patients, title=title)


@app.route('/<family>/')
def doctor_detail(family):
    '''  records = db.session.query(Appointment, Doctor, Patient)\
        .filter(Appointment.doctor_id == Doctor.id)\
        .filter(Appointment.patient_id == Patient.id)\
        .filter(Doctor.id == id).order_by(Appointment.data_appointment).all()
    '''
    print("...family=..", family)
    doctor = db.session.query(Doctor).filter(Doctor.family == family).first()
    appointments = doctor.appointment

    print("...patient...=", doctor)
    print("....appoint...=", appointments)
    return render_template('doctor_detail.html', doctor=doctor, appointments=appointments)


@app.route('/secret/')
def secret_test():
    return 'Only authenticated users are allowed'



@app.route('/patients/<family>/')
def patient_detail(family):
    '''
    select doctors.family, doctors_patients.data_appointment from doctors_patients, doctors
     where doctors.id = doctors_patients.doctor_id and doctors.id=2;

     records = db.session.query(Appointment, Doctor, Patient)\
        .filter(Appointment.doctor_id == Doctor.id)\
        .filter(Appointment.patient_id == Patient.id)\
        .filter(Doctor.id == id).order_by(Appointment.data_appointment).all()
    '''
    #doctor = db.session.query(Doctor).get_or_404(id)
    print("family.......=", family)
    patient = db.session.query(Patient).filter(Patient.family == family).first()
    appointments = patient.appointment
    comments = list()
    for app in appointments:
        comments.append(app.comment)

    print("...patient...=", patient)
    print("....appoint...=", appointments)
    return render_template('patient_detail.html', patient=patient,
                           appointments=appointments, comments=comments)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/comments/')
def get_comments():
    appoint = db.session.query(Appointment).first()
    comments = appoint.comment

    print("+++ appoint++", appoint)
    print("...comments..", comments)
    return f'comments{comments}'
