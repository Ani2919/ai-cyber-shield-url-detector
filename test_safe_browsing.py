import requests
import json

API_KEY = 'AIzaSyArjzKs9vN66fY_vZ-x0XSoxMLjTRhnsJM'  # <-- Paste your actual API key here

def check_url_safe_browsing(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client": {
            "clientId": "yourcompanyname",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    response = requests.post(endpoint, json=payload)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return

    result = response.json()
    if result:
        print("WARNING: The URL is unsafe!")
        print(json.dumps(result, indent=2))
    else:
        print("The URL is safe!")

if __name__ == "__main__":
    url = input("Enter a URL to check: ")
    check_url_safe_browsing(url)
