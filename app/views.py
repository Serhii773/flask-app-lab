# app/views.py
import logging

from app import app
from flask import render_template, url_for, request, flash, redirect, current_app

from app.forms import ContactForm

contact_logger = logging.getLogger("contact_form")

if not contact_logger.handlers:
    file_handler = logging.FileHandler("contact.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    contact_logger.addHandler(file_handler)
    contact_logger.setLevel(logging.INFO)

@app.route("/")
def home():
    return redirect(url_for("resume"))


@app.route("/resume")
def resume():
    title = "Резюме"
    about = (
        "Full-Stack розробник із досвідом створення web-додатків, баз даних і IoT-проєктів. "
        "Працював у співпраці з Google над академічними ініціативами та розробляю full-stack рішення "
        "в рамках хакатонів InnovateX Labs (США). "
    )
    education = [
        {
            "school": "Stanford University",
            "program": "Software Engineering",
            "period": "2021 — 2023",
        }
    ]
    skills = [
        "Python (Flask, REST API, Jinja2)",
        "Java (OOP, Spring basics)",
        "Frontend: Angular, TypeScript, HTML5, CSS3, Bootstrap 5, Tailwind",
        "Databases: SQL (Oracle, PostgreSQL, MySQL)",
        "Algorithms & Data Structures",
        "Docker (Basics), Linux (CLI)",
    ]
    technologies = ["Flask", "Python", "Angular", "GitHub", "PostgreSQL"]
    experience = [
        {
            "role": "Student Developer",
            "company": "Google / U.S. Tech Collaboration",
            "period": "2023 — 2024",
            "desc": [
                "Розробка web-, database- та IoT-проєктів у співпраці з Google."
            ],
        },
        {
            "role": "Full-Stack Developer (Hackathon Projects)",
            "company": "InnovateX Labs (California, USA)",
            "period": "2024 — now",
            "desc": [
                "Розробка full-stack прототипів у рамках хакатонів InnovateX Labs."
            ],
        },
    ]
    return render_template(
        "resume.html",
        title=title,
        about=about,
        education=education,
        skills=skills,
        technologies=technologies,
        experience=experience,
    )

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    title = "Контакти"
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        try:
            contact_logger.info(
                "Contact form submitted: name=%s, email=%s, phone=%s, subject=%s, message=%s",
                name,
                email,
                phone,
                subject,
                message,
            )

            flash(
                f"Дякуємо, {name}! Повідомлення успішно відправлено. "
                f"Ми зв'яжемося з вами на {email}.",
                "success",
            )
        except Exception as exc:
            current_app.logger.exception("Помилка при записі у contact.log: %s", exc)
            flash(
                "Сталася помилка при відправці форми. Спробуйте, будь ласка, пізніше.",
                "danger",
            )

        return redirect(url_for("contacts"))

    return render_template("contacts.html", title=title, form=form)
