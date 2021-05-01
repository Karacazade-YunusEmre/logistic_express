from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('', [
        validators.Length(min=2, max=25, message="Kullanıcı adı alanı en az 2 en fazla 25 karakterden oluşabilir."),
        validators.DataRequired()], render_kw={"placeholder": "Kullanıcı Adı"})
    password = PasswordField('', [validators.DataRequired(), validators.length(min=4, max=16,
                                                                               message="Şifre alanı en az 4 en fazla 16 karakterden oluşabilir")],
                             render_kw={"placeholder": "Şifreniz"})
