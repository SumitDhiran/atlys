import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET="please_please_update_me_please"
JWT_ALGORITHM="HS256"

# JWT_SECRET = config("secret")
# JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


# {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzIjoxNzI3NTkyNDI1LjAyMTgyOTF9.Z6IpShsvk7WRUisCkog_hEGa2nwh_xvQhfVSd9AcKB8'}
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzIjoxNzI3NTkyNDI1LjAyMTgyOTF9.Z6IpShsvk7WRUisCkog_hEGa2nwh_xvQhfVSd9AcKB8
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

# print(sign_jwt(1))


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

# print(decode_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzIjoxNzI3NTkyNDI1LjAyMTgyOTF9.Z6IpShsvk7WRUisCkog_hEGa2nwh_xvQhfVSd9AcKB8"))