from flask import (render_template, request, redirect, url_for, flash,session, make_response)

from app.users import users_bp

# Заглушкові дані для входу
VALID_USERNAME = "Serhii"
VALID_PASSWORD = "123"


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


#Login

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Сторінка входу:
    - GET: показати форму
    - POST: перевірити логін/пароль, покласти користувача в сесію або показати помилку
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            flash("Ви успішно увійшли до системи.", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірне ім'я користувача або пароль.", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


#Profile

@users_bp.route("/profile")
def profile():
    """
    Якщо користувач не у сесії -> редирект на login з flash-помилкою.
    Також тут зчитуємо всі cookie та вибраний theme.
    """
    username = session.get("user")
    if not username:
        flash("Будь ласка, увійдіть до системи для перегляду профілю.", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("profile_theme", "light")
    cookies = list(request.cookies.items())  # [(key, value), ...]

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=username,
        theme=theme,
        cookies=cookies,
    )


#Logout

@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


#Cookie actions

@users_bp.route("/profile/add-cookie", methods=["POST"])
def add_cookie():
    """
    Додати кукі (ключ, значення, термін дії в днях).
    """
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

    max_age = days * 24 * 60 * 60  # у секундах

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=max_age)
    flash(f"Кукі '{key}' успішно додано.", "success")
    return resp


@users_bp.route("/profile/delete-cookie", methods=["POST"])
def delete_cookie():
    """
    Видалити один кукі за ключем.
    """
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
    """
    Видалити всі кукі користувача (включно з session).
    """
    if "user" not in session:
        flash("Спочатку увійдіть до системи.", "warning")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))

    for key in list(request.cookies.keys()):
        resp.delete_cookie(key)

    session.clear()
    flash("Усі кукі успішно видалено.", "info")
    return resp


#Colour

@users_bp.route("/set-theme/<string:theme>")
def set_theme(theme: str):
    """
    Зберігає вибір (light / dark) у кукі 'profile_theme' і повертає на profile.
    """
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
