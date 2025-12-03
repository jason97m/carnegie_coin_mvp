from flask import Blueprint, render_template, jsonify
from web3 import Web3
import os
from app.utils import get_balance
from app.utils import get_transfer_events
from dotenv import load_dotenv

main = Blueprint("main", __name__, template_folder="templates")

load_dotenv()

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
    # Connect to blockchain
    url = os.getenv("WEB3_PROVIDER")
    w3 = Web3(Web3.HTTPProvider(url))
    contract_address = os.getenv("CONTRACT_ADDRESS")

    print(contract_address)
    print("Connected:", w3.is_connected())
    print("Chain:", w3.eth.chain_id)
    print("Latest block:", w3.eth.block_number)

    # Example scholarships to pass to template
    scholarships = [
        {"name": "Scholarship A", "amount": 1000},
        {"name": "Scholarship B", "amount": 2000},
    ]

    return render_template("admin_dashboard.html", scholarships=scholarships, connected=w3.is_connected(),
        chain_id=w3.eth.chain_id,
        latest_block=w3.eth.block_number,
        contract_address=contract_address)

@main.route("/ledger")
def ledger():
    events = get_transfer_events()

    # Newest first
    events.sort(key=lambda x: x["block"], reverse=True)

    return render_template("ledger.html", events=events)
