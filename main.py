import dataframeUtils
import gSheetsUtils
import jobUtils


def main():
    jobs = jobUtils.fetch_jobs()
    if len(jobs) == 0:
        print("No jobs found.")
        return
    company_jobs = jobUtils.group_jobs_by_company_and_fetch_company_details(jobs)
    company_jobs = jobUtils.filter_and_sort_companies(company_jobs)
    dataframe = dataframeUtils.transform_to_df(company_jobs)
    gSheetsUtils.write_dataframe_to_google_sheets(dataframe)


if __name__ == "__main__":
    main()
