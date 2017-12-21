from flask_wtf import Form  
from flask_security.forms import LoginForm, _datastore
from flask_security.utils import encrypt_password
from wtforms import StringField, BooleanField 
from wtforms.validators import DataRequired  



class ExtendedLoginForm(LoginForm):

    def validate(self):
        response = super(ExtendedLoginForm, self).validate()
        return response