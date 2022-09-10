from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, SubmitField, FloatField, DateField, TimeField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from clinic_app import Clinic, City, Street, House, Cabinet, Specialty, Patient, Apartment, Doctor, Appointment


class ClinicModelForm(ModelForm):
    class Meta:
        model = Clinic
        include = ['city_id', 'street_id', 'house_id' ]


choice_city = list()
for city in City.query.all():
    choice_city.append((city.id, city.name))

choice_street = list()
for street in Street.query.all():
    choice_street.append((street.id, street.name))

choice_house = list()
for house in House.query.all():
    choice_house.append((house.id, house.number))

choice_cabinet = list()
for cabinet in Cabinet.query.all():
    choice_cabinet.append((cabinet.id, cabinet.number))

choice_clinic = list()
for clinic in Clinic.query.all():
    choice_clinic.append((clinic.id, clinic.title))

choice_specialty = list()
for special in Specialty.query.all():
    choice_specialty.append((special.id, special.title))

choice_apartment = list()
for apart in Apartment.query.all():
    choice_apartment.append((apart.id, apart.number))

choice_doctor = []
for doctor in Doctor.query.all():
    choice_doctor.append((doctor.id, doctor.family))

choice_patient = [(None, "")]
for patient in Patient.query.all():
    choice_patient.append((patient.id, patient.family))


class ClinicForm(FlaskForm):
    title = StringField(label='название', validators=[DataRequired(), Length(max=256)])
    city_id = SelectField(label='город', choices=choice_city, validators=[DataRequired()])
    street_id = SelectField(label='улица', choices=choice_street, validators=[DataRequired()])
    house_id = SelectField(label='дом', choices=choice_house, validators=[DataRequired()])
    phone = StringField(label='телефон', validators=[DataRequired(), Length(max=12)])


class DoctorForm(FlaskForm):
    family = StringField(label='Фамилия:', validators=[DataRequired(), Length(max=256)])
    name = StringField(label='Имя:', validators=[DataRequired(), Length(max=256)])
    patronymic = StringField(label='Отчество:', validators=[DataRequired(), Length(max=256)])
    clinica_id = SelectField(label='Клиника:', choices=choice_clinic, validators=[DataRequired()])
    cabinet_id = SelectField(label='Кабинет:', choices=choice_cabinet, validators=[DataRequired()])
    specialty_id = SelectField(label='Специальность:', choices=choice_specialty, validators=[DataRequired()])
    admission_cost = FloatField(label='Тариф:', validators=[DataRequired()])
    deduction_percentage = FloatField(label='Поцент:', validators=[DataRequired()])


class PatientForm(FlaskForm):
    family = StringField(label='Фамилия:', validators=[DataRequired(), Length(max=256)])
    name = StringField(label='Имя:', validators=[DataRequired(), Length(max=256)])
    patronymic = StringField(label='Отчество:', validators=[DataRequired(), Length(max=256)])
    date_of_birth = DateField(label='Дата рождения', validators=[DataRequired()])
    city_id = SelectField(label='город', choices=choice_city, validators=[DataRequired()])
    street_id = SelectField(label='улица', choices=choice_street, validators=[DataRequired()])
    house_id = SelectField(label='дом', choices=choice_house, validators=[DataRequired()])
    apartment_id = SelectField(label='Квартира', choices=choice_apartment, validators=[DataRequired()])
    phone = StringField(label='телефон', validators=[DataRequired(), Length(max=12)])


class AppointmentForm(FlaskForm):
    doctor_id = SelectField(label='Доктор:', choices=choice_doctor, validators=[DataRequired()])
    patient_id = SelectField(label='Пациент:', choices=choice_patient, validators=[DataRequired()])
    data = DateField(label='Дата приема:', validators=[DataRequired()])
    time = TimeField(label='Время приема:', validators=[DataRequired()])


class AppointmentFormWitOutDoctor(FlaskForm):
    patient_id = SelectField(label='Пациент:', choices=choice_patient, validators=[DataRequired()])
    data = DateField(label='Дата приема:', validators=[DataRequired()])
    time = TimeField(label='Время приема:', validators=[DataRequired()])
