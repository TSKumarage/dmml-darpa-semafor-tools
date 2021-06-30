from aomsdk import *

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

directory = "/home/tskunara/Evaluation1/Pristine_Articles/*.tar.gz"
tmpdir = "/home/tskunara/Evaluation1/Pristine_Articles/temp/"
label = 0

grover_headers = ['title', 'text', 'authors', 'Topic label', 'url',
       'publish_date', 'domain']

packages = glob.glob(directory, recursive=True)

articles = []

for p in packages:
  #print(p)
  tar = tarfile.open(p, "r")
  json = [m for m in tar.getmembers() if m.name.endswith('json')]
  tar.extractall(tmpdir, members=json)
  document = AOMDocument.load_aom_from_json(os.path.join(tmpdir, json[0].name))
  main_body_text = document.text
  articles.append([main_body_text, label])

train_df = pd.DataFrame(articles, columns=['text', 'label'])

jsonl_data = train_df.to_json(orient='records', lines=True)

with open("/home/tskunara/Evaluation1/Manipulated_Articles/" +"eval1.real.jsonl", "w") as text_file:
  text_file.write(jsonl_data)