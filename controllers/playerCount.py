import requests
import re

def PlayerCount(game):
    # Send an HTTP GET request to fetch metrics
    response = requests.get('http://10.196.242.62/metrics')

    # Check if the request was successful
    if response.status_code == 200:
        # Extract lines containing "Castle Clicker"
        lines = response.text.splitlines()
        regex = rf'title="{game}"'
        lines = [line for line in lines if re.search(regex, line)]

        # Use regex to remove everything before and including the last '}'
        result = [re.sub(r'.*} ', '', line) for line in lines]

        try:
            count = int(result[0])
        except:
            print("Failed to fetch player count")
            count = None
        # Print or return the result
        return count
    else:
        return f"Failed to fetch metrics. Status code: {response.status_code}"
