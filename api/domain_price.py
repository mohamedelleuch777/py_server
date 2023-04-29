import requests

# Replace "example.com" with the domain name you want to check
domain = "kartaj.ai"

# GoDaddy API endpoint for obtaining domain availability information
url = f"https://api.godaddy.com/v1/domains/available?domain={domain}"

# API headers containing authorization and content type information
headers = {
    "Authorization": f"sso-key eo1nGwcz6HHZ_UR9M8YNXJhvW5eS428rJFg:PMVmPf6r3PeQcnJ2QG1uaw",
    "Content-Type": "application/json"
}

# Query the GoDaddy API to obtain the availability status of the domain
response = requests.get(url, headers=headers)

# Parse the response JSON to obtain the availability status
response_json = response.json()
if response_json["available"]:
    print(f"The domain {domain} is available")
else:
    print(f"The domain {domain} is taken")
