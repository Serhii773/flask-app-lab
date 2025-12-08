from flask import render_template, request, redirect, url_for, flash, session, make_response

from app.users import users_bp
from app.forms import LoginForm

# Заглушкові дані для входу
VALID_USERNAME = "Serhii"
VALID_PASSWORD = "1234"

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=67, _external=True)
    print(to_url)
    return redirect(to_url)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            session["remember"] = remember

            remember_msg = (
                "Опція remember увімкнена."
                if remember
                else "Опція remember не була обрана."
            )

            flash(
                f"Вітаємо, {username}! Ви успішно увійшли. {remember_msg}",
                "success",
            )

            return redirect(url_for("users.profile"))
        else:
            flash("Невірне ім'я користувача або пароль.", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід", form=form)

@users_bp.route("/profile")
def profile():
    username = session.get("user")
    if not username:
        flash("Будь ласка, увійдіть до системи для перегляду профілю.", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("profile_theme", "light")
    cookies = list(request.cookies.items())  # [(key, value), ...]
    remember = session.get("remember", False)

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=username,
        theme=theme,
        cookies=cookies,
        remember=remember,
    )

@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    session.pop("remember", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/profile/add-cookie", methods=["POST"])
def add_cookie():
    if "user" not in session:
        flash("Спочатку увійдіть до системи.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("cookie_key", "").strip()
    value = request.form.get("cookie_value", "").strip()
    days_str = request.form.get("cookie_days", "").strip()

    if not key or not value:
        flash("Ключ і значення кукі не можуть бути порожніми.", "danger")
        return redirect(url_for("users.profile"))

    try:
        days = int(days_str) if days_str else 1
        if days <= 0:
            raise ValueError
    except ValueError:
        flash("Термін дії (у днях) має бути додатним цілим числом.", "danger")
        return redirect(url_for("users.profile"))

    max_age = days * 24 * 60 * 60

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=max_age)
    flash(f"Кукі '{key}' успішно додано.", "success")
    return resp


@users_bp.route("/profile/delete-cookie", methods=["POST"])
def delete_cookie():
    if "user" not in session:
        flash("Спочатку увійдіть до системи.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("cookie_key_delete", "").strip()
    resp = make_response(redirect(url_for("users.profile")))

    if not key:
        flash("Вкажіть ключ кукі для видалення.", "danger")
        return resp

    if key not in request.cookies:
        flash(f"Кукі з ключем '{key}' не знайдено.", "warning")
        return resp

    resp.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено.", "info")
    return resp


@users_bp.route("/profile/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "user" not in session:
        flash("Спочатку увійдіть до системи.", "warning")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))

    for key in list(request.cookies.keys()):
        resp.delete_cookie(key)

    session.clear()
    flash("Усі кукі успішно видалено.", "info")
    return resp
@users_bp.route("/set-theme/<string:theme>")
def set_theme(theme: str):
    if theme not in ("light", "dark"):
        flash("Невірна схема кольорів.", "danger")
        return redirect(url_for("users.profile"))

    if "user" not in session:
        flash("Спочатку увійдіть до системи.", "warning")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("profile_theme", theme, max_age=30 * 24 * 60 * 60)
    flash(
        "Кольорова схема змінена на "
        + ("темну." if theme == "dark" else "світлу."),
        "info",
    )
    return resp
