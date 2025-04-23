import requests
from typing import Optional
from .response import Response

class E164:

    def __init__(self, client=None):

        self.client = client or requests.Session()
        if not client:
            self.client.headers.update({
                'User-Agent': 'MyCustomAgent/1.0 (Not a browser)',
                'Referer': 'https://www.e164.com/',
            })
    
    def lookup(self, phone_number: str) -> Response:

        try:
            # Sanitize the number (equivalent to PHP's FILTER_SANITIZE_NUMBER_INT)
            phone_number = ''.join(char for char in phone_number if char.isdigit() or char in ['+', '-'])
            url = f"https://e164.com/{phone_number}"
            
            response = self.client.get(url)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            data = response.json()
            
            if not data:
                raise ValueError("Invalid phone number")
            
            if isinstance(data, list) and data:
                data = data[0] 

            return Response.from_dict(data)
        except Exception as e:
            raise ValueError(f"Error during lookup: {e}")

