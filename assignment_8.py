import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

BASE_URL = "https://berlinstartupjobs.com"
ENGINEERING_URL = "/engineering"
SKILL_URL = "/skill-areas/"

skills = ["python", "typescript", "javascript", "rust"]


@dataclass
class Job:
    company_url: str
    company_name: str
    job_position: str
    job_link: str
    job_description: str

    def __str__(self):
        return (
            f"Company: {self.company_name}\n"
            f"Position: {self.job_position}\n"
            f"Description: {self.job_description}\n"
            f"Link: {self.job_link}\n"
            f"Company URL: {self.company_url}\n"
        )


class RequestJobs:
    def __init__(self, base_url, *args):
        self.base_url = base_url
        match args:
            case [detail_url]:
                self.detail_url = detail_url
            case [skill_url, skill_name]:
                self.detail_url = f"{skill_url}/{skill_name}"
            case _:
                raise ValueError("Invalid number of arguments provided.")
        self.fetch_jobs()

    def request_website(self, url):
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        response.raise_for_status()
        return response.text

    def fetch_jobs(self):
        current_url = f"{self.base_url}{self.detail_url}"
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
                print(job_data)
            current_url = self.get_more_page(soup)

    def get_more_page(self, soup):
        if next_page := soup.find("a", {"class": "next page-numbers"}):
            return next_page["href"]
        return None


RequestJobs(BASE_URL, ENGINEERING_URL)

for skill in skills:
    RequestJobs(BASE_URL, SKILL_URL, skill)
