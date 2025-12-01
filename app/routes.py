from flask import Blueprint, render_template, jsonify
import os
from app.utils import get_balance

main = Blueprint("main", __name__, template_folder="templates")

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/educator")
def educator_dashboard():
    balance = get_balance()  # real token balance
    return render_template("educator_dashboard.html", balance=balance)

@main.route("/student")
def student_dashboard():
    grades = {"Math": 95, "Science": 88, "History": 92}
    return render_template("student_dashboard.html", grades=grades)

@main.route("/finance")
def finance_dashboard():
    tuition_due = 5000
    school_balance = get_balance()
    return render_template("finance_dashboard.html", tuition_due=tuition_due)

@main.route("/admin")
def admin_dashboard():
    scholarships = [{"name": "Alice", "amount": 1000}, {"name": "Bob", "amount": 1500}]
    return render_template("admin_dashboard.html", scholarships=scholarships)

@main.route("/ledger")
def ledger():
    entries = get_transfer_events()

    # Newest first
    entries.sort(key=lambda x: x["block"], reverse=True)

    return render_template("ledger.html", entries=entries)
