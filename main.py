import requests
from bs4 import BeautifulSoup
import gspread
from datetime import datetime
import time

class TrustPilotScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")

        total_rating = float(soup.find('span', class_='typography_heading-m__T_L_X typography_appearance-default__AAY17').text)
        total_reviews = int(''.join(filter(str.isdigit, soup.find('p', class_='typography_body-l__KUYFJ typography_appearance-default__AAY17').text)))

        star_tags = soup.find_all('label', class_='styles_row__wvn4i')
        star_ratings_numbers = [int(tag['title'].split(' ')[0].replace(',', '')) for tag in star_tags if tag.has_attr('title')]

        star_ratings_percentage = [int(tag.text.strip('%')) / 100 for tag in soup.find_all('p', class_='typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_percentageCell__cHAnb')]

        return {
            "total_rating": total_rating,
            "total_reviews": total_reviews,
            "star_ratings_numbers": star_ratings_numbers,
            "star_ratings_percentage": star_ratings_percentage
        }

def main():
    while True:
        try:
            url = "https://www.trustpilot.com/review/www.google.com"
            scraper = TrustPilotScraper(url)
            data = scraper.scrape_data()

            results = [
                data["total_rating"],
                data["total_reviews"],
                *data["star_ratings_numbers"],
                str(datetime.now())
            ]

            sa = gspread.service_account(filename='prpillartest-e1e954c79ce9.json')
            sheets = sa.open('PRpillar')
            worksheet = sheets.worksheet('Google Data')
            worksheet.append_row(results)

            print('Data successfully scraped and uploaded.')
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        time.sleep(3600)

main()
