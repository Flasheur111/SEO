from wtforms import Form, TextAreaField, StringField, SelectField, validators

class RegistrationForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=120)])
    content = TextAreaField('Content', [validators.Length(min=6)])
    image = SelectField('Image', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')],)
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.required()])