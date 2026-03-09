from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()],
                       render_kw ={"placeholder" : "Имя игрока"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 6)],
                       render_kw ={"placeholder" : "Пароль"})
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo("password")],
                                     render_kw={"placeholder": "Повтор пароля"})
    submit = SubmitField("Confirm", render_kw={"value": "Зарегистрироваться"} )

class AuthForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()],
                       render_kw ={"placeholder" : "Имя игрока"})
    password = PasswordField("Password", validators=[DataRequired()],
                       render_kw ={"placeholder" : "Пароль"})
    submit = SubmitField("Confirm", render_kw={"value": "Войти"} )