import json
from bs4 import BeautifulSoup as bs
import requests as rq
import os

def removeBracket(s):          # this func is to remove Bracket "(11/2/2005)" --> 11/02/2005
    s = str(s);
    return s[1:len(s) - 1];

def getRawHTML(url):           # this func get div tag in html that contain, {titlte, publish date, content}
    tmpPage = rq.get(url)
    if tmpPage.status_code == 200:
        tmpHTML = bs(tmpPage.text, "html.parser")
        bodyHTML = tmpHTML.find_all("div", class_="col-md-12 mb-3")
        return str(bodyHTML)
    return "null"

class Data:                   # define a class to store {link, title, date, html}
    def __init__(self, title, link, date, html):
        self.title = title
        self.link = link
        self.date = date
        self.html = html

def AddToDictionary(item):      # item: Data --> add dictionary
    if item is not None:
            data_dicts.append({
                "title": item.title,
                "link": item.link,
                "date": item.date,
                "html": item.html
            })

os.system('clear||cls')          # i hate messy terminal

data_dicts = []                  # Dictionary to convert to json

for i in range(1, 68):  
    url = "https://bachmai.gov.vn/bai-viet-chuyen-mon?p_p_id=com_soft_article_listnew_ListNewByCategoryPortlet_INSTANCE_llxq&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_com_soft_article_listnew_ListNewByCategoryPortlet_INSTANCE_llxq_resetCur=false&_com_soft_article_listnew_ListNewByCategoryPortlet_INSTANCE_llxq_delta=10&_com_soft_article_listnew_ListNewByCategoryPortlet_INSTANCE_llxq_cur=" + str(i)
    currentPage = rq.get(url)
    if currentPage.status_code == 200:
        print("Page" + str(i) + "  --> OK \n");

        htmlContent = bs(currentPage.text, "html.parser")
        titles = htmlContent.find_all("h4")  # get all title of the page, return a list
        dates = htmlContent.find_all("span", class_="post-ago") # get all publish of the article in page, return a list

        for title, date in zip(titles, dates):           # traverse all elements found in titles and date
            a_tag = title.find("a")                   # get the link
            currentHref = "null"
            myRawHTML = "null"
            if a_tag and 'href' in a_tag.attrs:
                currentHref = a_tag["href"]
                myRawHTML = getRawHTML(currentHref)
            myTitle = title.text.strip()
            myDate = removeBracket(date.text.strip())
            # myData[i][j] = Data(myTitle, currentHref, myDate, myRawHTML)
            AddToDictionary(Data(myTitle, currentHref, myDate, myRawHTML));
    else:
        print("Error on page", i)


file_path = 'data.json'

with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_dicts, json_file, indent=4)

print(f"Data has been written to {file_path}")
