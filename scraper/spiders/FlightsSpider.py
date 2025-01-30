import json
import os
import scrapy
import re
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.items import FlightItem


config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

SRC_AIRPORTS = config['src_airports']
SRC_AIRPORT_QUERY = "&srcAirport=Lodz+[LCJ]+(" + "%2C".join(SRC_AIRPORTS) + ")"
DST_AIRPORTS = config['dst_airports']
date_range = config['date_range']
duration_range = config['duration_range']
currency = config['currency']

# Define top X results of each destination
top_results = 5


# Spider with data normalization
class FlightsSpider(scrapy.Spider):
    name = "FlightsSpider"
    allowed_domains = ["azair.cz"]
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
    }
    scrape_date = datetime.now()

    @staticmethod
    def urls_to_scrape():
        urls = []

        for dst_code, dst_param in DST_AIRPORTS.items():
            url = (f"https://www.azair.cz/azfin.php?tp=0&searchtype=flexi"
                   f"{SRC_AIRPORT_QUERY}"
                   f"&dstAirport=[{dst_param}]"
                   f"&adults=1"
                   f"&children=0"
                   f"&infants=0"
                   f"&minHourStay=0%3A45"
                   f"&maxHourStay=23%3A20"
                   f"&minHourOutbound=0%3A00"
                   f"&maxHourOutbound=24%3A00"
                   f"&minHourInbound=0%3A00"
                   f"&maxHourInbound=24%3A00"
                   f"&dstFreeAirport="
                   f"&depdate={date_range['dep_date']}"
                   f"&arrdate={date_range['arr_date']}"
                   f"&minDaysStay={duration_range['min_day_stay']}"
                   f"&maxDaysStay={duration_range['max_day_stay']}"
                   f"&nextday=0"
                   f"&autoprice=true"
                   f"&currency={currency}"
                   f"&wizzxclub=false"
                   f"&flyoneclub=false"
                   f"&blueairbenefits=false"
                   f"&megavolotea=false"
                   f"&schengen=false"
                   f"&transfer=false"
                   f"&samedep=true"
                   f"&samearr=true"
                   f"&dep0=true"
                   f"&dep1=true"
                   f"&dep2=true"
                   f"&dep3=true"
                   f"&dep4=true"
                   f"&dep5=true"
                   f"&dep6=true"
                   f"&arr0=true"
                   f"&arr1=true"
                   f"&arr2=true"
                   f"&arr3=true"
                   f"&arr4=true"
                   f"&arr5=true"
                   f"&arr6=true"
                   f"&maxChng=0"
                   f"&isOneway=return"
                   f"&resultSubmit=Search")
            urls.append(url)

        return urls

    @staticmethod
    def normalize_date(date_str):
        return datetime.strptime(date_str, '%a %d/%m/%y').strftime('%Y-%m-%d')

    start_urls = urls_to_scrape()

    def parse(self, response, scraping_date=scrape_date):
        result_list = response.css('div.list > div.result')[:top_results]

        for result in result_list:
            price_total = result.css('div.totalPrice span.tp::text').get()
            price_total = price_total.split()[0]

            dates = result.css('span.date::text').getall()
            date_of_departure = self.normalize_date(dates[0])
            date_of_return = self.normalize_date(dates[1])

            airports_codes = result.css('span.from span.code::text').getall()
            departure_airport_outbound = airports_codes[0]
            arrival_airport_outbound = airports_codes[2]
            departure_airport_return = airports_codes[3]
            arrival_airport_return = airports_codes[1]

            dep_times = result.css('span.from strong::text').getall()
            dep_time_outbound = dep_times[0]
            dep_time_return = dep_times[1]

            arr_times = result.css('span.to::text').getall()
            arr_time_outbound = arr_times[0].split()[0]
            arr_time_return = arr_times[4].split()[0]

            flights_no = result.css('a[title="flightradar24"]::text').getall()
            flight_no_outbound = flights_no[0]
            flight_no_return = flights_no[1]

            flight_durations = result.css('span.durcha::text').getall()
            flight_duration_outbound = flight_durations[0].split()[0]
            flight_duration_return = flight_durations[1].split()[0]

            price_there_and_back = result.css('span.subPrice::text').getall()
            price_outbound = price_there_and_back[0].split()[0]
            price_return = price_there_and_back[1].split()[0]

            airlines = result.css('span.airline::text').getall()
            airline_outbound = airlines[0]
            airline_return = airlines[1]

            length_of_stay_text = result.css('span.lengthOfStay::text').get()
            length_of_stay = re.search(r'(\d+)', length_of_stay_text).group(1)

            flight_item = FlightItem()

            flight_item['scrape_date'] = scraping_date
            flight_item['price_total'] = price_total
            flight_item['price_outbound'] = price_outbound
            flight_item['price_return'] = price_return
            flight_item['date_of_departure'] = date_of_departure
            flight_item['date_of_return'] = date_of_return
            flight_item['length_of_stay'] = length_of_stay
            flight_item['airline_outbound'] = airline_outbound
            flight_item['flight_no_outbound'] = flight_no_outbound
            flight_item['departure_airport_outbound'] = departure_airport_outbound
            flight_item['arrival_airport_outbound'] = arrival_airport_outbound
            flight_item['dep_time_outbound'] = dep_time_outbound
            flight_item['arr_time_outbound'] = arr_time_outbound
            flight_item['flight_duration_outbound'] = flight_duration_outbound
            flight_item['airline_return'] = airline_return
            flight_item['flight_no_return'] = flight_no_return
            flight_item['departure_airport_return'] = departure_airport_return
            flight_item['arrival_airport_return'] = arrival_airport_return
            flight_item['dep_time_return'] = dep_time_return
            flight_item['arr_time_return'] = arr_time_return
            flight_item['flight_duration_return'] = flight_duration_return

            yield flight_item


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FlightsSpider)
    process.start()
