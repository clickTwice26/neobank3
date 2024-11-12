from starlette_wtf import StarletteForm  # Correct import for StarletteForm
from wtforms import StringField, PasswordField, EmailField  # WTForms fields
from wtforms.validators import DataRequired, Email
from wtforms.widgets import PasswordInput

# LoginForm using StarletteForm from starlette_wtf
class LoginForm(StarletteForm):
    username = StringField(
        'Username',
        validators=[DataRequired('Please enter your username')]
    )

    password = PasswordField(
        'Password',
        widget=PasswordInput(hide_value=True),  # Hide password input value
        validators=[DataRequired('Please enter your password')]
    )


# SignupForm using WTForms Form class
class SignupForm(StarletteForm):  # Use StarletteForm for form handling
    username = StringField(
        'Username',
        validators=[DataRequired('Please enter your username')]
    )

    password = PasswordField(
        'Password',
        widget=PasswordInput(hide_value=True),  # Password field with hidden value
        validators=[DataRequired('Please enter your password')]
    )

    email = EmailField(
        'Email Address',
        validators=[DataRequired('Please enter your email'), Email('Invalid email address')]
    )
