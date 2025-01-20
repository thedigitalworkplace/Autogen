import hashlib
from fastapi import Request, HTTPException

# Mock database or service for users
database = {
    "users": {
        "user@example.com": {
            "name": "John Doe",
            "email": "user@example.com",
            "company": "Officio",
            "isAdmin": False,
        }
    }
}


def hash_value(value: str) -> str:
    """Hash a value using SHA-256."""
    return hashlib.sha256(value.encode()).hexdigest()


def get_user_session(request: Request):
    """Simulate fetching a user session based on headers."""
    email = request.headers.get("X-User-Email")
    if not email or email not in database["users"]:
        raise HTTPException(status_code=401, detail="Unauthorized: User not found")

    return database["users"][email]


def create_hashed_id(email: str, company: str) -> str:
    """Generate a hashed user ID."""
    return hash_value(email + company)


import hashlib
import os
import requests
from fastapi import Request, HTTPException


def hash_value(value: str) -> str:
    """Hash a value using SHA-256."""
    return hashlib.sha256(value.encode()).hexdigest()


def get_user_session(request: Request):
    """Fetch user session dynamically from app.officio.work."""
    # Retrieve the user email from request headers
    email = request.headers.get("X-User-Email")
    if not email:
        raise HTTPException(
            status_code=401, detail="Unauthorized: Email header is missing"
        )

    # Define the API URL and authentication token for app.officio.work
    officio_api_url = os.getenv(
        "OFFICIO_API_URL", "https://app.officio.work/api/v1/get-user-details"
    )
    api_token = os.getenv("OFFICIO_API_TOKEN")
    if not api_token:
        raise HTTPException(
            status_code=500, detail="Server misconfiguration: API token is missing"
        )

    # Make a request to the external API
    try:
        response = requests.post(
            officio_api_url,
            headers={"Authorization": f"Bearer {api_token}"},
            json={"email": email},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to app.officio.work: {str(e)}"
        )

    # Parse the response
    user_data = response.json()
    if not user_data.get("status") or "user" not in user_data.get("data", {}):
        raise HTTPException(
            status_code=404, detail="User not found in app.officio.work"
        )

    return user_data["data"]["user"]


def create_hashed_id(email: str, company: str) -> str:
    """Generate a hashed user ID."""
    return hash_value(email + company)
