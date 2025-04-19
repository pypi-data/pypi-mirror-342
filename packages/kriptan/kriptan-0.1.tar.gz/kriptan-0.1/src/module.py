import requests

def get_crypto_price(coin_id: str, currency: str = "usd"):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Проверка на ошибки HTTP
    data = response.json()

    if coin_id in data and currency in data[coin_id]:
        return {
            "coin_id": coin_id,
            "currency": currency.upper(),
            "price": data[coin_id][currency]
        }
    else:
        return {"error": "Криптовалюта или валюта не найдены."}
