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

api = Blueprint('api', __name__)

@api.route("/eth_price")
def eth_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "ethereum",
            "vs_currencies": "usd",
        }

        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Heroku Dyno)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": f"CoinGecko error: {response.status_code}"}), 500

        data = response.json()

        # Extra validation (Heroku sometimes gets empty JSON)
        if "ethereum" not in data or "usd" not in data["ethereum"]:
            return jsonify({"error": "Invalid data format from API"}), 500

        return jsonify({"eth_usd": data["ethereum"]["usd"]})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
