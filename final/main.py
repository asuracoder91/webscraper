# main.py
from flask import Flask, render_template, request, redirect, url_for
from request_jobs_berlin import RequestJobsFromBerlin
from request_jobs_web3 import RequestJobsFromWeb3Career

app = Flask(__name__)

app.jinja_env.globals.update(enumerate=enumerate)

# 전역 변수로 Web3의 페이지 관리
web3_jobs = None
web3_job_urls = []
berlin_jobs_data = []
web3_jobs_data = []


class JobSearchError(Exception):
    """Custom exception for job search errors."""

    pass


@app.route("/", methods=["GET", "POST"])
def index():
    global web3_jobs, berlin_jobs_data, web3_jobs_data

    if request.method == "POST":
        keyword = request.form.get("keyword")

        try:
            # Berlin Jobs
            berlin_jobs = RequestJobsFromBerlin(keyword)
            berlin_jobs_data = berlin_jobs.fetch_jobs()
            if not berlin_jobs_data:
                raise JobSearchError("No jobs found in Berlin for the given keyword.")

            # Web3 Jobs
            web3_jobs = RequestJobsFromWeb3Career(keyword)
            web3_job_urls = web3_jobs.get_next_page()
            if web3_job_urls:
                web3_jobs_data = web3_jobs.fetch_jobs(web3_job_urls)
            else:
                web3_jobs_data = []
                raise JobSearchError("No jobs found in Web3 for the given keyword.")

            return redirect(url_for("results"))

        except JobSearchError as e:
            print(f"Job search error: {e}")
            return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/results")
def results():
    return render_template(
        "results.html", berlin_jobs=berlin_jobs_data, web3_jobs=web3_jobs_data
    )


@app.route("/next_web3_page")
def next_web3_page():
    global web3_jobs, web3_jobs_data

    web3_job_urls = web3_jobs.get_next_page()
    if web3_job_urls:
        web3_jobs_data.extend(web3_jobs.fetch_jobs(web3_job_urls))
    else:
        print("No more jobs available in Web3.")

    return render_template(
        "results.html", berlin_jobs=berlin_jobs_data, web3_jobs=web3_jobs_data
    )


if __name__ == "__main__":
    app.run(debug=True)
