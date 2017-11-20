from flask_wtf import Form  
from wtforms import StringField, BooleanField  
from wtforms.validators import DataRequired  
from flask_security.forms import LoginForm, _datastore


class ExtendedLoginForm(LoginForm):

    def validate(self):
        validation = Form.validate(self)
        self.user = _datastore.get_user(self.email.data)
        return validation
