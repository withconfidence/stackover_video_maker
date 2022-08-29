from turtle import title
import pandas as pd
import requests
from bs4 import BeautifulSoup


def href(soup):
    # get all href links from one page 
    href=[]
    for i in soup.find_all("a",class_="s-link",href=True):
        if i['href'].startswith("/questions/"):
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
            m=prefix+h+"answertab=Newest#tab-top"
            new_href.append(m)
        else:
            new_href.append(h+"answertab=Newest#tab-top")
    return new_href


def single_page_scraper(url):
    req=requests.get(url=url)
    soup=BeautifulSoup(req.text,"html.parser")
    return soup


def single_page_question_answer(url):
    page=single_page_scraper(url).find_all("div", class_="s-prose js-post-body",itemprop="text")
    question = ""
    answer = ""
    asked_username = ""
    answered_username = ""
    
    q_title = single_page_scraper(url).find_all("a", class_="question-hyperlink")[0].get_text()
    user_element = single_page_scraper(url).find_all("div", class_="user-details",itemprop="author")
    user_names = [a.find("a").get_text() for a in user_element]

    user_links = ["https://stackoverflow.com" + a.find("a")["href"] for a in user_element]
    # print("user_links: ", user_links)

    for i, div_ele in enumerate(page):
        p_list = [p.get_text() for p in div_ele.find_all(recursive=False)]
        if i == 0:
            question = "\n".join(p_list)
            asked_username = user_names[i]
            asked_userlink = user_links[i]
        elif i > 0:
            answer = "\n".join(p_list)
            answered_username = user_names[i]
            answered_userlink = user_links[i]
            break
        if i == 2:
            break

    return question,asked_username, asked_userlink, answer, answered_username, answered_userlink, q_title

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

    print("All hrefs are ready!")
    # print(f"{len(new_hrefs_list)=}")
    quesitons=[]
    answers=[]
    asked_users = []
    answer_users = []
    urls = []
    titles = []
    asked_users_link = []
    answered_users_link = []
    
    for url in new_hrefs_list:
        try:
            q, q_u, q_u_link, a, a_u, a_u_link, q_title=single_page_question_answer(url)
            print(q_title)

            quesitons.append(q.strip())
            answers.append(a.strip())
            asked_users.append(q_u.strip())
            asked_users_link.append(q_u_link.strip())
            answer_users.append(a_u.strip())
            answered_users_link.append(a_u_link.strip())
            urls.append(url)
            titles.append(q_title)
            print("question num:", len(quesitons), num_question)
            if len(quesitons) >= num_question:
                break
        except Exception as err:
            # print(repr(err))
            pass
    print("quesitons and answers are ready!")

    new_answers=[]
    new_answer_users = []
    new_answer_users_link = []

    key_list = []
    for i in range(len(answers)):
        try:
            ans = answers[i]
            user = answer_users[i]
            user_link = answered_users_link[i]
            new_answers.append(ans)
            new_answer_users.append(user)
            new_answer_users_link.append(user_link)
            key_list.append(keyword)
        except:
            new_answers.append(None)
            new_answer_users.append(None)
            new_answer_users_link.append(None)

    print("All most done!")
    assert(len(urls) == len(quesitons) == len(asked_users) == len(new_answers) == len(new_answer_users) == len(titles))

    df = pd.DataFrame(
        {
            "url": urls,
            "keyword": key_list,
            "title": titles,
            "asked_user": asked_users,
            "asked_user_link": asked_users_link,
            "question": quesitons,
            "answered_user": new_answer_users,
            "answered_user_lnik": new_answer_users_link,
            "answer": new_answers
        }
    )

    df.to_csv("_list_.csv", mode="w", index=True)

    print("csv file successfully created...")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', type=str, default="python", help='keyword to be searched')
    parser.add_argument('entries', type=int, default=1, help='keyword to be searched')

    args = parser.parse_args()
    key = args.keyword
    entries = args.entries

    result = questions_answers(key, entries)

