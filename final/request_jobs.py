import requests


class RequestJobs:

    def __init__(self, base_url: str, search_word: str):
        self.base_url = base_url
        self.search_word = search_word
        self.session = requests.Session()

    def request_website(self, url: str) -> str:
        response = self.session.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        response.raise_for_status()
        return response.text
