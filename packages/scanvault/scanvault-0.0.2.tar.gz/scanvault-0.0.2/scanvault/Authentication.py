import requests
from ._config import get_api_url

class Authentication:
    """
    Authentication class for handling user login and authentication.
    Methods:
        __init__():
            Initializes the Authentication class and sets the base URL for API requests.
        login(username: str, password: str) -> str:
            Authenticates the user with the provided username and password.
            Sends a POST request to the authentication endpoint to retrieve an authentication token.
            Args:
                username (str): The username of the user.
                password (str): The password of the user.
            Returns:
                str: The authentication token received from the server.
            Raises:
                HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    def __init__(self):
        """
        Initializes the Authentication class.

        This constructor sets up the base URL for API interactions by calling
        the `get_api_url` function.

        Attributes:
            base_url (str): The base URL for the API.
        """
        self.base_url = get_api_url()
    
    def login(self, username: str, password: str) -> str:
        """
        Authenticates a user by sending their username and password to the server 
        and retrieves an authentication token.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user attempting to log in.

        Returns:
            str: The authentication token received from the server.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request to the server fails 
            or returns an error status code.
        """
        response = requests.post(f"{self.base_url}/auth/token", json={
            "username": username,
            "password": password
        })
        response.raise_for_status()
        return response.json()