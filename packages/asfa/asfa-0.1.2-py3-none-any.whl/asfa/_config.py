import base64

# Base64-encoded version of your base URL
# e.g., "https://your-api.aws.com" → encoded to:
ENCODED_URL = "aHR0cDovLzEzLjIzMy4xNTQuMTAzOjgwMDA="

def get_api_url():
    return base64.b64decode(ENCODED_URL).decode("utf-8")
