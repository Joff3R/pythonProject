import requests
from bs4 import BeautifulSoup
import re
import string
from collections import Counter

req = requests.get("http://wp.pl")
# req = requests.get("http://tvn24.pl")
soup = BeautifulSoup(req.text, 'html.parser')


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


page_text_list = []
for t in filter(visible, soup.findAll(text=True)):
    page_text_list.append(t)

# laczy wszystkie elementy listy w jeden string
page_text = " ".join(page_text_list)
# print(page_text[:80])

# split() domyslnie dzieli tekst na liste rozdzielajac po spacji
page_words = page_text.split()
# print(len(page_words), page_words[:10])

# usuwa znaki interpunkcyjne i zamienia litery na male


page_words2 = [w.strip(string.punctuation).lower() for w in page_words if
               len(w.strip(string.punctuation)) > 0]
# print(len(page_words2), page_words2[:10])

#najpopularnoiejsze  slowa:
page_word_freq=Counter(page_words2).most_common()
# print(page_word_freq[:15])

dict_page_word_freq = {}
for i in page_word_freq:
    dict_page_word_freq[i[0]]=i[1]

#usuwanie stopwords

# listaSlow=['na','w','się','do','o','dla','nie','to','jak','już','z','są','']
# for slowo in listaSlow:
#     try:
#         del dict_page_word_freq[slowo]
#     except:
#         print("nie znaleziono stopwords", slowo)

print("DIC: ********")
print(dict_page_word_freq)
print("LIST: ********")
print(page_word_freq)
print("LIST: number")
print(page_word_freq[0])
firstElement = page_word_freq[0]
print(firstElement[0])
print(firstElement[1])

# plik=open("slowa.csv","w",encoding="utf8")
# for element in page_word_freq:
#     plik.write(element[0]+";"+str(element[1])+"\n")
#     plik.flush()
#     # print(element[0])
#     # print(element[1])
#
# plik.close()
