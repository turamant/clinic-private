import datetime
import os
import random
from datetime import datetime

from flask_login import current_user
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security
from flask_wtf import CSRFProtect

from markupsafe import Markup


from .auth import auth
from flask import Flask, url_for, redirect, request
from flask_admin import Admin, form, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from config import DevelopementConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates",  static_folder="static")
csrf = CSRFProtect(app)
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''
#######3   Models ###########

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


class Signup(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    department = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(256), nullable=False)
    message = db.Column(db.Text(1000), nullable=False)

    def __str__(self):
        return self.email


class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    doctors = db.relationship('Doctor', backref='specialty', lazy='dynamic')

    def __repr__(self):
        return f'<Speciality: {self.title}>'

    def __str__(self):
        return f'{self.title}'


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    doctors = db.relationship('Doctor', backref='departments')

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
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    category = db.Column(db.String(256), nullable=True)
    stage = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(1000), nullable=True)
    education = db.Column(db.String(1000), nullable=True)
    work_experience = db.Column(db.String(1000), nullable=True)
    admission_cost = db.Column(db.Numeric(10, 2))
    deduction_percentage = db.Column(db.Numeric(10, 2))
    comments = db.relationship('Comment', backref='doctor', lazy='dynamic')
    photo = db.relationship('PhotoModel', backref='doctor', uselist=False)

    def __repr__(self):
        return f'{self.family}'

    def __str__(self):
        return f'{self.family}'


class PhotoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))
    type = db.Column(db.Unicode(3))
    create_date = db.Column(db.DateTime, default=datetime.now)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)

    def __repr__(self):
        return f'{self.name}'


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
        return f'???????? {self.data} ?? ?????????? {self.time} ????????????: '

    def __str__(self):
        if self.patient != None:
            return f'????????: {self.data} ??????????: {self.time}'
        return f'????????: {self.data} ??????????: {self.time} '


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
        return f'?????????? {self.name}: {self.body},{self.created}'

    def __str__(self):
        return f'?????????? {self.name}: {self.body},{self.created}'




class PhotoAdminModel(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        url = url_for('static', filename=os.path.join('storage/', model.path))

        if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup('<img src="%s" width="100">' % url)

        if model.type in ['mp3']:
            return Markup('<audio controls="controls"><source src="%s" type="audio/mpeg" /></audio>' % url)

    column_formatters = {
        'path': _list_thumbnail
    }
    form_extra_fields = {
        'file': form.FileUploadField('file', base_path=app.config['STORAGE'])
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)

                storage_file.save(
                    os.path.join(app.config['STORAGE'], path)
                )

                _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = path
                _form.type.data = ext

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(PhotoAdminModel, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(PhotoAdminModel, self).create_form(obj)
        )


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    pass

########## End Models #######


app.register_blueprint(auth, url_prefix='/auth')

### Admin panel ###
admin = Admin(app, 'Democlinic', url='/', index_view=HomeAdminView())

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

admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(PhotoAdminModel(PhotoModel, db.session))
admin.add_view(ModelView(Signup, db.session))


from clinic_app import routers, auth

