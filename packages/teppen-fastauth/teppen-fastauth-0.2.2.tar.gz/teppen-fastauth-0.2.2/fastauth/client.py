import time
import requests
import jwt
from .exceptions import AuthenticationServerException
from .env import AUTH_APP_HOST, AUTH_APP_PROTOCOL


class AuthClientV2:
    """
    Client for handling authentication tokens with automatic refresh
    """

    def __init__(
        self,
        access_key: str,
    ):
        """
        Initialize a token client

        Args:
            access_key: System user access key for authentication
        """
        self.access_key = access_key
        self.base_url = f"{AUTH_APP_PROTOCOL}://{AUTH_APP_HOST}"
        self.token_endpoint = f"{self.base_url}/api/v2/tokens"
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = 0
        self._jwks_client = None

    def get_token(self, force_refresh: bool = False) -> str:
        """
        Get a valid access token, refreshing if necessary

        Args:
            force_refresh: Force token refresh even if current token is still valid

        Returns:
            Valid access token
        """
        current_time = time.time()

        # Check if we need to refresh the token (if it's expired or will expire in the next 30 seconds)
        if (
            self._access_token is None
            or force_refresh
            or current_time > (self._token_expires_at - 30)
        ):
            if self._refresh_token and not force_refresh:
                self._refresh_tokens()
            else:
                self._generate_tokens()

        return self._access_token

    def _generate_tokens(self) -> None:
        """Generate new tokens using the access key"""
        if not self.access_key:
            raise ValueError("Access key is required to generate tokens")

        url = f"{self.token_endpoint}"

        response = requests.post(
            url,
            json={"grant_type": "access_key"},
            headers={"Authorization": f"Basic {self.access_key}"},
        )

        if response.status_code >= 500:
            raise AuthenticationServerException("Authentication server error")

        if response.status_code != 201:
            raise AuthenticationServerException(
                f"Failed to generate tokens: {response.status_code} {response.text}"
            )

        self._process_token_response(response)

    def _refresh_tokens(self) -> None:
        """Refresh tokens using the refresh token"""
        if not self._refresh_token:
            # Fall back to generating new tokens if we don't have a refresh token
            return self._generate_tokens()

        url = f"{self.token_endpoint}"

        try:
            response = requests.post(
                url,
                json={"grant_type": "refresh_token"},
                headers={"Authorization": f"Bearer {self._refresh_token}"},
            )

            # Handle specific error cases for refresh tokens
            if response.status_code == 401:
                # This typically indicates an expired refresh token
                self._refresh_token = None  # Clear the expired refresh token
                return self._generate_tokens()  # Generate new tokens using access key

            if response.status_code != 201:
                # Any other error, try to generate new tokens
                return self._generate_tokens()

            self._process_token_response(response)

        except requests.RequestException:
            # Network errors also indicate we should try from scratch
            return self._generate_tokens()

    def _process_token_response(self, response) -> None:
        """Process token response and extract token information"""
        data = response.json()

        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]

        # Parse token to get expiration time
        token_payload = jwt.decode(
            self._access_token,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )

        self._token_expires_at = token_payload["exp"]

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an authenticated request with automatic token handling

        Args:
            method: HTTP method (GET, POST, etc)
            url: URL to request
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object
        """
        headers = kwargs.get("headers", {})

        # If Authorization is not already set, add it
        if "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.get_token()}"
            kwargs["headers"] = headers

        response = requests.request(method, url, **kwargs)

        # If we get a 401, our token might be expired even if we thought it wasn't
        # Try refreshing once and retry
        if response.status_code == 401:
            headers["Authorization"] = f"Bearer {self.get_token(force_refresh=True)}"
            kwargs["headers"] = headers
            response = requests.request(method, url, **kwargs)

        return response

    def get(self, url: str, **kwargs) -> requests.Response:
        """Authenticated GET request"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Authenticated POST request"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """Authenticated PUT request"""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """Authenticated DELETE request"""
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        """Authenticated PATCH request"""
        return self.request("PATCH", url, **kwargs)
