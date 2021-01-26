import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
from itertools import islice
import os

json_file_no = 0

def scrape_base_wiki_page(start_url):
    response = requests.get(url=start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = 'https://en.wikipedia.org'
    urls = [a['href'] for a in soup.find_all('a', href=re.compile(r"^/wiki/List"))]
    with (open('urls_list.txt', 'w')) as url_file:
        for url in urls:
            url_file.write(str(base_url) + str(url)+'\n')
            # url_file.write(str(url).replace('/wiki/', '').replace('_', ' ')+'\n')
    scrape_wiki_tables()


def scrape_wiki_tables():
    with (open('urls_list.txt', 'r')) as url_file:
        urls_10 = [next(url_file).strip() for x in range(10)]
    print(urls_10)

    for url in urls_10:

        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        tables = soup.find_all('table', {'class': lambda value: value and value.startswith(("sortable wikitable", "wikitable"))})
        # print(len(tables))
        for table in tables:
            table_df = pd.read_html(str(table))
            table_df = table_df[0]

            # Capture the caption of the table, useful to add context to pure numerical columns
            try:
                table_caption = table.find('caption').text
            except:
                # If no caption, use the page title
                table_caption = soup.find('h1').text

            if table_df.columns.nlevels > 1:
                # Flatten multilevel headers by merging levels
                table_df.columns = [' '.join(col).strip() for col in table_df.columns.values]

            # If only one column in the table skip the table
            if len(table_df.columns) < 2:
                continue

            for col in table_df.columns.values:
                if col.isdigit():
                    pass

            table_df.columns = [table_caption.strip() + ' '+ col if col.isdigit() else col for col in table_df.columns.values ]

            print(table_df.columns)
            if not isinstance(table_df.index, pd.MultiIndex):
                # print('true')
                # table_df = table_df.reset_index(level=[0,1])
                # table_df.columns = table_df.columns.droplevel()
                pass

            # print(table_df.shape)
            # search_for = ['→','↑','↓']
            # table_df = table_df[~table_df.apply(lambda r: r.str.contains('|'.join(search_for), case=False).any(), axis=1)]
            # table_df = table_df.replace(r'\[.*\]', '', regex=True)
            # print(table_df.shape)
            # # while os.path.exists("countryjson%s.json" % json_file_no):
            # global json_file_no
            # json_file_no = json_file_no + 1
            # table_df.to_json("countryjson%s.json" % json_file_no, index=False, orient = 'split')

# if "__name__" == "__main__":
scrape_base_wiki_page('https://en.wikipedia.org/wiki/Lists_of_countries_and_territories')
# scrape_wiki_tables()