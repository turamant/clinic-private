from flask import render_template

from clinic_app import app, Appointment, Doctor, db


@app.route('/')
def index():
    appointments = db.session.query(Appointment.data_appointment, Doctor.family).select_from(Appointment)\
        .join(Doctor).filter(Appointment.doctor_id == Doctor.id).all()
    print("...appointments...=", appointments)
    return render_template('index.html', appointments=appointments)


@app.route('/doctors')
def index_doctors():
    doctors = db.session.query(Doctor).all()
    return render_template('doctors.html', doctors=doctors)