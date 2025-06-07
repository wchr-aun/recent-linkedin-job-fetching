from datetime import datetime, timedelta, timezone

import pygsheets

import config


def write_dataframe_to_google_sheets(df, service_file):
    gc = pygsheets.authorize(service_file=service_file)

    spreadsheet_id = config.getGoogleSheetsId()
    sh = gc.open_by_key(spreadsheet_id)

    new_sheet_title = f"{config.getKeywords()[:50]} - {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}"

    try:
        existing_ws = sh.worksheet_by_title(new_sheet_title)
        sh.del_worksheet(existing_ws)
    except Exception:
        # Worksheet doesn't exist; nothing to delete
        pass

    new_ws = sh.add_worksheet(new_sheet_title)
    new_ws.set_dataframe(df, (1, 1), copy_index=False)

    print(f"DataFrame successfully written to '{new_sheet_title}' sheet in the Google Sheet.")


def delete_old_google_sheets(service_file):
    print("Deleting old sheets")
    gc = pygsheets.authorize(service_file=service_file)

    spreadsheet_id = config.getGoogleSheetsId()
    sh = gc.open_by_key(spreadsheet_id)

    worksheets = sh.worksheets(force_fetch=True)

    for sheet in worksheets:
        print(f"Checking sheet: {sheet.title}")
        now = datetime.now(timezone.utc)
        sheet_date_created = datetime.strptime(sheet.title.split(" - ")[-1], "%Y-%m-%d %H:%M").replace(
            tzinfo=timezone.utc
        )
        if now - sheet_date_created > timedelta(days=7):
            sh.del_worksheet(sheet)
            print(f"Deleted {sheet.title} as it was created over a week ago.")
