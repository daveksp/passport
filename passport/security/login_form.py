from flask_wtf import Form  
from flask_security.forms import LoginForm, _datastore
from flask_security.utils import encrypt_password
from wtforms import StringField, BooleanField 
from wtforms.validators import DataRequired  


class ExtendedLoginForm(LoginForm):

    def validate(self):
        validation = Form.validate(self)
        self.user = _datastore.find_user(
        	email=self.email.data)
        	#password=encrypt_password(self.password.data))
        import pdb; pdb.set_trace()
        return validation
