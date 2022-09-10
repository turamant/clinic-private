from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from sqlalchemy import func

from clinic_app import app, Appointment, Doctor, db, Patient, Specialty, Comment, Clinic
from clinic_app.forms import ClinicForm, DoctorForm, PatientForm, AppointmentForm, AppointmentFormWitOutDoctor


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
    print("-------appoint--=", appointments)

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


@app.route('/special/')
def index_specialty():
    """
    Все специальности
    params:
           specials - все специальности
    """
    specials = db.session.query(Specialty).all()
    return render_template('specials.html', specials=specials)


@app.route('/specials/<int:id>/')
def special_detail(id):
    """
    Страница специальности
    params:
            special - специальность доктора
            doctors - доктора этой специальности
    """
    special = db.session.query(Specialty).filter(Specialty.id == id).first()
    doctors = special.doctors
    return render_template('special_detail.html',
                           doctors=doctors,
                           special=special)


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
    print("DOCTOR_APP", appointments)
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


##################  пока никуда не выведено ######################
@app.route('/doctors/patients/<title>/')
def doctors_spec(title):
    """
        Доктора по специальности
        params:
                patients - пациенты, побывавшие на приеме у доктора конкретной специальности
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


@app.route('/doctors/new', methods=['GET', 'POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        new_doctor = Doctor(
            family=request.form.get('family'),
            name=request.form.get('name'),
            patronymic=request.form.get('patronymic'),
            clinica_id=request.form.get('clinica_id'),
            cabinet_id=request.form.get('cabinet_id'),
            specialty_id=request.form.get('specialty_id'),
            admission_cost=request.form.get('admission_cost'),
            deduction_percentage=request.form.get('deduction_percentage'))
        db.session.add(new_doctor)
        db.session.commit()
        flash('Доктор был успешно добавлен', 'success')
        return redirect(url_for('doctor_detail', id=new_doctor.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_doctor.html', form=form)


@app.route('/doctor/update/<int:id>/', methods=['GET', 'POST'])
def update_doctor(id):
    doctor = db.session.query(Doctor).get(id)
    form = DoctorForm(obj=doctor)
    if form.validate_on_submit():
        form.populate_obj(doctor)
        db.session.add(doctor)
        db.session.commit()
        flash('Доктор был успешно добавлен', 'success')
        return redirect(url_for('doctor_detail', id=doctor.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_doctor.html', form=form)


@app.route('/doctor/delete/<int:id>/', methods=['GET', 'POST'])
def del_doctor(id):
    doctor = db.session.query(Doctor).filter(Doctor.id == id).one()
    if request.method == 'POST':
        db.session.delete(doctor)
        db.session.commit()
        return redirect(url_for('index_doctors'))
    return render_template('delete_doctor.html', doctor=doctor)



@app.route('/clinics/new', methods=['GET', 'POST'])
def add_clinic():
    form = ClinicForm()
    if form.validate_on_submit():
        new_clinic = Clinic(
            title=request.form.get('title'),
            city_id=request.form.get('city_id'),
            street_id=request.form.get('street_id'),
            house_id=request.form.get('house_id'),
            phone=request.form.get('phone'))
        db.session.add(new_clinic)
        db.session.commit()
        flash('Клиника была успешно добавлена', 'success')
        return redirect(url_for('clinic_detail', id=new_clinic.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_clinic.html', form=form)


@app.route('/clinic/update/<int:id>/', methods=['GET', 'POST'])
def update_clinic(id):
    clinic = db.session.query(Clinic).get(id)
    form = ClinicForm(obj=clinic)
    if form.validate_on_submit():
        form.populate_obj(clinic)
        db.session.add(clinic)
        db.session.commit()
        flash('Клиника была успешно отредактирована', 'success')
        return redirect(url_for('clinic_detail', id=clinic.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_clinic.html', form=form)


@app.route('/clinic/delete/<int:id>/', methods=['GET', 'POST'])
def del_clinic(id):
    clinic = db.session.query(Clinic).filter(Clinic.id == id).one()
    if request.method == 'POST':
        db.session.delete(clinic)
        db.session.commit()
        return redirect(url_for('index_clinics'))
    return render_template('delete_clinic.html', clinic=clinic)


@app.route('/patients/new', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        new_patient = Patient(
            family=request.form.get('family'),
            name=request.form.get('name'),
            patronymic=request.form.get('patronymic'),
            date_of_birth=request.form.get('date_of_birth'),
            city_id=request.form.get('city_id'),
            street_id=request.form.get('street_id'),
            house_id=request.form.get('house_id'),
            apartment_id=request.form.get('apartment_id'),
            phone=request.form.get('phone'))
        db.session.add(new_patient)
        db.session.commit()
        flash(' Пациент был успешно добавлен', 'success')
        return redirect(url_for('patient_detail', id=new_patient.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_patient.html', form=form)


@app.route('/patient/update/<int:id>/', methods=['GET', 'POST'])
def update_patient(id):
    patient = db.session.query(Patient).get(id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.add(patient)
        db.session.commit()
        flash('Данные пациента были успешно изменены', 'success')
        return redirect(url_for('patient_detail', id=patient.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_patient.html', form=form)


@app.route('/patient/delete/<int:id>/', methods=['GET', 'POST'])
def del_patient(id):
    patient = db.session.query(Patient).filter(Patient.id == id).one()
    if request.method == 'POST':
        db.session.delete(patient)
        db.session.commit()
        return redirect(url_for('index_patients'))
    return render_template('delete_patient.html', patient=patient)


@app.route('/appointments/')
def index_appointments():
    """
    Все доктора
    params:
           doctors - все доктора
    """
    appointments = db.session.query(Appointment).all()
    for appoint in appointments:
        print("++++++", appoint.patient_id)
    print("====appointments==", appointments)
    return render_template('appointments.html', appointments=appointments)



@app.route('/appointment/<int:id>/')
def appointment_detail(id):
    """
    Страница доктора
    params:
            appointments - все приемы конкретного доктора
            comments - все комменты для доктора от пациентов
    """
    appointment = db.session.query(Appointment).filter(Appointment.id == id).first()
    doctor = appointment.doctor
    patient = appointment.patient
    return render_template('appointment_detail.html',
                           appointment=appointment,
                           doctor=doctor,
                           patient=patient)


@app.route('/doctor/appointments/<int:id>/', methods=['GET', 'POST'])
def add_doctor_appointment(id):
    doctor = db.session.query(Doctor).filter(Doctor.id == id).first()
    form = AppointmentFormWitOutDoctor()
    if form.validate_on_submit():
        pathient = request.form.get('patient_id')
        if pathient == 'None':
            pathient = None
        new_appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=pathient,
            data=request.form.get('data'),
            time=request.form.get('time'))
        db.session.add(new_appointment)
        db.session.commit()
        flash(' Прием был успешно записан', 'success')
        return redirect(url_for('doctor_detail', id=doctor.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_doctor_appointment.html', form=form)



@app.route('/appointments/new', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        pathient = request.form.get('patient_id')
        doctor = request.form.get('doctor_id')
        if pathient == 'None':
            pathient = None
        new_appointment = Appointment(
            doctor_id=request.form.get('doctor_id'),
            patient_id=pathient,
            data=request.form.get('data'),
            time=request.form.get('time'))
        db.session.add(new_appointment)
        db.session.commit()
        flash(' Прием был успешно записан', 'success')
        return redirect(url_for('doctor_detail', id=doctor))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_appointment.html', form=form)


@app.route('/appointment/update/<int:id>/', methods=['GET', 'POST'])
def update_appointment(id):
    appointment = db.session.query(Appointment).get(id)
    form = AppointmentForm(obj=appointment)
    patient = request.form.get('patient_id')
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.add(appointment)
        db.session.commit()
        flash('Данные пприема были успешно изменены', 'success')
        return redirect(url_for('patient_detail', id=patient))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('new_appointment.html', form=form)


@app.route('/appointment/delete/<int:id>/', methods=['GET', 'POST'])
def del_appointment(id):
    appointment = db.session.query(Appointment).filter(Appointment.id == id).one()
    if request.method == 'POST':
        db.session.delete(appointment)
        db.session.commit()
        return redirect(url_for('index_appointments'))
    return render_template('delete_appointment.html', appointment=appointment)


