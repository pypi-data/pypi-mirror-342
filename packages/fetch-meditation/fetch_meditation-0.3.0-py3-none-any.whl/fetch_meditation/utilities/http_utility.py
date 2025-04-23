import urllib3
from urllib3.exceptions import HTTPError
from typing import Dict, Optional, Any
import urllib.parse


class HttpUtility:
    def __init__(self):
        pass

    @staticmethod
    def http_get(url: str, params: Optional[Dict[str, Any]] = None):
        http = urllib3.PoolManager()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0"
        }

        # Properly append query parameters to the URL for GET requests
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}{'&' if '?' in url else '?'}{query_string}"

        try:
            response = http.request("GET", url, headers=headers)
            if response.status in [200, 302, 304]:
                try:
                    # First try decoding with utf-8
                    return response.data.decode("utf-8")
                except UnicodeDecodeError:
                    # If utf-8 fails, look for charset in Content-Type header
                    content_type = response.headers.get("Content-Type", "")
                    charset = HttpUtility.find_charset(content_type)
                    if charset:
                        try:
                            return response.data.decode(charset)
                        except UnicodeDecodeError:
                            pass
                    # Decode with utf-8 using 'replace' and replace undecodable bytes with a space
                    return response.data.decode("utf-8", errors="replace").replace("\ufffd", " ")
            else:
                raise Exception("Received non-acceptable status code: " + str(response.status))
        except HTTPError as e:
            raise Exception("HTTP error occurred: " + str(e))

    @staticmethod
    def find_charset(content_type):
        """Extract charset from Content-Type header if present."""
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
            return charset
        return ""
