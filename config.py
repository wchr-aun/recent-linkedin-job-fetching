from urllib.parse import quote_plus


def getDelayGapInSecond():
    return 0.05


def getKeywords():
    return "Marketing Analyst"


def getJobPostedTime():
    return 43200 + 3600  # Half a day + 1 hour in seconds


def getLocation():
    return "London Area, United Kingdom"


def getHeaders():
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }


def getBaseUrl():
    # geoId=90009496 for London
    return f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?distance=0&{getJobPostedTimeParameter()}&{getLocationParameter()}&{getKeywordsParameter()}&origin=JOB_SEARCH_PAGE_JOB_FILTER&position=0&pageNum=0&start="


def getKeywordsParameter():
    return f"keywords={quote_plus(getKeywords())}"


def getJobPostedTimeParameter():
    return f"f_TPR=r{getJobPostedTime()}"


def getLocationParameter():
    return f"location={quote_plus(getLocation())}"


def getGoogleSheetsId():
    return "1TQcd5_-4NunNRHXVd5F6ww6oNA3bkig0gG5_Ojob5Hs"
