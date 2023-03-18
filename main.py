from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://calebgill.com",
    "https://calebgill.com:3001",
    "https://calebgill.com:443",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mortgage_rate")
async def get_mortgage_rate():
    # URL of the Freddie Mac website to scrape
    url = "https://www.freddiemac.com/pmms/pmms_archives"
    # Set user agent string to avoid getting blocked by server
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Make a GET request to the website
    response = requests.get(url, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table of historical rates
        table = soup.find("table", {"class": "hover stack"})

        # Find the row for the most recent week
        rows = table.find_all("tr")
        recent_row = rows[1]

        # Extract the date and rate from the row, then clean up the rate data
        cells = recent_row.find_all("td")
        date = cells[0].text.strip()
        rate = cells[1].text.strip()
        clean_rate = rate.split()[-1]
        
        return {"date": date, "mortgage_rate": clean_rate}
    
    # If the response was not successful, return an error message
    return {"error": "Failed to retrieve mortgage rate."}
