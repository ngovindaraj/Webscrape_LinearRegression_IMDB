'''
Unfortunately, each IMDB results page does not have
all the information we need. So we need to visit
individual movie page to get the following fields:
- Budget             - Int
- Production Company - Enum
- Release Date       - Date/Time
- Writer             - Enum
'''

import re
from utils import readURL, html2Soup, getTagText


# Get the 2nd writier for a movie if one exists
def get_second_writer(mv):
    try:
        return mv.find_all('a', href=re.compile('tt_ov_wr'))[1]
    except IndexError:
        return None


def get_budget(mv):
    try:
        return mv.find(text=re.compile("Budget:")).next.strip()
    except:
        return 'Empty'


def get_release_dt(mv):
    try:
        return ' '.join(
            mv.find(text=re.compile("Release Date:")).next.split()[:3])
    except:
        return 'Empty'


def process_one_movie_url(url):
    url = 'http://www.imdb.com' + url
    html = readURL(url)
    if html is None:
        return None, None, None, None
    else:
        movie_section = html2Soup(html).find(id="pagecontent")
        mv = movie_section.select(".flatland")[0]
        budget = get_budget(mv)
        release_dt = get_release_dt(mv)
        writer1 = getTagText(mv.find('a', href=re.compile('tt_ov_wr')))
        writer2 = getTagText(get_second_writer(mv))
        return budget, release_dt, writer1, writer2


# Test
# budget, release_dt, writer1, writer2 = process_one_movie_url(
#     '/Users/navina/Desktop/movie.html')
# print("Budget: {}".format(budget))
# print("Release Date: {}".format(release_dt))
# print("Writer1: {}".format(writer1))
# print("Writer2: {}".format(writer2))
