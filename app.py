from flask import Flask, request, session, redirect, url_for, render_template, flash
from passlib.handlers.sha2_crypt import sha256_crypt

from crud import add_request_price, add_message, get_user, add_user, create_freight, get_freight, get_my_freights, \
    get_admin, get_all_users, get_all_freights, get_request_freight, get_all_messages
from forms.register_form import RegistrationForm
from forms.login_form import LoginForm

from decorators.login_required import login_required
from decorators.admin_login_required import admin_login_required
from utilities import get_freight_number

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "logged_in" in session:
            freight_number = request.form.get("freight_number")
            session["freight_number"] = freight_number
            return redirect(url_for("search_freight", search=True))

        else:
            return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        freight_type = request.form.get("freight_type")
        departure_city = request.form.get("departure_city")
        incoterms = request.form.get("incoterms")
        weight = request.form.get("weight")
        height = request.form.get("height")
        width = request.form.get("width")
        length = request.form.get("length")
        radio_extra = request.form.get("radio_extra")

        add_request_price(
            {
                "name": name,
                "email": email,
                "phone": phone,
                "freight_type": freight_type,
                "departure_city": departure_city,
                "incoterms": incoterms,
                "weight": weight,
                "height": height,
                "width": width,
                "length": length,
                "radio_extra": radio_extra,
            }
        )
        flash("Talebiniz Başarıyla Alındı.", "success")
        return redirect(url_for("about"))
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = request.form.get("message")
        name_lastname = request.form.get("name_lastname")
        email = request.form.get("email")
        subject = request.form.get("subject")

        add_message({
            "message": message,
            "name_lastname": name_lastname,
            "email": email,
            "subject": subject
        })

        flash("Mesajınız Başarıyla Alındı", "success")
        return redirect(url_for("index"))

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        result = get_user(username)
        if result:
            if sha256_crypt.verify(password, result.password):
                flash("Giriş İşlemi Başarılı", "success")

                session["logged_in"] = True
                session["id"] = result.id
                session["username"] = username
                session["name_lastname"] = f"{result.name} {result.last_name}"

                return redirect(url_for("index"))
            else:
                flash("Girilen Şifre Hatalı", "danger")
                return redirect(url_for("login"))
        else:
            flash("Kullanıcı Adı ve Şifre Hatalı", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = sha256_crypt.encrypt(form.password.data)

        add_user({
            "name": name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone_number": phone_number,
            "password": password
        })

        flash("Başarıyla Kayıt Oldunuz", "success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route("/add_freight", methods=["GET", "POST"])
@login_required
def add_freight():
    if request.method == "POST":
        freight_type = request.form.get("freight_type")
        departure_city = request.form.get("departure_city")
        incoterms = request.form.get("incoterms")
        weight = request.form.get("weight")
        height = request.form.get("height")
        width = request.form.get("width")
        length = request.form.get("length")
        radio_extra = request.form.get("freight_type")
        freight_number = get_freight_number()

        user = get_user(session["username"])

        data = {
            "user_id": user.id,
            "freight_type": freight_type,
            "departure_city": departure_city,
            "incoterms": incoterms,
            "weight": weight,
            "height": height,
            "width": width,
            "length": length,
            "radio_extra": radio_extra,
            "freight_number": freight_number
        }
        create_freight(data)

        flash("Gönderi Kaydınız Başarıyla Oluşturulmuştur.", "success")
        flash(f"Gönderi Numaranız: {freight_number}.", "danger")

        return redirect(url_for("index"))

    return render_template("add_freight.html")


@app.route("/search_freight", methods=["GET", "POST"])
@login_required
def search_freight():
    if request.method == "POST":
        table = None
        freight_number = request.form.get("freight_number")

        freight = get_freight(freight_number)

        if freight:
            table = {
                "id": freight.id,
                "freight_type": freight.freight_type,
                "departure_city": freight.departure_city,
                "weight": freight.weight,
                "height": freight.height,
                "freight_number": freight.freight_number
            }
            session["table"] = table

        return redirect(url_for("search_freight", table=table if table else None))

    return render_template("search_freight.html")


@app.route("/my_freight")
@login_required
def my_freight():
    my_freights = get_my_freights()
    return render_template("my_freight.html", freights=my_freights)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if get_admin(username, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_content"))
        else:
            flash("Giriş İşlemi Başarısız", "danger")
            return redirect(url_for("index"))
    return render_template("admin_login.html")


@app.route("/admin_content", methods=["POST", "GET"])
@admin_login_required
def admin_content():
    return render_template("admin_content.html")


@app.route("/admin_users")
@admin_login_required
def admin_users():
    users = get_all_users()
    return render_template("admin_users.html", users=users)


@app.route("/admin_freights")
@admin_login_required
def admin_freights():
    freights = get_all_freights()
    return render_template("admin_freights.html", freights=freights)


@app.route("/admin_request_freight")
@admin_login_required
def admin_request_freight():
    request_freight = get_request_freight()
    return render_template("admin_request_freight.html", request_freight=request_freight)


@app.route("/admin_get_messages")
@admin_login_required
def admin_messages():
    messages = get_all_messages()
    return render_template("admin_messages.html", messages=messages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
