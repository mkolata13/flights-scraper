# Flight Price Scraper

This project scrapes flight prices from azair.cz for selected destinations and airports. It saves the data to a CSV file and generates price trend charts.

## Usage

1. **Set up airports and destinations in `config.json`:**
   Define the source and destination airports, as well as the date range and stay duration.

   - Source airports: `WAW`, `WMI`, `KTW`, `WRO`, `POZ` (Base airport: Lodz LCJ)
   - Destination airports: Malta (MLA), Tbilisi (TBS), Lisbon (LIS), Porto (OPO), Madeira (FNC), etc.
   - Date range: Departure date from "1.7.2025" to Arrival date "31.8.2025".
   - Stay duration: Minimum 5 days, Maximum 8 days.

2. **Run the scraper:**
   Use the following command to start scraping flight prices to csv and generate price trend charts:

   ```bash
   python -m scraper.run
   ```