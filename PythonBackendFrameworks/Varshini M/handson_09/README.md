# Hands-on 9

Run `uvicorn main:app --reload`. Register with `/api/v1/auth/register/`, login to receive a 30-minute bearer token, then send `Authorization: Bearer <token>` to protected course POST/DELETE routes. The database stores `hashed_password`, never the plaintext password.
