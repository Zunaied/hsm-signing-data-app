# # import os
# # import json
# # import subprocess

# # SOFTHSM2_CONF = os.getenv("SOFTHSM2_CONF")
# # PKCS11_MODULE = os.getenv("PKCS11_MODULE")

# # SIGNED_DIR = "/app/app/signed"

# # ORIGINAL_DATA_FILE = f"{SIGNED_DIR}/original_data.txt"
# # VERIFY_DATA_FILE = f"{SIGNED_DIR}/verify_data.txt"
# # SIGNATURE_FILE = f"{SIGNED_DIR}/sig.bin"


# # def write_json_file(path, payload):

# #     os.makedirs(SIGNED_DIR, exist_ok=True)

# #     canonical_json = json.dumps(
# #         payload,
# #         separators=(",", ":"),
# #         sort_keys=True
# #     )

# #     with open(path, "w", encoding="utf-8") as f:
# #         f.write(canonical_json)

# #     print(f"DATA WRITTEN TO {path}: {canonical_json}")

# # def sign_data(name, email, pin):

# #     payload = {
# #         "name": name,
# #         "email": email
# #     }

# #     write_json_file(
# #         ORIGINAL_DATA_FILE,
# #         payload
# #     )

# #     command = [
# #         "pkcs11-tool",
# #         "--module", PKCS11_MODULE,
# #         "--login",
# #         "--pin", pin,
# #         "--sign",
# #         "--label", "sign-key",
# #         "--id", "01",
# #         "--mechanism", "SHA256-RSA-PKCS",
# #         "--input-file", ORIGINAL_DATA_FILE,
# #         "--output-file", SIGNATURE_FILE
# #     ]

# #     env = os.environ.copy()
# #     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

# #     result = subprocess.run(
# #         command,
# #         capture_output=True,
# #         text=True,
# #         env=env
# #     )

# #     if result.returncode == 0:

# #         return {
# #             "status": "success",
# #             "message": "Data signed successfully",
# #             "stdout": result.stdout
# #         }

# #     return {
# #         "status": "failed",
# #         "message": "Signing failed",
# #         "stderr": result.stderr
# #     }


# # def verify_signature(name, email, pin):

# #     if not os.path.exists(SIGNATURE_FILE):

# #         return {
# #             "status": "failed",
# #             "message": "No signature found. Please sign data first."
# #         }

# #     payload = {
# #         "name": name,
# #         "email": email
# #     }

# #     write_json_file(
# #         VERIFY_DATA_FILE,
# #         payload
# #     )

# #     command = [
# #         "pkcs11-tool",
# #         "--module", PKCS11_MODULE,
# #         "--login",
# #         "--pin", pin,
# #         "--verify",
# #         "--label", "sign-key",
# #         "--id", "01",
# #         "--mechanism", "SHA256-RSA-PKCS",
# #         "--input-file", VERIFY_DATA_FILE,
# #         "--signature-file", SIGNATURE_FILE
# #     ]

# #     env = os.environ.copy()
# #     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

# #     result = subprocess.run(
# #         command,
# #         capture_output=True,
# #         text=True,
# #         env=env
# #     )

# #     print("VERIFY STDOUT:", result.stdout)
# #     print("VERIFY STDERR:", result.stderr)

# #     stdout = result.stdout.lower()

# #     # SUCCESS CASE
# #     if "signature is valid" in stdout:

# #         return {
# #             "status": "success",
# #             "message": "Signature verified successfully"
# #         }

# #     # INVALID CASE
# #     if "invalid signature" in stdout:

# #         return {
# #             "status": "failed",
# #             "message": "INVALID SIGNATURE",
# #             "stderr": result.stderr
# #         }

# #     # FALLBACK
# #     return {
# #         "status": "failed",
# #         "message": "Verification failed",
# #         "stdout": result.stdout,
# #         "stderr": result.stderr
# #     }



# # # import os
# # # import json
# # # import base64
# # # import subprocess

# # # from app.database.db import SessionLocal
# # # from app.database.models import SignatureStore

# # # SOFTHSM2_CONF = os.getenv("SOFTHSM2_CONF")
# # # PKCS11_MODULE = os.getenv("PKCS11_MODULE")

# # # SIGNED_DIR = "/app/app/signed"

# # # ORIGINAL_DATA_FILE = f"{SIGNED_DIR}/original_data.txt"
# # # VERIFY_DATA_FILE = f"{SIGNED_DIR}/verify_data.txt"

# # # TEMP_SIGNATURE_FILE = f"{SIGNED_DIR}/temp_verify_sig.bin"


# # # def write_json_file(path, payload):

# # #     os.makedirs(SIGNED_DIR, exist_ok=True)

