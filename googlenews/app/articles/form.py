from wtforms import Form, TextAreaField, StringField, SelectField, validators

class RegistrationForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=60)])
    content = TextAreaField('Content', [validators.Length(min=6)])
    image = SelectField('Image', choices=[('default', 'Choose an image')])