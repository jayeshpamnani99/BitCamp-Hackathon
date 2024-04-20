import requests
from bs4 import BeautifulSoup
import json




# Check if the request was successful (status code 200)
def get_contracts_from_single_page(url):
    response = requests.get(url)
    contracts_data = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")


        sections = soup.find_all("p", style="text-align: center;")
        for section in sections:

            title = section.find("strong").text.strip()
            section_contracts = []

            contracts = section.find_next_siblings("p")
            for contract in contracts:
                contract_data = contract.text.strip()
                section_contracts.append(contract_data)
            contracts_data[title] = section_contracts

    else:
        print("Failed to retrieve webpage:", response.status_code)
    print(contracts_data)
    with open("contracts.json", "a") as json_file:
        json.dump(contracts_data, json_file, indent=4)
        json_file.write(", ")

    print("Contract data saved to contracts.json")

def get_urls_from_main_page():
    for i in range(1,2):
        url = f"https://www.defense.gov/News/Contracts/?Page={i}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            article_urls = []
            for tag in soup.find_all('listing-titles-only'):
                article_url = tag.get('article-url')
                article_urls.append(article_url)
                get_contracts_from_single_page(article_url)
        print(article_urls)

get_urls_from_main_page()
