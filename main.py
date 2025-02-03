# Triggering Railway redeployment

import requests
from bs4 import BeautifulSoup

nick = "Alex"  # Replace with any real player nickname
url = f"https://bluepanel.bugged.ro/profile/{nick}"

# Fake browser headers to prevent being blocked
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ Successfully accessed the profile page!")
else:
    print("❌ Failed to access the page. Status Code:", response.status_code)
    exit()

# Print the first 1000 characters of the HTML
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify()[:1000])
