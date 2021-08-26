## for national post: https://nationalpost.com/search/?search_text=covid19&date_range=-365d&sort=score


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

filename = "norway_today_urls.csv"
with open(filename, 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)

for keyword in keywords:
    print("Scanning Norway Today for {}".format(keyword))
    url_link = "https://norwaytoday.info/?s={}".format(keyword)  

    driver = webdriver.Firefox()
    driver.get(url_link)
    #changed = 1
    base_url = "https://norwaytoday.info"
    while len(urls)<4000 :
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_containers = soup.find_all("h3", {"class", "entry-title content-list-title"})
        for i in article_containers:
            url = [i.find("a").get("href"), "Norway Today", keyword, "norwaytoday.info"]
            print(url)
            urls.append(url)
            
            
        print(len(urls))
        # reached end of pages
        try:
            driver.find_element_by_link_text("»").send_keys("\n")
            print("next page successful")
        except Exception as e:
            print(e)
            break
    with open(filename, "a") as url_file:
        csvwriter = csv.writer(url_file)
        csvwriter.writerows(urls)
    urls = []
    driver.quit()

waste_url = []  # saves memory

