from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField("", [
        validators.DataRequired(),
        validators.length(min=2, max=25,
                          message="İsim alanı en az 2 en fazla 25 karakterden oluşabilir")],
                       render_kw={"placeholder": "Adınız"})

    last_name = StringField("", [
        validators.DataRequired(),
        validators.length(min=2, max=25, message="Soyisim alanı en az 2 en fazla 25 karakterden oluşabilir")],
                            render_kw={"placeholder": "Soyadınız"})

    username = StringField("", [
        validators.DataRequired(),
        validators.length(min=2, max=25, message="Kullanıcı adı alanı en az 2 en fazla 25 karakterden oluşabilir")],
                           render_kw={"placeholder": "Kullanıcı Adı"})

    email = StringField("", [
        validators.DataRequired(),
        validators.Length(min=6, max=35, message="Lütfen geçerli bir mail adresi girin")],
                        render_kw={"placeholder": "Email"})

    phone_number = StringField("", [
        validators.DataRequired(),
        validators.length(min=10, max=11)],
                               render_kw={"placeholder": "İletişim Numarası"})

    password = PasswordField("", [
        validators.DataRequired(),
        validators.length(min=4, max=16, message="Şifre alanı en az 4 en fazla 16 karakterden oluşabilir"),
        validators.equal_to("confirm", message="Şifreler Uyuşmuyor")],
                             render_kw={"placeholder": "Şifre"})

    confirm = PasswordField("", render_kw={"placeholder": "Şifrenizi Doğrulayın"})
