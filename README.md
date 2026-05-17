
# 📌 OpenBao + SoftHSM Signing & Verification System (Detailed Documentation)

---

## 🧾 Project Overview

This project implements a **secure digital signing and verification system** using a software-based Hardware Security Module (HSM).

It demonstrates a real-world architecture where cryptographic operations are fully isolated inside an HSM boundary and never handled directly by the application.

### 🔐 Core Idea
> The application does NOT perform cryptography.  
> All signing and verification happens inside SoftHSM via PKCS#11.

---

## 🏗️ System Architecture

```
            ┌────────────────────────────┐
            │        Frontend UI         │
            │   (HTML / CSS / JS)        │
            └────────────┬───────────────┘
                         │ REST API
                         ▼
            ┌────────────────────────────┐
            │     FastAPI Backend        │
            │  (Orchestration Layer)     │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │        OpenBao             │
            │  - Auth & Policies         │
            │  - HSM PIN Storage         │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │     PKCS#11 Interface      │
            │   (libsofthsm2.so)         │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │        SoftHSM2            │
            │  - Key Storage             │
            │  - Sign / Verify Ops       │
            └────────────────────────────┘
```

---

## ⚙️ Tech Stack

- FastAPI (Backend API)
- JavaScript (Frontend logic)
- HTML/CSS (UI)
- SoftHSM2 (Software HSM)
- OpenBao (Secrets + Policy engine)
- PKCS#11 (`pkcs11-tool`, libsofthsm2)
- Docker (Containerization)

---

## 🔄 System Flow

---

## 🔐 1. Signing Flow

### Step-by-step:

1. User submits:
```json
{
  "name": "rafee",
  "email": "user@gmail.com"
}
```

2. Backend:
- Requests OpenBao token
- Validates policy permission
- Fetches HSM PIN securely

3. Data handling:
- Data written to file (`original_data.txt`)
- Sent to SoftHSM via PKCS#11

4. SoftHSM:
- Generates RSA signature internally
- Returns binary signature

5. Application:
- Encodes signature in Base64
- Returns response to frontend

---

## 🔍 2. Verification Flow (REAL CRYPTOGRAPHIC FLOW)

### Step-by-step:

1. User sends:
```json
{
  "name": "rafee",
  "email": "user@gmail.com",
  "signature": "BASE64_STRING"
}
```

2. Backend:
- Decodes Base64 signature → binary
- Sends SAME data to SoftHSM

3. SoftHSM:
- Uses public key stored in token
- Performs cryptographic verification

4. Result:
- ✔ Valid signature → SUCCESS
- ❌ Invalid signature → FAIL

---

## 🔐 Security Model

### ✔ What is secured?

- Private keys NEVER leave SoftHSM
- PIN is stored in OpenBao (not hardcoded)
- All cryptographic operations happen inside PKCS#11 boundary

### ❌ What is NOT done?

- No manual crypto verification in backend
- No re-signing comparison logic
- No application-level signature validation

---

## 📂 Project Structure

```
openbao-hsm-signing-app/
│
├── app/
│   ├── main.py
│   ├── services/
│   │   ├── hsm_service.py
│   │   ├── openbao_service.py
│   │   ├── capability_service.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   ├── app.js
│   │   ├── style.css
│   │
│   ├── signed/
│       ├── original_data.txt
│       ├── verify_data.txt
│       ├── sig.bin
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🚀 API Endpoints

---

### 🔹 SIGN

`POST /sign`

Request:
```json
{
  "name": "string",
  "email": "string"
}
```

Response:
```json
{
  "status": "success",
  "signature": "BASE64_SIGNATURE"
}
```

---

### 🔹 VERIFY

`POST /verify`

Request:
```json
{
  "name": "string",
  "email": "string",
  "signature": "BASE64_SIGNATURE"
}
```

Response:
```json
{
  "status": "success",
  "message": "Signature verified successfully"
}
```

---

## 🔐 OpenBao Role

OpenBao is used for:

- Authentication token generation
- Policy-based access control
- Secure retrieval of HSM PIN
- Preventing direct exposure of sensitive credentials

---

## 🧠 Key Design Principles

### 1. Separation of Concerns
- App handles API logic
- SoftHSM handles cryptography
- OpenBao handles secrets

### 2. Zero Trust for Application Layer
- App never trusts or modifies crypto results
- All trust is delegated to HSM

### 3. Hardware-like Security Simulation
SoftHSM behaves like a real hardware HSM.

---

## 📊 Logging System

Every request includes:

- Token generation logs
- Capability checks
- PIN retrieval logs
- PKCS#11 command execution logs
- Signature output logs

---

## 📌 Summary

This system demonstrates a full **HSM-backed signing architecture**:

✔ Secure key storage  
✔ PKCS#11 cryptographic execution  
✔ OpenBao secret management  
✔ FastAPI orchestration layer  
✔ Base64 transport for signatures  

---

## 🚀 Future Improvements

- PostgreSQL audit logging
- JWT authentication layer
- Multi-key support
- Real hardware HSM migration (AWS CloudHSM / Thales)
- Microservice decomposition


