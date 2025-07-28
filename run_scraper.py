from src.data.scrape import scrape_tw_rackets

if __name__ == "__main__":
    scrape_tw_rackets(
        shop_all_URL = "https://www.tennis-warehouse.com/TennisRacquets.html",
        file_name = "Scraped Racquet Data",
        datashelf = True,
        collection_name = "racquets",
        tag = "raw",
        message = "Raw racquet information scraped from each brand's page on tenniswarehouse.com."
    )