# # #     canonical_json = json.dumps(
# # #         payload,
# # #         separators=(",", ":"),
# # #         sort_keys=True
# # #     )

# # #     with open(path, "w", encoding="utf-8") as f:
# # #         f.write(canonical_json)

# # #     print(f"DATA WRITTEN TO {path}: {canonical_json}")


# # # def sign_data(name, email, pin):

# # #     payload = {
# # #         "name": name,
# # #         "email": email
# # #     }

# # #     write_json_file(
# # #         ORIGINAL_DATA_FILE,
# # #         payload
# # #     )

# # #     temp_sig_file = "/tmp/signature.bin"

# # #     command = [
# # #         "pkcs11-tool",
# # #         "--module", PKCS11_MODULE,
# # #         "--login",
# # #         "--pin", pin,
# # #         "--sign",
# # #         "--id", "01",
# # #         "--label", "sign-key",
# # #         "--mechanism", "SHA256-RSA-PKCS",
# # #         "--input-file", ORIGINAL_DATA_FILE,
# # #         "--output-file", temp_sig_file
# # #     ]

# # #     env = os.environ.copy()
# # #     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

# # #     result = subprocess.run(
# # #         command,
# # #         capture_output=True,
# # #         text=True,
# # #         env=env
# # #     )

# # #     if result.returncode != 0:

# # #         return {
# # #             "status": "failed",
# # #             "message": "Signing failed",
# # #             "stderr": result.stderr
# # #         }

# # #     with open(temp_sig_file, "rb") as f:
# # #         signature_bytes = f.read()

# # #     signature_base64 = base64.b64encode(
# # #         signature_bytes
# # #     ).decode()

# # #     db = SessionLocal()

# # #     db_record = SignatureStore(
# # #         name=name,
# # #         email=email,
# # #         signature_base64=signature_base64
# # #     )

# # #     db.add(db_record)
# # #     db.commit()

# # #     os.remove(temp_sig_file)

# # #     return {
# # #         "status": "success",
# # #         "message": "Data signed successfully and stored in database"
# # #     }


# # # def verify_signature(name, email, pin):

# # #     payload = {
# # #         "name": name,
# # #         "email": email
# # #     }

# # #     write_json_file(
# # #         VERIFY_DATA_FILE,
# # #         payload
# # #     )

# # #     db = SessionLocal()

# # #     record = db.query(SignatureStore).filter(
# # #         SignatureStore.name == name,
# # #         SignatureStore.email == email
# # #     ).order_by(
# # #         SignatureStore.id.desc()
# # #     ).first()

# # #     if not record:

# # #         return {
# # #             "status": "failed",
# # #             "message": "No signature found in database"
# # #         }

# # #     signature_bytes = base64.b64decode(
# # #         record.signature_base64
# # #     )

# # #     with open(TEMP_SIGNATURE_FILE, "wb") as f:
# # #         f.write(signature_bytes)

# # #     command = [
# # #         "pkcs11-tool",
# # #         "--module", PKCS11_MODULE,
# # #         "--login",
# # #         "--pin", pin,
# # #         "--verify",
# # #         "--id", "01",
# # #         "--label", "sign-key",
# # #         "--mechanism", "SHA256-RSA-PKCS",
# # #         "--input-file", VERIFY_DATA_FILE,
# # #         "--signature-file", TEMP_SIGNATURE_FILE
# # #     ]

# # #     env = os.environ.copy()
# # #     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

# # #     result = subprocess.run(
# # #         command,
# # #         capture_output=True,
# # #         text=True,
# # #         env=env
# # #     )

# # #     print("VERIFY STDOUT:", result.stdout)

# # #     stdout = result.stdout.lower()

# # #     if "signature is valid" in stdout:

# # #         return {
# # #             "status": "success",
# # #             "message": "Signature verified successfully"
# # #         }

# # #     return {
# # #         "status": "failed",
# # #         "message": "INVALID SIGNATURE"
# # #     }






# import os
# import json
# import base64
# import subprocess

# SOFTHSM2_CONF = os.getenv("SOFTHSM2_CONF")
# PKCS11_MODULE = os.getenv("PKCS11_MODULE")

# SIGNED_DIR = "/app/app/signed"

# ORIGINAL_DATA_FILE = f"{SIGNED_DIR}/original_data.txt"
# VERIFY_DATA_FILE = f"{SIGNED_DIR}/verify_data.txt"
# SIGNATURE_FILE = f"{SIGNED_DIR}/sig.bin"


# def write_json_file(path, payload):

#     os.makedirs(SIGNED_DIR, exist_ok=True)

#     canonical_json = json.dumps(
#         payload,
#         separators=(",", ":"),
#         sort_keys=True
#     )

