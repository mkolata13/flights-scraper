from charts.charts import generate_price_trends
from scraper.spiders.FlightsSpider import run_spider

if __name__ == '__main__':
    run_spider()
    generate_price_trends()
