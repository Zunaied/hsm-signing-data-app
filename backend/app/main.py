# # from fastapi import FastAPI
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.responses import FileResponse
# # from pydantic import BaseModel

# # from dotenv import load_dotenv

# # # from app.database.db import engine
# # # from app.database.models import Base




# # load_dotenv()

# # from app.services.openbao_service import (
# #     get_client_token,
# #     get_hsm_pin
# # )

# # from app.services.capability_service import (
# #     check_read_capability
# # )

# # from app.services.hsm_service import (
# #     sign_data,
# #     verify_signature
# # )
# # # Base.metadata.create_all(bind=engine) 

# # app = FastAPI()

# # app.mount("/static", StaticFiles(directory="app/static"), name="static")


# # class UserData(BaseModel):
# #     name: str
# #     email: str


# # @app.get("/")
# # def home():
# #     return FileResponse("app/static/index.html")


# # @app.post("/sign")
# # def sign(user: UserData):

# #     token = get_client_token()

# #     capability = check_read_capability(
# #         token,
# #         "sign-key"
# #     )

# #     if not capability:
# #         return {
# #             "status": "failed",
# #             "message": "Try again. Token has no read capability."
# #         }

# #     pin = get_hsm_pin(token)

# #     result = sign_data(
# #         user.name,
# #         user.email,
# #         pin
# #     )

# #     return result


# # @app.post("/verify")
# # def verify(user: UserData):

# #     token = get_client_token()

# #     capability = check_read_capability(
# #         token,
# #         "sign-key"
# #     )

# #     if not capability:
# #         return {
# #             "status": "failed",
# #             "message": "Try again. Token has no read capability."
# #         }

# #     pin = get_hsm_pin(token)

# #     result = verify_signature(
# #         user.name,
# #         user.email,
# #         request.signature,
# #         pin
# #     )

# #     return result




# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel

# from dotenv import load_dotenv

# load_dotenv()

# from app.services.openbao_service import (
#     get_client_token,
#     get_hsm_pin
# )

# from app.services.capability_service import (
#     check_read_capability
# )

# from app.services.hsm_service import (
#     sign_data,
#     verify_signature
# )

# app = FastAPI()

# app.mount(
#     "/static",
#     StaticFiles(directory="app/static"),
#     name="static"
# )


# class UserData(BaseModel):
#     name: str
#     email: str
#     signature: str | None = None


# @app.get("/")
# def home():

#     print("\n========== HOME PAGE REQUEST ==========\n")

#     return FileResponse("app/static/index.html")


# @app.post("/sign")
# def sign(user: UserData):

#     print("\n========== SIGN REQUEST START ==========\n")

#     print("Incoming User Data:")
#     print(f"NAME  : {user.name}")
#     print(f"EMAIL : {user.email}")

#     print("\n[1] Requesting OpenBao client token...")

#     token = get_client_token()

#     print("CLIENT TOKEN RECEIVED:")
#     print(token)

#     print("\n[2] Checking read capability for sign-key...")

#     capability = check_read_capability(
#         token,
#         "sign-key"
#     )

#     print("CAPABILITY RESULT:")
#     print(capability)

#     if not capability:

#         print("\nACCESS DENIED")

#         return {
#             "status": "failed",
#             "message": "Try again. Token has no read capability."
#         }

#     print("\n[3] Fetching HSM PIN from OpenBao KV...")

#     pin = get_hsm_pin(token)

#     print("PIN RECEIVED:")
#     print(pin)

#     print("\n[4] Starting SoftHSM signing operation...")

#     result = sign_data(
#         user.name,
#         user.email,
#         pin
#     )

#     print("\nSIGN RESULT:")
#     print(result)

#     print("\n========== SIGN REQUEST END ==========\n")

#     return result


# @app.post("/verify")
# def verify(user: UserData):

#     print("\n========== VERIFY REQUEST START ==========\n")

#     print("Incoming Verification Data:")
#     print(f"NAME      : {user.name}")
#     print(f"EMAIL     : {user.email}")

#     if user.signature:

#         print(f"SIGNATURE LENGTH : {len(user.signature)}")

#     else:

#         print("SIGNATURE : MISSING")

#     if not user.signature:

#         print("\nVERIFY FAILED - SIGNATURE MISSING")

