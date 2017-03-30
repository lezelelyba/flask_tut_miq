import flask_wtf
import wtforms


class LoginForm(flask_wtf.Form):
    openid = wtforms.StringField('openid', validators=[
        wtforms.validators.DataRequired()])
    remember_me = wtforms.BooleanField('rember_me', default=False)
