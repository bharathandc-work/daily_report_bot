
import pyautogui
import pyperclip
import subprocess
import time
import os
import re
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

WEATHER_URL = (
    "https://www.accuweather.com/en/in/chennai/"
    "206671/weather-forecast/206671"
)

OUTPUT_DIR = "/Users/bharath-7555/Documents/learn/day 3/DailyReports"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app_name):

    print(f"Opening {app_name}...")

    subprocess.Popen(["open", "-a", app_name])

    time.sleep(8)


# ==========================================
# FETCH WEATHER FROM ACCUWEATHER
# ==========================================

def fetch_weather():

    print("\nOpening Google Chrome...")

    open_application("Google Chrome")

    # Navigate to AccuWeather
    pyautogui.hotkey("command", "l")

    pyperclip.copy(WEATHER_URL)
    pyautogui.hotkey("command", "v")

    pyautogui.press("enter")

    print("Loading AccuWeather Chennai page...")

    time.sleep(15)

    # Copy webpage text
    pyautogui.hotkey("command", "a")
    pyautogui.hotkey("command", "c")

    time.sleep(3)

    page_content = pyperclip.paste().strip()

    if not page_content:
        raise Exception("Unable to copy AccuWeather page content.")

    print("Weather page content copied.")

    # Extract relevant weather information
    weather_data = extract_weather(page_content)

    print("\nFetched Weather Information:")
    print(weather_data)

    return weather_data


# ==========================================
# EXTRACT IMPORTANT WEATHER INFORMATION
# ==========================================

def extract_weather(page_content):

    lines = [
        line.strip()
        for line in page_content.splitlines()
        if line.strip()
    ]

    # Find current weather section
    start_index = None

    for i, line in enumerate(lines):

        if "Current Weather" in line:
            start_index = i
            break

    if start_index is not None:

        # Capture a limited portion of current weather details
        weather_lines = lines[start_index:start_index + 15]

        return " | ".join(weather_lines)

    # Fallback: retain a limited amount of copied page content
    return " | ".join(lines[:15])


# ==========================================
# GENERATE REPORT DETAILS
# ==========================================

def generate_report_data(weather_data):

    current_time = datetime.now()

    report_date = current_time.strftime("%Y-%m-%d")

    report_datetime = current_time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    comment = "Chennai weather status captured from AccuWeather."

    return (
        report_date,
        report_datetime,
        weather_data,
        comment
    )


# ==========================================
# CREATE REPORT USING APPLE NUMBERS
# ==========================================

def create_numbers_report(
    report_date,
    report_datetime,
    weather_data,
    comment
):

    print("\nOpening Apple Numbers...")

    open_application("Numbers")

    # Create new spreadsheet
    pyautogui.hotkey("command", "n")

    time.sleep(5)

    # Select Blank template
    pyautogui.press("enter")

    time.sleep(6)

    # Prepare spreadsheet data
    spreadsheet_data = (
        "Date & Time\tWeather Information\tComment\n"
        f"{report_datetime}\t{weather_data}\t{comment}"
    )

    # Paste data into Numbers
    pyperclip.copy(spreadsheet_data)

    # New blank Numbers spreadsheet normally starts
    # with its first table cell selected.
    pyautogui.hotkey("command", "v")

    time.sleep(5)

    # ======================================
    # SAVE NUMBERS FILE
    # ======================================

    filename = f"daily_report_{report_date}.numbers"

    filepath = os.path.join(OUTPUT_DIR, filename)

    print("\nSaving Numbers report...")

    pyautogui.hotkey("command", "s")

    time.sleep(4)

    # Enter filename in Save dialog
    pyperclip.copy(filename)
    pyautogui.hotkey("command", "a")
    pyautogui.hotkey("command", "v")

    time.sleep(2)

    # Select output folder
    pyautogui.hotkey("command", "shift", "g")

    time.sleep(2)

    pyperclip.copy(OUTPUT_DIR)
    pyautogui.hotkey("command", "v")

    pyautogui.press("enter")

    time.sleep(3)

    # Confirm save
    pyautogui.press("enter")

    time.sleep(5)

    # ======================================
    # TAKE SCREENSHOT
    # ======================================

    screenshot_path = os.path.join(
        OUTPUT_DIR,
        f"daily_report_{report_date}_screenshot.png"
    )

    pyautogui.screenshot().save(screenshot_path)

    print("\nReport saved successfully!")

    print("Numbers File:", filepath)

    print("Screenshot:", screenshot_path)

    return filepath, screenshot_path


# ==========================================
# MAIN AUTOMATION
# ==========================================

def main():

    print("=" * 55)
    print("DAILY WEATHER REPORT AUTOMATION")
    print("=" * 55)

    try:

        # STEP 1: Fetch AccuWeather information
        weather_data = fetch_weather()

        # STEP 2: Generate date and time
        (
            report_date,
            report_datetime,
            weather_data,
            comment
        ) = generate_report_data(weather_data)

        # STEP 3: Create Numbers report
        numbers_file, screenshot_file = create_numbers_report(
            report_date,
            report_datetime,
            weather_data,
            comment
        )

        print("\n" + "=" * 55)
        print("AUTOMATION COMPLETED SUCCESSFULLY")
        print("=" * 55)

    except Exception as error:

        print("\nAUTOMATION FAILED!")
        print("Reason:", error)


if __name__ == "__main__":
    main()
