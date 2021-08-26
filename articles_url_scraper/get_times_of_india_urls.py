from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["URL", "Source", "Keyword/Topic", "Source URL"]

keywords = ["Climate Change", "COVID 19", "Military Vehicles"]

filename = "times_of_india_urls.csv"
with open(filename, 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)

urls = []

for keyword in keywords:
    print("Scanning Times of India for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0
        web_addresses = []

        if (keyword == "Climate Change"):
            web_addresses.append("https://timesofindia.indiatimes.com/topic/climate-change/{}".format(page))

        # Times of india has a covid landing page and multiple subpages per location. This is all the sublocations
        elif (keyword == "COVID 19"):
            if (page > 1):
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/delhi/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/bangalore/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/hyderabad/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/kolkata/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/mumbai/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/world/{}".format(page))
            else:
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/delhi/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/bangalore/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/hyderabad/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/kolkata/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/mumbai/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/world/")
        elif (keyword == "Military Vehicles"):
            web_addresses.append("https://timesofindia.indiatimes.com/topic/Military-Vehicles/{}".format(page))

        for web_address in web_addresses:
            print(web_address)
            r = requests.get(web_address)
            soup = BeautifulSoup(r.content, "html.parser")

            if (keyword != "COVID 19"):
                article_containers = soup.find_all("li", {"class": "article"})
            else:
                article_containers = soup.find("ul", {"class": "list5 clearfix"}).find_all("span", {"class": "w_tle"})

            for i in article_containers:
                if (keyword == "COVID 19"):
                    url_text = "https://timesofindia.indiatimes.com{}".format(i.find("a").get("href"))
                    url = [url_text, "Times of India", keyword, "timesofindia.indiatimes.com"]
                    if url not in urls:
                        urls.append(url)
                        changed = 1
                else:
                    if ("2021" in i.text):
                        url_text = "https://timesofindia.indiatimes.com{}".format(i.find("a").get("href"))
                        url = [url_text, "Times of India", keyword, "timesofindia.indiatimes.com"]
                        if url not in urls:
                            urls.append(url)
                            changed = 1


with open(filename, "a") as url_file:
    csvwriter = csv.writer(url_file)
    csvwriter.writerows(urls)
