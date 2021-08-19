from bs4 import BeautifulSoup
import pandas as pd
import requests
from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Create your views here.

def home(request):
    return render(request, 'home.html')

def get_soup(url):
    r = requests.get("http://localhost:8050/render.html", params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviewlist = []
    reviews = soup.find_all('div', {'data-hook': 'review'})
    for item in reviews:
        review = item.find('span', {'data-hook': 'review-body'}).text.strip()
        reviewlist.append(review)
    return reviewlist

def Reviews(url):
    soup = get_soup(url)
    reviewlist = get_reviews(soup)
    finalReviewList = str(reviewlist).replace('\n', '\n\n')
    return reviewlist

def get_summary():

   
# Input text - to summarize 
    text = """ """
   
# Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
   
# Creating a frequency table to keep the 
# score of each word
   
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
   
# Creating a dictionary to keep the score
# of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()
   
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq 
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
   
# Average value of a sentence from the original text
   
    average = int(sumValues / len(sentenceValue))
   
# Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    return summary

def store(request):
    url = request.GET['usrCode']
    reviewsList = Reviews(url)
    reviewsDataset = []
    for r in reviewsList:
        r = str(r).replace('Your browser does not support HTML5 video.', '').replace('xa0', '').replace("',", '",')
        reviewsDataset.append(r)
    reviewsDisplay = str(reviewsList).replace('[','').replace(']', '').replace('Read more', '').replace('Your browser does not support HTML5 video.', '').replace('xa0', '').replace("',", '",').replace('",', '"\n\n')
    summary = get_summary()
    df = pd.read_csv("dataset3.csv")
    dfTemp = pd.DataFrame([[reviewsDataset, summary]], columns=['Review', 'Summary'])
    dfFinal = df.append(dfTemp, ignore_index=True)
    dfFinal.to_csv('dataset3.csv', index=False)
    return render(request, 'home.html', {'summary' : summary, 'userCode' : url, 'reviews': reviewsDisplay})





