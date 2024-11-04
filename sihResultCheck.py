import requests
import re
import time
import threading
import winsound

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",  # Add this line to prevent caching
    "Pragma": "no-cache",          # Older HTTP/1.0 header to prevent caching
}

# Function to beep continuously
def continuous_beep(frequency=1000, duration=500):
    while not stop_event.is_set():
        winsound.Beep(frequency, duration)

# Event to control the stop condition
stop_event = threading.Event()

def ring_alarm():
    beep_thread = threading.Thread(target=continuous_beep)
    beep_thread.start()

    while True:
        user_input = input("Type 'stop' to stop the alarm: ")
        if user_input.lower() == "stop":
            stop_event.set()
            break

    beep_thread.join()
    print("Alarm stopped.")

def remove_comments(html):
    # Use the regex pattern to remove multiline comments
    return re.sub(r'(?s)<!--.*?-->', '', html)

def check_for_keyword(url, keyword):
    while True:
        try:
            response = requests.get(url, verify=False, headers=headers)  # Optional: verify=False to suppress SSL warnings
            html_content = response.text

            # Remove comments from HTML
            uncommented_html = remove_comments(html_content)


            # Directly check for the keyword in the uncommented HTML
            if keyword.lower() in uncommented_html.lower():
                print("Keyword found! Ringing alarm...")
                ring_alarm()  # Call the alarm function
                break  # Exit the loop if the keyword is found

            print("Keyword not found. Checking again in 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes before the next check

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(300)  # Wait before retrying in case of an error

if __name__ == "__main__":
    url_to_monitor = "https://sih.gov.in"
    keyword_to_find = "Batch 2"
    check_for_keyword(url_to_monitor, keyword_to_find)
