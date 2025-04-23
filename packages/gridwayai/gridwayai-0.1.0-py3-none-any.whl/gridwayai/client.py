import requests
from typing import List, Optional
from .exceptions import AuthenticationError, RateLimitError, APIError

class GridwayAI:
    """
    GridwayAI client for calling the /embeddings endpoint.
    """

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the client with your API key.

        Args:
            api_key (str): Your GridwayAI API key.
            base_url (str, optional): Override the default API URL.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") if base_url else "https://api.gridwayai.com"

    def embeddings(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of input texts.

        Args:
            input (List[str]): A list of strings to embed.

        Returns:
            List[List[float]]: A list of embedding vectors.

        Raises:
            AuthenticationError: Invalid or missing API key.
            RateLimitError: Too many requests.
            APIError: Any other error from the API.
        """
        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"input": input}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Invalid or unauthorized API key.")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded. Try again later.")
        elif response.status_code >= 400:
            raise APIError(f"API returned error {response.status_code}: {response.text}")

        try:
            return response.json()["data"]
        except (KeyError, ValueError):
            raise APIError("Malformed API response.")
