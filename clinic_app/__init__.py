from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from config import DevelopementConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates",  static_folder="static")
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#######3   Models ###########

class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    doctors = db.relationship('Doctor', backref='specialties', lazy='dynamic')

    def __repr__(self):
        return f'<Speciality: {self.title}>'

    def __str__(self):
        return f'{self.title}'


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    family = db.Column(db.String(256))
    name = db.Column(db.String(256))
    patronymic = db.Column(db.String(256))
    date_of_birth = db.Column(db.DateTime)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    def __repr__(self):
        return f'<Patient: {self.family}>'

    def __str__(self):
        return f'{self.family}'


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    family = db.Column(db.String(256))
    name = db.Column(db.String(256))
    patronymic = db.Column(db.String(256))
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'))
    admission_cost = db.Column(db.Numeric(10, 2))
    deduction_percentage = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f'<Doctor: {self.family}>'

    def __str__(self):
        return f'{self.family}'


class Appointment(db.Model):
    __tablename__ = 'doctors_patients'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor = db.relationship(Doctor, backref="appointment")
    patient = db.relationship(Patient, backref="appointment")
    data_appointment = db.Column(db.DateTime, unique=True)

    def __repr__(self):
        return f'Дата приема: {self.data_appointment}'

    def __str__(self):
        return f'{self.data_appointment}'


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    street = db.Column(db.String(256))
    house_number = db.Column(db.Integer)
    apartment_number = db.Column(db.Integer)
    patients = db.relationship('Patient', backref='address', lazy='dynamic')

    def __repr__(self):
        return f'<Addres: {self.street}>'

    def __str__(self):
        return f'{self.street}'


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    post_index = db.Column(db.String(6), unique=True)
    latitude = db.Column(db.Numeric(11, 7))
    longitude = db.Column(db.Numeric(11, 7))
    addresses = db.relationship('Address', backref='city', lazy='dynamic')

    def __repr__(self):
        return f'<City: {self.name}>'

    def __str__(self):
        return f'{self.name}'


########## End Models #######



### Admin panel ###
admin = Admin(app, 'Clinic', url='/admin')

admin.add_view(ModelView(Specialty, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Doctor, db.session))
admin.add_view(ModelView(Appointment, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(City, db.session))


from clinic_app import routers
