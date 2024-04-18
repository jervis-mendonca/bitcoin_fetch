import os
import json
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

# Format: {timestamp: {"BTC-CZK": price, "BTC-EUR": price}}
stored_data = {}

# Valid API keys (replace with your actual keys)
VALID_API_KEYS = ["your-api-key-1", "your-api-key-2"]

def calculate_daily_average(prices):
    return sum(prices) / len(prices)

def calculate_monthly_average(prices):
    return sum(prices) / 30  # Assuming 30 days in a month


BASE_URL = "https://www.google.com/finance"
SYMBOLS = ["BTC-CZK", "BTC-EUR"]
LANGUAGE = "en"

def get_bitcoin_price(symbol):
    target_url = f"{BASE_URL}/quote/{symbol}?hl={LANGUAGE}"
    page = requests.get(target_url)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", {"class": "gyFHrc"})

    stock_description = {}
    for item in items:
        item_description = item.find("div", {"class": "mfs7Fc"}).text
        item_value = item.find("div", {"class": "P6K39c"}).text
        stock_description[item_description] = item_value

    return stock_description

def store_data():
    start_time = int(time.time())
    end_time = start_time + 365 * 24 * 60 * 60  # 365 days in seconds
    daily_prices_czk = []
    daily_prices_eur = []

    while True:
        client_request_time = int(time.time())
        btc_czk_price = get_bitcoin_price("BTC-CZK")
        btc_eur_price = get_bitcoin_price("BTC-EUR")

        # Store data in the locally stored dictionary
        stored_data[client_request_time] = {"BTC-CZK": btc_czk_price, "BTC-EUR": btc_eur_price}

        # Check if 365 days have passed
        if client_request_time >= end_time:
            break

        # Sleep for 5 minutes (adjust as needed)
        time.sleep(300)

        monthly_average_czk = calculate_monthly_average(daily_prices_czk)
        monthly_average_eur = calculate_monthly_average(daily_prices_eur)

        print(f"Daily Average (CZK): {daily_average_czk}")
        print(f"Daily Average (EUR): {daily_average_eur}")
        print(f"Monthly Average (CZK): {monthly_average_czk}")
        print(f"Monthly Average (EUR): {monthly_average_eur}")

        with open("stored_bitcoin_data.txt", "w") as file:
            json.dump(stored_data, file)

@app.route('/bitcoin', methods=['GET'])
def bitcoin_prices():
    try:
        api_key = request.headers.get("X-API-Key")
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Invalid API key."}), 401

        client_request_time = int(time.time())
        btc_czk_price = stored_data.get(client_request_time, {}).get("BTC-CZK")
        btc_eur_price = stored_data.get(client_request_time, {}).get("BTC-EUR")

        if btc_czk_price is not None and btc_eur_price is not None:
            response_data = {
                "client_request_time": client_request_time,
                "server_data_time": int(time.time()),
                "BTC-CZK": btc_czk_price,
                "BTC-EUR": btc_eur_price
            }
            return jsonify(response_data)
        else:
            return jsonify({"error": "Bitcoin data not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    # Set FLASK_APP environment variable to run the app
    os.environ["FLASK_APP"] = "bitcoin_microservice.py"

    # Start the data retention loop
    store_data()
