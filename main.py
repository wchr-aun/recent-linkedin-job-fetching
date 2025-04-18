import dataframeUtils
import gSheetsUtils
import jobUtils

jobs = jobUtils.fetch_jobs()
company_jobs = jobUtils.group_jobs_by_company_and_fetch_company_details(jobs)
company_jobs = jobUtils.filter_and_sort_companies(company_jobs)
dataframe = dataframeUtils.transform_to_df(company_jobs)
gSheetsUtils.write_dataframe_to_google_sheets(dataframe)
