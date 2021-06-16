from bs4 import BeautifulSoup, BeautifulStoneSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk import text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
# Create your views here.

def home(request):
    return render(request, 'home.html')


def runAlgo(userCode):
    

    finalReviewList = []
    reviewlist = []


    def get_soup(url):
        r = requests.get("http://localhost:8050/render.html", params={'url': url, 'wait': 2})
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup


    def get_reviews(soup):
        reviews = soup.find_all('div', {'data-hook': 'review'})
        for item in reviews:
            review = item.find('span', {'data-hook': 'review-body'}).text.strip()
            reviewlist.append(review)
        return reviewlist


    soup = get_soup(userCode)
    reviews = get_reviews(soup)

    for review in reviews:
        finalReviewList.append(str(review).replace('(', '').replace(')', '').replace(',', '').replace('"', ''))

    return finalReviewList


def store(request):
    userCode = request.GET['usrCode']
    summary = runAlgo(userCode)
    df = pd.read_csv('dataset3.csv')
    dfTemp = pd.DataFrame([[userCode, summary]], columns=['Code', 'Summary'])
    dfFinal = df.append(dfTemp, ignore_index=True)
    dfFinal.to_csv('dataset3.csv', index=False)
    return render(request, 'home.html', {'summary' : summary, 'userCode' : userCode})





