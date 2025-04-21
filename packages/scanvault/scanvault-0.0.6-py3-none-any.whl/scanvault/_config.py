import base64

# Base64-encoded version of your base URL
# e.g., "https://your-api.aws.com" → encoded to:
ENCODED_URL = "aHR0cDovLzY1LjIuMTQ1LjIxNjo4MDAw"

def get_api_url():
    # Decode the base64-encoded URL
    decoded_url = base64.b64decode(ENCODED_URL).decode('utf-8')
    
    # Return the decoded URL
    return decoded_url