#     with open(path, "w", encoding="utf-8") as f:
#         f.write(canonical_json)

#     print(f"\nDATA WRITTEN TO {path}")
#     print(canonical_json)

#     return canonical_json


# def sign_data(name, email, pin):

#     print("\n========== SIGNING PROCESS START ==========\n")

#     payload = {
#         "name": name,
#         "email": email
#     }

#     write_json_file(
#         ORIGINAL_DATA_FILE,
#         payload
#     )

#     command = [
#         "pkcs11-tool",
#         "--module", PKCS11_MODULE,
#         "--login",
#         "--pin", pin,
#         "--sign",
#         "--label", "sign-key",
#         "--id", "01",
#         "--mechanism", "SHA256-RSA-PKCS",
#         "--input-file", ORIGINAL_DATA_FILE,
#         "--output-file", SIGNATURE_FILE
#     ]

#     print("\nPKCS11 COMMAND:")
#     print(" ".join(command))

#     env = os.environ.copy()
#     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

#     result = subprocess.run(
#         command,
#         capture_output=True,
#         text=True,
#         env=env
#     )

#     print("\n========== SOFTHSM SIGN OUTPUT ==========\n")

#     print("STDOUT:")
#     print(result.stdout)

#     print("\nSTDERR:")
#     print(result.stderr)

#     print("\nRETURN CODE:")
#     print(result.returncode)

#     print("\n=========================================\n")

#     if result.returncode != 0:

#         return {
#             "status": "failed",
#             "message": "Signing failed",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         }

#     if not os.path.exists(SIGNATURE_FILE):

#         return {
#             "status": "failed",
#             "message": "Signature file not generated"
#         }

#     with open(SIGNATURE_FILE, "rb") as f:

#         signature_bytes = f.read()

#     signature_base64 = base64.b64encode(
#         signature_bytes
#     ).decode()

#     print("\nSIGNATURE BASE64:\n")
#     print(signature_base64)

#     print("\n========== SIGNING PROCESS END ==========\n")

#     return {
#         "status": "success",
#         "message": "Data signed successfully",
#         "signature": signature_base64,
#         "stdout": result.stdout,
#         "stderr": result.stderr
#     }


# def verify_signature(name, email, signature_base64, pin):

#     print("\n========== VERIFICATION PROCESS START ==========\n")

#     payload = {
#         "name": name,
#         "email": email
#     }

#     write_json_file(
#         VERIFY_DATA_FILE,
#         payload
#     )

#     try:

#         signature_bytes = base64.b64decode(
#             signature_base64
#         )

#     except Exception as e:

#         return {
#             "status": "failed",
#             "message": f"Base64 decode failed: {str(e)}"
#         }

#     with open(SIGNATURE_FILE, "wb") as f:

#         f.write(signature_bytes)

#     print("\nBASE64 SIGNATURE DECODED")
#     print(f"Signature written to: {SIGNATURE_FILE}")

#     command = [
#         "pkcs11-tool",
#         "--module", PKCS11_MODULE,
#         "--login",
#         "--pin", pin,
#         "--verify",
#         "--label", "sign-key",
#         "--id", "01",
#         "--mechanism", "SHA256-RSA-PKCS",
#         "--input-file", VERIFY_DATA_FILE,
#         "--signature-file", SIGNATURE_FILE
#     ]

#     print("\nPKCS11 COMMAND:")
#     print(" ".join(command))

#     env = os.environ.copy()
#     env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

#     result = subprocess.run(
#         command,
#         capture_output=True,
#         text=True,
#         env=env
#     )

#     print("\n========== SOFTHSM VERIFY OUTPUT ==========\n")

#     print("STDOUT:")
#     print(result.stdout)

#     print("\nSTDERR:")
#     print(result.stderr)

#     print("\nRETURN CODE:")
#     print(result.returncode)

#     print("\n===========================================\n")

#     stdout = result.stdout.lower()

#     if "signature is valid" in stdout:

#         print("\nFINAL RESULT: SIGNATURE VALID\n")

#         return {
#             "status": "success",
#             "message": "Signature verified successfully",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         }

#     if "invalid signature" in stdout:

#         print("\nFINAL RESULT: INVALID SIGNATURE\n")

#         return {
#             "status": "failed",
#             "message": "INVALID SIGNATURE",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         }

#     print("\nFINAL RESULT: UNKNOWN VERIFICATION FAILURE\n")

#     return {
#         "status": "failed",
#         "message": "Verification failed",
#         "stdout": result.stdout,
#         "stderr": result.stderr
#     }



import os
import json
import base64
import subprocess

SOFTHSM2_CONF = os.getenv("SOFTHSM2_CONF")
PKCS11_MODULE = os.getenv("PKCS11_MODULE")

