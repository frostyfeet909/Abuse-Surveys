# Program to get a random senntance
from requests import get
from bs4 import BeautifulSoup
from re import findall
from random import randint


def get_sentence():
    """
    Returns a random sentance from fungenerators.com
    """
    if randint(0, 9) == 0:
        sentence = "You've been pranked by the prank patrol!"
    else:
        html = get('https://fungenerators.com/random/sentence')
        soup = BeautifulSoup(html.text, "lxml")
        text = str(soup.find_all("h2")[0])
        sentence = findall('>(.*)<', text)[0]

    return sentence
