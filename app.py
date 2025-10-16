from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__)
app.secret_key = "super_long_demo_secret_key_change_me"

@app.route("/")
def home():
    return redirect(url_for("resume"))

@app.route("/resume")
def resume():
    title = "Резюме"
    about = (
        "Full-Stack розробник із досвідом створення web-додатків, баз даних і IoT-проєктів. Працював у співпраці з Google над академічними ініціативами та розробляю full-stack рішення в рамках хакатонів InnovateX Labs (США). "
    )
    education = [
        {"school": "Stanford University", "program": "Software Engineering", "period": "2021 — 2023"}
    ]
    skills = ["Python (Flask, REST API, Jinja2)",
    "Java (OOP, Spring basics)",
    "Frontend: Angular, TypeScript, HTML5, CSS3, Bootstrap 5, Tailwind",
    "Databases: SQL (Oracle, PostgreSQL, MySQL)",
    "Algorithms & Data Structures",
    "Docker (Basics), Linux (CLI)"]
    technologies = ["Flask", "Python", "Angular", "GitHub", "PostgreSQL"]
    experience = [
        {"role": "Student Developer", "company": "Google / U.S. Tech Collaboration", "period": "2023 — 2024",
         "desc": ["Розробка web-, database- та IoT-проєктів у співпраці з Google."]},
        {"role": "Full-Stack Developer (Hackathon Projects)", "company": "InnovateX Labs (California, USA)", "period": "2024 — now",
         "desc": ["Розробка full-stack прототипів у рамках хакатонів InnovateX Labs."]}
    ]
    return render_template(
        "resume.html",
        title=title, about=about, education=education,
        skills=skills, technologies=technologies, experience=experience
    )

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    title = "Контакти"
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Будь ласка, заповніть усі поля форми.", "danger")
        else:
            flash("Дякуємо! Повідомлення прийнято.", "success")
            return redirect(url_for("contacts"))
    return render_template("contacts.html", title=title)

if __name__ == "__main__":
    app.run(debug=True)
