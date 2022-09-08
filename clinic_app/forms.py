from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from clinic_app import Clinic


class ClinicForm(ModelForm):
    class Meta:
        model = Clinic
        include = ['city_id', 'street_id', 'house_id' ]


class ClinicForm2(Form):
    title = StringField(validators=[DataRequired(), Length(max=100)])
    phone = StringField(validators=[DataRequired(), Length(max=255)])
