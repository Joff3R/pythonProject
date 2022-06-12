import requests
from bs4 import BeautifulSoup
import re
import string
from collections import Counter
import matplotlib.pyplot as plt
import csv

http = "https://"

user_url = input("Enter URL: ")
if http not in user_url:
    user_url = http + user_url

user_number_of_words = int(input("Enter number of words: "))
counter = user_number_of_words

req = requests.get(user_url)
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

# split() domyslnie dzieli tekst na liste rozdzielajac po spacji
page_words = page_text.split()

# usuwa znaki interpunkcyjne i zamienia litery na male
page_words2 = [w.strip(string.punctuation).lower() for w in page_words if
               len(w.strip(string.punctuation)) > 0]

# najpopularnoiejsze  slowa:
page_word_freq = Counter(page_words2).most_common()

dict_page_word_freq = {}
for i in page_word_freq:
    dict_page_word_freq[i[0]] = i[1]

# usuwanie stopwords
stop_words_file = open("polish.stopwords.txt", "r")
content = stop_words_file.read()
content_list = content.split()

for word in content_list:
    try:
        del dict_page_word_freq[word]
    except:
        pass

plik = open("words.csv", "w")
for key, value in dict_page_word_freq.items():
    plik.write('%s;%s\n' % (key, value))
    plik.flush()
plik.close()

Words = []
Values = []

with open('words.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=';')

    for row in lines:
        Words.append(row[0])
        Values.append(int(row[1]))
        counter -= 1
        if counter == 0:
            break

plt.scatter(Words, Values, color='g', s=100)
plt.xticks(rotation=25)
plt.xlabel('Words')
plt.ylabel('Count')
plt.title('TOP ' + str(user_number_of_words) + " words in " + user_url, fontsize=20)

plt.show()
