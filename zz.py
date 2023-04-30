import pandas as pd
import requests
from bs4 import BeautifulSoup

# Set the URL of the webpage to scrape
url = 'https://www.espn.com/mlb/stats'

# Send an HTTP request to the URL and get the HTML response
response = requests.get(url)

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the MLB statistics
table = soup.find('table', {'class': 'Table Table--align-right Table--fixed Table--fixed-left'})

# Load the table data into a Pandas DataFrame
df = pd.read_html(str(table))[0]

# Print the first five rows of the DataFrame
print(df.head())
