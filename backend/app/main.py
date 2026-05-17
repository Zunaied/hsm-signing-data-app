from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from app.services.openbao_service import (
    get_client_token,
    get_hsm_pin
)

from app.services.capability_service import (
    check_read_capability
)

from app.services.hsm_service import (
    sign_data,
    verify_signature
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# =========================
# REQUEST MODEL
# =========================
class UserData(BaseModel):
    name: str
    email: str
    signature: str | None = None


# =========================
# HOME
# =========================
@app.get("/")
def home():
    print("\n========== HOME PAGE ==========\n")
    return FileResponse("app/static/index.html")


# =========================
# SIGN
# =========================
@app.post("/sign")
def sign(user: UserData):

    print("\n========== SIGN START ==========\n")

    print(f"NAME: {user.name}")
    print(f"EMAIL: {user.email}")

    token = get_client_token()
    print(f"TOKEN: {token}")

    if not check_read_capability(token, "sign-key"):
        return {"status": "failed", "message": "No capability"}

    pin = get_hsm_pin(token)
    print(f"PIN: {pin}")

    result = sign_data(user.name, user.email, pin)

    print("\nSIGN RESULT:", result)
    print("\n========== SIGN END ==========\n")

    return result


# =========================
# VERIFY (NEW LOGIC)
# =========================
@app.post("/verify")
def verify(user: UserData):

    print("\n========== VERIFY START ==========\n")

    if not user.signature:
        return {"status": "failed", "message": "Signature missing"}

    print(f"NAME: {user.name}")
    print(f"EMAIL: {user.email}")
    print(f"OLD SIGNATURE: {user.signature}")

    token = get_client_token()

    if not check_read_capability(token, "sign-key"):
        return {"status": "failed", "message": "No capability"}

    pin = get_hsm_pin(token)

    # STEP 1: regenerate signature from HSM
    new_result = sign_data(user.name, user.email, pin)

    new_signature = new_result.get("signature")

    print("\nNEW SIGNATURE FROM HSM:", new_signature)

    # STEP 2: compare
    if new_signature == user.signature:
        print("MATCH FOUND → VALID SIGNATURE")
        return {"status": "success", "message": "Signature valid"}

    print("NO MATCH → INVALID SIGNATURE")
    return {"status": "failed", "message": "Invalid signature"}