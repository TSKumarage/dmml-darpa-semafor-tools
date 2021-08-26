from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["URL", "Source", "Keyword/Topic", "Source URL"]
keywords = ["Climate Change", "COVID 19", "Military Vehicles", "coronavirus", "civilian casualty"]
urls = []
waste_url = []

filename = "straits_times_urls.csv"
with open(filename, 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)

for keyword in keywords:
    print("Scanning Straits Times for {}".format(keyword))
    url_link = "https://www.straitstimes.com/search?searchkey={}".format(keyword)

    driver = webdriver.Firefox()
    driver.get(url_link)
    changed = 1

    while (changed) and len(urls)<4000:
        changed = 0
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_containers = soup.find_all("div", {"class", "queryly_item_row"})
        for i in article_containers:
            if ("2021" in i.text and i.find("a").get("href") not in urls):
                url = [i.find("a").get("href"), "Straits Times", keyword, "straitstimes.com"]
                urls.append(url)
                changed = 1
            elif ("2020" in i.text and i not in waste_url):
                waste_url.append(i)
                changed = 1
        print(len(urls))
        # reached end of pages
        try:
            driver.find_element_by_css_selector('#resultdata > a:nth-child(22)').send_keys("\n")
        except Exception as e:
            print(e)
            break
    with open(filename, "a") as url_file:
        csvwriter = csv.writer(url_file)
        csvwriter.writerows(urls)
    urls = []
    driver.quit()

waste_url = []  # saves memory

