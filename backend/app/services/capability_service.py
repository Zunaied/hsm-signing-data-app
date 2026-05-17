import os
import requests

OPENBAO_ADDR = os.getenv("OPENBAO_ADDR")
OPENBAO_CERT = os.getenv("OPENBAO_CERT")


def check_read_capability(token, key_label):

    path = f"demo/keys/{key_label}"

    url = f"{OPENBAO_ADDR}/v1/sys/capabilities-self"

    headers = {
        "X-Vault-Token": token
    }

    payload = {
        "paths": [path]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        verify=OPENBAO_CERT
    )

    data = response.json()

    capabilities = data["capabilities"]

    return "read" in capabilities