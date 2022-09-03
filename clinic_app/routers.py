from flask import render_template

from clinic_app import app, Appointment, Doctor, db


@app.route('/')
def index():
    '''
    reviews = db.session.query(Reservation.room_id, Room.address, func.avg(Review.rating)).select_from(Reservation) \
        .join(Review).filter(Review.reservation_id == Reservation.id) \
        .join(Room).filter(Room.id == Reservation.room_id) \
        .group_by(Reservation.room_id).having(func.avg(Review.rating)).all() '''

    ''' select data_appointment, doctors.family from doctors_patients JOIN doctors
    ON doctors_patients.id = doctors.id; '''
    appointments = db.session.query(Appointment.data_appointment, Doctor.family).select_from(Appointment)\
        .join(Doctor).filter(Appointment.doctor_id == Doctor.id).all()
    print("...appointments...=", appointments)
    return render_template('index.html', appointments=appointments)


@app.route('/doctors')
def index_doctors():
    doctors = db.session.query(Doctor).all()
    return render_template('doctors.html', doctors=doctors)