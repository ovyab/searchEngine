# Assignment 3 - Retriever

from indexer import getFilePaths
import math, json, requests, os
import tkinter as tk
from bs4 import BeautifulSoup

index = {}
files = []
N = 0

def initialize():
    global index, files, N
    files = getFilePaths()
    N = len(files)
    with open('indexjson.json') as f:
        index = json.load(f)

def formatQuery(query):
    lower = query.lower()
    return lower.split()

def search(query):
    q = formatQuery(query)
    docs, validWords = gatherDocs(q)
    if len(docs) == 0:
        return []
    else:
        scores = rankResults(docs, validWords)
        return returnResults(scores, query)

def gatherDocs(words):
    ''' gathers all the documents where all of the words are found '''
    global index
    allDocs = []
    commonDocs = []
    validWords = []
    for word in words:
        if word not in index:
            continue
        else:
            validWords.append(word)
            docs = [i[0] for i in index[word]]
            allDocs.append(docs)
    if len(validWords) < 1: return [], []
    if len(words) > 1:
        for sublist in allDocs:
            commonDocs = list(set(allDocs[0]).intersection(sublist))
    else:
        commonDocs = allDocs[0]
    return commonDocs, validWords

def rankResults(docs, query):
    length = len(docs)
    allScores = {}
    for doc in docs:
        allScores[doc] = calculateScore(doc, query, length)
    return allScores

def calculateScore(doc, query, length):
    global index, N
    tf = 0
    idf = length

    ''' calculate total term frequency '''
    for word in query:
        matches = index[word]
        for match in matches:
            if match[0] == doc:
                tf += match[1]
                numSpecial = match[2]
                break

    ''' calculate tf idf score '''
    tfidf = (1+math.log(tf) * math.log(N/idf))

    ''' factor in weight of headings/bolded words '''
    return tfidf * numSpecial 
    
def getPageTitle(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.title.string

def returnResults(scores, query):
    rankedScores = [v for v in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
    results = []
    if len(rankedScores) == 0:
        return []
    for score in rankedScores:
        url = getURL(score[0])
        removedFragmentURL = url.split('#')
        if removedFragmentURL[0] not in results:
            results.append(removedFragmentURL[0])
    return results

def getURL(docID):
    global files
    file = files[docID]
    with open(file) as f:
        content = json.load(f)
        url = content["url"]
    f.close()
    return url
