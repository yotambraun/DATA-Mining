# ----------------------------------------------------------------------------------------------
# Yotam Braun - 309914646
# Shira  Rothmann - 208309245
# 15001 items - 300 pages; time to crawl page: 1294.94 seconds
# ----------------------------------------------------------------------------------------------
import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
import time
from warnings import warn
import numpy as np
import json
from collections import OrderedDict
import re


RECORDS_KEY = 'records'
PAGE_KEY = '{}'
url = "https://www.imdb.com/search/title/?genres=comedy&" + \
      "explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f" \
      "-4fac-8694-c56ce6f490fe&pf_rd_r=S2Q84XF0Q1KP5G59NZE8&pf_rd_s=center-1" \
      "&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"

start_time =time.time()

def crawl_imdb ( ):
    global start_time
    save_dict = OrderedDict() # dict to accumulate all the data.
    final_dict = {RECORDS_KEY:  save_dict}

    items = 0
    number_of_page = 0
    pages = np.arange(1, 15051, 50)

    is_new_page = True
    for page in pages:
        if not is_new_page:
            is_new_page = True
        #page = i+1
        # page_num = page + 1
        print('now crawling search result page num', page, end='')


        # get request
        response = get("https://www.imdb.com/search/title/?genres=comedy&"
                       + "start="
                       + str(page)
                       + "&explore=title_type,genres&ref_=adv_nxt")
        # wait between search result requests

        sleep(2)


        page_url = url.format(page)

        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests,
                                                       response.status_code))

        # parse the content of current iteration of request
        # parse page html
        page_html = BeautifulSoup(response.text, 'html.parser')

        movie_of_containers = page_html.find_all('div',
                                              class_='lister-item '
                                                     'mode-advanced')
        single_record_list_imdb = ["record: {}".format(items)]


        # extract data itemwise
        # iterate movie in search result page.
        for item_id, container in enumerate(movie_of_containers):
            #try with out of range of index error
            try:
                # save desired data.


                single_record_list_imdb.append(OrderedDict({"id": items,
                                                            "url": "https://www.imdb.com/search/title/?genres=comedy&"
                       + "start="
                       + str(page)
                       + "&explore=title_type,genres&ref_=adv_nxt",
                                                            'movie/TV Shows': container.h3.a.text ,
                                                            'year': container.h3.find('span',
                                         class_='lister-item-year text-muted '
                                                'unbold').text.replace("\{0-9}","").replace("(","").replace(")",""),
                                                            'MovieRating': container.p.find('span', class_='certificate').text if container.p.find('span', class_='certificate') is not None else "-",
                                                            'Genres': container.p.find('span', class_='genre').text.replace("\n","") if container.p.find('span', class_='genre') is not None else "-",
                                                            'Length': container.p.find('span',
                                        class_='runtime').text if container.p.find(
                    'span', class_='runtime') is not None else "-",
                                                            'IMDBRating': float(container.strong.text) if container.strong is not None else "-",
                                                            'metascore': container.find('span',
                                         class_='metascore').text if container.find(
                    'span', class_='metascore') is not None else "-",
                                                            'NumberOfVotes': container.find('span', attrs={'name': 'nv'})['data-value'] if container.find('span', attrs={'name': 'nv'}) is not None else "-",
                                                            "Director": str(container.find('p',class_='').find_all('a')[0].text) if container.find('p',class_='').find_all('a') is not None else "-",
                                                            "Stars": [actor.text for actor in container.find('p',class_='').findAll('a')[1:]] if container.find('p',class_='').find_all('a')[1:] is not None else "-",
                                                            "Gross":
                                                                container
                                                           .find_all(
                                                                    "span",
                                                                    attrs={
                                                                        'name': 'nv'})[
                                                                    1].text if len(
                                                                    container.find_all(
                                                                        'span',
                                                                        attrs={
                                                                            'name': 'nv'})) > 1 else "-",
                                                            "FullText": container.find_all('p', class_='text-muted')[-1].text.strip() if container.find_all('p', class_='text-muted')[-1] is not None else "-"}))

                items += 1
                #is_new_page=False
            except (IndexError):
                pass
                continue


        save_dict[PAGE_KEY.format(items)] = single_record_list_imdb
        end_time =time.time()
        print('; time to crawl page: {0:.2f} seconds'.format(end_time -start_time))
        number_of_page+=1
    print("number of the items {} and the number of page that we scan is {}".format(str(items),number_of_page))

    return final_dict

crawl_the_imdb = crawl_imdb()
with open('crawl_firstmovies.json', 'w', encoding="utf-8") as final:
    json.dump(crawl_the_imdb , final, indent=4,ensure_ascii=False)