SIGNED_DIR = "/app/app/signed"

ORIGINAL_DATA_FILE = f"{SIGNED_DIR}/original_data.txt"
VERIFY_DATA_FILE = f"{SIGNED_DIR}/verify_data.txt"
SIGNATURE_FILE = f"{SIGNED_DIR}/sig.bin"


def write_json_file(path, payload):

    os.makedirs(SIGNED_DIR, exist_ok=True)

    canonical_json = json.dumps(
        payload,
        separators=(",", ":"),
        sort_keys=True
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(canonical_json)

    print(f"\nDATA WRITTEN TO {path}")
    print(canonical_json)


# ============================================================================
# SIGN FUNCTION
# ============================================================================

def sign_data(name, email, pin):

    print("\n========== SIGNING PROCESS START ==========\n")

    payload = {
        "name": name,
        "email": email
    }

    write_json_file(
        ORIGINAL_DATA_FILE,
        payload
    )

    command = [
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

    print("\nPKCS11 COMMAND:")
    print(" ".join(command))

    env = os.environ.copy()
    env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env
    )

    print("\n========== SOFTHSM SIGN OUTPUT ==========\n")

    print("STDOUT:")
    print(result.stdout)

    print("\nSTDERR:")
    print(result.stderr)

    print("\nRETURN CODE:")
    print(result.returncode)

    print("\n=========================================\n")

    if result.returncode != 0:

        return {
            "status": "failed",
            "message": "Signing failed",
            "stderr": result.stderr
        }

    # ----------------------------------------------------------------------
    # Convert signature binary -> Base64
    # ----------------------------------------------------------------------

    with open(SIGNATURE_FILE, "rb") as f:

        signature_base64 = base64.b64encode(
            f.read()
        ).decode()

    print("\nSIGNATURE BASE64:\n")
    print(signature_base64)

    print("\n========== SIGNING PROCESS END ==========\n")

    return {
        "status": "success",
        "message": "Data signed successfully",
        "signature": signature_base64,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


# ============================================================================
# VERIFY FUNCTION
# ============================================================================

def verify_signature(name, email, signature_base64, pin):

    print("\n========== VERIFICATION PROCESS START ==========\n")

    payload = {
        "name": name,
        "email": email
    }

    write_json_file(
        VERIFY_DATA_FILE,
        payload
    )

    # ----------------------------------------------------------------------
    # Decode Base64 signature
    # ----------------------------------------------------------------------

    try:

        signature_bytes = base64.b64decode(
            signature_base64
        )

    except Exception as e:

        return {
            "status": "failed",
            "message": f"Invalid Base64 signature: {str(e)}"
        }

    # ----------------------------------------------------------------------
    # Save binary signature temporarily
    # ----------------------------------------------------------------------

    with open(SIGNATURE_FILE, "wb") as f:

        f.write(signature_bytes)

    print("\nBASE64 SIGNATURE DECODED SUCCESSFULLY")

    # ----------------------------------------------------------------------
    # PKCS11 VERIFY COMMAND
    # ----------------------------------------------------------------------

    command = [
        "pkcs11-tool",
        "--module", PKCS11_MODULE,
        "--login",
        "--pin", pin,
        "--verify",
        "--label", "sign-key",
        "--id", "01",
        "--mechanism", "SHA256-RSA-PKCS",
        "--input-file", VERIFY_DATA_FILE,
        "--signature-file", SIGNATURE_FILE
    ]

    print("\nPKCS11 VERIFY COMMAND:")
    print(" ".join(command))

    env = os.environ.copy()
    env["SOFTHSM2_CONF"] = SOFTHSM2_CONF

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env
    )

    print("\n========== SOFTHSM VERIFY OUTPUT ==========\n")

    print("STDOUT:")
    print(result.stdout)

    print("\nSTDERR:")
    print(result.stderr)

    print("\nRETURN CODE:")
    print(result.returncode)

    print("\n===========================================\n")

    combined_output = (
        result.stdout +
        result.stderr
    ).lower()

    # ----------------------------------------------------------------------
    # SUCCESS
    # ----------------------------------------------------------------------

    if "signature is valid" in combined_output:

        return {
            "status": "success",
            "message": "Signature verified successfully",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    # ----------------------------------------------------------------------
    # INVALID SIGNATURE
    # ----------------------------------------------------------------------

    if (
        "invalid signature" in combined_output
        or result.returncode != 0
    ):

        return {
            "status": "failed",
            "message": "INVALID SIGNATURE",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    # ----------------------------------------------------------------------
    # FALLBACK
    # ----------------------------------------------------------------------

    return {
        "status": "failed",
        "message": "Verification failed",
        "stdout": result.stdout,
        "stderr": result.stderr
    }