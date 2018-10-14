import requests
import re
from bs4 import BeautifulSoup


# Given URL, create request and get HTML contents
# if its a file and not a URL, try reading file contents before returning None
def readURL(url):
    try:
        page = requests.get(url)
        if page:
            return page.text
        else:
            return None
    except:  # Assume its a file and try to read it
        try:
            with open(url, 'r') as myfile:
                data = myfile.read()
            return data
        except:
            return None


# Given HTML, create and return BeautifulSoup object
def html2Soup(htmlContent):
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup


# Remove double or single quotes from text
def remove_quotes(text):
    return text.replace("'", '').replace('"', '')


# Given bs4.element.Tag, get and clean the text
def getTagText(tag):
    if tag:
        text = tag.get_text().strip()
        return remove_quotes(text)
    else:
        return 'Empty'


# Given a non-null string which != 'Empty' convert it to int
def getInt(str):
    str = str.replace(',', '').replace('.', '')
    return int(str) if str is not 'Empty' else 0


# Given a non-null string which != 'Empty' convert it to float
def getFloat(str):
    str = str.replace(',', '')
    return float(str) if str is not 'Empty' else 0.0


# Test
# print(readURL('http://www.imdb.com/search/title?count=100&countries=us&languages=en&production_status=released&release_date=2013,2016-12&sort=year,asc&title_type=feature'))
# print(remove_quotes('abcd "efgh" ijkl'))
# print(remove_quotes('"abcd"_123'))
# print(remove_quotes('$1,500,500.5M'))
# print(remove_quotes("abcd'efg'asd"))
# print(getInt("1,000."))
# print(getFloat("1,0,0,0.00"))
