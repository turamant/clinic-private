import datetime

from flask_login import UserMixin, LoginManager
from sqlalchemy.ext.orderinglist import ordering_list

from .auth import auth
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

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#######3   Models ###########


class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    doctors = db.relationship('Doctor', backref='specialty', lazy='dynamic')

    def __repr__(self):
        return f'<Speciality: {self.title}>'

    def __str__(self):
        return f'{self.title}'


class Clinic(db.Model):
    __tablename__ = 'clinics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    street_id = db.Column(db.Integer, db.ForeignKey('streets.id'))
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    phone = db.Column(db.String(12), unique=True)
    doctors = db.relationship('Doctor', backref='clinic99', lazy='dynamic')
    cabinets = db.relationship('Cabinet', backref='clinic', lazy='dynamic')

    def __repr__(self):
        return f'{self.title}'

    def __str__(self):
        return f'{self.title}'


class Cabinet(db.Model):
    __tablename__ = 'cabinets'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))
    doctor = db.relationship('Doctor', backref='cabinet', lazy='dynamic')


    def __repr__(self):
        return f'{self.number}'

    def __str__(self):
        return f'{self.number}'


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    post_index = db.Column(db.String(6), unique=True)
    latitude = db.Column(db.Numeric(11, 7))
    longitude = db.Column(db.Numeric(11, 7))
    patients = db.relationship('Patient', backref='city', lazy='dynamic')
    clinics = db.relationship('Clinic', backref='city', lazy='dynamic')


    def __repr__(self):
        return f'<City: {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Street(db.Model):
    __tablename__ = 'streets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    patients = db.relationship('Patient', backref='street', lazy='dynamic')
    clinics = db.relationship('Clinic', backref='street', lazy='dynamic')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(6))
    patients = db.relationship('Patient', backref='house', lazy='dynamic')
    clinics = db.relationship('Clinic', backref='house', lazy='dynamic')

    def __repr__(self):
        return self.number

    def __str__(self):
        return self.number


class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(6), unique=True)
    patients = db.relationship('Patient', backref='apartment', lazy='dynamic')

    def __repr__(self):
        return self.number

    def __str__(self):
        return self.number


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    family = db.Column(db.String(256))
    name = db.Column(db.String(256))
    patronymic = db.Column(db.String(256))
    date_of_birth = db.Column(db.Date)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    street_id = db.Column(db.Integer, db.ForeignKey('streets.id'))
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    phone = db.Column(db.String(12), unique=True)
    comments = db.relationship('Comment', backref='patient', lazy='dynamic')

    @property
    def get_age(self):
        now = datetime.datetime.now()
        now_b = datetime.date(year=now.year, month=now.month, day=now.day)
        age = (int((now_b - self.date_of_birth).days / (365.2425)))
        print(age)
        return age

    def __repr__(self):
        return f'{self.family}'

    def __str__(self):
        return f'{self.family}'


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    family = db.Column(db.String(256))
    name = db.Column(db.String(256))
    patronymic = db.Column(db.String(256))
    clinica_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))
    cabinet_id = db.Column(db.Integer, db.ForeignKey('cabinets.id'))
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'))
    admission_cost = db.Column(db.Numeric(10, 2))
    deduction_percentage = db.Column(db.Numeric(10, 2))
    comments = db.relationship('Comment', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return f'{self.family}'

    def __str__(self):
        return f'{self.family}'


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor = db.relationship(Doctor, backref="appointment")
    patient = db.relationship(Patient, backref="appointment")
    data = db.Column(db.Date)
    time = db.Column(db.Time)


    def __repr__(self):
        return f'Дата {self.data} и время {self.time} приема: '

    def __str__(self):
        if self.patient != None:
            return f'Дата: {self.data} Время: {self.time} Доктор: {self.doctor}, Пациент: {self.patient}'
        return f'Дата: {self.data} Время: {self.time} Доктор: {self.doctor} Пациент:'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    body = db.Column(db.String(1024))
    created = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)



    def __repr__(self):
        return f'Автор {self.name}: {self.body},{self.created}'

    def __str__(self):
        return f'Автор {self.name}: {self.body},{self.created}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    image = db.Column(db.String(20), nullable=True, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


########## End Models #######


app.register_blueprint(auth, url_prefix='/auth')

### Admin panel ###
admin = Admin(app, 'Clinic', url='/admin')

admin.add_view(ModelView(Specialty, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Doctor, db.session))
admin.add_view(ModelView(Appointment, db.session))

admin.add_view(ModelView(City, db.session))
admin.add_view(ModelView(Street, db.session))
admin.add_view(ModelView(House, db.session))
admin.add_view(ModelView(Apartment, db.session))

admin.add_view(ModelView(Clinic, db.session))
admin.add_view(ModelView(Cabinet, db.session))
admin.add_view(ModelView(Comment, db.session))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))


from clinic_app import routers, auth
