from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time

# === Google Sheets Setup ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet_name = "Big 4 Internship Tracker"
sheet = client.open(spreadsheet_name).sheet1

# === Selenium Setup ===
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment for headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Detect column positions in Google Sheet
    header_row = 3
    headers = sheet.row_values(header_row)
    column_map = {header: index + 1 for index, header in enumerate(headers)}

    total_added = 0

    # Open the Deloitte Internships page directly
    internships_url = "https://apply.deloitte.com/en_US/careers/SearchJobs?3_149_3=637&3_5_3=478&sort=relevancy"
    print(f"🌐 Visiting internships page: {internships_url}")
    driver.get(internships_url)

    # Wait for job listings to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.article--result a.link"))
    )

    # Get all job links
    job_cards = driver.find_elements(By.CSS_SELECTOR, "article.article--result a.link")
    if not job_cards:
        print("❌ No internships found on this page.")
    else:
        print(f"✅ Found {len(job_cards)} internships on this page.")

    for job in job_cards:
        title = job.text.strip()
        link = job.get_attribute("href")

        # Visit job detail page to extract location(s) and deadline
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        location_str = "Unknown"
        deadline_str = "Unknown"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.article__header"))
            )

            # === Extract Locations ===
            try:
                toggle_link = driver.find_element(By.CSS_SELECTOR, "a.toggleLocations")
                toggle_link.click()
                time.sleep(1)  # Allow hidden locations to appear

                multi_loc_container = driver.find_element(By.CSS_SELECTOR, "div.fluid-cols.fluid-cols--cols2")
                multi_loc_elements = multi_loc_container.find_elements(By.CSS_SELECTOR, "p.paragraph")
                locations = [loc.text.strip() for loc in multi_loc_elements if loc.text.strip()]
                if locations:
                    location_str = ", ".join(locations)
            except:
                # Fallback to single location
                try:
                    single_loc_elem = driver.find_element(By.CSS_SELECTOR, "div.fluid-cols.fluid-cols--cols2 p.paragraph")
                    location_str = single_loc_elem.text.strip()
                except:
                    location_str = "Unknown"

            # === Extract Deadline ===
            try:
                # Find all <p> tags and check if they contain the deadline phrase
                p_tags = driver.find_elements(By.TAG_NAME, "p")
                for p in p_tags:
                    if "Recruiting for this role ends" in p.text:
                        # Extract date part after the phrase
                        deadline_text = p.text
                        deadline_str = deadline_text.replace("Recruiting for this role ends", "").strip()
                        break
            except:
                deadline_str = "Unknown"

        except:
            print(f"⚠️ Could not load details for {title}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Default status
        status = "Not Applied"

        # Detect practice area
        practice = "General"
        if "audit" in title.lower():
            practice = "Audit"
        elif "tax" in title.lower():
            practice = "Tax"
        elif "advisory" in title.lower():
            practice = "Advisory"
        elif "technology" in title.lower() or "tech" in title.lower():
            practice = "Technology"

        # Row data
        row = {
            "Firm": "Deloitte",
            "Role Title": title,
            "Practice": practice,
            "Industry": "General",
            "Location": location_str,
            "Deadline": deadline_str,
            "Link": link,
            "Status": status
        }

        # Find first empty row in Google Sheet
        start_row = 4
        while sheet.cell(start_row, column_map["Firm"]).value:
            start_row += 1

        # Write row to Google Sheet
        for field, value in row.items():
            col = column_map.get(field)
            if col:
                sheet.update_cell(start_row, col, value)

        print(f"✅ Added: {title} → Row {start_row}")
        total_added += 1

    print(f"🚀 Finished! Added {total_added} internships to Google Sheet.")

finally:
    driver.quit()
    print("🛑 Browser closed.")
