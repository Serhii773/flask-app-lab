from flask import render_template, request, redirect, url_for

from app.users import users_bp

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/hi.html", name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", age=67, _external=True)
    print(to_url)
    return redirect(to_url)