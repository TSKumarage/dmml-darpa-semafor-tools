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

filename = "afghanistan_times_urls.csv"
with open(filename, 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)

for keyword in keywords:
    print("Scanning Afghanistan Times for {}".format(keyword))
    url_link = "http://www.afghanistantimes.af/?s={}".format(keyword)

    driver = webdriver.Firefox()
    driver.get(url_link)

    pre_soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        page = pre_soup.find("span", {"class", "pages"})
        page_text = page.text
        end_page_num = page_text.strip().split()[-1]
    except Exception as e:
        print(e)
        continue
    page_num = 1
    try:
        while len(urls)<4000 and page_num <= int(end_page_num):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            article_containers = soup.find_all("h2", {"class", "post-box-title"})
            for i in article_containers:
                url = [i.find("a").get("href"), "Afghanistan Times", keyword, "afghanistantimes.af"]
                urls.append(url)
            print(len(urls))
            page_num+=1
            # reached end of pages

            
            print("Page {} of {}", page_num, end_page_num)
            new_url = "http://www.afghanistantimes.af/page/"+str(page_num)+"/?s={}".format(keyword)
            driver.get(new_url)
    except Exception as ee:
        print(ee)

        with open(filename, "a") as url_file:
            csvwriter = csv.writer(url_file)
            csvwriter.writerows(urls)
        urls = []
        driver.quit()


    with open(filename, "a") as url_file:
        csvwriter = csv.writer(url_file)
        csvwriter.writerows(urls)

