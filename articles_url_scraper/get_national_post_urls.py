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

filename = "national_post_urls.csv"
with open(filename, 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)

for keyword in keywords:
    print("Scanning National Post for {}".format(keyword))
    url_link = "https://nationalpost.com/search/?search_text={}&date_range=-365d&sort=score".format(keyword)  # posts from the last 1 year

    driver = webdriver.Firefox()
    driver.get(url_link)
    #changed = 1
    base_url = "https://nationalpost.com"
    while len(urls)<4000 :
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_containers = soup.find_all("div", {"class", "article-card__details"})
        for i in article_containers:
            url = [base_url + i.find("a").get("href"), "National Post", keyword, "nationalpost.com"]
            urls.append(url)
            
            
        print(len(urls))
        # reached end of pages
        try:
            driver.find_element_by_class_name("pagination__link").send_keys("\n")
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

