from fastapi import Request, HTTPException, Depends
import jwt
import os
from functools import lru_cache


@lru_cache()
def get_secret_key():
    return os.getenv("SECRET_KEY")


async def verify_token(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")

        token = auth_header.split(" ")[1]
        secret_key = get_secret_key()
        jwt.decode(token, secret_key, algorithms=["HS256"])
        return True
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")
