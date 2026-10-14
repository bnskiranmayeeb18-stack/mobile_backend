import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class IntegrationError(Exception): pass

class BaseExternalClient:
    TIMEOUT = 5
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
        reraise=True
    )
    def _make_request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', self.TIMEOUT)
        safe_kwargs = {k: v for k, v in kwargs.items() if k != 'headers'}
        logger.info(f"External call: {method} {url} | {safe_kwargs}")
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout:
            logger.error(f"Integration TIMEOUT: {url} - no secrets logged")
            raise IntegrationError(f"Timeout calling {url}")
        except requests.HTTPError as e:
            logger.error(f"Integration FAILED: {url} status={e.response.status_code} body={e.response.text[:200]}")
            raise IntegrationError(f"External service error: {e.response.status_code}")
