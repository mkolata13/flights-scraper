from datetime import datetime

from itemadapter import ItemAdapter


class FlightScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field in item.fields:
            adapter[field] = self.convert_field(field, adapter[field])
        return item

    @staticmethod
    def convert_field(field, value):
        try:
            if field == "scrape_date" and isinstance(value, datetime):
                return value.isoformat()
            if field in {"date_of_departure", "date_of_return"} and value:
                return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
            if field in {"dep_time_outbound", "arr_time_outbound", "dep_time_return", "arr_time_return"} and value:
                return datetime.strptime(value, "%H:%M").strftime("%H:%M")
            if field in {"price_outbound", "price_return", "price_total"} and value:
                return float(value)
            if field == "length_of_stay" and value:
                return int(value)
        except Exception as e:
            print(f"Error converting field {field}: {e}")
        return value
