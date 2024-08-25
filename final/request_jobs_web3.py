from bs4 import BeautifulSoup
from request_jobs import RequestJobs
from models import Job, JobList
from typing import List


class RequestJobsFromWeb3Career(RequestJobs):
    WEB3_CAREER_URL = "https://web3.career/"

    def __init__(self, search_word: str):
        super().__init__(self.WEB3_CAREER_URL, search_word)
        self.page_number = 1
        self.has_more_pages = True

    def get_next_page(self) -> List[str]:
        if not self.has_more_pages:
            return None

        current_url = f"{self.base_url}{self.search_word}-jobs?page={self.page_number}"
        soup = BeautifulSoup(self.request_website(current_url), "html.parser")

        job_urls_source = soup.find_all("a", {"data-turbo-frame": "job"})
        job_urls = list(set(a_tag["href"] for a_tag in job_urls_source))

        # 다음 페이지 확인
        next_page = soup.find("li", {"class": "page-item next"})
        if next_page and "disabled" not in next_page.get("class", []):
            self.page_number += 1
        else:
            self.has_more_pages = False

        return job_urls

    def fetch_jobs(self, job_urls: List[str]) -> JobList:
        job_search_result = []
        for job_url in job_urls:
            detail_url = f"{self.base_url}{job_url}"
            soup = BeautifulSoup(self.request_website(detail_url), "html.parser")
            company_tag = soup.find("div", {"class": "position-sticky"}).find("a")
            position_source = soup.find("h1").text.strip()
            if "Web3" in position_source:
                position_tag = position_source.split("Web3", 1)[1].strip()
            else:
                position_tag = position_source

            # 50글자 이상인 첫 번째 <p> 태그의 텍스트를 찾아서 job_description으로 사용
            paragraphs = soup.find_all("p")
            selected_paragraph = None
            for p in paragraphs:
                if len(p.get_text(strip=True)) >= 50:
                    selected_paragraph = p.get_text(strip=True)
                    break
            if selected_paragraph:
                job_description = selected_paragraph
            else:
                job_description = ""
            job_data = Job(
                company_url=(
                    f"{self.base_url}{company_tag['href']}" if company_tag else ""
                ),
                company_name=company_tag.text.strip() if company_tag else "-",
                job_position=position_tag,
                job_link=detail_url,
                job_description=job_description,
            )
            job_search_result.append(job_data)
        return job_search_result
