from flask import render_template, url_for
from flask_login import login_required, current_user

from clinic_app import app, Appointment, Doctor, db, Patient, Specialty


@app.route('/')
def index():
    ''' SELECT   doctors_patients.data_appointment, doctors.family, patients.family
        FROM doctors_patients INNER JOIN doctors ON doctors.id = doctors_patients.doctor_id
            LEFT JOIN patients ON patients.id = doctors_patients.patient_id

    appointments = db.session.query(Appointment.data_appointment, Doctor.family, Patient.family)\
        .select_from(Appointment)\
        .join(Doctor, Appointment.doctor_id == Doctor.id)\
        .join(Patient, Appointment.patient_id == Patient.id)\
        .filter(Appointment.patient_id == 1).all()
    print("..........appointmets.......=", appointments)
    '''
    specialty = db.session.query(Doctor.family, Specialty.title).join(Specialty).filter(Doctor.specialty_id == Specialty.id).all()

    query = db.session.query(Appointment).join(Doctor)\
        .filter(Appointment.doctor_id == Doctor.id)\
        .order_by(Doctor.family, Appointment.data_appointment)

    records = query.all()
    #print(query)

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

    query = db.session.query(Appointment.id, Appointment.data_appointment, Specialty.title, Doctor.family, Patient.family).select_from(Appointment)\
        .join(Doctor) \
        .filter(Appointment.doctor_id == Doctor.id)\
        .join(Specialty)\
        .filter(Doctor.specialty_id == Specialty.id)\
        .outerjoin(Patient)\
        .order_by(Doctor.family, Appointment.data_appointment)

    records = query.all()
    print(query)

    for appointment in records:
        print("....appointment=..", appointment)
        print("....records=..", records)
    return render_template('index_appoints.html', records=records)


@app.route('/doctors/')
def index_doctors():
    doctors = db.session.query(Doctor).all()
    return render_template('doctors.html', doctors=doctors)


@app.route('/secret/')
def secret_test():
    return 'Only authenticated users are allowed'

