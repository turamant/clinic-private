from flask import render_template, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from clinic_app import app, Appointment, Doctor, db, Patient, Specialty, Comment, Clinic, Address


@app.route('/')
def index():
    """Все приемы, все врачи
    params:
        specialty - специальность доктора
        records - все приемы
        client_count - количество пациентов по докторам
    """
    specialty = db.session.query(Specialty).all()
    print(".--..spec", specialty)

    records = db.session.query(Appointment)\
        .join(Doctor)\
        .filter(Appointment.doctor_id == Doctor.id)\
        .order_by(Appointment.data, Doctor.family)\
        .all()

    client_count = db.session.query(Doctor, Specialty, func.count(Patient.id)).select_from(
        Appointment) \
        .join(Doctor).filter(Doctor.id == Appointment.doctor_id) \
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id) \
        .join(Patient).filter(Patient.id == Appointment.patient_id) \
        .group_by(Doctor.family).having(func.count(Patient.id)).all()

    return render_template('index.html',
                           records=records,
                           specialty=specialty,
                           client_count=client_count)



@app.route('/doctors/')
def index_doctors():
    doctors = db.session.query(Doctor, Specialty)\
        .filter(Doctor.specialty_id == Specialty.id)\
        .all()
    print("...doctors..=", doctors)
    return render_template('doctors.html', doctors=doctors)


@app.route('/patients/')
def index_patients():
    patients = db.session.query(Patient).all()
    return render_template('patients.html', patients=patients)


@app.route('/doctors/<title>/')
def doctors_spec(title):
    print("..title..=", title)
    query = db.session.query(Patient, Doctor, Specialty, Clinic, Appointment)\
        .select_from(Appointment)\
        .join(Patient).filter(Appointment.patient_id == Patient.id)\
        .join(Doctor).filter(Appointment.doctor_id == Doctor.id)\
        .join(Clinic).filter(Doctor.clinica_id == Clinic.id)\
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id)\
        .filter(Specialty.title == title)
    patients = query.all()

    print("...QQQQpatients..=", patients)
    return render_template('patients_specialty.html', patients=patients, title=title)



@app.route('/doctors/<int:id>/')
def doctor_detail(id):
    """Страница доктора"""
    """appointments - все приемы"""
    """comments - все комменты"""
    doctor = db.session.query(Doctor).filter(Doctor.id == id).first()
    appointments = doctor.appointment
    comments = doctor.comments
    return render_template('doctor_detail.html',
                           doctor=doctor,
                           appointments=appointments,
                           comments=comments)


@app.route('/secret/')
def secret_test():
    return 'Only authenticated users are allowed'


@app.route('/patients/<int:id>/')
def patient_detail(id):
    """Страница пациента"""
    """appointments - все приемы"""
    """comments - все комменты"""
    patient = db.session.query(Patient).filter(Patient.id == id).first()
    appointments = patient.appointment
    comments = patient.comments
    return render_template('patient_detail.html',
                           patient=patient,
                           appointments=appointments,
                           comments=comments)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/comments/')
def get_all_comments():
    """Все комменты в кучу"""
    comments = db.session.query(Comment).all()
    return f'Все комменты:{comments}'


@app.route('/comments/<int:id>/')
def get_doctor_comments(id):
    """Комменты по конкретному доктору (публично)"""
    comments = db.session.query(Comment).filter(Comment.doctor_id == id).all()
    if comments:
        comment = comments[0]
        doc = comment.doctor
        print("doc....=", doc)
    else:
        doc = "PUSTO"
    print("...comments..", comments)
    return f'Доктор: {doc} комменарии для него: {comments}'


@app.route('/count_patient/')
def count_patient():
    """
    Подсчет пациентов по докторам(визитам)
    """
    client_count = db.session.query(Doctor.family, Doctor.name, Specialty.title, func.count(Patient.id)).select_from(Appointment) \
        .join(Doctor).filter(Doctor.id == Appointment.doctor_id)\
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id)\
        .join(Patient).filter(Patient.id == Appointment.patient_id)\
        .group_by(Doctor.family).having(func.count(Patient.id)).all()

    print(".......client_count....", client_count)
    return render_template('count_patient.html')


@app.route('/profile/')
@login_required
def profile():
    image_file = url_for('static', filename='images/' + current_user.image)
    return render_template('profile.html', username=current_user.username, image_file=image_file)


@app.route('/clinics/')
def clinics():
    clinics = db.session.query(Clinic.title).all()
    return f'клиники: {clinics}'


@app.route('/clinics/<title>')
def clinic_patient(title):
    pass


@app.route('/pati/<int:id>/')
def address_patient(id):
    '''
    select addresses.street, patients.family from addresses, patients
    where addresses.id = patients.address_id and addresses.id = 6;
    '''
    address = db.session.query(Address, Patient).\
        filter(Address.id == Patient.address_id).\
        filter(Address.id == id).all()
    print("id....=", id)
    print("address....=", address)
    #return f'{address}'
    return render_template('address_patient.html', address=address)

