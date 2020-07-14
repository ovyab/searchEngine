# Assignment 3 Indexer

from pathlib import Path
import nltk, json, os, sys, requests, re
from bs4 import BeautifulSoup

index = {}
files = []

def extractFileContent(f):
    try:
        file = open(f,'r')
        files.append(file)
        data = json.load(file)
        content = data["content"]
        soup = BeautifulSoup(content, "html.parser")
        return soup
    except:
        return ''

def getFilePaths():
    global files
    directory = '/Users/ovyabarani/Desktop/assignment3/ANALYST'
    paths = Path(directory).glob('**/*.json')
    pathlist = map(str, paths)
    return list(pathlist)

def tokenize(content, file):
    ''' any regular tokens '''
    try:
        splittext = nltk.word_tokenize(content.get_text())
        wordsonly = [word.lower() for word in splittext if (word.isalpha() and len(word) > 1)]
        wordcounts = {}
        for word in wordsonly:
            if word in wordcounts:
                wordcounts[word][0] += 1
            else:
                wordcounts[word] = [1,0]
        
        wordcounts = findSpecialWords(wordcounts, content)
        return wordcounts
    except:
        return []

def stripTags(words:list):
    validWords = []
    for match in words:
        strippedHeading = match.get_text().lower()
        words = nltk.word_tokenize(strippedHeading)
        validWords = validWords + [word for word in words if word.isalpha()]
    return validWords

def findSpecialWords(wordcounts, content):
    ''' page titles '''
    title = content.find_all('title')
    formattedTitle = stripTags(title)
    for word in formattedTitle:
        if word in wordcounts:
            wordcounts[word][1] += 15

    ''' h1-h2 '''
    headingsBig = content.find_all(re.compile('^h[1-2]$'))
    validHeadingsBig = stripTags(headingsBig)

    for heading in validHeadingsBig:
        if heading in wordcounts:
            wordcounts[heading][1] += 10

    ''' h3-h6 '''
    headingsSmall = content.find_all(re.compile('^h[3-6]$'))
    validHeadingsSmall = stripTags(headingsSmall)

    for heading in validHeadingsSmall:
        if heading in wordcounts:
            wordcounts[heading][1] += 5

    ''' bolded words '''
    bold = content.find_all(['b', 'strong'])
    validBold = stripTags(bold)

    for bolded in validBold:
        if bolded in wordcounts:
            wordcounts[bolded][1] += 1

    return wordcounts

def updateIndex(filepath, content, tokens):
    global index, files
    print(f'updating index for {str(filepath)}')
    docID = files.index(filepath)
    for key in tokens:
        if key in index:
            index[key].append((docID, tokens[key][0], tokens[key][1]))
        else:
            index[key] = [(docID, tokens[key][0], tokens[key][1])]

def update():
    with open('indexjson.json', 'w') as n:
        data = {}
        for key in index:
            data[key] = index[key]
        json.dump(data, n)
    
        print(f'number of documents: {len(files)}')
        print(f'number of unique tokens: {len(index)}')
        size = int(os.path.getsize('indexjson.json'))/1000
        print(f'size of index: {size} kb')
    n.close()

def main():
    global files
    files = getFilePaths()
    for file in files:
        content = extractFileContent(file)
        updateIndex(file, content, tokenize(content, file))
    update()

if __name__ == "__main__":
    main()