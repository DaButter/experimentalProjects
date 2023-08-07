import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt

def formatToJson(response):
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the table rows (tr) containing data-hours attribute
    table_rows = soup.find_all('tr', {'data-hours': True})

    # initialize an empty list to store the data in JSON format
    data_list = []

    # loop through each table row and extract the data
    for row in table_rows:
        # extract data from the row
        hour_range = row.th.text.strip()
        prices = [float(td.text) for td in row.find_all('td', class_='price')]

        # create a dictionary for each row and add it to the data list
        data_list.append({
            'hour_range': hour_range,
            'today': prices[0],
            'tomorrow': prices[1]
        })

    # convert the data_list to JSON format
    json_data = json.dumps(data_list, indent=2)
    return json_data


def visualizeNordpool(json_data):
    print(json_data)

    data = json.loads(json_data)

    # extracting the hour ranges, today prices, and tomorrow prices
    hour_ranges = [entry["hour_range"] for entry in data]
    today_prices = [entry["today"] for entry in data]
    tomorrow_prices = [entry["tomorrow"] for entry in data]

    # plotting the data as a line plot with connected dots
    plt.figure(figsize=(10, 6))
    plt.plot(hour_ranges, today_prices, marker='o', label="Today's Price", color="b")
    plt.plot(hour_ranges, tomorrow_prices, marker='o', label="Tomorrow's Price", color="r")

    plt.xlabel('Hour Range')
    plt.ylabel('Price')
    plt.title('Nordpool Electroenergy Prices')
    plt.legend(loc='upper right')

    plt.grid(True)

    # add text annotations (value boxes) for each data point
    for i, today_price in enumerate(today_prices):
        plt.text(hour_ranges[i], today_price, f"{today_price:.4f}", ha='center', va='bottom', color="b", fontsize=10)

    for i, tomorrow_price in enumerate(tomorrow_prices):
        plt.text(hour_ranges[i], tomorrow_price, f"{tomorrow_price:.4f}", ha='center', va='bottom', color="r", fontsize=10)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    url = 'https://nordpool.didnt.work/?vat'
    nordpool_response = requests.get(url)

    # json_data = formatToJson(nordpool_response)

    # for test purposes, using a given json mock
    with open('nordpool_data_example.json', 'r', encoding='utf-8') as file:
        json_data = file.read()

    # Print the JSON data
    visualizeNordpool(json_data)




