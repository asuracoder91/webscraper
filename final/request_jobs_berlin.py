from bs4 import BeautifulSoup
from request_jobs import RequestJobs
from models import Job, JobList
from typing import Optional


class RequestJobsFromBerlin(RequestJobs):
    BERLIN_URL = "https://berlinstartupjobs.com/skill-areas/"

    def __init__(self, search_word: str):
        super().__init__(self.BERLIN_URL, search_word)

    def fetch_jobs(self) -> JobList:
        current_url = f"{self.base_url}{self.search_word}"
        job_search_result = []
        while current_url:
            soup = BeautifulSoup(self.request_website(current_url), "html.parser")
            jobs = soup.find_all("li", {"class": "bjs-jlid"})
            for job in jobs:
                company_tag = job.find("a", {"class": "bjs-jlid__b"})
                position_tag = job.find("h4", {"class": "bjs-jlid__h"}).find("a")
                job_data = Job(
                    company_url=company_tag["href"],
                    company_name=company_tag.text,
                    job_position=position_tag.text,
                    job_link=position_tag["href"],
                    job_description=job.find(
                        "div", {"class": "bjs-jlid__description"}
                    ).text,
                )
                job_search_result.append(job_data)

            current_url = self.get_more_page(soup)
        return job_search_result

    @staticmethod
    def get_more_page(soup: BeautifulSoup) -> Optional[str]:
        next_page = soup.find("a", {"class": "next page-numbers"})
        return next_page["href"] if next_page else None
