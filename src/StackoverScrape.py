import pandas as pd
import requests
from bs4 import BeautifulSoup


def href(soup):
    # get all href links from one page 
    href=[]
    for i in soup.find_all("a",class_="question-hyperlink",href=True):
        href.append(i['href'])
    return href


def clean_empty_hrefs(hrefs):
   # remove all empty lists
    list_hrefs=[]
    for i in hrefs:
        if i!=[]:
            list_hrefs.append(i)
    # merge all elemenets in one list
    herfs_list=[]
    for i in list_hrefs:
        for j in i:
            herfs_list.append(j)
    return herfs_list


def add_prefix(herfs_list):
    # rearrage those links who do not have 'https://stackoverflow.com' prefix    
    new_href=[]
    prefix='https://stackoverflow.com'
    for h in herfs_list:
        if 'https' not in h:
            m=prefix+h+"answertab=votes#tab-top"
            new_href.append(m)
        else:
            new_href.append(h+"answertab=votes#tab-top")
    return new_href


def single_page_scraper(url):
    req=requests.get(url=url)
    soup=BeautifulSoup(req.text,"html.parser")
    return soup


def single_page_question_answer(url):
    print(f"{url=}")
    page=single_page_scraper(url).find_all("div", class_="s-prose js-post-body",itemprop="text")
    question = ""
    answer = []
    asked_username = ""
    answered_username = []
    
    user_element = single_page_scraper(url).find_all("div", class_="user-details",itemprop="author")
    user_names = [a.find("a").get_text() for a in user_element]

    for i, div_ele in enumerate(page):
        p_list = [p.get_text() for p in div_ele.findAll("p")]
        if i == 0:
            question = "\n".join(p_list)
            asked_username = user_names[i]
        elif i > 0:
            answer.append("\n".join(p_list))
            answered_username.append(user_names[i])
        if i == 2:
            break

    return question,asked_username, answer, answered_username

import itertools
def questions_answers(keyword, num_question):

    page_len = int(num_question/15) + 1
    soups=[]
    for page in range(page_len):
        req=requests.get(url='https://stackoverflow.com/questions/tagged/{}?tab=votes&page={}&pagesize=15'.format(keyword, page))
        soup=BeautifulSoup(req.text,"html.parser")
        soups.append(soup)
    
    print("Soups are ready!")
    # obtain all href
    hrefs=[]
    for soup in soups:
        hrefs.append(href(soup))
    herfs_list=clean_empty_hrefs(hrefs)
    new_hrefs_list=add_prefix(herfs_list)

    # print(f"{len(new_hrefs_list)=}")

    # new_hrefs_list = new_hrefs_list[:num_question]

    print("All hrefs are ready!")
    # print(f"{len(new_hrefs_list)=}")
    quesitons=[]
    answers=[]
    asked_users = []
    answer_users = []
    urls = []
    for url in new_hrefs_list:
        try:
            q, q_u, a, a_u=single_page_question_answer(url)

            quesitons.append(q)
            answers.append(a)
            asked_users.append(q_u)
            answer_users.append(a_u)
            urls.append(url)
            if len(quesitons) >= num_question:
                break
        except Exception as err:
            # print(repr(err))
            pass
    print("quesitons and answers are ready!")

    
    new_answers=[]
    new_answer_users = []
    for i in range(len(answers)):
        try:
            ans = answers[i][0]
            user = answer_users[i][0]
            new_answers.append(ans)
            new_answer_users.append(user)
        except:
            new_answers.append(None)
            new_answer_users.append(None)

    print("All most done!")
    assert(len(urls) == len(quesitons) == len(asked_users) == len(new_answers) == len(new_answer_users))

    return_value = [
        {
            "url": urls[j],
            "asked_user": asked_users[j].strip(),
            "question": quesitons[j].strip(),
            "answered_user": new_answer_users[j].strip(),
            "answer": new_answers[j].strip()
        } for j in range(len(urls))
    ]

    return return_value



if __name__ == "__main__":
    key = "python"
    entries = 5
    result = questions_answers(key, entries)

