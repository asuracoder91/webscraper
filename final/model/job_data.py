from dataclasses import dataclass


@dataclass
class Job:
    company_url: str
    company_name: str
    job_position: str
    job_link: str
    job_description: str
