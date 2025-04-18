from datetime import datetime, timezone

import pygsheets

import config


def write_dataframe_to_google_sheets(df):
    gc = pygsheets.authorize(service_file="./credentials.json")

    spreadsheet_id = config.getGoogleSheetsId()
    sh = gc.open_by_key(spreadsheet_id)

    new_sheet_title = f"{config.getKeywords()} - {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}"

    try:
        existing_ws = sh.worksheet_by_title(new_sheet_title)
        sh.del_worksheet(existing_ws)
    except Exception:
        # Worksheet doesn't exist; nothing to delete
        pass

    new_ws = sh.add_worksheet(new_sheet_title)
    new_ws.set_dataframe(df, (1, 1), copy_index=False)

    print(f"DataFrame successfully written to '{new_sheet_title}' sheet in the Google Sheet.")
