import requests

BASE_URL = "https://whov.dev/customer.php"

class TrSolverError(Exception):
    """Base exception class for trsolver errors."""
    pass

class SiteNotAllowedError(TrSolverError):
    """Raised when access to a site is not allowed for the token."""
    def __init__(self, message="Bu site için erişim izniniz yok.", allowed_sites=None, requested_site=None):
        self.message = message
        self.allowed_sites = allowed_sites or []
        self.requested_site = requested_site
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (İstenen: {self.requested_site}, İzinliler: {self.allowed_sites})"

class NoTokenAvailableError(TrSolverError):
    """Raised when no token is available for the requested site."""
    def __init__(self, message="Bu site için kullanılabilir token kalmadı.", site=None):
        self.message = message
        self.site = site
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (Site: {self.site})"

class TrSolverClient:
    """
    A client for interacting with the whov.dev API.
    """
    def __init__(self, base_url=BASE_URL, timeout=30):
        """
        Initializes the TrSolverClient.

        Args:
            base_url (str): The base URL for the API. Defaults to https://whov.dev/customer.php.
            timeout (int): Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url
        self.timeout = timeout

    def _make_request(self, params):
        """Helper method to make GET requests."""
        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            raise TrSolverError(f"API isteği sırasında hata oluştu: {e}") from e

    def get_customer_data(self, token: str) -> dict:
        """
        Retrieves customer data using a token.

        Args:
            token (str): The customer's API token.

        Returns:
            dict: A dictionary containing customer data ('kullanici_adi', 'eposta',
                  'izinli_siteler', 'kalan_kredi').

        Raises:
            TrSolverError: If the API request fails or returns an error.
        """
        params = {
            'data': 'true',
            'token': token
        }
        response = self._make_request(params)

        try:
            data = response.json()
            if data.get('success') is True:
                return data.get('data', {})
            else:
                # Handle potential specific errors if the API defines them for this endpoint
                error_message = data.get('message', 'API bilinmeyen bir hata döndürdü.')
                raise TrSolverError(f"Müşteri verisi alınamadı: {error_message}")
        except ValueError: # Includes JSONDecodeError
             raise TrSolverError("API'den geçersiz JSON yanıtı alındı.")

    def get_access_value(self, token: str, site: str) -> str:
        """
        Retrieves an access value for a specific site using a token.

        Args:
            token (str): The customer's API token.
            site (str): The URL of the site for which access is requested.

        Returns:
            str: The access value string if successful.

        Raises:
            SiteNotAllowedError: If access to the site is denied.
            NoTokenAvailableError: If no token is available for the site.
            TrSolverError: If the API request fails or returns an unexpected error.
        """
        params = {
            'access': 'true',
            'token': token,
            'site': site
        }
        response = self._make_request(params)

        # Check content type to determine if it's the value string or a JSON error
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            try:
                data = response.json()
                if data.get('success') is False:
                    message = data.get('message', '')
                    error_data = data.get('data', {})
                    if "erişim izniniz yok" in message:
                        raise SiteNotAllowedError(
                            message=message,
                            allowed_sites=error_data.get('izinli_siteler'),
                            requested_site=error_data.get('istenen_site')
                        )
                    elif "token kalmadı" in message:
                        raise NoTokenAvailableError(
                            message=message,
                            site=error_data.get('site')
                        )
                    else:
                        raise TrSolverError(f"API hatası: {message}")
                else:
                    # Should not happen if success=false is expected for errors
                    raise TrSolverError("Başarısız JSON yanıtı beklenirken beklenmedik format.")
            except ValueError:
                raise TrSolverError("API'den geçersiz JSON hata yanıtı alındı.")
        else:
            # Assume it's the access value string
            return response.text # Return the raw response text 