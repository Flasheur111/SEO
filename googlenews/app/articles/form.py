from wtforms import Form, TextAreaField, StringField, SelectField, BooleanField, validators

class RegistrationForm(Form):
    full_analysis = BooleanField('Full extraction', [validators.required])
    title = StringField('Title', [validators.Length(min=4, max=60)])
    content = TextAreaField('Content', [validators.Length(min=6)])
    image = SelectField('Image', choices=[('default', 'Choose an image')])