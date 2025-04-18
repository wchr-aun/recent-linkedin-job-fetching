import pandas as pd


def transform_to_df(company_jobs):
    rows = []
    for company, info in company_jobs:
        for pos in info.get("position", []):
            rows.append(
                {
                    "Company": company,
                    "Role": pos.get("role"),
                    "Job URL": pos.get("url"),
                    "Time Posted": pos.get("timePosted"),
                    "Followers Count": info.get("followersCount"),
                    "Company Size": info.get("companySize"),
                    "Company Industry": info.get("industry"),
                    "Company URL": pos.get("companyUrl"),
                }
            )

    print("Done transforming to dataframe")

    return pd.DataFrame(rows)
