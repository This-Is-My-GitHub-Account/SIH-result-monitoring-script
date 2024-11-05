import requests
import re
import time
import threading
import winsound


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
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

def check_for_keyword(url, keyword, threshold):
    while True:
        try:
            response = requests.get(url, verify=False, headers=headers)
            html_content = response.text

            # Remove comments from HTML
            uncommented_html = remove_comments(html_content)

            # Count occurrences of the keyword in the uncommented HTML
            count = uncommented_html.lower().count(keyword.lower())

            if count > threshold:
                print(f"Keyword found {count} times! Ringing alarm...")
                ring_alarm()
                break  # Exit the loop if the threshold is exceeded

            print(f"Keyword found {count} times. Checking again in 2 minutes...")
            time.sleep(120)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(300)

if __name__ == "__main__":
    url_to_monitor = "https://sih.gov.in/screeningresult"
    keyword_to_find = "The Shetkari Shikshan Mandals Padma Vasantdada Patil Institute of Technology, Bavdhan Khurd,Pune 38"
    threshold_count = 2
    check_for_keyword(url_to_monitor, keyword_to_find, threshold_count)
