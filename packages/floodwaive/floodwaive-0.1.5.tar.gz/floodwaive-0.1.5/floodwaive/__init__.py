import requests


def info():
    print("FloodWaive SDK – Tools for predictive flood intelligence.")
    print("Docs: [TBD]")

def hello_world():
    print("🌊 Hello from FloodWaive!")
    

def validate_token(token: str, api_url: str = "https://api.floodwaive.de", timeout: int = 5) -> bool:
    """
    Validates an API token against a default or provided endpoint.

    Args:
        token (str): The token to validate.
        api_url (str, optional): The API endpoint to validate against.
        timeout (int): Timeout for the request in seconds.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            print("✅ Token is valid and accepted.")
            return True
        elif response.status_code in (401, 403):
            print(f"❌ Token rejected (status: {response.status_code}).")
            return False
        else:
            print(f"⚠ Unexpected response (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False
