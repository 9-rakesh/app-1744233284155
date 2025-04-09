import requests
import logging
import json
from typing import Optional, Dict, Any, Union
from pathlib import Path
from config.settings import settings
from urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)

class APIUtils:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self._setup_session()

    def _setup_session(self):
        """Configure session with default headers and auth"""
        self.session.headers.update({
            "Authorization": f"Bearer {settings.API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.session.verify = False  # Disable SSL verification for testing
        self.session.hooks = {
            'response': lambda r, *args, **kwargs: r.raise_for_status()
        }

    def _make_request(self, method: str, endpoint: str, 
                     data: Optional[Union[Dict, str]] = None,
                     params: Optional[Dict] = None,
                     files: Optional[Dict] = None,
                     headers: Optional[Dict] = None,
                     max_retries: int = 3) -> requests.Response:
        """Core request method with retry logic and enhanced error handling"""
        url = urljoin(self.base_url, endpoint)
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        last_exception = None
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if isinstance(data, dict) else None,
                    data=data if isinstance(data, str) else None,
                    params=params,
                    files=files,
                    headers=request_headers,
                    timeout=self.timeout
                )
                logger.debug(f"API {method} to {url} - Status: {response.status_code}")
                return response
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                logger.error(f"API request failed after {max_retries} attempts: {method} {url} - Error: {str(e)}")
                raise last_exception

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET request with JSON response"""
        return self._make_request("GET", endpoint, params=params).json()

    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None) -> Dict:
        """POST request with JSON response"""
        return self._make_request("POST", endpoint, data=data).json()

    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None) -> Dict:
        """PUT request with JSON response"""
        return self._make_request("PUT", endpoint, data=data).json()

    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None) -> Dict:
        """PATCH request with JSON response"""
        return self._make_request("PATCH", endpoint, data=data).json()

    def delete(self, endpoint: str) -> bool:
        """DELETE request"""
        return self._make_request("DELETE", endpoint).status_code == 204

    def upload_file(self, endpoint: str, file_path: Path, field_name: str = "file", 
                  extra_data: Optional[Dict] = None) -> Dict:
        """Upload file with multipart form data and optional extra fields"""
        try:
            with open(file_path, 'rb') as f:
                files = {field_name: (file_path.name, f)}
                data = extra_data or {}
                return self._make_request(
                    "POST", 
                    endpoint,
                    files=files,
                    data=data,
                    headers={"Content-Type": None}  # Let requests set boundary
                ).json()
        except Exception as e:
            logger.error(f"File upload failed: {str(e)}")
            raise

    def download_file(self, endpoint: str, save_path: Path) -> bool:
        """Download file from API"""
        try:
            response = self._make_request("GET", endpoint, headers={"Accept": "*/*"})
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            logger.error(f"File download failed: {str(e)}")
            raise

    def close(self):
        """Clean up session resources"""
        self.session.close()
        logger.info("API session closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
