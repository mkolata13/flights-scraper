import os
import glob
import pandas as pd
import matplotlib.pyplot as plt


def generate_price_trends(data_dir="data/"):
    file_pattern = os.path.join(data_dir, "flights_*.csv")
    csv_files = glob.glob(file_pattern)

    all_data = pd.DataFrame()

    for file in csv_files:
        data = pd.read_csv(file)
        all_data = pd.concat([all_data, data], ignore_index=True)

    all_data['scrape_date'] = pd.to_datetime(all_data['scrape_date'])
    all_data['date_of_departure'] = pd.to_datetime(all_data['date_of_departure'])
    all_data['date_of_return'] = pd.to_datetime(all_data['date_of_return'])

    grouped = all_data.groupby(['arrival_airport_outbound', 'scrape_date'])['price_total'].min().reset_index()

    destination_airports = grouped['arrival_airport_outbound'].unique()

    for airport in destination_airports:
        airport_data = grouped[grouped['arrival_airport_outbound'] == airport]

        # Plotting price trend based on scrape date
        plt.figure(figsize=(10, 6))
        plt.plot(airport_data['scrape_date'], airport_data['price_total'], marker='o')
        plt.title(f"Price Trend for {airport}")
        plt.xlabel("Scrape Date")
        plt.ylabel("Cheapest Total Price")
        plt.grid()
        plt.tight_layout()

        output_file = os.path.join(f"./results/price_trend_{airport}.png")
        plt.savefig(output_file)
        plt.close()

    print("Charts have been saved.")
