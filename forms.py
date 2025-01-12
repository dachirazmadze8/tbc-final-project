from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileSize,FileAllowed
from wtforms import StringField, DecimalField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired, NumberRange, length,ValidationError,equal_to


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(min=3, max=32)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange()])
    img = FileField("Product image here", validators=[
        FileRequired(),
        FileSize(max_size=10 * 1024 * 1024, message="File must be 10 MB maximum!"),
        FileAllowed(["jpg", "png", "jpeg"], message="Only JPG, PNG, JPEG files are allowed."),
    ])
    grape = StringField('Grape', validators=[DataRequired(), length(min=3, max=32)])
    region = StringField('Region', validators=[DataRequired(), length(min=3, max=32)])
    aroma = StringField('Aroma', validators=[DataRequired(), length(min=3, max=32)])
    taste = StringField('Taste', validators=[DataRequired(), length(min=3, max=32)])
    color = StringField('Color', validators=[DataRequired(), length(min=3, max=32)])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The name must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The name must contain at least one lowercase letter.")

    def validate_grape(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The grape must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The grape must contain at least one lowercase letter.")

    def validate_region(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The region must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The region must contain at least one lowercase letter.")

    def validate_aroma(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The aroma must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The aroma must contain at least one lowercase letter.")

    def validate_taste(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The taste must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The taste must contain at least one lowercase letter.")

    def validate_color(self, field):
        contains_lowercase = any(char.islower() for char in field.data)
        contains_uppercase = any(char.isupper() for char in field.data)

        if not contains_uppercase:
            raise ValidationError("The color must contain at least one uppercase letter.")
        if not contains_lowercase:
            raise ValidationError("The color must contain at least one lowercase letter.")



class RegisterForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired(),length(min=8,max=32)])
    repeat_password = PasswordField("repeat password",validators=[equal_to("password")])
    register = SubmitField("register")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), length(min=8, max=32)])
    remember_me = BooleanField("remember me")

    login = SubmitField("login")




