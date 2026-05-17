import os
import requests

OPENBAO_ADDR = os.getenv("OPENBAO_ADDR")
OPENBAO_CERT = os.getenv("OPENBAO_CERT")

ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")


def get_client_token():

    url = f"{OPENBAO_ADDR}/v1/auth/approle/login"

    payload = {
        "role_id": ROLE_ID,
        "secret_id": SECRET_ID
    }

    response = requests.post(
        url,
        json=payload,
        verify=OPENBAO_CERT
    )

    data = response.json()

    return data["auth"]["client_token"]


def get_hsm_pin(token):

    url = f"{OPENBAO_ADDR}/v1/kv/hsm/data/hsm_pin"

    headers = {
        "X-Vault-Token": token
    }

    response = requests.get(
        url,
        headers=headers,
        verify=OPENBAO_CERT
    )

    data = response.json()

    return data["data"]["data"]["pin"]