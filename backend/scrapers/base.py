from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    @abstractmethod
    def search_jobs(self, keyword, location, page=1):
        pass

    @abstractmethod
    def get_job_detail(self, url):
        pass
