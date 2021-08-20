from aomsdk import *
import pandas as pd
from tqdm import tqdm
import os

url_links = "/home/tskunara/Data Scraping/Article URL Lists/"

for filename in (os.listdir(url_links)):
    if filename.endswith(".csv"):

        news_source = pd.read_csv(url_links + filename)

        main_body_text = []
        title = []
        authors = []
        published_date = []
        summary = []
        iterations = 0
        batch_size = 100

        for url in tqdm(news_source["URL"].values):

            document = fetch_parsed_document(url)

            main_body_text.append(document.text)

            title.append(document.title)

            if not document.authors:
                authors.append(["No Author"])
            else:
                authors.append(document.authors)

            published_date.append(document.published_date)

            if document.summary is None:
                summary.append(document.title)
            else:
                summary.append(document.summary)

            iterations += 1

            if iterations % batch_size == 0:
                news_source["title"] = pd.DataFrame(title)
                news_source["text"] = pd.DataFrame(main_body_text)
                news_source["authors"] = pd.DataFrame(authors)
                news_source["published_date"] = pd.DataFrame(published_date)
                news_source["summary"] = pd.DataFrame(summary)

                news_source.to_csv(url_links + "updated_" + filename)

        news_source["title"] = pd.DataFrame(title)
        news_source["text"] = pd.DataFrame(main_body_text)
        news_source["authors"] = pd.DataFrame(authors)
        news_source["published_date"] = pd.DataFrame(published_date)
        news_source["summary"] = pd.DataFrame(summary)

        news_source.to_csv(url_links + "updated_" + filename)

# print(main_body_text)

