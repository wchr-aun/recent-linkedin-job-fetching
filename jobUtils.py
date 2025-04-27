import collections
import re
import time

import requests
from bs4 import BeautifulSoup

import config
import requestsUtils
from urlUtils import remove_subdomain


def fetch_jobs():
    jobs = []

    for i in range(10):
        url = config.getBaseUrl() + str(i * 10)
        jobSeen = set()

        response = requestsUtils.requests_with_retry(lambda: requests.get(url, headers=config.getHeaders()))

        soup = BeautifulSoup(response.text, "html.parser")
        div_base_card_elements = soup.find_all("div", class_="base-card")

        if len(div_base_card_elements) == 0:
            print(f"start={i * 10} -  No elements found. Stop fetching.")
            break

        for div_element in div_base_card_elements:
            job_title_elements = div_element.find_all("a", class_="base-card__full-link")
            company_name_elements = div_element.find_all("a", class_="hidden-nested-link")
            time_posted_elements = div_element.find_all("time", class_="job-search-card__listdate--new")

            for job, company, timePosted in zip(job_title_elements, company_name_elements, time_posted_elements):
                job_link = remove_subdomain(job["href"].split("?")[0])

                if job_link in jobSeen:
                    continue

                jobs.append(
                    {
                        "role": job.text.strip(),
                        "company": company.text.strip(),
                        "url": job_link,
                        "companyUrl": remove_subdomain(company["href"].split("?")[0]),
                        "timePosted": timePosted.text.strip(),
                    }
                )
                jobSeen.add(job_link)

    print("Done fetching jobs")

    return jobs


def group_jobs_by_company_and_fetch_company_details(jobs):
    group_by_company = collections.defaultdict(lambda: {"position": [], "companyUrl": ""})

    for job in jobs:
        group_by_company[job["company"]]["companyUrl"] = job["companyUrl"]

        followers_count, number_of_employees, industry = fetch_company_details(job["companyUrl"])
        group_by_company[job["company"]]["followersCount"] = followers_count
        group_by_company[job["company"]]["companySize"] = number_of_employees
        group_by_company[job["company"]]["industry"] = industry

        time.sleep(config.getDelayGapInSecond())  # Delay 100 ms for each request

        group_by_company[job["company"]]["position"].append(job)

    print("Done grouping and fetching company details")

    return group_by_company


def fetch_company_details(company_url):
    response = requestsUtils.requests_with_retry(lambda: requests.get(company_url, headers=config.getHeaders()))

    if response == None:
        print(f"Failed to fetch company details for {company_url}")
        return (0, 0, "")

    soup = BeautifulSoup(response.text, "html.parser")
    company_size_element = soup.find_all("div", {"data-test-id": "about-us__size"})

    number_of_employees_element = get_number_of_employees_element(company_size_element)

    number_of_followers_element = soup.find_all("meta", {"name": "description"})
    industry_element = soup.find_all("h2", class_="top-card-layout__headline")

    pattern = r"([\d,]+)\s+followers"
    match = re.search(pattern, get_number_of_followers(number_of_followers_element), re.IGNORECASE)

    followers_count = 0
    if match:
        followers_count = int(match.group(1).replace(",", ""))
    else:
        print(f"{company_url} - No followers count found.")

    return (followers_count, number_of_employees_element[0].text.strip(), get_industry(industry_element))


def filter_and_sort_companies(company_jobs):
    filtered_company_jobs = {
        k: v for k, v in company_jobs.items() if "followersCount" in v and v["followersCount"] > 10_000
    }

    print("Done filtering and sorting")

    return sorted(filtered_company_jobs.items(), key=lambda x: x[1]["followersCount"], reverse=True)


def get_number_of_employees_element(company_size_element):
    if len(company_size_element) == 0:
        return 0
    else:
        return company_size_element[0].find_all("dd")


def get_number_of_followers(number_of_followers_element):
    if len(number_of_followers_element) == 0:
        return 0
    else:
        return number_of_followers_element[0]["content"]


def get_industry(industry_element):
    if len(industry_element) == 0:
        return ""
    else:
        return industry_element[0].text.strip()