#         return {
#             "status": "failed",
#             "message": "Signature is missing"
#         }

#     print("\n[1] Requesting OpenBao client token...")

#     token = get_client_token()

#     print("CLIENT TOKEN RECEIVED:")
#     print(token)

#     print("\n[2] Checking read capability for sign-key...")

#     capability = check_read_capability(
#         token,
#         "sign-key"
#     )

#     print("CAPABILITY RESULT:")
#     print(capability)

#     if not capability:

#         print("\nACCESS DENIED")

#         return {
#             "status": "failed",
#             "message": "Try again. Token has no read capability."
#         }

#     print("\n[3] Fetching HSM PIN from OpenBao KV...")

#     pin = get_hsm_pin(token)

#     print("PIN RECEIVED:")
#     print(pin)

#     print("\n[4] Starting SoftHSM verification operation...")

#     result = verify_signature(
#         user.name,
#         user.email,
#         user.signature,
#         pin
#     )

#     print("\nVERIFY RESULT:")
#     print(result)

#     print("\n========== VERIFY REQUEST END ==========\n")

#     return result
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


# ===============================
# STATIC FILES
# ===============================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ===============================
# REQUEST MODEL
# ===============================

class UserData(BaseModel):
    name: str
    email: str
    signature: str | None = None


# ===============================
# HOME PAGE
# ===============================

@app.get("/")
def home():

    print("\n========== HOME PAGE REQUEST ==========\n")

    return FileResponse("app/static/index.html")


# ===============================
# SIGN API
# ===============================

@app.post("/sign")
def sign(user: UserData):

    print("\n========== SIGN REQUEST START ==========\n")

    print("Incoming User Data:")
    print(f"NAME  : {user.name}")
    print(f"EMAIL : {user.email}")

    # STEP 1
    print("\n[1] Requesting OpenBao client token...")

    token = get_client_token()

    print("CLIENT TOKEN:")
    print(token)

    # STEP 2
    print("\n[2] Checking OpenBao capability...")

    capability = check_read_capability(
        token,
        "sign-key"
    )

    print("CAPABILITY RESULT:")
    print(capability)

    if not capability:

        print("\nACCESS DENIED")

        return {
            "status": "failed",
            "message": "Token has no permission"
        }

    # STEP 3
    print("\n[3] Fetching HSM PIN from OpenBao...")

    pin = get_hsm_pin(token)

    print("PIN RECEIVED:")
    print(pin)

    # STEP 4
    print("\n[4] Starting HSM Signing Process...")

    result = sign_data(
        user.name,
        user.email,
        pin
    )

    print("\nSIGN RESULT:")
    print(result)

    print("\n========== SIGN REQUEST END ==========\n")

    return result


# ===============================
# VERIFY API
# ===============================

@app.post("/verify")
def verify(user: UserData):

    print("\n========== VERIFY REQUEST START ==========\n")

    print("Incoming Verification Data:")
    print(f"NAME      : {user.name}")
    print(f"EMAIL     : {user.email}")

    if user.signature:
        print(f"SIGNATURE LENGTH : {len(user.signature)}")
    else:
        print("SIGNATURE : MISSING")

    # CHECK SIGNATURE
    if not user.signature:

        print("\nVERIFY FAILED - SIGNATURE MISSING")

        return {
            "status": "failed",
            "message": "Signature is required"
        }

    # STEP 1
    print("\n[1] Requesting OpenBao client token...")

    token = get_client_token()

    print("CLIENT TOKEN:")
    print(token)

    # STEP 2
    print("\n[2] Checking OpenBao capability...")

    capability = check_read_capability(
        token,
        "sign-key"
    )

    print("CAPABILITY RESULT:")
    print(capability)

    if not capability:

        print("\nACCESS DENIED")

        return {
            "status": "failed",
            "message": "Token has no permission"
        }

    # STEP 3
    print("\n[3] Fetching HSM PIN from OpenBao...")

    pin = get_hsm_pin(token)

    print("PIN RECEIVED:")
    print(pin)

    # STEP 4
    print("\n[4] Starting Verification Process...")

    result = verify_signature(
        user.name,
        user.email,
        user.signature,
        pin
    )

    print("\nVERIFY RESULT:")
    print(result)

    print("\n========== VERIFY REQUEST END ==========\n")

    return result