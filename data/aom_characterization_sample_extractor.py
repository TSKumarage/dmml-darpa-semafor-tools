from aomsdk import *

import aomsdk

import os
import pandas as pd
import re
from dateutil import parser
from datetime import datetime
from tqdm import tqdm

import os
import csv
import glob
import random
import shutil
import tarfile
import tempfile
import argparse
from pathlib import Path

print(aomsdk.__version__)

path = "/home/tskunara/Eval 3.2/Eval 3.2.1/"
directory = "/home/tskunara/Eval2/Text_And_Images/*.tar.gz"
tmpdir = "/home/tskunara/Eval 3.2/Eval 3.2.1/temp/"

# label = 1

col_names = ['probe_id', 'text', 'loc_text', 'article_title', 'article_authors', 'article_source', 'article_pubdate', 'article_url', 'article_tags',
                           'article_summary']

articles = []

sub_content = os.listdir(path)

count = 0

for item in tqdm(sub_content, desc="Sub-directory processing"):

    if os.path.isdir(path + item):

        directory = path + item + "/*.tar.gz"

        filename = "input-eg-fb8d38551ac7874eff102fdae95bd7a22e57b233111446f494db23e022741301.json"

        input_eg =  path + item +"/input-eg-"+ item+".json"

        text_spans = []

        with open(input_eg, 'r') as filehandle:

            data = json.load(filehandle)

            # Iterating through the json
            # list
            for node in data['nodes']:

                if node['nodeType'] == "EvAomLocIdNode":
                    res = json.loads(node['aomLoc'])

                    start_id = res['start']['index']

                    end_id = res['stop']['index']

                    text_spans.append((start_id, end_id))

        packages = glob.glob(directory, recursive=True)

        loc_texts = []

        for p in packages:
          probe_id = str(p).split("/")[-1]
          tar = tarfile.open(p, "r")
          json = [m for m in tar.getmembers() if m.name.endswith('json')]
          tar.extractall(tmpdir, members=json)
          document = AOMDocument.load_aom_from_json(os.path.join(tmpdir, json[0].name))
          main_body_text = document.text

          for span in text_spans:
              loc_texts.append(main_body_text[span[0]:span[1]+1])

          article_title = document.title
          article_source = document.source
          article_url = document.source_uri
          article_authors = document.authors
          article_pubdate = document.published_date
          article_summary = document.summary
          article_tags = document.tags

          articles.append([probe_id, main_body_text, loc_texts, article_title, article_authors, article_source, article_pubdate, article_url, article_tags,
                           article_summary])

          count += 1

data_df = pd.DataFrame(articles, columns=col_names)

print("Original size:", len(data_df))
print(count)

data_df = data_df.drop_duplicates(subset=['text'])


print("Size of the final dataset", len(data_df))

data_df.to_csv(path +"sample.csv", index=False)
