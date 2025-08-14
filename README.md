# Deloitte Internship Tracker

This Python script automates the process of scraping internship postings from the Deloitte careers website and adding them to a Google Sheet for easy tracking.

## Features

- **Web scraping with Selenium**: Automatically collects internship listings from Deloitte's careers page.
- **Google Sheets integration**: Inserts scraped data directly into a Google Sheet for centralized tracking.
- **Dynamic column mapping**: Detects header positions in your Google Sheet for flexible data writing.
- **Details extraction**: Retrieves role titles, locations (single/multiple), deadlines, and application links.
- **Practice area detection**: Categorizes roles into Audit, Tax, Advisory, Technology, or General based on title keywords.

## Requirements

- Python 3.7+
- Google Sheets API credentials JSON file (`credentials.json`)
- Installed dependencies (see below)

## Installation

1. **Clone or download this repository**.

2. **Install required Python packages**:
    ```bash
    pip install selenium gspread oauth2client webdriver-manager
    ```

3. **Set up Google Sheets API**:
    - Go to [Google Cloud Console](https://console.cloud.google.com/)
    - Create a new project and enable the **Google Sheets API** and **Google Drive API**
    - Create a Service Account and download the JSON credentials file
    - Rename the credentials file to `credentials.json` and place it in the same directory as the script
    - Share your Google Sheet with the service account email

4. **Configure your Google Sheet**:
    - Create a Google Sheet named **"Big 4 Internship Tracker"**
    - Ensure your headers are in **row 3**
    - Supported headers include:
        - Firm
        - Role Title
        - Practice
        - Industry
        - Location
        - Deadline
        - Link
        - Status

## Usage

1. Run the script:
    ```bash
    python deloitte_internship_tracker.py
    ```

2. The script will:
    - Open the Deloitte internships page
    - Scrape available internships
    - Extract role title, practice area, location(s), deadlines, and links
    - Insert data into the first available row of your Google Sheet starting from row 4

3. Output logs in the terminal will indicate the progress and number of internships added.

## Configuration Notes

- The script uses `webdriver-manager` to handle ChromeDriver installation automatically.
- The default view is in a visible Chrome browser window. To run in headless mode, uncomment:
    ```python
    options.add_argument("--headless")
    ```
- The Deloitte internships URL is set to filter for specific categories; you can modify the `internships_url` variable for other roles.

## Example Output

```
🌐 Visiting internships page: https://apply.deloitte.com/en_US/careers/SearchJobs?3_149_3=637&3_5_3=478&sort=relevancy
✅ Found 15 internships on this page.
✅ Added: Tax Analyst Intern → Row 4
✅ Added: Audit Intern → Row 5
🚀 Finished! Added 15 internships to Google Sheet.
🛑 Browser closed.
```

## Disclaimer

This script is for educational purposes only. Be mindful of Deloitte's website terms of service when running automated scripts.
