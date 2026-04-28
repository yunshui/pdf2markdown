"""Model client for calling LLM APIs."""

import base64
import io
import time
from typing import List, Optional, Tuple

import requests
from PIL import Image

from .logger import get_logger


class ModelClient:
    """Client for calling OpenAI-compatible LLM APIs with image support."""

    def __init__(self, model_name: str, api_url: str, api_key: str,
                 timeout: int = 60, max_retries: int = 3,
                 logger_name: str = "ModelClient"):
        """Initialize model client.

        Args:
            model_name: Name of the model to use
            api_url: Base URL for the API endpoint
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            logger_name: Name for the logger instance
        """
        self.model_name = model_name
        self.api_url = api_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = get_logger(logger_name)

        self.logger.info("ModelClient initialized",
                        model_name=model_name,
                        api_url=api_url,
                        timeout=timeout,
                        max_retries=max_retries)

    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string.

        Args:
            image: PIL Image object

        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    def _prepare_request(self, prompt: str, images: List[Image.Image]) -> dict:
        """Prepare API request payload.

        Args:
            prompt: Text prompt for the model
            images: List of PIL Image objects to include

        Returns:
            Request payload dictionary
        """
        content = [{"type": "text", "text": prompt}]

        for img in images:
            base64_img = self._image_to_base64(img)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_img}"
                }
            })

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        }

        self.logger.debug("Request payload prepared",
                         message_count=len(payload["messages"]),
                         image_count=len(images),
                         content_types=[item["type"] for item in content])

        return payload

    def _make_request(self, payload: dict) -> requests.Response:
        """Make HTTP request to the API.

        Args:
            payload: Request payload dictionary

        Returns:
            Response object

        Raises:
            requests.RequestException: If request fails
        """
        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Ensure API URL ends with /v1/chat/completions if it's a base URL
        endpoint = self.api_url
        if not endpoint.endswith('/chat/completions'):
            # Remove trailing slash first to normalize
            endpoint = endpoint.rstrip('/')
            # Add the path
            endpoint = endpoint + '/chat/completions'
            # If there's no /v1 in the path, add it
            if '/v1/' not in endpoint:
                endpoint = endpoint.replace('/chat/completions', '/v1/chat/completions')

        self.logger.debug(f"Making request to: {endpoint}")

        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )

        return response

    def _extract_response_content(self, response: requests.Response) -> str:
        """Extract content from API response.

        Args:
            response: Response object

        Returns:
            Extracted content string

        Raises:
            ValueError: If response format is invalid
        """
        try:
            response_json = response.json()

            # Handle different response formats
            if "choices" in response_json and len(response_json["choices"]) > 0:
                content = response_json["choices"][0]["message"]["content"]
                return content.strip()
            else:
                raise ValueError("Invalid response format: no 'choices' found")

        except (ValueError, KeyError, IndexError) as e:
            self.logger.error("Failed to extract response content",
                            response_text=response.text[:500],
                            exception=e)
            raise ValueError(f"Invalid response format: {e}")

    def call(self, prompt: str, images: List[Image.Image],
             retry_count: int = None) -> str:
        """Call the model with prompt and images.

        Args:
            prompt: Text prompt for the model
            images: List of PIL Image objects
            retry_count: Current retry attempt (for recursion)

        Returns:
            Model response content

        Raises:
            ValueError: If request fails after all retries
        """
        if retry_count is None:
            retry_count = 0

        max_retries = self.max_retries

        try:
            payload = self._prepare_request(prompt, images)

            # Display progress
            if retry_count == 0:
                self.logger.info(f"Calling model {self.model_name}...",
                                prompt_length=len(prompt),
                                image_count=len(images))
            else:
                self.logger.info(f"Retry {retry_count}/{max_retries} calling model...")

            response = self._make_request(payload)

            if response.status_code == 200:
                content = self._extract_response_content(response)
                self.logger.info("Model call successful",
                                response_length=len(content))
                return content
            else:
                error_msg = f"API returned status code {response.status_code}"
                self.logger.error(error_msg,
                                response_text=response.text[:500])
                raise requests.HTTPError(error_msg)

        except requests.Timeout as e:
            self.logger.warning(f"Request timeout after {self.timeout}s",
                               attempt=retry_count + 1,
                               max_attempts=max_retries)
            if retry_count < max_retries:
                self.logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                return self.call(prompt, images, retry_count + 1)
            else:
                raise ValueError(f"Request failed after {max_retries} retries: timeout")

        except requests.ConnectionError as e:
            self.logger.warning(f"Connection error: {str(e)}",
                               attempt=retry_count + 1,
                               max_attempts=max_retries)
            if retry_count < max_retries:
                self.logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                return self.call(prompt, images, retry_count + 1)
            else:
                raise ValueError(f"Request failed after {max_retries} retries: connection error")

        except requests.HTTPError as e:
            if retry_count < max_retries:
                self.logger.warning(f"HTTP error: {str(e)}",
                                   attempt=retry_count + 1,
                                   max_attempts=max_retries)
                self.logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                return self.call(prompt, images, retry_count + 1)
            else:
                raise ValueError(f"Request failed after {max_retries} retries: {str(e)}")

        except Exception as e:
            self.logger.error("Unexpected error during model call",
                            exception=e)
            if retry_count < max_retries:
                self.logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                return self.call(prompt, images, retry_count + 1)
            else:
                raise ValueError(f"Request failed after {max_retries} retries: {str(e)}")

    def validate_api(self) -> Tuple[bool, str]:
        """Validate API connectivity and credentials.

        Returns:
            Tuple of (success, message)
        """
        if not self.api_url:
            return False, "API URL is not configured"

        # Create a simple test payload
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": "test"}]
                }
            ],
            "max_tokens": 10
        }

        try:
            response = self._make_request(payload)
            if response.status_code == 200:
                return True, "API connection successful"
            else:
                return False, f"API returned status code {response.status_code}"
        except Exception as e:
            return False, f"API validation failed: {str(e)}"