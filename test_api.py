import uuid
import os
import requests

base_url = os.getenv("base_url")
wallet_name = f"{uuid.uuid4()}"
valid_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
invalid_address = "2NGZrVvZG92qGYqzTLjCAewvPZ7JE8S8VxE"
api_token = "928a33760c87f8fa19b8b0d8825b2f98c5a0fbdf56997627b5b64df88d773c75"


class TestAPI:
    def test_create_wallet(self):
        url = base_url + "wallets"
        headers = {"Content-Type": "application/json",
                   "Authorization": f"{api_token}",
                   "Idempotency-Key": f"{uuid.uuid4()}"}
        json = {"name": wallet_name,
                "currency": "BTC",
                "human": "Crypto BTC",
                "description": "For inner use of the new crypto-exchange"}
        response = requests.post(url=url, headers=headers, json=json)
        data = response.json()["data"]
        assert response.status_code == 201
        assert data["id"]
        assert data["name"] == wallet_name
        assert data["currency"] == "BTC"
        assert data["human"] == "Crypto BTC"
        assert data["description"] == "For inner use of the new crypto-exchange"
        assert data["system_fee_percent"] == "1.0"
        assert data["merchant_fee_percent"] == "0.0"
        assert data["created_at"]
        assert data["updated_at"]

    def test_valid_address(self):
        url = base_url + f"validate/eth/{valid_address}"
        response = requests.get(url=url)
        data = response.json()["data"]
        assert data["is_valid"]

    def test_invalid_address(self):
        url = base_url + f"validate/btc/{valid_address}"
        response = requests.get(url=url)
        data = response.json()["data"]
        assert not data["is_valid"]
