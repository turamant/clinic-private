from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from sqlalchemy import func

from clinic_app import app, Appointment, Doctor, db, Patient, Specialty, Comment, Clinic, Cabinet
from clinic_app.forms import ClinicForm


@app.route('/')
def index():
    """
    Все приемы, все специальности, количество пациентов по докторам
    params:
        specialty - все специальности докторов
        appointments - все приемы
        client_count - количество пациентов по докторам
    """
    specialty = db.session.query(Specialty).all()
    appointments = db.session.query(Appointment).all()

    client_count = db.session.query(Doctor, Specialty, func.count(Patient.id)).select_from(
        Appointment) \
        .join(Doctor).filter(Doctor.id == Appointment.doctor_id) \
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id) \
        .join(Patient).filter(Patient.id == Appointment.patient_id) \
        .group_by(Doctor.family).having(func.count(Patient.id)).all()
    return render_template('index.html',
                           appointments=appointments,
                           specialty=specialty,
                           client_count=client_count)


@app.route('/doctors/')
def index_doctors():
    """
    Все доктора
    params:
           doctors - все доктора
    """
    doctors = db.session.query(Doctor).all()
    return render_template('doctors.html', doctors=doctors)


@app.route('/doctors/<int:id>/')
def doctor_detail(id):
    """
    Страница доктора
    params:
            appointments - все приемы конкретного доктора
            comments - все комменты для доктора от пациентов
    """
    doctor = db.session.query(Doctor).filter(Doctor.id == id).first()
    appointments = doctor.appointment
    comments = doctor.comments
    return render_template('doctor_detail.html',
                           doctor=doctor,
                           appointments=appointments,
                           comments=comments)


@app.route('/patients/')
def index_patients():
    """
    Все пациенты
    params:
           patients - все пациенты
    """
    patients = db.session.query(Patient).all()
    return render_template('patients.html', patients=patients)


@app.route('/patients/<int:id>/')
def patient_detail(id):
    """
    Страница пациента
    params:
            appointments - все приемы конкретного пациента
            comments - все комменты написанные пациентом
    """
    patient = db.session.query(Patient).filter(Patient.id == id).first()
    appointments = patient.appointment
    comments = patient.comments
    return render_template('patient_detail.html',
                           patient=patient,
                           appointments=appointments,
                           comments=comments)


@app.route('/clinics/')
def index_clinics():
    """
    Все клиники
    params:
           clinics - все клиники
    """
    clinics = db.session.query(Clinic).all()
    return render_template('clinics.html', clinics=clinics)


@app.route('/clinics/<int:id>/')
def clinic_detail(id):
    """
    Страница клиники
    params:
            clinic - страница конкретной клиники
    """
    clinic = db.session.query(Clinic).filter(Clinic.id == id).first()
    return render_template('clinic_detail.html',
                           clinic=clinic)


@app.route('/doctors/<title>/')
def doctors_spec(title):
    """
        Доктора по специальности
        params:
                patients - пациенты на приеме у доктора конкретной специальности
    """

    patients = db.session.query(Patient, Doctor, Specialty, Clinic, Appointment)\
        .select_from(Appointment)\
        .join(Patient).filter(Appointment.patient_id == Patient.id)\
        .join(Doctor).filter(Appointment.doctor_id == Doctor.id)\
        .join(Clinic).filter(Doctor.clinica_id == Clinic.id)\
        .join(Specialty).filter(Doctor.specialty_id == Specialty.id)\
        .filter(Specialty.title == title)\
        .all()
    return render_template('patients_specialty.html', patients=patients, title=title)


@app.errorhandler(404)
def page_not_found(e):
    """
    Нет такой страницы на сервере
    params:
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Внутренняяя ошибка сервера
    params:
    """
    return render_template('500.html'), 500


@app.route('/profile/')
@login_required
def profile():
    image_file = url_for('static', filename='images/' + current_user.image)
    return render_template('profile.html', username=current_user.username, image_file=image_file)

################   Черновики ###################


@app.route('/comments/')
def index_comments():
    """
    Все комментарии на сайте
    params:
           comments - все комментарии
    """
    comments = db.session.query(Comment).all()
    return render_template('comments.html', comments=comments)


@app.route('/comments/<int:id>/')
def comment_detail(id):
    """
        Комменты по конкретному доктору (публично)
    params:
            comments
    """
    comment = db.session.query(Comment).filter(Comment.id == id).first()
    return render_template('comment_detail.html', comment=comment)


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


@app.route('/secret/')
def secret_test():
    return 'Only authenticated users are allowed'



@app.route('/add-clinic/', methods=['GET', 'POST'])
def add_clinic():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
    email = form.email.data
    message = form.message.data
    print(name)
    print(email)
    print(message)
    # здесь логика базы данных
    print("\nData received. Now redirecting ...")
    return redirect(url_for('contact'))

    return render_template('contact.html', form=form)
    return render_template('form_add_clinic.html', form=form)
