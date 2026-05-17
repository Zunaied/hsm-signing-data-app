import os
import json
import subprocess
import base64

SOFTHSM2_CONF = os.getenv("SOFTHSM2_CONF")
PKCS11_MODULE = os.getenv("PKCS11_MODULE")

SIGNED_DIR = "/app/app/signed"

ORIGINAL_DATA_FILE = f"{SIGNED_DIR}/original_data.txt"
SIGNATURE_FILE = f"{SIGNED_DIR}/sig.bin"


# =========================
# WRITE CLEAN JSON
# =========================
def write_json_file(path, payload):

    os.makedirs(SIGNED_DIR, exist_ok=True)

    data = json.dumps(payload, sort_keys=True, separators=(",", ":"))

    with open(path, "w") as f:
        f.write(data)

    print(f"DATA WRITTEN: {data}")


# =========================
# SIGN DATA
# =========================
def sign_data(name, email, pin):

    payload = {"name": name, "email": email}

    write_json_file(ORIGINAL_DATA_FILE, payload)

    cmd = [
        "pkcs11-tool",
        "--module", PKCS11_MODULE,
        "--login",
        "--pin", pin,
        "--sign",
        "--label", "sign-key",
        "--id", "01",
        "--mechanism", "SHA256-RSA-PKCS",
        "--input-file", ORIGINAL_DATA_FILE,
        "--output-file", SIGNATURE_FILE
    ]

    print("\nPKCS11 SIGN COMMAND:", " ".join(cmd))

    env = os.environ.copy()
    env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    # read binary signature
    with open(SIGNATURE_FILE, "rb") as f:
        raw_sig = f.read()

    b64_sig = base64.b64encode(raw_sig).decode()

    print("\nBASE64 SIGNATURE:", b64_sig)

    return {
        "status": "success",
        "signature": b64_sig,
        "stderr": result.stderr
    }


# =========================
# VERIFY (NOT USING HSM VERIFY)
# =========================
def verify_signature(name, email, signature, pin):

    # regenerate signature again
    result = sign_data(name, email, pin)

    return result