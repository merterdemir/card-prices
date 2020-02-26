#! /usr/bin/env python3
"""
Author: Mert Erdemir

How to Use:

You can put this file in the same directory with your
script, and import it as:

    from get_prices import GetPrices

Then, initialize the GetPrices object with correct parameters:
    
    test = GetPrices()

Next, call the crawl function to initiate the process:

    test.crawl_prices()

You are done!

OR

You can change the object in main function with the correct parameters
and directly run this script as:

    $> python3 get_prices.py

        OR

    $> ./get_prices.py

Have fun!
"""

import os
import sys
import csv
import json
from urllib.request import urlopen
from urllib.parse import quote

class GetPrices():
    def __init__(self, file_path="YGO_Collection.csv", 
                       price_mode="high", 
                       output="prices.csv", 
                       target_field="Price (FE)"):
        """
        :param file_path: Absolute path for the dataset
        :param price_mode: Price type -> high, low, average
        :param output: New CSV file with prices. Just file name.
        :param target_field: Which field to write the prices
        """
        self.file         = None
        self.file_path    = file_path
        self.price_mode   = price_mode
        self.target_field = target_field
        self.main_url     = "http://yugiohprices.com/api/get_card_prices/"
        self.fieldnames   = ["name", "code", "price"]

        if (os.path.exists(self.file_path)):
            self.file       = open(self.file_path, "r")
            self.fieldnames = self.file.readline().split(",")
            self.file_csv   = csv.DictReader(self.file, fieldnames=self.fieldnames)
        
        self.output     = open(os.path.join(os.getcwd(), output), "w+")
        self.output_csv = csv.DictWriter(self.output, fieldnames=self.fieldnames)
        self.output_csv.writeheader()

    def _match_price(self, card_name, code):
        """
        - Looks the price in API.
        - If it cannot find any price, assigns -1.
        - Chooses prices according to self.price_mode.
        - Looks the code given for the card in the input file.
        """
        link = (self.main_url + card_name).replace(" ", "%20")
        with urlopen(link) as response:
            price = -1
            data = json.loads(response.read())
            if data['status'] == "success":
                for entry in data['data']:
                    if entry["print_tag"] == code:
                        price = entry["price_data"]["data"]["prices"][self.price_mode]
                        break
            return price

    def crawl_prices(self):
        """
        Crawls all of the prices for the cards in given input file.
        Writes all prices to the given output file.
        """
        print("Crawling prices...")
        for row in self.file_csv:
            print("")
            card_name = row["Card Name"]
            code      = row["Code"]
            price     = self._match_price(card_name, code)
            new_row   = dict(zip(list(row.keys()), [row[key] for key in row]))
            new_row[self.target_field] = price
            self.output_csv.writerow(new_row)
            print("Card: {} - Code: {} - Price({}): {}".format(card_name, 
                                                               code, 
                                                               self.price_mode, 
                                                               price))
        print("Done!")
        print("Files are being closed.")
        self.file.close()
        self.output.close()
        print("Files are closed.")

def main():
    test = GetPrices()
    test.crawl_prices()

if __name__ == "__main__":
    main()